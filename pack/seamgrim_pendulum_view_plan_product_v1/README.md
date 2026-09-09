# seamgrim_pendulum_view_plan_product_v1

진자 세계의 명시적 view plan 제품 배선을 검증하는 pack이다.

검증 범위:

- `rep_phys_pendulum_wave1_v1` DDN을 제품 CLI frontdoor와 WASM frontdoor로 실행한다.
- view plan anchor `obs.theta`, `obs.angular_velocity`, `obs.pivot`, `obs.bob`, `obs.time`을 이름 추측 없이 사용한다.
- 각도재기 baseline/current/arc/label이 같은 `obs.theta`에서 나온다.
- 그래프 현재점, 관찰 패널 각도값, 보개 추 위치가 같은 실행 결과를 가리킨다.
- 각도재기 표시 on/off는 view-only이며 `state_hash`를 바꾸지 않는다.
- camera policy `fixed`, `fit`, `follow`를 제품 UI에서 바꿔도 `state_hash`와 world-coordinate draw payload 후보 해시는 유지된다. 이 FNV 후보값은 정본 `bogae_hash=blake3(detbin)`를 주장하지 않는다.

이 pack의 golden은 실행 마커만 검증한다. 실제 제품 행동은 `tests/seamgrim_pendulum_view_plan_product_runner.mjs`가 검증한다.
