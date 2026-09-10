use ddonirang_lang::{
    canonicalize, canonicalize_ddl_wave1, normalize, parse_ddl_wave1, parse_v25, NormalizationLevel,
};
use ddonirang_tool::lsp::{byte_offset_to_position, LspServer, PositionEncoding, RpcMessage};
use serde_json::{json, Value};

const URI: &str = "file:///lsp-formatting.ddn";
const DDL_URI: &str = "file:///lsp-formatting.ddl";
const ONGIM_URI: &str = "file:///lsp-formatting.옮김";
const LARGE_URI: &str = "file:///lsp-formatting-large.ddn";

fn init(server: &mut LspServer) -> Value {
    let event = server
        .handle_message(RpcMessage::Request {
            id: json!(1),
            method: "initialize".into(),
            params: Some(json!({
                "capabilities": {"general": {"positionEncodings": ["utf-16"]}}
            })),
        })
        .unwrap();
    match &event.responses[0] {
        RpcMessage::Response {
            result: Ok(value), ..
        } => value.clone(),
        _ => panic!("initialize must return success: {event:?}"),
    }
}

fn open(server: &mut LspServer, source: &str, version: i64) {
    open_uri(server, URI, "ddn", source, version);
}

fn open_uri(server: &mut LspServer, uri: &str, language_id: &str, source: &str, version: i64) {
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didOpen".into(),
            params: Some(json!({
                "textDocument": {
                    "uri": uri,
                    "languageId": language_id,
                    "version": version,
                    "text": source,
                }
            })),
        })
        .unwrap();
}

fn format(server: &mut LspServer, id: i64, version: Option<i64>, identity: Option<&str>) -> Value {
    format_uri(server, id, URI, version, identity)
}

fn format_uri(
    server: &mut LspServer,
    id: i64,
    uri: &str,
    version: Option<i64>,
    identity: Option<&str>,
) -> Value {
    let mut document = json!({"uri": uri});
    if let Some(version) = version {
        document["version"] = json!(version);
    }
    if let Some(identity) = identity {
        document["snapshotIdentity"] = json!(identity);
    }
    let event = server
        .handle_message(RpcMessage::Request {
            id: json!(id),
            method: "textDocument/formatting".into(),
            params: Some(json!({"textDocument": document, "options": {}})),
        })
        .unwrap();
    match &event.responses[0] {
        RpcMessage::Response {
            result: Ok(value), ..
        } => value.clone(),
        _ => panic!("formatting must return success: {event:?}"),
    }
}

fn will_save_wait_until(
    server: &mut LspServer,
    id: i64,
    uri: &str,
    version: Option<i64>,
    identity: Option<&str>,
    reason: i64,
) -> Value {
    let mut document = json!({"uri": uri});
    if let Some(version) = version {
        document["version"] = json!(version);
    }
    if let Some(identity) = identity {
        document["snapshotIdentity"] = json!(identity);
    }
    let event = server
        .handle_message(RpcMessage::Request {
            id: json!(id),
            method: "textDocument/willSaveWaitUntil".into(),
            params: Some(json!({
                "textDocument": document,
                "reason": reason
            })),
        })
        .unwrap();
    match &event.responses[0] {
        RpcMessage::Response {
            result: Ok(value), ..
        } => value.clone(),
        _ => panic!("willSaveWaitUntil must return success: {event:?}"),
    }
}

fn range_format(server: &mut LspServer, id: i64, uri: &str, range: Value) -> Value {
    let event = server
        .handle_message(RpcMessage::Request {
            id: json!(id),
            method: "textDocument/rangeFormatting".into(),
            params: Some(json!({
                "textDocument": {"uri": uri},
                "range": range,
                "options": {}
            })),
        })
        .unwrap();
    match &event.responses[0] {
        RpcMessage::Response {
            result: Ok(value), ..
        } => value.clone(),
        _ => panic!("range formatting must return success: {event:?}"),
    }
}

fn document_symbol_ranges(server: &mut LspServer, id: i64, uri: &str) -> Vec<Value> {
    let event = server
        .handle_message(RpcMessage::Request {
            id: json!(id),
            method: "textDocument/documentSymbol".into(),
            params: Some(json!({"textDocument": {"uri": uri}})),
        })
        .unwrap();
    match &event.responses[0] {
        RpcMessage::Response {
            result: Ok(value), ..
        } => value.as_array().cloned().unwrap_or_default(),
        _ => panic!("document symbols must return success: {event:?}"),
    }
}

fn canonical(source: &str) -> String {
    let mut program = parse_v25(source, URI).expect("formatting fixture must parse");
    canonicalize(&mut program).expect("formatting fixture must canonicalize");
    normalize(&program, NormalizationLevel::N1)
}

fn ddl_canonical(source: &str) -> String {
    canonicalize_ddl_wave1(&parse_ddl_wave1(source, DDL_URI).expect("DDL fixture must parse"))
}

#[test]
fn lsp13_formatting_uses_shared_canonical_owner_and_live_snapshot() {
    let source = "첫함수 : 셈씨 := {\n\"🙂\" 보여주기.\n}\n문자 : 글 := \"🙂\".";
    let expected = canonical(source);
    assert_ne!(expected, source);
    assert_eq!(canonical(&expected), expected);

    let mut server = LspServer::new();
    let initialized = init(&mut server);
    assert_eq!(
        initialized["capabilities"]["documentFormattingProvider"],
        true
    );
    open(&mut server, source, 1);
    let identity = server
        .documents()
        .get(URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    let edits = format(&mut server, 2, Some(1), Some(&identity));
    assert_eq!(edits.as_array().unwrap().len(), 1);
    assert_eq!(edits[0]["newText"], expected);
    let end = byte_offset_to_position(source, source.len(), PositionEncoding::Utf16).unwrap();
    assert_eq!(
        edits[0]["range"],
        json!({
            "start": {"line": 0, "character": 0},
            "end": {"line": end.line, "character": end.character}
        })
    );
    assert_eq!(edits, format(&mut server, 3, Some(1), Some(&identity)));

    let canonical_source = expected.clone();
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didChange".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": 2},
                "contentChanges": [{"text": canonical_source}]
            })),
        })
        .unwrap();
    assert_eq!(format(&mut server, 4, Some(2), None), json!([]));
}

#[test]
fn lsp13_formatting_fails_closed_for_stale_and_legacy_input() {
    let source = "첫함수:셈씨 := {\n    1 돌려줘.\n}";
    let mut server = LspServer::new();
    init(&mut server);
    open(&mut server, source, 7);
    let identity = server
        .documents()
        .get(URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    assert_eq!(format(&mut server, 10, Some(6), Some(&identity)), json!([]));
    assert_eq!(
        format(&mut server, 11, Some(7), Some("sha256:stale")),
        json!([])
    );

    let legacy_equals_event = server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didChange".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": 8},
                "contentChanges": [{"text": "첫함수:셈씨 = { 1 돌려줘. }"}]
            })),
        })
        .unwrap();
    let RpcMessage::Notification {
        params: Some(params),
        ..
    } = &legacy_equals_event.responses[0]
    else {
        panic!("legacy equals must preserve a diagnostic notification");
    };
    assert_eq!(
        params["diagnostics"][0]["code"],
        "E_V25_DEFINITION_MIGRATION_REQUIRED"
    );
    assert_eq!(format(&mut server, 12, Some(8), None), json!([]));

    let legacy_chaebi_event = server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didChange".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": 9},
                "contentChanges": [{"text": "첫함수:셈씨 := { 보임 { 1 돌려줘. }. }"}]
            })),
        })
        .unwrap();
    let RpcMessage::Notification {
        params: Some(params),
        ..
    } = &legacy_chaebi_event.responses[0]
    else {
        panic!("legacy chaebi must preserve a diagnostic notification");
    };
    assert_eq!(params["diagnostics"][0]["code"], "E_BOIM_LEGACY_REMOVED");
    assert_eq!(format(&mut server, 13, Some(9), None), json!([]));
}

#[test]
fn lsp32_formatting_supports_authoritative_ddl_and_closes_open_snapshot() {
    let source = "#!한국어\n원주율:셈수 :={...}.\n\n#!日本語\n円周率:数値 :={...}.\n\n";
    let expected = ddl_canonical(source);
    assert_eq!(ddl_canonical(&expected), expected);

    let mut server = LspServer::new();
    init(&mut server);
    open_uri(&mut server, DDL_URI, "ddl", source, 1);
    let identity = server
        .documents()
        .get(DDL_URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    let edits = format_uri(&mut server, 20, DDL_URI, Some(1), Some(&identity));
    assert_eq!(edits.as_array().unwrap().len(), 1);
    assert_eq!(edits[0]["newText"], expected);
    let end = byte_offset_to_position(source, source.len(), PositionEncoding::Utf16).unwrap();
    assert_eq!(
        edits[0]["range"],
        json!({
            "start": {"line": 0, "character": 0},
            "end": {"line": end.line, "character": end.character}
        })
    );
    assert_eq!(
        edits,
        format_uri(&mut server, 21, DDL_URI, Some(1), Some(&identity))
    );

    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didClose".into(),
            params: Some(json!({"textDocument": {"uri": DDL_URI}})),
        })
        .unwrap();
    assert_eq!(format_uri(&mut server, 22, DDL_URI, None, None), json!([]));
}

#[test]
fn lsp32_formatting_is_bounded_and_cancellation_is_atomic() {
    let source = "첫함수:셈씨 := { 1 돌려줘. }";
    let mut server = LspServer::new();
    init(&mut server);
    open(&mut server, source, 1);
    let identity = server
        .documents()
        .get(URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    server
        .handle_message(RpcMessage::Notification {
            method: "$/cancelRequest".into(),
            params: Some(json!({"id": 30})),
        })
        .unwrap();
    let event = server
        .handle_message(RpcMessage::Request {
            id: json!(30),
            method: "textDocument/formatting".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": 1, "snapshotIdentity": identity},
                "options": {}
            })),
        })
        .unwrap();
    match &event.responses[0] {
        RpcMessage::Response {
            result: Err(error), ..
        } => assert_eq!(error.code, -32800),
        other => panic!("cancelled formatting must not publish edits: {other:?}"),
    }

    let oversized = format!("{}{}", source, " ".repeat(1_000_001));
    open_uri(&mut server, LARGE_URI, "ddn", &oversized, 2);
    let large_identity = server
        .documents()
        .get(LARGE_URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    assert_eq!(
        format_uri(&mut server, 31, LARGE_URI, Some(2), Some(&large_identity)),
        json!([])
    );
}

#[test]
fn lsp37_will_save_wait_until_reuses_safe_formatting_for_live_surfaces() {
    let source = "첫함수 : 셈씨 := {\n\"🙂\" 보여주기.\n}\n문자 : 글 := \"🙂\".";
    let expected = canonical(source);
    assert_ne!(expected, source);

    let mut server = LspServer::new();
    let initialized = init(&mut server);
    assert_eq!(initialized["capabilities"]["textDocumentSync"]["willSaveWaitUntil"], true);
    open(&mut server, source, 1);
    let identity = server
        .documents()
        .get(URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    assert_eq!(
        will_save_wait_until(&mut server, 60, URI, Some(1), Some(&identity), 1),
        json!([{
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 3, "character": 15}
            },
            "newText": expected.clone()
        }])
    );
    assert_eq!(
        will_save_wait_until(&mut server, 601, URI, Some(0), Some(&identity), 1),
        json!([])
    );
    assert_eq!(
        will_save_wait_until(&mut server, 602, URI, Some(1), Some("sha256:stale"), 1),
        json!([])
    );
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didChange".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": 2},
                "contentChanges": [{"text": expected}]
            })),
        })
        .unwrap();
    let current_identity = server
        .documents()
        .get(URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    assert_eq!(
        will_save_wait_until(
            &mut server,
            61,
            URI,
            Some(2),
            Some(&current_identity),
            1
        ),
        json!([])
    );
    assert_eq!(
        will_save_wait_until(&mut server, 611, URI, Some(1), Some(&current_identity), 1),
        json!([])
    );
    assert_eq!(
        will_save_wait_until(&mut server, 612, URI, Some(2), Some("sha256:stale"), 1),
        json!([])
    );

    let ddl_source =
        "#!한국어\n  원주율:셈수 :={...}.  \n\n\n#!日本語\n円周率:数値 :={...}.\n\n";
    let ongim_source =
        "#!한국어\n  원주율:셈수 :={...}.  \n\n\n#!日本語\n円周率:数値 :={...}.\n\n";
    open_uri(&mut server, DDL_URI, "ddl", ddl_source, 3);
    open_uri(&mut server, ONGIM_URI, "옮김", ongim_source, 4);
    assert_eq!(
        will_save_wait_until(&mut server, 62, DDL_URI, Some(3), None, 1)
            .as_array()
            .unwrap()
            .len(),
        1
    );
    assert_eq!(
        will_save_wait_until(&mut server, 63, ONGIM_URI, Some(4), None, 1)
            .as_array()
            .unwrap()
            .len(),
        1
    );

    server
        .handle_message(RpcMessage::Notification {
            method: "$/cancelRequest".into(),
            params: Some(json!({"id": 66})),
        })
        .unwrap();
    let cancelled = server
        .handle_message(RpcMessage::Request {
            id: json!(66),
            method: "textDocument/willSaveWaitUntil".into(),
            params: Some(json!({
                "textDocument": {"uri": ONGIM_URI, "version": 4},
                "reason": 1
            })),
        })
        .unwrap();
    match &cancelled.responses[0] {
        RpcMessage::Response {
            result: Err(error), ..
        } => assert_eq!(error.code, -32800),
        other => panic!("cancelled willSaveWaitUntil must not publish edits: {other:?}"),
    }

    let malformed = "첫함수 : 셈씨 := {";
    open_uri(&mut server, "file:///lsp-formatting.txt", "plaintext", malformed, 1);
    assert_eq!(
        will_save_wait_until(&mut server, 64, "file:///lsp-formatting.txt", Some(1), None, 1),
        json!([])
    );
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didClose".into(),
            params: Some(json!({"textDocument": {"uri": URI}})),
        })
        .unwrap();
    assert_eq!(
        will_save_wait_until(&mut server, 65, URI, None, None, 1),
        json!([])
    );
}

#[test]
fn lsp36_range_formatting_accepts_one_complete_ddn_declaration_only() {
    let source = "첫함수 : 셈씨 := {\n\"🙂\" 보여주기.\n}\n문자 : 글 := \"🙂\".";
    let mut server = LspServer::new();
    let initialized = init(&mut server);
    assert_eq!(
        initialized["capabilities"]["documentRangeFormattingProvider"],
        true
    );
    open(&mut server, source, 1);
    let symbols = document_symbol_ranges(&mut server, 40, URI);
    assert_eq!(symbols.len(), 2);
    let first_range = symbols[0]["range"].clone();
    let first_start = source.find("첫함수").unwrap();
    let first_end = source.find("}\n").unwrap() + 1;
    assert_eq!(
        first_range,
        json!({
            "start": {"line": 0, "character": 0},
            "end": {"line": 2, "character": 1}
        })
    );
    assert_eq!(
        range_format(&mut server, 41, URI, first_range.clone()),
        json!([{
            "range": first_range,
            "newText": canonical(&source[first_start..first_end])
        }])
    );
    assert_eq!(
        range_format(
            &mut server,
            42,
            URI,
            json!({
                "start": {"line": 0, "character": 1},
                "end": {"line": 2, "character": 1}
            })
        ),
        json!([])
    );
    let second_range = symbols[1]["range"].clone();
    let second_start = source.find("문자").unwrap();
    assert_eq!(
        range_format(&mut server, 43, URI, second_range.clone()),
        json!([{
            "range": second_range,
            "newText": canonical(&source[second_start..])
        }])
    );

    let updated = "첫함수 : 셈씨 := {\n\"🙂\" 보여주기.\n}\n  문자 : 글 := \"🙂\".  ";
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didChange".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": 2},
                "contentChanges": [{"text": updated}]
            })),
        })
        .unwrap();
    let updated_symbols = document_symbol_ranges(&mut server, 44, URI);
    let updated_range = updated_symbols[1]["range"].clone();
    let updated_start = updated.find("문자").unwrap();
    assert_eq!(
        range_format(&mut server, 45, URI, updated_range.clone()),
        json!([{
            "range": updated_range,
            "newText": canonical(&updated[updated_start..])
        }])
    );
}

#[test]
fn lsp36_range_formatting_supports_ddl_sections_and_lifecycle_guards() {
    let source = "#!한국어\n  원주율:셈수 :={...}.  \n\n\n#!日本語\n円周率:数値 :={...}.\n\n";
    let mut server = LspServer::new();
    init(&mut server);
    open_uri(&mut server, DDL_URI, "ddl", source, 3);
    let second_header = source.find("#!日本語").unwrap();
    let section_end =
        byte_offset_to_position(source, second_header, PositionEncoding::Utf16).unwrap();
    let first_section_range = json!({
        "start": {"line": 0, "character": 0},
        "end": {"line": section_end.line, "character": section_end.character}
    });
    let edits = range_format(&mut server, 50, DDL_URI, first_section_range.clone());
    assert_eq!(edits.as_array().unwrap().len(), 1);
    assert_eq!(edits[0]["range"], first_section_range);
    assert_eq!(edits[0]["newText"], {
        let canonical = ddl_canonical(source);
        let canonical_second_header = canonical.find("#!日本語").unwrap();
        canonical[..canonical_second_header].to_string()
    });

    let stale = server
        .handle_message(RpcMessage::Request {
            id: json!(51),
            method: "textDocument/rangeFormatting".into(),
            params: Some(json!({
                "textDocument": {"uri": DDL_URI, "version": 2},
                "range": first_section_range.clone(),
                "options": {}
            })),
        })
        .unwrap();
    match &stale.responses[0] {
        RpcMessage::Response {
            result: Err(error), ..
        } => assert_eq!(error.code, -32801),
        other => panic!("stale range formatting must fail closed: {other:?}"),
    }
    let stale_identity = server
        .documents()
        .get(DDL_URI)
        .unwrap()
        .identity
        .as_str()
        .to_string();
    let stale_identity_event = server
        .handle_message(RpcMessage::Request {
            id: json!(53),
            method: "textDocument/rangeFormatting".into(),
            params: Some(json!({
                "textDocument": {
                    "uri": DDL_URI,
                    "version": 3,
                    "snapshotIdentity": "sha256:stale"
                },
                "range": first_section_range.clone(),
                "options": {}
            })),
        })
        .unwrap();
    assert_ne!(stale_identity, "sha256:stale");
    match &stale_identity_event.responses[0] {
        RpcMessage::Response {
            result: Err(error), ..
        } => assert_eq!(error.code, -32802),
        other => panic!("stale range snapshot must fail closed: {other:?}"),
    }
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didClose".into(),
            params: Some(json!({"textDocument": {"uri": DDL_URI}})),
        })
        .unwrap();
    assert_eq!(
        range_format(
            &mut server,
            52,
            DDL_URI,
            json!({"start": {"line": 0, "character": 0}, "end": {"line": 1, "character": 0}})
        ),
        json!([])
    );
}
