# MUST_GAP_DEEPDIVE_A33_imeumssi_body_init_V1

## 대상

- Track A item: `A33`
- SSOT rule: `이름씨 본문 초기화 규칙`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2466`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:54`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `이름씨` 본문 `{}`를 생성 시 1회 실행되는 초기화/준비 본문으로 읽고, 머리의 필드 선언에 대입한 값만 인스턴스 상태에 남긴다고 정한다. 현재 `teul-cli` 제품 경로에서는 `이름씨` surface, constructor init, implicit field 금지 진단 경로가 확인되지 않는다.

## 근거

- SSOT 이름씨 본문 초기화 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2466`
- 본문은 생성 시 1회 실행된다는 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2468`
- 머리 기본값 바인딩 후 본문 실행: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2469`
- 본문 지역 변수/영속 필드/암묵 필드 금지 규칙: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2470`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2471`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2472`
- 올바른 예시는 머리 필드와 본문 대입을 분리한다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2494`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2496`
- 직접 검색: `rg -n '이름씨|KwImeumssi|Imeumssi|NameType|constructor' tools/teul-cli/src/lang tools/teul-cli/src/runtime` = NO_MATCH
- 감사 행은 `이름씨` surface/constructor init 경로 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:54`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a33_imeumssi_body_init_red_v1`

## 결정 필요

- `이름씨`를 현재 ECS/임자 모델의 component type으로 직접 낮출지, 별도 type constructor 계층으로 둘지 결정 필요.
- 본문 내 실행문과 nested seed definition의 static binding 순서를 확정해야 한다.
