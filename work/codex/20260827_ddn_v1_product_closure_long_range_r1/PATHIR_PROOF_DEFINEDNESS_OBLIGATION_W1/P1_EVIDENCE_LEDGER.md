# PathIR/Proof XP02·XP05·XP06 successor evidence ledger

## Fixed-head verification

| Gate | Result |
|---|---|
| `cargo test -p ddonirang-symbolic --lib -q` | 17/17 PASS |
| `cargo test -p ddonirang-proof --lib -q` | 12/12 PASS |
| `cargo test -p ddonirang-tool --lib -q` | 532/532 PASS |
| `python tests/run_symbolic_v2_pack_check.py` | PASS |
| `python tests/run_ddn_cli_wasm_freshness_check.py` | PASS |
| official WASM release build repeated twice | byte-identical PASS |
| actual tracked WASM raw DDN `x^2/x` | fail-closed PASS |
| `git diff --check` | PASS |

Tracked WASM:

- bytes: 5,571,041;
- SHA-256:
  `ac750ce56f9ee34200136147ba7dd6b3d9187c5e023b0817c4ab030dade35de2`;
- repeat build identity: exact match;
- source roots:
  `core/src,lang/src,numeric/src,proof/src,symbolic/src,tool/src`;
- source file count: 102;
- source tree SHA-256:
  `362229b4cfb5633cc270263f5ed0832c15708fdfc07a3b23fa14670f1f237c29`.

The actual WASM failure contains
`E_SYMBOLIC_DEFINEDNESS_OBLIGATION_REQUIRED_INTERNAL nonzero(x)`; no result was
returned.

## XP disposition

| Case | Result | Evidence |
|---|---|---|
| XP-01 | PASS_PRESERVED | unconditional cancellation remains fail-closed |
| XP-02 | PARTIAL | explicit checked assumption succeeds through the internal typed request; public ingress is OPEN |
| XP-03 | PASS_PRESERVED | direct undefined cases remain fail-closed |
| XP-04 | PASS_INTERNAL | closure changes alter downstream identity |
| XP-05 | PASS_INTERNAL_IMPLEMENTED_UNDER_REVIEW | provider-independent checker recomputes rewrite/definedness |
| XP-06 | PASS_INTERNAL_CHAIN / PARTIAL_PUBLIC | problem/certificate/execution/check/report/receipt are bound; public projection OPEN |

## Atomicity and identity

- same source, closure, provider, checker and profile produce identical problem,
  certificate, execution, check-result, report and receipt identities;
- missing checked evidence produces no checker/report/receipt success;
- unknown internal request version produces no fallback;
- result publish count: 1 only after checker PASS;
- state publish count: 0;
- outbox release count: 0;
- hidden assumption fallback: 0;
- diagnostic-text semantic reconstruction: 0.

## Anti-meta

- existing tests reused: symbolic 17 + proof predecessor 10 + tool 532 + existing
  Symbolic v2 pack + existing freshness checker;
- new test artifact count: 0;
- new cases inside the existing proof test module: 2;
- meta-test created: 0;
- new pack/runner/checker framework: 0.

The freshness checker extension is release-critical: before the change,
`proof/src/lib.rs` could change while tracked-WASM freshness incorrectly
returned PASS.
