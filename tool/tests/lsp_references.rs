use ddonirang_tool::lsp::{
    byte_offset_to_position, LspServer, PositionEncoding, RpcMessage, ServerEvent,
};
use serde_json::{json, Value};

const URI: &str = "file:///lsp-references.ddn";
const SOURCE: &str = "(문자:글) 첫함수:셈씨 := { 1 돌려줘. }\n둘함수:셈씨 := { (\"🙂\") 첫함수. }\n셋함수:셈씨 := { 첫함수. }";

fn init(server: &mut LspServer) -> ServerEvent {
    server
        .handle_message(RpcMessage::Request {
            id: json!(1),
            method: "initialize".into(),
            params: Some(json!({
                "capabilities": {"general": {"positionEncodings": ["utf-16", "utf-8"]}}
            })),
        })
        .unwrap()
}

fn open(server: &mut LspServer, source: &str, version: i64) -> ServerEvent {
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didOpen".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "languageId": "ddn", "version": version, "text": source}
            })),
        })
        .unwrap()
}

fn change(server: &mut LspServer, source: &str, version: i64) -> ServerEvent {
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didChange".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": version},
                "contentChanges": [{"text": source}]
            })),
        })
        .unwrap()
}

fn close(server: &mut LspServer) -> ServerEvent {
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didClose".into(),
            params: Some(json!({"textDocument": {"uri": URI}})),
        })
        .unwrap()
}

fn open_uri(server: &mut LspServer, uri: &str, source: &str, version: i64) -> ServerEvent {
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didOpen".into(),
            params: Some(json!({
                "textDocument": {"uri": uri, "languageId": "ddn", "version": version, "text": source}
            })),
        })
        .unwrap()
}

fn change_uri(server: &mut LspServer, uri: &str, source: &str, version: i64) -> ServerEvent {
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didChange".into(),
            params: Some(json!({
                "textDocument": {"uri": uri, "version": version},
                "contentChanges": [{"text": source}]
            })),
        })
        .unwrap()
}

fn close_uri(server: &mut LspServer, uri: &str) -> ServerEvent {
    server
        .handle_message(RpcMessage::Notification {
            method: "textDocument/didClose".into(),
            params: Some(json!({"textDocument": {"uri": uri}})),
        })
        .unwrap()
}

fn references_request(
    server: &mut LspServer,
    id: i64,
    uri: &str,
    position: Value,
    version: Option<i64>,
    include_declaration: bool,
) -> ServerEvent {
    let mut document = json!({"uri": uri});
    if let Some(version) = version {
        document["version"] = json!(version);
    }
    server
        .handle_message(RpcMessage::Request {
            id: json!(id),
            method: "textDocument/references".into(),
            params: Some(json!({
                "textDocument": document,
                "position": position,
                "context": {"includeDeclaration": include_declaration}
            })),
        })
        .unwrap()
}

fn occurrence(source: &str, needle: &str, ordinal: usize) -> usize {
    source
        .match_indices(needle)
        .nth(ordinal)
        .map(|(byte, _)| byte)
        .unwrap()
}

fn position(source: &str, byte: usize) -> Value {
    let position = byte_offset_to_position(source, byte, PositionEncoding::Utf16).unwrap();
    json!({"line": position.line, "character": position.character})
}

fn location(source: &str, byte: usize, name: &str) -> Value {
    let start = position(source, byte);
    let end = position(source, byte + name.len());
    json!({"uri": URI, "range": {"start": start, "end": end}})
}

fn references(
    server: &mut LspServer,
    id: i64,
    source: &str,
    needle: &str,
    ordinal: usize,
    version: Option<i64>,
    include_declaration: bool,
) -> Value {
    let byte = occurrence(source, needle, ordinal);
    let mut document = json!({"uri": URI});
    if let Some(version) = version {
        document["version"] = json!(version);
    }
    let position = position(source, byte);
    let event = server
        .handle_message(RpcMessage::Request {
            id: json!(id),
            method: "textDocument/references".into(),
            params: Some(json!({
                "textDocument": document,
                "position": position,
                "context": {"includeDeclaration": include_declaration}
            })),
        })
        .unwrap();
    match &event.responses[0] {
        RpcMessage::Response {
            result: Ok(result), ..
        } => result.clone(),
        _ => panic!("references request must return a success response: {event:?}"),
    }
}

#[test]
fn i01_identity_order_utf16_and_declaration_context() {
    let mut server = LspServer::new();
    let initialized = init(&mut server);
    assert_eq!(
        initialized.responses[0].clone_response().unwrap()["capabilities"]
            ["referencesProvider"],
        true
    );
    open(&mut server, SOURCE, 1);

    let without_declaration = references(&mut server, 2, SOURCE, "첫함수", 1, Some(1), false);
    assert_eq!(
        without_declaration,
        json!([
            location(SOURCE, occurrence(SOURCE, "첫함수", 1), "첫함수"),
            location(SOURCE, occurrence(SOURCE, "첫함수", 2), "첫함수"),
        ])
    );
    let with_declaration = references(&mut server, 3, SOURCE, "첫함수", 1, Some(1), true);
    assert_eq!(
        with_declaration,
        json!([
            location(SOURCE, occurrence(SOURCE, "첫함수", 0), "첫함수"),
            location(SOURCE, occurrence(SOURCE, "첫함수", 1), "첫함수"),
            location(SOURCE, occurrence(SOURCE, "첫함수", 2), "첫함수"),
        ])
    );
    assert_eq!(
        references(&mut server, 4, SOURCE, "첫함수", 2, Some(1), true),
        with_declaration
    );
}

#[test]
fn i02_change_stale_malformed_and_close_empty() {
    let mut server = LspServer::new();
    init(&mut server);
    open(&mut server, SOURCE, 1);
    let changed = "새함수:셈씨 := { 1 돌려줘. }\n다른함수:셈씨 := { 새함수. }";
    change(&mut server, changed, 2);

    let stale = server
        .handle_message(RpcMessage::Request {
            id: json!(2),
            method: "textDocument/references".into(),
            params: Some(json!({
                "textDocument": {"uri": URI, "version": 1},
                "position": {"line": 0, "character": 0},
                "context": {"includeDeclaration": true}
            })),
        })
        .unwrap();
    assert!(matches!(
        &stale.responses[0],
        RpcMessage::Response {
            result: Err(error), ..
        } if error.code == -32801
    ));

    let changed_reference = occurrence(changed, "새함수", 1);
    assert_eq!(
        references(
            &mut server,
            3,
            changed,
            "새함수",
            1,
            Some(2),
            true,
        ),
        json!([
            location(changed, occurrence(changed, "새함수", 0), "새함수"),
            location(changed, changed_reference, "새함수"),
        ])
    );

    let legacy = "새함수:셈씨 = { 1 돌려줘. }";
    change(&mut server, legacy, 3);
    assert_eq!(
        references(&mut server, 4, legacy, "새함수", 0, Some(3), true),
        json!([])
    );
    close(&mut server);
    assert_eq!(
        server
            .handle_message(RpcMessage::Request {
                id: json!(5),
                method: "textDocument/references".into(),
                params: Some(json!({
                    "textDocument": {"uri": URI},
                    "position": {"line": 0, "character": 0},
                    "context": {"includeDeclaration": true}
                })),
            })
            .unwrap()
            .responses[0]
            .clone_response()
            .unwrap(),
        json!([])
    );
}

#[test]
fn lsp25_open_document_cross_file_references_contract() {
    const URI_A: &str = "file:///lsp25-a.ddn";
    const URI_B: &str = "file:///lsp25-b.ddn";
    const URI_C: &str = "file:///lsp25-c.ddn";
    const SOURCE_A: &str = "공유함수:셈씨 := { 1 돌려줘. }\n";
    const SOURCE_B: &str = "(값:새값, 앞:글 = \"🙂\") 호출함수:셈씨 := { 공유함수. }\n";
    const SOURCE_C: &str = "셋함수:셈씨 := { 공유함수. }\n";
    const SOURCE_B_CHANGED: &str = "(값:새값, 앞:글 = \"🙂\") 호출함수:셈씨 := { 1 돌려줘. }\n";

    let mut server = LspServer::new();
    init(&mut server);
    open_uri(&mut server, URI_A, SOURCE_A, 1);
    open_uri(&mut server, URI_B, SOURCE_B, 1);
    open_uri(&mut server, URI_C, SOURCE_C, 1);

    let stale_snapshot = server
        .handle_message(RpcMessage::Request {
            id: json!(19),
            method: "textDocument/references".into(),
            params: Some(json!({
                "textDocument": {
                    "uri": URI_B,
                    "version": 1,
                    "snapshotIdentity": "sha256:stale"
                },
                "position": position(SOURCE_B, occurrence(SOURCE_B, "공유함수", 0)),
                "context": {"includeDeclaration": true}
            })),
        })
        .unwrap();
    assert!(matches!(
        &stale_snapshot.responses[0],
        RpcMessage::Response { result: Err(error), .. } if error.code == -32802
    ));

    let b_reference = occurrence(SOURCE_B, "공유함수", 0);
    let all = references_request(
        &mut server,
        20,
        URI_B,
        position(SOURCE_B, b_reference),
        Some(1),
        true,
    );
    let all = all.responses[0].clone_response().unwrap();
    assert_eq!(
        all.as_array().unwrap().iter().map(|item| item["uri"].as_str().unwrap()).collect::<Vec<_>>(),
        vec![URI_A, URI_B, URI_C]
    );
    assert_eq!(
        all[1]["range"],
        json!({
            "start": position(SOURCE_B, b_reference),
            "end": position(SOURCE_B, b_reference + "공유함수".len())
        })
    );
    assert_eq!(all, references_request(
        &mut server,
        21,
        URI_B,
        position(SOURCE_B, b_reference),
        Some(1),
        true,
    ).responses[0].clone_response().unwrap());

    let without_declaration = references_request(
        &mut server,
        22,
        URI_B,
        position(SOURCE_B, b_reference),
        Some(1),
        false,
    ).responses[0].clone_response().unwrap();
    assert_eq!(
        without_declaration.as_array().unwrap().iter().map(|item| item["uri"].as_str().unwrap()).collect::<Vec<_>>(),
        vec![URI_B, URI_C]
    );

    change_uri(&mut server, URI_B, SOURCE_B_CHANGED, 2);
    let changed = references_request(
        &mut server,
        23,
        URI_C,
        position(SOURCE_C, occurrence(SOURCE_C, "공유함수", 0)),
        Some(1),
        true,
    ).responses[0].clone_response().unwrap();
    assert_eq!(
        changed.as_array().unwrap().iter().map(|item| item["uri"].as_str().unwrap()).collect::<Vec<_>>(),
        vec![URI_A, URI_C]
    );

    close_uri(&mut server, URI_C);
    let closed = references_request(
        &mut server,
        24,
        URI_A,
        position(SOURCE_A, occurrence(SOURCE_A, "공유함수", 0)),
        Some(1),
        true,
    ).responses[0].clone_response().unwrap();
    assert_eq!(
        closed.as_array().unwrap().iter().map(|item| item["uri"].as_str().unwrap()).collect::<Vec<_>>(),
        vec![URI_A]
    );

    server.cancel_request(&json!(25));
    let cancelled = references_request(
        &mut server,
        25,
        URI_A,
        position(SOURCE_A, occurrence(SOURCE_A, "공유함수", 0)),
        Some(1),
        true,
    );
    assert!(matches!(
        cancelled.responses[0],
        RpcMessage::Response { result: Err(ref error), .. } if error.code == -32800
    ));
}

#[test]
fn lsp25_duplicate_definition_identity_fails_closed_and_result_bound_is_deterministic() {
    const URI_A: &str = "file:///lsp25-duplicate-a.ddn";
    const URI_B: &str = "file:///lsp25-duplicate-b.ddn";
    const SOURCE_A: &str = "겹침:셈씨 := { 1 돌려줘. }\n";
    const SOURCE_B: &str = "겹침:셈씨 := { 2 돌려줘. }\n호출:셈씨 := { 겹침. }\n";
    let mut server = LspServer::new();
    init(&mut server);
    open_uri(&mut server, URI_A, SOURCE_A, 1);
    open_uri(&mut server, URI_B, SOURCE_B, 1);
    assert_eq!(
        references_request(
            &mut server,
            30,
            URI_B,
            position(SOURCE_B, occurrence(SOURCE_B, "겹침", 1)),
            Some(1),
            true,
        ).responses[0].clone_response().unwrap(),
        json!([])
    );

    let mut many = String::from("대상:셈씨 := { 1 돌려줘. }\n");
    for index in 0..1000 {
        many.push_str(&format!("호출{index}:셈씨 := {{ 대상. }}\n"));
    }
    const URI_MANY: &str = "file:///lsp25-many.ddn";
    open_uri(&mut server, URI_MANY, &many, 1);
    let bounded = references_request(
        &mut server,
        31,
        URI_MANY,
        position(&many, occurrence(&many, "대상", 1)),
        Some(1),
        true,
    ).responses[0].clone_response().unwrap();
    assert_eq!(bounded.as_array().unwrap().len(), 1_000);
    assert_eq!(bounded, references_request(
        &mut server,
        32,
        URI_MANY,
        position(&many, occurrence(&many, "대상", 1)),
        Some(1),
        true,
    ).responses[0].clone_response().unwrap());
}

trait RpcMessageTestExt {
    fn clone_response(&self) -> Option<Value>;
}

impl RpcMessageTestExt for RpcMessage {
    fn clone_response(&self) -> Option<Value> {
        match self {
            RpcMessage::Response {
                result: Ok(value), ..
            } => Some(value.clone()),
            _ => None,
        }
    }
}
