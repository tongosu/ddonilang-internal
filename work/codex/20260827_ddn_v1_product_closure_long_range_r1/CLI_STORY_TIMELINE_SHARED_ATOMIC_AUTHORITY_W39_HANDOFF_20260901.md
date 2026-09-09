# CLI story/timeline shared atomic authority W39 handoff

## Identity and authority

- Live authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline and direct parent: `a7bc9f827ffb35e0eb8c99ae74c5cea723486d9c`.
- Baseline tree: `f3e5550e071ad8e795179b90eb91f00fdb693682`.
- Product fixed: `e6731f161b4e8da04013fdc4c17c280789510a8f`.
- Fixed tree: `65d580540ec73c63fef12b2b5f72f89b932507ae`.
- Merge count: 0.
- P5 review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` and CLI review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` remain ancestors. W39 created or dispatched no reviewer/worktree.

The v25.47 successor impact is `ADDITIVE`: the fixed workflow changes no public command membership, executable/package spelling, SSOT/SPEC, membership, or release state.

## User workflow and exact product diff

The retained `story make --geoul ... --out ...` and `timeline make --geoul ... --story ... --out ...` commands now consume one shared non-WASM tool authority. Their teul files are one-line consumer adapters and retain no private Geoul-header parsing, frame-count, story/timeline serialization, or artifact-output fallback semantics.

The shared owner preserves the existing Geoul v1 header/index frame-count contract and exact story/timeline JSON bytes. It publishes both artifacts through the shared atomic artifact writer. It does not move the full private Geoul writer/state/detbin family, promote these commands publicly, or decide their final physical custody.

Exact product paths:

- `tool/src/lib.rs`
- `tool/src/story_timeline_workflow.rs`
- `tools/teul-cli/src/cli/story.rs`
- `tools/teul-cli/src/cli/timeline.rs`

## Product RED to GREEN

At baseline, both complete workflows had one private teul implementation and no shared tool owner. The fixed state has one shared owner and zero private teul semantic/output fallback owners for these two commands.

Direct fixed probes against a minimal valid Geoul bundle preserved exact prior artifact identities:

- story: 155 bytes, SHA-256 `5F8B5CFB73D7AE79391B784F3F41B1973B23A607AEED64F168F00410906A580B`
- timeline: 144 bytes, SHA-256 `A5D8A6EFAD94608F96B62549409AD8D186CEB8D5015E3590E4F3F45080A58B9F`

A directory-valued story output target returns exit 1 with `E_SHARED_ARTIFACT_OUTPUT_TARGET_NOT_FILE`, preserves the predecessor directory, and publishes no partial artifact.

The risk-relevant mutation changed the Geoul version guard from reject-mismatch to reject-match. A version-2 bundle then returned exit 0 and published the story artifact, an actual semantic RED. The source was restored byte-exact to SHA-256 `871E2DB301141891B9827255BEA932DF53D920D4464769385B34CD777E5954FD`; the same invalid bundle then returned exit 1 with `audit.ddni version 불일치: 2`, output absent. Valid story/timeline and directory-target probes returned GREEN; mutation source/process residue is 0.

## Verification and bounded environment events

- `cargo check --manifest-path tool/Cargo.toml --lib`: PASS.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml`: PASS.
- Shared artifact-output focused tests: 5/5 PASS.
- Tool library regression: 560/562 PASS. The only failures are the unchanged isolated-worktree missing-`docs/ssot` ai_prompt environment failures; W39 regression 0.
- Direct valid story/timeline byte identity: 2/2 PASS.
- Direct invalid-version and directory-target fail-closed probes: 2/2 PASS.
- Version-guard mutation: RED -> byte-exact restore -> GREEN; residue 0.
- `git diff --check`: PASS.
- New pack/runner/checker/meta-test: 0/0/0/0.

Two existing Geoul packet checkers and the existing `run_pack_golden.py geoul_replay_playback_closure_v1` were attempted but could not execute their historical generated product fixtures in this isolated worktree. The packet checkers reported missing W43/W35 `manifest.detjson`; the golden reported missing generated Geoul paths and `E_GEOUL_ENTRY_MISSING`. These are fixture/environment custody events, not product PASS or W39 regression evidence.

## Frontdoor and publication boundary

- Native retained CLI: GREEN with exact output compatibility and atomic/fail-closed publication.
- WASM: not applicable to these filesystem Geoul-to-artifact commands; no tracked WASM change or parity claim.
- Workbench: no applicable command consumer or visible UI transition; semantic reconstruction and visual/copy/layout diff 0.
- Partial result/state/artifact publish on tested failures: 0/0/0.

## C0 through C8 bounded state

| Gate | Fixed-target state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91-command inventory remains custody; no membership transition. |
| C1 | `ddn.project-run.v1` and executable/package/alias gates remain unchanged. |
| C2 | Story/timeline Geoul validation, frame-count projection, serialization, and atomic output now have one shared tool owner. |
| C3 | Public story/timeline/test/view/repl membership remains OPEN. |
| C4 | Private teul story/timeline semantic and output fallback authority is 0; other INTERNAL/DEFERRED custody remains nonzero. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0; historical/internal fixture references remain custody. |
| C6 | Exact artifact bytes are preserved and failure publication is atomic/fail-closed with partial publish 0. |
| C7 | Prior target-bound reviews remain preserved; W35~W39 await one coherent rolling-review dispatch by management. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Review state, next safe slice, and nonclaims

Status is `IMPLEMENTED_UNDER_REVIEW`. Review bundle target is the existing rolling reviewer, management dispatch only. Active/new review task/worktree created by W39: 0/0.

The next safe slice is another approved complete INTERNAL/DEFERRED workflow whose current private authority can move behind the shared tool frontdoor without deciding public membership or physical retirement. It must reuse existing product tests and change a user workflow rather than create evidence-only artifacts.

This does not claim whole C0~C8 closure, repository-wide teul authority/dependency 0, story/timeline public support, full Geoul authority convergence, teul physical retirement, PathIR public closure, VC17 exact landing, P0~P6 closure, V1 readiness/release, activation, legal approval, Owner Human Smoke, or Human PASS.
