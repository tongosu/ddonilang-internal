use serde::Deserialize;
use serde_json::{json, Value as JsonValue};
use sha2::{Digest, Sha256};
use std::{env, fs, path::{Path, PathBuf}};

#[derive(Debug, Deserialize)]
struct Manifest {
    schema: String,
    source_profile_identity: String,
    cases: Vec<Case>,
}

#[derive(Debug, Deserialize)]
struct Case {
    id: String,
    path: String,
    fixture_sha256: String,
    fixture_kind: String,
    #[serde(default)]
    canon_roundtrip: bool,
}

fn sha256(data: &[u8]) -> String {
    hex::encode(Sha256::digest(data))
}

fn read_source(pack: &Path, case: &Case) -> Result<Option<String>, String> {
    let path = pack.join(&case.path);
    let bytes = fs::read(&path).map_err(|err| format!("{}: {err}", path.display()))?;
    if sha256(&bytes) != case.fixture_sha256 {
        return Err(format!("E_FIXTURE_HASH_MISMATCH:{}", case.id));
    }
    match case.fixture_kind.as_str() {
        "raw_utf8" => String::from_utf8(bytes)
            .map(Some)
            .map_err(|_| format!("E_FIXTURE_INVALID_UTF8:{}", case.id)),
        "transport_json" => {
            let transport: JsonValue = serde_json::from_slice(&bytes)
                .map_err(|err| format!("E_TRANSPORT_PARSE:{}:{err}", case.id))?;
            match transport.get("encoding").and_then(JsonValue::as_str) {
                Some("utf-8-json-string") => transport
                    .get("source_text")
                    .and_then(JsonValue::as_str)
                    .map(|value| Some(value.to_string()))
                    .ok_or_else(|| format!("E_TRANSPORT_SOURCE_MISSING:{}", case.id)),
                Some("hex-bytes") => {
                    let raw = transport
                        .get("bytes_hex")
                        .and_then(JsonValue::as_str)
                        .ok_or_else(|| format!("E_TRANSPORT_HEX_MISSING:{}", case.id))?;
                    let decoded = hex::decode(raw)
                        .map_err(|_| format!("E_TRANSPORT_HEX_INVALID:{}", case.id))?;
                    match String::from_utf8(decoded) {
                        Ok(text) => Ok(Some(text)),
                        Err(_) => Ok(None),
                    }
                }
                _ => Err(format!("E_TRANSPORT_ENCODING_UNSUPPORTED:{}", case.id)),
            }
        }
        _ => Err(format!("E_FIXTURE_KIND_UNSUPPORTED:{}", case.id)),
    }
}

fn parse_error_payload(error: String) -> JsonValue {
    serde_json::from_str(&error).unwrap_or_else(|_| json!({"raw_error": error}))
}

fn run_case(source: &str, path: &str, profile: &str) -> JsonValue {
    match ddonirang_tool::runtime_surface::run_summary_from_supported_source_profile(
        source,
        path,
        Some(1),
        Some(profile),
    ) {
        Ok(payload) => json!({"outcome": "ACCEPTED", "payload": payload}),
        Err(error) => json!({"outcome": "REJECTED", "diagnostic": parse_error_payload(error)}),
    }
}

fn canon_case(source: &str, profile: &str) -> JsonValue {
    match ddonirang_tool::runtime_surface::canonicalize_shared_source_with_supported_profile(
        source,
        Some(profile),
    ) {
        Ok(first) => match ddonirang_tool::runtime_surface::canonicalize_shared_source_with_supported_profile(
            &first.ddn,
            Some(profile),
        ) {
            Ok(second) => json!({
                "first_outcome": "ACCEPTED",
                "first_ddn": first.ddn,
                "second_outcome": "ACCEPTED",
                "second_ddn": second.ddn,
                "roundtrip_equal": first.ddn == second.ddn,
            }),
            Err(error) => json!({
                "first_outcome": "ACCEPTED",
                "first_ddn": first.ddn,
                "second_outcome": "REJECTED",
                "second_error": error,
                "roundtrip_equal": false,
            }),
        },
        Err(error) => json!({
            "first_outcome": "REJECTED",
            "first_error": error,
            "second_outcome": "NOT_RUN",
            "roundtrip_equal": false,
        }),
    }
}

fn runtime_canon_reparse(run: &JsonValue, path: &str, profile: &str) -> Option<JsonValue> {
    let canonical = run
        .get("payload")?
        .get("canonical_ddn")?
        .as_str()?;
    let reparsed = run_case(canonical, path, profile);
    Some(json!({
        "canonical_ddn_sha256": sha256(canonical.as_bytes()),
        "canonical_ddn": canonical,
        "reparse": reparsed,
        "reparse_green": reparsed.get("outcome").and_then(JsonValue::as_str) == Some("ACCEPTED"),
    }))
}

fn main() -> Result<(), String> {
    let manifest_path = env::args().nth(1).ok_or("manifest path required")?;
    let manifest_path = PathBuf::from(manifest_path);
    let pack = manifest_path.parent().ok_or("manifest parent missing")?;
    let manifest_bytes = fs::read(&manifest_path).map_err(|err| err.to_string())?;
    let manifest: Manifest = serde_json::from_slice(&manifest_bytes).map_err(|err| err.to_string())?;
    let mut rows = Vec::new();
    for case in &manifest.cases {
        let source = read_source(pack, case)?;
        let source_sha256 = source.as_ref().map(|value| sha256(value.as_bytes()));
        let run = source
            .as_ref()
            .map(|value| run_case(value, &case.path, &manifest.source_profile_identity))
            .unwrap_or_else(|| json!({
                "outcome": "NO_TEXT_SURFACE",
                "diagnostic": {"code": "E_INVALID_UTF8_BEFORE_STRING_API"}
            }));
        let canon = if case.canon_roundtrip {
            source
                .as_ref()
                .map(|value| canon_case(value, &manifest.source_profile_identity))
        } else {
            None
        };
        let runtime_canon_reparse = if case.canon_roundtrip {
            runtime_canon_reparse(&run, &case.path, &manifest.source_profile_identity)
        } else {
            None
        };
        rows.push(json!({
            "id": case.id,
            "fixture_sha256": case.fixture_sha256,
            "source_sha256": source_sha256,
            "run": run,
            "canon": canon,
            "runtime_canon_reparse": runtime_canon_reparse,
        }));
    }
    let report = json!({
        "schema": "ddn.vc06.native_probe_report.v1",
        "manifest_schema": manifest.schema,
        "manifest_sha256": sha256(&manifest_bytes),
        "source_profile_identity": manifest.source_profile_identity,
        "cases": rows,
    });
    println!("{}", serde_json::to_string(&report).map_err(|err| err.to_string())?);
    Ok(())
}
