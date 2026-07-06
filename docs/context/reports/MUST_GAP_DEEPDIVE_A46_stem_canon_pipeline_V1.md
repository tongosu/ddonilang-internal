# MUST_GAP_DEEPDIVE_A46_stem_canon_pipeline_V1

## 대상

- Track A item: `A46`
- SSOT rule: `11.3.4 정본 처리 파이프라인`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3821`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:53`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 움직씨 어간과 형태소 결합을 1) 어간 교대, 2) 어미 결정, 3) 축약 및 표기 정리 + 후행 형태소 결합 순서로 처리해야 한다고 정한다. 현재 제품 경로는 `~별명`을 추가 seed 정의로 확장하고, 런타임에서 고정 call-tail 문자열을 strip해 후보를 찾는다. 어간 교대, 받침 유무 기반 어미 선택, 아/어 선택, 축약/표기 정리, 후행 형태소 결합을 하나의 canonical pipeline으로 집행하는 근거는 확인되지 않는다.

A46은 A45 대표 pack에 연결한다. A45 fixture가 trigger 부재를 직접 겨냥하고, A46은 그 trigger를 포함하는 3-step pipeline 전체의 미착지 상태를 설명한다.

## 근거

- SSOT 11.3.4 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3821`
- 1단계 어간 교대: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3824`
- 2단계 어미 결정: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3828`
- 모음 끼움 쌍 선택: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3829`
- 관형/미래 계열 쌍어미 선택: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3831`
- 아/어 선택 규칙과 추측 금지: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3833`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3834`
- 3단계 축약/표기 정리: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3836`
- 감사 행은 후보 생성/중복 검사/AST 확정 3-step 처리 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:53`
- 현재 parser call-tail 목록은 고정 문자열 목록이다: `tools/teul-cli/src/lang/parser.rs:14`
- 현재 runtime call-tail 목록도 고정 문자열 목록이다: `tools/teul-cli/src/runtime/eval.rs:30`
- 현재 seed alias parser는 별칭을 읽는다: `tools/teul-cli/src/lang/parser.rs:4080`, `tools/teul-cli/src/lang/parser.rs:4087`
- 현재 seed alias는 추가 `Stmt::SeedDef`로 확장된다: `tools/teul-cli/src/lang/parser.rs:4016`, `tools/teul-cli/src/lang/parser.rs:4017`
- 현재 runtime dispatch는 suffix strip으로 후보를 만든다: `tools/teul-cli/src/runtime/eval.rs:2422`, `tools/teul-cli/src/runtime/eval.rs:2423`
- 현재 runtime은 후보 2개 이상에서만 ambiguity 오류를 낸다: `tools/teul-cli/src/runtime/eval.rs:2435`, `tools/teul-cli/src/runtime/error.rs:223`
- A45 대표 red pack은 trigger/pipeline 선행 gap을 고정한다: `pack/must_gap_a45_stem_alternation_trigger_red_v1/README.md:3`, `pack/must_gap_a45_stem_alternation_trigger_red_v1/contract.detjson:2`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 관련 red pack: `pack/must_gap_a45_stem_alternation_trigger_red_v1`

## 결정 필요

- 3-step pipeline을 parser/canon에서 실행해 AST를 확정할지, runtime dispatch 직전의 별도 resolver에서 실행할지 결정 필요.
- 축약/표기 정리는 save/format 출력 전용으로 둘지, 입력 정본화에도 포함할지 결정 필요.
- `E_CALL_TAIL_AMBIGUOUS`와 별도 형태소 pipeline 오류 코드의 관계를 정해야 한다.
