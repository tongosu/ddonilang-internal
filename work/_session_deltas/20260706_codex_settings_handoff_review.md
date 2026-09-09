# 20260706 Codex Session Delta — 설정 헤더 핸드오프 지시문 보정

Status: Pending

## 읽은 문서

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `ARTIFACT_POLICY.md`
- `CLAUDE.md`
- `docs/context/all/DEV_SUMMARY.md`
- `docs/ssot/ssot/SSOT_INDEX_v24.12.9.md`
- `docs/ssot/ssot/SSOT_MASTER_v24.12.9.md`
- `docs/ssot/ssot/SSOT_LANG_v24.12.9.md`
- `docs/ssot/ssot/SSOT_PLATFORM_v24.12.9.md`
- `docs/ssot/ssot/SSOT_TERMS_v24.12.9.md`
- `docs/ssot/appendix/DIALECT_LANGUAGE_LEDGER_V1_20260414.md`
- `docs/ssot/appendix/DIALECT_FULL_SWEEP_LEDGER_V2_20260414.md`
- `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md`

## 반영한 결정

- `docs/ssot/**` 직접 수정 금지 경계를 핸드오프 문서의 공통 불변 경계에 추가했다.
- 지시문 1의 `설정.실행.차림새` preset ↔ `설정.거울.살핌내주기갈래` 교차-절 경로는 SSOT 직접 수정이 아니라 리포트/제안서로 명시하도록 낮췄다.
- 지시문 4의 DoD를 "예시 키 drift 0건" 직접 달성에서 "전수조사표 + 통일안 PROPOSAL + OI 후보"로 낮췄다. SSOT 오너 반영 뒤 별도 단계에서 drift 0건 검증 대상으로 둔다.
- 지시문 5의 reset 관련 구버전 문장을 현행 v24.12.9 reset kind 5종(`마당다시/판다시/누리다시/보개다시/모두다시`) 기준으로 정정했다.
- 지시문 7을 추가했다. 성격은 AUDIT·경계 문구 제안이며, 선언적 시뮬레이션/교육/교착어권 국제 표면/게임 엔진 역할을 `closed / conditional / proposal / not-claim`로 분류하도록 했다.
- `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md`를 추가했다. 보개 표준팩(`grid2d/graph2d/table/timeline/nurigym/seulgi_lab/grid3d/game3d`)과 lowering 계약을 제안한다.
- 핸드오프 문서에 지시문 8(보개 표준팩/lowering 계약 설계)을 추가했다.
- 이후 논의된 사용성 원칙을 제안서에 보강했다. `모양`은 저수준 탈출구이고, 그래프/표/격자/타임라인/시뮬레이션 기본 보기/AI 실험 화면은 표준 보개팩으로 미리 제공해야 한다는 기준을 추가했다.
- 시뮬레이션 보개 기본 제공 항목(좌표계, 축, 격자, 카메라, 확대/축소, 궤적, 벡터, 충돌 영역, 시간 조절, 상태표, 마디/재연 타임라인, state diff)을 추가했다.
- `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md`를 추가했다. 큰마디/속마디, completion, action_status, filter-before-merge, deterministic merge, 슬기 지연마디, `(agent_id, recv_seq)` 실행 정렬을 하나의 실행 계약으로 정리한다.
- 핸드오프 문서에는 기존 지시문 9가 있었으므로, 누리 시간/마디/태스크 경합 계약은 지시문 10으로 추가했다.
- 누리 시간/마디/태스크 경합 제안서에 기본값 평가를 보강했다. 설정을 거의 건드리지 않으면 "동기식 큰마디 commit 기반 결정적 turn/tick engine"에 가깝다고 평가하고, 일반 preset과 고급 preset, 고급 옵션 위험표를 추가했다.
- 핸드오프 지시문 10에도 기본 운용형 평가, 일반 preset/고급 preset 분리, 고급 옵션 위험표를 추가했다.

## 검증

- `git diff --check -- "또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md"` PASS
- `Select-String`으로 `docs/ssot/**` 금지 문장, 지시문 4 DoD, reset 5종 정정 문장 확인
- 지시문 7의 `docs/ssot/**` 수정 0건, parser/runtime 변경 0건, closure 주장 없음 DoD 확인
- 보개 표준팩 제안서는 `docs/context/proposals/`에만 추가했고, `docs/ssot/**`와 parser/runtime은 수정하지 않았다.
- 추가 보강도 문서 제안 범위에만 머물렀고, `docs/ssot/**`와 parser/runtime은 수정하지 않았다.
- 누리 시간/마디/태스크 경합 제안도 `docs/context/proposals/`에만 추가했고, `docs/ssot/**`와 parser/runtime은 수정하지 않았다.
- 기본값/고급 옵션 보강도 문서 제안 범위에만 머물렀고, `docs/ssot/**`와 parser/runtime은 수정하지 않았다.

## 미해결

- `또니랑/` 폴더는 현재 git 미추적 상태다. 사용자가 원하면 적절한 개발 문서 위치로 승격하거나 현재 위치를 유지할지 결정해야 한다.
- 보개 표준팩은 아직 PROPOSAL 단계다. 실제 pack skeleton, renderer helper, web2d/console parity 테스트는 후속 작업이다.
- 누리 시간/마디/태스크 경합도 아직 PROPOSAL 단계다. 실제 pack skeleton, merge policy closure, `지연마디` 소유권 결정은 후속 작업이다.
