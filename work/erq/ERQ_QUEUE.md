# ERQ_QUEUE

> Evidence Required Queue. 근거 확인 전 주장을 보류하는 비정본 큐다.

| ID | 상태 | 질문/주장 | 관련 모듈 | 필요 근거 | 담당 | 기록일 |
|---|---|---|---|---|---|---|
| ERQ-20260706-001 | Resolved | 새 AI 협업 운영 체계를 향후 SSOT 운영 규칙으로 승격할지 여부 | 협업/정본 운영 | 사용자 승인 또는 SSOT 관리자 반영 제안 | 사용자 | 2026-07-06 |
| ERQ-20260706-002 | Resolved | 루트 `PROJECT_SELF_BOOTSTRAP_PROMPT.md`가 현재 워킹트리에 없음. 사용자가 의도한 prompt 원본/위치 확인 필요 | 협업/부트스트랩 | 파일 제공, 경로 정정, 또는 현재 산출물 기준 진행 승인 | 사용자 | 2026-07-06 |

## 상태값

- `Open`: 근거 또는 결정 대기
- `Resolved`: 근거 확인 또는 사용자 결정 완료
- `Rejected`: 반영하지 않기로 결정

## 해결 내역 (2026-07-06)

**ERQ-20260706-001 — 사용자 결정:**
- 이번 AI 협업 운영 체계는 **당장 실무 운영 규칙으로 채택**한다.
- 다만 `docs/ssot/**` 정식 SSOT 본문으로 **즉시 승격하지는 않는다**.
- 먼저 `AGENT_WORKFLOW.md` / `ARTIFACT_POLICY.md` / `work/_session_deltas` / `work/erq` 체계로 운영하고, 충분히 안정되면 `docs/context/proposals/`에 SSOT 승격 제안서를 별도로 만든다.

**ERQ-20260706-002 — 사용자 결정:**
- `PROJECT_SELF_BOOTSTRAP_PROMPT.md`의 원본 위치는 `I:\dev\template\PROJECT_SELF_BOOTSTRAP_PROMPT.md`이다.
- 이번 작업의 목적은 이 파일을 **읽고 참조**하는 것이었고, 루트에 반드시 복사해야 한다는 뜻은 아니었다.
- 다른 AI가 재사용하기 쉽도록 repo-local 사본을 `work/_templates/PROJECT_SELF_BOOTSTRAP_PROMPT.md`에 추가했다(2026-07-06, Claude Code 세션).
