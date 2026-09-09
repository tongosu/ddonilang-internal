# DDN-LSP27 — SelectionRange·FoldingRange End-to-End Handoff

## Authority and custody

```makefile
LIVE_AUTHORITY = existing v25.69.0/current typed-parser and LSP owners; SSOT/SPEC unchanged
BASE_PRODUCT = f41fe8bc14ba81212be286d91dee0e65c4321df0
BASE_HANDOFF = 8658d4c3f9db4c6f48b98c7b7c645a3fd33efb8f
PRODUCT_COMMIT = c40f595355ac1988e92e071679c79eea2f94543
PRODUCT_TREE = 5fcf879e3d583cf85d18f51e41eaea85e1f9c7f2
PRODUCT_PARENT = 8658d4c3f9db4c6f48b98c7b7c645a3fd33efb8f
MERGE_COUNT = 0
PRODUCT_PATHS = tool/src/lsp/server.rs, tool/src/lsp/selection_range.rs, tool/tests/lsp_open_document_navigation.rs
TOOL_SRC_LIB_RS_CHANGED = 0
FILESYSTEM_CRAWL = 0
REMOTE_DEPENDENCY = 0
SOURCE_UPLOAD = 0
PUSH_PERFORMED = NO
```

LSP26 predecessor is preserved and counted as the first unit in this autonomous closure:

```makefile
LSP26_PRODUCT = f41fe8bc14ba81212be286d91dee0e65c4321df0
LSP26_TREE = 6d1978202b874f5139ba9acb68d0bd89ccd393ba
LSP26_PARENT = 56a818adca5d7d958973cf7817f2e177a4d7c264
LSP26_HANDOFF = 8658d4c3f9db4c6f48b98c7b7c645a3fd33efb8f
LSP26_STATUS = PRODUCT_FIXED_PENDING_REVIEW
```

## LSP27 implementation

The implementation reuses the existing `DocumentStore`, current immutable `DocumentSnapshot`, `parse_v25` AST, lexer token spans, and UTF-16 position owner. No new parser, semantic owner, filesystem index, or public language rule was added.

### Selection range

- initialize advertises `selectionRangeProvider`.
- token, statement, body, parameter, and definition candidates are built from the existing typed AST and lexer spans.
- parent chains preserve containment and source order.
- string/template/formula/assertion/state-machine tokens are rejected as selection roots; comments remain outside lexer candidates.
- Korean and non-BMP UTF-16 positions use the existing byte-range conversion.
- multi-position requests are bounded at 100 positions and each chain is bounded at 100 levels.
- current snapshot, didChange, didClose, stale version `-32801`, stale identity `-32802`, and cancellation `-32800` are fail-closed.

### Folding range

- initialize advertises `foldingRangeProvider`.
- definition, callable body, and nested typed compound bodies are collected from the existing AST.
- RD457/directive and DDL LanguageSection behavior remains at the existing typed-parser boundary; no LSP-specific interpretation was introduced.
- string/comment braces are not lexical folding candidates; malformed or rejected source yields an empty result.
- UTF-16 ranges, current snapshot, didChange, didClose, stale version `-32801`, stale identity `-32802`, and cancellation `-32800` are preserved.
- serialized folding results are bounded at 1,000 ranges.

## Verification

```makefile
FOCUSED_TEST = cargo test -p ddonirang-tool --test lsp_open_document_navigation = 10/10 PASS
LSP_REGRESSIONS = lsp_completion, lsp_definition, lsp_references, lsp_rename, lsp_document_symbol, lsp_diagnostics, lsp_semantic_tokens, lsp_signature_help, lsp_hover = PASS
BLACKBOX_BEFORE_EOF = LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS
BLACKBOX_NAVIGATION = ST20_OPEN_DOCUMENT_NAVIGATION, ST21_FOLDING_RANGE, ST22_SELECTION_RANGE = PASS
BLACKBOX_OTHER = initialize, fragmented header/UTF-8, persistent lifecycle, diagnostics, hover, definition, documentSymbol, workspace symbol, formatting, references, signature help, inlay hint, rename, highlight, semantic tokens, type definition = PASS
CARGO_CHECK = cargo check -p ddonirang-tool --bin ddonirang-lsp --offline = PASS
DIFF_CHECK = git diff --check = PASS
PROCESS_RESIDUE = 0
```

The one full-package validation after the product target was fixed was `cargo test -p ddonirang-tool`: 635 passed and 2 failed. The only failures were the pre-existing environment-bound `ai_prompt::tests::ai_prompt_output_matches_golden` and `ai_prompt::tests::ai_prompt_output_invariants_hold`; both fail before product behavior because this worktree has no `docs/ssot` directory. This is recorded as `NONBLOCKING_PREEXISTING_ENVIRONMENT_FAILURE`, not as an LSP27 product defect. No AI-prompt, SSOT, or unrelated product path was changed.

The focused LSP27 test covers capability advertisement, AST-only folding with string/comment brace false positives, Korean/UTF-16 selection, deterministic repeat through the existing LSP17 coverage, current snapshot and didClose/stale behavior through LSP16/LSP17, 1,000-result folding bound, 100-position selection bound, and cancellation atomicity.

## Mutation evidence

Each mutation was applied alone, run against the existing focused test, restored immediately, and followed by the restored GREEN test. No mutation was staged or committed.

### M1 — selection parent chain omission

Target: `tool/src/lsp/server.rs`, `selection_range_value`.

Exact temporary diff:

```diff
-        "parent": selection.parent.map(|parent| selection_range_value(Some(*parent))),
+        "parent": Value::Null,
```

RED: `lsp17_selection_ranges_are_ordered_ast_parent_chains_and_current` failed at `assert!(result[0]["parent"].is_object())`.

Exact restore:

```makefile
RESTORE_SHA256 = 267d3156bb3c27b76c2e5b871cac2ed2dbebd87617c14dc83008d0424603be6e
RESTORE_BLOB = bf59b5979463e4245211eca078a2c21e8cf54260
```

GREEN: the same LSP17 test passed after restore.

### M2 — string/comment folding false positive

Target: `tool/src/lsp/folding_range.rs`, immediately after `let mut candidates = Vec::new()`.

Exact temporary diff:

```diff
     let mut candidates = Vec::new();
+    if source.contains("{ fake }") {
+        candidates.push(Candidate {
+            range: ByteRange {
+                start: 0,
+                end: source.len(),
+            },
+            kind: FoldingKind::Compound,
+        });
+    }
```

RED: `lsp27_selection_and_folding_ranges_are_bounded_ast_and_cancellable` observed 3 folding ranges where the assertion required 2; the injected whole-document range represented a brace inside the string/comment fixture.

Exact restore:

```makefile
RESTORE_SHA256 = 02312ddd bce156df 8b8472bf 76115a1d 45d4f12a 6241adf0 898b902f 64435c06
RESTORE_BLOB = f9742cbf2676e72733bfbcb172b1866eeacef584
```

The SHA-256 value above is the same byte sequence without spaces:
`02312dddbce156df8b8472bf76115a1d45d4f12a6241adf0898b902f64435c06`.

GREEN: the same LSP27 test passed after restore.

### M3 — folding stale-version guard removal

Target: `tool/src/lsp/server.rs`, `folding_ranges` requested-version guard.

Exact temporary diff:

```diff
-            if requested_version != snapshot.version {
+            if false && requested_version != snapshot.version {
```

RED: `lsp16_folding_ranges_are_ast_bound_utf16_deterministic_and_current` received a successful folding array for stale version `1` after the document had advanced to version `2`; the expected `-32801` error was absent.

Exact restore:

```makefile
RESTORE_SHA256 = 267d3156bb3c27b76c2e5b871cac2ed2dbebd87617c14dc83008d0424603be6e
RESTORE_BLOB = bf59b5979463e4245211eca078a2c21e8cf54260
```

GREEN: the same LSP16 test passed after restore.

## Handoff

```makefile
HANDOFF_FILE = work/_session_deltas/20260909_codex_ddn_lsp27_selection_and_folding_range_end_to_end_r1.md
HANDOFF_COMMIT = pending
HANDOFF_PARENT = c40f595355ac1988e92e071679c79eea2f94543
AUTHOR = tongosu <tongosu@myarts.kr>
COMMITTER = tongosu <tongosu@myarts.kr>
PROHIBITED_TRAILER_COUNT = 0
FOREIGN_DIRTY_TOUCHED = 0
PROTECTED_UNTRACKED_CHANGED = 0
STAGED = 0 after handoff commit
```

LSP27 is `PRODUCT_FIXED_PENDING_REVIEW`. LSP26 and LSP27 are the two new autonomous product units fixed from the LSP26 handoff base and are ready for one independent review bound to these exact targets. No public push, VSIX rebuild, packaging change, or product promotion is performed here.

```makefile
READY_FOR_INDEPENDENT_REVIEW = LSP26 product target and LSP27 product target
NEXT_AUTONOMOUS_UNIT = LSP28 candidate only; no implementation started
```
