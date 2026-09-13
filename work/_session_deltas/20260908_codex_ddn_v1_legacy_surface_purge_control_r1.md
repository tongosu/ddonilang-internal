# V1 legacy-surface purge control R1 — session delta

```ini
AI_PROVIDER = OpenAI
AI_SURFACE = Codex Work
SESSION_NICKNAME = V1레거시통제 Work
PROJECT_ROLE = V1 active tree legacy 제거 실행계획 담당
RETURN_LABEL = [DDN V1 제품 마감 실행 -> 또니랑 개발 관리자 Work]
TASK_TYPE = CONTROL / IMPLEMENTATION PLANNING
DIRECT_PRODUCT_WRITE = NO
```

## Fixed planning boundary

- Live authority read-only: internal SSOT `v25.65.0 / RD-001~586`; public
  Language SPEC `v0.6.0`.
- Product baseline: `78e7d1fbf5f5cce5e14ad80d351c6ba205e5c30b`, tree
  `b8086a973c0ea70ec8dd201ccf6271b29c3e96f3`, parent
  `62635bccfcfe870eb17cd7ff87cbd7049d6ae72f`.
- The clean-break Policy R1 fixed proposal/review is `PASS / NOT_CURRENT`.
  Therefore `POLICY_READY_FOR_EXECUTION=NO` and
  `PRODUCT_PURGE_EXECUTION=HOLD`; planning completed without a product write.
- Chaebi hardcut target `303b411c53db71d3f5aff482198363eb238ecb5f` is reused
  as `CLOSED_TARGET_BOUND`; B00 successor
  `18b5bd08e60b7b46e03c4948b3457da475da8129` remains separate custody.

## Ownership and outcome

- The control matrix records L01--L12, ten FILE_OWNER lanes, the mandatory
  producer-before-parser PR-A through PR-I DAG, exact policy holds, and one
  implementation-ready PR-A candidate.
- `lang/src/parser.rs`, `tool/src/ddn_runtime.rs`, `tool/src/wasm_api.rs`,
  `tool/src/runtime_surface.rs`, and LSP paths were already foreign tracked
  WIP; no existing WIP, untracked custody, or protected material was staged,
  moved, reset, cleaned, or changed.
- The first post-promotion product unit is deliberately LP-02 producer
  correction only. It requires exact source-role proof and a clean lease; it
  cannot rewrite Owner-held examples or activate a parser hardcut.

## Changes and nonclaims

```ini
PRODUCT_MUTATION_THIS_CONTROL_PASS = 0
SSOT_CHANGE = 0
PUBLIC_SPEC_CHANGE = 0
NEW_PACK_RUNNER_META_TEST = 0/0/0
PUSH_PERFORMED = NO
```

The only intended commit content is this delta and
`work/codex/DDN_V1_LEGACY_SURFACE_PURGE_R1/CONTROL_MATRIX_AND_PR_DAG.md`.
It does not close a grammar family, P0--P6, P5, V1 readiness/release, or
Human gate.
