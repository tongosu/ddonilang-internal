use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::Path;

use serde_json::{json, Value as JsonValue};
use sha2::{Digest, Sha256};

use crate::lang::ast::{ArgBinding, Binding, Expr, Program, Stmt};

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

pub fn write_solveplan_out(path: &Path, program: &Program) -> Result<(), String> {
    let plans = collect_assertion_exprs(program)
        .into_iter()
        .map(|expr| build_solveplan_for_assertion(&expr.assertion.body_source))
        .collect::<Vec<_>>();
    let payload = match plans.as_slice() {
        [single] => single.clone(),
        _ => json!({
            "schema": BUNDLE_SCHEMA,
            "plans": plans,
        }),
    };
    write_json(path, &payload)
}

#[derive(Clone, Copy)]
struct AssertionExpr<'a> {
    assertion: &'a crate::lang::ast::Assertion,
}

fn collect_assertion_exprs(program: &Program) -> Vec<AssertionExpr<'_>> {
    let mut out = Vec::new();
    collect_assertions_from_stmts(&program.stmts, &mut out);
    out
}

fn collect_assertions_from_stmts<'a>(stmts: &'a [Stmt], out: &mut Vec<AssertionExpr<'a>>) {
    for stmt in stmts {
        match stmt {
            Stmt::DeclBlock { items, .. } => {
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
        Expr::Assertion { assertion, .. } => out.push(AssertionExpr { assertion }),
        Expr::Unary { expr, .. } => collect_assertions_from_expr(expr, out),
        Expr::Binary { left, right, .. } => {
            collect_assertions_from_expr(left, out);
            collect_assertions_from_expr(right, out);
        }
        Expr::SeedLiteral { body, .. } => collect_assertions_from_expr(body, out),
        Expr::Call { args, .. } => collect_assertions_from_args(args, out),
        Expr::FieldAccess { target, .. } => collect_assertions_from_expr(target, out),
        Expr::TemplateFill {
            template,
            bindings,
            ..
        } => {
            collect_assertions_from_expr(template, out);
            collect_assertions_from_bindings(bindings, out);
        }
        Expr::Pack { bindings, .. } => collect_assertions_from_bindings(bindings, out),
        Expr::FormulaFill {
            formula,
            bindings,
            ..
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

fn build_solveplan_for_assertion(body_source: &str) -> JsonValue {
    let rows = parse_relation_rows(body_source);
    if rows.is_empty() {
        return unsupported_plan(body_source, Vec::new(), "E_SEUM_UNSUPPORTED", "no relation rows");
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
        return diagnostic_plan(body_source, "S3", "unsupported_deferred_v1", &rows, unknowns, "E_SEUM_ASSIGN_CONFLICT", &format!("duplicate definition: {conflict}"));
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
    s1_plan(body_source, &rows, unknowns)
}

fn parse_relation_rows(body_source: &str) -> Vec<RelationRow> {
    body_source
        .replace("\r\n", "\n")
        .replace('\r', "\n")
        .split(|ch| ch == '.' || ch == '\n')
        .map(str::trim)
        .filter(|line| !line.is_empty())
        .enumerate()
        .filter_map(|(idx, line)| parse_relation_row(idx, line))
        .collect()
}

fn parse_relation_row(idx: usize, line: &str) -> Option<RelationRow> {
    let (lhs, rhs) = line.split_once("=:= " ).or_else(|| line.split_once("=:="))?;
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
        if ch == '_' || ch == '\'' || ch.is_alphanumeric() {
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
    if !current.chars().all(|ch| ch.is_ascii_digit()) {
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
        .filter_map(|row| row.defines.as_ref().map(|name| (name.clone(), row.id.clone())))
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
        },
        "diagnostics": [],
        "state_hash_inputs": default_state_hash_inputs(),
    })
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
            }
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
        let plan = build_solveplan_for_assertion("x =:= 2.\ny =:= x + 3.");
        assert_eq!(plan["stage"], "S0");
        assert_eq!(plan["lowering"]["causal_order"], json!(["r1", "r2"]));
        assert_eq!(plan["unknowns"], json!(["x", "y"]));
    }

    #[test]
    fn s1_rejects_more_than_eight_unknowns() {
        let plan = build_solveplan_for_assertion(
            "x1 =:= 1.\nx2 =:= 2.\nx3 =:= 3.\nx4 =:= 4.\nx5 =:= 5.\nx6 =:= 6.\nx7 =:= 7.\nx8 =:= 8.\nx9 =:= 9.",
        );
        assert_eq!(plan["stage"], "S3");
        assert_eq!(plan["diagnostics"][0]["code"], "E_SEUM_UNSUPPORTED");
    }

    #[test]
    fn run_frontdoor_assertion_collection_uses_product_parser_output() {
        let source = "검사 <- 세움{x =:= 2.}.\n검사 보여주기.";
        let (program, _) = parse_program_for_runtime(source).expect("parse");
        let plans = collect_assertion_exprs(&program)
            .into_iter()
            .map(|expr| build_solveplan_for_assertion(&expr.assertion.body_source))
            .collect::<Vec<_>>();
        assert_eq!(plans.len(), 1);
        assert_eq!(plans[0]["stage"], "S0");
    }
}
