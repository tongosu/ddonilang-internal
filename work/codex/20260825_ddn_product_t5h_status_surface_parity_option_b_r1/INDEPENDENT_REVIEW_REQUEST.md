# [셈그림Codex -> 독립검증ClaudeCode] T5H status·surface·OPTION_B fixed-HEAD 독립 검토 요청

```text
TASK_ID: DDN_PRODUCT_T5H_STATUS_SURFACE_PARITY_OPTION_B_INDEPENDENT_REVIEW_R1
PRODUCT_FIXED_HEAD: c4f4c6411bf04b6fcb0e494611d282f6df67f046
IMPLEMENTATION_COMMIT: 411d01435fb80556aa4f0e9aa70fe7a7f83cf3b1
T5G_PASS_BINDING_COMMIT: 962cd410794956fd3b9e3cf054fc2068579866c5
MODE: ISOLATED_FIXED_HEAD_READ_ONLY
VERDICT_ENUM: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

## 필수 독립 판정

1. 단일 canonical owner를 유지하고 제3 View abstraction을 만들지 않았는가.
2. unknown status가 14/14 exact `invalid`로 fail-closed하고 family-local candidate diagnostic을 반환하는가.
3. 허용된 5개 non-success status와 available-path 기존 bytes/identity가 보존되는가.
4. 실제 current-product surface 26개가 executable evidence로 모두 닫히는가.
5. Playground 12개가 current-product parity가 아니라 Owner-approved legacy compatibility로 명시되는가.
6. Workbench-family Run 4개가 synthetic alias로 성공 주장되지 않고 실제 non-consumer 근거와 일치하는가.
7. legacy redirect가 보존되고 별도 parser/runtime, raw-state semantic inference, hidden fallback, canonical 의미 변형이 없는가.
8. status 2개, surface 3개, OPTION_B 3개 mutation이 각각 RED를 만들고 exact restore GREEN, residue `0`인가.
9. T5B~T5G 회귀, 14-family browser probes, 5 browser groups, supplemental curriculum browser, strict checks가 직접 재현되는가.
10. clean-detached, merge `0`, SSOT/SPEC/tracked-WASM diff `0`, network install `0` 경계가 맞는가.

## 필수 재현

```powershell
$env:DDN_T5F_SOURCE_WASM_DIR = 'I:\home\urihanl\ddn\codex\build\wasm\ddonirang_tool'
$env:DDN_LOCAL_PLAYWRIGHT_NODE_MODULES = 'I:\home\urihanl\ddn\codex\build\node-playwright-rd206-20260817\node_modules'

node tests/seamgrim_canonical_view_t5h_readiness_audit_runner.mjs
node tests/seamgrim_canonical_view_t5h_status_totality_mutation_runner.mjs
node tests/seamgrim_canonical_view_t5h_playground_surface_identity_audit_runner.mjs
node tests/seamgrim_canonical_view_t5h_playground_option_b_mutation_runner.mjs
node tests/seamgrim_canonical_view_t5h_surface_evidence_audit_runner.mjs
node tests/seamgrim_canonical_view_t5h_surface_evidence_audit_mutation_runner.mjs
node tests/seamgrim_canonical_view_t5h_browser_fallback_readiness_runner.mjs
python tests/run_seamgrim_play_redirect_surface_check.py
python tests/run_seamgrim_runtime_view_source_strict_check.py
git diff --check
```

## 비주장 경계

- 독립 reviewer만 verdict를 발행한다.
- `PASS_WITH_FOLLOW_UP` 또는 `REWORK`이면 T5H를 닫거나 T5I로 진행하지 않는다.
- 이 검토는 public ABI/stable wire, Native implementation, SSOT/SPEC 승격, Web S0, Human PASS를 승인하지 않는다.
