# SESSION_DELTA

- 작성일: 2026-07-17
- 작성 주체: Codex
- 세션명: goal-expansion-business-readability-collaboration
- 관련 SSOT: `docs/ssot/ssot/*_v24.15.1.md` (읽기 전용)

## 결정된 것

| 상태 | 관련 모듈 | 내용 | 근거/파일 |
|---|---|---|---|
| Reflected | 장기 목표 | 기존 7축 목표를 설계 철학, 결정론 엔진, 언어 구현, 한국어 가독성, 셈그림 UX, 교육 효과, AI 안전성, 창작자 가지 생태계, 사업성·시장 검증의 9축으로 확장한다. | 사용자 지시 2026-07-17, 이 session delta |
| Reflected | 한국어 가독성 | 순우리말 수가 아니라 낯선 사용자의 원문 이해·결과 예측·수정·진단 복구·낭독·접근성·일반 프로그래밍 개념 전이로 판정한다. | 사용자 지시와 독립 세션 검토 |
| Reflected | 사업성 | 물리 차시 wedge, 체험→첫 실행→창작→공유 funnel, 반복 사용, 콘텐츠 재사용, 도입·구매 의사, 제작·지원 비용, LTS·보안·라이선스·배포 준비를 외부 증거로 판정한다. | 사용자 지시와 독립 세션 검토 |
| Reflected | 다중 AI 검토 | 주요 중간 산출물은 같은 snapshot/hash·DoD·증거 목록을 Claude, Gemini, 독립 Codex 세션에 주고 각각 반례 검토를 받는다. | `CLAUDE.md`, `GEMINI.md`, Web AI context bundle |
| Reflected | 검토 권위 | 외부 AI 답변은 Proposal이며 모델 간 다수결로 승격하지 않는다. SSOT, 실제 제품 경로, 검증 명령, 외부 사용자 증거를 우선한다. | `AGENT_WORKFLOW.md`, `SSOT_POLICY.md` |
| Reflected | 분업 경계 | 다른 세션에는 경로·산출물·검증이 겹치지 않는 bounded task만 위임한다. 주 세션이 쓰기 소유권과 통합 순서를 봉인한다. | 현재 대규모 dirty worktree 보호 |

## 조정된 장기 목표

사업성을 포함해 또니랑을 실제 10점 수준으로 끌어올린다. 평가는 설계 철학, 결정론 엔진,
언어 구현, 한국어 가독성, 셈그림 UX, 교육 효과, AI 안전성, 창작자 가지 생태계,
사업성·시장 검증의 9축으로 한다. 문서·체커와 제품 행동을 분리하고 K0~K7·함수 타입,
원문 frontdoor parity, 재현·성능·LTS, 대표 5세계, 접근성·복구, 외부 사용자 실증,
replay-safe AI, 신뢰 가능한 가지곳간을 증거로 닫는다. 물리 차시 wedge와 모르는 사용자
10명의 창작·공유 성공을 우선한다.

## 중간 산출물 검토 순환

1. 주 세션이 대상 범위, authoritative files, snapshot/hash, DoD, 쓰기 소유권을 고정한다.
2. 구현 세션과 검증 세션을 겹치지 않는 경로로 분리한다.
3. 소규모 slice는 독립 Codex 세션 1회 이상 검토한다.
4. 주요 milestone/release 후보는 Claude, Gemini, 독립 Codex가 같은 bundle로 blind review한다.
5. 지적을 `수용 / 기각 / 보류 / ERQ`로 처분하고 근거를 남긴다.
6. 수용 지적을 반영한 뒤 제품 경로와 회귀를 다시 검증한다.
7. 검토 횟수가 아니라 실제 제품 행동과 외부 사용자 결과로 닫힘을 판정한다.

## 확인이 필요한 것

| 질문 | 관련 모듈 | 필요 근거 | 확인 담당 | 상태 |
|---|---|---|---|---|
| 활성 goal 객체의 옛 `사업화 제외` 문구를 제품 UI에서 새 목표로 교체할 수 있는가 | goal orchestration | 사용자 또는 제품의 goal replace/resume 기능 | 사용자/제품 | Open |
| 미성년 학생 pilot의 동의·개인정보·보관 정책은 무엇인가 | 교육 실증 | pilot protocol과 보호자/기관 승인 | 사용자/교사 검토 | Open |
| 사업성 10점의 구매·유료 pilot 또는 동등 조달 신호 기준은 무엇인가 | 시장 검증 | 외부 기관·교사·창작자 evidence | 사용자/외부 검토 | Open |

## 다음 세션에 이어받을 것

- 새 구현 전에 현재 대규모 dirty worktree를 기능군별로 감사하고 파일 쓰기 소유권을 봉인한다.
- K0~K7·함수 타입 OPEN과 현재 full gate 실패를 내부 구현 최우선으로 유지한다.
- 첫 외부 wedge는 설치 없는 물리 차시와 창작·공유 성공으로 둔다.
- 중간 milestone마다 동일 Web AI context bundle을 Claude와 Gemini에 제공한다.

## 생성/수정 파일

| 파일 | 목적 | 후속 처리 |
|---|---|---|
| `GEMINI.md` | Gemini current SSOT/public spec 포인터 및 독립 검토 경계 교정 | Claude/Codex 지침과 주기적 parity 확인 |
| `work/_templates/WEB_AI_CONTEXT_BUNDLE.template.md` | 동일 snapshot/hash·DoD 기반 외부 AI 검토 입력 추가 | 첫 milestone 검토 때 실제 bundle 생성 |
| `work/_session_deltas/20260717_codex_goal_expansion_business_readability_collaboration.md` | 확장 목표와 협업 운영 인수인계 | 후속 세션이 상태·검증 결과 갱신 |

## 검증

| 명령/확인 | 결과 | 비고 |
|---|---|---|
| `Get-Command claude`, `Get-Command gemini` | PASS | 로컬 실행 경로 존재 확인 |
| `GEMINI.md` current pointer 확인 | PASS | v24.15.1 / v0.2.1 기준 |
| Web AI context bundle current pointer 확인 | PASS | v24.15.1 / v0.2.1 기준 |
| `docs/ssot/**` 변경 여부 | 변경 없음 | SSOT 직접 수정 금지 준수 |

## SSOT 병합 메모

- 주 모듈: 없음. 이번 변경은 목표·협업 운영층이다.
- 포인터 반영: `GEMINI.md`, Web AI context bundle만 current로 교정했다.
- 병합 시 주의: 사업성·가독성 평가 결과가 언어 의미 변경을 요구하면 proposal과 사용자 승인을 먼저 거친다.
