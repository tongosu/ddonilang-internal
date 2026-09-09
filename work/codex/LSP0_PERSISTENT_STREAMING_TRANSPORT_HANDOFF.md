# LSP-0 Persistent Streaming Transport Handoff

## Authority and fixed target

- Worktree: `I:\home\urihanl\ddn\codex\build\worktrees\ddn-p-v1-project-ux-r2-census-r1-20260828`
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Start: `99862e5147cb29ad34f7db0eb6c7712d2fd8d371` (`001fe2452c5254f772f5183f803f320faf34ca72`), parent `2809a7a1b0489d164bf6a418c8cbf5de59c6dfb9`
- Product fixed: `932487a3d92fc2384f51acd64f869bcfb7742675`
- Product tree: `e5a0c92c5437ac40481ca86ddc85ca85b1a77fe4`
- Product parent: `99862e5147cb29ad34f7db0eb6c7712d2fd8d371`
- Product merge count: `0`
- Product commit identity: `tongosu <tongosu@myarts.kr>` for author and committer
- Product commit changed exactly three allowed files:
  - `tool/src/bin/ddonirang-lsp.rs`
  - `tool/tests/lsp0_transport_document_sync.rs`
  - `tests/run_lsp0_transport_document_sync_check.py`

Foreign dirty files were preserved and were never staged or restored: `lang/src/ddl.rs`, `lang/src/model.rs`, `lang/src/parser.rs`, `lang/src/runtime.rs`, `lang/src/stdlib.rs`, and `lang/tests/ddl_physical_first_vertical.rs`.

## Implemented transport boundary

- stdin is read incrementally with an 8192-byte buffer while the stream remains open.
- `FrameDecoder::push` is called for every read chunk and every complete message is processed in order.
- each response is written and flushed immediately.
- `FrameDecoder::finish` is called only after EOF.
- an `exit` notification returns its status without waiting for EOF.
- stdout contains only JSON-RPC frames; errors go to stderr.
- no diagnostics, completion, hover, semantic tokens, or other LSP semantic surface was added.

## Mutation evidence

The pre-mutation byte-exact hash of `tool/src/bin/ddonirang-lsp.rs` was:

`3315b496e6c78c44bbdebb58dd315f553514ee6de9636da037e2018e887c495f`

The existing checker was used for every RED/GREEN run. Cargo's normal rebuild was blocked before test execution by preserved foreign `lang/**` changes and a shared `core` mismatch. To isolate the transport mutation without touching those files, the mutated bin was directly linked against the already-built target library, then the existing checker was run with only its build step bypassed. This is an environment workaround, not a new runner or test pack.

### M1 — `READ_TO_END_INSTEAD_OF_INCREMENTAL_READ`

Exact temporary diff in `tool/src/bin/ddonirang-lsp.rs`:

```diff
-    let mut input = [0_u8; READ_BUFFER_SIZE];
+    let mut input = Vec::new();
     loop {
         let read = stdin
-            .read(&mut input)
+            .read_to_end(&mut input)
```

- Command: direct compile of the mutated bin, then the existing `run_lsp0_transport_document_sync_check.py` with only `build_binary` bypassed.
- Expected RED: initialize response must arrive before EOF.
- Actual RED: `TimeoutError: timed out waiting for JSON-RPC frame` in `check_initialize_before_eof`.
- Exact restore: restored to SHA-256 `3315b496e6c78c44bbdebb58dd315f553514ee6de9636da037e2018e887c495f`.
- Restore GREEN: I1 through I8 completed and `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.

### M2 — `FINISH_ON_EVERY_INCOMPLETE_CHUNK`

Exact temporary diff in `tool/src/bin/ddonirang-lsp.rs`:

```diff
         let messages = decoder
             .push(&input[..read])
             .map_err(|error| error.to_string())?;
+        decoder.finish().map_err(|error| error.to_string())?;
         for message in messages {
```

- Command: direct compile of the mutated bin, then the existing checker with only `build_binary` bypassed.
- Expected RED: fragmented header/body must remain buffered until complete.
- Actual RED: `AssertionError: stdout closed before a complete frame` in `check_fragmented_header`.
- Exact restore: restored to SHA-256 `3315b496e6c78c44bbdebb58dd315f553514ee6de9636da037e2018e887c495f`.
- Restore GREEN: I1 through I8 completed and `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.

### M3 — `PROCESS_ONLY_FIRST_PUSHED_MESSAGE`

Exact temporary diff in `tool/src/bin/ddonirang-lsp.rs`:

```diff
-        for message in messages {
+        for message in messages.into_iter().take(1) {
```

- Command: direct compile of the mutated bin, then the existing checker with only `build_binary` bypassed.
- Expected RED: multiple complete frames in one write must all be processed.
- Actual RED: `TimeoutError: timed out waiting for JSON-RPC frame` while waiting for the shutdown response in `check_multiple_frames_single_write`.
- Exact restore: restored to SHA-256 `3315b496e6c78c44bbdebb58dd315f553514ee6de9636da037e2018e887c495f`.
- Restore GREEN: I1 through I8 completed and `LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS`.

No mutation residue remains in the product source.

## Verification

- Rust focused test executable: ST01–ST08 plus the existing five tests, `13 passed; 0 failed`.
- Existing transport checker on restored binary: I1–I8 PASS, protocol repeat byte-stable, truncated/malformed input fail closed.
- `python tests/run_lsp_followon_minimum_pack_check.py`: PASS.
- `git diff --check`: PASS.
- `cargo test` and `cargo check` replay after the foreign dirty state changed: blocked in `ddonirang-lang` before LSP test execution by pre-existing `UnitDim::{AXIS_COUNT,exponents,from_exponents}` and `Fixed64::parse_decimal_exact` mismatches, plus a DDL equality derive error. No foreign path was modified to bypass this.

## Review boundary

- Product diff from start target: exactly the three allowed LSP transport/test/checker files.
- New dependency: `0`
- New pack/runner/meta-test: `0/0/0`
- Push: `NO`
- Public source/spec/SSOT changed: `NO`
- `READY_FOR_INDEPENDENT_REVIEW=YES`
- This handoff does not claim product promotion, release readiness, Human PASS, or semantic LSP closure.
