# LSP-0 transport/document sync v1

이 팩은 또니랑 LSP-0의 좁은 제품 수직만 검증한다.

포함 범위:

- Content-Length 기반 JSON-RPC framing과 partial/multiple frame 처리
- `initialize` → `initialized` → `didOpen`/`didChange`/`didClose` → `shutdown` → `exit`
- 문서 version 증가, atomic multi-change, stale snapshot과 cancellation 거부
- 협상된 UTF-8·UTF-16·UTF-32 line/character projection
- `SourceSnapshotIdentity × ByteRange` projection consumer 경계

completion, hover, definition, references, rename, formatting, CodeFix, semantic tokens와
DDN diagnostic 의미는 지원하지 않는다. placeholder consumer는 언어 의미 권위나 제품
언어 지원 완료를 뜻하지 않는다.

실행:

```powershell
$env:CARGO_TARGET_DIR='I:/home/urihanl/ddn/codex/build/lsp0-transport-document-sync-r1'
cargo check --offline --manifest-path tool/Cargo.toml --lib
cargo test --offline --manifest-path tool/Cargo.toml lsp
cargo test --offline --manifest-path tool/Cargo.toml --test lsp0_transport_document_sync
python tests/run_lsp0_transport_document_sync_check.py
```

golden JSONL에는 절대경로, 시간, PID, 임시경로를 넣지 않는다.
