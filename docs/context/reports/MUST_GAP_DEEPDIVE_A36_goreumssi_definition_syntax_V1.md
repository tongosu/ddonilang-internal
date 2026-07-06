# MUST_GAP_DEEPDIVE_A36_goreumssi_definition_syntax_V1

## 대상

- Track A item: `A36`
- SSOT rule: `고름씨 정의 문법`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2654`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:59`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `행동:고름씨 = { #대기 ... }.` 형태의 정의 문법과 variant field 순서/ABI 규칙을 둔다. 현재 `teul-cli` parser의 seed kind 인식은 `셈씨/움직씨` 중심이고, `고름씨` 정의 헤더와 variant list를 type declaration으로 파싱하는 경로는 확인되지 않는다.

## 근거

- SSOT 고름씨 정의 문법 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2654`
- 표준 정의 예시: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2657`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2661`
- variant 이름은 `#원자`, field 순서는 ABI 순서다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2664`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2665`
- field 기본값 허용: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2666`
- 현재 `SeedKind::from_name`은 `셈씨/움직씨`만 정본 kind로 인식한다: `tools/teul-cli/src/lang/ast.rs:23`, `tools/teul-cli/src/lang/ast.rs:26`, `tools/teul-cli/src/lang/ast.rs:27`
- 현재 atom expression parser는 `#atom` 값만 만든다: `tools/teul-cli/src/lang/parser.rs:5107`, `tools/teul-cli/src/lang/parser.rs:5110`
- 감사 행은 `고름씨` 정의 파서 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:59`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a35_goreumssi_tag_union_red_v1`

## 결정 필요

- `고름씨` 정의를 기존 seed parser에 통합할지, type declaration parser로 분리할지 결정 필요.
- variant field default와 ABI ordering을 canon/state_hash 경계에서 어떻게 직렬화할지 결정해야 한다.
