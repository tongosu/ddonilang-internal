# must_gap_a25_josa_canon_tilde_insertion_red_v1

조사 접미사 자동 분리 후 canon `~` 삽입 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: 붙임형 조사 입력이 자동 분리될 때 정본 출력에 `~`가 삽입되어야 함을 red 기준선으로 남긴다.
- 비범위: 자동 split 구현, canon writer 구현, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6994`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6995`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:57`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A25_josa_canon_tilde_insertion_V1.md`

## 기대 red

`cases/c01_attached_josa_canon/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
