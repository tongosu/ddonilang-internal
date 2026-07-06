# SESSION_DELTA

- 작성일: 2026-07-06
- 작성 주체: Codex
- 세션명: ai_collab_bootstrap
- 관련 SSOT: `docs/ssot/ssot/*_v24.12.9.md`, `docs/ssot/age/**`, `docs/ssot/walks/**`

## 결정된 것

| 상태 | 관련 모듈 | 내용 | 근거/파일 |
|---|---|---|---|
| Reflected | AI 협업 | 이 프로젝트에는 새 루트 `ssot/`를 만들지 않고 기존 `docs/ssot/**`를 정본으로 유지한다. | `AGENT_WORKFLOW.md` |
| Reflected | SSOT 경계 | `docs/ssot/**`는 읽기 전용이며, 변경 필요 시 `docs/context/proposals/`로 라우팅한다. | `AGENT_WORKFLOW.md`, `AGENTS.md`, `CLAUDE.md` |
| Reflected | SSOT 운영 | SSOT 권위 순서, 직접 수정 금지, 닫힘 주장 등급(`docs_first/runner_fill/golden_closed`)을 전용 정책으로 분리했다. | `SSOT_POLICY.md` |
| Reflected | session_delta | AI handoff 큐는 `work/_session_deltas/`로 둔다. | `work/_session_deltas/README.md` |
| Reflected | ERQ | 근거 없는 주장과 외부 AI 제안은 `work/erq/ERQ_QUEUE.md`에서 보류한다. | `work/erq/README.md`, `work/erq/ERQ_QUEUE.md` |
| Reflected | artifact policy | 로컬 산출물은 외부 `build/out` 경로를 우선하고, 공개 문서는 `publish/`, 릴리스 바이너리는 GitHub Releases 대상으로 분리한다. | `ARTIFACT_POLICY.md` |
| Reflected | web-only AI | 폴더 접근 없는 AI는 `WEB_AI_CONTEXT_BUNDLE`을 받아 Proposal만 반환한다. | `work/_templates/WEB_AI_CONTEXT_BUNDLE.template.md` |

## 확인이 필요한 것

| 질문 | 관련 모듈 | 필요 근거 | 확인 담당 | 상태 |
|---|---|---|---|---|
| 새 AI 협업 운영 체계를 향후 SSOT 운영 규칙으로 승격할지 여부 | 협업/정본 운영 | 사용자 승인 또는 SSOT 관리자 반영 제안 | 사용자 | Open |
| 루트 `PROJECT_SELF_BOOTSTRAP_PROMPT.md`의 의도된 위치/원본 확인 | 협업/부트스트랩 | 파일 제공 또는 사용자 확인 | 사용자 | Open |

## 다음 세션에 이어받을 것

- 새 AI가 들어오면 `AGENT_WORKFLOW.md`와 자기 도구별 지침을 먼저 읽게 한다.
- SSOT 관련 판단은 `SSOT_POLICY.md`의 권위 순서와 닫힘 주장 등급을 먼저 적용한다.
- 웹 전용 AI 검토가 필요하면 `work/_templates/WEB_AI_CONTEXT_BUNDLE.template.md`를 복사해 필요한 발췌만 채운다.
- SSOT 운영 규칙으로 공식 승격하려면 `docs/context/proposals/`에 별도 제안서를 작성한다.

## 생성/수정 파일

| 파일 | 목적 | 후속 처리 |
|---|---|---|
| `AGENT_WORKFLOW.md` | 공통 AI 협업 규칙 | 신규 AI 진입점 |
| `SSOT_POLICY.md` | SSOT 운영 경계와 닫힘 주장 등급 | SSOT 변경 판단 시 참조 |
| `AI_COLLABORATION_PLAYBOOK.md` | 역할/흐름 상세 | 필요 시 갱신 |
| `ARTIFACT_POLICY.md` | 산출물 정책 | 작업 시 참조 |
| `GEMINI.md` | Gemini 전용 지침 | Gemini 검토 시 사용 |
| `work/_session_deltas/**` | session delta 큐 | 지속 사용 |
| `work/erq/**` | ERQ 큐 | 지속 사용 |
| `work/_templates/**` | 템플릿 | 복사해 사용 |
| `_inbox/README.md`, `inputs/README.md`, `_archive/README.md` | 입력/사본/보관 경계 | 지속 사용 |

## 검증

| 명령/확인 | 결과 | 비고 |
|---|---|---|
| `git status --short` | 확인 | 기존 미추적 `또니랑/`은 사용자 변경으로 보존 |
| `Get-ChildItem -Recurse -Filter PROJECT_SELF_BOOTSTRAP_PROMPT.md` | NO_MATCH | 루트 prompt 파일 부재를 ERQ에 기록 |
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` 읽기 | 확인 | 기존 문서 역할 보존, 포인터 보강만 수행 |
| `.github/workflows/seamgrim-ci.yml`, `.github/branch-protection/main.required_checks.json` 읽기 | 확인 | CI/branch protection 구조 변경 없음 |
| `work/_session_deltas`, `work/erq`, `work/_templates`, `_inbox`, `inputs`, `_archive` 읽기 | 확인 | 기존 초안 구조 보존 후 SSOT policy만 보강 |
| `docs/ssot/**` 수정 여부 | PASS | 수정하지 않음 |

## SSOT 병합 메모

- 주 모듈: 협업/정본 운영
- 포인터 반영: 필요 시 `docs/context/proposals/`에 승격 제안 작성
- 병합 시 주의: 이 세션의 협업 파일 추가는 SSOT runtime landed claim이 아니며, 프로젝트 운영 보조 문서다.
