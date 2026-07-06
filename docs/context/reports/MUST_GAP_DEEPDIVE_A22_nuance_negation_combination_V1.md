# MUST_GAP_DEEPDIVE_A22_nuance_negation_combination_V1

## 대상

- Track A item: `A22`
- SSOT rule: `뉘.3 부정과의 조합`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6769`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:50`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 부정과 말결이 함께 사용될 때 결합 규칙을 별도 MUST로 둔다. 현재 runtime에는 논리 부정 builtin `아님`/`아니다`와 문자열 기반 `말결값`이 각각 존재하지만, `$말결` token과 부정어를 같은 문장 의미론으로 결합하는 제품 경로는 확인되지 않는다.

## 근거

- SSOT 뉘.3 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6769`
- 부정과 말결의 동시 사용 규칙 anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6772`
- 현재 runtime의 부정 builtin 분기: `tools/teul-cli/src/runtime/eval.rs:2760`
- 현재 말결 weight 계산은 `말결값` builtin과 `nuance_weight` 함수에 갇혀 있다: `tools/teul-cli/src/runtime/eval.rs:5235`, `tools/teul-cli/src/runtime/eval.rs:15617`
- builtin 허용 목록에서도 `말결값`과 `아님`/`아니다`는 별도 이름이다: `tools/teul-cli/src/runtime/eval.rs:5969`, `tools/teul-cli/src/runtime/eval.rs:5995`
- 감사 행은 부정 결합 규칙을 미구현으로 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:50`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a20_nuance_token_combination_red_v1`

## 결정 필요

- `아님`이 논리값 자체를 뒤집을 때 말결 weight를 어떻게 보존/반전할지 결정 필요.
- `$전혀` 같은 0.0 계열과 부정어가 결합할 때 결과 weight의 하한/상한 및 정본 표현을 확정해야 한다.
