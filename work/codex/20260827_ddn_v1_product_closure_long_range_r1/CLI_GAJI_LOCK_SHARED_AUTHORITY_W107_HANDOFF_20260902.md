# CLI gaji lock shared authority W107 handoff

## Custody

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex local product worktree
AI_CAPABILITY: product single-writer implementation and verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure single writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
CONTROL_OWNER: Owner / Codex관리Work
MANAGER: Codex관리Work
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: tool/src/gaji_lock_workflow.rs, tool/src/lib.rs, tools/teul-cli/src/cli/gaji.rs, tracked WASM binary/manifest freshness family
REVIEWER: no new reviewer or worktree created
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Authority and lineage

- Live internal CURRENT: SSOT v25.49.0 / RD-001~543.
- Public Language SPEC: v0.6.0.
- Baseline: `dec1b47419dcf6353ccb85143170d7dcccb238b2`.
- Product/test fixed: `e3c461a2fa397c074dda9c64a8b60a5562a97603`.
- Fixed tree: `0d4b569817845caee2ad370a1c15c5063265eab7`.
- Direct parent: exact. Merge count: 0.

The current authority adds no conflicting public gaji spelling or membership
decision to this reversible internal authority convergence. Rights/publication
attribution remains an independent release gate and did not block this internal
product implementation. No publication, distribution, or rights-cleared claim
is made.

## Product behavior and authority convergence

The actual retained `gaji lock` workflow formerly owned its recursive package
scan, `gaji.toml` interpretation, file and package hash calculation, lock hash,
registry metadata validation, deterministic JSON serialization, and atomic
lock publication inside `tools/teul-cli`.

W107 moves that coherent authority into host-only
`ddonirang_tool::gaji_lock_workflow`. The retained teul command delegates lock
creation to the shared product module. `gaji vendor` also consumes the shared
file inventory, skip-directory policy, and package hash authority, eliminating
a second implementation of those integrity decisions. Registry verification
and command argument parsing remain retained adapter custody; public command
membership and executable/package naming are unchanged.

Exact fixed paths:

1. `tool/src/gaji_lock_workflow.rs` — shared scan/hash/lock/wire/atomic publish owner.
2. `tool/src/lib.rs` — host-only shared module export.
3. `tools/teul-cli/src/cli/gaji.rs` — shared consumer; 333 net private lines removed.
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` — official source-custody refresh only; no new WASM export.
5. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` — exact source/artifact freshness identity.

No new external dependency, pack, runner, framework, public API spelling,
command membership, SSOT, SPEC, or visible UI change was introduced.

## Verification

- New shared-module unit gate: 1/1 PASS.
- Existing teul gaji focused suite: 47/47 PASS.
- Tool library regression: 612 PASS + the same 2 isolated-worktree
  `docs/ssot`-absence ai-prompt failures; new failure 0.
- Official tracked-WASM freshness: initial expected source inventory RED;
  official rebuild plus manifest refresh; final PASS.
- Shared-consumer mutation: replacing the optioned delegate with
  `E_GAJI_SHARED_LOCK_AUTHORITY_BYPASSED` made the existing registry metadata
  lock test RED. Exact restore SHA-256
  `468df474cebbfbeebb48dcb76a3cdc95c64dc2c773ece3fce067e0700b3ca90a`
  returned the same test GREEN. Mutation residue: 0.
- `git diff --check`: PASS.

Fixed identities:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tool/src/gaji_lock_workflow.rs` | 12,551 | `675052bc768b52c7bf962cf38fa1358d81f96ea7903489e692a66d6f085d1469` |
| `tool/src/lib.rs` | 3,919 | `a2110cd9f6a3ac38cd3e56e92623d1fe5f3d8ee79e3541b02e87de5337997d76` |
| `tools/teul-cli/src/cli/gaji.rs` | 109,111 | `468df474cebbfbeebb48dcb76a3cdc95c64dc2c773ece3fce067e0700b3ca90a` |
| tracked WASM | 5,579,392 | `6e62b09e7c1d7e312453d55d4a5f23e3c09681bb387844c53ff3892d322b068e` |
| tracked manifest | 30,135 | `97fa858e20517af8f497a6f0701d0dfedbe577c22c65356cfd6e1b5f1a45d93c` |

## Gate impact and anti-meta

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: retained gaji lock and vendor integrity now consume one reusable shared product authority
CHANGED_V1_GATE: teul private lock/package integrity authority reduced to adapter custody
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
NEW_EXTERNAL_DEPENDENCY_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 4 gates (shared unit, teul gaji suite, tool regression, official freshness)
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
```

Remaining teul custody includes registry verification, install/update/vendor
orchestration, deferred command dispatch, physical binary/package, and the
membership-frozen public `test/view/repl` surfaces. Whole repository teul
semantic authority 0 and physical retirement are not claimed.

Rights/Legal attribution, public command membership, executable/package
naming, legacy alias duration, VC17 exact landing, PathIR public physical
contract, P5 whole closure, P6 Human Smoke, V1 readiness/release/activation,
publication authorization and Human PASS remain OPEN.

Status: `CLI_GAJI_LOCK_SHARED_AUTHORITY_W107_IMPLEMENTED_PENDING_REVIEW`.
