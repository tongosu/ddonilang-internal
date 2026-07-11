# seamgrim_sealed_observation_trace_v1

진자 수업의 제품 WASM 실행에서 `dotbogi` timeline에 쌓인 관찰 샘플을 봉인 trace artifact로 노출하는 계약을 검증한다.

검증 범위:

- 입력은 제품 실행이 만든 `tick_id`, `t`, `theta`, `omega` 샘플이다.
- console 문자열 파싱 없이 제품 observation timeline에서 artifact를 만든다.
- artifact schema는 `seamgrim.sealed_observation_trace.v1`이다.
- artifact와 hash 후보는 `state_hash`에 참여하지 않는다.
- 이 pack은 아직 4조건 evaluator 완료를 주장하지 않는다.
