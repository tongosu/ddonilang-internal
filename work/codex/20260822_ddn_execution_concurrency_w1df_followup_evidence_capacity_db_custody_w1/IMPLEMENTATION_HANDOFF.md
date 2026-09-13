# [Work관리] DDN-W-W1DF-FU01 구현 인계

## 상태

```text
DDN_EXECUTION_CONCURRENCY_W1DF_FOLLOW_UP_CORRECTION_IMPLEMENTED_UNDER_REVIEW
W1DF_LOGICAL_ORACLE_AND_PRODUCT_EVIDENCE_SEPARATED
W1DF_CAPACITY_TWO_REGRESSION_LANDED
W1DF_OFFICIAL_DB_CUSTODY_CURRENTIZED
READY_FOR_DDN_EXECUTION_CONCURRENCY_W1DF_FOLLOW_UP_TARGETED_INDEPENDENT_REVIEW
W1_FULL_CLOSURE_OPEN
RD207_PUBLIC_STABLE_WIRE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
external_user_success_count: 0
```

이 문서는 구현자 인계이며 독립 판정을 발행하지 않는다. 선재 Claude 판정
`PASS_WITH_FOLLOW_UP`을 보존하고 F1·F2·F3 후속만 교정했다.

## 고정점과 검토 원본 custody

- W1-C1 baseline: `eca2fbc50cd5cd50af299aad4fd87f33683c575a`
- W1-D~F product fixed HEAD: `d8a4b2ab5b7c5fe68b1738f955d2d3d5b2b86ad1`
- final implementation handoff: `42caa9a53cf85a3b638f85d45e0b564a1bbf92d9`
- Claude review commit: `01b2484a462c6aa691bdd11982e4046d1fbedc23`
- review direct parent: `42caa9a53cf85a3b638f85d45e0b564a1bbf92d9`
- verdict: `PASS_WITH_FOLLOW_UP`
- correction product/test commit: `084906e08ac6870d5dfcce715abf995139756913`
- review report: `work/claude/20260822_ddn_execution_concurrency_w1d_w1f_independent_review/DDN_REVIEW_DDN_R_W1DF_01_REVIEW_RESULT.md`
- report raw bytes: `43,973`
- report SHA-256: `70159db411f342fe14a0a5ed3519cd16e717afcf5e1fa44578bc1803d4b73ab0`
- `eca2fbc5... -> d8a4b2ab... -> 42caa9a5... -> 01b2484a... -> 084906e0...`는 선형이며 merge commit은 0이다.
- 원 검토 보고서와 검토 commit은 수정하거나 재작성하지 않았다.

## F1 — 논리 oracle과 제품 근거 분리

- 65행 전부를 `LOGICAL_ORACLE_ONLY`로 고정하고 stale `PRODUCT_PASS` 및
  `product_status`를 제거했다.
- 별도 근거 분류는 public source 제품 4건(P09/P10/N10/X20), internal typed 제품
  3건(P11/N11/X14), 제품 미지원 58건이다.
- 각 지원 행에 fixed HEAD, 실제 frontdoor, exact test ID와 검증 scope를 기록했다.
- 새 product-evidence runner는 W1-C1 official native/source-built WASM/tracked WASM
  10건과 연결된 Rust test 7개를 실제로 실행한다. 테스트 이름의 존재만 확인하거나
  runner 내부에 의미 기대값을 중복하지 않는다.
- 잘못된 W1-C1 case ID 주입은 RED, 원복 뒤 GREEN이었다.
- 논리 worker digest: `205c7c3738454a17d594b4cb25b4fe977fc300f17d5577f6939e3049782173b7`
- 논리 metadata digest: `377d2eb01d95e309d41870ae702423f1e68cda9cc801c2038bfb4e013f56e129`

## F2 — capacity 2 회귀와 변이 검출

- 공개 CLI/WASM/Workbench capacity override는 추가하지 않았다.
- tool integration test는 capacity 2에서 중첩 4회 전송이 `123456` FIFO 결과로
  수렴함을 검증한다.
- teul-cli test는 동일 결과와 `WAIT, WAIT, RESUME, RESUME` receipt phase를 함께
  검증한다. observer는 `cfg(test)` 전용이다.
- 다음 네 변이는 모두 RED 후 즉시 원복하고 GREEN을 재확인했다.
  1. pending FIFO `pop_front`를 LIFO `pop_back`으로 변경
  2. bounded-full admission 조건을 무시하고 항상 accept
  3. waiting FIFO `pop_front`를 LIFO `pop_back`으로 변경
  4. teul-cli WAIT receipt 기록 누락
- full regression: lang `361`, tool unit `492` + 신규 integration `1`, teul-cli `1,165` PASS.

## F3 — 공식 DB custody

- 공식 DB: `I:\home\urihanl\ddn\codex\build\seamgrim_project_data\seamgrim_projects.sqlite3`
- current bytes: `540,672`
- current SHA-256: `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228`
- current mtime: `2026-08-02T15:25:18.9785384+09:00`
- 기존 handoff의 `573,440` bytes / `3fbf028e...` 값은 current 증거가 아닌
  superseded stale snapshot으로 명시했다.
- 공식 DB write와 activation call은 0이다.

## 재현 검증

- logical oracle runner: 65/65 GREEN
- product-evidence runner: public 4, internal 3, unsupported 58; official W1-C1 10/10;
  연결 Rust evidence 7/7 GREEN
- W1-B native/source-built/tracked WASM parity: GREEN
- W1-C1 native/source-built/tracked WASM parity: 10/10 GREEN
- `run_ddn_cli_wasm_freshness_check.py`: PASS
- `run_seamgrim_deploy_artifacts_check.py`: PASS
- source build A, clean-detached source build B, tracked Workbench WASM은 모두
  `5,482,770` bytes, SHA-256
  `fbccef544253e2ffe1c05abda1826ce34e785a4de193bfe59dec48d7898dde05`로 byte-identical
- clean-detached HEAD `084906e0...`: runner·freshness·deploy·WASM identity GREEN,
  worktree clean, staged 0
- `git diff --check`: PASS

## 불변 경계와 OPEN

- 제품 runtime 의미 변경 0; 변경은 oracle/evidence runner, test-only regression,
  custody 문서에 한정했다.
- UI source/behavior diff 0, tracked WASM diff 0, `docs/ssot/**` diff 0,
  `publish/spec/**` diff 0.
- W1-B/C1 역사 rewrite 0, Malhimnuri R2 ancestry 혼입 0.
- PID `53196`은 `python`, `127.0.0.1:8787` owner는 `53196`으로 유지했다.
- W1-C2 public ReactionProvider surface, rendezvous runtime, RD-207 stable wire,
  Workbench structured diagnostic propagation, W1 전체 closure는 OPEN이다.
- targeted independent plain PASS 전에는 `PASS`, `CLOSED`, public activation 또는
  Human PASS를 주장하지 않는다.

## FU02 — README 재현 환경변수 완결

- successor baseline: `ccee4366373c77e48ef929e2fd502dda19ba0a0a`
- bound plain-PASS review: `091a08d107637ce7b282db16f71017cadb552ff9`
- `ccee4366...`에서 `W1DF_INDEPENDENT_PLAIN_PASS_BOUND`가 이미 결속됐으며,
  FU02는 그 비차단 README 누락만 닫는다.
- exact README:
  `pack/future_grammar_atlas_owner_closed_delta_r2_w1df/README.md`
- exact runner:
  `tests/ddn_execution_concurrency_w1df_product_evidence_runner.mjs`
- inherited W1-C1 runner:
  `tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs`
- README 이전 SHA-256:
  `6c071cf53d25fe583d2eeeb09676263b4bf6092394069aa5373e605b3e8942be`
- README 이후 SHA-256:
  `daf96b3ef4338abe35cfcb38fe4136b07f7367531bf215d33efaa192d9fed7e8`
- README는 `DDN_W1C1_CLI`를 source-built CLI 파일로,
  `DDN_W1C1_WASM_DIR`을 source-built Node.js WASM 디렉터리로,
  `DDN_W1C1_TRACKED_WASM_DIR`을 tracked Workbench WASM 디렉터리로 명시한다.
- logical oracle은 제품 실행 근거로 승격하지 않았고 capacity 증거는 계속
  `RUST_INTERNAL_TYPED_ONLY`이며 public bounded-capacity surface는 OPEN이다.
- 재현 artifact는 `e46f653d...` clean-detached CLI
  (`9f9f9fad053351a59eddfa8a6f54bf8d5608f3f9f7fc1ebc3d56aef11fee5291`),
  source-built Node.js WASM
  (`87992c2393592c4f9c568242b37261209708488f1e3e28f5ba69bb4a00054ed2`),
  baseline tracked Workbench WASM
  (`fbccef544253e2ffe1c05abda1826ce34e785a4de193bfe59dec48d7898dde05`)이다.
  `e46f653d...` 이후 baseline까지 runtime 제품 코드 diff는 0이다.
- README 전체 재생은 logical 65/65, W1-C1 public 10/10, internal named Rust
  evidence 7/7 PASS였다. 누락 CLI 환경변수, 존재하지 않는 CLI 파일, source-built
  위치의 tracked 디렉터리 대입, tracked 위치의 source-built 디렉터리 대입은 모두
  exit 1로 fail-closed했다.
- 제품, runner, oracle, expected ledger, UI, tracked WASM, `docs/ssot/**`, public
  SPEC 변경은 0이다.
