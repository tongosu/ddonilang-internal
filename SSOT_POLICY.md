# SSOT_POLICY.md

> 또니랑/셈그림 저장소의 SSOT 운영 경계와 변경 라우팅 정책.
> 이 문서는 `docs/ssot/**` 정본을 대체하지 않는다. 에이전트가 정본을 안전하게 읽고, 변경 필요를 제안으로 넘기는 운영 규칙이다.

## 권위 순서

충돌 시 아래 순서로 판단한다.

1. `docs/ssot/ssot/*_v24.17.1.md` (live current, 사용자 최종 승인 2026-07-26, docs-first 제품 경계 유지)
2. `docs/ssot/walks/gogae#/` 및 `docs/ssot/age/age#/`
3. `AGENTS.md`, `CLAUDE.md`, 도구별 시스템 지침
4. `AGENT_WORKFLOW.md`, 이 파일, `AI_COLLABORATION_PLAYBOOK.md`
5. `work/_session_deltas/**`, `work/erq/**`

`work/**`와 `docs/context/**`는 운영/제안/보고 영역이다. SSOT 자체가 아니다.

## 직접 수정 금지

에이전트는 아래 경로를 직접 수정하지 않는다.

```text
docs/ssot/**
```

SSOT 본문, AGE 문서, WALK 문서, SSOT pack/samples/gaji 자료가 모두 포함된다. 변경이 필요하면 `docs/context/proposals/` 또는 완료된 감사 위치인 `docs/reports/audit/`로 우회한다.

## 변경 필요 시 라우팅

SSOT 변경이 필요하다고 판단되면 작업을 다음 중 하나로 분류한다.

| 분류 | 산출물 위치 | 설명 |
|---|---|---|
| 용어/규칙 변경 | `docs/context/proposals/PROPOSAL_<topic>_V<N>_YYYYMMDD.md` | 사용자 또는 SSOT 관리자가 반영할 제안 |
| 영향 조사 | 작업 중 `work/<agent>/`, 완료 후 `docs/reports/audit/` | 코드/팩/문서 영향 범위 감사 |
| 미확인 주장 | `work/erq/ERQ_QUEUE.md` | 근거 또는 사용자 결정 대기 |
| 세션 인수인계 | `work/_session_deltas/` | 다음 AI가 이어받을 결정/미완료/검증 |
| 실행 근거 | `pack/`, `tests/`, `docs/reports/impl/` | 제품 경로 검증 자료 |

제안서에는 최소한 아래를 포함한다.

- 대상 SSOT 파일/절
- 현재 문구 또는 현재 동작
- 제안 변경
- 이유
- 제품 영향
- 검증 명령 또는 필요한 pack
- 범위 밖
- 사용자 결정 필요 항목

## 닫힘 주장 등급

SSOT 운영에서는 "있다"와 "제품에서 닫혔다"를 구분한다.

| 등급 | 뜻 | 허용 주장 |
|---|---|---|
| `docs_first` | 문서/스켈레톤/의도만 있음 | 설계 또는 후보 |
| `runner_fill` | runner/checker가 있으나 closure claim은 보류 | 검증 중, 부분 증빙 |
| `golden_closed` | 제품 경로 + golden/checker PASS + 문서 상태 동기화 | 제한된 범위의 닫힘 |

`닫힘-동작`, `runtime landed`, `CLOSED`는 `golden_closed` 또는 그에 준하는 제품 경로 증빙 없이는 쓰지 않는다.

## 제품 경로 원칙

정식 언어/런타임 지원은 제품 경로에 있어야 한다.

허용 제품 경로:

- `lang/`
- `tool/`
- `tools/teul-cli/`
- WASM frontdoor / 제품 UI runtime

금지 완료 처리:

- 테스트 전용 Python/JS lowering
- harness-only 변환
- 문서/README만으로 runtime landed 주장
- pack skeleton만으로 제품 동작 닫힘 주장

## 충돌 처리

SSOT와 구현 또는 pack이 충돌하면 임의로 맞추지 않는다.

1. 실제 동작을 재현한다.
2. 파일:행 근거를 남긴다.
3. 어느 쪽이 더 권위 있는지 표시한다.
4. 수리가 필요한 경우 proposal 또는 brief로 분리한다.
5. session delta에 남긴다.

예:

```text
SSOT says: X
Product says: Y
Pack expects: Z
판정: drift
조치: docs/reports/audit/<...>.md + work/_session_deltas/<...>.md
```

## 외부 AI 답변

폴더 접근 없는 AI의 답변은 정본이 아니다.

- 답변 상태: Proposal
- 새 사실 주장: ERQ 등록
- 반영 후보: session delta 기록
- SSOT 반영: 사용자/SSOT 관리자 결정 후 진행

## 세션 종료 기록

SSOT 관련 작업을 한 세션은 `work/_session_deltas/`에 아래를 남긴다.

- 읽은 SSOT/문서
- 변경하지 않은 경계
- 제안/보고 산출물
- 검증 명령과 결과
- 미해결 ERQ
- 다음 세션이 이어받을 일
