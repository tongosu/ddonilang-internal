# [DDN V1제품마감Codex -> Codex관리Work] P5 Windows x64 path-clean artifact — session delta

## Current authority

- Internal CURRENT: v25.35.0 / RD-001~490 / Owner final 2026-08-30.
- Public Language SPEC: v0.6.0.
- Impact: `UNAFFECTED_WITH_FIXED_P5_PRODUCT_ADDITION`; no SSOT/SPEC/support membership transition.

## Product result

- Baseline: `aa2e7f087ca0485d2752e945905b9c718e32f647`.
- Product fixed: `b2fa6db1b422122155d5b90f5f2f4bc6ec69b0aa`.
- Product fixed tree: `54c770af56a09a281388b6ae36c260fab77d0562`.
- Linear product commits: `b6deb6f3 -> 3f316a80 -> a32adac2 -> b2fa6db1`; merge count 0.
- Product diff: one new Windows x64 candidate build entrypoint plus six existing compile-time root consumers.
- User workflow: public-source projection -> offline Windows x64 build -> two path-clean/startup-valid/reproducible EXEs.

## Executable evidence

- Initial physical source-root scan RED: `ddonirang-tool.exe=1`, `teul-cli.exe=2`.
- Initial independent-output determinism RED: both EXE hashes differed without `/Brepro`.
- Final A/B build: PASS/PASS.
- A/B byte equality: 2/2 PASS.
- `ddonirang-tool.exe`: 8,537,600 bytes / `6aa349011bc1cf304777292cdfea9fe612dfc7dc5c2a9c1291c0ec8b6a68c6bd`.
- `teul-cli.exe`: 21,873,152 bytes / `4c6bb5165376003a7e8a29b874f0acfc8ffb1108b613ce0bdbe7dfec72cf519b`.
- Both: forbidden physical-root occurrence 0, PE stack reserve 16,777,216, `--help` exit 0.
- Projection: 898 files / final public tree `sha256:27c7a7829dfb91c0d4f104db6cf8b91b443812bfa33eaf8f99645316cae22626`.
- Validation receipt: 654 bytes / `1c34e3db807ae833fbd49c0b9fbef73dd073d2d9ceeb9289e41e6fa02fc599f8`.
- WASM semantic identity: `sha256:615b6612e8177678790919acc8570c7515494c2ec5b1594bab7bc61f705207ab`.
- Existing projection/remap unit tests: 61/61 PASS.
- Existing focused product regression: 41/41 PASS.

## Anti-meta and custody

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: fixed public-source Windows x64 native candidate build is path-clean and reproducible.
- `NEW_TEST_ARTIFACT_COUNT`: 0.
- `EXISTING_TEST_REUSED_COUNT`: 102 plus A/B executable builds/startups.
- `META_TEST_CREATED`: 0.
- `STOP_RULE_APPLIED`: YES.
- `NEXT_PRODUCT_DECISION_ENABLED`: independent review of the coherent path-clean Windows artifact milestone, followed by exact package/rights/release gate decisions.
- `NEW_REVIEW_TASK_COUNT`: 0.
- `NEW_REVIEW_WORKTREE_COUNT`: 0.
- Review dispatch: not performed; existing rolling reviewer is management-owned.
- Protected process lifecycle commands: 0; TCP 8787 listeners at checkpoint: 0.
- Four predecessor task-owned untracked custody files remain byte-preserved and unstaged.

## Open gates and nonclaims

- Exact package/archive/installer and signed receipt schema: OPEN.
- Rights/license/SBOM/notices/signing/distribution: Owner/legal/release gate OPEN.
- P5 whole closure, RC promotion, V1 membership/readiness, public release,
  activation and Owner Human Smoke/Human PASS are not claimed.
