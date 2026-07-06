# MUST_GAP_DEEPDIVE_A01_x_xha_collision_V1

## 대상

- Track A item: `A01`
- SSOT rule: `[V18-00D] X vs X하 이름 충돌 금지`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:875`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:22`
- 산출물 성격: red conformance skeleton + 구현 전 심화조사

## 현재 재검증

현재 브랜치에는 감사 이후 call-tail 일부 구현이 들어와 있다.

- `CALL_TAILS` 후보 집합은 parser/runtime 양쪽에 있다: `tools/teul-cli/src/lang/parser.rs:14`, `tools/teul-cli/src/runtime/eval.rs:30`
- bare call-tail statement lowering이 있다: `tools/teul-cli/src/lang/parser.rs:886`, `tools/teul-cli/src/lang/parser.rs:932`
- runtime은 tail 후보를 모아 단일 후보면 실행하고, 2개 이상이면 `RuntimeError::CallTailAmbiguous`를 낸다: `tools/teul-cli/src/runtime/eval.rs:2421`, `tools/teul-cli/src/runtime/eval.rs:2435`
- 오류 코드는 `E_CALL_TAIL_AMBIGUOUS`로 매핑된다: `tools/teul-cli/src/runtime/error.rs:32`, `tools/teul-cli/src/runtime/error.rs:223`
- 기존 conformance pack도 이 상태를 반영한다: `pack/lang_kernel_v1_conformance/README.md:9`, `pack/lang_kernel_v1_conformance/golden.jsonl:2`

하지만 V18-00D의 직접 요구는 "호출 시 ambiguous fail"이 아니라 "같은 스코프에서 `X`와 `X하`를 서로 다른 씨앗으로 동시에 정의할 수 없다"이다. 현재 확인한 근거는 그 금지를 정의/파싱 시점에 집행하지 못한다.

- 씨앗 alias parser는 `~별명` 중복만 다룬다는 감사 근거가 남아 있다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:22`
- 현재 runtime unit test도 `계산`/`계산하`를 함께 정의한 뒤 호출 시점 ambiguity를 확인한다: `tools/teul-cli/src/runtime/eval.rs:20161`, `tools/teul-cli/src/runtime/eval.rs:20167`

## 판정

- 감사의 "E_CALL_TAIL_AMBIGUOUS 없음" 부분은 현재 브랜치에서 stale이다.
- `X/X하` 정의시 충돌 금지 자체는 아직 red로 남는다.
- 이번 작업은 언어 커널을 고치지 않고, red conformance skeleton만 추가한다.

## 관련 pack 상태

- 기존 `pack/lang_kernel_v1_conformance`는 call-tail ambiguity runtime fail을 이미 다룬다.
- 본 항목의 잔여 gap은 정의 시점 금지이므로 별도 red pack `pack/must_gap_a01_x_xha_collision_red_v1`로 분리했다.
- 새 pack은 `evidence_tier: docs_first`, `closure_claim: no`이며 runtime landed claim이 아니다.

## 결정 필요

- 정의 시점에서 바로 `E_SEED_NAME_CONFLICT_X_HA`류 진단을 낼지, AGE2 별칭 문법이 도입될 때까지 runtime ambiguity fail만 유지할지 결정 필요.
- 오류 코드 이름은 SSOT에 고정되어 있지 않으므로 사용자/SSOT 관리자 결정이 필요하다.
