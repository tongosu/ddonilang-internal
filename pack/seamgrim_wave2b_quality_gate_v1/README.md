# seamgrim_wave2b_quality_gate_v1

Wave 2B G8 최종 제품 품질 관문 pack이다.

브라우저 품질 관문:

- 1440x900, 1280x720, 1024x768, 390x844 viewport.
- 보개 canvas 비어 있지 않음과 충분한 크기.
- DDN 원문 접근 가능.
- 가로 overflow/clip 방지.
- 주요 버튼 keyboard activation.
- icon/compact controls tooltip and aria name.
- resolved scene trace replay hash stability.

회귀 관문은 checker에서 기존 Wave 1/Wave 2A와 Wave 2B G3~G7 checker, cargo, core_lang sanity를 함께 실행한다.
