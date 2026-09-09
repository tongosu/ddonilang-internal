# CLI detjson shared hash/atomic authority W46 handoff

## Identity

- status: `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- live authority audited: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0
- baseline/handoff parent: `c2c3b22a01ee6424f1409a21e4f9f0a834a6a402`
- product fixed commit: `9e47eb5004ad69c55bc66373d48b5907a348b86d`
- product fixed tree: `4bae0301aa1478dc2b4bb6fed5d20817805dd34d`
- direct lineage: yes
- merge count: 0

## Product value and scope

The teul CLI detjson adapter no longer owns a private SHA-256 implementation or a
non-atomic `fs::write` artifact path. Its 13 existing consumer modules now reuse:

- `ddonirang_tool::runtime_surface::sha256_hex`
- `ddonirang_tool::artifact_output::write_text_artifact_atomic`

The existing dotbogi user workflow now creates missing output parent directories
and atomically replaces its output, after-state, and report artifacts through the
shared tool authority. Public command membership, executable/package naming,
wire spelling, and deferred-command custody did not change.

## Exact product diff

- `tools/teul-cli/src/cli/detjson.rs`
- `tools/teul-cli/src/main.rs`

Diff: 5 insertions, 14 deletions. New pack 0, new runner 0, new framework 0,
meta-test 0.

## RED, implementation, and mutation

- Product RED: the existing dotbogi CLI test was parameterized to write three
  artifacts below absent nested parent directories. The prior private
  `fs::write` path failed closed with exit 101 / Windows OS error 3.
- Product GREEN: after the shared atomic-writer re-export, the same test passed
  1/1 and all three parent directories/artifacts were produced.
- Risk mutation: the adapter was temporarily changed back to private
  `fs::write`; the same product test reproduced RED exit 101 / OS error 3.
- Exact restore: `tools/teul-cli/src/cli/detjson.rs` restored to SHA-256
  `ff45db8b60283b08b5e3b719343e2649a59edfec7691a7f00924557070557bbb`.
- Restore GREEN: focused dotbogi test 1/1 PASS; mutation residue 0.

## Verification

- dotbogi focused group: 5/5 PASS
- shared tool artifact-output focused group: 5/5 PASS
- teul-cli full binary regression: 1042 PASS / 9 FAIL / 0 ignored
- the 9 failures are pre-existing, out-of-scope frontdoor contract drift in
  legacy `보임`, bidirectional/right assignment parsing, and one atomicity case;
  none touches the two W46 paths. Whole-suite PASS is not claimed.
- private detjson SHA definition count: 0
- private detjson `fs::write` count: 0
- shared hash authority import count: 1
- shared atomic writer authority import count: 1
- existing consumer file count: 13
- `git diff --check`: PASS before fixed commit

## Frontdoor and custody boundary

This is a native filesystem artifact seam. WASM and Workbench do not own or
execute this filesystem writer, so no UI/WASM surface was changed and broad
native/WASM/Workbench parity is not claimed. The shared hash implementation is
the existing tool runtime authority; W46 does not define another semantic hash.

Protected VC06/VC17/P1 task-owned untracked files remained byte-identical and
unstaged. `docs/ssot/**`, public SPEC, tracked WASM, UI, pack, and publish paths
have zero diff.

## Anti-meta checkpoint

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: dotbogi nested artifact publication now
  uses parent creation plus atomic replacement.
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: 3 groups (focused dotbogi, dotbogi group, shared
  artifact-output group), plus the existing full teul-cli binary suite.
- META_TEST_CREATED: 0
- STOP_RULE_APPLIED: yes; only the fail-open/non-atomic product risk was mutated.
- NEXT_PRODUCT_DECISION_ENABLED: the 13 detjson consumers can be assessed as
  shared artifact/hash consumers rather than private semantic owners.

## Nonclaims and open gates

This does not claim public `view`/`test`/`repl` membership, executable naming,
teul-cli physical deletion or public retirement, required-dependency zero for
the whole V1 projection, whole CLI parity, P0~P6 closure, V1 readiness, release,
activation, legal clearance, Owner Human Smoke, or Human PASS. The milestone
awaits inclusion in one coherent rolling independent review.
