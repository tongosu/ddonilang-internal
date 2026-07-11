# seamgrim_lab_e1_minimal_v1

셈그림 실험실 E1 최소 흐름을 제품 UI에서 검증하는 pack이다.

검증 범위:

- L1 수업 실행 화면에서 DDN 원문이 편집 가능한 상태로 로드된다.
- 조절값 변경이 제품 DDN 입력을 갱신하고 다시 실행한다.
- 실행 이력에 원본 run과 내 버전 run이 기록된다.
- `origin_hash`, `delta_ref`, 비교 상태가 제품 UI에 표시된다.
- 자동 적용, 파일 쓰기, AI 권한 주장은 하지 않는다.

이 pack의 golden은 실행 마커만 검증한다. 실제 제품 행동은 `tests/seamgrim_lab_e1_minimal_runner.mjs`가 검증한다.
