# DDN-LSP15-OPEN-DOCUMENT-CALL-HIERARCHY-R1

## Identity

- active product unit: `textDocument/prepareCallHierarchy`, `callHierarchy/incomingCalls`, `callHierarchy/outgoingCalls`
- predecessor product: `26438f74aab1ce9dc17a3aa21589c17006512cc4`
- product fixed: `9e3574b5cb99dad171d212d3aa813c0e87a14054`
- product tree: `4e2822891ca96c3c3f6c2c0f0728e448154cadd8`
- product parent: `26438f74aab1ce9dc17a3aa21589c17006512cc4`
- semantic owner: existing `DocumentStore` and `tool/src/lsp/symbol.rs`; no filesystem index, closed-document cache, parser, registry, dependency, `tool/src/lib.rs`, `lang`, `core`, public CLI/WASM, SSOT, or SPEC change

## Product behavior

- initialize declares `callHierarchyProvider`.
- prepare resolves a declaration or an AST-resolved call site to one sealed callable item containing URI, current document version, current snapshot identity, and callable/definition identity.
- incoming and outgoing calls are built only from currently open documents, in URI order and source order. Same-document, cross-document, recursive one-edge, Korean/emoji UTF-16, didChange, didClose, comment/string exclusion, and duplicate identity fail-closed behavior are covered.
- payload version/snapshot validation rejects stale items. Unknown, closed, or ambiguous items produce null/empty results.
- no recursive expansion or unbounded call graph cache is retained.

## Focused and black-box verification

Commands:

```text
cargo test -p ddonirang-tool --test lsp_open_document_navigation --offline --quiet
python tests/run_lsp0_transport_document_sync_check.py
rustfmt --edition 2021 --check tool/src/lsp/symbol.rs tool/src/lsp/server.rs tool/tests/lsp_open_document_navigation.rs
git diff --check
cargo check --manifest-path tool/Cargo.toml --bin ddonirang-lsp --offline
```

Results:

- focused call-hierarchy/navigation suite: `4 passed`
- black-box persistent transport: `ST20_BLACKBOX_OPEN_DOCUMENT_NAVIGATION_BEFORE_EOF=PASS`; final `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`
- applicable LSP definition, references, rename, document symbol, open-document navigation, signature help, semantic tokens, hover, diagnostics, completion, formatting, and document highlight suites: all passed
- changed-file rustfmt check: `PASS`
- product diff check: `PASS`
- current dirty-root cargo check: blocked by pre-existing foreign `lang/core` API mismatch (`UnitDim::{AXIS_COUNT,exponents,from_exponents}`, `Fixed64::parse_decimal_exact`); no foreign path was changed
- clean immutable source snapshot `I:\home\urihanl\ddn\codex\build\lsp15-clean-snapshot-r1-zip`: `cargo check --manifest-path tool/Cargo.toml --bin ddonirang-lsp --offline` `PASS`

## Mutation evidence

Each mutation was applied alone, tested immediately, restored byte-exactly, then the same focused test returned GREEN.

### M1 — name-only binding guard

Target: `tool/src/lsp/symbol.rs`, `call_hierarchy_call_at_position`.

Exact mutation hunk:

```diff
-    Ok(collect_call_hierarchy_calls(snapshot)?
-        .into_iter()
-        .find(|call| call.range.start <= cursor && cursor < call.range.end))
+    let calls = collect_call_hierarchy_calls(snapshot)?;
+    if let Some(call) = calls.into_iter().find(|call| call.range.start <= cursor && cursor < call.range.end) {
+        return Ok(Some(call));
+    }
+    let source = snapshot.text().map_err(|_| SymbolError::InvalidUtf8)?;
+    let tokens = Lexer::new(source).tokenize().map_err(|_| SymbolError::InvalidUtf8)?;
+    let Some(token) = token_at(&tokens, cursor) else { return Ok(None); };
+    let name = token_name(token)
+        .or_else(|| token.raw.strip_prefix('"').and_then(|raw| raw.strip_suffix('"')))
+        .filter(|name| !name.is_empty())
+        .unwrap_or_default();
+    if name.is_empty() { return Ok(None); }
+    Ok(Some(CallHierarchyCall { caller_identity: String::new(), callee_name: name.to_string(), range: ByteRange { start: token.span.start, end: token.span.end } }))
```

The final mutation used the equivalent raw quoted-string fallback. The existing string false-positive assertion returned a non-null callable and produced RED. Original SHA-256 before mutation and after restore: `78AE19C082AC4F0F4D8622339BFDBF7D5C575926989BC97BE39832BABCD04804`.

### M2 — closed-document retention

Target: `tool/src/lsp/document_store.rs`, `DocumentStore::close`.

Exact mutation hunk:

```diff
-        self.documents.remove(uri)
+        self.documents.get(uri).cloned()
```

The closed declaration remained available and the focused lifecycle assertions returned a non-null definition/call-hierarchy item. RED. Exact restored SHA-256: `B2D1B815CFFBD609C1C8D01D55F9CAE3D7F62FE17156D661F846F203DE9BFA87`.

### M3 — stale payload version/snapshot guard

Target: `tool/src/lsp/server.rs`, `call_hierarchy_payload`.

Exact mutation hunks:

```diff
-        if snapshot.version != version || snapshot.identity.as_str() != snapshot_identity {
+        if false && (snapshot.version != version || snapshot.identity.as_str() != snapshot_identity) {
```

```diff
-                    && symbol.document_version == version
-                    && symbol.snapshot_identity == snapshot_identity
```

The old declaration item was accepted after a target document version change and incoming calls became non-empty. RED. Original SHA-256 before mutation and after restore: `1493F6EC103631ED3782B0502B1580EAF92ECD54089F67A1FB2256E1A66B7271`.

## Final file hashes

```text
tool/src/lsp/server.rs=4F145F6B7824CD4C0602D3668FD4662B7545AD50D34B61AC642FC106B1C40BE2
tool/src/lsp/symbol.rs=98B133EE265ECE3AA6F3B79A0FA6CB72391AE074A41F709A3CD806BB114648FE
tool/tests/lsp_open_document_navigation.rs=8EE80B7C815749A18DD9E8BD29D98491FCCF18C8A5223619F29D608DD14CF7FB
tests/run_lsp0_transport_document_sync_check.py=8CDBC662FDDFF43850E5355E3E4A1BCC4EE49724C606532FF15352CB28FD798E
```

## Handoff

- product commit: `9e3574b5cb99dad171d212d3aa813c0e87a14054`
- product tree: `4e2822891ca96c3c3f6c2c0f0728e448154cadd8`
- product parent: `26438f74aab1ce9dc17a3aa21589c17006512cc4`
- this document is docs-only and is to be committed separately.
- author/committer: `tongosu <tongosu@myarts.kr>`
- prohibited trailer count: `0`
- push: `NO`
- foreign dirty paths, protected untracked session deltas, and the pre-existing cargo-check environment issue remain untouched.
- ready for independent review: `YES` after docs-only handoff commit
