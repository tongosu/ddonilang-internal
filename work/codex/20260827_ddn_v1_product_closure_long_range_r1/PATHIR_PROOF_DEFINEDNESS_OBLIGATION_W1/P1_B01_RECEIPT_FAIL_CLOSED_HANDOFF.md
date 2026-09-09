# PathIR/Proof B-01 receipt fail-closed correction

## Fixed identity

- predecessor independent-review verdict: `FAIL`
- predecessor review commit: `5eff9bda328fb9b3a1c6318970808a25e65258b6`
- reviewed product: `477f888ef95747d14e2965851690658cd5edf181`
- correction fixed commit: `c44279d4c4a3cd8b6289de76b125c29e46257a50`
- correction tree: `220087d516f6f1bd25db0dc1a299579ed5346c1c`
- direct parent: `5eff9bda328fb9b3a1c6318970808a25e65258b6`
- merge count: `0`

The fixed commit changes exactly:

1. `proof/src/lib.rs`
2. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The tracked WASM bytes remain byte-identical because the changed receipt helper
is not part of the currently exported WASM execution path. The manifest changes
to bind the changed `proof/src` source identity.

## Product correction

`seal_definedness_receipt` now rejects invalid publish evidence before receipt
identity calculation:

- `check_completed_before_publish` must be true;
- `result_publish_count` must be exactly 1;
- `state_publish_count` must be 0;
- `outbox_release_count` must be 0;
- `pre_state_hash` and `post_state_hash` must be equal for the current pure
  proof profile.

The existing profile was not widened. Provider, checker, check-execution,
check-result, report and result identities are still validated before a receipt
can be returned.

## RED, mutation and exact restore

Before the product guard was added, permanent tests produced actual RED for:

| axis | observed RED |
|---|---|
| result publish count 0 | invalid receipt returned / exit 101 |
| state publish count 1 | invalid receipt returned / exit 101 |
| outbox release count 1 | invalid receipt returned / exit 101 |
| changed post-state | invalid receipt returned / exit 101 |
| reviewer compound state+outbox+changed-state | invalid receipt returned / exit 101 |

The existing incomplete-checker axis was already fail-closed.

After implementation, two actual source mutations were performed:

1. remove the result-count guard: focused test RED / exit 101;
2. remove state/outbox/state-hash guards together: reviewer compound test RED /
   exit 101.

Both were restored byte-exactly to `proof/src/lib.rs` 51,688 bytes / SHA-256
`0b3e77a6590dad66987ce86cfc172f1627713118d4f6e3d58f4d911c19530351`,
then the full proof library returned GREEN 18/18. Mutation residue is 0.

## Fixed-head validation

| validation | result |
|---|---|
| `ddonirang-symbolic --lib` | 17/17 PASS |
| `ddonirang-proof --lib` | 18/18 PASS |
| `ddonirang-tool --lib` | 532/532 PASS |
| existing Symbolic v2 pack checker | PASS |
| official tracked-WASM freshness | PASS |
| official release WASM build repeat 1/2 | byte-identical PASS |
| actual tracked WASM raw cancellation | fail-closed PASS |

Tracked WASM remains 5,571,041 bytes / SHA-256
`ac750ce56f9ee34200136147ba7dd6b3d9187c5e023b0817c4ab030dade35de2`.
The refreshed manifest working content is 20,880 bytes; its fixed Git blob is
`20e70fd2b3bba13475dbbe953cfa1281c2722d29` (20,268 bytes, LF materialized).
The raw DDN WASM check returned `E_RUNTIME_EXECUTION` containing
`E_SYMBOLIC_DEFINEDNESS_OBLIGATION_REQUIRED_INTERNAL`, with partial result/state
publish 0.

## Status and nonclaims

- `P0_CONTAINMENT`: `PRESERVED`
- `B01_RECEIPT_FAIL_CLOSED`: `IMPLEMENTED_UNDER_TARGETED_REREVIEW`
- `XP_05`: `PASS_INTERNAL_IMPLEMENTED_UNDER_REVIEW`
- `XP_06`: `PARTIAL_PENDING_TARGETED_REREVIEW_AND_PUBLIC_CONTRACT`
- `XP_02_PUBLIC`: `CONTRACT_DECISION_REQUIRED`
- `ERQ_20260825_001`: `OPEN`

This correction does not approve a public registry, CLI option, raw-DDN
assumption syntax, WASM field, Workbench mapping, P1 PASS, ERQ closure, V1
membership/readiness, release, activation or Human PASS.
