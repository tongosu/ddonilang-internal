# MUST_GAP_DEEPDIVE_A32_assign_arrow_right_V1

## 대상

- Track A item: `A32`
- SSOT rule: `[ASSIGN-ARROW-RIGHT-01] -> 우향 대입`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1908`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:42`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `식 -> 자리.`를 입력 설탕으로 허용하고 정본 출력은 반드시 `자리 <- 식.`으로 수렴해야 한다고 정한다. 현재 `teul-cli` lexer/token/parser에는 `<-`용 `Arrow`, `<<-`용 `FlowArrow`, `~~>`용 `SignalArrow`는 있지만, 대입용 `->` 또는 `RightArrow` token/canon path는 확인되지 않는다.

## 근거

- SSOT 우향 대입 규칙 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1908`
- `식 -> 자리.` 의미: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1911`
- `A -> B.`를 `B <- A.`로 정본화해야 한다는 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1913`
- 우항 L-Value 요구와 낮은 우선순위: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1916`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1920`
- 현재 token enum에는 `Arrow`, `FlowArrow`, `SignalArrow`가 있으나 `RightArrow`는 없다: `tools/teul-cli/src/lang/token.rs:74`, `tools/teul-cli/src/lang/token.rs:75`, `tools/teul-cli/src/lang/token.rs:76`
- lexer는 `<<-`와 `<-`를 각각 `FlowArrow`/`Arrow`로 읽는다: `tools/teul-cli/src/lang/lexer.rs:296`, `tools/teul-cli/src/lang/lexer.rs:323`
- parser assignment 경로는 `Arrow`/`Equal`/복합 화살표를 소비한다: `tools/teul-cli/src/lang/parser.rs:713`, `tools/teul-cli/src/lang/parser.rs:717`
- 감사 행은 `->`/`RightArrow` 구현 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1_V1.md:42`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a32_assign_arrow_right_red_v1`

## 결정 필요

- `->`를 lexer token으로 둘지, parser에서 `Minus` + `Gt`를 sugar로 조립할지 결정 필요.
- 대입용 `->`와 타입 시그니처 `T -> U`의 문맥 충돌을 어느 단계에서 분리할지 결정해야 한다.
