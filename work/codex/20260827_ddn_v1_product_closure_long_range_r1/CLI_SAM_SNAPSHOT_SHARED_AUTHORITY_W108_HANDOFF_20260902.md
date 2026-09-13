# CLI sam snapshot shared authority W108 handoff

## 결론

- 상태: `IMPLEMENTED_PENDING_COHERENT_REVIEW`
- 기준: `249aecbc9611bd41bd86c10896cbe1ae9da2310f`
- 제품 fixed: `5552b583cbd413eac7ff6bb0b242f5df68a10074`
- fixed tree: `084d7001355815439d77b6d6e9d81dd456479cf7`
- merge count: 0
- authority: internal SSOT v25.49.0 / public Language SPEC v0.6.0, 둘 다 변경 0

## 사용자·제품 가치

`sam`, geoul replay, replay-branch 및 live run이 사용하는 키보드 상태·한국어 별칭·네트워크 이벤트 투영을 `tool::geoul_snapshot`의 typed pure projection으로 수렴했다. `teul-cli`에는 private `State` 쓰기 adapter만 남았다. 기존 `run`의 네트워크 입력 미지정과 빈 입력 구분을 보존해 state hash 변화를 막았다.

## exact FILE_OWNER와 변경

- `tool/src/geoul_snapshot.rs`
- `tools/teul-cli/src/cli/sam_snapshot.rs`
- `tools/teul-cli/src/cli/run.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

새 dependency, pack, runner, framework, public command, public spelling, wire schema, UI 변경은 0이다. tracked WASM binary는 build 결과 byte-identical했고 manifest의 source identity만 갱신됐다.

## 검증

- shared `geoul_snapshot`: 5/5 PASS
- teul shared adapter seam: 1/1 PASS
- replay focused: 5/5 PASS
- tool lib: 614/616 PASS. 실패 2건은 isolated worktree에 `docs/ssot`가 없는 기존 ai-prompt environment failure다.
- teul full: 1025/1034 PASS. 실패 9건은 기존 legacy 보임/right-assignment frontdoor 기대와 current shared authority의 historical contract drift다.
- WASM freshness: source drift RED 후 build+manifest refresh, 최종 PASS
- `git diff --check`: PASS

## mutation

`sam_snapshot` adapter가 shared projection 결과를 전부 버리도록 주입했다. adapter product seam test가 exit 101로 RED가 되었고, 원본 SHA-256 `9a33d86355dd678edff540203af80de5bb6b2504edb19876095d1fc822d3d8f9`로 exact restore한 뒤 1/1 GREEN, residue 0을 확인했다.

## identities

- `tool/src/geoul_snapshot.rs`: 14,622 bytes / SHA-256 `e79c5f212f922c14a9ccb798e3c28480fd7dc01e7dd22e30e67a2cac635a6e8a`
- `tools/teul-cli/src/cli/run.rs`: 429,570 bytes / SHA-256 `ddc3fc7eaf7d3a9433fcf91614a04889f2dc079967c8ae9a1218a5b4e883e778`
- `tools/teul-cli/src/cli/sam_snapshot.rs`: 2,583 bytes / SHA-256 `9a33d86355dd678edff540203af80de5bb6b2504edb19876095d1fc822d3d8f9`
- WASM: 5,579,392 bytes / SHA-256 `6e62b09e7c1d7e312453d55d4a5f23e3c09681bb387844c53ff3892d322b068e`
- manifest: 30,136 bytes / SHA-256 `9fd9aff0d37c857438d9a830df429072499603d51016ecabbe92bc1e1cac0813`

## anti-meta / rights boundary

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: YES — sam/replay/live run 상태 투영의 single semantic owner 확보
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `META_TEST_CREATED`: 0
- 기존 제품 모듈 내부 test 추가: 3
- Rights Track `UNAVAILABLE-3`: 별도 OPEN. 이 구현과 내부 QA를 막지 않는다.
- 새 외부 dependency: 0

## 남은 경계

이 milestone은 teul 전체 semantic authority 0, required dependency 0, CLI 전체 통합, public binary/package retirement, P5/P6, V1 readiness/release/activation/legal/Human PASS를 주장하지 않는다. gaji public registry/physical contract와 public view/test/repl membership도 OPEN이다.
