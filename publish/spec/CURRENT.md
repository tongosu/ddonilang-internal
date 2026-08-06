# 또니랑 공개 언어 스펙

현재 공개판: [`v0.5.0`](./v0.5.0/SPEC_MANIFEST_v0.5.0.md)

이전 공개판: [`v0.4.0`](./v0.4.0/SPEC_MANIFEST_v0.4.0.md)

검토 완료 후보 보존본: [`v0.5.0-candidate-r3`](./v0.5.0-candidate-r3/SPEC_MANIFEST_v0.5.0.md), [`v0.4.0-candidate`](./v0.4.0-candidate/SPEC_MANIFEST_v0.4.0.md)

관리자 자체 검사 실패 보존본: [`v0.5.0-candidate`](./v0.5.0-candidate/SPEC_MANIFEST_v0.5.0.md), [`v0.5.0-candidate-r2`](./v0.5.0-candidate-r2/SPEC_MANIFEST_v0.5.0.md), [`v0.5.0-public-promotion-preclosure-failed-r1`](./v0.5.0-public-promotion-preclosure-failed-r1/SPEC_MANIFEST_v0.5.0.md)

- `v0.5.0`은 내부 SSOT `v24.24.1`의 RD-001~RD-122와 KSL·표준 그래프·
  공통 모형 계약을 투영한 docs-first 공개판이며, 독립 검토
  `PASS / 13 of 13 / NO CORRECTIONS`와 2026-08-03 owner 최종 승격 지시를 거쳤다.
- `v0.4.0`은 내부 SSOT `v24.22.1` 시점의 고정 공개판이다.
- `v0.3.0`은 내부 SSOT `v24.17.1` 시점의 고정 공개 스냅샷이다.
- 내부 SSOT live current는 2026-08-06부터 `v24.25.0`이다. 공개판 `v0.5.0`은
  `v24.24.1` 시점의 고정 투영판으로 소급 수정하지 않는다.
- `v0.5.0-candidate-r3`는 독립 검토가 끝난 승격 입력으로 byte 보존한다.
- 첫 `v0.5.0-candidate`와 R2는 각각 형식·계승 의미 자체 검사 실패판으로 byte 보존한다.
- 첫 public 생성본은 후보 표지 잔존을 self-check에서 발견한 pre-closure 실패판으로 byte 보존한다.
- `v0.4.0-candidate`와 `v0.3.0`은 제자리에서 byte 보존한다.
- `v0.2.1`과 이전 공개 초안은 제자리 보존한다.
- P1·C-02·C-04·C-05·C-06·KS 최종 syntax·exact wire·제품 관문은 OPEN이다.
- 문서 public current와 제품 구현·runtime landed·기본 배포는 분리한다.
- 내부 SSOT와 공개 Language SPEC은 별도 버전 계보다. 충돌하면 internal current가 우선한다.
