# 20260709 Codex Decision Closure Batch D2

## 결과 요약

- D0: 진행 중. `codex/queue-20260706`에서 시작 상태와 경계를 기록한다.
- D1 Settings keyset: 미착수.
- D2 NuriGym step_record v0.2 public schema: 미착수.
- D3 Report: 미착수.

## 경계

- 브랜치: `codex/queue-20260706`.
- `main` 직접 커밋 금지.
- `docs/ssot/**` 직접 수정 금지.
- parser 문법 변경 금지.
- runtime `state_hash` 산식 변경 금지.
- 기본 NuriGym v0.1 output/golden 유지. v0.2 wire는 opt-in으로만 추가한다.
- 기존 untracked 참고 파일은 커밋하지 않는다.

## 시작 상태

- `git branch --show-current`: `codex/queue-20260706`.
- `git status --short`: 추적 변경 없음, 기존 untracked 참고 파일만 존재.
- `git status --short -- docs/ssot`: 변경 없음.
- 최근 기준 커밋: `2f40a0f [DC-D1-REPORT] record decision closure d1 results`.

## 결정 가정

1. `설정.누리` key set은 현재 증빙 기준 `시앗`, `시앗묶음`으로 고정한다.
2. `설정.이야기` key set은 `들머리`만 result-affecting으로 고정한다.
3. `설정.셈 { 적분: ... }`는 이번 keyset에 포함하지 않고 현황 기록만 한다.
4. NuriGym `step_record_version="v0.2"`는 opt-in public schema로 시작하며 default v0.1 출력은 변경하지 않는다.
5. v0.2 `done`은 `terminated || truncated`와 같아야 한다.

## 검증 로그

- D0 시작: `git status --short -- docs/ssot` PASS.
