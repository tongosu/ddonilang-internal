# must_gap_a33_imeumssi_body_init_red_v1

`이름씨` 본문 초기화 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `이름씨` 생성 시 본문이 1회 실행되고 머리 필드 대입만 인스턴스 상태에 남아야 함을 red 기준선으로 남긴다.
- 비범위: type/constructor/runtime 구현, ECS lowering 결정, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2466`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:54`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A33_imeumssi_body_init_V1.md`

## 기대 red

`cases/c01_imeumssi_body_init/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
