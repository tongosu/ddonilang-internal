# DDN execution concurrency W1-C1 F1 parity runner 개행 교정 인계

## 상태와 고정점

```text
GOAL_ID: DDN_EXECUTION_CONCURRENCY_W1C1_F1_PARITY_RUNNER_NEWLINE_NORMALIZATION_W1
W1C1_PRODUCT_FIXED_HEAD: da791953f51a38e9489d0b2a158eeb419645fd43
W1C1_FINAL_REVIEW_REQUEST_COMMIT: 6d84137aa6aa560e958d2e9cf5046da569bc8d69
INDEPENDENT_REVIEW_COMMIT: fe9077839130ba6fa33d80b7d09494a5f9f62faa
INDEPENDENT_REVIEW_PARENT: 6d84137aa6aa560e958d2e9cf5046da569bc8d69
INDEPENDENT_REVIEW_VERDICT: PASS_WITH_FOLLOW_UP
F1_CORRECTION_COMMIT: 2e080cdb36d5497454430b4c7cb27f04c29b178e
DDN_EXECUTION_CONCURRENCY_W1C1_F1_PARITY_RUNNER_NEWLINE_NORMALIZATION_IMPLEMENTED_UNDER_REVIEW
W1C1_F1_TARGETED_REREVIEW_PENDING
W1C1_PLAIN_PASS_NOT_YET_ISSUED
```

독립 검토 원본은 다음 경로의 review commit blob으로 보존된다.

```text
work/claude/20260822_ddn_execution_concurrency_w1c1_sender_route_internal_provider_independent_review/REVIEW_RESULT.md
bytes: 26,885
SHA-256: 3dc650554eb06858cf82990164bc8ad432f3d3527fe3236af16d7bddcb9e5a06
```

review commit은 `6d84137...`의 단일 자식이며 cherry-pick, squash, rebase 또는
commit 재작성 없이 그 후손 branch에서 교정했다.

## F1 교정

변경 파일은 다음 하나뿐이다.

```text
tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs
```

runner는 WASM canonical body를 변경하지 않고 native CLI의 기존 표시 계약만 다음처럼
모형화한다.

```text
expected_native_stdout = canonical_body.endsWith("\n")
  ? canonical_body
  : canonical_body + "\n"
```

`.trim()`, `.trimEnd()` 또는 일반 whitespace 정규화는 사용하지 않았다. source-built
WASM body와 tracked WASM body는 직접 byte-equivalent string으로 비교하고, 각각에 대해
위 표시용 LF 규칙으로 native stdout을 exact 비교한다. 이미 LF로 끝나는 body에 LF를
중복하지 않는 assertion도 runner 안에 둔다.

## RED에서 GREEN

정확한 제품 CLI는 `tool/src/main.rs`에서 빌드한 `ddonirang-tool.exe`다. 최초 탐색 중
`teul-cli.exe`를 runner에 주입한 GREEN은 다른 frontdoor이므로 증거에서 제외했다.
`ddonirang-tool.exe`와 v24.44.1 read-only SSOT bridge를 사용한 수정 전 runner는
case 00~08을 지난 뒤 case 09에서 다음 차이로 RED였다.

```text
WASM canonical body: ... "}"
native stdout:       ... "}\n"
```

교정 후 official runner 결과는 다음과 같다.

```json
{"schema":"ddn.execution_concurrency.w1c1.sender_route_provider.parity.v1","cases":10,"success_cases":6,"failure_cases":4,"source_built_wasm":true,"tracked_workbench_wasm":true,"reaction_provider_public_surface":"OPEN"}
```

case 09는 exact canonical body와 native 표시용 마지막 LF 하나를 구분해 PASS했고,
case 00~08의 runtime/diagnostic/summary parity도 그대로 PASS했다.

## 실패주입

corrected runner에 임시 변이를 한 번씩 적용하고 각 실행 뒤 완전히 원복했다.

| 변이 | 결과 |
|---|---|
| source WASM canonical body 내부 `관제탑`을 비교 직전에 `관제실`로 변경 | RED |
| native expected presentation 끝에 space 1개 추가 | RED |
| native expected presentation 끝에 LF 1개 추가 | RED |

최종 원복 runner SHA-256은
`35b48fa86d3a5faf8aaaf4b15050588a3b7a66596acc146e44af4c8b91770cc6`이며,
원복 뒤 official 10-case runner가 다시 GREEN이었다.

## 회귀와 clean-detached

| 검증 | 결과 |
|---|---:|
| `cargo test -p ddonirang-lang -q` | 357/357 PASS |
| `cargo test -p ddonirang-tool --lib -q` | 491/491 PASS |
| source-built native/source-WASM/tracked-WASM official runner | 10/10 PASS |
| `python tests/run_ddn_cli_wasm_freshness_check.py` | PASS |
| `python tests/run_seamgrim_deploy_artifacts_check.py` | PASS |
| `git diff --check` | PASS |

clean-detached worktree `ddn-execution-concurrency-w1c1-f1-clean-detached-2e080cdb`에서
새 Cargo target과 새 Node WASM staging으로 native CLI와 WASM을 다시 빌드했다. detached
runner는 10/10 PASS했고 source-built/tracked WASM은 다음으로 raw byte-identical했다.

```text
bytes: 5,467,851
SHA-256: 7106d312993408029404db967d100fdb6838192daef9e38bc45e2aa8acd7a6e7
```

검증용 SSOT junction은 두 worktree에서 target을 확인한 뒤 링크만 제거했다. 종료 시
Cargo, wasm-pack, ddonirang-tool, teul-cli, Node 잔존 process는 0이었다.

## 변경 금지 경계

`fe907783..2e080cdb`에는 official runner 한 파일만 변경되었다. 다음 diff는 0이다.

- `lang/**`, `tool/src/**`, `tools/teul-cli/**`
- `solutions/seamgrim_ui_mvp/ui/workbench/**`, UI `index.html`
- tracked WASM과 WASM API
- `docs/ssot/**`, public SPEC
- W1-B historical/successor pack
- CLI 출력 구현과 W1-C1 runtime code/phase

공식 store write와 activation endpoint call은 수행하지 않았다. 보호 PID `53196`과
`127.0.0.1:8787`은 읽기 전용 상태 확인만 수행했다.

## F2와 나머지 OPEN

F2는 이 목표에서 구현하지 않았으며 UI source 변경은 0이다.

```text
WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION_OPEN
RUNTIME_CODE_PHASE_PRESERVED_IN_PRODUCT_STATE
EXECUTION_FAILURE_MUST_NOT_BE_MASKED_BY_GENERIC_NO_VIEW_WARNING
UI_CHANGE_NOT_AUTHORIZED
UI_CHANGE_0
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE_OPEN
W1_FULL_CLOSURE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```

이 문서는 Codex 구현·직접 검증 인계다. targeted 독립 plain `PASS`, W1-C1 `CLOSED`
또는 W1 전체 닫힘을 발행하지 않는다.

## 2026-08-22 후속 targeted plain PASS 결속

위 문구는 구현 인계 시점의 역사 상태다. Claude review commit
`c8b0f3d46c4d400d0ed83431974c8badacd2295c`가 plain `PASS`와
`W1C1_F1_FOLLOW_UP_CLOSED`를 발행했고 successor branch에 `--ff-only`로 결속됐다.
W1-C1 제한 핵심 범위 마감은
`work/codex/20260822_ddn_execution_concurrency_w1c1_independent_pass_closure/W1C1_LIMITED_SCOPE_CLOSURE.md`를 따른다. F2와 W1-C2/W1 full closure는 계속 OPEN이다.
