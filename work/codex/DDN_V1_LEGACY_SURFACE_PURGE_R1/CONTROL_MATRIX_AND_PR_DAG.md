# DDN V1 legacy-surface purge: control matrix and PR DAG R1

## Control identity

```ini
TASK = DDN-V1-LEGACY-SURFACE-PURGE-CURRENT-EXAMPLE-REBASE-CONTROL-R1
TASK_TYPE = CONTROL / IMPLEMENTATION PLANNING
DIRECT_PRODUCT_WRITE = NO
LIVE_SSOT = v25.65.0 / RD-001~586
PUBLIC_SPEC = Language SPEC v0.6.0
PRODUCT_BRANCH = codex/ddn-v1-p1a-core-supported-ingress-w1-20260829
BASE_HEAD = 78e7d1fbf5f5cce5e14ad80d351c6ba205e5c30b
BASE_TREE = b8086a973c0ea70ec8dd201ccf6271b29c3e96f3
BASE_PARENT = 62635bccfcfe870eb17cd7ff87cbd7049d6ae72f
```

This is a product-execution program, not a deletion authorization or a claim
that every search hit is current.  Source-like historical evidence, fixed
review targets, sealed inputs, deferred surfaces, and an unproven active
selector stay distinct.  `UNKNOWN` neither means zero nor authorizes rewrite
or deletion.

## Authority and execution hold

The live pointers are `docs/ssot/CURRENT.md`,
`docs/ssot/ssot/CURRENT.md`, `SSOT_ALL_v25.65.0.md`, its manifest and seal;
the public pointer is `publish/spec/CURRENT.md`.  The Policy R1 proposal and
its independent review are fixed inputs, not current authority:

```ini
SSOT_POLICY_INPUT = NO-HISTORY ACTIVE TREE / CLEAN-BREAK POLICY R1
POLICY_FIXED_REVIEW = PASS / NOT_CURRENT
POLICY_READY_FOR_EXECUTION = NO
PRODUCT_PURGE_EXECUTION = HOLD
SAFE_TO_PURGE_PRODUCT_HISTORY = NO
```

The missing gate is latest-live C1 successor assembly and Owner promotion.
After that gate, every planned write still needs the exact-path dependency,
backup/restore, and writer lease checks in its own PR.  No historical asset or
`tools/teul-cli` directory is in this plan's delete set.

Predecessors reused without reimplementation or rereview:

```ini
CHAEBI_HARDCUT_TARGET = 303b411c53db71d3f5aff482198363eb238ecb5f
CHAEBI_HARDCUT_STATUS = CLOSED_TARGET_BOUND
B00_R2_SUCCESSOR = 18b5bd08e60b7b46e03c4948b3457da475da8129
B00_BOUNDARY = preserved separate lineage; this purge is broader than BF05
```

L01--L03 below therefore reference the Chaebi result; they do not schedule a
duplicate hardcut.

## Active ownership boundary at planning time

Foreign tracked WIP is present and was not staged or edited:
`lang/src/model.rs`, `lang/src/parser.rs`, `lang/src/runtime.rs`,
`lang/src/stdlib.rs`, `tool/src/cert_workflow.rs`, `tool/src/completion.rs`,
`tool/src/ddn_runtime.rs`, `tool/src/domain_evidence_manifest.rs`,
`tool/src/gaji_plan_workflow.rs`, `tool/src/geoul_snapshot.rs`,
`tool/src/host_resource.rs`, `tool/src/hover.rs`, `tool/src/local_project.rs`,
`tool/src/lsp/mod.rs`, `tool/src/lsp/server.rs`, `tool/src/project_authoring.rs`,
`tool/src/proof_workflow.rs`, `tool/src/runtime_surface.rs`,
`tool/src/source_analysis.rs`, `tool/src/unit_wire.rs`, `tool/src/warp_workflow.rs`,
`tool/src/wasm_api.rs`, and `tool/src/workbench_host.rs`.

Any lane containing one of those files is `WRITE_LEASE_BLOCKED` until its
writer delivers a clean fixed handoff.  LSP3 remains read-only.

## Family control matrix

Hit fields name observed role and exact candidate roots, not a count of
current acceptance. `H` means `HISTORICAL_OR_DEFERRED`; `U` means `UNKNOWN`;
`TB` means `TRACK_B_TEMPORARY`; `SP` means `STRICT_PARSER_ADMISSION` or its
rejection guard.  Numeric rewrite/delete values deliberately remain
`UNSET_UNTIL_PROMOTION_AND_PATH_LEASE`: this prevents a search census from
becoming an unauthorized bulk rewrite.

| LEGACY_FAMILY | CURRENT_HITS | PRODUCT_HITS | TEST_HITS | PACK_HITS | WALK_HITS | PUBLIC_HITS | OWNER | FIRST_PR | FINAL_PR | REWRITE_COUNT | DELETE_COUNT | NEGATIVE_GUARD_COUNT | DEPENDENCIES | BLOCKERS |
|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---|---|
| L01 legacy `name:kind =` declaration | `SP: lang/src/parser.rs:230,573,1879` | `RUNTIME_CONSUMER: tool/src/ddn_runtime.rs` | `lang/tests/v25_definition_binding_pack.rs` | `pack/ddn_v25_pc01_definition_binding_v1/negative_old_equals.ddn` | U | H: versioned SPEC history | LP-01 | reused Chaebi boundary; no duplicate code | PR-I | UNSET | 0 | 1 | L01--03 fixed target | parser/runtime WIP; policy hold |
| L02 `채비 {...}` | producer: `lang/src/currentline.rs:174`; `lang/src/normalizer.rs:202`; `tool/src/preprocess.rs:341+` | runtime/WASM: `tool/src/ddn_runtime.rs`; `tool/src/wasm_api.rs` | `lang/tests/v25_definition_binding_pack.rs` | `pack/lang_chaebi_scope_v1/**` and legacy fixture candidates | U | H/U | LP-02 then LP-03 | reference only; already hardcut | PR-E/I | UNSET | 0 | 1 | Chaebi target; producer provenance | active WIP; policy hold |
| L03 `채비: {...}` | producer normalization test: `lang/src/normalizer.rs:1288+` | parser reject `lang/src/parser.rs:120,563` | same binding test | `pack/lang_chaebi_scope_v1/**` | U | H/U | LP-02 | reference only; producer census cannot re-enable it | PR-E/I | UNSET | 0 | 1 | Chaebi target | policy hold |
| L04 `돌려줘` | U | U | U | U | U | U | LP-01 | PR-A only after current-reachable proof | PR-I | UNSET | UNSET | 1 | exact source-role evidence | no path ledger; policy hold |
| L05 `반환` | U | U | U | U | U | U | LP-01 | PR-A only after current-reachable proof | PR-I | UNSET | UNSET | 1 | exact source-role evidence | no path ledger; policy hold |
| L06 generic `되돌림` | U | U | U | U | U | U | LP-01 | PR-A only after current-reachable proof | PR-I | UNSET | UNSET | 1 | exact source-role evidence | no path ledger; policy hold |
| L07 repetition compatibility alias | U | U | U | U | U | U | LP-02 | PR-A producer correction if a current producer is proved | PR-I | UNSET | UNSET | 1 | producer call graph | policy hold |
| L08 `T?` | U | U | U | U | U | U | LP-01 | PR-A only after profile/source proof | PR-I | UNSET | UNSET | 1 | type/profile authority | policy hold |
| L09 old Regex | U | U | U | U | U | U | LP-01 | PR-A only after current entrypoint proof | PR-I | UNSET | UNSET | 1 | current profile and typed literal owner | policy hold |
| L10 bare `[a,b]` collection | U | U | U | U | U | U | LP-01 + LP-03 | PR-A only after current profile proof | PR-I | UNSET | UNSET | 1 | collection authority and runtime reachability | policy hold |
| L11 `쓰임{}` / `드러냄{}` / `공개{}` | U | U | U | U | U | U | LP-02 | **FIRST_SAFE_PR candidate**: eliminate one proved current producer without parser acceptance change | PR-I | UNSET | UNSET | 2 | producer output, current example owner | policy promotion; OD overlap check |
| L12 `구성{}` alias | U | U | U | U | U | U | LP-02 | PR-A only if exact producer/canonical output is proven | PR-I | UNSET | UNSET | 1 | canonical/current-line source owner | policy hold |

No L13 was added: this control pass did not establish a new
current-reachable family.  Search-only results are deliberately not elevated.

### Owner-sensitive examples

Any source/example that is actually governed by either item below is marked
`HOLD_OWNER_DECISION`, not rewritten:

```ini
OD-GRAMMAR-R1-01 = Product value construction exact source
OD-GRAMMAR-R1-02 = formal 작품 root exact source
```

The future PR owner must record the exact path and role before choosing any
replacement.  This hold does not block unrelated producer retirement.

## FILE_OWNER lanes

| lane | EXACT_PATHS (candidate, no lease granted) | FILE_OWNER / WRITER | dependencies | PARALLEL_SAFE | WRITE_LEASE_STATUS | DoD / focused test | risk mutation / rollback | active-history boundary |
|---|---|---|---|---|---|---|---|---|
| LP-01 parser/lexer/canon | `lang/src/parser.rs`, `lexer.rs`, `canonicalizer.rs`, `frontdoor.rs`, focused lang tests | language-core writer | PR-A--C evidence; profile policy | no with LP-02/03 | `WRITE_LEASE_BLOCKED` (`parser.rs`) | strict reject only after producers and positive inputs are clean; `cargo test -p ddonirang-lang` focused | restore parser/lexer/canon blob; mutate retired admission and silent canon | immutable history stays byte-preserved |
| LP-02 producers | `lang/src/normalizer.rs`, `currentline.rs`, `tool/src/preprocess.rs`, their existing unit tests | language/tool producer writer | policy promotion; current producer graph | yes with LP-07/08 after paths split | `HOLD_POLICY`; `preprocess.rs` clean at plan point | a real current producer emits only current source; existing producer test | reintroduce retired producer output; exact blob restore | legacy fixtures become Track-B or history, never rewritten blindly |
| LP-03 runtime/WASM | `tool/src/ddn_runtime.rs`, `wasm_api.rs`, `runtime_surface.rs`, existing native/WASM parity tests | shared runtime writer | LP-02; tracked WASM refresh only when source changes | no | `WRITE_LEASE_BLOCKED` | native/WASM reject same retired input and publish no partial result | reinsert runtime/WASM fallback; restore raw blobs | history/review payloads excluded |
| LP-04 Track-B | `tools/teul-cli/**`, named legacy adapters only after call graph proof | teul custody writer | PR-D, exact dependency inventory | yes with LP-07/08 | `HOLD_POLICY` | current reachability zero; deferred custody retained | reconnect fallback; restore exact adapter blob | no directory deletion, no public retirement claim |
| LP-05 tests | existing `lang/tests/v25_definition_binding_pack.rs`, `tests/ddn_current_public_rejection_parity_runner.mjs`, existing focused test sources | test owner | PR-A/B expected outputs | yes after product target frozen | `HOLD_POLICY` | current positives use current source; one negative resurrection guard/family | remove reject assertion; restore test blob | fixed historical tests remain H |
| LP-06 packs | `pack/ddn_v25_pc01_definition_binding_v1/**`, `pack/lang_chaebi_scope_v1/**`, exact selected active pack only | pack owner | active selector proof, LP-05 | yes with docs lanes | `HOLD_POLICY` | disposition `KEEP_CURRENT/REWRITE_CURRENT/DEFERRED/DELETE` documented per path | stale fixture admission; restore path bytes | sealed/current-referenced pack never deleted |
| LP-07 walks/examples | current `docs/steps/**` and selected `docs/guides/**`, excluding `docs/ssot/**` | documentation writer | selector and OD-GRAMMAR check | yes with LP-08 | `HOLD_POLICY` | each current example parses under current profile; holds preserved | legacy positive example; restore | fixed walks/history preserved |
| LP-08 guidance | unversioned `publish/**` except `publish/spec/**` versioned history | public-doc writer | policy promotion, current selector | yes with LP-07 | `HOLD_POLICY` | no current-facing retired positive claim; public SPEC untouched | reintroduce legacy claim; restore | versioned SPEC/history never edited here |
| LP-09 formatter/LSP/tooling | `tool/src/lsp/mod.rs`, `server.rs`, `hover.rs`, formatter/tool callers | LSP/tooling writer | LP-01/02, structured current source | no with LSP3 WIP | `WRITE_LEASE_BLOCKED` | formatter/LSP consumes same current parser/canon path | tool-only alias; restore | LSP3 fixed target remains untouched |
| LP-10 validation/oracle | existing `tests/ddn_current_public_rejection_parity_runner.mjs`, supported-ingress and native/WASM gates | validation owner | every preceding PR | yes only after target fixed | `HOLD_POLICY` | all target gates in final section; no new runner | bypass one gate; restore | planned-only NHAT is not an oracle |

## Producer-before-parser DAG

```text
PR-A -> PR-B -> PR-C -> PR-D -> PR-E -> PR-F -> PR-G -> PR-H -> PR-I
```

| PR | one coherent product objective | exact lease candidates | start / DoD | focused validation | 2--4 risk mutations | rollback | review target |
|---|---|---|---|---|---|---|---|
| PR-A | remove one actually current legacy producer without altering grammar admission | LP-02 paths plus one existing producer test | C1 promoted, clean writer lease, exact output role proved; current producer no longer emits that family | existing normalizer/currentline/preprocess test | emit retired token; select wrong profile; silently reformat; no-op removal | exact raw blob restore | product fixed target only |
| PR-B | converge current-line, preprocess, native/WASM producer paths | LP-02 + LP-03 | PR-A green; no split producer remains | existing native/WASM parity and producer test | WASM-only producer; native-only lowerer; fallback; lost source epoch | exact raw blobs and tracked WASM manifest if refreshed | fixed target |
| PR-C | rebase one current positive fixture/example vertical | exact selected current test/example; no OD hold | producer green and source role known; positive uses current grammar | existing test and supported frontdoor | legacy fixture retained; test-only lowering; result drift | exact fixture/test blob | fixed target |
| PR-D | strict parser hardcut for the same family | LP-01 and a negative guard | producers/current positives green; no current callback depends on admission | focused parser plus current parity | accept retired source; silent canon; hidden migration; diagnostics-as-input | exact parser blob | fixed target |
| PR-E | quarantine Track-B reachability | exact adapter paths after call graph proof | PR-D green; direct/indirect current reachability known | existing official CLI/runtime/WASM gates | reinsert subprocess/PATH fallback; route current selector to Track-B | exact adapter blob | fixed target |
| PR-F | rebase or defer exactly selected active packs | exact selected pack paths only | selector proof; no seal/manifest dependency conflict | pack's existing checker | stale positive legacy input; incorrect delete selection | raw fixture restore | fixed target |
| PR-G | rebase current walks/examples | exact current doc/example paths only | no OD-GRAMMAR hold; current parser target green | existing example/frontdoor check | old positive source; generated output stale | exact bytes restore | docs product handoff target |
| PR-H | remove current guidance claim only | exact unversioned public guidance path | PR-G green; public ownership lease | direct link/text check; no new framework | current claim reintroduced; versioned history edited | raw blob restore | documentation fixed target |
| PR-I | close one family at fixed target | no new product scope; existing gates | PR-A--H relevant paths green | current strict parse, canon/reparse, native/WASM/Workbench parity | one admission, fallback, producer, partial-publish mutation | restore each mutated blob | one coherent independent review |

Parallel work is permitted only for disjoint clean leases: PR-G and PR-H can
run beside PR-F after PR-D; LP-09 must wait for LSP3.  PR-D cannot precede
producer correction.

## First product vertical after policy approval

```ini
FIRST_SAFE_PR = PR-A / LP-02
VERTICAL = eliminate one proved CURRENT_REACHABLE_PRODUCER for L11 (old visibility/use block) from the current-line/preprocess producer path, without changing parser acceptance
EXACT_INITIAL_INSPECTION_PATHS = lang/src/currentline.rs; lang/src/normalizer.rs; tool/src/preprocess.rs; their existing focused tests
PRE_WRITE_GATE = identify one emitted current source role and verify it is not OD-GRAMMAR-R1-01 or OD-GRAMMAR-R1-02
USER_VALUE = a current authoring/formatting path stops re-emitting retired syntax before strict admission is narrowed
NO_OWNER_SEMANTIC_DECISION = required for the vertical once C1 is promoted; physical replacement uses the then-current typed owner only
CURRENT_STATUS = IMPLEMENTATION_HOLD_PENDING_POLICY_PROMOTION_AND_EXACT_LEASE
```

This is an implementation-ready vertical, not a census or a docs PR.  If the
pre-write inspection finds no L11 producer, it must not substitute another
family: record `NO_PRODUCER_FOR_L11` and advance to the next proven producer
under the same PR-A contract.

## Target validation design (not current proof)

```ini
CURRENT_STRICT_PARSE = 38/38 PASS
CURRENT_PARSE_CANON_EMIT_REPARSE = 38/38 PASS
NONCURRENT_STRICT_ACCEPTANCE = 0
CURRENT_EXAMPLE_LEGACY = 0
CURRENT_POSITIVE_TEST_LEGACY = 0
CURRENT_V1_PACK_LEGACY = 0
CURRENT_WALK_LEGACY = 0
CURRENT_PUBLIC_GUIDANCE_LEGACY = 0
IMPLICIT_MIGRATION_COMPATIBILITY = 0
```

The `38` target is a future current-target gate, not an assertion that the
v25.62 bounded audit automatically proves v25.65 behavior.  Each family
closes only after the authoritative parser, canonical emission/reparse, and
applicable native/WASM/Workbench typed projection agree; failure publishes no
partial success/state/receipt.

## Nonclaims

This plan changes no product, test, pack, SSOT, public SPEC, membership,
readiness, release, activation, legal, Human, P0--P6, P5, or teul physical
retirement status.  It authorizes neither history purge nor an independent
review task.
