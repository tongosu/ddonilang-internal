# DDN-LSP13 Shared Current-Document Formatting — Handoff R1

## Binding

- Unit: `LSP13_SHARED_CURRENT_DOCUMENT_FORMATTING`
- LSP12 product: `cb4aafef7f4f9bc32522b1708e4eabc684f1f9f1`
- LSP12 handoff: `ac770f4cb794a8bf51e46f49198ad7a46e3ea577`
- LSP13 product commit: `1e0cf60cec5f59ce907e7608a05234df2ab9f00c`
- Product tree: `89e7b4b0c154c80d7d10a71f15981a6138d98154`
- Product parent: `ac770f4cb794a8bf51e46f49198ad7a46e3ea577`
- Review state: `IMPLEMENTED_PENDING_REVIEW`; no LSP13 independent PASS is claimed.

## Shared owner and scope

Formatting uses only the existing V25 language owner:

`parse_v25 -> canonicalize -> normalize(N1)`

The LSP layer adds no parser, formatter, syntax-rewrite authority, alias, migration, filesystem lookup, remote dependency, or source upload. It reads only the current `DocumentStore` snapshot, verifies optional version and snapshot identity bindings, and returns one full-document `TextEdit` or `[]`.

Changed exactly these task-owned paths:

- `tool/src/lsp/server.rs`
- `tool/tests/lsp_formatting.rs`
- `tests/run_lsp0_transport_document_sync_check.py`

`tool/src/lib.rs`, public CLI/WASM/UI, language source, runtime source, SSOT/SPEC, and foreign dirty paths were not changed.

## DoD evidence

- `documentFormattingProvider = true` in initialize.
- Noncanonical spacing/indentation uses the shared canonical owner.
- Canonical output is parse/canonicalize/normalize byte-stable.
- Canonical input returns `edits=[]`.
- One full-document edit is returned when changed.
- Full-document end range is negotiated UTF-16 and covers Korean/non-BMP source bytes.
- didChange version 2 is formatted from the current snapshot only.
- Stale version and stale snapshot identity return `[]`.
- Legacy `=` and legacy `보임 {}` return `[]`; existing diagnostics retain `E_V25_DEFINITION_MIGRATION_REQUIRED` and `E_BOIM_LEGACY_REMOVED`.
- Persistent transport returns formatting response before EOF; repeated request result is byte-stable.

## Exact mutation evidence

Each mutation was applied alone, run, restored immediately, and followed by the same focused GREEN test.

### M1 — separate local formatter

```diff
-        let canonical = normalize(&program, NormalizationLevel::N1);
+        let canonical = source.trim().to_string();
```

Command: `cargo test -p ddonirang-tool --test lsp_formatting --offline --quiet`

RED: `lsp13_formatting_uses_shared_canonical_owner_and_live_snapshot` failed; left edit count `0`, expected `1`.

Restore: `normalize(&program, NormalizationLevel::N1)` restored. GREEN: `2 passed; 0 failed`.

### M2 — UTF-16 range downgraded to UTF-8

```diff
-            encoding,
+            PositionEncoding::Utf8,
```

Command: same focused formatting command.

RED: full-range end character was `23`, expected UTF-16 character `15`.

Restore: negotiated `encoding` restored. GREEN: `2 passed; 0 failed`.

### M3 — stale version/snapshot guard bypass

```diff
-        if snapshot.language_id != "ddn"
-            || (document.contains_key("version")
-                && document.get("version").and_then(Value::as_i64) != Some(snapshot.version))
-            || (document.contains_key("snapshotIdentity")
-                && document.get("snapshotIdentity").and_then(Value::as_str)
-                    != Some(snapshot.identity.as_str()))
-        {
+        if snapshot.language_id != "ddn" {
```

Command: same focused formatting command.

RED: stale-input test returned one full-document edit instead of `[]`.

Restore: language, version, and snapshot identity guard restored. GREEN: `2 passed; 0 failed`.

## Verification

```text
cargo test -p ddonirang-tool --test lsp_formatting --offline --quiet
2 passed; 0 failed

cargo test -p ddonirang-tool --test lsp_formatting --test lsp_document_symbol --test lsp_open_document_navigation --test lsp_rename --test lsp_definition --test lsp_references --test lsp_document_highlight --test lsp_signature_help --test lsp_semantic_tokens --test lsp_hover --test lsp_diagnostics --test lsp_completion --offline --quiet
all listed test groups passed

python tests/run_lsp0_transport_document_sync_check.py
F13_BLACKBOX_FORMATTING_BEFORE_EOF=PASS
LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS

git archive 1e0cf60c -- Cargo.toml Cargo.lock .cargo core lang numeric proof symbolic tool tests
cargo check --manifest-path I:\home\urihanl\ddn\codex\build\lsp13-clean-snapshot-r1\tool\Cargo.toml --bin ddonirang-lsp --offline
Finished `dev` profile

git diff --check -- tool/src/lsp/server.rs tool/tests/lsp_formatting.rs tests/run_lsp0_transport_document_sync_check.py
PASS
```

Final task-file SHA-256:

```text
tool/src/lsp/server.rs = 9C5035CB7ED4ECEC040E2BC9A7FAE05FB8F5DE51FA71D9AAAD171C11ACC81189
tool/tests/lsp_formatting.rs = D9E008E21376240F8EF11D14DDFB922ACC9BEBDF45D9A4CC04681A2AD2E4CE31
tests/run_lsp0_transport_document_sync_check.py = 25502CEBF5E574DF2032ACE46A0F5E2D25E4588DFEA09CD4838DC8E3B645B96A
```

## Custody

- New dependency: `0`
- New pack: `0`
- New runner: `0`; existing runner extended
- Filesystem crawl: `0`
- Source upload / remote dependency: `0 / 0`
- Foreign dirty touched: `0`
- Protected untracked changed: `0`
- Product push: `NO` at handoff creation
- Author and committer: `tongosu <tongosu@myarts.kr>`
- Prohibited trailer count: `0`
- Next unit: not started; wait for LSP13 review boundary before selecting the next non-overlapping user workflow.
