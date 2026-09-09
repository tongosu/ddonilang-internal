# 2026-08-29 DDN V1 P1-A FU01 evidence correction handoff

## 역할

- EXECUTOR / FILE_OWNER: DDN V1제품마감Codex
- execution thread: `01a04a01-b812-7840-a2a3-33208dd36e36`
- manager: Codex관리Work `01a00f98-da37-7b62-9b9a-cd2533075f1c`
- predecessor reviewer: `01a04a9e-5fae-7940-ba5d-df5c7cca1f70`

## lineage

- review parent: `b65463cc8f6f981e290000ffb4e14e1db6699fad`
- correction fixed: `25a271bfab45ef5c0b5f9abb67d6323547e1f5b4`
- fixed tree: `3644bfb81f41c0226d395c26188cb87eb93b91c3`
- fixed diff: fault-injection runner 한 파일
- merge count: 0

## correction

- 기존 전면 PreV25 치환을 `PREV25_PATH_SUBSTITUTION`으로 개명했다.
- 실제 `.or_else(...)` fallback을 `HIDDEN_PREV25_RETRY`로 추가했다.
- `PROFILE_IDENTITY_DISABLED`, `RECURSION_GUARD_BYPASS`를 유지했다.
- 네 축 모두 예상 test signature가 있는 RED를 요구한다.
- 각 RED 뒤 source bytes exact restore, SHA-256 확인, focused GREEN을 수행한다.

## evidence

- runner: 4,339 bytes / `68efdc3a831819f076cf1f5d3e18f64d26c21f5146e068078d62ee6ad054e33c`
- execution runtime restore: CRLF 28,913 / `f8752ac4a2841eebfc4cd15c0d7ec461d7c7273851e7139a6e8aa1c894b00cbc`
- mutation RED exits: 101 / 101 / 101 / 3221225725
- 각 mutation restore 뒤 focused 6/6 GREEN
- 최종 focused 6/6, native/WASM 1/1, tracked-WASM 8/8
- lib 523/523, freshness PASS, diff-check PASS
- 제품 source/WASM/SSOT/SPEC/visible UI diff 0

## custody

- 기존 branch/worktree/lease 재사용
- 새 branch/worktree/writer 0
- server/port/browser/protected process mutation 0
- cargo/rustc/python residue 0
- 기존 task-owned untracked preflight 문서 미stage·보존

## status

```text
P1A_FU01_EVIDENCE_CORRECTION_IMPLEMENTED_UNDER_REREVIEW
P1A_CLOSURE_NOT_ISSUED
```

targeted independent rereview는 handoff commit을 parent로, `25a271bf...`를 fixed
product/test target으로 사용해야 한다. plain PASS, P1-A closure, membership,
readiness, release, activation, Human PASS는 미주장이다.
