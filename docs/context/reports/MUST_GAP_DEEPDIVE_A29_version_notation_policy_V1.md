# MUST_GAP_DEEPDIVE_A29_version_notation_policy_V1

## 대상

- Track A item: `A29`
- SSOT rule: `[V18-00B] 버전 표기 정책`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1355`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:28`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 문서 보강/명세 명료화는 PATCH, 하위호환 파괴는 MAJOR, 호환 기능 추가는 MINOR로 표기해야 한다고 정한다. 현재 tool/teul-cli AI prompt helper에는 `v...` 형식 문자열 파서와 버전 비교 함수가 있지만, `r1/r2` 같은 revision 표기를 금지하거나 SSOT 문서 변경 종류를 PATCH/MINOR/MAJOR 정책에 맞춰 검사하는 제품 경로는 확인되지 않는다.

## 근거

- SSOT 버전 표기 정책 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1355`
- PATCH/MINOR/MAJOR 정책: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1357`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1358`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1359`
- legacy tool AI prompt helper는 `v...` 문자열을 version-like로 파싱한다: `tool/src/ai_prompt.rs:325`, `tool/src/ai_prompt.rs:330`
- `teul-cli` AI prompt helper도 같은 형태의 version parser/comparator를 가진다: `tools/teul-cli/src/ai_prompt.rs:290`, `tools/teul-cli/src/ai_prompt.rs:295`
- 직접 검색: `rg -n 'revision|r1|r2' tools/teul-cli/src core/src tool/src` 결과는 일반 변수명/테스트 값 수준이며, 문서 revision 표기 금지 정책 집행 지점은 확인되지 않는다.
- 감사 행은 버전 파싱은 있으나 SSOT 문서/언어 리비전 표기 금지 검사가 없어 미구현으로 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:28`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a29_version_notation_policy_red_v1`

## 결정 필요

- 이 정책을 docs lint로 둘지, SSOT release helper로 둘지, AI prompt 생성 단계의 hard gate로 둘지 결정 필요.
- `r1/r2` 탐지를 단순 regex로 할지, 문맥상 revision 표기만 골라낼지 기준이 필요하다.
