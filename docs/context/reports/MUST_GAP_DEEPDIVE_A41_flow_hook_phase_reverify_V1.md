# MUST_GAP_DEEPDIVE_A41_flow_hook_phase_reverify_V1

## 대상

- Track A item: `A41`
- SSOT rule: `7.3 흐름씨-훅 위상 분리`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2986`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:27`
- 산출물 성격: GOAL-MUSTAUDIT stale 판정 재검증

## 현재 재검증

감사 행은 `<<-` 흐름씨 surface, fixed-point, conflict/cycle 진단이 제품 경로에 없다고 보아 미구현으로 분류했다. 그러나 현재 `tools/teul-cli`에는 `FlowArrow`, `Stmt::FlowAssign`, `apply_flow_fixed_point`, `E_FLOW_MULTIPLE_SOURCE_CONFLICT`, `E_FLOW_CIRCULAR_REFERENCE`가 확인된다. 기존 `pack/lang_flow_hook_interaction_v1`도 `evidence_tier: runtime`, `closure_claim: yes`로 바뀌어 있으며, 현재 checker는 네 케이스를 제품 runtime으로 실행한다.

따라서 A41은 신규 red pack 대상이 아니라 감사 stale / 재분류 필요 항목으로 기록한다. 이 보고서는 기존 닫힘 주장을 승인하지 않고, 근거 차이를 남긴다.

## 근거

- SSOT §7.3 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2986`
- fixed-point 단계: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2992`
- P1-P6 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2997`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2998`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2999`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3000`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3001`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3002`
- SSOT가 지정한 pack: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3009`
- 감사 행의 기존 미구현 근거: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:27`
- 이전 검증 보고서는 당시 제품 경로가 `<<-`를 받지 못한다고 기록했다: `docs/context/reports/FLOW_HOOK_PHASE_SEPARATION_VERIFICATION_V1.md:12`
- 현재 lexer token: `tools/teul-cli/src/lang/token.rs:75`, `tools/teul-cli/src/lang/lexer.rs:296`
- 현재 parser flow assign 분기: `tools/teul-cli/src/lang/parser.rs:692`, `tools/teul-cli/src/lang/parser.rs:703`
- 현재 parser unit test: `tools/teul-cli/src/lang/parser.rs:6792`, `tools/teul-cli/src/lang/parser.rs:6800`
- 현재 runtime flow state/record: `tools/teul-cli/src/runtime/eval.rs:105`, `tools/teul-cli/src/runtime/eval.rs:305`
- 현재 runtime fixed-point 호출: `tools/teul-cli/src/runtime/eval.rs:721`, `tools/teul-cli/src/runtime/eval.rs:748`, `tools/teul-cli/src/runtime/eval.rs:792`
- 현재 runtime flow assign 기록/적용: `tools/teul-cli/src/runtime/eval.rs:980`, `tools/teul-cli/src/runtime/eval.rs:1008`, `tools/teul-cli/src/runtime/eval.rs:1917`
- 현재 error code mapping: `tools/teul-cli/src/runtime/error.rs:224`, `tools/teul-cli/src/runtime/error.rs:225`
- 현재 runtime tests: `tools/teul-cli/src/runtime/eval.rs:15956`, `tools/teul-cli/src/runtime/eval.rs:15988`, `tools/teul-cli/src/runtime/eval.rs:16020`, `tools/teul-cli/src/runtime/eval.rs:16044`
- 기존 pack README는 runtime/closure yes를 주장한다: `pack/lang_flow_hook_interaction_v1/README.md:5`, `pack/lang_flow_hook_interaction_v1/README.md:6`, `pack/lang_flow_hook_interaction_v1/README.md:8`, `pack/lang_flow_hook_interaction_v1/README.md:9`
- 기존 pack contract도 runtime/closure yes다: `pack/lang_flow_hook_interaction_v1/contract.detjson:3`, `pack/lang_flow_hook_interaction_v1/contract.detjson:4`
- 현재 checker는 runtime tier와 closure yes를 검사한다: `tests/run_lang_flow_hook_interaction_pack_check.py:169`, `tests/run_lang_flow_hook_interaction_pack_check.py:171`
- 현재 checker runtime output: `python tests/run_lang_flow_hook_interaction_pack_check.py` PASS, `runtime_checks=5`

## 판정

- 현재 판정: red 유지 아님, 재분류 필요
- 언어 커널 구현 변경: 없음
- 신규 red pack: 만들지 않음
- 관련 pack: `pack/lang_flow_hook_interaction_v1`

## 결정 필요

- `SSOT_MUST_RULE_AUDIT_TIER2_V1.md`의 A41 행을 다음 감사 라운드에서 `미구현`에서 `구현/검증됨 후보` 또는 `추가 검증 필요`로 재분류할지 결정 필요.
- 이전 `FLOW_HOOK_PHASE_SEPARATION_VERIFICATION_V1.md`는 현재 코드와 충돌하므로, 별도 문서 정정/폐기/후속 검증 보고서 승격 여부 결정 필요.
- `closure_claim: yes`를 공식 behavior-closed로 인정하려면 core_lang sanity 외에 해당 pack checker를 정규 CI 게이트에 포함할지 결정 필요.
