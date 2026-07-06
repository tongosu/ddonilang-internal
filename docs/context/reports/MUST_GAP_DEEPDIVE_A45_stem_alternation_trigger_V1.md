# MUST_GAP_DEEPDIVE_A45_stem_alternation_trigger_V1

## 대상

- Track A item: `A45`
- SSOT rule: `11.3.3 교대 트리거`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3810`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:52`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `돕~도우` 같은 어간 별칭이 모음 시작 어미와 모음 끼움 짝어미 계열을 만났을 때 정본 분류 기반으로 교대를 적용해야 한다고 정한다. 현재 제품 경로는 `~별명`을 추가 seed 정의로 확장하고, 런타임 call-tail dispatch에서 정해진 suffix 문자열을 strip하는 구조다. `니/으니`, `면/으면`, `니까/으니까`, `며/으며`, `면서/으면서` 같은 어미 정본 분류와 교대 trigger table은 확인되지 않는다.

감사 행의 "CALL_TAIL 없음" 근거는 A44처럼 일부 stale이지만, A45의 핵심인 어미 분류 기반 교대 트리거는 여전히 red다.

## 근거

- SSOT 11.3.3 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3810`
- 모음 시작 어미 trigger: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3812`
- 모음 끼움 짝어미 trigger: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3813`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3815`
- trigger 판정은 표면 첫 글자가 아니라 어미 토큰 정본 분류 기준이다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3817`
- 보수 규칙: 모호/미지정 trigger는 교대 미적용이다: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3819`
- 감사 행은 trigger 집합/활용 파이프라인 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:52`
- 현재 parser call-tail 목록은 고정 문자열 목록이다: `tools/teul-cli/src/lang/parser.rs:14`
- 현재 runtime call-tail 목록도 고정 문자열 목록이다: `tools/teul-cli/src/runtime/eval.rs:30`
- 현재 seed alias parser는 `~별명`을 읽어 alias seed를 추가한다: `tools/teul-cli/src/lang/parser.rs:4080`, `tools/teul-cli/src/lang/parser.rs:4087`, `tools/teul-cli/src/lang/parser.rs:4105`
- alias는 추가 `Stmt::SeedDef`로 확장된다: `tools/teul-cli/src/lang/parser.rs:4016`, `tools/teul-cli/src/lang/parser.rs:4017`
- 현재 unit test도 `막~막으~막아`가 추가 seed 이름으로 확장되는지만 확인한다: `tools/teul-cli/src/lang/parser.rs:7630`
- 현재 runtime dispatch는 suffix strip으로 후보를 만든다: `tools/teul-cli/src/runtime/eval.rs:2422`, `tools/teul-cli/src/runtime/eval.rs:2423`
- 직접 검색: `rg -n 'vowel|받침|으니|니까|으면|어서|교대|Stem Alternation|suffix selection' tools/teul-cli/src`에서 SSOT 11.3.3 trigger table 구현 근거 없음

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a45_stem_alternation_trigger_red_v1`

## 결정 필요

- trigger table을 parser/canon 단계에서 표면 이름으로 낮출지, runtime seed dispatch 전에 후보 생성기로 둘지 결정 필요.
- `니/으니`, `면/으면`, `니까/으니까`, `며/으며`, `면서/으면서`의 최소 Gate0 scope와 오류 코드를 확정해야 한다.
- A46의 3-step pipeline과 같은 pack으로 닫을지, trigger 전용 pack과 pipeline 전용 pack을 분리할지 결정 필요.
