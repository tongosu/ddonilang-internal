# DDN-R-V1-VC06-VC12-VC04-COHERENT-MILESTONE-I1 독립검토

## 판정

`PASS_WITH_FOLLOW_UP`

VC06 supported-profile canon/string escape, VC12 language-core collection constructor authority, VC04 shared Value/type authority와 structured mismatch의 고정 제품 동작은 요청 범위에서 PASS다. 다만 재사용 Windows worktree의 clean 상태가 raw pack byte identity를 보장하지 않아 VC06 runner가 최초 실행에서 fixture SHA 불일치로 실패했다. Git blob 11개는 manifest와 모두 일치했고 LF materialization 뒤 전체 제품 검증은 GREEN이었으므로 제품 logic REWORK는 아니지만, fixed-artifact 재현 custody 보강이 필요하다.

## 고정 identity와 계보

- baseline: `7921a4d7832f1e89b2380b9729b2072e4651d3cc`
- VC06 fixed: `429c8dec3b1a8022005552f2eb1de050991c8e0e`, tree `13d6eda851828cc70292f81cb228d1342345a30b`
- VC06 handoff: `d798b90384077675a496906067b610ffcf768b66`
- VC12 fixed: `2a83ec409fedd00b9f7642362fe55bf72f00b583`, tree `495be98ee6e5f35dd29b970bae151207f9b0ff6a`
- VC12 handoff: `83fdf911ea7a59c44ae6aac541eb0b2b4e3f3a8e`
- VC04 fixed target: `163f14b47180ffd84312fb6609e8ce721c02acc7`, tree `868b402622840d4c220b019118adafd5458e17cf`
- review parent: `86a094d556a2c87104cbb56cdc94576e8e8c0a94`, tree `91aecf09f60892c52828d86213208e7869ef1b54`

`7921a4d7 → 429c8dec → d798b903 → 363f3e15 → 2c78dad8 → ee700e8e → 3ca95c15 → 7079dd0f → 2a83ec40 → 83fdf911 → 163f14b4 → 86a094d5`는 모두 ancestor 관계이며 merge count는 0이다. 세 handoff는 각 fixed의 direct successor이고 정확히 report/session-delta 2개만 추가한다. VC12 fixed의 direct parent는 docs-only authority refresh review `7079dd0f`이며, VC04 fixed의 direct parent는 VC12 handoff다.

## 독립 코드 판독

### VC06

- `tool::ddn_runtime::resolve_supported_source_profile` 정의는 1개다. source analysis, supported canon, supported native run이 이를 직접 소비하고 WASM은 동일 runtime-surface 함수를 위임 호출한다.
- explicit `v1-core-v25`만 허용한다. omitted/빈 identity는 `E_SOURCE_PROFILE_REQUIRED`, unknown은 `E_SOURCE_PROFILE_UNSUPPORTED`로 fail closed다.
- supported parser/canon은 `DdnProgram::from_supported_source_profile_with_mode` 한 경로를 사용한다. direct/mutual named recursion은 `E_V1_CORE_RECURSION_UNSUPPORTED`로 결정적으로 거절한다.
- normalizer는 quote, backslash, LF, CR, tab을 lexer가 다시 읽을 수 있는 escape로 출력하며 raw string NFC를 바꾸지 않는다.
- legacy `canonicalize_shared_source`와 default parse mode는 변경되지 않았다. 제품 diff의 추가행에서 PreV25 retry, semantic fallback, global default switch는 0이다.
- 보존 OPEN/PRODUCT_GAP: identifier NFC, byte literal/explicit UTF-8, BOM-as-data, invalid UTF-8 before String API, local-project raw-byte receipt, model string NFC, stable public diagnostic spelling.

### VC12

- construction authority는 `lang::runtime::list_new` 한 정의다. `tool::ddn_runtime`의 `차림|목록` dispatch는 직접 `Value::List`를 만들지 않고 `list_new`를 호출한다.
- `language_core_collection_constructor_sigs`가 `차림`과 `목록` callable surface를 보존하고, `list_function_sigs`에는 두 constructor provider가 없다.
- create/read는 `runtime_list_ops_work`, iterate는 기존 VC11 `natural_iteration_current_item_runs_through_existing_foreach_runtime`으로 회귀 확인했다.
- public spelling, parser/AST/canon surface와 legacy default는 바뀌지 않았다.

### VC04

- 공식 제품 경로의 type authority는 `lang::runtime::{check_value_type,value_type_name,TypeMismatchDetail}`다. tool runtime은 이를 소비하며 자체 matcher/name 구현을 제거했다.
- native, tracked WASM, official teul run adapter가 `E_RUNTIME_TYPE_MISMATCH / 값 / 수 / 글`을 보존한다. 실패 응답에 `output_rows` 또는 `output_log_texts`가 없어 partial publish는 0이다.
- `tools/teul-cli/src/runtime/eval.rs`의 private legacy `value_type_name`은 남아 있으나 official shared run adapter의 fallback으로 소비되지 않는다. whole legacy-engine convergence는 이 검토의 PASS 대상이 아니다.

## 실행 검증 — VC04 fixed target

- `python tests/run_v1_core_supported_ingress_w1.py`: PASS — native `7`, native/WASM exact `2`, tracked-WASM cases `10`, deterministic repeats `4`, partial summary `0`.
- `python tests/run_v1_core_text_byte_nfc_rebase_w1.py`: Git-blob LF materialization에서 PASS — `GREEN=7`, `RED=0`, `PRODUCT_GAP=4`, native/WASM exact `11`, repeats `3`, freshness PASS, local-project CRLF unit PASS.
- `cargo test -p ddonirang-lang --lib`: `366/366 PASS`.
- `cargo test -p ddonirang-tool --lib`: `525/525 PASS`.
- collection create/read, provider authority, nested type authority, VC11 current-item iteration: 각 실제 `1/1 PASS`.
- `cargo test --manifest-path tools/teul-cli/Cargo.toml run_file_preserves_shared_runtime_type_identity_diagnostic`: `1/1 PASS`.
- 세 제품 commit별 `git diff --check`: PASS.

## 결정적 mutation

`lang/src/stdlib.rs`의 `list_function_sigs`에 `목록` constructor provider 한 행을 임시로 되살렸다.

- RED: `collection_constructor_is_language_core_not_stdlib_provider` exit 1, `assertion failed: !list_sigs.iter().any(|sig| sig.name == "목록")`.
- reverse patch 후 원본 SHA-256 `d865154f5d2dbb0779c9bde5d994df85a7680eb9b8029e570f935fc6633604f1`로 byte-exact 복원.
- GREEN: 같은 테스트 `1/1 PASS`.
- product/source/test residue: 0. 추가 mutation/meta-test/framework: 0.

## tracked WASM identity와 freshness

- binary raw bytes: `5,561,603` / SHA-256 `74e935d194173bb3199bd7573d320742ca928cd5899c6a4567b3b065b4bbe170`; worktree와 Git blob 동일.
- manifest reused-worktree raw bytes: `19,550` / SHA-256 `d25f1ef349dd34fdaac0337a2e1f21bbda7f0cbe4f603fa7d30ef8e9c7cb73af`.
- manifest Git blob/canonical LF bytes: `18,981` / SHA-256 `ba35aa3b9adb19c681e19ec131738cb9900bb8c987d385ffef825e2b0c03042e`.
- JS binding reused-worktree raw: `92,991` / `a2573a427bb2f109245e06e7c60bbaec318d9f8459e8bfd4fbfcd79b3f75e8a8`; Git blob/canonical LF: `90,516` / `fdaede9f8b17f19c6a5719c06494afc677c2368bb79675a69cd3dc479adf96ee`.
- official freshness contract uses `crlf_to_lf_then_sha256` for text and raw bytes for WASM; independent freshness result is PASS.

## diff scope와 보호 경계

- VC06 product/evidence diff: exact `24` paths.
- VC12 product/evidence diff: exact `10` paths.
- VC04 product/evidence diff: exact `10` paths.
- 각 handoff diff: exact `2` work paths.
- baseline→VC04 fixed union: `50` paths = lang 3, tool 4, tools 1, pack 18, tests 4, tracked-WASM 4, work 10, publish/v1 6.
- `docs/ssot/**`, `publish/spec/**`, `lang/src/parser.rs`, `tool/src/canon.rs`, `tools/teul-cli/src/main.rs`, visible UI source diff: `0`.
- intermediate `publish/v1/**` 6개는 docs-only pre-release projection이며 제품 commit과 분리된다.

## follow-up

재사용 worktree 최초 clean 상태에서 VC06 fixture 11개의 worktree raw SHA가 모두 manifest와 달랐지만, 대응 Git blob SHA는 11/11 manifest와 일치했다. 대표 T01은 expected/Git blob `c0f201ec…`(276 bytes), worktree `cce14768…`(286 bytes)였다. VC06 pack만 LF로 임시 materialize해 전체 GREEN을 얻은 뒤 원래 CRLF bytes로 정확히 되돌렸고 Git clean/untracked0/ignored0을 확인했다.

후속은 raw-byte pack materialization을 checkout 단계에서 강제하거나, runner가 의도한 Git blob identity와 worktree transport identity를 명시적으로 분리하도록 하는 것이다. 이 follow-up은 fixed product logic PASS를 뒤집지 않지만, 현재 재사용 Windows worktree를 그대로 둔 clean-detached raw-hash 재현은 PASS라고 주장할 수 없다.

## live successor 영향과 nonclaims

Owner가 제공한 live internal CURRENT `v25.25.0 / RD-001~469`는 이 fixed line이 사용한 RD 의미를 계승하지만 membership/readiness는 별도 live authority다. review parent의 `publish/v1/CURRENT.md`는 역사적으로 `v25.22.0`을 가리키므로 live-current 문서라고 취급하지 않았다. `docs/ssot/**`와 `publish/spec/**`는 읽기 전용이며 mutation 0이다.

이 판정은 VC06/VC12/VC04 고정 coherent milestone의 제한된 제품 검토다. P1-A/P1/V1 whole closure, 40-row 또는 전체 membership/readiness, `SUPPORTED_FOR_V1`, public command/WASM membership, public docs promotion, release, activation, legal status, external-user success, Owner Human Smoke 또는 Human PASS를 승인하지 않는다.
