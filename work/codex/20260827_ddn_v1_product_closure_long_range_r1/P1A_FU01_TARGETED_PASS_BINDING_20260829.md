# P1-A FU01 Targeted PASS Binding — 2026-08-29

## 허용 상태

```text
P1A_FU01_EVIDENCE_CORRECTION_CLOSED
P1A_FU01_INDEPENDENT_PLAIN_PASS_BOUND
```

이 결속은 fault-injection evidence correction FU01만 닫는다. P1-A 전체 closure,
P1 closure, V1 membership/readiness, public default ingress, release, activation,
Human PASS를 발급하지 않는다.

## 권위

- internal CURRENT: SSOT v25.19.0 / RD-001~461
- public Language SPEC CURRENT: v0.6.0
- `docs/ssot/**`, `publish/spec/**`: read-only / diff 0

## 선형 계보

- P1-A product semantics fixed: `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`
- P1-A product handoff: `151923c9d6a0708574416895c159ab21ffa87795`
- predecessor independent review: `b65463cc8f6f981e290000ffb4e14e1db6699fad`
- FU01 evidence fixed: `25a271bfab45ef5c0b5f9abb67d6323547e1f5b4`
- FU01 handoff: `9a5fca2fe6a8f1cad611a7998a23ecd3bcbb2300`
- FU01 independent PASS: `4a565c4ffc4a69281f5bb9b2c8a20e7b71214afb`
- FU01 PASS tree: `1d3d36ba90f1448901da09a1547085eeaa97074d`
- merge count: 0

모든 위 commit은 기재 순서의 direct-parent 선형 계보다.

## 독립검토 결속

- verdict: `PASS`
- scope: targeted evidence correction only
- review parent: `9a5fca2fe6a8f1cad611a7998a23ecd3bcbb2300`
- review commit: `4a565c4ffc4a69281f5bb9b2c8a20e7b71214afb`
- review diff: `REVIEW_RESULT.md` + reviewer session delta 정확히 2개
- report: 9,572 bytes
- report SHA-256:
  `56f63d6097eecdc5efe1b5d2413b578a2fd50aaee914007b80fcae85db66391c`
- product/test/pack/WASM/SSOT/SPEC/UI/lang/tools review diff: 0
- reviewer final: clean / staged 0 / untracked 0 / merge 0

## 닫힌 FU01 범위

- 기존 전면 PreV25 치환 mutation을 `PREV25_PATH_SUBSTITUTION`으로 정확히 개명
- 실제 V25 실패 뒤 `.or_else(...)` PreV25 fallback을
  `HIDDEN_PREV25_RETRY`로 추가
- `PROFILE_IDENTITY_DISABLED`, `RECURSION_GUARD_BYPASS` 유지
- 네 mutation 각각 예상 RED signature, exact restore, focused GREEN 검증
- final `P1A_MUTATION_PASS mutations=4`
- runner Git blob: 4,339 bytes / SHA-256
  `68efdc3a831819f076cf1f5d3e18f64d26c21f5146e068078d62ee6ad054e33c`

## 검증 결속

- mutation RED exits: 101 / 101 / 101 / 3221225725
- 각 mutation 뒤 focused native: 6/6 PASS
- native/WASM exact: 1/1 PASS
- tracked-WASM: 8/8 PASS
- deterministic repeats: 3 / partial summary leak: 0
- tool lib: 523/523 PASS
- official tracked WASM freshness: PASS
- source exact restore와 residue 0: PASS

첫 재실행의 공유 Cargo executable 잠금 `LNK1104`는 finally exact restore와 clean을
확인한 환경 사건이다. 잠금 해제 뒤 `CARGO_BUILD_JOBS=1` 전체 재실행이 네 축과 모든
회귀를 통과했으므로 correction 결함으로 분류하지 않는다.

## protected custody

- reviewer server/port/browser/protected process stop/restart/kill: 0
- baseline Node PID 10개 중 PID 60264가 검증 중 외부 수명주기로 종료된 사실 관찰
- reviewer가 종료 명령을 실행한 증거: 0
- persistent new Node: 0
- TCP 8787 listener: 0
- cargo/rustc/python/test residue: 0

## OPEN / NONCLAIMS

- P1-A 전체 closure: 미발급
- P1 전체 closure: 미발급
- Foundation-12: OPEN
- 실제 18/18 membership, 전체 4/4 execution contract, 9/9 exclusions: 미승격
- public executable/command membership과 stable profile spelling: OPEN
- Workbench default ingress와 visible UI behavior: OPEN
- whole P0/P1/V1 readiness, P2~P6/RC, release, activation, legal,
  Owner Human Smoke PASS, Human PASS, external-user success: OPEN

이 문서는 targeted PASS를 exact identity에 결속할 뿐, 더 넓은 제품·정본·릴리스
상태를 승격하지 않는다.
