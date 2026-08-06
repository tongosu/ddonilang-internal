use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::Path;

use ddonirang_lang::connect_endpoint_relation_seum_rows;
use serde_json::{json, Value as JsonValue};
use sha2::{Digest, Sha256};

use crate::lang::ast::{ArgBinding, Assertion, Binding, Expr, Program, Stmt};

const SCHEMA: &str = "ddn.solveplan.v1";
const BUNDLE_SCHEMA: &str = "ddn.solveplan.bundle.v1";
const MAX_S1_UNKNOWNS: usize = 8;

#[derive(Clone, Debug)]
struct RelationRow {
    id: String,
    source_order: usize,
    text: String,
    lhs: String,
    rhs: String,
    defines: Option<String>,
    depends_on: Vec<String>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum IntegratorMethod {
    Euler,
    SemiImplicitEuler,
}

impl IntegratorMethod {
    fn from_source(source: &str) -> Self {
        if source.contains("적분.반암시적오일러") || source.contains("반암시적오일러")
        {
            Self::SemiImplicitEuler
        } else {
            Self::Euler
        }
    }

    fn solveplan_method(self) -> &'static str {
        match self {
            Self::Euler => "ode_explicit_euler_v1",
            Self::SemiImplicitEuler => "ode_semi_implicit_euler_v1",
        }
    }

    fn surface(self) -> &'static str {
        match self {
            Self::Euler => "적분.오일러",
            Self::SemiImplicitEuler => "적분.반암시적오일러",
        }
    }
}

pub fn write_solveplan_out(path: &Path, program: &Program, source: &str) -> Result<(), String> {
    let method = IntegratorMethod::from_source(source);
    let mut plans = collect_assertion_exprs(program)
        .into_iter()
        .map(|expr| build_solveplan_for_assertion_expr(expr, method))
        .collect::<Vec<_>>();
    plans.extend(collect_connect_desugar_plans(source, method));
    let payload = match plans.as_slice() {
        [single] => single.clone(),
        _ => json!({
            "schema": BUNDLE_SCHEMA,
            "plans": plans,
        }),
    };
    write_json(path, &payload)
}

pub fn write_connect_diagnostic_out_if_any(path: &Path, source: &str) -> Result<bool, String> {
    let plans = collect_connect_desugar_plans(source, IntegratorMethod::from_source(source))
        .into_iter()
        .filter(|plan| {
            plan.get("diagnostics")
                .and_then(JsonValue::as_array)
                .is_some_and(|diagnostics| !diagnostics.is_empty())
        })
        .collect::<Vec<_>>();
    if plans.is_empty() {
        return Ok(false);
    }
    let payload = match plans.as_slice() {
        [single] => single.clone(),
        _ => json!({
            "schema": BUNDLE_SCHEMA,
            "plans": plans,
        }),
    };
    write_json(path, &payload)?;
    Ok(true)
}

#[derive(Clone, Copy)]
struct AssertionExpr<'a> {
    assertion: &'a Assertion,
    context: AssertionContext,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum AssertionContext {
    Runtime,
    Init,
}

fn collect_assertion_exprs(program: &Program) -> Vec<AssertionExpr<'_>> {
    let mut out = Vec::new();
    collect_assertions_from_stmts(&program.stmts, &mut out);
    out
}

fn collect_connect_desugar_plans(
    source: &str,
    _integrator_method: IntegratorMethod,
) -> Vec<JsonValue> {
    source
        .replace("\r\n", "\n")
        .replace('\r', "\n")
        .lines()
        .map(|line| line.trim().trim_start_matches('\u{feff}').trim())
        .filter(|line| line.contains("잇기"))
        .map(|line| {
            if let Some((code, message)) = connect_diagnostic_for_surface(line) {
                return connect_diagnostic_plan(line, code, &message);
            }
            let Some(rows) = connect_endpoint_relation_seum_rows(line) else {
                return connect_diagnostic_plan(
                    line,
                    "E_CONNECT_UNSUPPORTED_RULE",
                    "connect surface cannot lower to seum rows",
                );
            };
            connect_desugar_plan(line, &rows)
        })
        .collect()
}

fn connect_diagnostic_for_surface(surface: &str) -> Option<(&'static str, String)> {
    let rhs = surface
        .trim()
        .trim_end_matches('.')
        .split_once("<-")
        .map(|(_, expr)| expr.trim())
        .unwrap_or_else(|| surface.trim().trim_end_matches('.'));
    let (endpoints_part, rest) = rhs.split_once("을 (").or_else(|| rhs.split_once("를 ("))?;
    let endpoints = split_connect_endpoint_names(endpoints_part)?;
    if endpoints.iter().any(|endpoint| !endpoint.contains('.')) {
        return Some((
            "E_CONNECT_NO_PORT",
            "connect endpoint must name an object and port".to_string(),
        ));
    }
    let inner = rest.split_once(") 잇기").map(|(inner, _)| inner)?;
    let mut channel_rules = BTreeMap::new();
    for sentence in inner.split(',').map(str::trim).filter(|it| !it.is_empty()) {
        let Some((channel, rule)) = parse_connect_inner_sentence(sentence) else {
            return Some((
                "E_CONNECT_UNSUPPORTED_RULE",
                format!("unsupported connect inner sentence: {sentence}"),
            ));
        };
        if let Some(previous) = channel_rules.insert(channel.to_string(), rule) {
            if previous != rule {
                return Some((
                    "E_CONNECT_CHANNEL_MISMATCH",
                    format!("conflicting connect rules for channel: {channel}"),
                ));
            }
        }
    }
    None
}

fn split_connect_endpoint_names(input: &str) -> Option<[String; 2]> {
    let (left, right) = input
        .split_once("과 ")
        .or_else(|| input.split_once("와 "))
        .or_else(|| input.split_once("과"))
        .or_else(|| input.split_once("와"))?;
    Some([left.trim().to_string(), right.trim().to_string()])
}

fn parse_connect_inner_sentence(sentence: &str) -> Option<(&str, &'static str)> {
    if sentence.contains("실리게") || sentence.contains("거슬러 흐르게") {
        return None;
    }
    let (channel, rest) = sentence
        .split_once("은 ")
        .or_else(|| sentence.split_once("는 "))
        .or_else(|| sentence.split_once("가 "))
        .or_else(|| sentence.split_once('은'))
        .or_else(|| sentence.split_once('는'))
        .or_else(|| sentence.split_once('가'))?;
    let rule = if rest.contains("같게") {
        "equality"
    } else if rest.contains("흐르게") {
        "flow"
    } else {
        return None;
    };
    Some((channel.trim(), rule))
}

fn collect_assertions_from_stmts<'a>(stmts: &'a [Stmt], out: &mut Vec<AssertionExpr<'a>>) {
    for stmt in stmts {
        match stmt {
            Stmt::DeclBlock {
                items,
                init_assertions,
                ..
            } => {
                for assertion in init_assertions {
                    out.push(AssertionExpr {
                        assertion,
                        context: AssertionContext::Init,
                    });
                }
                for item in items {
                    if let Some(expr) = item.value.as_ref() {
                        collect_assertions_from_expr(expr, out);
                    }
                    if let Some(maegim) = item.maegim.as_ref() {
                        collect_assertions_from_bindings(&maegim.fields, out);
                    }
                }
            }
            Stmt::SeedDef { body, .. }
            | Stmt::Receive { body, .. }
            | Stmt::Hook { body, .. }
            | Stmt::HookWhenBecomes { body, .. }
            | Stmt::HookWhile { body, .. }
            | Stmt::OpenBlock { body, .. }
            | Stmt::BeatBlock { body, .. }
            | Stmt::LifecycleBlock { body, .. }
            | Stmt::Repeat { body, .. }
            | Stmt::While { body, .. }
            | Stmt::ForEach { body, .. }
            | Stmt::Quantifier { body, .. } => collect_assertions_from_stmts(body, out),
            Stmt::Assign { value, .. }
            | Stmt::FlowAssign { value, .. }
            | Stmt::Expr { value, .. }
            | Stmt::Return { value, .. }
            | Stmt::Show { value, .. }
            | Stmt::Inspect { value, .. } => collect_assertions_from_expr(value, out),
            Stmt::Send {
                sender,
                payload,
                receiver,
                ..
            } => {
                if let Some(sender) = sender {
                    collect_assertions_from_expr(sender, out);
                }
                collect_assertions_from_expr(payload, out);
                collect_assertions_from_expr(receiver, out);
            }
            Stmt::If {
                condition,
                then_body,
                else_body,
                ..
            } => {
                collect_assertions_from_expr(condition, out);
                collect_assertions_from_stmts(then_body, out);
                if let Some(else_body) = else_body {
                    collect_assertions_from_stmts(else_body, out);
                }
            }
            Stmt::Choose {
                branches,
                else_body,
                ..
            } => {
                for branch in branches {
                    collect_assertions_from_expr(&branch.condition, out);
                    collect_assertions_from_stmts(&branch.body, out);
                }
                if let Some(else_body) = else_body {
                    collect_assertions_from_stmts(else_body, out);
                }
            }
            Stmt::Contract {
                condition,
                then_body,
                else_body,
                ..
            } => {
                collect_assertions_from_expr(condition, out);
                if let Some(then_body) = then_body {
                    collect_assertions_from_stmts(then_body, out);
                }
                collect_assertions_from_stmts(else_body, out);
            }
            Stmt::Boim { entries, .. } => collect_assertions_from_bindings(entries, out),
            Stmt::ImportBlock { .. }
            | Stmt::ExportBlock { .. }
            | Stmt::BogaeDraw { .. }
            | Stmt::Break { .. }
            | Stmt::ContinueLoop { .. }
            | Stmt::Pragma { .. } => {}
        }
    }
}

fn collect_assertions_from_bindings<'a>(bindings: &'a [Binding], out: &mut Vec<AssertionExpr<'a>>) {
    for binding in bindings {
        collect_assertions_from_expr(&binding.value, out);
    }
}

fn collect_assertions_from_args<'a>(args: &'a [ArgBinding], out: &mut Vec<AssertionExpr<'a>>) {
    for arg in args {
        collect_assertions_from_expr(&arg.expr, out);
    }
}

fn collect_assertions_from_expr<'a>(expr: &'a Expr, out: &mut Vec<AssertionExpr<'a>>) {
    match expr {
        Expr::Assertion { assertion, .. } => out.push(AssertionExpr {
            assertion,
            context: AssertionContext::Runtime,
        }),
        Expr::Unary { expr, .. } => collect_assertions_from_expr(expr, out),
        Expr::Binary { left, right, .. } => {
            collect_assertions_from_expr(left, out);
            collect_assertions_from_expr(right, out);
        }
        Expr::SeedLiteral { body, .. } => collect_assertions_from_expr(body, out),
        Expr::Call { args, .. } => collect_assertions_from_args(args, out),
        Expr::FieldAccess { target, .. } => collect_assertions_from_expr(target, out),
        Expr::TemplateFill {
            template, bindings, ..
        } => {
            collect_assertions_from_expr(template, out);
            collect_assertions_from_bindings(bindings, out);
        }
        Expr::Pack { bindings, .. } => collect_assertions_from_bindings(bindings, out),
        Expr::FormulaFill {
            formula, bindings, ..
        } => {
            collect_assertions_from_expr(formula, out);
            collect_assertions_from_bindings(bindings, out);
        }
        Expr::Literal(_, _)
        | Expr::Path(_)
        | Expr::Atom { .. }
        | Expr::Formula { .. }
        | Expr::FormulaEval { .. }
        | Expr::Template { .. } => {}
    }
}

fn build_solveplan_for_assertion_expr(
    expr: AssertionExpr<'_>,
    integrator_method: IntegratorMethod,
) -> JsonValue {
    let plan = build_solveplan_for_assertion(&expr.assertion.body_source, integrator_method);
    match expr.context {
        AssertionContext::Runtime => plan,
        AssertionContext::Init => init_plan_from_base(&expr.assertion.body_source, plan),
    }
}

fn init_plan_from_base(body_source: &str, mut plan: JsonValue) -> JsonValue {
    let stage = plan
        .get("stage")
        .and_then(JsonValue::as_str)
        .unwrap_or("S3");
    if matches!(stage, "S0" | "S1") {
        if let Some(object) = plan.as_object_mut() {
            object.insert("init_plan".to_string(), init_plan_marker());
        }
        return plan;
    }

    let rows = parse_relation_rows(body_source);
    let unknowns = collect_unknowns(&rows);
    let mut unsupported = diagnostic_plan(
        body_source,
        "S3",
        "init_unsupported_v1",
        &rows,
        unknowns,
        "E_INIT_UNSUPPORTED",
        "채비 안 세움 초기화는 S0/S1 SolvePlan만 허용합니다",
    );
    if let Some(object) = unsupported.as_object_mut() {
        object.insert("init_plan".to_string(), init_plan_marker());
    }
    unsupported
}

fn init_plan_marker() -> JsonValue {
    json!({
        "kind": "t0_one_shot",
        "source": "chaebi_inner_seum",
        "apply": "before_madi_0",
        "allowed_stages": [
            "S0",
            "S1"
        ]
    })
}

fn build_solveplan_for_assertion(
    body_source: &str,
    integrator_method: IntegratorMethod,
) -> JsonValue {
    let rows = parse_relation_rows(body_source);
    if rows.is_empty() {
        return unsupported_plan(
            body_source,
            Vec::new(),
            "E_SEUM_UNSUPPORTED",
            "no relation rows",
        );
    }
    if rows.iter().any(|row| derivative_slot(&row.lhs).is_some()) {
        return s2_plan(body_source, &rows, integrator_method);
    }
    let unknowns = collect_unknowns(&rows);
    if unknowns.len() > MAX_S1_UNKNOWNS {
        return unsupported_plan(
            body_source,
            unknowns,
            "E_SEUM_UNSUPPORTED",
            "S1 linear SolvePlan supports at most 8 unknowns",
        );
    }
    if let Some(conflict) = find_assign_conflict(&rows) {
        return diagnostic_plan(
            body_source,
            "S3",
            "unsupported_deferred_v1",
            &rows,
            unknowns,
            "E_SEUM_ASSIGN_CONFLICT",
            &format!("duplicate definition: {conflict}"),
        );
    }
    if rows.iter().all(|row| row.defines.is_some()) {
        match causal_order(&rows) {
            Ok(order) => return s0_plan(body_source, &rows, unknowns, order),
            Err(code) => {
                return diagnostic_plan(
                    body_source,
                    "S3",
                    "unsupported_deferred_v1",
                    &rows,
                    unknowns,
                    code,
                    "cyclic or unsupported explicit algebra",
                )
            }
        }
    }
    if rows.len() < unknowns.len() {
        return diagnostic_plan(
            body_source,
            "S3",
            "unsupported_deferred_v1",
            &rows,
            unknowns,
            "E_SEUM_UNDERDETERMINED",
            "S1 linear SolvePlan has fewer relations than unknowns",
        );
    }
    if rows.len() > unknowns.len() {
        return diagnostic_plan(
            body_source,
            "S3",
            "unsupported_deferred_v1",
            &rows,
            unknowns,
            "E_SEUM_OVERDETERMINED",
            "S1 linear SolvePlan has more relations than unknowns",
        );
    }
    s1_plan(body_source, &rows, unknowns)
}

fn parse_relation_rows(body_source: &str) -> Vec<RelationRow> {
    split_relation_statements(body_source)
        .into_iter()
        .enumerate()
        .filter_map(|(idx, line)| parse_relation_row(idx, &line))
        .collect()
}

fn split_relation_statements(body_source: &str) -> Vec<String> {
    let normalized = body_source.replace("\r\n", "\n").replace('\r', "\n");
    let mut out = Vec::new();
    let mut start = 0usize;
    for (idx, ch) in normalized.char_indices() {
        let split_here = if ch == '.' {
            normalized[idx + ch.len_utf8()..]
                .chars()
                .next()
                .map(|next| next.is_whitespace())
                .unwrap_or(true)
        } else {
            ch == '\n'
        };
        if split_here {
            let line = normalized[start..idx].trim();
            if !line.is_empty() {
                out.push(line.to_string());
            }
            start = idx + ch.len_utf8();
        }
    }
    let line = normalized[start..].trim().trim_end_matches('.').trim();
    if !line.is_empty() {
        out.push(line.to_string());
    }
    out
}

fn parse_relation_row(idx: usize, line: &str) -> Option<RelationRow> {
    let (lhs, rhs) = line.split_once("=:= ").or_else(|| line.split_once("=:="))?;
    let lhs = lhs.trim().to_string();
    let rhs = rhs.trim().to_string();
    let defines = is_simple_symbol(&lhs).then(|| lhs.clone());
    let define_set = defines.iter().cloned().collect::<BTreeSet<_>>();
    let depends_on = tokens_from_expr(&rhs)
        .into_iter()
        .filter(|token| !define_set.contains(token))
        .collect::<Vec<_>>();
    Some(RelationRow {
        id: format!("r{}", idx + 1),
        source_order: idx,
        text: format!("{lhs} =:= {rhs}"),
        lhs,
        rhs,
        defines,
        depends_on,
    })
}

fn derivative_slot(symbol: &str) -> Option<(String, usize)> {
    let apostrophes = symbol.chars().rev().take_while(|ch| *ch == '\'').count();
    if apostrophes == 0 || apostrophes > 2 {
        return None;
    }
    let base_len = symbol.len().checked_sub(apostrophes)?;
    let base = symbol[..base_len].trim();
    if base.is_empty() || !is_simple_symbol(base) {
        return None;
    }
    Some((base.to_string(), apostrophes))
}

fn is_simple_symbol(text: &str) -> bool {
    let mut chars = text.chars();
    let Some(first) = chars.next() else {
        return false;
    };
    if first.is_ascii_digit() {
        return false;
    }
    text.chars()
        .all(|ch| ch == '_' || ch == '\'' || ch.is_alphanumeric())
}

fn tokens_from_expr(text: &str) -> Vec<String> {
    let mut out = Vec::new();
    let mut current = String::new();
    for ch in text.chars() {
        if ch == '_' || ch == '\'' || ch == '.' || ch.is_alphanumeric() {
            current.push(ch);
        } else {
            push_token(&mut out, &mut current);
        }
    }
    push_token(&mut out, &mut current);
    let mut seen = BTreeSet::new();
    out.into_iter()
        .filter(|token| seen.insert(token.clone()))
        .collect()
}

fn push_token(out: &mut Vec<String>, current: &mut String) {
    if current.is_empty() {
        return;
    }
    if !current.chars().all(|ch| ch.is_ascii_digit() || ch == '.') {
        out.push(current.clone());
    }
    current.clear();
}

fn collect_unknowns(rows: &[RelationRow]) -> Vec<String> {
    let mut out = Vec::new();
    let mut seen = BTreeSet::new();
    for row in rows {
        if let Some(name) = row.defines.as_ref() {
            if seen.insert(name.clone()) {
                out.push(name.clone());
            }
        }
        for token in tokens_from_expr(&row.lhs)
            .into_iter()
            .chain(tokens_from_expr(&row.rhs).into_iter())
        {
            if seen.insert(token.clone()) {
                out.push(token);
            }
        }
    }
    out
}

fn find_assign_conflict(rows: &[RelationRow]) -> Option<String> {
    let mut seen = BTreeSet::new();
    for row in rows {
        let Some(name) = row.defines.as_ref() else {
            continue;
        };
        if !seen.insert(name.clone()) {
            return Some(name.clone());
        }
    }
    None
}

fn causal_order(rows: &[RelationRow]) -> Result<Vec<String>, &'static str> {
    let defined = rows
        .iter()
        .filter_map(|row| {
            row.defines
                .as_ref()
                .map(|name| (name.clone(), row.id.clone()))
        })
        .collect::<BTreeMap<_, _>>();
    let mut emitted = BTreeSet::new();
    let mut order = Vec::new();
    loop {
        let before = order.len();
        for row in rows {
            if emitted.contains(&row.id) {
                continue;
            }
            let ready = row.depends_on.iter().all(|dep| {
                defined
                    .get(dep)
                    .map(|dep_row| emitted.contains(dep_row))
                    .unwrap_or(true)
            });
            if ready {
                emitted.insert(row.id.clone());
                order.push(row.id.clone());
            }
        }
        if order.len() == rows.len() {
            return Ok(order);
        }
        if order.len() == before {
            return Err("E_SEUM_CYCLE");
        }
    }
}

fn s0_plan(
    body_source: &str,
    rows: &[RelationRow],
    unknowns: Vec<String>,
    causal_order: Vec<String>,
) -> JsonValue {
    json!({
        "schema": SCHEMA,
        "source_hash": sha256_prefixed(body_source),
        "stage": "S0",
        "method": "explicit_algebra_causalized_v1",
        "relations": relation_json(rows, true),
        "unknowns": unknowns,
        "lowering": {
            "causalization": "bipartite_matching_toposort_source_order_tiebreak",
            "causal_order": causal_order,
            "materialized_values": rows.iter().filter_map(|row| row.defines.clone()).collect::<Vec<_>>(),
            "phase": seum_phase_json(),
        },
        "diagnostics": [],
        "state_hash_inputs": default_state_hash_inputs(),
    })
}

fn s1_plan(body_source: &str, rows: &[RelationRow], unknowns: Vec<String>) -> JsonValue {
    json!({
        "schema": SCHEMA,
        "source_hash": sha256_prefixed(body_source),
        "stage": "S1",
        "method": "linear_system_bounded_exact_v1",
        "relations": relation_json(rows, false),
        "unknowns": unknowns,
        "lowering": {
            "bound": {
                "unknown_count_max": MAX_S1_UNKNOWNS,
                "unknown_count": collect_unknowns(rows).len(),
            },
            "causalization": "linear_system_source_order_tiebreak",
            "causal_order": rows.iter().map(|row| row.id.clone()).collect::<Vec<_>>(),
            "phase": seum_phase_json(),
        },
        "diagnostics": [],
        "state_hash_inputs": default_state_hash_inputs(),
    })
}

fn s2_plan(
    body_source: &str,
    rows: &[RelationRow],
    integrator_method: IntegratorMethod,
) -> JsonValue {
    let slots = rows
        .iter()
        .filter_map(|row| {
            derivative_slot(&row.lhs).map(|(state, order)| {
                json!({
                    "source_order": row.source_order,
                    "slot": row.lhs,
                    "state": state,
                    "derivative_order": order,
                    "rhs": row.rhs,
                })
            })
        })
        .collect::<Vec<_>>();
    let mut seen = BTreeSet::new();
    let unknowns = slots
        .iter()
        .filter_map(|slot| slot.get("state").and_then(|value| value.as_str()))
        .filter(|state| seen.insert((*state).to_string()))
        .map(str::to_string)
        .collect::<Vec<_>>();
    let vector_components = vector_components_json(&slots);
    let mut lowering = json!({
        "derivative_lowering": "prime_slot_to_stdlib_integrator_v1",
        "integrator": {
            "surface": integrator_method.surface(),
            "stdlib_reference": integrator_method.surface(),
        },
        "state_slots": slots,
        "phase": seum_phase_json(),
    });
    if !vector_components.is_empty() {
        if let Some(object) = lowering.as_object_mut() {
            object.insert(
                "vector_components".to_string(),
                JsonValue::Array(vector_components),
            );
        }
    }
    json!({
        "schema": SCHEMA,
        "source_hash": sha256_prefixed(body_source),
        "stage": "S2",
        "method": integrator_method.solveplan_method(),
        "relations": relation_json(rows, false),
        "unknowns": unknowns,
        "lowering": lowering,
        "diagnostics": [],
        "state_hash_inputs": default_state_hash_inputs(),
    })
}

fn vector_components_json(slots: &[JsonValue]) -> Vec<JsonValue> {
    let mut groups: BTreeMap<String, BTreeMap<String, String>> = BTreeMap::new();
    for slot in slots {
        let Some(state) = slot.get("state").and_then(JsonValue::as_str) else {
            continue;
        };
        let Some((base, axis)) = state.rsplit_once('_') else {
            continue;
        };
        if !matches!(axis, "x" | "y" | "z") {
            continue;
        }
        let Some(slot_name) = slot.get("slot").and_then(JsonValue::as_str) else {
            continue;
        };
        groups
            .entry(base.to_string())
            .or_default()
            .insert(axis.to_string(), slot_name.to_string());
    }

    groups
        .into_iter()
        .map(|(base, axes)| {
            let present_components = ["x", "y", "z"]
                .into_iter()
                .filter(|axis| axes.contains_key(*axis))
                .collect::<Vec<_>>();
            let slots = ["x", "y", "z"]
                .into_iter()
                .filter_map(|axis| axes.get(axis).cloned())
                .collect::<Vec<_>>();
            json!({
                "base": base,
                "component_order": [
                    "x",
                    "y",
                    "z"
                ],
                "present_components": present_components,
                "slots": slots,
            })
        })
        .collect()
}

fn unsupported_plan(
    body_source: &str,
    unknowns: Vec<String>,
    code: &'static str,
    message: &str,
) -> JsonValue {
    json!({
        "schema": SCHEMA,
        "source_hash": sha256_prefixed(body_source),
        "stage": "S3",
        "method": "unsupported_deferred_v1",
        "relations": [],
        "unknowns": unknowns,
        "lowering": {
            "bound": {
                "unknown_count_max": MAX_S1_UNKNOWNS,
                "unknown_count": unknowns.len(),
            },
            "phase": seum_phase_json(),
        },
        "diagnostics": [{
            "code": code,
            "severity": "error",
            "message": message,
        }],
        "state_hash_inputs": default_state_hash_inputs(),
    })
}

fn diagnostic_plan(
    body_source: &str,
    stage: &'static str,
    method: &'static str,
    rows: &[RelationRow],
    unknowns: Vec<String>,
    code: &'static str,
    message: &str,
) -> JsonValue {
    json!({
        "schema": SCHEMA,
        "source_hash": sha256_prefixed(body_source),
        "stage": stage,
        "method": method,
        "relations": relation_json(rows, true),
        "unknowns": unknowns,
        "lowering": {
            "causalization": "bipartite_matching_toposort_source_order_tiebreak",
            "phase": seum_phase_json(),
        },
        "diagnostics": [{
            "code": code,
            "severity": "error",
            "message": message,
        }],
        "state_hash_inputs": default_state_hash_inputs(),
    })
}

fn connect_desugar_plan(surface: &str, rows: &[String]) -> JsonValue {
    let body_source = rows.join("\n");
    let relation_rows = parse_relation_rows(&body_source);
    json!({
        "schema": SCHEMA,
        "source_hash": sha256_prefixed(surface),
        "stage": "S1",
        "method": "connect_desugar_to_seum_rows_v1",
        "relations": relation_json(&relation_rows, false),
        "unknowns": collect_unknowns(&relation_rows),
        "lowering": {
            "connect_desugar": {
                "surface": surface,
                "rows": rows,
                "sign_convention": "incoming_positive_v1",
                "pure_desugar": true,
                "runtime_path": "seum_solveplan",
            },
            "phase": seum_phase_json(),
        },
        "diagnostics": [],
        "state_hash_inputs": default_state_hash_inputs(),
    })
}

fn connect_diagnostic_plan(surface: &str, code: &'static str, message: &str) -> JsonValue {
    json!({
        "schema": SCHEMA,
        "source_hash": sha256_prefixed(surface),
        "stage": "S3",
        "method": "connect_desugar_unsupported_v1",
        "relations": [],
        "unknowns": [],
        "lowering": {
            "connect_desugar": {
                "surface": surface,
                "rows": [],
                "sign_convention": "incoming_positive_v1",
                "pure_desugar": true,
                "runtime_path": "seum_solveplan",
            },
            "phase": seum_phase_json(),
        },
        "diagnostics": [{
            "code": code,
            "severity": "error",
            "message": message,
        }],
        "state_hash_inputs": default_state_hash_inputs(),
    })
}

fn relation_json(rows: &[RelationRow], include_defines: bool) -> Vec<JsonValue> {
    rows.iter()
        .map(|row| {
            if include_defines {
                json!({
                    "id": row.id,
                    "source_order": row.source_order,
                    "text": row.text,
                    "kind": if row.defines.is_some() { "explicit_algebra" } else { "linear" },
                    "defines": row.defines,
                    "depends_on": row.depends_on,
                })
            } else {
                json!({
                    "id": row.id,
                    "source_order": row.source_order,
                    "text": row.text,
                    "kind": "linear",
                    "depends_on": row.depends_on,
                })
            }
        })
        .collect()
}

fn default_state_hash_inputs() -> JsonValue {
    json!({
        "include": [
            "schema",
            "source_hash",
            "stage",
            "method",
            "relations",
            "unknowns",
            "lowering"
        ],
        "exclude": [
            "diagnostics",
            "execution_results"
        ]
    })
}

fn seum_phase_json() -> JsonValue {
    json!({
        "name": "seum_solve",
        "tick_order": [
            "state_read",
            "seum_solve",
            "state_write",
            "hook_next_segment"
        ],
        "writes_apply": "same_tick_before_hook_next_segment"
    })
}

fn sha256_prefixed(text: &str) -> String {
    let digest = Sha256::digest(text.as_bytes());
    format!("sha256:{}", hex::encode(digest))
}

fn write_json(path: &Path, payload: &JsonValue) -> Result<(), String> {
    if let Some(parent) = path.parent() {
        if !parent.as_os_str().is_empty() {
            fs::create_dir_all(parent).map_err(|err| err.to_string())?;
        }
    }
    let text = serde_json::to_string_pretty(payload).map_err(|err| err.to_string())?;
    fs::write(path, format!("{text}\n")).map_err(|err| err.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::cli::frontdoor_parse::parse_program_for_runtime;

    #[test]
    fn s0_causalizes_by_dependency_then_source_order() {
        let plan = build_solveplan_for_assertion("x =:= 2.\ny =:= x + 3.", IntegratorMethod::Euler);
        assert_eq!(plan["stage"], "S0");
        assert_eq!(plan["lowering"]["causal_order"], json!(["r1", "r2"]));
        assert_eq!(plan["unknowns"], json!(["x", "y"]));
    }

    #[test]
    fn s1_rejects_more_than_eight_unknowns() {
        let plan = build_solveplan_for_assertion(
            "x1 =:= 1.\nx2 =:= 2.\nx3 =:= 3.\nx4 =:= 4.\nx5 =:= 5.\nx6 =:= 6.\nx7 =:= 7.\nx8 =:= 8.\nx9 =:= 9.",
            IntegratorMethod::Euler,
        );
        assert_eq!(plan["stage"], "S3");
        assert_eq!(plan["diagnostics"][0]["code"], "E_SEUM_UNSUPPORTED");
    }

    #[test]
    fn s1_reports_under_and_over_determined_diagnostics() {
        let under = build_solveplan_for_assertion("x + y =:= 3.", IntegratorMethod::Euler);
        assert_eq!(under["stage"], "S3");
        assert_eq!(under["diagnostics"][0]["code"], "E_SEUM_UNDERDETERMINED");

        let over = build_solveplan_for_assertion(
            "x + y =:= 3.\nx - y =:= 1.\nx + 2*y =:= 4.",
            IntegratorMethod::Euler,
        );
        assert_eq!(over["stage"], "S3");
        assert_eq!(over["diagnostics"][0]["code"], "E_SEUM_OVERDETERMINED");
    }

    #[test]
    fn s0_reports_cycle_and_assign_conflict_diagnostics() {
        let cycle = build_solveplan_for_assertion("x =:= y.\ny =:= x.", IntegratorMethod::Euler);
        assert_eq!(cycle["stage"], "S3");
        assert_eq!(cycle["diagnostics"][0]["code"], "E_SEUM_CYCLE");

        let conflict = build_solveplan_for_assertion("x =:= 1.\nx =:= 2.", IntegratorMethod::Euler);
        assert_eq!(conflict["stage"], "S3");
        assert_eq!(conflict["diagnostics"][0]["code"], "E_SEUM_ASSIGN_CONFLICT");
    }

    #[test]
    fn run_frontdoor_assertion_collection_uses_product_parser_output() {
        let source = "검사 <- 세움{x =:= 2.}.\n검사 보여주기.";
        let (program, _) = parse_program_for_runtime(source).expect("parse");
        let plans = collect_assertion_exprs(&program)
            .into_iter()
            .map(|expr| build_solveplan_for_assertion_expr(expr, IntegratorMethod::Euler))
            .collect::<Vec<_>>();
        assert_eq!(plans.len(), 1);
        assert_eq!(plans[0]["stage"], "S0");
    }

    #[test]
    fn chaebi_inner_seum_marks_init_plan_or_rejects_s2() {
        let source = "채비 { 세움 { 위치 =:= 0. }. }.";
        let (program, _) = parse_program_for_runtime(source).expect("parse");
        let plans = collect_assertion_exprs(&program)
            .into_iter()
            .map(|expr| build_solveplan_for_assertion_expr(expr, IntegratorMethod::Euler))
            .collect::<Vec<_>>();
        assert_eq!(plans.len(), 1);
        assert_eq!(plans[0]["stage"], "S0");
        assert_eq!(plans[0]["init_plan"]["kind"], "t0_one_shot");
        assert_eq!(plans[0]["init_plan"]["apply"], "before_madi_0");

        let source = "채비 { 세움 { 위치' =:= 속도. }. }.";
        let (program, _) = parse_program_for_runtime(source).expect("parse");
        let plans = collect_assertion_exprs(&program)
            .into_iter()
            .map(|expr| build_solveplan_for_assertion_expr(expr, IntegratorMethod::Euler))
            .collect::<Vec<_>>();
        assert_eq!(plans[0]["stage"], "S3");
        assert_eq!(plans[0]["method"], "init_unsupported_v1");
        assert_eq!(plans[0]["diagnostics"][0]["code"], "E_INIT_UNSUPPORTED");
    }

    #[test]
    fn connect_surface_lowers_to_solveplan_rows() {
        let source = "전지.양극과 전구.왼핀을 (전압은 같게, 전류는 흐르게) 잇기.";
        let plans = collect_connect_desugar_plans(source, IntegratorMethod::Euler);
        assert_eq!(plans.len(), 1);
        assert_eq!(plans[0]["stage"], "S1");
        assert_eq!(
            plans[0]["lowering"]["connect_desugar"]["rows"],
            json!([
                "전지.양극.전압 =:= 전구.왼핀.전압.",
                "전지.양극.전류 + 전구.왼핀.전류 =:= 0."
            ])
        );
        assert_eq!(
            plans[0]["lowering"]["connect_desugar"]["sign_convention"],
            "incoming_positive_v1"
        );
    }

    #[test]
    fn connect_surface_reports_artifact_diagnostics() {
        let plans = collect_connect_desugar_plans(
            "이음관계 <- 전지.양극과 전구.왼핀을 (전압은 같게, 전압은 흐르게) 잇기.",
            IntegratorMethod::Euler,
        );
        assert_eq!(plans[0]["stage"], "S3");
        assert_eq!(
            plans[0]["diagnostics"][0]["code"],
            "E_CONNECT_CHANNEL_MISMATCH"
        );
    }

    #[test]
    fn prime_slots_lower_to_s2_integrator_method() {
        let euler = build_solveplan_for_assertion(
            "위치' =:= 속도.\n속도' =:= 가속도.",
            IntegratorMethod::Euler,
        );
        assert_eq!(euler["stage"], "S2");
        assert_eq!(euler["method"], "ode_explicit_euler_v1");
        assert_eq!(euler["lowering"]["integrator"]["surface"], "적분.오일러");

        let semi = build_solveplan_for_assertion(
            "위치'' =:= 가속도.",
            IntegratorMethod::SemiImplicitEuler,
        );
        assert_eq!(semi["stage"], "S2");
        assert_eq!(semi["method"], "ode_semi_implicit_euler_v1");
        assert_eq!(
            semi["lowering"]["integrator"]["surface"],
            "적분.반암시적오일러"
        );
    }

    #[test]
    fn vector_prime_slots_record_xyz_component_order() {
        let plan = build_solveplan_for_assertion(
            "위치_x' =:= 속도_x.\n위치_y' =:= 속도_y.",
            IntegratorMethod::Euler,
        );
        assert_eq!(
            plan["lowering"]["vector_components"][0]["component_order"],
            json!(["x", "y", "z"])
        );
        assert_eq!(
            plan["lowering"]["vector_components"][0]["present_components"],
            json!(["x", "y"])
        );
    }
}
