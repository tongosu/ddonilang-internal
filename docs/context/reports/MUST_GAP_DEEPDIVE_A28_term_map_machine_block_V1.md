# MUST_GAP_DEEPDIVE_A28_term_map_machine_block_V1

## 대상

- Track A item: `A28`
- SSOT rule: `기계 판독용 TERM-MAP 블록`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:993`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:27`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 TERM-MAP의 기계 판독용 JSON 블록을 두고, 이 블록의 해시가 TermMap 해시의 근거가 된다고 정한다. 현재 제품 경로에서 확인되는 것은 version 문자열 메타데이터뿐이며, SSOT JSON 블록을 추출/검증/codegen하여 lint 상수와 해시 근거로 쓰는 경로는 확인되지 않는다.

## 근거

- SSOT 기계 판독용 TERM-MAP 블록 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:993`
- TermMap 해시 근거 설명: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:999`
- `fatal_terms` JSON 필드 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1000`
- `legacy_terms` JSON 필드 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1197`
- 현재 legacy tool의 `TERM_MAP_VERSION` 상수: `tool/src/main.rs:60`
- repro report는 version 문자열을 싣지만 JSON 블록 해시를 검증하지 않는다: `tool/src/main.rs:749`
- 직접 검색: `rg -n 'TERM-MAP|TERM_MAP|fatal_terms|term map' tools/teul-cli/src core/src tool/src`에서 extractor/codegen/해시 검증 경로는 확인되지 않는다.
- 감사 행은 extractor/codegen 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:27`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a27_term_map_single_source_red_v1`

## 결정 필요

- SSOT markdown 내부 JSON 블록을 제품 빌드가 직접 읽을지, 별도 generated artifact를 승인 후 생성할지 결정 필요.
- TermMap hash를 report metadata, lint diagnostic, pack contract 중 어디에 필수로 실을지 결정해야 한다.
