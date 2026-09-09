# must_gap_a04_p1_pipe_surface_red_v1

§P1 파이프(해서) red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `해서` 파이프 표면/AST/runtime은 제품 경로에서 확인되지 않는다. 현재 `Pipe` token은 `|`이고 seed literal parameter에만 쓰인다.
- 비범위: parser/runtime 구현, golden 갱신, 오류 코드 확정.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5947`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:19`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A04_p1_pipe_surface_V1.md`

## 기대 red

`cases/c01_haseo_pipe_surface/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
