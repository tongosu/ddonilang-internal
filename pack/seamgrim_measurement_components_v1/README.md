# seamgrim_measurement_components_v1

Wave 2B G4의 한국어 Manim 측정 부품 가족을 제품 경로에서 검증하는 pack이다.

범위:

- 기존 `seamgrim.view_plan.v1` 위에서 각도재기, 길이재기, 벡터 화살표, 좌표축·눈금, 궤적선을 만든다.
- 부품은 세계 상태를 읽기만 하며 `state_hash`에 참여하지 않는다.
- 제품 실행 화면에서 각 부품을 켜고 끌 수 있어야 한다.
- 접근성 이름, 단위/의미 이름, view hash 후보와 world draw payload hash 후보를 산출한다.

이 pack의 golden은 실행 마커만 검증한다. 실제 제품 동작은 `tests/seamgrim_measurement_components_runner.mjs`와 `tests/run_seamgrim_measurement_components_check.py`가 검증한다.
