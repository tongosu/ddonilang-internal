# seamgrim_trace_predicate_evaluator_v1

봉인 관찰 trace sample에서 보기 반응 조건 4종을 결정적으로 도출하는 순수 evaluator 계약이다.

검증 범위:

- `zero_crossing`, `sign_change`, `extremum`, `tolerance_entry`를 trace sample에서 계산한다.
- 정확한 0, 0 plateau, epsilon 경계, 극대/극소 plateau, tolerance 재진입을 vector로 고정한다.
- 중복 tick, 역순 tick, 누락값, 비유한 수 진단을 고정한다.
- 수동 `utterance_tick` schedule만으로 조건 지원을 주장하지 않는다.
- evaluator 결과는 같은 trace와 rule에서 byte-stable하다.
