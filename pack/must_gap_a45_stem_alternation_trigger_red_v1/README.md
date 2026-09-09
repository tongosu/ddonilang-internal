# must_gap_a45_stem_alternation_trigger_red_v1

어간 별칭 교대 트리거 red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: `돕~도우`류 별칭이 모음 시작/모음 끼움 짝어미 trigger와 결합되는 경로가 제품에 없음을 red 기준선으로 남긴다.
- 비범위: parser/runtime 구현, 형태소 사전, formatter 표면 출력, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3810`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER2_V1.md:52`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A45_stem_alternation_trigger_V1.md`

## 기대 red

`cases/c01_vowel_pair_suffix_trigger/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
