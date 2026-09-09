# CLI Dataset 공유·원자적 게시 권위 W55 인계

## 범위와 계보

- persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- live authority: internal SSOT v25.47.0 / RD-001~543
- public Language SPEC: v0.6.0
- baseline: `84871bf503266b456bc91bdf6944e3bf1b536379`
- product fixed: `86d0c0eab768f4e9300bb529420356a9492b2bce`
- fixed tree: `9d312fd5c785a117c2d0b8907a9e2ab9f17db69b`
- direct parent exact, merge count 0
- public command membership, executable/package naming, legacy alias period, physical `teul-cli` retirement transition: 0

## BLOCKED 재감사

기존 rolling reviewer가 P5 fixed `3e205ce816e47d29f6488bd86d029750e6afaaf5` / handoff `ccaa7132e9192a26f003917ae4f2795482c4e74f`를 검토한 review commit `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`는 현재 계보의 ancestor다. Review report SHA-256은 `05d9522c900d5c164064a003f92fabc100f64daf40100690b0e3c3747892a6d6`이고 verdict는 `PASS_TARGET_BOUND`, blocking finding은 0이다.

따라서 reviewer handle 부재는 현재 persistent goal의 blocker가 아니다. SPEC history, PathIR 공개 계약, public test/view/repl membership, VC17 exact landing은 해당 slice만 OPEN으로 유지하며 전체 개발 impasse로 집계하지 않는다.

## 제품 변화

`dataset export`의 format validation 이후 의미 처리, provenance, canonical hashing, artifact 구성과 게시를 `ddonirang-tool`의 shared `dataset_workflow`로 이동했다. `teul-cli`에는 기존 명령 spelling과 Geoul transport decode를 보존하는 adapter만 남는다.

`nurigym-v0`과 `nurigym-v1` 모두 다섯 산출물을 전부 준비한 뒤 existing shared atomic artifact-set authority로 게시한다. 한 target이라도 유효한 file target이 아니면 기존 predecessor를 포함한 어느 산출물도 변경하지 않는다.

## 변경 경로

1. `tool/src/dataset_workflow.rs`
2. `tool/src/lib.rs`
3. `tools/teul-cli/src/cli/dataset.rs`

새 pack 0, 새 runner 0, 새 framework 0, meta-test 0, tracked WASM/UI/SSOT/SPEC diff 0이다.

## RED → GREEN과 mutation

- baseline RED: empty Geoul input의 실패 경로에서 exit 1이지만 `action_spec.detjson`과 `obs_spec.detjson` 두 파일이 먼저 게시됨
- baseline partial artifacts:
  - action: 48 bytes / SHA-256 `f429769842eb3ea2034d40727bcea85bcca272298e5a08fbea5332efade14985`
  - observation: 48 bytes / SHA-256 `cb4733790acfd96ca558d51324e5e3703637f71e031e9d2b945957479ce1211b`
- fixed direct CLI: exit 1, partial artifact 0, staging residue 0
- risk mutation: shared atomic set을 sequential per-file atomic writes로 바꾸면 invalid target 실패 뒤 predecessor observation이 변경되어 RED
- exact restored shared source SHA-256: `216da592a1349b030fac1ffe16a5fa775a872e841a47697beb6756f58ea5bb39`
- restore GREEN: predecessor five-artifact set byte-preserved
- mutation/test temporary residue: 0

## 제품 검증

- shared dataset focused tests: 2/2 PASS
- deterministic v0 dataset hash: `sha256:182abe3aa3bb1a837bc03a897cbcd9b5f274a457ff44c5b518a786393a446f67`
- deterministic v1 dataset hash: `sha256:a7d6241ef2e5936c3e76029e5b538810fdb221870bb35d5debf453e8c7da87c2`
- `cargo check` teul-cli: PASS
- tool lib: 564/566 PASS; isolated worktree의 `docs/ssot` 부재에 의한 기존 `ai_prompt` 2 failures, new drift 0
- teul full: 1047/1056 PASS; 기존 boim/legacy/right-assignment 9 failures, new drift 0
- `git diff --check`: PASS

기존 `run_dataset_export_v0_provenance_check.py`와 `run_nuri_gym_contract_check.py`는 dataset workflow 도달 전에 legacy teul run options가 `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`로 거부되어 각각 5건과 2건이 실패했다. 이는 W55가 만든 dataset regression이 아니라 기존 runner/run-frontdoor rebase gap이며 PASS로 승격하지 않는다.

## C0~C8와 의존성 경계

- C0 registry/inventory: bounded custody; 전체 public command membership 미결정
- C1 single lang/tool frontdoor: 여러 승인 workflow가 shared authority로 수렴했으나 전체는 진행 중
- C2 private parser authority: 부분 잔여
- C3 private runtime authority: dataset의 Geoul transport decode 등 internal/deferred adapter custody 잔여
- C4 private value/canon/fallback authority: 부분 잔여, 전체 authority 0 미주장
- C5 required build/test/pack/publish dependency: 이전 M1의 bounded V1-required zero를 보존하되 historical/internal runner 의존은 잔여
- C6 parity: dataset native shared authority와 teul adapter를 검증; WASM/Workbench는 이 internal/deferred slice에서 NOT_APPLICABLE
- C7 public projection/Windows: P5 fixed-target `PASS_TARGET_BOUND`; whole P5/release closure 아님
- C8 physical retirement: OPEN, Owner deletion approval 전 삭제 후보 아님

## 제품 가치와 상태

- USER_WORKFLOW_CHANGED_OR_UNBLOCKED: 실패한 dataset export가 일부 schema 파일만 게시해 출력 디렉터리를 모순 상태로 만드는 위험을 제거했다.
- REUSED_TEST_COUNT: existing runner 2 families + existing Rust regression suites
- NEW_TEST_ARTIFACT_COUNT: 0
- META_TEST_CREATED: 0
- CHANGED_V1_GATE: internal/deferred dataset private semantic implementation 감소 및 failure partial publish 0
- status: `IMPLEMENTED_PENDING_REVIEW`

이 결과는 whole CLI convergence, teul semantic authority/dependency 0 전체, physical retirement, public membership, P0~P6 closure, V1 readiness/release/activation, legal, Owner Human Smoke 또는 Human PASS를 주장하지 않는다.
