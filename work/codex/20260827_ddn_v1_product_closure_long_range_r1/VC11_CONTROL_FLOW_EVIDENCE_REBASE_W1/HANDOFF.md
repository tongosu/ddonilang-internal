# DDN-P-V1-VC11-CONTROL-FLOW-EVIDENCE-REBASE-W1 handoff

## Disposition

- Status: `VC11_CONTROL_FLOW_EVIDENCE_REBASE_IMPLEMENTED_UNDER_REVIEW`
- Evidence class: executable product-frontdoor evidence; not a semantic authority
- Independent review: required and not yet decided
- Product source change: 0
- Tracked WASM refresh/change: 0
- SSOT/SPEC/visible UI change: 0

## Fixed identity and lineage

- Audit/lease baseline: `6c1963c066388f0fb798b2c2e3f9bfc2617c8beb`
- Evidence/test fixed HEAD: `1b71537b6af2400a1929984183be155af001f94a`
- Fixed tree: `bcba9aae0c8e8b676aa6df91920ac3e923d9cffb`
- Direct parent: `6c1963c066388f0fb798b2c2e3f9bfc2617c8beb`
- Merge count baseline to fixed: 0
- Fixed diff: exactly 25 leased paths under the VC11 pack and three VC11 runners

Fixed Git-blob identities:

- `pack/v1_core_control_flow_evidence_rebase_w1/manifest.detjson`: 3,241 bytes / SHA-256 `1b55e05d5d56065f32dc273dbb584d59c956f14da55a1118eb74a0bee6006e9f`
- native runner: 13,838 bytes / SHA-256 `f5a54174cf5b9d1512bdda875694910926745cb8fd99fad9bfc1edccfc2947e5`
- WASM parity runner: 7,251 bytes / SHA-256 `65fa6e0d28ac6abe67f638b34e90115ae42f1c58dcd261d1a46900f5f4070d97`
- fault runner: 4,408 bytes / SHA-256 `64021fc52f3c17d9de99aa11e006a4b67763ae17016c6ed3f9e6c77473057c8d`

Tracked official WASM custody at the fixed HEAD:

- binary: 5,553,353 bytes / SHA-256 `29480a59d264cffa280d6c1fb8a5a74da857955a6f028cd8b2adaf71e2366f51`
- JS binding: 89,038 bytes / SHA-256 `c5a80302a3a872fab1e8d14c2385f8b5b6ddde8cfc1096c64ee0231e4ec8df3d`
- freshness manifest: 18,938 bytes / SHA-256 `7ad02442eb9b6542e586b86880b7814560611cf927a51cd657e2c72ddc7b843e`

## Exact executable cases

The packet fixes 10 cases, all using raw Korean source through the explicit
`v1-core-v25` supported-profile product frontdoors.

| Case | Surface | Fixed outcome |
|---|---|---|
| CF01 | condition true/false plus else | success; `TRUE`, `ELSE` |
| CF02 | while zero iterations | success; `0` |
| CF03 | while one iteration | success; `1` |
| CF04 | while multiple iterations | success; `3` |
| CF05 | iterable zero items | success; `0` |
| CF06 | iterable one item and container accumulation | success; `7`, `7` |
| CF07 | iterable multiple items in authored order | success; `3`, `1`, `2`, `6` |
| CF08 | implicit current item through a called routine and nested condition | success; `1`, `MIDDLE`, `3` |
| CF09 | failure inside a selected branch | structured `E_RUNTIME_EXECUTION` only |
| CF10 | failure inside a running loop | structured `E_RUNTIME_EXECUTION` only |

Every case is repeated three times. Native and tracked WASM receive identical
LF-normalized source bytes; CRLF-to-LF is the only checkout transport
normalization. There is no syntax/token/semantic lowering in Python or JS.

## Verification evidence

Product-worktree verification:

- native packet: `cases=10 success=8 failure=2 deterministic_repeats=3 partial_publish=0`
- native supplementary custody: 10 executable cases across 5 commands
  - existing continue/control-flow pack: 4/4
  - existing generic iterable order pack: 3/3
  - exact focused Rust filters: 3/3, each exactly one matched test
- native/WASM exact full structured payload parity: 10/10
- WASM deterministic repetitions: 3 per case
- official tracked WASM freshness: PASS
- `cargo test -p ddonirang-tool --lib`: 523/523 PASS
- `git diff --check`: PASS

Failure atomicity is measured at the official supported-profile boundary.
CF09 and CF10 return only the structured diagnostic and expose none of
`output_log_texts`, `output_rows`, `resources`, `patch`, `state_hash`, or
`public_observation_trace_hash`. The supplementary failed-foreach focused test
also requires unchanged world hash and no committed output. Observed partial
state/result/output/effect publication is 0 for this fixed scope.

Fail-closed and mutation custody:

- `CASE_OMISSION`: RED exit 1 / `VC11_CASE_COUNT_MISMATCH`
- `FIXTURE_HASH_TAMPER`: RED exit 1 / `VC11_FIXTURE_HASH_MISMATCH`
- `RECEIPT_TAMPER`: RED exit 1 / `VC11_RECEIPT_HASH_MISMATCH`
- `PROFILE_IDENTITY_TAMPER`: RED exit 1 / `VC11_PROFILE_IDENTITY_MISMATCH`
- all four mutations occur only in isolated temporary packet copies
- exact task-owned identity before/after, native GREEN, WASM GREEN, residue 0
- final normalized tracked-identity SHA-256: `2da35581b038320edf323ed01dc582cdeab9058d97b67f470fd1adf66cea5826`
- missing native result, missing WASM binary/export, stale manifest, missing
  fixture/receipt, hash drift, zero-match focused test, case omission/order
  drift, outcome drift, receipt drift, nondeterminism, and partial-publish keys
  all fail closed in the committed runners

## Clean-detached reproduction and custody

A temporary local clone, not a Git worktree or product branch, checked out
`1b71537b6af2400a1929984183be155af001f94a` detached and reproduced:

- native packet PASS 10/10
- native/WASM exact parity PASS 10/10
- fault injection PASS 4/4 with final native/WASM GREEN
- detached status clean, staged 0, untracked 0, merge 0
- protected Node PIDs start/end identical:
  `17232,23912,45264,47736,56500,56632,57068,58644,60632`
- TCP 8787 listeners start/end: 0/0
- protected server/port/browser/process start/stop/restart/kill commands: 0
- temporary clone removed after the validated reproduction

The first detached attempt correctly failed on checkout-specific CRLF receipt
identity. The packet was corrected before handoff to make fixture and receipt
hashing checkout-independent while preserving the same LF source at both
official frontdoors. The final fixed object above is the only review target.

## Independent review request

Review only the fixed VC11 evidence-rebase scope. Validate fixed identity,
lease-only diff, exact case membership/order, official product-frontdoor use,
native/WASM full payload parity, failure atomicity, deterministic repetitions,
freshness, zero-match and missing-artifact fail-closed behavior, the four
temporary-copy mutations, clean-detached reproduction, and residue/custody.

The reviewer must not edit product source, tracked WASM, SSOT, SPEC, or visible
UI. A review commit, if any, must be a direct successor of this handoff and
contain only the review report and reviewer session delta.

## Nonclaims and open gates

This handoff does not claim independent PASS, VC11 closure, P1-A/P1 closure,
18/18 V1-Core membership, whole execution/exclusion coverage, public
executable or command membership, public stable spelling, Workbench default
ingress or visible behavior, whole P0/P1/V1 readiness, P2-P6/RC, release,
activation, legal status, Owner Human Smoke PASS, Human PASS, or external-user
success. VC17 Owner decision remains separate and is not included.
