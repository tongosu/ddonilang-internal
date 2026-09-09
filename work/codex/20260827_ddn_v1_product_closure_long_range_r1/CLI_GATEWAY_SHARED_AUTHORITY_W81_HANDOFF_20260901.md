# CLI gateway shared authority W81 handoff

## Identity and status

- Live authority: internal SSOT `v25.47.0 / RD-001~543`; public Language SPEC `v0.6.0`.
- Successor impact: `ADDITIVE`; no prior PASS is automatically inherited.
- Baseline: `98ffda9810d08211482428c18659d3755fefc681`.
- Product fixed: `f950d6fa9bed2f3554022c102373dd773629d405`.
- Product tree: `a381259db035f6b0d9d18917802ea11feef182cd`.
- Status: `CLI_GATEWAY_SHARED_AUTHORITY_W81_IMPLEMENTED_UNDER_REVIEW`.

## Product workflow and authority delta

The existing gateway workflows retain their exact physical contract while their
complete implementation moves from the retained teul command tree into
`ddonirang_tool::gateway_workflow`:

- deterministic `gateway load-sim` report generation;
- file-backed `gateway serve` for detjson, JSONL, and SAM inputs;
- loopback TCP and UDP ingestion with deterministic event ordering/deduplication;
- source-provenance, source-hash, report-hash, and atomic report output.

Exact product paths:

- `tool/src/gateway_workflow.rs` (new shared owner, moved implementation);
- `tool/src/lib.rs` (host-only module export);
- `tools/teul-cli/src/cli/gateway.rs` (2-line retained adapter).

Private teul gateway semantic/runtime/value/canon fallback count is now 0. No
command spelling, option spelling, public membership, wire field, diagnostic,
network semantics, pack, runner, SSOT, SPEC, WASM export, or UI behavior changed.

## Executable evidence

- Existing `tests/run_gateway_provenance_check.py`: baseline PASS and fixed PASS.
- Existing `pack/gogae9_w90_meta_universe`: 6/6 PASS.
  - load-sim 1/1;
  - file-backed serve 3/3;
  - real loopback TCP/UDP serve 2/2.
- Source provenance and fixed report identities matched all existing goldens.
- Deterministic event ordering and dedupe remained byte-identical.
- Atomic report writer remains the shared `artifact_output` authority.
- `git diff --check`: PASS.

Risk mutation changed the canonical comparator argument order. The existing pack
went RED in serve cases 2 through 6, proving that network event ordering is
product-observed. The exact source was restored to SHA-256
`523f9a95706a882d10527669b491ae07c1c45bbb975a7ff129d6c862e1c089fa`,
the 6-case pack/provenance runner returned GREEN, and mutation residue is 0.

## Frozen Geoul predecessor decision

The W80 end-to-end predecessor `run --geoul-out` remains slice-locally frozen as
`CONCRETE_DETAIL_GAP_DETECTED`. Shared execution owns `NuriWorld`, while the
versioned replay bundle currently stores legacy teul `State` detbin. Inventing a
new state encoding or silently writing incompatible bytes would break replay
custody. Required decision: reuse/define a versioned shared state snapshot codec,
or explicitly restrict the existing legacy Geoul writer to migration custody.
This gap does not block the W81 gateway workflow or the whole persistent goal.

## Anti-meta, review, and nonclaims

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: gateway load-sim/serve now execute from one shared product owner.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `EXISTING_TEST_REUSED_COUNT`: 2 artifacts (one runner and one 6-case pack).
- `META_TEST_CREATED`: 0.
- `ACTIVE_REVIEW_TASK_COUNT`: 0.
- `NEW_REVIEW_TASK_COUNT`: 0.
- `NEW_REVIEW_WORKTREE_COUNT`: 0.
- Review target: existing rolling reviewer, one coherent W81-plus-next-nearby internal CLI bundle after management dispatch.

This does not claim public gateway membership, network release exposure, whole
C0-C8 closure, repository-wide teul authority/dependency zero, physical teul
retirement, P0-P6 closure, V1 membership/readiness/release, activation, legal
approval, Owner Human Smoke, or Human PASS.
