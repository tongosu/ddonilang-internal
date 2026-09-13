# 2026-08-21 Codex session delta — execution/concurrency migration W1

## 결정

- root dirty를 건드리지 않고 verified G30 product head 계보에서 격리 worktree를 사용했다.
- typed delivery/cardinality/queue authority는 `lang/src/delivery.rs` 한 곳이 소유한다.
- 첫 vertical은 `<~ / ~>` async, exact-one route, FIFO/no-reentry, bounded WAIT hook로 제한했다.
- old `~~>`와 기존 fixed-point `<<-` corpus는 역사 증거로 보존했다.

## 구현

- product commit: `aaf72e08498031feeabfabc6692316e42dcfdc42`
- successor D-PACK: `pack/future_grammar_atlas_owner_closed_delta_r2/**`
- SSOT/public SPEC/UI/deployment/activation 변경 없음.

## 검증

- lang `342/342`
- tool `484/484`
- teul-cli `1,159/1,159`
- WASM compile PASS
- successor D-PACK `4/4`
- alrim dispatch selftest PASS
- 보호 PID `53196`, port `8787` 유지

## 미완료

- old `~~>` clean cut, ReactionProvider, sender filter, worker permutation, staged outbox,
  resumable WAIT, full frontdoor convergence, rendezvous, persistent dependency, 65-case oracle.
- historical pack failures의 fixed-parent 귀속 독립 재검토.
- 최신 dirty root 통합 전 authority drift 재감사 및 `DEV_SUMMARY`/협업 공유판 동기화.
