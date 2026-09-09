# DDN-R-V1-P5-WASM-CANDIDATE-MATERIALIZATION-GUARD-I1 독립검토

## Verdict

`PASS`

이 판정은 P5 candidate-only fixed-HEAD source materialization guard에만 한정한다. Windows 장경로로 tracked source 한 파일이 누락돼도 pre-fix entrypoint가 실제 WASM build를 계속하고 exit 0을 반환하는 fail-open을 재현했다. fixed target은 repository-local `core.longpaths=true`와 clean-tree guard로 이 위험을 닫고, 불완전 checkout은 build 전에 `E_WASM_CANDIDATE_MATERIALIZATION_INCOMPLETE`로 fail closed했다.

## 고정 identity와 계보

- baseline/FU02 handoff: `2a71996c616d626d4c7850675a096ba42311ee0d`
- FU02 review bound: `436b6b6ba3ebbef06a348679051fd48f2b58fcf9`, tree `932f29ce3f36ffc604fef7918dcad15d077c956a`
- product/test fixed: `6edf6b586d0c0ff62761174fe958a204ce5f6938`, tree `8b771c96dc3705a96daf6ae9b626cb89b9889230`
- product fixed exact parent: `436b6b6ba3ebbef06a348679051fd48f2b58fcf9`
- handoff/review parent: `951d5f5b0f28b23bba12264fba84687b08a1b995`, tree `3849dd6e6c1f1c28674a6c9a698690ce359883d6`
- handoff exact parent: `6edf6b586d0c0ff62761174fe958a204ce5f6938`
- product 및 handoff merge count: 각각 `0`
- product diff: `scripts/build_wasm_tool.ps1`, `tests/test_wasm_source_remap_entrypoint.py` 정확히 2개
- handoff diff: writer handoff와 writer session delta 정확히 2개
- handoff report Git blob: `6,155 bytes`, SHA-256 `f6d97aa26fbcc7ef0adc4a3d1dec97db3554837be799bc8249d276cd80cdd51d`

이전 FU02 review commit `436b6b6b…`와 역사 branch `e72df779…`는 삭제·rewrite 없이 보존했다.

## 제품 변경 검토

candidate outer entrypoint는 기존 dirty/staged/RUSTFLAGS/CopyToUi fail-closed gate 뒤에 다음 두 조건만 추가한다.

1. materialized repository checkout 전에 local `core.longpaths=true`를 설정한다.
2. checkout 뒤 `git diff --quiet HEAD --`가 실패하면 `E_WASM_CANDIDATE_MATERIALIZATION_INCOMPLETE`를 throw하고 recursive build를 시작하지 않는다.

변경은 `SourceRemapMode=candidate`이면서 아직 canonical source materialization 안에 있지 않은 outer branch에만 있다. default entrypoint, three-root remap policy, candidate seal, runtime, tracked WASM, public spelling/UI/command behavior는 변경하지 않는다. 기존 focused test에는 두 guard 문자열 assertion만 추가됐고 새 test artifact, framework, meta-test는 `0`이다.

## pre-fix 실제 fail-open 재현

pre-fix `436b6b6b…`에서 공식 candidate entrypoint를 `CARGO_NET_OFFLINE=true`, `CopyToUi=false`로 실행했다. 장경로 누락 대상의 전체 경로 길이는 `270`자였다.

- checkout 오류: `Filename too long`
- 누락 tracked path: `work/codex/20260822_ddn_execution_concurrency_w1b_successor_canon_clean_cut/DDN_EXECUTION_CONCURRENCY_W1C_SENDER_FILTER_AND_REACTION_PROVIDER_OWNER_DECISION_PACKET.md`
- materialized HEAD/tree: `436b6b6b…` / `932f29ce…`
- materialized `core.longpaths`: 미설정
- materialized tracked status: 위 파일 `D` 정확히 1개
- entrypoint: checkout 오류 뒤 실제 compilation과 candidate seal을 계속 수행
- entrypoint final exit: `0`
- 생성 WASM: `5,558,787 bytes`, SHA-256 `58a32eb83527da6da3b39dfb8f335d5293cc6499bbbae628bfe390018a6577bc`

따라서 missing tracked source인데도 exit 0인 pre-fix fail-open은 실제 제품 경로에서 재현됐다. 이 build는 RED custody이며 release evidence가 아니다.

## fixed guard의 incomplete materialization RED

fixed script와 source worktree를 byte-clean 상태로 유지한 채, 호출 프로세스에서 `core.longpaths=true` 설정 한 호출만 일회성으로 무효화했다. 이는 같은 장경로 checkout 누락을 재현하면서 새 clean-tree guard는 그대로 실행시키기 위한 결정적 환경 mutation이다.

- source worktree mutation: `0`, Git status clean
- materialized HEAD: `6edf6b586d0c0ff62761174fe958a204ce5f6938`
- 장경로 checkout: 동일 tracked 파일 `D` 1개
- exact diagnostic: `E_WASM_CANDIDATE_MATERIALIZATION_INCOMPLETE`
- entrypoint exit: `1`
- candidate WASM 생성: `0`

guard는 recursive build, wasm-pack compilation, receipt seal보다 먼저 중단했다. 이 한 번의 위험 mutation 뒤 추가 변형은 수행하지 않았다.

## post-fix offline fixed-target GREEN

mutation 없는 fixed target에서 전체 경로 길이 `272`자의 별도 build root로 같은 공식 candidate entrypoint를 `CARGO_NET_OFFLINE=true`, `CopyToUi=false`로 실행했다.

- entrypoint exit: `0`
- materialized HEAD: `6edf6b586d0c0ff62761174fe958a204ce5f6938`
- materialized tree: `8b771c96dc3705a96daf6ae9b626cb89b9889230`
- materialized repository config: `core.autocrlf=false`, `core.longpaths=true`
- materialized tracked/untracked status: `0/0`
- candidate WASM: `5,558,787 bytes`, SHA-256 `58a32eb83527da6da3b39dfb8f335d5293cc6499bbbae628bfe390018a6577bc`
- candidate receipt: `2,470 bytes`, SHA-256 `2ad1120cdeeef3521a07bfdda31ac98e9cc34a92fbc20e6d0f30ff8b4655cf28`
- receipt semantic identity: `sha256:2716d1eb7b81b2482766457b174f890eee2ed4258fd43786c7dfc0cd2db0f85b`
- receipt source commit/tree: fixed identity와 exact 일치
- receipt artifact identity: `.gitignore`, JS, DTS 2개, WASM, package JSON의 `6/6` bytes/SHA exact 일치
- tracked WASM/manifest write: `0/0`

기존 inspector를 candidate WASM raw bytes에 다시 실행한 결과:

- internal absolute path count: `0`
- unknown path count: `0`
- private include count: `0`
- `/ddn-src` occurrence: `1`
- `/ddn-cargo-registry` occurrence: `95`
- `/ddn-rust-toolchain` occurrence: `21`
- inspector `--require-zero` exit: `0`

## focused tests와 기존 동작

`tests.test_wasm_source_remap_entrypoint`와 `tests.test_wasm_candidate_remap`의 기존 두 module을 재사용했다.

- total: `26/26 PASS`
- default repository-only remap contract: PASS
- candidate exact three mappings와 seal: PASS
- inherited flags 및 tracked-copy fail closed: PASS
- materialization contract assertions: PASS
- path scan, receipt identity/tamper, atomic substitution tests: PASS
- 새 runner/framework/meta-test: `0/0/0`

default build는 product diff상 변경된 candidate outer branch를 통과하지 않으며 기존 default-mode test도 PASS했다. tracked WASM은 `5,561,603 bytes`, SHA-256 `74e935d194173bb3199bd7573d320742ca928cd5899c6a4567b3b065b4bbe170`; tracked manifest checkout raw는 `19,550 bytes`, SHA-256 `d25f1ef349dd34fdaac0337a2e1f21bbda7f0cbe4f603fa7d30ef8e9c7cb73af`로 유지됐다.

## diff, 보호 범위와 cleanup

`436b6b6b… → 6edf6b58…`에서 `core/**`, `lang/**`, `tool/**`, `tools/**`, `pack/**`, tracked WASM/UI, `.gitattributes`, `docs/ssot/**`, `publish/spec/**` diff는 각각 `0`이다. `git diff --check`도 PASS했다.

독립 재현용으로 생성한 pre-fix RED, guard mutation RED, post-fix GREEN build/materialization 디렉터리 세 개는 identity 채증 후 검증된 build 경계 안에서 제거했다. 모두 고정 Git commit과 명령으로 재생성 가능한 임시 산출물이며 삭제 후 존재 `0`이다. source review worktree에는 tracked/staged/untracked/ignored residue가 없다.

## v25.32.0 영향 분류

읽기 전용 live internal `v25.32.0 / RD-001~483`은 RD-001~469를 보존하고 RD-470~483 GAJI module·잔여 compile-ready surface 계보를 결속한다. actual membership `40 = 28 REQUIRED + 2 OPTIONAL + 10 DEFERRED`, blocker `28`, readiness `UNCLAIMABLE`, numeric maturity `0 / NOT ASSIGNED`, `SUPPORTED_FOR_V1=0`도 유지한다. public SPEC 진입점은 `v0.6.0`이며 내부 successor는 자동 투영되지 않는다.

이 fixed target의 영향은 `P5_CANDIDATE_SOURCE_MATERIALIZATION_ADDITIVE_GUARD_ONLY`다. P0/P1-A와 기존 VC04/VC06/VC09/VC11/VC12 fixed product evidence에는 relevant semantic impact가 없고, P1 membership/readiness·P2 durable storage·P3 default ingress·P4 whole closure·public P5 release에는 승격 효력이 없다.

## Nonclaims

이 `PASS`는 P5 candidate materialization guard만 승인한다. P2/P3/P4/P5 전체 closure, Windows x64 package completion, tracked/public WASM 또는 command membership, rights/license clearance, public release·activation, P1/V1 membership/readiness, external-user success, Owner Human Smoke 또는 Human PASS를 승인하지 않는다.
