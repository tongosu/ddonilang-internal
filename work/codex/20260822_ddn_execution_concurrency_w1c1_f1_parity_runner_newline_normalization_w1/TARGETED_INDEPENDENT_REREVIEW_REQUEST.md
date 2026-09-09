# DDN execution concurrency W1-C1 F1 targeted 독립 재검토 요청서

## fixed HEAD와 판정 경계

```text
GOAL_ID: DDN_EXECUTION_CONCURRENCY_W1C1_F1_PARITY_RUNNER_NEWLINE_NORMALIZATION_W1
W1C1_PRODUCT_FIXED_HEAD: da791953f51a38e9489d0b2a158eeb419645fd43
W1C1_PRIOR_REVIEW_REQUEST: 6d84137aa6aa560e958d2e9cf5046da569bc8d69
PRIOR_INDEPENDENT_REVIEW_COMMIT: fe9077839130ba6fa33d80b7d09494a5f9f62faa
PRIOR_VERDICT: PASS_WITH_FOLLOW_UP
F1_CORRECTION_COMMIT: 2e080cdb36d5497454430b4c7cb27f04c29b178e
TARGETED_REREVIEW_FIXED_HEAD: 07f22eb20de650ad064bfcb1f9278a4b4daf6c38
REVIEW_MODE: FIXED_HEAD_READ_ONLY
ALLOWED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

검토자는 `TARGETED_REREVIEW_FIXED_HEAD`를 격리된 clean-detached worktree에서 읽기
전용으로 검토한다. 제품, runner, oracle, tracked WASM, UI와 기존 review 원본을
수정하지 않는다. 이 재검토는 prior review의 F1에만 한정한다.

## 원본 custody

prior review commit이 `6d84137...`의 단일 자식인지 확인한다. 원본 판정서는 다음이다.

```text
work/claude/20260822_ddn_execution_concurrency_w1c1_sender_route_internal_provider_independent_review/REVIEW_RESULT.md
bytes: 26,885
SHA-256: 3dc650554eb06858cf82990164bc8ad432f3d3527fe3236af16d7bddcb9e5a06
```

prior `PASS_WITH_FOLLOW_UP`와 F2 관찰을 다시 쓰거나 삭제하지 않는다.

## targeted 검토 항목

1. `fe907783..2e080cdb`의 변경 파일이
   `tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs` 하나인지 확인한다.
2. runner가 broad `.trim()`, `.trimEnd()` 또는 일반 whitespace 제거를 사용하지 않는지
   확인한다.
3. 비교 계약이 정확히 다음인지 확인한다.

   ```text
   expected_native_stdout = wasm_canon_body.endsWith("\n")
     ? wasm_canon_body
     : wasm_canon_body + "\n"
   ```

4. source-built WASM과 tracked WASM의 canonical body를 서로 직접 exact 비교하고,
   native 표시용 마지막 LF 하나만 별도 허용하는지 확인한다.
5. WASM body가 이미 LF로 끝날 때 LF를 중복하지 않는 assertion이 실제로 실행되는지
   확인한다.
6. 수정 전 runner가 정확한 `ddonirang-tool.exe` frontdoor에서 case 00~08 뒤 case 09
   trailing-newline 차이로 RED인지 재현한다.
7. 수정 후 case 00~09가 모두 PASS하고 native/source-WASM/tracked-WASM 의미 parity와
   canonical body identity가 유지되는지 재현한다.
8. 다음 세 임시 변이가 각각 RED인지 확인하고 완전히 원복한다.
   - canonical body 내부 문자 1개 변경
   - native expected output에 trailing space 1개 추가
   - native expected output에 LF 1개 추가
9. lang 357, tool 491, WASM freshness와 deploy artifact checker가 PASS하는지 확인한다.
10. clean-detached fresh native/WASM build에서 runner 10/10과 source-built/tracked WASM
    raw byte identity를 확인한다.
11. product code, CLI 출력 구현, WASM API/artifact, Workbench UI, SSOT/SPEC와 W1-B pack
    diff가 0인지 확인한다.

## 필수 실행

검토용 별도 target, WASM staging과 read-only v24.44.1 SSOT bridge를 사용한다.

```text
cargo build -p ddonirang-tool --bin ddonirang-tool
wasm-pack build tool --target nodejs --out-dir <isolated-output> -- --features wasm
node tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs
cargo test -p ddonirang-lang -q
cargo test -p ddonirang-tool --lib -q
python tests/run_ddn_cli_wasm_freshness_check.py
python tests/run_seamgrim_deploy_artifacts_check.py
git diff --check
```

runner에는 `DDN_W1C1_CLI=<isolated target>/debug/ddonirang-tool.exe`를 제공한다.
`teul-cli.exe`는 이 F1의 native canon presentation 증거가 아니므로 대체하지 않는다.

기준 tracked/source-built WASM은 5,467,851 bytes, SHA-256
`7106d312993408029404db967d100fdb6838192daef9e38bc45e2aa8acd7a6e7`이다.

## 보호 경계

- shared dirty root를 reset, stash, clean 또는 수정하지 않는다.
- `docs/ssot/**`, public SPEC, UI, tracked WASM을 수정하지 않는다.
- 공식 store write와 activation endpoint call을 하지 않는다.
- PID `53196`과 `127.0.0.1:8787`에 연결·종료·재시작하지 않는다.
- 임시 process, socket, profile, DB와 SSOT bridge를 종료 시 정리한다.
- review commit은 fixed HEAD의 직접 후손인 문서 전용 commit으로 만든다.

## 판정과 OPEN

독립 판정은 새
`work/claude/20260822_ddn_execution_concurrency_w1c1_f1_parity_runner_newline_normalization_targeted_rereview/REVIEW_RESULT.md`
에 직접 재현 근거와 함께 기록한다. `PASS_WITH_FOLLOW_UP` 또는 `REWORK`이면 우회하지
않고 해당 상태에서 중단한다.

plain `PASS` 전에는 다음 상태만 유지한다.

```text
DDN_EXECUTION_CONCURRENCY_W1C1_F1_PARITY_RUNNER_NEWLINE_NORMALIZATION_IMPLEMENTED_UNDER_REVIEW
W1C1_F1_TARGETED_REREVIEW_PENDING
W1C1_PLAIN_PASS_NOT_YET_ISSUED
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
