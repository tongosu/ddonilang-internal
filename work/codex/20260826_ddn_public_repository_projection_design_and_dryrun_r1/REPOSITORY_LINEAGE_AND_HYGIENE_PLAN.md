# Repository lineage and hygiene plan

## 원칙

정리는 삭제가 아니라 custody 분류부터 시작한다. 현재 폴더를 통째로 옮기거나 shared root를 clean/reset/stash하지 않는다.

## 순서

### R1 — 현재 단계

- read-only/inventory
- clean commit 기반 projection prototype
- dry-run A/B identity
- public self-contained gap 검출

### R2 — checkpoint rationalization

- active/implemented-review/closed/unknown worktree inventory
- 최신 프로그램별 fixed HEAD 및 review/closure 결속
- dirty worktree owner에게 checkpoint 또는 disposition 요청
- release feature set과 integration baseline owner 결정

### R3 — public-source readiness corrections

- test-only private fixture dependency 제거
- public-safe config/path fallback
- 최소 public conformance dependency closure
- public facade/license/security/support 문서
- public CI

### R4 — sealed projection and review

- clean integration commit에서 A/B projection
- fresh initialized repository build/test/WASM/examples/SPEC-link 검증
- independent fixed-tree review
- 공개 source tree와 release artifact receipt 봉인

### R5 — GitHub operation

- 기존 저장소 private 여부 확인·변경
- 새 public repository 생성
- 공개 tree만 push
- protection/CI/release 설정

R5는 별도 network/visibility authorization 전에는 시작하지 않는다.

## archive 정책

- 삭제 대신 먼저 `ARCHIVE_CANDIDATE`만 부여
- owner, fixed HEAD, closure/review, last unique commit, recovery route를 기록
- branch/worktree 삭제는 별도 승인과 recovery evidence 뒤 수행
- history rewrite는 기본 금지

## backup 상태

현재 local Git common database와 origin URL은 확인됐지만, whole-project backup과 restore drill은 이 R1에서 완료하지 않았다. GitHub visibility를 바꾸기 전에 remote state 확인, Git bundle/offsite backup, restore test를 별도 gate로 둔다.
