# DDN-W1C2-I2-FU01 구현 인계

## 상태

```text
DDN_EXECUTION_CONCURRENCY_W1C2_I2_FOLLOW_UP_CORRECTION_IMPLEMENTED_UNDER_REVIEW
W1C2_I2_INTERNAL_INJECTION_API_CONFINED
W1C2_I2_EFFECT_PRECOMMIT_DIRECT_INVARIANT_LANDED
W1C2_I2_WASM_REPRODUCIBILITY_FOLLOW_UP_CLOSED
READY_FOR_W1C2_I2_TARGETED_INDEPENDENT_REREVIEW
W1C2_I2_PLAIN_PASS_NOT_YET_ISSUED
```

Codex는 독립 plain `PASS`나 W1-C2 I2 `CLOSED`를 발행하지 않는다.

## FU01A successor evidence 보강

FU01A는 기존 구현을 다시 하지 않고 test/checker evidence만 교정했다. 새 제품·테스트
fixed HEAD는 `6d39254b6d2d6116b5839a3afffddb6ab40ce1ce`다. exact 12축 fault,
외부 Cargo consumer `E0624`, 두 DB의 경로 identity, 보호 PID/port drift, baseline
failure와 UI/WASM 분리 증거는 `FU01A_TARGETED_REREVIEW_EVIDENCE.md`에 봉인했다.
새 검토 요청서는 `TARGETED_INDEPENDENT_REREVIEW_REQUEST_FU01A.md`다.

## 계보와 artifact custody

- implementation baseline: `af7ad5224c4645c81316fe72fb092ac337374347`
- I2 product/test fixed: `5b822e3f8754d3cf38fa1d26a9786dc9fbd6115e`
- I2 handoff: `a74fb85094b4219a89a77a1d0226676d2e106903`
- independent review/start parent: `c21c6820ba9ae936f029accaa3757490a4a80fa4`
- review report: `work/claude/20260823_ddn_execution_concurrency_w1c2_i2_ddnrunner_dispatch_independent_review/REVIEW_RESULT.md`
- report: 25,884 bytes / SHA-256
  `6ddddaa226ed80a200bb1a068bdfff61c638d138cce81a61519518f43b987ff8`
- correction commit: `556f63d59963a7bf13b5d6b5425775dc00cf10e8`
- product/test fixed HEAD: `f6be35616418b748b7201f9fcfa48c2524c8bcd4`
- merge commit count from starting parent: `0`

## F1 — 내부 injection API 봉쇄

세 DdnRunner injection builder를 `pub(#[doc(hidden)])`에서 `pub(crate)`로 제한했다.
crate root/prelude/CLI/WASM/UI re-export는 없다. 실제 DdnRunner 제품 dispatch는 그대로다.

```text
EXTERNAL_RUST_PROVIDER_INJECTION_API_COUNT: 0
PUBLIC_PROVIDER_SOURCE_INGRESS_COUNT: 0
PUBLIC_PROVIDER_WASM_EXPORT_COUNT: 0
PUBLIC_PROVIDER_CLI_OPTION_COUNT: 0
PUBLIC_PROVIDER_ENV_COUNT: 0
PUBLIC_PROVIDER_UI_CONTROL_COUNT: 0
```

공개 API에 의존하던 integration-style 사례는 runtime module 내부 unit-test context에서
실행하며, 실제 한국어 DDN과 `DdnRunner::run_update`를 그대로 사용한다. 제품 의미를
`cfg(test)`로 복제하지 않았다.

## F2 — effect와 commit 원자성 직접 증거

actual DdnRunner 15-case 중 직접 사례가 다음을 검증한다.

- 성공: prepare 외부 effect `0`, commit 뒤 허용 effect 정확히 `1`
- provider 실패: candidate state/outbox/receipt/effect intent 생성 뒤 실패해도 외부
  effect `0`, state `0`, outbox `0`, success receipt `0`, revision `0`
- merge conflict: 외부 effect `0`, partial state/outbox `0`
- 성공 effect observation은 committed world와 revision `1`, committed route frame을 본다.

effect sink 관찰 원장은 실패 EvalContext clone과 별개의 외부 경계로 유지해 실패 경로의
실제 호출 여부를 검출한다. publish 자체는 outer commit 이후에만 일어난다.

## F3 — WASM

판정은 `REPRODUCIBILITY_RESTORED`다. A/B/C/D/tracked가 모두 5,509,880 bytes,
SHA-256 `27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa`로
일치했다. 정확한 명령·환경·원인은 `WASM_REPRODUCIBILITY_MATRIX.md`에 기록했다.

## 회귀와 fault injection

- actual DdnRunner: `15/15 PASS`
- I1: `23/23 PASS`; case 22 label 교정 유지
- fault injection: 요구된 6축 모두 `GREEN -> source mutation RED -> restore GREEN`
- lang: `363/363 PASS`
- tool library: `507/507 PASS`
- tool binary: `410/412 PASS`; 아래 F4의 사전 존재 환경 실패 2건만 실패
- teul-cli: `1165/1165 PASS`
- W1-D~F logical oracle: `65/65 PASS`
- W1-D~F named product evidence: `7/7 PASS`
- freshness checker: `PASS`
- actual Edge: success/unhandled/ambiguity/exact reopen/PID swap `PASS`, served WASM
  hash 일치, console/page/network error `0`, public provider UI/input `0`

W1-C1 전체 orchestration은 현재 격리 worktree에
`docs/ssot/SSOT_MASTER_v24.44.1.md`가 없어 case 00 native 실행 전에 fail-closed했다.
run-mode 의미를 완화하거나 SSOT bridge를 임시 생성하지 않았다.

## F4 — 사전 존재 회귀 분리

| 항목 | baseline `af7ad522` | 현재 fixed HEAD | 제품 영향 | I2 인과 | 별도 과제 |
|---|---|---|---|---|---|
| `ai_prompt_output_invariants_hold` | `docs/ssot` 부재, exit 101 | 동일, exit 101 | AI prompt 생성 환경에서 fail-closed | 없음 | tool SSOT bundle/bridge 환경 계약 |
| `ai_prompt_output_matches_golden` | `docs/ssot` 부재, exit 101 | 동일, exit 101 | golden 생성 환경에서 fail-closed | 없음 | tool SSOT bundle/bridge 환경 계약 |
| W1-C1 case 09 canon LF | raw CLI exit 0, trailing LF 1 | raw CLI exit 0, trailing LF 1 | raw 제품 출력 차이 없음 | 없음 | full runner 환경 복원 뒤 재확인 |
| W1-C1/W1-D~F orchestration | baseline project/SSOT 계약에서 fail-closed | `SSOT_MASTER_v24.44.1.md` 부재로 fail-closed | 제품 의미를 실행하기 전 차단 | 없음 | isolated SSOT bundle custody task |

따라서 보고된 LF 문제 자체는 raw baseline/HEAD에서 재현되지 않았지만, full parity
runner를 현 환경에서 완주하지 못했으므로 후속을 임의로 닫지 않는다.

```text
PREEXISTING_AI_PROMPT_GOLDEN_REGRESSION_OPEN
PREEXISTING_W1C1_CANON_LF_REGRESSION_OPEN
PREEXISTING_ENV_SENSITIVE_TOOL_TEST_OPEN
```

## 보호 경계

- `docs/ssot/**`: diff `0`
- `publish/spec/**`: diff `0`
- Workbench UI source: diff `0` (tracked WASM과 manifest만 공식 절차로 변경)
- official DB: 573,440 bytes / SHA-256
  `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0`
- 시작·종료 실측: 보호 PID `53196` absent, `127.0.0.1:8787` not listening
- official write `0`, activation call `0`, deployment `0`, external outreach `0`
- task-owned auxiliary worktree/Cargo target/WASM capture/Edge process/socket residue `0`

## 계속 OPEN

```text
PUBLIC_KOREAN_NAME_OPEN
PUBLIC_PROVIDER_EXACT_SYNTAX_OPEN
PUBLIC_PROVIDER_SOURCE_INGRESS_0
STABLE_PROVIDER_IDENTITY_WIRE_OPEN
STABLE_PROVIDER_DIAGNOSTICS_OPEN
W1_FULL_CLOSURE_OPEN
RD207_PUBLIC_STABLE_WIRE_OPEN
PUBLIC_ACTIVATION_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
external_user_success_count: 0
```
