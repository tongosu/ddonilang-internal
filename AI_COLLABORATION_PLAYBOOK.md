# AI_COLLABORATION_PLAYBOOK.md

> 또니랑/셈그림 저장소용 멀티 AI 협업 운영 가이드.
> 공통 규칙은 `AGENT_WORKFLOW.md`와 `SSOT_POLICY.md`가 우선하고, 이 문서는 실행 방법을 보완한다.

## 핵심 원칙

AI의 대화 기억은 공유되지 않는다. 공유 기억은 파일이다.

이 프로젝트에서 공유 기억은 세 층으로 나눈다.

| 층 | 위치 | 의미 |
|---|---|---|
| 정본 | `docs/ssot/**` | SSOT 관리자 영역. 에이전트 직접 수정 금지 |
| 개발 운영 | `docs/context/**`, `docs/reports/**`, `docs/status/**` | 제안, 보고, 최신 운영 요약 |
| 세션 큐 | `work/_session_deltas/**`, `work/erq/**` | AI 간 handoff와 근거 대기열 |

## 역할 분담

| 역할 | 권장 담당 |
|---|---|
| 코드 구현, 파일 정리, 검증 실행, 델타 병합 | Codex |
| 설계 검토, 문서 초안, 위험 식별, 사용자 대화 정리 | Claude |
| 독립 리뷰, 대안 제안, 웹/Drive 기반 검토 | Gemini |
| 최종 승인, SSOT 반영, 공개 배포 결정 | 사용자 |

역할은 고정 권한이 아니다. 어떤 AI가 작업하든 `AGENT_WORKFLOW.md`와 기존 지침을 따른다.

SSOT 관련 판단은 `SSOT_POLICY.md`의 권위 순서와 닫힘 주장 등급을 따른다.

## 세션 델타 흐름

1. 세션 중 중요한 결정이 생기면 `work/_session_deltas/YYYYMMDD_agent_<session>.md`에 기록한다.
2. 미검증 주장이나 외부 AI 제안은 ERQ에도 올린다.
3. 다음 에이전트는 세션 시작 시 `_session_deltas`의 미병합 항목을 확인한다.
4. 반영이 끝난 항목은 `Reflected`로 바꾼다.
5. 장기 보관이 필요한 완료 델타는 `work/_session_deltas/_merged/`로 옮긴다.

## ERQ 흐름

ERQ는 "정본에 올리기 전 근거가 필요한 주장"을 보류하는 큐다.

예:

- "이 기능은 100% 닫혔다"
- "이 정책은 SSOT에 반영됐다"
- "이 외부 검토가 현재 기준이다"
- "릴리스 준비가 끝났다"

근거가 생기면 `work/erq/ERQ_QUEUE.md`에서 상태를 `Resolved`로 바꾸고, 근거 경로와 검증 명령을 남긴다.

## SSOT 변경 제안

SSOT를 바꿔야 하면 `docs/ssot/**`를 직접 수정하지 않는다.

제안서 기본 위치:

```text
docs/context/proposals/PROPOSAL_<topic>_V<N>_YYYYMMDD.md
```

제안서에는 최소한 아래를 넣는다.

- 변경 분류: `DOCS_ONLY`, `SSOT_RULE`, `SSOT_TERM`, `PACK`, `ENGINE`, `TOOLING`
- 대상 경로
- 이유
- DoD
- 검증 pack 또는 검증 명령
- 범위 밖/이월

## 웹 전용 AI 핸드오프

웹 전용 AI에는 필요한 발췌만 준다.

1. `work/_templates/WEB_AI_CONTEXT_BUNDLE.template.md`를 복사한다.
2. 관련 SSOT 발췌, 현재 세션 델타, ERQ 발췌, 요청 작업을 채운다.
3. 웹 AI 답변은 Proposal로 받는다.
4. Codex/사용자가 근거를 검토한 뒤 세션 델타나 제안서로 병합한다.

웹 AI가 만든 새 사실은 바로 SSOT나 완료 주장으로 쓰지 않는다.

## 협업 품질 기준

- 기존 구조와 파일 역할을 먼저 따른다.
- 새 폴더를 만들기 전에 기존 폴더 역할로 충분한지 확인한다.
- `docs/ssot/**` 수정 필요가 보이면 중단하고 제안서로 전환한다.
- 테스트 전용 변환기나 harness-only lowering으로 언어/런타임 완료를 주장하지 않는다.
- `닫힘-동작`은 실제 제품 경로와 검증 기록이 있을 때만 쓴다.
