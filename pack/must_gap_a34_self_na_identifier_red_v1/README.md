# must_gap_a34_self_na_identifier_red_v1

`이름씨` 본문 자기참조 `나` red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `나`가 `이름씨` 본문 안에서 현재 객체를 가리키고 본문 밖에서는 존재하지 않아야 함을 red 기준선으로 남긴다.
- 비범위: `이름씨` 구현, self binding/runtime 구현, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2542`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:55`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A34_self_na_identifier_V1.md`

## 기대 red

`cases/c01_na_self_in_imeumssi/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
