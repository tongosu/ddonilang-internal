# MUST_GAP_DEEPDIVE_A23_ai_end_episode_surface_V1

## 대상

- Track A item: `A23`
- SSOT rule: `AI.1 끝내`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6670`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:46`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 AI/Gym episode 종료 표면으로 `끝내.`를 MUST로 둔다. 현재 NuriGym CLI backend는 step record의 `done` 값을 기록하고 환경별 종료 상태를 다루지만, DDN stdlib/runtime builtin 또는 parser 표면 함수로 `끝내`를 처리하는 제품 경로는 확인되지 않는다.

## 근거

- SSOT AI.1 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6670`
- SSOT 예시 표면 `끝내.`: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:6677`
- NuriGym CLI step record는 `done` 필드를 가진다: `tools/teul-cli/src/cli/nurigym.rs:119`, `tools/teul-cli/src/cli/nurigym.rs:125`
- CLI episode runner는 JSON 입력을 받아 dataset/episode artifacts를 생성한다: `tools/teul-cli/src/cli/nurigym.rs:188`, `tools/teul-cli/src/cli/nurigym.rs:303`, `tools/teul-cli/src/cli/nurigym.rs:334`
- 현재 runtime builtin 목록 근거에는 `말결값`, `아님`, `아니다` 등은 보이나 `끝내` 표면 함수는 없다: `tools/teul-cli/src/runtime/eval.rs:5969`, `tools/teul-cli/src/runtime/eval.rs:5995`
- 직접 검색: `rg -n '끝내' tools/teul-cli/src/lang tools/teul-cli/src/runtime tools/teul-cli/src/cli/nurigym.rs core/src lang/src tool/src` = NO_MATCH
- 감사 행은 `끝내` DDN stdlib/runtime builtin을 찾지 못해 미구현으로 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:46`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a23_ai_end_episode_surface_red_v1`

## 결정 필요

- `끝내`를 DDN runtime builtin으로 둘지, NuriGym 전용 effect statement로 둘지 결정 필요.
- `끝내.` 호출 시 현재 episode의 `done` 처리, reward zeroing 여부, multi-agent/shared-env 전파 범위를 확정해야 한다.
