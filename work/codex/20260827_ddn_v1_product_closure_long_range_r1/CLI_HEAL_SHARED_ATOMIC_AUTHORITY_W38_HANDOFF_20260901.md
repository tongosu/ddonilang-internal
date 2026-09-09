# CLI heal shared atomic authority W38 handoff

## Identity and authority

- Live authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline and direct parent: `2828e178332e36b0dadfc61894f0196a9bee5632`.
- Baseline tree: `27e9a1d172bab3cacb819452046d6caf1e57408b`.
- Product fixed: `2094630f91304906243429f8b8ef88d62a9cbb0c`.
- Fixed tree: `fcf8933c210cdf9f54d8d708e9e4daf2108758cf`.
- Merge count: 0.
- P5 review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` and CLI review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` remain ancestors. No review was duplicated or dispatched.

## User workflow and exact product diff

The existing `heal run --pack ... --out ...` workflow now consumes `ddonirang_tool::heal_workflow::run_pack`. The retained `tools/teul-cli/src/cli/heal.rs` is a one-line consumer adapter and contains no parser, validation, state-hash, report, path, or output fallback semantics.

The shared owner preserves the existing W97 input and report schemas, diagnostic codes, source provenance, final-state hash, report hash, stdout keys, and default output location. It publishes `heal_report.detjson` through the shared atomic artifact writer. Public command membership, executable/package naming, and legacy alias policy were not changed.

Exact product paths:

- `tool/src/artifact_output.rs`
- `tool/src/heal_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/heal.rs`

## Product RED to GREEN

Authority RED at baseline: W97 heal semantics had one private teul owner and no shared tool owner. Fixed state: shared tool owner 1 and private teul semantic/fallback owner 0 for this workflow.

The first fixed directory-target probe exposed a real shared single-artifact gap: the helper returned raw OS error 5 rather than the shared target diagnostic. The shared helper was corrected to preflight every single artifact target. The final probe exits 1 with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, preserves the directory-valued predecessor, creates zero files, and leaves residue 0.

The shared-authority disconnect mutation changed the teul adapter to a nonexistent shared symbol. Product compilation returned actual RED `E0432`/`E0425`. The adapter was restored to SHA-256 `e6de1f332ad0dffcb3bf490783c619c12e702e4997beb923b5e36a65d7afe6c1`, compilation and W97 returned GREEN, and mutation residue is 0.

## Determinism and compatibility

The existing W97 runner passed before and after the change with the same three cases and exact identities:

- heal report hash: `blake3:f5a39a98faff0017ba5624ed3334e902f53b22413e3e3d99cd49343436d39b21`
- sample final-state hash: `sha256:a1a7dadc52acaa8620e0bf7e4c36e170f9f442c306ee1799a6f622a31942a61d`

The existing `E_HEAL_NO_CHECKPOINT`, `E_HEAL_NONREPLAYABLE`, and `E_HEAL_LOOP` negative cases remain fail-closed. Source/report field loss is 0, partial state/result/artifact publish is 0, and no JS or Workbench semantic reconstruction was introduced.

## Verification

- Existing `tests/run_w97_self_heal_pack_check.py`: baseline PASS and fixed/restore PASS, 3/3 cases.
- `cargo check --manifest-path tool/Cargo.toml --lib`: PASS.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`: PASS.
- Shared artifact-output focused tests: 5/5 PASS.
- Tool library regression: 560/562 PASS. The two failures are the unchanged isolated-worktree missing-`docs/ssot` ai_prompt environment failures; W38 regression 0.
- Direct directory-target product probe: expected exit 1, shared diagnostic present, predecessor preserved, partial file count 0.
- Shared-authority disconnect mutation: RED exit 101, exact restore, GREEN, residue 0.
- `git diff --check`: PASS.
- New pack/runner/checker/meta-test: 0/0/0/0.

## C0 through C8 bounded state

| Gate | Fixed-target state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody; no membership transition. |
| C1 | `ddn.project-run.v1` and executable/package/alias gates remain unchanged. |
| C2 | W97 heal validation, deterministic hashing, report serialization, default path, and publication now have one shared tool owner. |
| C3 | Public heal/test/view/repl membership remains OPEN. |
| C4 | Private teul heal semantic and artifact fallback authority is 0; other INTERNAL/DEFERRED custody remains nonzero. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | W97 output is deterministic and single-artifact publication is atomic/fail-closed with partial publish 0. |
| C7 | Prior target-bound reviews remain preserved; W35~W38 await one coherent rolling-review dispatch by management. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Review state, next safe slice, and nonclaims

Status is `IMPLEMENTED_UNDER_REVIEW`. Review bundle target is the existing rolling reviewer, management dispatch only. Active/new review task or worktree created by W38: 0/0.

The next safe slice is another approved INTERNAL/DEFERRED complete workflow with an existing executable contract and no public-membership decision. It should continue removing private teul authority rather than creating an evidence-only micro-slice.

This does not claim whole C0~C8 closure, repository-wide teul authority/dependency 0, heal public support, Workbench/Human PASS, teul physical retirement, PathIR public closure, VC17 landing, P0~P6 closure, V1 readiness/release, activation, legal approval, or Human PASS.
