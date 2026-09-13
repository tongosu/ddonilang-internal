# C2 V1 REQUIRED Physical Surface Profile candidate R1

> Status: `PROPOSAL_NOT_ORACLE` / evidence-derived physical mapping candidate.
> It is not a membership, support, readiness, release, or public-command promotion.

## Fixed inputs and boundary

- Product target: `864f7344aa82e9763846f168e2887d2e45cc7769`, tree `e19932c1a8a580d39c7531ce87ee0c91a592600c`, parent `d96d638ed55f29e1b51813318b93e0d635ca9bdc`, merge count from the P0-A fixed successor to target: `0`.
- Internal authority (read-only shared root): SSOT `v25.56.0 / RD-001~560`; public Language SPEC: `v0.6.0`.
- Semantic C2 membership is `40 = REQUIRED 28 + OPTIONAL 2 + DEFERRED 10`. This candidate maps the 28 REQUIRED rows only.
- Physical release membership remains `0 / AUDIT-PENDING`. That is a distinct axis: no row below is a release claim.
- Source of the required-row identities: `docs/ssot/ssot/SSOT_DECISIONS_v25.25.0.md`, lines 1047-1074, preserved by the live-current succession.
- No product, test, pack, SSOT, SPEC, public export, or membership files were changed for this candidate.

## Evidence keys

| Key | Current fixed-product evidence | What it proves / does not prove |
|---|---|---|
| E1 | `Cargo.toml` workspace members and `tool/Cargo.toml` | `ddonirang-tool` is a workspace member and the three native targets `ddonilang`, `또니랑`, `ddonirang` share `tool/src/bin/ddonirang.rs`; `tools/teul-cli` is not a workspace member or `ddonirang-tool` dependency. It does not establish release membership. |
| E2 | `tool/src/bin/ddonirang.rs` and P0-A fixed ancestor `d96d638e` | `ddonilang` and `또니랑` are the two official native names sharing one source entry. `ddonirang` is a compatibility alias using the same implementation. There is no argv[0]-dependent semantic branch; the command rejects private `teul-cli` help residue. |
| E3 | `solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js`, `ui/runtime/wasm_canon_runtime.js`, `ui/wasm/ddonirang_tool.manifest.detjson` | Workbench consumes tracked `ddonirang_tool` WASM through its shared bridge. It does not prove every C2 row is reachable there. |
| E4 | `tests/run_v1_core_supported_ingress_w1.py` and P0-A handoff | Existing native/WASM supported-ingress evidence exercises a subset of V1 Core, not a complete 28-row physical release gate. |
| E5 | `scripts/build_windows_x64_public_candidate.ps1:70` | The public-candidate projection has a deny check for `teul-cli` artifact paths; it is not evidence that every required row has a publish artifact. |
| E6 | `.github/workflows/seamgrim-ci.yml:82-118` | A job explicitly labelled historical builds and runs `tools/teul-cli` golden material. It is a discovered historical CI edge, not proof of an active REQUIRED-row gate. |
| E7 | `solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py:36,466` and `tools/README.md:58` | The private pilot server can resolve `teul-cli`, including an optional `TEUL_CLI_WORKER=1` route. It is internal/deferred custody unless a future approved physical profile maps it to a REQUIRED row. |
| E8 | `tool/src/patch_workflow.rs:5-21,355-359`; `scripts/seamgrim_batch_quality_gate_v1.py:55-66` | Internal workflow/quality helpers have explicit teul path or invocation parameters. No current required-row registry mapping connects them to a REQUIRED release gate. |

### Reading rule

`NONE_OBSERVED` means no direct invocation/dependency was found in the cited current common frontdoor. It is not a dependency-zero conclusion when the row's complete physical gate is `UNKNOWN`. `UNKNOWN` is retained in the dependency calculation and is never counted as zero.

## Required-28 physical-surface candidate table

Common native entrypoint is `E1/E2`; common Workbench bridge is `E3`; build producer is `E1`; the only current publish projection is `E5`. These observations have the following deliberately narrow meaning:

```ini
COMMON_NATIVE_FRONTDOOR_OBSERVED=YES
COMMON_WORKBENCH_BRIDGE_OBSERVED=YES
PER_ROW_NATIVE_REACHABILITY=NOT_PROVEN
PER_ROW_WORKBENCH_REACHABILITY=NOT_PROVEN
```

Thus every `E2` or `E3` cell below means `common path only / row reachability not proven`. `NOT_PROVEN` is deliberate where no current physical release profile binds the semantic row to an executable gate.

| ROW_ID | CAPABILITY | C2_STATUS | OFFICIAL_NATIVE_ENTRYPOINT | WORKBENCH_ENTRYPOINT | BUILD_PRODUCER | CI_JOB | REQUIRED_TEST_GATE | REQUIRED_PACKS | RUNTIME_OWNER | PUBLISH_ARTIFACT | TEUL_DIRECT_EDGE | TEUL_INDIRECT_EDGE | EVIDENCE_PATH_AND_IDENTITY | CLASSIFICATION | UNRESOLVED_REASON |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VC01 | Korean raw source | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | E4 subset | NOT_PROVEN | lang + tool shared runtime | E5 candidate only | NONE_OBSERVED | UNKNOWN | E1-E5 @ `864f7344` | UNKNOWN | Complete required physical gate absent |
| VC02 | Definition `:=` | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | E4 subset | NOT_PROVEN | lang + tool shared runtime | E5 candidate only | NONE_OBSERVED | UNKNOWN | E1-E5 @ `864f7344` | UNKNOWN | Same |
| VC03 | Binding/Rebinding `<-` | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | E4 subset | NOT_PROVEN | lang + tool shared runtime | E5 candidate only | NONE_OBSERVED | UNKNOWN | E1-E5 @ `864f7344` | UNKNOWN | Same |
| VC04 | basic value/type/identity | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | lang + tool runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Row detail remains product-open |
| VC05 | exact/basic deterministic numeric | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | numeric + tool runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Row physical gate absent |
| VC06 | text/bytes/NFC | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | existing VC06 evidence, not release gate | NOT_PROVEN | lang normalizer + tool | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Scope/evidence rebase still required |
| VC07 | Product | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | lang + tool runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | No physical profile binding |
| VC08 | Sum/optional/typed result | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | lang + tool runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | No physical profile binding |
| VC09 | named callable | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | named-callable evidence, not release gate | NOT_PROVEN | tool shared runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E4 @ `864f7344` | UNKNOWN | Exact CI/pack/publish mapping absent |
| VC10 | ResultPlace | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | tool shared runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | No physical profile binding |
| VC11 | condition/iteration | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | control-flow evidence, not release gate | NOT_PROVEN | tool shared runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E4 @ `864f7344` | UNKNOWN | Exact CI/pack/publish mapping absent |
| VC12 | basic collection | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | collection workflow evidence, not release gate | NOT_PROVEN | lang runtime + adapters | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Product convergence is separate |
| VC13 | typed Selection | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | lang + tool runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | No physical profile binding |
| VC14 | Basic Tensor R1 | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | numeric + tool runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | No physical profile binding |
| VC15 | Korean morphology | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | lang + tool runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | No physical profile binding |
| VC16 | closed multisurface/canon | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | NOT_PROVEN | NOT_PROVEN | lang canon + tool | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | No physical profile binding |
| VC17 | basic stdlib/PURE_MINIMAL family | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | provider evidence is separate | NOT_PROVEN | lang stdlib + tool adapters | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Exact provider-to-physical mapping not established here |
| VC18 | basic diagnostics | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | E4 subset | NOT_PROVEN | tool structured diagnostics | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E4 @ `864f7344` | UNKNOWN | Complete diagnostic projection absent |
| VE01 | deterministic execution | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | P4 scoped evidence | NOT_PROVEN | shared runtime/receipt | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | P4 physical profile is not fixed |
| VE02 | state/result identity | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | P4 scoped evidence | NOT_PROVEN | shared runtime/receipt | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Same |
| VE03 | internal receipt/replay | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | P4 scoped evidence | NOT_PROVEN | shared runtime/receipt | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Host-resource contract target not fixed |
| VE04 | fail-closed/no fallback/partial publish 0 | REQUIRED | E2 | E3 | E1 | NOT_PROVEN | scoped regressions | NOT_PROVEN | shared runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Cross-frontdoor gate absent |
| P0 | official Native CLI | REQUIRED | E2 | N/A | E1 | NOT_PROVEN | E4/P0-A | NOT_PROVEN | shared lang/tool | E5 candidate only | NONE_OBSERVED | UNKNOWN | E1-E5 @ `864f7344` | UNKNOWN | Command membership and release profile remain open |
| P3 | Workbench | REQUIRED | E2 where applicable | E3 | E1 | NOT_PROVEN | bridge/WASM scoped evidence | NOT_PROVEN | typed WASM bridge | NOT_PROVEN | NONE_OBSERVED | E7 route is deferred | E1,E3,E7 @ `864f7344` | INTERNAL_DEFERRED_CUSTODY | Private pilot teul route is not an approved V1 gate |
| P1 | single-file product form | REQUIRED | E2 | E3 where applicable | E1 | NOT_PROVEN | E4 subset | NOT_PROVEN | shared runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E4 @ `864f7344` | UNKNOWN | Complete single-file physical profile absent |
| P2 | Local Project product form | REQUIRED | E2 | E3 where applicable | E1 | NOT_PROVEN | local-project scoped evidence | NOT_PROVEN | local project + shared runtime | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E3 @ `864f7344` | UNKNOWN | Exact schema/wire/reopen gate not bound |
| P5 | Windows x64 first distribution target | REQUIRED | E2 | N/A | E1 + E5 | NOT_PROVEN | Windows candidate scoped checks | NOT_PROVEN | public candidate script | E5 candidate only | NONE_OBSERVED | UNKNOWN | E1,E5 @ `864f7344` | UNKNOWN | Candidate is not a physical release membership |
| P6 | Owner Human Smoke | REQUIRED | E2 | E3 where applicable | E1 | N/A | fixed-artifact human gate | N/A | fixed artifact consumer | NOT_PROVEN | NONE_OBSERVED | UNKNOWN | E1-E5 @ `864f7344` | UNKNOWN | Human gate cannot be inferred from source |

## Discovered teul edge ledger

| Edge group | Caller and current role | Classification | Required-row relation |
|---|---|---|---|
| G1 | `seamgrim-ci.yml` builds `tools/teul-cli` and runs W49/W111/W109/W107 goldens; job and step labels say historical | HISTORICAL_DOCUMENTATION | No REQUIRED-row mapping in current physical registry |
| G2 | `ddn_exec_server.py` optional/private `TEUL_CLI_WORKER` route | INTERNAL_DEFERRED_CUSTODY | No approved V1 REQUIRED relation |
| G3 | `patch_workflow.rs` and `seamgrim_batch_quality_gate_v1.py` explicit teul helper path/invocation | INTERNAL_DEFERRED_CUSTODY | No REQUIRED-row mapping in current physical registry |
| G4 | lesson/golden metadata naming teul-cli | HISTORICAL_DOCUMENTATION | Metadata is not an execution edge |

```ini
NON_EDGE_COMMON_PATH_OBSERVATION=G5
G5=common workspace/tool/native/WASM/P0 public-candidate paths: no direct teul invocation observed; this is not an edge and does not erase unresolved indirect mapping
```

### Aggregate and dependency disposition

```ini
REQUIRED_ROW_TOTAL=28
REQUIRED_ROW_ACCOUNTED=28
UNMAPPED_ROW_COUNT=28
PHYSICAL_RELEASE_MEMBERSHIP=0/AUDIT-PENDING

DISCOVERED_TEUL_EDGE_GROUPS=4
REQUIRED_ACTIVE_EDGE_GROUP_COUNT=0
COMPATIBILITY_TEST_ONLY_EDGE_GROUP_COUNT=0
INTERNAL_DEFERRED_EDGE_GROUP_COUNT=2
HISTORICAL_EDGE_GROUP_COUNT=2
UNKNOWN_DISCOVERED_EDGE_GROUP_COUNT=0
EDGE_CLASSIFICATION_SUM=0+0+2+2+0=4

REQUIRED_ROW_TOTAL=28
PHYSICAL_MAPPING_ROWS=0
UNMAPPED_ROW_COUNT=28
ROW_CLASSIFICATION_UNKNOWN_COUNT=27
ROW_CLASSIFICATION_INTERNAL_DEFERRED_CUSTODY_COUNT=1
UNKNOWN_REQUIRED_ROWS=27
UNKNOWN_DISCOVERED_EDGE_GROUPS=0

REQUIRED_DEPENDENCY_DIMENSION_COUNT=7
REQUIRED_DEPENDENCY_NOT_PROVEN_COUNT=7

REQUIRED_BUILD_TEUL_DEPENDENCY=NOT_PROVEN (workspace-level direct dependency 0)
REQUIRED_CI_TEUL_DEPENDENCY=NOT_PROVEN (historical CI edge exists; no required-job map)
REQUIRED_TEST_TEUL_DEPENDENCY=NOT_PROVEN
REQUIRED_PACK_TEUL_DEPENDENCY=NOT_PROVEN
REQUIRED_RUNTIME_TEUL_DEPENDENCY=NOT_PROVEN (official common frontdoor direct edge 0)
REQUIRED_PUBLISH_TEUL_DEPENDENCY=NOT_PROVEN (candidate deny check is not a full profile)
REQUIRED_WORKBENCH_TEUL_DEPENDENCY=NOT_PROVEN (private pilot route is deferred)
UNIQUE_TEUL_SEMANTIC_AUTHORITY=NOT_PROVEN_ZERO
FALLBACK_REACHABILITY=NOT_PROVEN_ZERO
```

The zero counts above are only counts of **classified discovered edge groups**. They do not convert the seven `NOT_PROVEN` required-dependency values to zero. `UNIQUE_TEUL_SEMANTIC_AUTHORITY` and `FALLBACK_REACHABILITY` are separate investigation axes, not dependency dimensions.

## Result and next decision

This candidate establishes a complete 28/28 semantic-row inventory and records the current concrete common product paths. It also shows why the older release registry's zero physical membership is not a contradiction: it has not yet bound rows to the common paths.

`NEXT_COHERENT_PRODUCT_VERTICAL=NONE_PENDING_CANDIDATE_REVIEW_AND_OWNER_PROMOTION`.

Before an implementation to remove a teul dependency, the profile needs independent review and Owner promotion. The next implementation must then choose a single workflow whose approved profile names (1) an official entrypoint, (2) a required CI/test/pack/publish gate, and (3) an actual teul edge. Until then, a removal would be based on inferred membership.

```ini
OWNER_INPUT_REQUIRED=NO_FOR_CANDIDATE; YES_FOR_PROMOTION
PRODUCT_MUTATION=0
SSOT_CHANGE=0
PUBLIC_SPEC_CHANGE=0
NEW_PACK_RUNNER_META_TEST=0/0/0
P0_D5_D6_STATUS=PHYSICAL_PROFILE_CANDIDATE_PREPARED_NOT_CLOSED
P0_FULL_CLOSURE=NO
V1_READINESS=UNCLAIMABLE
```
