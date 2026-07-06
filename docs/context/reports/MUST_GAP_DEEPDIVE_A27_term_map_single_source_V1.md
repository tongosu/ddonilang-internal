# MUST_GAP_DEEPDIVE_A27_term_map_single_source_V1

## 대상

- Track A item: `A27`
- SSOT rule: `[V18-00A-1] TERM-MAP 단일 소스`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:935`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:26`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 Gate0 TERM-LINT/NAME-LINT가 SSOT TERM-MAP을 유일한 근거로 삼아 FATAL/LEGACY 정책을 강제해야 한다고 정한다. 현재 제품 경로에서 확인되는 것은 `TERM_MAP_VERSION` 문자열과 repro report에 그 문자열을 싣는 경로뿐이며, SSOT TERM-MAP을 추출해 lint/canon의 단일 근거 테이블로 쓰는 제품 경로는 확인되지 않는다.

## 근거

- SSOT TERM-MAP 단일 소스 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:935`
- TERM-LINT/NAME-LINT가 TERM-MAP을 유일한 근거로 삼아야 한다는 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:937`
- TERM-MAP 확장/변경 정책: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:944`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:946`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:947`
- 현재 legacy tool에는 `TERM_MAP_VERSION` 문자열 상수만 있다: `tool/src/main.rs:60`
- 해당 문자열은 repro report 메타데이터에 실린다: `tool/src/main.rs:749`
- 직접 검색: `rg -n 'TERM-MAP|TERM_MAP|fatal_terms|term map' tools/teul-cli/src core/src tool/src` 결과는 `tool/src/main.rs:60`, `tool/src/main.rs:749` 수준이며, `fatal_terms` 기반 lint 테이블/추출기는 확인되지 않는다.
- 감사 행은 TERM-MAP 테이블/추출/치명어 테이블 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:26`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a27_term_map_single_source_red_v1`

## 결정 필요

- TERM-MAP 추출기를 빌드 단계 codegen으로 둘지, 런타임에 SSOT JSON 블록 해시를 읽는 방식으로 둘지 결정 필요.
- FATAL/LEGACY/WARN 정책을 `teul-cli` canon, lint, LSP quick-fix 중 어느 계층에서 authoritative하게 적용할지 결정 필요.
