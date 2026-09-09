# CLI train/eval shared atomic authority W40 handoff

## Identity and authority

- Live authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline and direct parent: `619035cac3c7bc686ed3884727b2a6b7d7bd92fb`.
- Baseline tree: `b7a8da2b5908d4f13f4852df9c31c99d43940812`.
- Product fixed: `ec93a1cb9b9f521f95de6bbb72a50c8eca03d3ca`.
- Fixed tree: `ebda2834cb42281fc770d878de436311c6c5d254`.
- Merge count: 0.
- Review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and P5 review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` remain ancestors. W40 created or dispatched no reviewer/worktree.

The v25.47 successor impact is `ADDITIVE`. This milestone changes no public command membership, executable/package spelling, model schema, SSOT/SPEC, membership, or release state.

## User workflows and exact product diff

The retained `train <config> --out <dir>` and `eval <config> --out <dir>` commands now consume shared non-WASM tool product authorities. Their teul modules are one-line adapters with no private config parsing, deterministic scoring, identity/hash, provenance, report, artifact, weights, or output fallback semantics.

The existing versioned physical contracts are preserved byte-for-byte:

- `seulgi.train_config.v1`, `seulgi.train_report.v1`, `seulgi.model_artifact.v1`
- `seulgi.eval_config.v1`, `seulgi.eval_report.v1`, `seulgi.mlp.v1`
- existing diagnostic codes, seeds, score formulas, hashes, provenance, stdout, defaults, and `v20.6.6` retained training artifact identity

The common artifact-set publisher now accepts text and binary payloads in one preflight/stage/rollback/publish transaction. Train publishes report/artifact/weights as one set; eval publishes report/artifact as one set.

Exact product paths:

- `tool/src/artifact_output.rs`
- `tool/src/train_workflow.rs`
- `tool/src/eval_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/train.rs`
- `tools/teul-cli/src/cli/eval.rs`

## Product RED to GREEN

At baseline, placing a directory at the second artifact target caused both commands to write the first report and then fail with raw OS error 5:

- train: exit 1, `train.report.detjson` remained, partial file count 1
- eval: exit 1, `eval_report.detjson` remained, partial file count 1

At fixed target the same faults fail during common set preflight with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`:

- train: exit 1, report/artifact/weights files 0
- eval: exit 1, report/artifact files 0
- predecessor directory preserved; staging/backup residue 0

The risk mutation replaced train's atomic set publish with sequential single-artifact writes. The same second-target fault again left one report, an actual RED. `tool/src/train_workflow.rs` was restored byte-exact to SHA-256 `4908440C5C85B1E8BEC80ED1F73C93E66BFB0486E3825E9D0C90BAC476A8C3E7`; rebuild and identical fault returned GREEN with file count 0 and mutation residue 0.

## Determinism and compatibility

Baseline and fixed normal outputs are exact:

| Workflow artifact | Bytes | SHA-256 |
|---|---:|---|
| train `artifact.detjson` | 973 | `F6692787213C7D882BD4FD62AFFB4EF02E1DD4C9BF08F20B7B16976DF3E95E37` |
| train `train.report.detjson` | 684 | `73CA0165C3B8452CD2DB61AC7451106851340AE4CD107AAC9593374E1995F488` |
| train `weights.bin` | 8 | `404F5E71E974CE803AD74DFA475A16A11B913D9AA8E622DF5FBECEDD2B4FC062` |
| eval `artifact.detjson` | 1302 | `249753EF0A6BD15166B4672B37579BC3219FDA115CAF8F7D73FB63CA8EFF3CC2` |
| eval `eval_report.detjson` | 895 | `3AECC6A589F0E1987CFCCAF6BE4ECE7DCFA77816F9D601F2339A65BE1876F39D` |

## Verification and bounded environment events

- Existing two-pack golden (`gogae8_w82_seulgi_train_v2`, `gogae8_w87_eval_suite_v1`): PASS.
- Existing `tests/run_train_eval_provenance_check.py`: PASS.
- Tool and teul compilation: PASS.
- Shared artifact-output focused tests: 5/5 PASS.
- Tool library regression: 560/562 PASS. The only failures remain the isolated-worktree missing-`docs/ssot` ai_prompt environment failures; W40 regression 0.
- Native baseline/fixed output byte parity: 5/5 PASS.
- Train/eval partial-publish fault probes: 2/2 PASS at fixed target.
- Sequential-publish mutation: RED -> byte-exact restore -> GREEN; residue 0.
- `git diff --check`: PASS.
- New pack/runner/checker/meta-test: 0/0/0/0.

The proportional wasm32 library check remains blocked by the pre-existing `deterministic_debug.rs` import of non-WASM `artifact_output`; W40's train/eval modules are explicitly non-WASM and did not change that boundary. No tracked WASM refresh, WASM behavior claim, or regression attribution is made.

## Frontdoor and publication boundary

- Native retained CLI: GREEN with exact schema/hash/provenance/output compatibility and atomic set publication.
- WASM: no applicable filesystem training/evaluation ingress transition; pre-existing library compile drift remains OPEN.
- Workbench: no applicable consumer or visible UI transition; JS semantic reconstruction and visual/copy/layout diff 0.
- Tested failure partial result/state/artifact publish: 0/0/0.

## C0 through C8 bounded state

| Gate | Fixed-target state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91-command inventory remains custody; no membership transition. |
| C1 | `ddn.project-run.v1` and executable/package/alias gates remain unchanged. |
| C2 | Train/eval parsing, deterministic computation, identities, provenance, serialization, and atomic set output now have shared tool owners. |
| C3 | Public train/eval/test/view/repl membership remains OPEN. |
| C4 | Private teul train/eval semantic and output fallback authority is 0; other INTERNAL/DEFERRED custody remains nonzero. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0; retained internal golden execution remains historical/product-test custody. |
| C6 | Five normal artifacts are byte-identical; multi-artifact failure is atomic/fail-closed with partial publish 0. |
| C7 | Prior target-bound reviews remain preserved; W35~W40 await one coherent rolling-review dispatch by management. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Review state, next safe slice, and nonclaims

Status is `IMPLEMENTED_UNDER_REVIEW`. Review bundle target is the existing rolling reviewer, management dispatch only. Active/new review task/worktree created by W40: 0/0.

The next safe slice is another complete INTERNAL/DEFERRED workflow with an existing executable pack and no public-membership decision. Public test/view/repl, PathIR public XP-02/M12, VC17 exact landing, and teul physical deletion remain individually frozen gates rather than whole-goal blockers.

This does not claim whole C0~C8 closure, repository-wide teul authority/dependency 0, train/eval public support, model-training product maturity, teul physical retirement, PathIR public closure, VC17 exact landing, P0~P6 closure, V1 readiness/release, activation, legal approval, Owner Human Smoke, or Human PASS.
