# LSP-0 Resource-Bounded Frame Decoder Handoff

## Target custody

- Original reviewed target: `932487a3d92fc2384f51acd64f869bcfb7742675`
- Original target tree: `e5a0c92c5437ac40481ca86ddc85ca85b1a77fe4`
- Original target parent: `99862e5147cb29ad34f7db0eb6c7712d2fd8d371`
- Correction base HEAD: `127a9589ed8298942188f817308e45171cab6f8e`
- Correction product commit: `54070b7362dd48f9c977ef835bb0f36fc478641d`
- Correction product tree: `8eb62e1d5610c41946b413c2d794f80e3bfc8493`
- Correction product parent: `127a9589ed8298942188f817308e45171cab6f8e`
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- Author and committer: `tongosu <tongosu@myarts.kr>`

The product commit changed exactly these three allowed paths:

```text
tool/src/lsp/protocol.rs
tool/tests/lsp0_transport_document_sync.rs
tests/run_lsp0_transport_document_sync_check.py
```

The existing foreign dirty paths were not modified, restored, staged, or committed:
`lang/src/model.rs`, `lang/src/parser.rs`, `lang/src/runtime.rs`, and
`lang/src/stdlib.rs`.

## Resource contract

```text
MAX_HEADER_SECTION_BYTES = 16384
MAX_CONTENT_LENGTH_BYTES = 16777216
MAX_PENDING_FRAME_BYTES = 16793600
```

The decoder now validates limits before appending input, uses checked arithmetic
for frame boundaries, clears and poisons itself after a limit rejection, and
returns `DecoderLimitExceeded` on later reuse. Normal fragmented and multiple
frame processing remains incremental and ordered. Response encoding is
unchanged.

The new internal error taxonomy is:

```text
HeaderTooLarge
ContentLengthTooLarge
FrameTooLarge
DecoderLimitExceeded
```

## Verification

Validation ran in the task-owned fixed snapshot:
`I:\home\urihanl\ddn\codex\build\validation\lsp-resource-bound-current`.
The snapshot was based on current HEAD with only the three LSP correction
paths applied, isolating shared checkout Cargo failures from this correction.

- Rust focused integration: `22 passed; 0 failed`
- Existing black-box checker: I1–I8 PASS, RB06/RB08 fail-closed PASS,
  protocol repeat byte-stable
- Binary cargo check: PASS
- `git diff --check`: PASS
- No semantic LSP feature, wire change, dependency, pack, runner, or meta-test
  was added.

## Mutation evidence

Final product source preimage for both mutations:

`d93eebb3775388e78af39a16ccd8d4f9369a3c6c2637a8c3381179ec80ac2d1f`

### CM1 — header cap removed

- Temporary mutation hash:
  `65a078a524d0a61fafc8195e7a3ee6d965c3e663fa06f7361eeda3ddfe99bbb5`
- Removed the no-terminator header cap before append and processing.
- RED: endless-header black-box child failed to exit within the bounded
  timeout; no success response was produced.
- Exact restore hash:
  `d93eebb3775388e78af39a16ccd8d4f9369a3c6c2637a8c3381179ec80ac2d1f`
- Restore GREEN: full existing checker PASS.

### CM2 — Content-Length cap removed

- Temporary mutation hash:
  `ad0534b039be2f45de86bd7c71a55d0c5928718b416d59ca2764740fa0324e48`
- Removed the declared body-size rejection.
- RED: oversized declared body black-box child failed to exit within the
  bounded timeout; no success response was produced.
- Exact restore hash:
  `d93eebb3775388e78af39a16ccd8d4f9369a3c6c2637a8c3381179ec80ac2d1f`
- Restore GREEN: full existing checker PASS.

CM3 was not needed: pending-buffer enforcement is covered by the production
append bound and RB10/RB11/RB12, while header and declared-body limits are
separate rejection guards.

## Boundary and next review

- Limit rejection messages: `0`
- Limit rejection retained bytes: `0`
- Post-limit recovery: `0`
- Shared worktree Cargo failure is pre-existing foreign `lang/**`/shared
  `core` mismatch; no foreign file was changed to bypass it.
- Push: `NO`
- This handoff claims only resource-bound correction and readiness for the
  same reviewer to inspect header/body/pending limits. It does not claim full
  LSP semantic completion, V1 readiness, release, public support, or Human
  PASS.
