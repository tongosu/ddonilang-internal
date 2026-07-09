# 2026-07-10 Codex Ganada Verification Contract

## 목적

- 가나다 15줄기 x 6마루 구조 재검토 전에 `닫힘-동작` 검증 조건을 먼저 고정한다.
- 이번 배치는 상태 재판정이나 제품 구현이 아니라, 90칸 판정 기준을 기계적으로 검증하는 contract/checker를 만든다.

## 시작 상태

- branch: `codex/queue-20260706`
- tracked dirty files: none at start.
- existing untracked reference files are left uncommitted:
  - `work/_session_deltas/20260709_codex_recent_proposals_reflection.md`
  - `또니랑/*.md`

## 경계

- `docs/ssot/**` 직접 수정 금지.
- parser/runtime/UI/product behavior 변경 금지.
- 기존 90칸을 새로 닫힘 처리하지 않는다.
- `닫힘-동작`은 제품 경로 실행 증거와 재현 가능한 checker/pack 증거가 있을 때만 허용하는 contract로만 고정한다.

## 진행 로그

- G0: 시작 상태와 경계를 기록했다.
