# P5 v25.45 current product-source candidate handoff

## Execution custody

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex local product worktree
AI_CAPABILITY: single-writer product implementation, validation, and handoff
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure single writer
RETURN_LABEL: [DDN V1제품마감Codex -> DDN V1 관리 Chat]
CONTROL_OWNER: Owner / DDN V1 관리 Chat
MANAGER: DDN V1 관리 Chat
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: P5 public projection manifest source_commit only; external candidate build roots
REVIEWER: existing rolling reviewer only; no new task, worktree, branch, or dispatch
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Authority and lineage

- Live internal CURRENT: SSOT v25.45.0 / RD-001~536.
- Index / aggregate / manifest / seal SHA-256:
  `3f998ad22bd1442b07978482877333ae238770ff6d069106d23fde027667cd7d`,
  `e94623f128cf9894d76e0b0d8db8de07d4c86ed0aada6cfafab5a2d6f74fad3e`,
  `4a5656c86dd80c33383075a5dd6a7319bb83d396a205c0baff75e858ee88bb5d`,
  `d8437401411f860e3f9bac5122d6ca76ce659e29185e4f2ebae6894402d8f9b7`.
- Public Language SPEC: v0.6.0, CURRENT SHA-256
  `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- CLI test shared-authority review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
  is already bound in the linear product history with `PASS_TARGET_BOUND` only.
- Current product source fixed: `873d3cb236e9f7ab40307bc55c305861e2d7aeef`,
  tree `bf753c9d47c1d3706b27da2531aa619ea1c85309`.
- Predecessor handoff: `82faac1fce862543cf4e48a11adcbf3a94bb4965`.
- Manifest fixed commit: `3e205ce816e47d29f6488bd86d029750e6afaaf5`,
  tree `53ccc5091ef2722bca4e9dcc107960c830838e9f`, direct parent `82faac1f...`, merge 0.
- Exact fixed diff: one `source_commit` line in
  `PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson`.
- Fixed manifest: 8,695 bytes / SHA-256
  `89176bca8386d2d3381d13df11d3fd9c555ab8f95aeb819f544ae5814b114e2c`.

The v25.45 successor adds no semantic rule that invalidates this bounded source
projection or Windows candidate build. Earlier fixed evidence remains
target-bound and is not promoted to whole P5, V1 readiness, or release.

## Product-facing RED and corrected source custody

The predecessor Windows candidate built from source `27418362...` started
successfully but did not contain the later `project-run` product vertical. The
current manifest therefore pointed at a stale product source and could not
represent the current V1 candidate.

The manifest now binds exact product fixed `873d3cb...`. A fresh public
projection and Windows x64 build from that product source exposes
`project-run`, and an existing real virtual-project fixture executes through
the fixed binary with exit 0 and byte-identical expected output.

The `test` workflow has a reviewed shared product authority but its public
command membership is still OPEN. It remains absent from this public candidate
instead of being inferred from private teul custody. `view` and `repl` remain
OPEN for the same membership/contract reason.

## Projection, WASM, Windows, and user workflow evidence

- Projection root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-v25-45-current-873d-projection-r1`.
- Projected file count: 171.
- Initial projection tree: `sha256:4167e8e9658326bf382ee44195279fa2aa5cbe85f98365a03ed5fa6ea22f5bc6`.
- Candidate-WASM remapped final tree:
  `sha256:4248328ef86b68418f53d9902605f175ef8b55d1f38a13dfafdb0197ee2a06ba`.
- Candidate WASM semantic identity:
  `sha256:802872575876e022acf47c911a1640626c62f1738dddc6879f8f0362e494f913`.
- Remap policy:
  `sha256:d80fdb94b79cbab3ac4fd580c701a0dc5947676706964cf0252111237ed6646a`.
- Validation receipt identity:
  `sha256:abf2a5862d92dac3833b04fc261dec0016cde7f29b0d0ae995861b5f61b533ba`.
- Normal projection validation: PASS, required receipt roles 4/4.
- Windows build root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-v25-45-current-873d-windows-r1`.
- Artifact: `ddonirang.exe`, 7,037,440 bytes, SHA-256
  `623b92c7fa5ebcd84d58cf2859b9a047e9d6972d1986f648f51be79d6c8af8e6`.
- PE stack reserve: 16,777,216 bytes; forbidden source/build/cargo/rustup/user
  path occurrence: 0; startup: PASS.
- Artifact executable count: 1; `teul-cli` path/binary/package match count in
  projection and artifact: 0.
- Reused tests: public projection/validation/remap unit tests 56/56 PASS.
- Existing project-run fixture:
  `pack/ddn_local_project_graph_v1/fixtures/project_run_physics_v1.json`.
- Candidate output: exit 0, stderr 0, 16,488 bytes, SHA-256
  `f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578`.
- Existing expected output: exact same bytes and SHA-256.
- New pack / runner / checker / meta-test: 0 / 0 / 0 / 0.

This milestone changes a release candidate decision: P5 can now evaluate the
current `ddn.project-run.v1` product source rather than a stale source snapshot.
It does not promote command membership or authorize publication.

## Remaining release blocker and fail-closed boundary

Strict `--require-spec-links` validation remains RED. Ten historical/candidate
`publish/spec/**/SPEC_MANIFEST_v*.md` links are absent from the public
projection. This is an exact public-SPEC projection/ownership gate, not a
product-code defect, and was not repaired by copying candidate or historical
SPEC files. `docs/ssot/**` and `publish/spec/**` diff are 0.

C0~C8 impact is narrow:

- C0 registry custody unchanged.
- C1 `ddn.project-run.v1` is reachable in the current Windows candidate.
- C2 shared parser/canon/preprocess authority unchanged.
- C3 official candidate remains bounded; public `test`/`view`/`repl` membership OPEN.
- C4 internal/deferred physical teul custody unchanged.
- C5 bounded required build/test/pack/publish teul execution dependency remains 0.
- C6 actual project-run result/artifact parity is byte-exact for the reused case.
- C7 candidate WASM and Windows x64 build/validation PASS in bounded scope.
- C8 projection excludes teul, but strict SPEC-link gate and independent review remain OPEN.

## Review and nonclaims

`REVIEW_BUNDLE_TARGET` is the current-source public projection, remapped WASM,
Windows x64 artifact, project-run exact output, teul exclusion, and strict
SPEC-link blocker. Management may queue it on the one existing rolling reviewer;
this task created and dispatched no reviewer or worktree.

Statuses are only:

```text
P5_V25_45_CURRENT_PRODUCT_SOURCE_CANDIDATE_IMPLEMENTED_UNDER_REVIEW
P5_STRICT_PUBLIC_SPEC_LINK_GATE_OPEN
```

This is not P5 closure, an exact public-command membership decision, teul
physical retirement/deletion, V1 readiness, release/publication/activation,
legal approval, Owner Human Smoke, or Human PASS.
