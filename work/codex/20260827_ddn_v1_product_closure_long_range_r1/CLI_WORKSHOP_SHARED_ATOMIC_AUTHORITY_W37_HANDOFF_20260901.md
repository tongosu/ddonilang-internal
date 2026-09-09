# CLI workshop shared atomic authority W37 handoff

## Identity and authority

- Live authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: `4819d422c16d64851add2fd2b078c346a3e19726`.
- Baseline tree: `855e2d3942a03a463f96395cda89750475aaf0fa`.
- Product fixed: `af4a922dad8d4f34aae06cffc231823c4a4dcde5`.
- Fixed tree: `3a9bf3003d381565a9c175ca63b9cfa452677f1f`.
- Direct parent: yes. Merge count: 0.
- P5 review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` and CLI review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` are already ancestors and were not rebound or duplicated.

## User workflow and product change

The existing `workshop gen`, `workshop apply`, and `workshop open` workflows now consume `ddonirang_tool::workshop_workflow`. The retained `tools/teul-cli/src/cli/workshop.rs` is a consumer adapter only.

`workshop gen` publishes `manifest.detjson` and `index.html` as one atomic artifact set. A failure on either target preserves the complete predecessor set. `workshop apply` uses the shared single-artifact atomic publisher. `workshop open` keeps the existing missing-index fail-closed diagnostic.

Existing command spelling, `workshop.v0` manifest schema, HTML bytes, visible copy, layout, patch bytes, and stdout keys are unchanged. No public command membership, executable/package naming, or alias decision was made.

Exact product paths:

- `tool/src/workshop_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/workshop.rs`

## Product RED to GREEN

Baseline reproduction placed exact bytes `PREDECESSOR` in `manifest.detjson` and a directory at the second target `index.html`. The baseline command exited 1 but replaced the manifest first with a 94-byte generated document: actual partial publish RED.

The fixed command exits 1 with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, preserves the 11-byte predecessor manifest exactly, publishes no new HTML file, and leaves artifact-set residue 0. The shared artifact-set fault test additionally injects failure before the second publication and proves complete rollback followed by exact GREEN, residue 0.

## Determinism and compatibility

The same Geoul path generated twice at the fixed target produced byte-identical files:

- manifest SHA-256: `e45399839adaaa3068058824864e94cbbe8c3f20d761dbdc3e193fcafec62325`
- index SHA-256: `cffac76da61a595a9dec7f9172f899c74d56a178b7e947288dcb7e2c9ce6be98`

Those two hashes exactly match a positive execution from the baseline binary. Therefore visual copy/layout and product serialization changed by 0 bytes.

`workshop apply` and `workshop open` were exercised as one product sequence. The applied artifact SHA-256 equals the input patch SHA-256 `b337d3a24e4256db8c4322f3a4874fb1abe169e31e753510f05914b78b8fa475`, all three commands exit 0, and residue is 0. Opening an empty workshop remains fail-closed with `E_WORKSHOP_MISSING`, exit 1.

## Verification

- `cargo build --manifest-path tools/teul-cli/Cargo.toml --offline`: PASS in the dedicated W37 target directory.
- Shared artifact-output focused tests: 5/5 PASS.
- Tool library regression: 560/562 PASS. The two failures are the unchanged isolated-worktree missing-`docs/ssot` ai_prompt environment failures; W37 regression 0.
- Existing W54 golden reaches its historical first `run --geoul-out` prerequisite and stops at the pre-existing `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` boundary before workshop generation. The exact workshop gen/apply/open frontdoors were therefore invoked directly and are GREEN; the golden was not rewritten into authority.
- Teul test-profile compilation remains environment-blocked by duplicate path-crate/serde materialization, while the normal offline product build is GREEN. No product workaround was introduced for that environment event.
- `git diff --check` and standalone Rust formatting checks: PASS.
- New pack/runner/checker/meta-test: 0/0/0/0.

## C0 through C8 bounded state

| Gate | Fixed-target state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody; no membership transition. |
| C1 | `ddn.project-run.v1` and executable/package/alias gates remain unchanged. |
| C2 | Workshop generation, patch application, HTML/manifest serialization, and artifact publication now have one shared tool owner. |
| C3 | Public workshop/test/view/repl membership remains OPEN. |
| C4 | Private teul workshop semantic and artifact fallback authority is 0; other INTERNAL/DEFERRED custody remains nonzero. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Workshop two-file publication is deterministic and failure has partial publish 0; HTML bytes are unchanged. |
| C7 | Prior target-bound reviews remain preserved; W35~W37 await one coherent rolling-review dispatch by management. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Next safe work and nonclaims

The next safe candidate is another approved INTERNAL/DEFERRED complete workflow with an existing executable contract whose parser/runtime/value/artifact seam can move to `tool` without deciding public membership. `view`, `story`, and `timeline` retain their slice-local UI/Geoul/unsupported-option gates and do not block the whole V1 goal.

Status is `IMPLEMENTED_UNDER_REVIEW`. This does not claim whole C0~C8 closure, repository-wide teul authority/dependency 0, workshop public support, browser/Human visual PASS, teul physical retirement, PathIR public closure, VC17 landing, P0~P6 closure, V1 readiness/release, activation, legal approval, or Human PASS.
