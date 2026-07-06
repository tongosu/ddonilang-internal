# MUST_GAP_DEEPDIVE_A44_stem_ambiguity_no_guess_principle_V1

## 대상

- Track A item: `A44`
- SSOT rule: `11.3.1 원칙`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3790`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:50`
- 산출물 성격: GOAL-MUSTAUDIT stale 판정 재검증 + 잔여 red 연결

## 현재 재검증

SSOT 11.3.1은 내부 정규형 1개, 표면 추천/출력 분리, 표면형 역추적 후보 2개 이상 시 추측 금지를 요구한다. 감사 행은 당시 제품 경로에 call-tail ambiguity 오류/후보 수집이 없다고 보아 미구현으로 분류했다.

현재 브랜치에는 call-tail 후보 수집과 `E_CALL_TAIL_AMBIGUOUS`가 착지해 감사 근거 일부는 stale이다. 다만 SSOT 11.3.1 전체 원칙이 닫힌 것은 아니다. A01에서 정의 시점 `X`/`X하` 충돌 금지가 red로 남아 있고, A02에서 0개 후보 전용 unresolved 진단이 red로 남아 있다. 따라서 A44는 신규 대표 pack을 만들지 않고 A01/A02의 잔여 red pack에 연결한다.

## 근거

- SSOT 11.3 원칙 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3790`
- 내부 정규형 1개 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3791`
- 표면 추천/출력 분리 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3792`
- 모호성 추측 금지 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3793`
- 감사 행은 call-tail ambiguity 후보 수집 부재를 근거로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:50`
- 현재 parser/runtime call-tail 후보 목록: `tools/teul-cli/src/lang/parser.rs:14`, `tools/teul-cli/src/runtime/eval.rs:30`
- 현재 runtime은 tail 후보를 모두 수집한다: `tools/teul-cli/src/runtime/eval.rs:2422`
- 후보 1개면 실행한다: `tools/teul-cli/src/runtime/eval.rs:2428`
- 후보 2개 이상이면 `CallTailAmbiguous`를 낸다: `tools/teul-cli/src/runtime/eval.rs:2435`, `tools/teul-cli/src/runtime/eval.rs:2436`
- 오류 코드는 `E_CALL_TAIL_AMBIGUOUS`다: `tools/teul-cli/src/runtime/error.rs:32`, `tools/teul-cli/src/runtime/error.rs:223`
- 기존 conformance pack은 이 상태를 반영한다: `pack/lang_kernel_v1_conformance/README.md:9`, `pack/lang_kernel_v1_conformance/README.md:16`
- A01 잔여 red는 정의 시점 `X`/`X하` 충돌 금지다: `docs/context/reports/MUST_GAP_DEEPDIVE_A01_x_xha_collision_V1.md:27`, `docs/context/reports/MUST_GAP_DEEPDIVE_A01_x_xha_collision_V1.md:38`
- A02 잔여 red는 0개 후보 전용 unresolved 진단이다: `docs/context/reports/MUST_GAP_DEEPDIVE_A02_call_tail_resolve_unresolved_V1.md:12`, `docs/context/reports/MUST_GAP_DEEPDIVE_A02_call_tail_resolve_unresolved_V1.md:19`

## 판정

- 현재 판정: 부분 해소 / 잔여 red 유지
- 언어 커널 구현 변경: 없음
- 관련 green-ish pack: `pack/lang_kernel_v1_conformance`
- 관련 red pack: `pack/must_gap_a01_x_xha_collision_red_v1`, `pack/must_gap_a02_call_tail_resolve_unresolved_red_v1`

## 결정 필요

- 11.3.1 원칙의 닫힘 기준을 runtime call-tail ambiguity만으로 볼지, 정의 시점 이름 충돌 금지와 0개 후보 전용 진단까지 포함해 볼지 결정 필요.
- 표면 추천/출력 계층(LSP/formatter/canon export)의 닫힘 기준 pack을 별도 분리할지 결정 필요.
