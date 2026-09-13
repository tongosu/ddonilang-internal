# P1-A V1-Core Supported Ingress W1 — Independent Review Handoff

## 상태

- `P1A_V1_CORE_SUPPORTED_INGRESS_IMPLEMENTED_UNDER_REVIEW`
- 이 문서는 구현·검증 handoff이며 독립 PASS, V1 membership/readiness, release 또는 Human PASS가 아니다.

## 권위와 고정 계보

- internal authority: Owner-approved SSOT v25.19.0 / RD-001~461
- public language authority: Language SPEC v0.6.0
- P0 limited closure: `fe7c38c53cc3e1946b109b8002447983c185ba9b`
- P1-A FILE_OWNER lease: `0d9dd6091d8df0b697dee7c7cf6e8438b592d782`
- product/test fixed HEAD: `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`
- product/test fixed tree: `a0d46873734ad50a8e5d4a8dbb5f84f73c03f23a`
- product/test parent: `0d9dd6091d8df0b697dee7c7cf6e8438b592d782`
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- merge count: 0
- product/test commit path count: 16, 모두 승인된 P1-A lease 안

## 구현 범위

- shared supported-profile identity `v1-core-v25`를 `tool/src/ddn_runtime.rs`의 단일 resolver에 결속했다.
- VC01 Korean raw source, VC02 Definition `:=`, VC03 Binding/Rebinding `<-`를 typed V25 constructor로 처리한다.
- legacy definition `=`는 `E_V25_DEFINITION_MIGRATION_REQUIRED`로 fail closed한다.
- profile 누락은 `E_SOURCE_PROFILE_REQUIRED`, 미지원 identity는 `E_SOURCE_PROFILE_UNSUPPORTED`로 fail closed한다.
- direct/mutual named-call recursion은 결정적 `E_V1_CORE_RECURSION_UNSUPPORTED`로 거부한다.
- source analysis, native run summary, WASM run summary가 같은 resolver와 typed program 경로를 소비한다.
- run summary는 선택된 `source_profile_identity`를 명시한다.
- supported-profile 경로에는 PreV25 retry/fallback이 없고, 전역 557-lesson 기본 dialect 전환도 없다.
- 기존 explicit `strict` legacy analysis 및 기존 run entrypoint는 그대로 보존했다.
- parser/canon에 새 의미 권위를 만들지 않았고 teul private semantics 또는 test-only lowering을 추가하지 않았다.

`v1-core-v25`는 이 구현 slice의 검토 대상 identity다. public stable spelling, executable/command membership, installer alias는 이 handoff가 승인하거나 닫지 않는다.

## 제품·테스트 변경

- product Rust: `tool/src/ddn_runtime.rs`, `tool/src/runtime_surface.rs`, `tool/src/source_analysis.rs`, `tool/src/wasm_api.rs`
- tracked WASM: `.wasm`, `.js`, `.d.ts`, freshness manifest
- evidence pack: `pack/v1_core_supported_ingress_w1/**`
- regression/parity/mutation runners: `tests/run_v1_core_supported_ingress_*`
- `docs/ssot/**`, `publish/spec/**`, `lang/src/parser.rs`, `lang/src/lib.rs`, `tool/src/canon.rs`, `tool/src/main.rs`, visible Workbench UI는 변경 0

## RED-first 및 최종 검증

### 최초 행동 RED

구현 전 focused test 4/4 FAIL:

1. valid V25 `:=`/`<-`가 supported ingress에서 ACCEPTED가 아니었음
2. legacy `=`가 exact migration diagnostic으로 REJECTED되지 않았음
3. direct/mutual recursion이 deterministic explicit unsupported가 아니었음
4. profile 누락이 required error가 아니라 implicit strict 경로로 들어갔음

### 구현 후 GREEN

- `cargo test -p ddonirang-tool --lib`: 523/523 PASS
- P1-A native focused: 6/6 PASS
- native/WASM exact host payload: 1/1 PASS
- tracked-WASM parity: 8/8 cases PASS, 각 3회 deterministic repeat
- partial summary leak: 0
- official WASM freshness: PASS

### 실제 source mutation

작업 worktree와 clean-detached fixed target에서 각각 다음 3개 변이를 실행했다.

1. `PROFILE_IDENTITY_DISABLED`: RED → exact restore → GREEN
2. `HIDDEN_PREV25_RETRY`: RED → exact restore → GREEN
3. `RECURSION_GUARD_BYPASS`: RED → exact restore → GREEN

- mutation residue: 0
- 작업 worktree restore SHA-256: `f8752ac4a2841eebfc4cd15c0d7ec461d7c7273851e7139a6e8aa1c894b00cbc`
- clean-detached restore SHA-256: `ed16acd803caa65ff5f88471ba675d1198087af71916b585faed02a8fa79ffbb`
- 두 restore hash 차이는 checkout EOL 바이트 차이이며 각 worktree에서 시작 바이트와 정확히 일치했다.
- recursion guard bypass는 recursion 수용과 run stack overflow를 실제로 유발했고, 원복 뒤 6/6 GREEN이었다.

### clean-detached reproduction

- target: `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`
- initial/final Git state: clean / staged 0 / untracked 0
- native 6/6, native/WASM 1/1, tracked-WASM 8/8, freshness PASS
- mutation 3/3 RED → exact restore → GREEN
- 임시 reproduction worktree는 검증 후 제거했다.

### 포맷 검사 disposition

`cargo fmt --check -p ddonirang-tool`은 P1-A 밖의 기존 package-wide 미정렬 파일과 기존 블록 때문에 기준선 성격으로 FAIL한다. 이 slice는 비임대 파일과 무관한 대규모 포맷 diff를 만들지 않았다. `git diff --check`는 PASS했다.

## 고정 WASM identity

- bytes: 5,553,353
- SHA-256: `29480a59d264cffa280d6c1fb8a5a74da857955a6f028cd8b2adaf71e2366f51`
- fixed Git manifest blob bytes: 18,938
- fixed Git manifest blob SHA-256: `7ad02442eb9b6542e586b86880b7814560611cf927a51cd657e2c72ddc7b843e`
- fixed Git manifest blob object: `74ee08dfe743d41406ce0f0126fbe4a22dde6e43`
- manifest source tree SHA-256: `7a152b44b689e91d9d48f0c1ec00aba5bd5d942bc486b60b76c538ff1dff2e37`
- manifest JS binding SHA-256: `c5a80302a3a872fab1e8d14c2385f8b5b6ddde8cfc1096c64ee0231e4ec8df3d`
- new export occurrence: `wasm_run_summary_with_source_profile_json` 1

## 독립검토 요청 계약

검토자는 clean isolation에서 product/test fixed HEAD `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`를 검증한다. 이 handoff commit을 review parent로 사용하며, 결과 commit은 review report와 reviewer session delta만 포함하는 direct successor여야 한다. 제품·테스트·pack·WASM·SSOT·SPEC·UI diff는 0이어야 한다.

필수 검토:

- single supported-profile resolver와 native/WASM consumer convergence
- supported path의 hidden PreV25 retry/fallback 0
- omitted/unknown profile fail closed
- exact legacy migration diagnostic
- direct/mutual recursion deterministic unsupported
- native/WASM exact parity와 partial summary 0
- tracked WASM/manifest identity와 freshness
- 3개 mutation의 실제 RED 및 exact restore
- 전역 default switch, parser/canon authority, command membership, visible UI 변경 0

## OPEN / NONCLAIMS

- 독립검토 PASS와 P1-A closure는 OPEN
- 18/18 V1-Core membership, 4/4 execution contract, 9/9 exclusions 전체 승격은 하지 않음
- bounded recursion의 향후 지원 의미는 OPEN; 이번 slice는 명시적 unsupported만 구현
- pre-v25 corpus migration custody와 Foundation-12 correction/review는 OPEN
- exact public profile spelling과 public/default executable command membership은 OPEN
- P2/P3/P4/P5/P6, RC, release, activation, legal, Owner Human Smoke PASS는 OPEN
- whole P0 closure 또는 V1 readiness를 주장하지 않음
