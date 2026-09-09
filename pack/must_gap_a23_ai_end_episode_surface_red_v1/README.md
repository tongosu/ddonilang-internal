# must_gap_a23_ai_end_episode_surface_red_v1

AI/Gym episode 종료 표면 `끝내.` red conformance skeleton이다.

- evidence_tier: `docs_first`
- current_status: `designed`
- closure_claim: `no`

## 범위

- 목표: DDN 표면 함수/문장 `끝내.`가 episode 종료 의미로 처리되어야 함을 red 기준선으로 남긴다.
- 비범위: runtime builtin 구현, NuriGym effect wiring, golden 갱신.

## 근거

- SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6670`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6677`
- 감사: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:46`
- deepdive: `docs/context/reports/MUST_GAP_DEEPDIVE_A23_ai_end_episode_surface_V1.md`

## 기대 red

`cases/c01_end_episode_surface/input.ddn`은 현재 구현을 고치기 전까지 red 기준선이다. 이 pack은 실행용 golden이 아니며 `closure_claim: no`를 유지한다.
