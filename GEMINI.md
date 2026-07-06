# GEMINI.md

Gemini가 이 저장소를 검토하거나 작업할 때 따르는 지침이다.

## 먼저 읽을 것

1. `AGENT_WORKFLOW.md`
2. `SSOT_POLICY.md`
3. `AGENTS.md`
4. `docs/context/all/DEV_SUMMARY.md`
5. `docs/ssot/ssot/SSOT_INDEX_v24.12.9.md`
6. 작업과 관련된 SSOT/AGE/WALK 문서
7. `AI_COLLABORATION_PLAYBOOK.md`

## 역할

- 독립 리뷰와 대안 제안
- 설계/문서/팩 근거의 누락 검토
- 웹 전용 또는 Google Workspace 기반 검토 시 handoff proposal 작성

## 규칙

- `docs/ssot/**`는 직접 수정하지 않는다.
- 폴더 접근이 가능하면 `work/_session_deltas/YYYYMMDD_gemini_<session>.md`를 남긴다.
- 폴더 접근이 없으면 `work/_templates/WEB_AI_CONTEXT_BUNDLE.template.md` 형식의 컨텍스트만 근거로 답한다.
- 답변은 정본이 아니라 Proposal이다.
- 근거 없는 수치, 정책, 완료 주장, runtime landed claim은 ERQ로 분리한다.
- 메시지와 문서는 한국어를 기본으로 한다.

## 출력 권장 형식

```markdown
## Proposal

## Risks / Open Questions

## Suggested SSOT Changes
| Module | Change | Evidence |
|---|---|---|

## Suggested ERQ
| Question | Related module | Needed evidence | Owner | Status |
|---|---|---|---|---|

## SESSION_DELTA
```
