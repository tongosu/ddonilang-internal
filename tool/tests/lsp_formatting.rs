use ddonirang_lang::{
    canonicalize, canonicalize_ddl_wave1, normalize, parse_ddl_wave1, parse_v25, NormalizationLevel,
};
use ddonirang_tool::lsp::{byte_offset_to_position, LspServer, PositionEncoding, RpcMessage};
use serde_json::{json, Value};

const URI: &str = "file:///lsp-formatting.ddn";
const DDL_URI: &str = "file:///lsp-formatting.ddl";
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
