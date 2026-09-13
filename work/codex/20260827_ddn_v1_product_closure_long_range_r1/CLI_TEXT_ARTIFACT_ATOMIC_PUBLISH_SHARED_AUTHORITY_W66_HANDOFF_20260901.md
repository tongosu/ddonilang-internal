# CLI text artifact atomic publish shared authority W66 handoff

## Identity

- live internal authority: v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- baseline: `a291b246203805c517a19c23d6dc6f45fda0255e`
- product fixed: `9d57ec8a87c9eb483486cc72e116d1e99d226591`
- product tree: `6c5eb5d2957f8bbe50fe6a3e58e282081b6ae286`
- direct parent: yes
- merge commit: no

## Product value

`ai extract`, `alrim registry`, `geoul record make --out`의 단일 텍스트 artifact 출력을
`ddonirang_tool::artifact_output::write_text_artifact_atomic` 하나로 수렴했다. 세 workflow는
parent directory 생성, 기존 artifact의 atomic replacement, 실패 시 predecessor 보존과 staging
residue 0을 공용 제품 권위에서 소비한다. 제품 출력 내용, command spelling, schema, public
membership은 바꾸지 않았다.

## Exact product diff

- `tools/teul-cli/src/cli/ai.rs`
- `tools/teul-cli/src/cli/alrim.rs`
- `tools/teul-cli/src/cli/geoul.rs`

새 pack, runner, test file, public export, registry, SSOT, SPEC, WASM, UI 변경은 0이다.

## Verification

- shared atomic writer fault/rollback unit tests: 5/5 PASS
- geoul focused unit tests: 4/4 PASS
- isolated-target `cargo check --offline --manifest-path tools/teul-cli/Cargo.toml`: PASS
- actual binary workflows:
  - AI extract repeat SHA-256: `7d9150c41e8193fe86135ceb7cb3ba3d8acbdd17800d695d303b2685364c0674`
  - geoul record repeat SHA-256: `c1547fa082bc34ad8d72b9a9e9e4307f961e4b7c7cbe810ba50a361fb7301f8a`
  - alrim registry repeat SHA-256: `4d8549f72e44c88abd76829b72accddca708d94b2d00f076cc129e56eb7e6dc3`
  - repeat equality: 3/3
  - geoul record check: PASS, steps 2
  - atomic staging residue: 0
- full teul regression: 1043 PASS + existing historical 9 FAIL; new drift 0
- `git diff --check`: PASS

초기 shared Cargo target 재사용 검증은 stale/incompatible dependency materialization으로 E0308을
재현했다. 별도 외부 target에서 동일 source를 clean materialize한 뒤 focused test, check, build,
actual workflow가 모두 통과했으므로 제품 결함 증거로 승격하지 않는다.

## Mutation

- mutation: `ai extract` consumer를 direct `fs::write`로 되돌려 shared-authority bypass 주입
- RED: direct writer count 1, exit 37
- byte-exact restore SHA-256:
  `d2847d2f5b96ae6c4e08b21d59692c951f9c7c08174c4c5c22af8b5d114693f3`
- GREEN: scoped direct writer count 0
- mutation residue: 0

## Gate impact

- teul private artifact-publish authority: 세 workflow에서 3 -> 0
- V1 required build/test/pack/publish teul execution dependency: 기존 bounded 0 유지
- C0 registry custody: 91 유지
- public executable/command membership: 변화 0
- physical `tools/teul-cli` custody: 보존

## Anti-meta

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: 세 CLI text artifact workflow의 atomic replacement/partial-publish 방지
- NEW_TEST_ARTIFACT_COUNT: 0
- EXISTING_TEST_REUSED_COUNT: 4 groups
- META_TEST_CREATED: 0
- STOP_RULE_APPLIED: yes
- NEXT_PRODUCT_DECISION_ENABLED: 남은 teul artifact writer를 공용 atomic authority로 수렴할 범위를 fixed evidence로 선택 가능

## Status and nonclaims

- status: `CLI_TEXT_ARTIFACT_ATOMIC_PUBLISH_SHARED_AUTHORITY_W66_IMPLEMENTED_UNDER_REVIEW`
- independent PASS: not claimed
- whole CLI convergence, whole teul authority 0, public retirement, P0~P6 closure, V1 readiness,
  release, activation, legal, Owner Human Smoke/Human PASS: OPEN

