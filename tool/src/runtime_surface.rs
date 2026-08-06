use std::collections::{BTreeMap, HashMap};

use blake3::hash as blake3_hash;
use ddonirang_core::platform::{
    DetNuri, InputSnapshot, InputSource, Patch, PatchOp, ResourceValue,
};
use ddonirang_core::{Fixed64, Nuri, ResourceHandle, SeulgiIntent};
use ddonirang_lang::runtime::Value;
use ddonirang_lang::{ExecutionModeDecision, ParseMode};
use serde_json::{json, Map, Value as JsonValue};

use crate::canon::{self, CanonOutput};
use crate::ddn_runtime::{
    formula_from_resource_value, formula_summary_parts, DdnProgram, DdnRunner,
};
use crate::preprocess::{
    execution_mode_decision_from_source, preprocess_source_for_parse, split_file_meta,
    validate_no_legacy_boim_surface, validate_no_legacy_header,
};

pub const DEFAULT_UPDATE_NAME: &str = "매마디";
pub const ENGINE_RESPONSE_SCHEMA: &str = "seamgrim.engine_response.v0";
pub const OBSERVATION_MANIFEST_SCHEMA: &str = "ddn.observation_manifest.v0";
pub const OBSERVATION_MANIFEST_VERSION: &str = "20.6.33";
pub const DEFAULT_VIEW_PREFIXES: &[&str] = &["보개_", "__view_"];

const BOGAE_DRAWLIST_TAG: &str = "보개_그림판_목록";
const BOGAE_WIDTH_TAG: &str = "보개_그림판_가로";
const BOGAE_HEIGHT_TAG: &str = "보개_그림판_세로";
const BOGAE_SHOW_LINES_TAG: &str = "보개_출력_줄들";

#[derive(Debug, Clone)]
pub struct PreparedSource {
    pub stripped_source: String,
    pub preprocessed_source: String,
    pub execution_source: String,
    pub canonical_ddn: String,
    pub meta_lines: usize,
    pub execution_mode_decision: ExecutionModeDecision,
}

pub fn prepare_source_for_execution(source: &str) -> Result<PreparedSource, String> {
    let meta = split_file_meta(source);
    validate_no_legacy_header(&meta.stripped)?;
    validate_no_legacy_boim_surface(&meta.stripped)?;
    let execution_mode_decision = execution_mode_decision_from_source(&meta.stripped)?;
    let preprocessed = preprocess_source_for_parse(&meta.stripped)?;
    let execution_source = ddonirang_lang::preprocess_frontdoor_source(&preprocessed);
    let canonical = canonicalize_prepared_source(&preprocessed)?;
    Ok(PreparedSource {
        stripped_source: meta.stripped,
        preprocessed_source: preprocessed,
        execution_source,
        canonical_ddn: canonical.ddn,
        meta_lines: meta.meta_lines,
        execution_mode_decision,
    })
}

pub fn canonicalize_shared_source(source: &str) -> Result<CanonOutput, String> {
    let prepared = prepare_source_for_execution(source)?;
    canonicalize_prepared_source(&prepared.preprocessed_source)
}

fn canonicalize_prepared_source(source: &str) -> Result<CanonOutput, String> {
    canon::canonicalize(source, false).map_err(|err| format!("파싱 실패: {err}"))
}

pub fn canonicalize_shared_ddn(source: &str) -> Result<String, String> {
    canonicalize_shared_source(source).map(|output| output.ddn)
}

fn sha256_hex(bytes: &[u8]) -> String {
    use sha2::{Digest, Sha256};
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    format!("{:x}", hasher.finalize())
}

pub fn current_state_hash(world: &ddonirang_core::platform::NuriWorld) -> String {
    format!(
        "blake3:{}",
        world
            .state_hash_excluding_resource_prefixes(DEFAULT_VIEW_PREFIXES)
            .to_hex()
    )
}

pub fn execution_envelope_from_source(
    source: &str,
    requested_ticks: Option<u32>,
) -> Result<JsonValue, String> {
    let prepared = prepare_source_for_execution(source)?;
    let program = DdnProgram::from_source_with_mode(
        &prepared.execution_source,
        "<execution-envelope>",
        ParseMode::Strict,
    )?;
    let configured_madi = program.configured_madi().unwrap_or(0);
    let execution_mode_decision = prepared.execution_mode_decision;
    let effective_ticks = requested_ticks
        .map(u64::from)
        .unwrap_or_else(|| configured_madi.max(1))
        .max(1);
    Ok(build_execution_envelope(
        source,
        &prepared,
        configured_madi,
        execution_mode_decision,
        requested_ticks,
        effective_ticks,
        Fixed64::from_i64(1),
        0,
    ))
}

fn build_execution_envelope(
    source: &str,
    prepared: &PreparedSource,
    configured_madi: u64,
    execution_mode_decision: ExecutionModeDecision,
    requested_ticks: Option<u32>,
    effective_ticks: u64,
    input_dt: Fixed64,
    rng_base_seed: u64,
) -> JsonValue {
    json!({
        "source_bytes_sha256": sha256_hex(source.as_bytes()),
        "stripped_source_sha256": sha256_hex(prepared.stripped_source.as_bytes()),
        "preprocessed_source_sha256": sha256_hex(prepared.execution_source.as_bytes()),
        "canonical_ddn_sha256": sha256_hex(prepared.canonical_ddn.as_bytes()),
        "input_snapshot": {
            "keys_pressed": 0,
            "last_key_name": "",
            "pointer_x_i32": 0,
            "pointer_y_i32": 0,
            "dt": input_dt.to_string(),
            "frame_source": InputSource::Person.label(),
            "frame_source_code": InputSource::Person.code_u8(),
            "rng_base_seed": rng_base_seed
        },
        "frame_source": InputSource::Person.label(),
        "frame_source_code": InputSource::Person.code_u8(),
        "rng_seed": rng_base_seed,
        "dt": input_dt.to_string(),
        "configured_madi": configured_madi,
        "execution_mode_decision": execution_mode_decision_json(execution_mode_decision),
        "requested_ticks": requested_ticks.map(u64::from),
        "effective_ticks": effective_ticks,
        "dialect_or_mode": "strict",
        "runtime_schema": ENGINE_RESPONSE_SCHEMA
    })
}

pub fn execution_mode_decision_json(decision: ExecutionModeDecision) -> JsonValue {
    json!({
        "schema": "ddn.execution_mode_decision.v1",
        "mode": decision.mode.as_str(),
        "authority": "parsed_program",
        "reason": decision.reason(),
        "live_hook_count": decision.live_hook_count,
        "every_madi_hook_count": decision.every_madi_hook_count,
        "every_n_madi_hook_count": decision.every_n_madi_hook_count,
    })
}

pub fn run_summary_from_source(
    source: &str,
    file_path: &str,
    requested_ticks: Option<u32>,
) -> Result<JsonValue, String> {
    let prepared = prepare_source_for_execution(source)?;
    let program = DdnProgram::from_source_with_mode(
        &prepared.execution_source,
        file_path,
        ParseMode::Strict,
    )?;
    let configured_madi = program.configured_madi().unwrap_or(0);
    let execution_mode_decision = prepared.execution_mode_decision;
    let parse_warnings = program.parse_warnings().to_vec();
    let effective_ticks = requested_ticks
        .map(u64::from)
        .unwrap_or_else(|| configured_madi.max(1))
        .max(1);

    let mut runner = DdnRunner::new(program, DEFAULT_UPDATE_NAME);
    let mut world = DetNuri::new();
    let mut defaults = HashMap::new();
    seed_bogae_defaults(&mut defaults);
    let rng_base_seed = 0u64;
    let mut tick_id = 0u64;
    let input_dt = Fixed64::from_i64(1);
    let mut last_patch = Patch::default();
    let mut last_input = serialize_input_state(0, "", 0, 0, input_dt, rng_base_seed, rng_base_seed);

    for _ in 0..effective_ticks {
        let tick_seed = rng_base_seed ^ tick_id;
        let input = InputSnapshot {
            tick_id,
            dt: input_dt,
            keys_pressed: 0,
            last_key_name: String::new(),
            pointer_x_i32: 0,
            pointer_y_i32: 0,
            ai_injections: Vec::new(),
            net_events: Vec::new(),
            frame_source: InputSource::Person,
            rng_seed: tick_seed,
        };
        let output = runner.run_update(world.world(), &input, &defaults)?;
        let mut sink = ddonirang_core::signals::VecSignalSink::default();
        world.apply_patch(&output.patch, input.tick_id, &mut sink);
        last_patch = output.patch;
        last_input = serialize_input_snapshot(&input, Some(rng_base_seed));
        tick_id = tick_id.saturating_add(1);
    }

    let state = build_engine_state_json(&world, tick_id, last_input, &last_patch);
    let final_row = index_row_from_state(&state);
    let output_log_texts = output_log_texts_from_state_json(&state);
    let parse_warnings_json = parse_warnings
        .iter()
        .map(|warning| {
            json!({
                "code": warning.code,
                "message": warning.message,
                "span": {
                    "start": warning.span_start,
                    "end": warning.span_end,
                }
            })
        })
        .collect::<Vec<_>>();

    Ok(json!({
        "schema": "ddn.ddonirang_tool.shared_run_summary.v1",
        "runtime_schema": ENGINE_RESPONSE_SCHEMA,
        "update_name": DEFAULT_UPDATE_NAME,
        "source_path": file_path,
        "canonical_ddn": prepared.canonical_ddn,
        "preprocessed_source": prepared.execution_source,
        "configured_ticks": configured_madi,
        "effective_ticks": effective_ticks,
        "ticks_run": effective_ticks,
        "parse_warnings": parse_warnings_json,
        "state_hash": state.get("state_hash").cloned().unwrap_or(JsonValue::String(String::new())),
        "view_hash": state.get("view_hash").cloned().unwrap_or(JsonValue::String(String::new())),
        "final_row": final_row,
        "resources": state.get("resources").cloned().unwrap_or_else(|| JsonValue::Object(Map::new())),
        "channels": state.get("channels").cloned().unwrap_or_else(|| JsonValue::Array(Vec::new())),
        "row": state.get("row").cloned().unwrap_or_else(|| JsonValue::Array(Vec::new())),
        "output_log_texts": output_log_texts,
        "output_rows": [],
        "engine_state": state,
        "execution_envelope": build_execution_envelope(
            source,
            &prepared,
            configured_madi,
            execution_mode_decision,
            requested_ticks,
            effective_ticks,
            input_dt,
            rng_base_seed,
        ),
        "parity_surface": {
            "domain": "ddonirang_tool_shared_runtime",
            "state_hash_formula_change": false,
            "view_prefix_exclusion": DEFAULT_VIEW_PREFIXES
        },
        "meta_lines": prepared.meta_lines
    }))
}

pub fn build_engine_state_json(
    world: &DetNuri,
    tick_id: u64,
    input_json: JsonValue,
    patch: &Patch,
) -> JsonValue {
    let resources = serialize_world_resources(world.world());
    let (columns, row) = collect_columns_and_row(world.world());
    let observation_manifest = build_observation_manifest(&columns);
    let view_meta = build_view_meta(world.world());
    let view_hash = hash_json_string(&view_meta);
    let patch_json = serialize_patch(patch);
    json!({
        "schema": ENGINE_RESPONSE_SCHEMA,
        "tick_id": tick_id,
        "state_hash": current_state_hash(world.world()),
        "input": input_json.clone(),
        "resources": resources.clone(),
        "channels": columns.clone(),
        "row": row.clone(),
        "observation_manifest": observation_manifest.clone(),
        "streams": JsonValue::Object(Map::new()),
        "patch": patch_json.clone(),
        "state": {
            "tick_id": tick_id,
            "input": input_json,
            "resources": resources,
            "channels": columns,
            "row": row,
            "observation_manifest": observation_manifest,
            "patch": patch_json,
            "streams": JsonValue::Object(Map::new())
        },
        "view_meta": view_meta,
        "view_hash": view_hash
    })
}

fn index_row_from_state(state: &JsonValue) -> JsonValue {
    let mut out = Map::new();
    let channels = state
        .get("channels")
        .and_then(JsonValue::as_array)
        .cloned()
        .unwrap_or_default();
    let row = state
        .get("row")
        .and_then(JsonValue::as_array)
        .cloned()
        .unwrap_or_default();
    for (idx, channel) in channels.iter().enumerate() {
        let key = channel
            .get("key")
            .and_then(JsonValue::as_str)
            .unwrap_or_default()
            .trim();
        if key.is_empty() {
            continue;
        }
        out.insert(
            key.to_string(),
            row.get(idx).cloned().unwrap_or(JsonValue::Null),
        );
    }
    JsonValue::Object(out)
}

fn output_log_texts_from_state_json(state: &JsonValue) -> Vec<String> {
    let Some(value) = state.pointer("/resources/value_json/output_log") else {
        return Vec::new();
    };
    let Some(items) = value.as_array() else {
        return Vec::new();
    };
    items.iter().filter_map(output_log_entry_text).collect()
}

fn output_log_entry_text(value: &JsonValue) -> Option<String> {
    if let Some(text) = value.as_str() {
        return Some(text.to_string());
    }
    if let Some(obj) = value.as_object() {
        if let Some(text) = obj.get("text").and_then(JsonValue::as_str) {
            return Some(text.to_string());
        }
        if let Some(value) = obj.get("value") {
            return Some(json_scalar_to_display_text(value));
        }
    }
    Some(json_scalar_to_display_text(value))
}

fn json_scalar_to_display_text(value: &JsonValue) -> String {
    match value {
        JsonValue::String(text) => text.clone(),
        JsonValue::Number(number) => number.to_string(),
        JsonValue::Bool(true) => "참".to_string(),
        JsonValue::Bool(false) => "거짓".to_string(),
        JsonValue::Null => "없음".to_string(),
        other => serde_json::to_string(other).unwrap_or_default(),
    }
}

pub fn seed_bogae_defaults(defaults: &mut HashMap<String, Value>) {
    defaults.insert(BOGAE_DRAWLIST_TAG.to_string(), Value::List(Vec::new()));
    defaults.insert(BOGAE_SHOW_LINES_TAG.to_string(), Value::List(Vec::new()));
    defaults.insert(
        BOGAE_WIDTH_TAG.to_string(),
        Value::Fixed64(Fixed64::from_i64(0)),
    );
    defaults.insert(
        BOGAE_HEIGHT_TAG.to_string(),
        Value::Fixed64(Fixed64::from_i64(0)),
    );
    defaults.insert("프레임수".to_string(), Value::Fixed64(Fixed64::from_i64(0)));
    defaults.insert(
        "__wasm_start_once".to_string(),
        Value::Fixed64(Fixed64::from_i64(0)),
    );
    defaults.insert("회전_x".to_string(), Value::Fixed64(Fixed64::from_i64(0)));
    defaults.insert("회전_y".to_string(), Value::Fixed64(Fixed64::from_i64(0)));
}

pub fn serialize_world_resources(world: &ddonirang_core::platform::NuriWorld) -> JsonValue {
    let mut out = Map::new();
    let mut value_json_map = Map::new();

    let mut json_map = Map::new();
    for (tag, json_text) in world.resource_json_entries() {
        value_json_map.insert(tag.clone(), resource_json_text_to_json(&json_text));
        json_map.insert(tag, JsonValue::String(json_text));
    }
    out.insert("json".to_string(), JsonValue::Object(json_map));

    let mut fixed_map = Map::new();
    for (tag, value) in world.resource_fixed64_entries() {
        value_json_map.insert(tag.clone(), json!(fixed64_to_f64(value)));
        fixed_map.insert(tag, JsonValue::String(value.to_string()));
    }
    out.insert("fixed64".to_string(), JsonValue::Object(fixed_map));

    let mut handle_map = Map::new();
    for (tag, handle) in world.resource_handle_entries() {
        handle_map.insert(tag, JsonValue::String(handle_to_string(handle)));
    }
    out.insert("handle".to_string(), JsonValue::Object(handle_map));

    let mut value_map = Map::new();
    for (tag, value) in world.resource_value_entries() {
        value_map.insert(tag.clone(), JsonValue::String(value.canon_key()));
        value_json_map.insert(tag, resource_value_to_json(&value));
    }
    out.insert("value".to_string(), JsonValue::Object(value_map));
    out.insert("value_json".to_string(), JsonValue::Object(value_json_map));

    JsonValue::Object(out)
}

pub fn collect_columns_and_row(
    world: &ddonirang_core::platform::NuriWorld,
) -> (Vec<JsonValue>, Vec<JsonValue>) {
    let mut table: BTreeMap<String, (String, JsonValue)> = BTreeMap::new();

    for (tag, value) in world.resource_fixed64_entries() {
        table.insert(tag, ("num".to_string(), json!(fixed64_to_f64(value))));
    }

    for (tag, value) in world.resource_json_entries() {
        if let Some((dtype, scalar)) = json_text_to_scalar(&value) {
            table.insert(tag, (dtype, scalar));
        }
    }

    for (tag, value) in world.resource_value_entries() {
        if let Some((dtype, scalar)) = resource_value_to_scalar(&value) {
            table.insert(tag, (dtype, scalar));
        }
    }

    let mut columns = Vec::with_capacity(table.len());
    let mut row = Vec::with_capacity(table.len());
    for (key, (dtype, value)) in table {
        columns.push(json!({
            "key": key,
            "dtype": dtype,
            "role": "state",
        }));
        row.push(value);
    }
    (columns, row)
}

pub fn build_observation_manifest(channels: &[JsonValue]) -> JsonValue {
    let mut nodes = Vec::new();
    let mut keys = Vec::new();

    for entry in channels {
        let JsonValue::Object(obj) = entry else {
            continue;
        };
        let Some(key) = obj.get("key").and_then(JsonValue::as_str) else {
            continue;
        };
        if key.trim().is_empty() {
            continue;
        }
        keys.push(key.to_string());
        let dtype = obj
            .get("dtype")
            .and_then(JsonValue::as_str)
            .unwrap_or("unknown");
        let role = obj
            .get("role")
            .and_then(JsonValue::as_str)
            .unwrap_or_else(|| classify_observation_role(key));
        nodes.push(json!({
            "name": key,
            "dtype": dtype,
            "role": role,
        }));
    }

    let x_channel = if keys.iter().any(|key| key == "프레임수") {
        "프레임수".to_string()
    } else if keys.iter().any(|key| key == "t") {
        "t".to_string()
    } else if keys.iter().any(|key| key == "tick_id") {
        "tick_id".to_string()
    } else {
        keys.first().cloned().unwrap_or_default()
    };
    let y_channels: Vec<String> = keys
        .iter()
        .filter(|key| *key != &x_channel)
        .take(2)
        .cloned()
        .collect();

    json!({
        "schema": OBSERVATION_MANIFEST_SCHEMA,
        "version": OBSERVATION_MANIFEST_VERSION,
        "nodes": nodes,
        "params": [],
        "traces": [],
        "diagnostics": [],
        "default_pivot": {
            "x_channel": x_channel,
            "y_channels": y_channels,
        }
    })
}

fn serialize_patch(patch: &Patch) -> JsonValue {
    let mut items = Vec::new();
    for op in &patch.ops {
        match op {
            PatchOp::SetResourceJson { tag, json } => {
                items.push(json!({ "op": "set_resource_json", "tag": tag, "value": json }));
            }
            PatchOp::SetResourceFixed64 { tag, value } => {
                items.push(
                    json!({ "op": "set_resource_fixed64", "tag": tag, "value": value.to_string() }),
                );
            }
            PatchOp::SetResourceHandle { tag, handle } => {
                items.push(json!({ "op": "set_resource_handle", "tag": tag, "value": handle_to_string(*handle) }));
            }
            PatchOp::SetResourceValue { tag, value } => {
                items.push(json!({
                    "op": "set_resource_value",
                    "tag": tag,
                    "value": value.canon_key(),
                    "value_json": resource_value_to_json(value),
                }));
            }
            PatchOp::DivAssignResourceFixed64 { tag, rhs, .. } => {
                items.push(json!({ "op": "div_assign_resource_fixed64", "tag": tag, "value": rhs.to_string() }));
            }
            PatchOp::SetComponentJson { entity, tag, json } => {
                items.push(json!({ "op": "set_component_json", "entity": entity.0, "tag": tag.0, "value": json }));
            }
            PatchOp::RemoveComponent { entity, tag } => {
                items.push(json!({ "op": "remove_component", "entity": entity.0, "tag": tag.0 }));
            }
            PatchOp::EmitSignal { signal, targets } => {
                items.push(
                    json!({ "op": "emit_signal", "signal": signal.name(), "targets": targets }),
                );
            }
            PatchOp::GuardViolation { entity, rule_id } => {
                items.push(
                    json!({ "op": "guard_violation", "entity": entity.0, "rule_id": rule_id }),
                );
            }
        }
    }
    JsonValue::Array(items)
}

fn serialize_input_snapshot(input: &InputSnapshot, rng_base_seed: Option<u64>) -> JsonValue {
    let mut out = Map::new();
    out.insert("keys_pressed".to_string(), json!(input.keys_pressed));
    out.insert("last_key_name".to_string(), json!(input.last_key_name));
    out.insert("pointer_x_i32".to_string(), json!(input.pointer_x_i32));
    out.insert("pointer_y_i32".to_string(), json!(input.pointer_y_i32));
    out.insert("dt".to_string(), json!(input.dt.to_string()));
    out.insert(
        "frame_source".to_string(),
        json!(input.frame_source.label()),
    );
    out.insert(
        "frame_source_code".to_string(),
        json!(input.frame_source.code_u8()),
    );
    out.insert("rng_seed".to_string(), json!(input.rng_seed));
    if let Some(base_seed) = rng_base_seed {
        out.insert("rng_base_seed".to_string(), json!(base_seed));
    }
    out.insert(
        "ai_injections".to_string(),
        JsonValue::Array(
            input
                .ai_injections
                .iter()
                .map(|packet| {
                    json!({
                        "agent_id": packet.agent_id,
                        "recv_seq": packet.recv_seq,
                        "accepted_madi": packet.accepted_madi,
                        "target_madi": packet.target_madi,
                        "source": packet.source.label(),
                        "source_code": packet.source.code_u8(),
                        "source_meta": input_source_json(packet.source),
                        "intent": seulgi_intent_json(&packet.intent),
                    })
                })
                .collect(),
        ),
    );
    out.insert(
        "net_events".to_string(),
        JsonValue::Array(
            input
                .net_events
                .iter()
                .map(|event| {
                    json!({
                        "sender": event.sender.as_str(),
                        "seq": event.seq,
                        "order_key": event.order_key.as_str(),
                        "payload_detjson": event.payload_detjson.as_str(),
                        "source": event.source.label(),
                        "source_code": event.source.code_u8(),
                        "source_meta": input_source_json(event.source),
                    })
                })
                .collect(),
        ),
    );
    JsonValue::Object(out)
}

fn serialize_input_state(
    keys_pressed: u64,
    last_key_name: &str,
    pointer_x_i32: i32,
    pointer_y_i32: i32,
    dt: Fixed64,
    rng_seed: u64,
    rng_base_seed: u64,
) -> JsonValue {
    json!({
        "keys_pressed": keys_pressed,
        "last_key_name": last_key_name,
        "pointer_x_i32": pointer_x_i32,
        "pointer_y_i32": pointer_y_i32,
        "dt": dt.to_string(),
        "frame_source": InputSource::Person.label(),
        "frame_source_code": InputSource::Person.code_u8(),
        "rng_seed": rng_seed,
        "rng_base_seed": rng_base_seed,
        "pending_ai_injection_count": 0,
    })
}

fn input_source_json(source: InputSource) -> JsonValue {
    json!({
        "label": source.label(),
        "code": source.code_u8(),
    })
}

fn seulgi_intent_json(intent: &SeulgiIntent) -> JsonValue {
    match intent {
        SeulgiIntent::None => json!({
            "kind": "none",
            "kind_code": intent.kind_u32(),
        }),
        SeulgiIntent::MoveTo { x, y } => json!({
            "kind": "move_to",
            "kind_code": intent.kind_u32(),
            "x": x.to_string(),
            "y": y.to_string(),
            "x_raw_i64": x.raw_i64(),
            "y_raw_i64": y.raw_i64(),
        }),
        SeulgiIntent::Attack { target_id } => json!({
            "kind": "attack",
            "kind_code": intent.kind_u32(),
            "target_id": target_id,
        }),
        SeulgiIntent::Say { text } => json!({
            "kind": "say",
            "kind_code": intent.kind_u32(),
            "text": text.as_str(),
        }),
    }
}

fn resource_json_text_to_json(text: &str) -> JsonValue {
    serde_json::from_str::<JsonValue>(text).unwrap_or_else(|_| JsonValue::String(text.to_string()))
}

fn json_text_to_scalar(text: &str) -> Option<(String, JsonValue)> {
    let trimmed = text.trim();
    if trimmed == "참" {
        return Some(("bool".to_string(), JsonValue::Bool(true)));
    }
    if trimmed == "거짓" {
        return Some(("bool".to_string(), JsonValue::Bool(false)));
    }
    if let Ok(parsed) = serde_json::from_str::<JsonValue>(trimmed) {
        return match parsed {
            JsonValue::Bool(v) => Some(("bool".to_string(), JsonValue::Bool(v))),
            JsonValue::Number(v) => Some(("num".to_string(), JsonValue::Number(v))),
            JsonValue::String(v) => Some(("str".to_string(), JsonValue::String(v))),
            _ => None,
        };
    }
    if let Ok(number) = trimmed.parse::<f64>() {
        if number.is_finite() {
            return Some(("num".to_string(), json!(number)));
        }
    }
    Some(("str".to_string(), JsonValue::String(text.to_string())))
}

fn resource_value_to_scalar(value: &ResourceValue) -> Option<(String, JsonValue)> {
    match value {
        ResourceValue::Bool(v) => Some(("bool".to_string(), JsonValue::Bool(*v))),
        ResourceValue::Fixed64(v) => Some(("num".to_string(), json!(fixed64_to_f64(*v)))),
        ResourceValue::Unit(v) => Some(("num".to_string(), json!(fixed64_to_f64(v.value)))),
        ResourceValue::String(v) => Some(("str".to_string(), JsonValue::String(v.clone()))),
        _ => None,
    }
}

fn resource_value_to_json(value: &ResourceValue) -> JsonValue {
    if let Some(formula) = formula_from_resource_value(value) {
        let (dialect, raw) = formula_summary_parts(&formula);
        return json!({
            "dialect": dialect,
            "raw": raw,
        });
    }
    match value {
        ResourceValue::None => JsonValue::Null,
        ResourceValue::Bool(v) => JsonValue::Bool(*v),
        ResourceValue::Fixed64(v) => json!(fixed64_to_f64(*v)),
        ResourceValue::Unit(v) => json!(fixed64_to_f64(v.value)),
        ResourceValue::String(s) => JsonValue::String(s.clone()),
        ResourceValue::ResourceHandle(handle) => JsonValue::String(handle_to_string(*handle)),
        ResourceValue::List(items) => {
            JsonValue::Array(items.iter().map(resource_value_to_json).collect())
        }
        ResourceValue::Set(items) => {
            JsonValue::Array(items.values().map(resource_value_to_json).collect())
        }
        ResourceValue::Map(entries) => {
            let mut obj = Map::new();
            for entry in entries.values() {
                let key = resource_key_to_string(&entry.key);
                obj.insert(key, resource_value_to_json(&entry.value));
            }
            JsonValue::Object(obj)
        }
    }
}

fn build_view_meta(world: &ddonirang_core::platform::NuriWorld) -> JsonValue {
    let mut out = Map::new();

    if let Some(width) = world.get_resource_fixed64(BOGAE_WIDTH_TAG) {
        out.insert("canvas_width".to_string(), json!(fixed64_to_f64(width)));
    }
    if let Some(height) = world.get_resource_fixed64(BOGAE_HEIGHT_TAG) {
        out.insert("canvas_height".to_string(), json!(fixed64_to_f64(height)));
    }

    if let Some(draw_list_value) = world.get_resource_value(BOGAE_DRAWLIST_TAG) {
        if let ResourceValue::List(items) = draw_list_value {
            let draw_items: Vec<JsonValue> = items
                .iter()
                .filter_map(resource_value_to_draw_item)
                .collect();
            out.insert("draw_list".to_string(), JsonValue::Array(draw_items));
            out.insert(
                "draw_list_meta".to_string(),
                json!({
                    "deprecated": true,
                    "use_instead": "view_meta.space2d",
                }),
            );
        }
    }

    let mut available_families = Vec::new();
    if let Some(space2d_json) = derive_space2d_from_bogae(world) {
        if let Ok(space2d) = serde_json::from_str::<JsonValue>(&space2d_json) {
            out.insert("space2d".to_string(), space2d);
            available_families.push("space2d");
        }
    }
    append_view_stack_meta(&mut out, &available_families);
    JsonValue::Object(out)
}

fn append_view_stack_meta(out: &mut Map<String, JsonValue>, available_families: &[&str]) {
    let Some((primary_family, secondary_families)) = available_families.split_first() else {
        return;
    };
    out.insert(
        "primary".to_string(),
        json!({
            "family": *primary_family,
            "role": "main",
        }),
    );
    let secondary = secondary_families
        .iter()
        .map(|family| {
            json!({
                "family": *family,
                "role": "secondary",
            })
        })
        .collect::<Vec<_>>();
    out.insert("secondary".to_string(), JsonValue::Array(secondary));
    out.insert("overlays".to_string(), JsonValue::Array(Vec::new()));
}

fn derive_space2d_from_bogae(world: &ddonirang_core::platform::NuriWorld) -> Option<String> {
    let list = world.get_resource_value(BOGAE_DRAWLIST_TAG)?;
    let ResourceValue::List(items) = list else {
        return None;
    };
    let mut draw_items = Vec::new();
    for item in &items {
        if let Some(obj) = resource_value_to_draw_item(item) {
            draw_items.push(obj);
        }
    }
    if draw_items.is_empty() {
        return None;
    }
    let mut space2d = Map::new();
    space2d.insert(
        "schema".to_string(),
        JsonValue::String("seamgrim.space2d.v0".to_string()),
    );
    space2d.insert("drawlist".to_string(), JsonValue::Array(draw_items));
    if let (Some(w), Some(h)) = (
        world.get_resource_fixed64(BOGAE_WIDTH_TAG),
        world.get_resource_fixed64(BOGAE_HEIGHT_TAG),
    ) {
        let w = fixed64_to_f64(w);
        let h = fixed64_to_f64(h);
        if w.is_finite() && h.is_finite() && w > 0.0 && h > 0.0 {
            space2d.insert(
                "camera".to_string(),
                json!({
                    "x_min": 0.0,
                    "x_max": w,
                    "y_min": 0.0,
                    "y_max": h,
                }),
            );
        }
    }
    Some(JsonValue::Object(space2d).to_string())
}

fn resource_value_to_draw_item(value: &ResourceValue) -> Option<JsonValue> {
    let ResourceValue::Map(entries) = value else {
        return None;
    };
    let mut obj = Map::new();
    let mut kind_raw: Option<String> = None;
    for entry in entries.values() {
        let key = resource_key_to_string(&entry.key);
        let json_value = resource_value_to_json(&entry.value);
        match key.as_str() {
            "결" | "kind" | "shape" | "도형" | "형태" => {
                kind_raw = Some(resource_value_to_string(&entry.value));
            }
            "채움색" | "채움" => {
                obj.insert("fill".to_string(), json_value);
            }
            "색" | "선색" => {
                obj.insert("color".to_string(), json_value);
            }
            "굵기" => {
                obj.insert("width".to_string(), json_value);
            }
            "크기" => {
                obj.insert("size".to_string(), json_value);
            }
            "글" | "내용" => {
                obj.insert("text".to_string(), json_value);
            }
            "층" | "레이어" | "layer" | "layerIndex" | "z" | "z_index" => {
                obj.insert("layer_index".to_string(), json_value);
            }
            "그룹" | "묶음" | "group" | "groupId" => {
                obj.insert("group_id".to_string(), json_value);
            }
            _ => {
                obj.insert(key, json_value);
            }
        }
    }
    if let Some(raw) = kind_raw {
        obj.insert("kind".to_string(), JsonValue::String(map_bogae_kind(&raw)));
    }
    Some(JsonValue::Object(obj))
}

fn resource_value_to_string(value: &ResourceValue) -> String {
    match value {
        ResourceValue::String(s) => s.clone(),
        _ => value.canon_key(),
    }
}

fn map_bogae_kind(raw: &str) -> String {
    let lower = raw.to_lowercase();
    if lower.contains("rect") {
        return "rect".to_string();
    }
    if lower.contains("text") {
        return "text".to_string();
    }
    if lower.contains("circle") {
        return "circle".to_string();
    }
    if lower.contains("polygon") {
        return "polygon".to_string();
    }
    if lower.contains("poly") {
        return "polyline".to_string();
    }
    if lower.contains("line") {
        return "line".to_string();
    }
    if lower.contains("point") {
        return "point".to_string();
    }
    if lower.contains("arrow") {
        return "arrow".to_string();
    }
    if lower.contains("sprite") {
        return "rect".to_string();
    }
    if lower.contains("사각") || lower.contains("네모") {
        return "rect".to_string();
    }
    if lower.contains("동그라미") || lower == "원" || lower.contains("원형") {
        return "circle".to_string();
    }
    if lower.contains("선분") || lower == "선" {
        return "line".to_string();
    }
    if lower == "점" || lower.contains("점형") {
        return "point".to_string();
    }
    if lower.contains("화살") || lower.contains("살표") {
        return "arrow".to_string();
    }
    if lower == "글" || lower.contains("글자") || lower.contains("문자") {
        return "text".to_string();
    }
    if lower.contains("다각") {
        return "polygon".to_string();
    }
    raw.to_string()
}

fn resource_key_to_string(value: &ResourceValue) -> String {
    match value {
        ResourceValue::String(s) => s.clone(),
        _ => value.canon_key(),
    }
}

fn classify_observation_role(key: &str) -> &'static str {
    if key == "__tick__"
        || key == "tick_id"
        || key == "tick"
        || key == "state_hash"
        || key == "view_hash"
        || key == "frame_id"
        || key == "tick_time_ms"
    {
        return "파생";
    }
    if key.starts_with("보개_") || key.starts_with("__view_") {
        return "뷰";
    }
    "상태"
}

fn hash_json_string(value: &JsonValue) -> String {
    let canonical = value.to_string();
    let digest = blake3_hash(canonical.as_bytes());
    format!("blake3:{}", hex::encode(digest.as_bytes()))
}

fn handle_to_string(handle: ResourceHandle) -> String {
    format!("handle:{}", handle.to_hex())
}

fn fixed64_to_f64(value: Fixed64) -> f64 {
    value.raw_i64() as f64 / Fixed64::ONE_RAW as f64
}

#[cfg(test)]
mod tests {
    use super::*;

    fn envelope_mode(source: &str) -> String {
        execution_envelope_from_source(source, Some(1))
            .unwrap_or_else(|err| panic!("execution envelope for {source:?}: {err}"))
            .get("execution_mode_decision")
            .and_then(|decision| decision.get("mode"))
            .and_then(JsonValue::as_str)
            .unwrap_or_default()
            .to_string()
    }

    #[test]
    fn execution_envelope_carries_shared_parsed_mode_decision() {
        assert_eq!(envelope_mode("1 보여주기."), "oneshot");
        assert_eq!(envelope_mode("(시작)할때 { 1 보여주기. }."), "oneshot");
        assert_eq!(envelope_mode("(매마디)마다 { 1 보여주기. }."), "live");
        assert_eq!(envelope_mode("(4마디)마다 { 1 보여주기. }."), "live");
    }
}
