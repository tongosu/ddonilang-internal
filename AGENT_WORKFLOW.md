# AGENT_WORKFLOW.md

> 목적: Codex, Claude, Gemini, 웹 전용 AI가 같은 프로젝트에서 작업할 때 공유할 최소 운영 규칙.
> 이 문서는 기존 `AGENTS.md`, `CLAUDE.md`, `docs/ssot/**` 구조를 대체하지 않는다.

## 우선순위

충돌 시 아래 순서로 따른다.

1. `docs/ssot/ssot/*_v24.17.0.md` (live current, 사용자 최종 승인 2026-07-24, docs-first 제품 경계 유지)
2. `docs/ssot/walks/gogae#/` 및 `docs/ssot/age/AGE#/`
3. `AGENTS.md`, `CLAUDE.md`, 각 도구별 시스템 지침
4. 이 파일, `SSOT_POLICY.md`, `AI_COLLABORATION_PLAYBOOK.md`
5. `work/_session_deltas/**`, `work/erq/**`의 임시 큐

`docs/ssot/**`는 SSOT 관리자 영역이다. 에이전트는 읽기만 하고 직접 수정하지 않는다.

## 프로젝트 구조 보존 원칙

이 저장소는 코드 저장소이며 새 루트 `ssot/`를 만들지 않는다. 정본은 기존 위치를 유지한다.

| 경로 | 역할 | AI 수정 |
|---|---|---|
| `core/`, `lang/`, `tool/`, `tools/teul-cli/` | 제품 구현 경로 | 요청 범위 안에서 가능 |
| `pack/`, `tests/` | 실행 가능한 근거와 회귀 검증 | 요청 범위 안에서 가능 |
| `solutions/`, `gaji/` | 제품선/가지/샘플 구현 | 요청 범위 안에서 가능 |
| `docs/ssot/**` | SSOT 정본/준정본/pack/walk/age | 직접 수정 금지 |
| `docs/context/proposals/` | SSOT/설계 변경 제안 | 가능 |
| `docs/context/reports/` | legacy 보고서 redirect/색인 | 새 완료 보고서 추가 금지 |
| `docs/reports/audit/` | 완료된 검토·정합·위험 감사 | 가능 |
| `docs/reports/impl/` | 완료된 구현·검증 근거 | 가능 |
| `docs/reports/rationalization/` | 완료된 구조 합리화 보고 | 가능 |
| `docs/context/all/DEV_SUMMARY.md` | 최신 개발 운영 요약 | 작업 완료 시 갱신 |
| `docs/status/` | 상태/변경 기록 | 큰 변경 시 갱신 |
| `work/_session_deltas/` | AI 간 세션 델타 큐 | 가능 |
| `work/erq/` | 근거 필요 질문 큐 | 가능 |
| `_inbox/` | 원본 투입구, 직접 편집 금지 | 원본 보관만 |
| `inputs/` | 작업용 사본 | 가능 |
| `_archive/` | 삭제 대신 보관 | 승인/계획 후 |

`docs/` 전체는 미출시 내부 문서를 공개 저장소에 올리지 않기 위해 Git에서 제외한다.
이 제외는 권위나 수명주기를 뜻하지 않는다. 내부 문서도 source registry와 위 경계를 따른다.

작업 지시 경계:

- `docs/context/queue/`: 승인 전 대기.
- `docs/context/briefs/`: 사용자 승인 후 실행 계약.
- `docs/context/codex_tasks/`, `docs/context/tasks/`: legacy/history. 신규 작업의 기본 집으로 쓰지 않는다.
- 활성 작업은 generated active view에서 최대 2건만 노출한다.

## 세션 시작 체크

폴더 접근 가능한 AI는 작업 전 아래를 확인한다.

1. `git status --short`
2. `AGENTS.md`
3. 자기 도구 지침: `CLAUDE.md`, `GEMINI.md`, 또는 Codex 시스템 지침
4. 이 파일
5. `SSOT_POLICY.md`
6. `docs/context/all/DEV_SUMMARY.md`
7. `docs/ssot/ssot/SSOT_INDEX_v24.17.0.md`
8. 작업과 관련된 SSOT/AGE/WALK 문서

빌드와 로컬 산출물은 `I:/home/urihanl/ddn/codex/build` 및 `I:/home/urihanl/ddn/codex/out`을 우선 사용한다. 없으면 `C:/ddn/codex/build`, `C:/ddn/codex/out`을 사용한다.

## North Star / wedge 체크

기술 작업을 시작하기 전에 아래 운영 질문을 한 번 확인한다.

```text
이 작업은 2026년 안에 우리가 모르는 사람 10명이 셈그림 물리 시뮬레이션을 만들고 공유하는 데 가까워지는가?
```

현재 wedge는 **셈그림 물리 차시**다. 7목적 전체가 중요하더라도, 실행 우선순위는 첫 외부 사용자가 성공하는 흐름을 앞에 둔다.

우선순위 기본값:

1. 설치 없이 눌러보기 / WASM / 브라우저 첫 실행.
2. 90초 데모와 랜딩 페이지.
3. 셈그림 물리 차시 예제와 진단 품질.
4. 안정/실험 라벨.
5. 그 밖의 7목적 확장.

이 순서를 바꾸는 작업은 세션 델타에 이유를 남긴다.

## WIP 한도

새 proposal, 새 OI, 새 목표 지시서를 만들기 전에 현재 누적량을 확인한다.

- 미병합 proposal 10건 초과: 신규 설계 금지, 병합/기각/아카이브 우선.
- 새 OI 생성: 같은 세션 또는 같은 주에 닫을 OI/보류 사유를 같이 기록.
- 활성 목표 지시서 2건 초과: 새 지시서보다 기존 지시서 상태 정리 우선.
- 실행 산출물 없이 전략 문서만 추가하는 작업은 한 번 더 사용자 의도를 확인한다.

## 폴더 네이티브 AI

아래 환경은 프로젝트 폴더를 직접 읽고 쓸 수 있으면 같은 규칙을 따른다.

| 환경 | 시작 지침 | 세션 델타 |
|---|---|---|
| Codex Windows app | `AGENTS.md`, 이 파일 | `work/_session_deltas/YYYYMMDD_codex_<session>.md` |
| Codex VS Code/plugin | `AGENTS.md`, 이 파일 | `work/_session_deltas/YYYYMMDD_codex_<session>.md` |
| Claude Windows/Desktop app | `CLAUDE.md`, 이 파일 | `work/_session_deltas/YYYYMMDD_claude_<session>.md` |
| Claude VS Code/plugin | `CLAUDE.md`, 이 파일 | `work/_session_deltas/YYYYMMDD_claude_<session>.md` |
| Gemini folder-native | `GEMINI.md`, 이 파일 | `work/_session_deltas/YYYYMMDD_gemini_<session>.md` |

## Session Delta 규칙

중요한 결정, 미완료 작업, 검증 결과, SSOT 반영 후보는 대화에만 두지 않고 세션 델타에 남긴다.

위치:

```text
work/_session_deltas/YYYYMMDD_agent_session-name.md
```

상태값:

- `Pending`: SSOT/문서/코드 반영 여부를 검토해야 함
- `Reflected`: 이미 문서/코드/운영 규칙에 반영됨
- `Rejected`: 반영하지 않기로 결정됨

세션 델타는 정본이 아니다. Codex/사용자가 검토해 `docs/context/proposals/`, `docs/context/all/DEV_SUMMARY.md`, 구현 파일, 또는 SSOT 관리자 절차로 승격한다.

## ERQ 규칙

ERQ는 Evidence Required Queue다. 아래 항목은 근거 없이 SSOT나 완료 주장으로 올리지 않는다.

- 수치, 가격, 일정, 정책
- 고객 약속, 공개 배포 약속
- 규제/컴플라이언스 주장
- "runtime landed", "닫힘-동작", "CLOSED" 주장
- 외부 AI가 만든 사실 주장

위치:

```text
work/erq/ERQ_QUEUE.md
work/_templates/ERQ_ITEM_TEMPLATE.md
```

ERQ 항목은 근거 파일, 검증 명령, 사용자 확인, 또는 SSOT 관리자 반영이 생기기 전까지 `Open` 상태로 둔다.

## SSOT 라우팅

세부 운영 규칙은 `SSOT_POLICY.md`를 따른다.

SSOT 직접 수정은 금지한다. 변경이 필요하면 아래로 라우팅한다.

| 필요 | 위치 |
|---|---|
| SSOT 변경 제안 | `docs/context/proposals/PROPOSAL_<topic>_V<N>_YYYYMMDD.md` |
| 영향표/근거 메모 | 작업 중 `work/<agent>/`, 완료 후 `docs/reports/audit/` |
| 실행 근거 | `pack/`, `tests/`, 완료 후 `docs/reports/impl/` |
| 최신 운영 요약 | `docs/context/all/DEV_SUMMARY.md` |
| AI handoff | `work/_session_deltas/` |

신규 문법/런타임 기능은 제품 경로(`lang`/`tool`/`tools/teul-cli`/WASM frontdoor)에 들어가기 전까지 구현 완료로 주장하지 않는다.

## Web-only AI

폴더 접근이 없는 AI에는 전체 저장소를 기대하지 않는다. `work/_templates/WEB_AI_CONTEXT_BUNDLE.template.md`를 복사해 필요한 발췌만 제공한다.

웹 AI의 답변은 항상 Proposal이다. 정본으로 승격하려면 Codex/사용자가 근거를 확인하고 세션 델타, ERQ, 제안서, 구현 파일 중 적절한 위치에 병합한다.

## Artifact Policy

세부 규칙은 `ARTIFACT_POLICY.md`를 따른다. 요약은 다음과 같다.

- `build/`와 `out/`은 배포 대상 정본이 아니다.
- 로컬 산출물은 외부 경로 `I:/home/urihanl/ddn/codex/{build,out}`를 우선한다.
- 공개 문서는 `publish/`에 별도 정리한다.
- 사용자 공개 바이너리는 저장소가 아니라 GitHub Releases 대상이다.
- 원본은 `_inbox/`에 두고, 작업은 `inputs/` 또는 `work/<agent>/` 사본으로 한다.

## 완료 주장

완료 주장은 근거와 함께 한다.

- `닫힘-문서`: manifest/checker/문서 추가만 포함
- `닫힘-동작`: 실제 제품 행동 변경과 검증 포함

마루 2 이상 UI/제품 행동은 runner, Playwright/browser smoke, 또는 실제 브라우저 확인 기록 없이 `닫힘-동작`으로 주장하지 않는다.

## 파일 이동과 삭제

대량 이동 전에는 이동 계획을 먼저 만든다.

필수 기록:

- source path
- target path
- reason
- sha256
- 실행 전/후 확인

불확실한 파일은 삭제하지 않고 `_archive/`로 보낸다. 파괴적 명령은 사용자 승인 없이는 실행하지 않는다.
