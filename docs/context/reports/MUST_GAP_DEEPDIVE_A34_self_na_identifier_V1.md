# MUST_GAP_DEEPDIVE_A34_self_na_identifier_V1

## 대상

- Track A item: `A34`
- SSOT rule: `자기 참조 나`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2542`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:55`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `나`를 `이름씨` 본문 안에서 현재 객체를 가리키는 읽기 전용 특별 식별자로 정의한다. 현재 `teul-cli`에는 임자/root 계층의 `제` 처리 경로는 있지만, `이름씨` 본문 안의 `나` 자동 바인딩, 타입 제한, 본문 밖 금지 경로는 확인되지 않는다.

## 근거

- SSOT `나` 자기참조 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2542`
- `나` 의미 설명: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2544`
- `이름씨` 본문 안 자동 바인딩/타입/읽기 전용/본문 밖 금지: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2549`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2550`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2551`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2553`
- `나`와 `제`는 서로 다른 층위의 특별 식별자다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2023`
- 현재 parser는 root path로 `살림/바탕/샘/제`를 인식한다: `tools/teul-cli/src/lang/parser.rs:6031`
- runtime은 `제` root를 현재 actor/entity 계층으로 처리한다: `tools/teul-cli/src/runtime/eval.rs:2195`, `tools/teul-cli/src/runtime/eval.rs:7028`
- 직접 검색: `rg -n '\"나\"|나\\.' tools/teul-cli/src/runtime/eval.rs tools/teul-cli/src/lang/parser.rs tools/teul-cli/src/lang/lexer.rs` 결과는 일반 문자열/예제 수준이며, self binding 구현 근거가 아니다.
- 감사 행은 `제`만 구현되고 `나` self 경로가 없어 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:55`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a34_self_na_identifier_red_v1`

## 결정 필요

- `나`를 `이름씨` constructor/init frame의 lexical binding으로 둘지, runtime object receiver slot으로 둘지 결정 필요.
- `나` 캡처 허용 범위와 `제`와의 충돌/동시 사용 진단을 확정해야 한다.
