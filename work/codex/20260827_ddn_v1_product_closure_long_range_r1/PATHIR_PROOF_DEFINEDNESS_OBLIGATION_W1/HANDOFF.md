# PathIR/Proof definedness containment W1 handoff

## Fixed authority and lineage

- Task: `DDN-PATHIR-PROOF-DEFINEDNESS-OBLIGATION-W1`
- Live internal authority: SSOT v25.42.0 / RD-001~534
- Semantic owners: RD-417, RD-421, RD-423
- Public Language SPEC: v0.6.0; unchanged
- Audit evidence: `docs/reports/audit/AUDIT_DDN_PATHIR_PROOF_X2_OVER_X_PRODUCT_EVIDENCE_R1_20260830.md`
- Audit evidence SHA-256: `6b7ae2f61396549305042544635de5c239a72e26964b810b15078e66dbeff506`
- Baseline: `7ff3c6812f63fd29f7b93143fb0430aab2451fb7`
- Product/test/WASM fixed HEAD: `499c348e55083ab53e76740f858d6f86dcff1ba1`
- Fixed tree: `b72fc9a9c2afcbacd7802b3377a2ea8174725ace`
- Direct parent relation: yes
- Merge count: 0

## Product behavior and exact scope

P0 containment is implemented. Any symbolic transformation that divides by a
nonconstant polynomial now generates a nonzero definedness obligation. Existing
unconditional `canon`, `simplify`, `equivalent`, and `prove_equivalent` entrypoints
fail closed while an obligation is pending. Constant nonzero division remains
supported and `0/0` retains `E_SYMBOLIC_DIV_ZERO`.

The internal product seam now keeps these objects and identities separate:

- `DeclaredAssumptionClosure`
- `TransformationObligationSet`
- proof problem identity
- provider identity
- checker identity
- profile identity
- receipt identity

An explicitly declared closure discharges only an exact matching obligation.
No missing obligation is inserted into the closure, and the closure object is
not merged with the obligation set. A closure change changes both proof problem
and receipt identities. These Rust representations are deliberately not a
stable JSON/public wire contract.

Exact changed paths:

1. `symbolic/src/lib.rs`
2. `proof/src/lib.rs`
3. `tool/src/ddn_runtime.rs`
4. `pack/symbolic_rational_expr_v1/README.md`
5. `pack/symbolic_rational_expr_v1/contract.detjson`
6. `pack/symbolic_rational_expr_v1/golden.jsonl`
7. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
8. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No CLI adapter source, Workbench JS/HTML/CSS, SSOT, public SPEC, or visible UI
source changed. The tracked WASM was refreshed through the official build
entrypoint. Fixed WASM identity is 5,570,357 bytes / SHA-256
`7193928fb1e36488635437392b5b617a838e7a5c5134d3b424a29e8373c976ee`.
The manifest Git blob is `62630595cb9055f1e44200c4228bf7e3f66206dd`
(19,295 bytes), and official freshness is PASS.

## XP-01~XP-06 disposition

| Case | Result | Fixed-head evidence |
|---|---|---|
| XP-01 | PASS | `x^2/x` simplify/equiv/prove all fail closed with pending `nonzero(x)` |
| XP-02 | PARTIAL | internal declared `nonzero(x)` exact discharge returns `x`; sealed public ingress and wire remain OPEN |
| XP-03 | PASS | symbolic cancellation cannot erase the `x=0` counterexample; direct `0/0` remains division-by-zero |
| XP-04 | PASS_INTERNAL | closure A and A+`nonzero(y)` have different closure/problem/receipt identities |
| XP-05 | PARTIAL | unsafe CAS/simplifier output no longer becomes proof PASS; an independently specified executable PathIR kernel checker remains OPEN |
| XP-06 | PARTIAL | provider/checker/profile/problem/receipt identities exist internally; certificate/report/public wire binding remains OPEN |

P0 containment status: `PASS_IMPLEMENTED_UNDER_REVIEW`.
P1 obligation vertical status: `PARTIAL_IMPLEMENTED_UNDER_REVIEW`.

## Frontdoor result

- raw DDN `정리하기`: PASS fail-closed; no partial output/state publish
- symbolic CLI simplify/equiv/prove-eq: PASS fail-closed, exit 1
- proof CLI prove-symbolic-eq: PASS fail-closed, exit 1
- tracked WASM raw run-summary: PASS fail-closed with `E_RUNTIME_EXECUTION`
- Workbench-applicable `wasm_project_run_summary_json`: PASS fail-closed with the same definedness cause
- transformation decision parity: PASS for fail-closed containment
- structured obligation/checker/receipt wire parity: OPEN; only the internal candidate diagnostic carries the pending expression today

The diagnostic token `E_SYMBOLIC_DEFINEDNESS_OBLIGATION_REQUIRED_INTERNAL` is
an internal containment candidate, not a chosen stable public spelling.

## Test and mutation evidence

- Initial product RED: symbolic simplify incorrectly returned `x`; proof verifier returned `valid=true`; raw DDN returned successful `x + 1`.
- `ddonirang-symbolic --lib`: 16/16 PASS
- `ddonirang-proof --lib`: 6/6 PASS
- `ddonirang-tool --lib`: 532/532 PASS
- `symbolic_rational_expr_v1` existing pack: PASS with two fail-closed cases
- existing Symbolic v2 pack checker: PASS
- official tracked-WASM freshness: PASS
- new pack: 0
- new runner/checker framework: 0
- meta-test: 0

Mutation results, each actual RED followed by exact restore and GREEN:

| ID | Risk | RED |
|---|---|---|
| M01 | obligation collection bypass | unconditional simplify succeeds |
| M02 | hidden assumption merge | wrong closure discharges `nonzero(x)` |
| M03 | closure identity omits contents | distinct closures collide |
| M04 | problem identity omits closure | cross-closure problem identities collide |
| M05 | receipt omits problem identity | cross-closure receipts collide |
| M06 | provider/checker authority collapse | identities become equal |
| M07 | simplifier failure promoted to checker PASS | unsafe historical certificate verifies |
| M08 | raw DDN hidden fallback | `정리하기` succeeds after definedness error |

Certified exact-restore working-file SHA-256 identities were:

- symbolic M01~M06: `ed048a90fdc1b99474f7705c7022a4642f728788fe8e2b4654460cb2a469a75e`
- proof M07 certifying rerun: `05a2ffa759e67fb0f8a99a8680924eb0531d05a3a76d33440a0606cf18f43fd2`
- tool M08: `00ea2dc7ed85db2ed735b590577f684d8ab493fdcb363925ecc00489d6246629`

Mutation residue: 0.

The full private `teul-cli` test binary reported 1,040 PASS + 14 unrelated
pre-existing failures in legacy `보임`, right-assignment, and foreach atomicity
tests. None is on the eight fixed paths or the PathIR/proof assertions, so this
handoff does not claim whole-teul regression PASS.

## Unsafe golden and remaining gaps

`pack/symbolic_rational_expr_v1` previously asserted unconditional success for
`(x^2-1)/(x-1) -> x+1`. It is preserved in place but reclassified as
`SUPERSEDED_UNCONDITIONAL_SUCCESS_GOLDEN`; both CLI and raw DDN cases now require
fail-closed containment.

Remaining `PRODUCT_GAP`:

1. stable public diagnostic spelling is OPEN;
2. public/sealed assumption and obligation wire schema is OPEN;
3. certificate/check/report/receipt wire identity binding is OPEN;
4. independently specified executable PathIR checker is OPEN;
5. a checked-assumption public CLI/raw-DDN/WASM/Workbench ingress is OPEN;
6. independent review of this fixed milestone is OPEN.

`CONCRETE_DETAIL_GAP_DETECTED=YES` for items 1~5. No incompatible semantic gap
was invented or closed. `ERQ_20260825_001_READY_TO_CLOSE=NO`.

## Anti-meta and nonclaims

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: unsafe symbolic cancellation can no longer silently succeed
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: 7 command/test groups
- META_TEST_CREATED: 0
- STOP_RULE_APPLIED: yes
- NEXT_PRODUCT_DECISION_ENABLED: define the public checked-obligation/checker/receipt representation or keep P0 fail-closed only
- SSOT_CHANGE: 0
- SPEC_CHANGE: 0

This is not independent PASS, whole PathIR/Proof closure, P0~P6 closure, V1
membership/readiness/release/activation, or Human PASS.
