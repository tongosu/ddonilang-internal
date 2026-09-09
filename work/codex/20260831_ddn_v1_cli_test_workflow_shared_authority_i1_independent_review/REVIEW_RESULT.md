# [DDN V1독립검토Work -> Codex개발관리Work] DDN-V1-CLI-TEST-WORKFLOW-SHARED-AUTHORITY-I1 — 독립검토 결과

## 판정

`PASS_TARGET_BOUND`

blocking finding은 0건이다. realms test의 입력 해석, thread mode 선택, 실행,
결과 직렬화와 pack/WASM test runner dispatch 권위는
`tool/src/test_workflow.rs`의 native product module로 단일화되었다.
`tools/teul-cli/src/cli/test.rs`는 공유 product API 5개를 재수출하는 4줄 adapter만
남으며 private runtime/value/result 또는 runner fallback authority는 0이다.

이 판정은 fixed product `eba99e9d...`의 CLI test-workflow shared-authority
slice에만 결속된다. public test command membership, whole CLI parity, view/repl,
public XP-02/M12, PathIR whole P1, ERQ, teul physical retirement, V1
closure/readiness/release/activation/legal/Human PASS는 승인하지 않는다.

## 검토 계약과 identity

- `CLAIM`: realms test-family semantic authority가 private teul 구현에서 shared
  `ddonirang-tool` product owner로 이동했고 CLI가 adapter로만 남았는가
- `TARGET_IDENTITY`: product
  `eba99e9d9ff7490400c2ef3ebae151df90fdd390` / tree
  `f301267d7845bd77ad234d4f8710c32274194fff`
- `PRIMARY_GATE`: private teul test-family semantic authority 0 + shared product
  owner parity
- `CLOSURE_EVIDENCE`: direct Git lineage, source/diff inspection, actual CLI
  threads 1/8, shared owner full tests, predecessor/fixed teul suite set comparison,
  existing pack, reviewer mutation, fail-closed output check와 tracked-WASM freshness
- `STOP_CONDITION`: private fallback authority가 남거나 invocation/output drift,
  신규 teul 실패, zero-realm partial publish 또는 stale-WASM acceptance가 관찰됨
- `DEEP_RESEARCH_CHECK`: `NOT_USE` — exact local product evidence로 충분함

## Reviewer와 lineage custody

- reused reviewer worktree:
  `I:\home\urihanl\ddn\codex\build\worktrees\review-ddn-v1-vc09-named-callable-evidence-rebase-i1-20260829`
- 시작 HEAD/review baseline:
  `0ba60fac3b930f9f6d8554bd8e9fe53ea36a64f9`
- 시작 상태: detached / clean / staged 0 / untracked 0 / merge 0
- fixed parent: exact baseline `0ba60fac...`
- fixed commit/tree: `eba99e9d9ff7490400c2ef3ebae151df90fdd390` /
  `f301267d7845bd77ad234d4f8710c32274194fff`
- docs-only handoff/review parent:
  `490bb97c7ecabdf0326fece2c7348c2ad7225e20` / tree
  `c2038716b14b66e085de578286a9d9c82b8e0738`
- fixed와 handoff는 각각 parent 1 / merge 0 / direct lineage
- new reviewer/task/worktree/branch/pack/runner/meta-test: 0
- producer/shared dirty root write, stage, reset, clean, stash: 0

Fixed product diff는 정확히 네 경로다.

1. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
2. `tool/src/lib.rs`
3. `tool/src/test_workflow.rs`
4. `tools/teul-cli/src/cli/test.rs`

`docs/ssot/**`, `publish/spec/**`, core/lang/pack, tracked WASM bytes와 manifest
외 UI diff는 0이다. handoff diff는 요청서와 producer session delta 두 문서뿐이며
product와 handoff custody가 분리되어 있다. `git diff --check`도 통과했다.

## Live authority refresh와 successor impact

검토 시점 live authority를 shared Work root에서 read-only로 재검증했다.

| authority | bytes | SHA-256 | 결과 |
|---|---:|---|---|
| `SSOT_INDEX_v25.45.0.md` | 144,214 | `3f998ad22bd1442b07978482877333ae238770ff6d069106d23fde027667cd7d` | MATCH |
| `SSOT_ALL_v25.45.0.md` | 4,733,265 | `e94623f128cf9894d76e0b0d8db8de07d4c86ed0aada6cfafab5a2d6f74fad3e` | MATCH |
| `SSOT_ALL_MANIFEST_v25.45.0.md` | 5,260 | `4a5656c86dd80c33383075a5dd6a7319bb83d396a205c0baff75e858ee88bb5d` | MATCH |
| `CURRENT_SHA256_v25.45.0.md` | 15,965 | `d8437401411f860e3f9bac5122d6ca76ce659e29185e4f2ebae6894402d8f9b7` | MATCH |
| `publish/spec/CURRENT.md` | 2,758 | `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0` | MATCH |

Official live checker도 `files=40`, `seal_rows=94`, mutations 10/10,
isolated regeneration 40/40, RD-001~536 drift 0, public v0.6.0으로 PASS했다.
v25.45.0은 promotion-added semantic RD 0이므로 이 slice의 요구 의미를 바꾸지
않는다. 다만 과거 검토 PASS를 successor 전체에 상속하지 않으며 본 판정은 위 exact
fixed identity에만 결속한다. public SPEC v0.6.0은 내부 v25.45.0과 별도 current다.

## Shared authority와 adapter 검증

- `tool/src/lib.rs`는 non-WASM native surface에서 `pub mod test_workflow`를
  제공한다.
- `tool/src/test_workflow.rs`가 `RealmsTestInput`, `RealmsStepInput`,
  `RealmsTestOutput`, `evaluate_realms_test`, `run_realms_test`, workspace root
  discovery와 golden/smoke runner dispatch를 모두 소유한다.
- CLI의 이전 `read_text`와 shared owner의 `std::fs::read_to_string`은 같은
  Rust API 호출/오류 mapping이어서 입력 semantics를 바꾸지 않는다.
- `tools/teul-cli/src/cli/test.rs`는 shared 함수 3개와 options type 2개를
  `pub use`할 뿐 별도 struct, evaluator, serializer, manager, Python runner 또는
  fallback branch가 없다.
- teul CLI main의 기존 `cli::test::*` invocation은 그대로이며 재수출을 통해
  shared owner만 호출한다.
- teul source 전체 검색에서 test-family의 제거된 private input/output/manager/
  runner 구현은 재등장하지 않았다. `cli/warp.rs`의 별도 warp workflow는 본
  test-family fallback이 아니다.

따라서 private teul test-family semantic authority count는 0이고 shared product
owner는 1이다.

## Invocation/output, regression과 partial publish

| 검증 | 결과 |
|---|---|
| shared owner focused tests | 3/3 PASS |
| `ddonirang-tool --lib` | 535/535 PASS |
| actual `teul-cli test` threads 1 | exit 0 / stdout·out 378 bytes / SHA-256 `09dfc4847b1dac2668a4b254727fede6729dcd0750e1e9f4f7d0f2119c33fd22` |
| actual `teul-cli test` threads 8 | exit 0 / stdout·out exact same bytes/SHA |
| existing `gogae8_w78_parallel_realms` pack | PASS |
| zero realm actual CLI | exit 1 / `E_REALM_INPUT realm_count must be > 0` / stdout 0 / out file absent |

checkout의 두 golden 파일은 CRLF materialization 때문에 working bytes가 388이고
SHA-256은 `97d4f940...19b4`이나, LF-normalized content는 378-byte actual output과
동일하고 기존 pack checker가 PASS했다. 이는 checkout EOL 차이이며 사용자
invocation/output semantic drift가 아니다.

Fixed와 predecessor에서 같은 teul 전체 suite를 각각 실행했다.

- fixed: 1040 PASS / 14 FAIL
- predecessor: 1040 PASS / 14 FAIL
- failure-name set symmetric difference: 0
- legacy failure 분류: 보임/frontdoor·right-assignment 6개,
  assignment/right-assignment/foreach atomicity 8개
- 신규 failure 또는 본 shared-authority slice drift: 0

## Reviewer mutation — RED → exact restore → GREEN

`REALM_COUNT_ZERO_GUARD_BYPASS`로
`if input.realm_count == 0` guard만 제거했다. permanent negative test는 exit 101
RED를 냈고 invalid input이 `realm_count: 0`, 빈 state hashes 결과를 반환하는
counterexample를 직접 관찰했다.

즉시 fixed source로 복원한 뒤:

- `tool/src/test_workflow.rs`: 6,235 bytes
- SHA-256:
  `96149ed6f311719ab1d516c6c03f7ceb7ef0c66b5e6a47939ad2e625284a05d9`
- Git blob: `64df821fa7c040c8a7d04cf204ee50ef3df083ba`
- focused GREEN: 1/1 PASS
- shared owner full GREEN: 535/535 PASS
- tracked/staged/untracked mutation residue: 0

실제 fixed CLI zero-realm 실행도 결과 파일을 만들지 않아 partial publish 0이다.

## Tracked WASM와 manifest dependency identity

- tracked WASM baseline→fixed diff: 0
- bytes/SHA-256: 5,571,041 /
  `ac750ce56f9ee34200136147ba7dd6b3d9187c5e023b0817c4ab030dade35de2`
- Git blob: `6764eab8be81bb5aea7722d45970bcdae946ebb1`
- official freshness checker: PASS
- manifest: 20,428 bytes / SHA-256
  `d0e3d64c38f025486e37dd7016f87f6c09307eb2c39717ef775ccfffb2c86d35`
- manifest source file count 103 / source tree SHA-256
  `feebf90a6bc961145572e9ca8960ba78d220f0b4498affe3df77d4c0dc1c9911`
- manifest의 `tool/src/lib.rs` 607 bytes/SHA와
  `tool/src/test_workflow.rs` 6,235 bytes/SHA가 actual fixed bytes와 2/2 exact match
- tracked WASM refresh/write: 0

native-only shared module을 source dependency identity에 포함하면서 actual WASM
artifact가 변하지 않는 계약이 fail-open 없이 검증되었다.

## Residue, process custody와 nonclaims

review-only cargo target과 test/log 디렉터리 두 곳은 exact path를 검증한 뒤
recoverable Recycle Bin cleanup했고 original-path residue는 0이다. protected
Node/process/port를 종료하거나 변경하지 않았고 port 8787 listener는 시작·종료
모두 0이다. 관찰 중 unrelated Node PID 한 개가 사라지고 한 개가 새로 보였으나
reviewer가 Node를 실행·종료하지 않았으며 task-owned process residue는 0이다.

다음은 여전히 NONCLAIM/OPEN이다.

- public test command membership, whole CLI parity, view/repl
- public XP-02/M12와 PathIR whole P1, ERQ
- teul physical retirement/deletion
- V1 closure/readiness/release/activation/legal/Human PASS

따라서 exact target-bound verdict는 `PASS_TARGET_BOUND`, blocking finding 0이다.
