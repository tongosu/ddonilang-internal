# CLI native input snapshot shared authority W109 handoff

## 결론

- 상태: `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- 기준: `06669acfd23c3070d4f14c7a354e59393c80185d`
- 제품 fixed: `717acf26cc5ada4e0fbbf42e9953c66312086142`
- fixed tree: `2ebf9b634a822c783dcf7e22f09acdfc2546414a`
- merge count: 0
- authority: internal SSOT v25.49.0 / RD-001~543, public Language SPEC v0.6.0, 둘 다 변경 0

## 사용자·제품 가치

native `DdnRunner`, tracked WASM, `teul-cli sam`, replay 및 live run의 키보드 held/pressed/released 상태와 한국어 별칭이 하나의 `tool::geoul_snapshot` 제품 권위를 소비한다. native runtime 안에 있던 별도 key registry와 상태 생성기를 제거해 같은 입력이 frontdoor마다 다른 상태를 만드는 위험을 줄였다.

## exact FILE_OWNER와 변경

- `tool/src/input_tape.rs`
- `tool/src/ddn_runtime.rs`
- `tool/src/lib.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

`tool/src/lib.rs`의 조건부 확장은 WASM compile이 `crate::geoul_snapshot` unresolved import로 실제 RED가 된 뒤 최소 적용했다. `geoul_snapshot`은 host filesystem이나 process 권위가 없는 pure typed projection이다. 새 dependency, pack, runner, framework, public command, public spelling, wire schema, UI 변경은 0이다.

## 검증

- native `DdnRunner` keyboard alias/transition seam: 1/1 PASS
- shared input tape registry와 runtime-mask roundtrip: 6/6 PASS
- tool lib: 614/616 PASS. 실패 2건은 isolated worktree에 `docs/ssot`가 없는 기존 ai-prompt environment failure다.
- WASM build: host-only module gate 때문에 최초 compile RED, 최소 module availability correction 뒤 PASS
- tracked WASM freshness: exact rebuild 및 manifest 갱신 뒤 PASS
- `git diff --check`: PASS

## mutation

runtime `KEY_A`를 잘못된 tape bit에 투영하도록 inverse mapping을 바꿨다. 실제 native `DdnRunner` keyboard seam이 exit 101과 `left: 0 / right: 1`로 RED가 됐다. `tool/src/input_tape.rs`를 SHA-256 `f667af9c603ca3d6230091153ffa34fbfad7144d79e5ac74aaf48dcf9f4ecf8a`로 byte-exact restore한 뒤 native 1/1 및 input-tape 6/6 GREEN, residue 0을 확인했다.

## identities

- `tool/src/input_tape.rs`: 12,081 bytes / SHA-256 `f667af9c603ca3d6230091153ffa34fbfad7144d79e5ac74aaf48dcf9f4ecf8a`
- `tool/src/ddn_runtime.rs`: 1,103,563 bytes / SHA-256 `2ad0e21f53498b9808cb88b32a945cec5b37f8920cdd810880d76a199ae01442`
- `tool/src/lib.rs`: 3,883 bytes / SHA-256 `57f01b3f86af760c37a08c314322663a98a9b108686c74baeaa6cb581011b45b`
- tracked WASM: 5,580,180 bytes / SHA-256 `d3aeefc5da313920834833874541db618d711a9a4c690dfb46aaa22cdbc46ebc`
- manifest working bytes: 30,136 bytes / SHA-256 `4d1934b23be64286f29fc7c7d93e4dd10ff0aca3dc4c5f1cdb5191c11156661c`

## anti-meta / rights boundary

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: YES — native/WASM/teul/replay가 같은 keyboard snapshot authority를 사용
- `REUSED_TEST_COUNT`: 2 focused families + existing tool regression + existing freshness gate
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `META_TEST_CREATED`: 0
- 기존 `input_tape` unit test 확장: 1
- Rights Track `UNAVAILABLE-3 attribution`: 별도 OPEN이며 제품 내부 구현·QA와 분리
- 새 외부 dependency: 0

## 남은 경계

이 milestone은 전체 teul semantic authority 0, V1 required dependency 0, public command membership, teul binary/package retirement, P1/P5/P6 closure, V1 readiness/release/activation/legal/Human PASS를 주장하지 않는다. 독립검토는 다음 coherent CLI/teul authority milestone에 묶는다.
