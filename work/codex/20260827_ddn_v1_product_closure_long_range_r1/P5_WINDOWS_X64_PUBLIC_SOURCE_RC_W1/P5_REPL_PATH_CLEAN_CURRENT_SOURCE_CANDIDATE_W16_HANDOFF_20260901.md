# P5 current-source path-clean candidate W16 handoff

STATUS: `P5_CURRENT_SOURCE_PATH_CLEAN_CANDIDATE_IMPLEMENTED_UNDER_REVIEW`

## Authority and lineage

- Live internal authority rechecked read-only: v25.47.0 / RD-001~543.
- Public Language SPEC: v0.6.0.
- v25.47 impact on this bounded CLI/P5 slice:
  `UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR`.
- Product source fixed: `edd4a158d1ff95bd1f68bf972709bacf40f334cc`.
- Product source tree: `2396b2e85dd5675eaafda4e73465a02d85f8c070`.
- W15 handoff parent: `a6ffc29b5eacf9e82e4ffcdda247418e059c1d45`.
- W16 correction fixed: `9e99ebaea41ede347eb432723acee3aabf804d86`.
- W16 correction tree: `889a082b69e2798ebee4edb9d8a2c5dbbc58a287`.
- Direct parent relation: yes; merge count: 0.
- P5 review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`
  and CLI test-workflow review
  `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` are both already bound
  ancestors. Reviewer-handle absence is not a blocker.

## Product regression and correction

W15 added the shared REPL session authority but refreshed tracked WASM with the
default build path. The existing public-projection test detected 115 embedded
Cargo/rustup absolute paths. This was a release-candidate product regression,
not a report-only discrepancy.

The immutable W16 successor rebuilds from exact product source `edd4a158...`
with the existing candidate remap policy and changes exactly three tracked
paths:

1. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
2. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
3. `work/codex/20260827_ddn_v1_product_closure_long_range_r1/P5_WINDOWS_X64_PUBLIC_SOURCE_RC_W1/PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson`

Corrected tracked WASM:

- bytes: 5,573,340
- SHA-256: `8e393c77c916b39ef97f2e90dee4f91034044c100b8b5557c681456b9bef0590`
- freshness manifest bytes: 21,549
- freshness manifest SHA-256:
  `782c2937defb5682eabe7c79fe3bb1ced46f822d49d3dc07eab5c7b4938d1215`
- embedded internal absolute paths: 0
- private include paths: 0
- official store paths: 0
- unknown paths: 0
- virtual remap roots: cargo registry 95, rust toolchain 21, source 1

## Public projection and receipts

- Projection:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-edd4-projection-r1`
- Receipt root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-edd4-projection-receipts-r1`
- Initial file count/tree: 174 /
  `sha256:b0c2408a3826e26d4ac79017ada12304b2a1f030f236d3990bd5ccd50cb0e563`
- Candidate-WASM final tree:
  `sha256:15f43703f853caaf533e1a11beb2d1ddacd24a62cd6ee6372e26ce5c3d080c33`
- Candidate artifact identity:
  `sha256:d4024741f3c593e314d60da8cda5cdaf080672d90d7f88f03c255cdca746b2df`
- Projection manifest identity:
  `sha256:3eaa16a776afc06d565c45cd2a79ac531583be00383f6bd052a9048d70b29aac`
- Remap policy identity:
  `sha256:d80fdb94b79cbab3ac4fd580c701a0dc5947676706964cf0252111237ed6646a`
- Required roles: `PRODUCT_SOURCE`, `PUBLIC_CONFORMANCE_RUNNER`,
  `TRACKED_WASM_FAMILY`, `WASM_CANDIDATE_TOOL` = 4/4 PASS.
- Validation receipt identity:
  `sha256:9729081c8d5dd258efc2c8355b070de50b40c4d10f7e958cc95a50650ae1a446`
- Projection teul path count: 0.

Strict `--require-spec-links` remains fail-closed for ten absent historical or
candidate SPEC manifests. No missing SPEC file was copied or invented. This is
a public-document projection/ownership gate, not a whole-goal impasse.

## Windows x64 and user workflow evidence

- Windows build root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-edd4-windows-r1`
- Artifact: `ddonirang.exe`
- Bytes: 7,043,584
- SHA-256: `8129df4e1fc0419b658bd74278751a286d5127b1a37db630f014f3d9f609ff71`
- PE stack reserve: 16,777,216 bytes.
- Forbidden source/build/cargo/rustup/user path occurrences: 0.
- Artifact executable count: 1; teul-named artifact count: 0.
- `--help`: exit 0 and official V1 candidate command surface reachable.
- Reused fixture:
  `pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`.
- `project-run` output: exit 0, 16,488 bytes,
  SHA-256 `f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578`.
- Existing expected output: byte-exact equal.
- Positional start plus `--virtual`: exit 2 /
  `E_CLI_OPTION_CONFLICT`, with no successful artifact publication.

## Verification and anti-meta accounting

- Existing projection/remap unit tests: 56/56 PASS.
- Existing tracked-WASM freshness: PASS.
- Existing state-machine raw WASM check: PASS.
- Existing post-WASM shared-change check from isolated output: PASS.
- Existing `project-run` product fixture: 1 reused workflow PASS.
- New pack: 0.
- New runner/checker/framework/meta-test: 0/0/0/0.
- Mutation/tamper added: 0; the concrete 115-path regression supplied the RED,
  and the existing zero-path inspection supplied GREEN.
- Product worktree tracked changes after fixed commit: 0.
- Protected four untracked session-custody files were not modified or staged.

USER_WORKFLOW_CHANGED_OR_UNBLOCKED: the current shared-REPL product source can
now be built as a path-clean Windows candidate while preserving exact
`ddn.project-run.v1` output and conflict behavior.

NEXT_PRODUCT_DECISION_ENABLED: the one rolling reviewer can evaluate the
coherent W13~W16 current-source CLI/P5 candidate rather than a path-leaking W15
artifact.

## C0~C8 and remaining gates

| Gate | Actual state after W16 |
|---|---|
| C0 | Historical 91-command registry remains custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` remains fixed and reachable; executable/package/alias naming OPEN. |
| C2 | Shared lang/tool canon, preprocess, runtime and value authorities preserved. |
| C3 | Approved candidate workflows including internal shared `test` and `repl` authorities exist; public `test/view/repl` membership remains OPEN. |
| C4 | REPL private semantic authority is 0; internal/deferred physical teul custody remains. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Reused project-run output is byte-exact; tracked WASM and path-clean inspection PASS. |
| C7 | Current-source public projection and Windows x64 candidate PASS in bounded scope. |
| C8 | Candidate projection/binary excludes teul; physical deletion and final public retirement remain Owner-gated. |

PathIR/Proof P0 containment remains preserved. Public XP-02/M12 physical
contract, full PathIR P1, ERQ closure, VC17 exact landing, public command
membership, strict SPEC-history projection, final release, activation and
Owner Human Smoke remain separate OPEN gates.

REVIEW_BUNDLE_TARGET: W13 current-source projection + W14 GOER guard + W15
shared REPL authority + W16 path-clean correction/current Windows candidate.
No new reviewer, task, branch or worktree was created or dispatched.

NONCLAIMS: this handoff is not P5 closure, whole CLI retirement, teul physical
deletion, V1 membership/readiness, release/publication/activation, legal
approval, Owner Human Smoke, Human PASS, or external-user success.
