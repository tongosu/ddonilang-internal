# P1 EVIDENCE_REBASE 재감사 R1 결과

## 1. 판정 범위

- 작업 ID: `DDN-P-V1-P1A-FU01-PASS-BIND-AND-EVIDENCE-REAUDIT-R1`
- 실행 성격: fixed Git object 기반 read-only 재감사
- 재감사 행: `VC04`, `VC06`, `VC09`, `VC11`, `VC12`, `VC15`, `VC17`
- 기준 census: `P1_V1_CORE_SUPPORTED_SUBSET_PREFLIGHT_R1/V1_CORE_SURFACE_PRODUCT_EVIDENCE_MATRIX.md`
- census 행 이름·의미를 그대로 사용했으며 새 registry/row를 만들지 않았다.
- 제품/test/pack/tracked-WASM/UI/SSOT/SPEC mutation은 0이다.
- 본 문서는 33행 census를 재작성하지 않고, 7개 기존 행의 evidence rebase disposition만 고정한다.

## 2. 고정 identity와 선형 계보

| 역할 | identity |
|---|---|
| P0 shared authority fixed | `84b307c5c84d43263ee342daa5610453c832fcf7` |
| P0 limited closure | `fe7c38c53cc3e1946b109b8002447983c185ba9b` |
| P1-A product semantics fixed | `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c` |
| P1-A product handoff | `151923c9d6a0708574416895c159ab21ffa87795` |
| P1-A first review | `b65463cc8f6f981e290000ffb4e14e1db6699fad` |
| FU01 evidence fixed | `25a271bfab45ef5c0b5f9abb67d6323547e1f5b4` |
| FU01 handoff | `9a5fca2fe6a8f1cad611a7998a23ecd3bcbb2300` |
| FU01 targeted PASS | `4a565c4ffc4a69281f5bb9b2c8a20e7b71214afb` |
| FU01 targeted PASS binding baseline | `2c3938c639ae274969a85c0735bcc7fb8470c12d` |
| binding baseline tree | `74a5a3a6348a60faeaab7940301d3f469e7d7061` |

`2c3938c6...`는 `4a565c4f...`의 direct successor이고 FU01 binding 문서 두 개만 더한다. 따라서 제품 의미는 P1-A fixed `bc883fd1...`, FU01 runner 의미는 `25a271bf...`, 독립 판정은 `4a565c4f...`에 각각 결속한다.

현재 authority는 내부 SSOT v25.19.0/RD-001~461과 공개 Language SPEC v0.6.0이다. 둘은 read-only로 사용했으며 public SPEC v0.6.0이 v25.16.1~v25.19.0 successor 의미 또는 제품 membership을 자동 포함한다고 간주하지 않았다.

## 3. 공통 frontdoor 경계

- native supported-profile 제품 API: `tool/src/runtime_surface.rs::run_summary_from_supported_source_profile[_diagnostic]`
- 공통 profile resolver/constructor: `tool/src/ddn_runtime.rs::resolve_supported_source_profile`, `DdnProgram::from_supported_source_profile_with_mode`
- WASM supported-profile 제품 API: `tool/src/wasm_api.rs::wasm_run_summary_with_source_profile_json`
- official CLI adapter 경로: `tools/teul-cli/src/cli/run.rs::run_file_with_emitter` -> `run_with_shared_runtime`
- Workbench 구조 경로: `solutions/seamgrim_ui_mvp/ui/runtime/runtime_bridge.js`, `host/host_bridge.js`, `workbench/workbench.js`
- Workbench source analysis profile은 `solutions/seamgrim_ui_mvp/ui/workbench/source_readiness.js::SOURCE_ANALYSIS_PROFILE_IDENTITY = "strict"`이다. Workbench 실행은 기존 project/VM frontdoor를 사용하며 `v1-core-v25`를 default ingress로 선택하지 않는다.

따라서 native/WASM에 `v1-core-v25` API가 존재한다는 사실을 public executable 이름, command membership, 또는 Workbench default ingress 승인으로 확장하지 않는다.

## 4. 행별 재감사

### VC04 — 기본 값·씨·identity

- exact semantic surface: 기본 값 family, type pin/`TypeRef`, 값 identity와 runtime type checking. V1 membership을 정하는 목록 자체는 포함하지 않는다.
- current owner paths/symbols:
  - `lang/src/ast.rs::TypeRef`
  - `lang/src/runtime.rs::Value`
  - `tool/src/ddn_runtime.rs::{check_param_type, check_value_type, check_named_type, check_applied_type, value_type_name}`
  - `tools/teul-cli/src/core/value.rs::Value`
- reachability:
  - native/WASM: 공통 `DdnProgram`과 `runtime_surface`/`wasm_api`에서 tool runtime value/type checking에 도달한다.
  - official CLI: shared runtime adapter로 도달하지만 private teul `Value` 모델이 별도로 남아 있다.
  - Workbench: generic project/VM execution을 통해 일부 도달한다. `v1-core-v25` default ingress 증거는 없다.
- executable evidence:
  - `pack/type_runtime_typecheck/**`
  - `tool/src/main.rs::{runtime_typecheck_rejects_mismatch_cases, runtime_typecheck_allows_optional_and_infer, runtime_typecheck_pack_inputs}`
  - `tool/src/ddn_runtime.rs::decl_block_type_alias_accepts_collection_and_string_none_aliases`는 fixed baseline에서 focused PASS 1/1.
  - source identity: `tool/src/ddn_runtime.rs` Git blob `b928a9af77a490d103d24f0e0bdb39d34eb5f856`; `tools/teul-cli/src/core/value.rs` Git blob `6da7d03222bdad479eafdfc221c88ffe23b014b1`.
- P0/P1-A impact:
  - P0 shared canon/preprocess는 type runtime ownership을 합치지 않았다.
  - P1-A는 `ddn_runtime.rs` supported-profile constructor를 추가했지만 private teul value model을 제거하지 않았다.
- disposition: `PRODUCT_GAP`
- 이유: typed checks 자체의 제품 근거는 있으나 census가 명시한 “single runtime authority 아님”이 그대로다. 두 `Value` enum과 adapter 변환 경계를 단일 제품 authority로 수렴하지 않은 상태에서 VC04 evidence-only 승격은 불가하다.
- independent review: 제품 수렴 fixed HEAD 뒤 필요.
- minimum coherent slice / FILE_OWNER 후보:
  - semantic goal: private teul value semantics를 새 authority로 남기지 않고 shared runtime value/serialization consumer로 축소한다.
  - 후보: `lang/src/runtime.rs`, `tool/src/ddn_runtime.rs`, `tools/teul-cli/src/core/value.rs`, `tools/teul-cli/src/cli/run.rs`, `pack/v1_core_value_type_identity_w1/**`, 전용 native/WASM/CLI parity runner.
  - 실제 lease는 별도 발급 전 0이며 현재 제품 수정은 하지 않았다.

### VC06 — 글·바이트·NFC

- exact semantic surface: UTF-8 원문, 글 escape, CR/LF 및 NFC 관련 ingress/canon, import/export byte custody.
- current owner paths/symbols:
  - `lang/src/lexer.rs::Lexer::read_string_escape`
  - `lang/src/frontdoor.rs::preprocess_frontdoor_source`
  - `tool/src/ddn_runtime.rs::from_source_epoch_with_mode`
  - `tool/src/local_project.rs::canonicalize_disk_text`
  - P0 shared canon의 `tool/src/canon.rs::lex_text_escape`
- reachability:
  - native/WASM: 공통 language/runtime path에서 escape와 source preprocess에 도달한다.
  - CLI: shared runtime adapter 앞의 pack runner/options 경계에서 현재 clean rebase가 되지 않는다.
  - Workbench: project source import/editor 분석에 부분 도달한다. import/export byte-roundtrip closure는 확인되지 않았다.
- executable evidence:
  - `pack/lang_text_escape_v1/**`, `tests/run_lang_text_escape_check.py`
  - first replay: c01/c02에서 expected `['첫','둘',...]` 대비 CLI가 `['첫\n둘',...]`을 내어 exact output mismatch.
  - repeat replay: tool binary link/lookup 환경에서 `E0463 can't find crate for ddonirang_tool`가 발생해 네 case 모두 clean product verdict를 만들지 못했다.
  - test runner Git blob: `a7e3a688e9306cd3519118a174ddb43335148b5a`.
- P0/P1-A impact:
  - P0 preprocess authority 수렴으로 과거 pack의 CLI expectation/runner 경로는 자동 상속할 수 없다.
  - P1-A supported-profile ingress는 같은 preprocess를 사용하지만 byte import/export closure를 추가하지 않았다.
- disposition: `EVIDENCE_REBASE_STILL_REQUIRED`
- independent review: 새 fixed evidence 뒤 필요.
- minimum coherent slice / FILE_OWNER 후보:
  - 먼저 product 수정 없이 current official native/WASM/CLI source profile을 쓰는 UTF-8/NFC/CRLF/escape/byte-roundtrip pack과 runner를 고정한다.
  - 후보 evidence paths: `pack/v1_core_text_byte_nfc_rebase_w1/**`, `tests/run_v1_core_text_byte_nfc_rebase_w1.py`, `tests/run_v1_core_text_byte_nfc_wasm_parity_w1.mjs`.
  - 그 RED가 import/export product gap을 재현할 때만 `lang/src/lexer.rs`, `tool/src/local_project.rs`, `tool/src/runtime_surface.rs`, `tool/src/wasm_api.rs`의 별도 lease를 요청한다.

### VC09 — named callable

- exact semantic surface: 이름 있는 callable 선언/호출/인자 전달과 non-recursive 실행. direct/mutual recursion은 VD01의 explicit unsupported이며 VC09 positive membership으로 포함하지 않는다.
- current owner paths/symbols:
  - parser/AST call nodes in `lang/src/ast.rs`와 parser/canonicalizer
  - `tool/src/ddn_runtime.rs::{DdnProgram::functions, eval_call, eval_callable}`
  - P1-A `validate_v1_core_no_named_callable_recursion`와 call graph collectors
- reachability:
  - native/WASM: `v1-core-v25` constructor가 callable graph를 검사한 뒤 runtime evaluator로 들어간다.
  - CLI: shared runtime adapter로 generic callable 실행은 도달한다.
  - Workbench: generic project/VM execution으로 부분 도달하며 supported-profile default는 아니다.
- executable evidence:
  - `tool/src/ddn_runtime.rs::tailed_call_alias_registers_myeonseo_variant` focused PASS 1/1.
  - P1-A fixed pack은 definition/rebinding positive와 recursion negative를 검증하지만 non-recursive named callable의 native/WASM exact positive parity fixture는 포함하지 않는다.
  - P1-A fixed identity `bc883fd1...`; runtime Git blob `b928a9af...`.
- P0/P1-A impact:
  - P0는 shared preprocess/canon authority를 제공한다.
  - P1-A는 recursion rejection을 추가해 VC09의 negative boundary는 강화했지만 positive callable 전체 evidence를 새 fixed head에 결속하지 않았다.
- disposition: `EVIDENCE_REBASE_STILL_REQUIRED`
- independent review: evidence-only fixed HEAD 뒤 필요.
- minimum coherent slice / FILE_OWNER 후보:
  - non-recursive named callable 정의·alias tail·typed args·failure atomicity의 supported-profile native/WASM/CLI exact parity pack.
  - 후보: `pack/v1_core_named_callable_rebase_w1/**`, `tests/run_v1_core_named_callable_rebase_w1.py`, `tests/run_v1_core_named_callable_wasm_parity_w1.mjs`.
  - 현재 구조 감사에서는 제품 source lease가 필요하다는 RED를 얻지 못했다.

### VC11 — 조건·반복

- exact semantic surface: `if`/조건 분기, `while`, `for-each`, natural iteration/current-item, scope restoration과 실패 atomicity. 전체 언어 control-flow membership 주장은 아니다.
- current owner paths/symbols:
  - `lang/src/ast.rs::{Stmt::If, Stmt::While, Stmt::ForEach}`와 parser/canonicalizer
  - `tool/src/ddn_runtime.rs::{eval_stmt_for_value, eval_stmt}`의 분기/반복 경로
  - `tool/src/local_project.rs`의 natural iteration/current-item project boundary
  - `tools/teul-cli/src/cli/run.rs` current-item diagnostic adapter
- reachability:
  - native/WASM: 공통 runtime surface로 도달한다.
  - CLI: shared runtime adapter로 도달한다.
  - Workbench: generic project/VM execution으로 도달하지만 `v1-core-v25` default ingress는 아니다.
- executable evidence at binding baseline:
  - `python tests/run_lang_continue_skip_pack_check.py`: PASS 4/4.
  - `python tests/run_lang_generic_iterable_order_contract_pack_check.py`: PASS 3/3.
  - `natural_iteration_current_item_runs_through_existing_foreach_runtime`: focused PASS 1/1.
  - `foreach_scope_restores_or_removes_binding_for_container_matrix`: focused PASS 1/1.
  - 기존 census의 P0 impact `UNAFFECTED`와 일치한다.
- P0/P1-A impact:
  - P0는 parser/canon 의미를 변경하지 않았다.
  - P1-A가 recursion call graph를 위해 `If`/`While`/`ForEach`를 순회하지만 control-flow 실행 의미는 바꾸지 않았다.
- disposition: `EVIDENCE_REBASE_READY`
- independent review: 필요. 이는 재감사 ready이지 scoped PASS 또는 membership 승격이 아니다.
- next coherent slice / FILE_OWNER 후보:
  - 제품 수정 0인 evidence-only VC11 rebase가 다음 추천 slice다.
  - 후보: `pack/v1_core_control_flow_evidence_rebase_w1/**`, `tests/run_v1_core_control_flow_evidence_rebase_w1.py`, `tests/run_v1_core_control_flow_wasm_parity_w1.mjs`, 전용 handoff/result docs.
  - 기존 테스트를 fixed object로 재생하고 supported-profile native/WASM parity와 failure atomicity를 한 packet에 결속한다.

### VC12 — 기본 collection

- exact semantic surface: 기본 list/set/map/pack 값과 typed collection, 접근·반복·순서·오류 경계. stdlib function membership은 VC17과 분리한다.
- current owner paths/symbols:
  - `lang/src/ast.rs::TypeRef::Applied`
  - `lang/src/runtime.rs::Value`
  - `tool/src/ddn_runtime.rs::{check_applied_type, eval_call}` 및 collection evaluator branches
- reachability:
  - native/WASM/CLI generic runtime에서 collection은 실행된다.
  - Workbench는 project/VM 실행과 view payload에서 일부 소비한다.
  - 각 collection family의 supported-profile public conformance packet은 없다.
- executable evidence:
  - `decl_block_type_alias_accepts_collection_and_string_none_aliases`: focused PASS 1/1.
  - `collection_search_and_point_access_charge_only_actual_visits`: focused PASS 1/1.
  - `foreach_scope_restores_or_removes_binding_for_container_matrix`: focused PASS 1/1.
  - `pack/type_runtime_typecheck/**`는 mismatch 중심이고 family별 native/WASM exact parity를 대체하지 않는다.
- P0/P1-A impact:
  - P0 영향은 additive preprocess authority 수준이다.
  - P1-A call graph traversal은 collection expression을 읽지만 collection 실행 의미를 바꾸지 않았다.
- disposition: `EVIDENCE_REBASE_STILL_REQUIRED`
- independent review: family-by-family fixed packet 뒤 필요.
- minimum coherent slice / FILE_OWNER 후보:
  - list/set/map/pack 각각의 typed success/failure, deterministic order, native/WASM parity를 묶는 evidence-only slice.
  - 후보: `pack/v1_core_basic_collection_rebase_w1/**`, `tests/run_v1_core_basic_collection_rebase_w1.py`, `tests/run_v1_core_basic_collection_wasm_parity_w1.mjs`.
  - 제품 gap이 재현될 때만 `lang/src/runtime.rs`, `tool/src/ddn_runtime.rs`, `runtime_surface.rs`, `wasm_api.rs` lease를 별도 요청한다.

### VC15 — 한국어 활용형

- exact semantic surface: 한국어 keyword/조사/호출 tail과 dialect alias를 canonical token/call로 해석하는 표면. public command spelling 결정은 포함하지 않는다.
- current owner paths/symbols:
  - `lang/src/dialect.rs::DialectConfig` 및 lexicon builders
  - `lang/src/dialect_keywords_v8.tsv`
  - `lang/src/lexer.rs::Lexer`
  - `lang/src/canonicalizer.rs` call-tail/josa canonicalization
  - P0 shared canon/preprocess consumer paths
- reachability:
  - native/WASM은 shared language tables와 preprocess를 사용한다.
  - CLI pack은 현재 shared-runtime option 경계에서 clean pass하지 않는다.
  - Workbench source analysis/editor는 `strict` 분석으로 부분 도달한다.
- executable evidence:
  - `pack/lang_dialect_smoke_v1/**`, `pack/dialect_builtin_equiv_v1/**`.
  - current replay 7건 모두 `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`로 FAIL: dialect smoke 4, builtin equivalence 3.
  - source blobs: `lang/src/dialect.rs` `d7ecebb3287b38c46123aba50c29d162182657c5`, table `fb075d9d448f2fa53b0e1de81097329d58ee7fd8`.
- P0/P1-A impact:
  - P0 shared canon/preprocess 수렴으로 과거 CLI option/pack evidence는 자동 상속되지 않는다.
  - P1-A는 shared supported ingress를 추가했지만 dialect pack을 새 profile/frontdoor에 재결속하지 않았다.
- disposition: `EVIDENCE_REBASE_STILL_REQUIRED`
- independent review: 새 fixed packet 뒤 필요.
- minimum coherent slice / FILE_OWNER 후보:
  - product change 없이 official shared-runtime invocation으로 dialect smoke/equivalence pack을 이식하고 native/WASM exact parity를 추가한다.
  - 후보: 기존 두 pack의 변경 대신 새 `pack/v1_core_korean_morphology_rebase_w1/**`, `tests/run_v1_core_korean_morphology_rebase_w1.py`, WASM parity runner.
  - RED가 table/call-tail product divergence를 재현할 때만 `lang/src/dialect.rs`, `dialect_keywords_v8.tsv`, `lexer.rs`, `canonicalizer.rs`의 single-writer lease를 요청한다.

### VC17 — 기본 stdlib

- exact semantic surface: V1-Core가 공개/default ingress에서 허용할 exact 기본 stdlib function membership과 alias/diagnostic contract.
- current owner paths/symbols:
  - `lang/src/stdlib.rs::{canonicalize_stdlib_alias, *_function_sigs, minimal_stdlib_sigs}`
  - `tool/src/ddn_runtime.rs::{verify_stdlib_registry_totality, canonicalize_stdlib_alias, eval_call}`
  - CLI consumer의 stdlib alias probes
- reachability:
  - 많은 기존 stdlib 함수는 generic native/WASM/CLI runtime에 존재한다.
  - Workbench도 generic VM을 통해 일부 실행한다.
  - 이 존재는 V1 membership을 뜻하지 않는다. 현재 exact V1 stdlib membership 목록은 0이다.
- executable evidence:
  - `python tests/run_stdlib_1_check.py`: 25 FAIL, 모두 legacy CLI option이 shared runtime 소유가 아니라는 `E_SHARED_RUNTIME_OPTION_UNSUPPORTED` 경계에서 중단.
  - `python tests/run_seamgrim_stdlib_1_wasm_check.py`: CLI에 `마디 0`과 `public_observation_trace_hash=...`가 추가되어 WASM output과 exact mismatch.
  - focused internal stdlib/collection tests는 존재하지만 membership과 public parity를 결정하지 않는다.
- P0/P1-A impact:
  - P0가 shared runtime/canon authority를 강화해 old stdlib pack invocation을 `REBASE_REQUIRED`로 만들었다.
  - P1-A는 stdlib membership selector를 추가하지 않았고 global default도 바꾸지 않았다.
- disposition: `CONFLICT_OR_OWNER_DECISION`
- independent review: Owner membership 결정, 제품/evidence fixed HEAD 뒤 필요.
- Owner 선택지:
  1. `PURE_MINIMAL` — public SPEC v0.6.0과 current runtime의 교집합에서 host/resource effect 없는 작은 deterministic pure subset을 exact 목록으로 승인. 장점은 closure·parity 위험 최소화, 단점은 초기 기능 폭이 작다. **추천**.
  2. `NO_STDLIB_FIRST_CORE` — 첫 V1-Core에서 VC17을 명시 제외하고 이후 successor로 분리. 장점은 가장 빠른 의미 안정화, 단점은 사용자 유용성과 기존 SPEC 기대가 낮아진다.
  3. `CURRENT_MINIMAL_STDLIB_SIGS_WHOLE` — 현재 `minimal_stdlib_sigs()` 전체를 후보 membership으로 승인. 장점은 기존 기능 활용 폭, 단점은 함수군·effect·alias·parity·rights 검토가 크게 늘고 현재 25+1 실패를 한 번에 떠안는다.
- recommended minimum slice / FILE_OWNER 후보:
  - Owner가 option 1 또는 별도 exact 목록을 고른 뒤 `lang/src/stdlib.rs`, `tool/src/ddn_runtime.rs`, `runtime_surface.rs`, `wasm_api.rs`, CLI adapter 및 새 membership/parity pack을 단일 writer에게 결속한다.
  - exact membership 결정 전에는 제품 lease를 발급하지 않는 것이 안전하다.

## 5. 분류 합계

| disposition | count | rows |
|---|---:|---|
| `EVIDENCE_REBASE_READY` | 1 | VC11 |
| `EVIDENCE_REBASE_STILL_REQUIRED` | 4 | VC06, VC09, VC12, VC15 |
| `PRODUCT_GAP` | 1 | VC04 |
| `EXPLICITLY_UNSUPPORTED` | 0 | - |
| `CONFLICT_OR_OWNER_DECISION` | 1 | VC17 |
| 합계 | 7 | exact audited rows |

## 6. 실행 로그 요약

- PASS:
  - `run_lang_continue_skip_pack_check.py`: 4/4
  - `run_lang_generic_iterable_order_contract_pack_check.py`: 3/3
  - focused Rust filters: current-item, foreach container scope, collection type alias, tailed callable, collection visit accounting 각 1/1
- FAIL/OPEN evidence:
  - text escape: first replay c01/c02 exact output mismatch; repeat replay build/link lookup `E0463`
  - stdlib pack: 25/25 current invocation failures at `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`
  - stdlib CLI/WASM: exact output mismatch 1
  - dialect packs: 7/7 current invocation failures at `E_SHARED_RUNTIME_OPTION_UNSUPPORTED`
- 최초 `cargo test ... -- --exact`는 module-qualified test 이름이 아니어서 0개가 선택됐고 근거에서 제외했다. 같은 filters를 `--exact` 없이 다시 실행해 각 1/1 PASS를 확인했다.
- 어떤 실패도 이 문서에서 whole-product defect, V1 membership, 또는 release verdict로 확대하지 않는다.

## 7. 다음 추천 slice

`VC11_CONTROL_FLOW_EVIDENCE_REBASE_W1`을 다음 safe slice로 추천한다.

- 이유: 일곱 행 중 유일하게 제품 gap/Owner 의미 결정 없이 기존 fixed-object 증거가 green이고, P0/P1-A 영향이 `UNAFFECTED`/traversal-only로 한정된다.
- 범위: 제품 source 0, 새 evidence pack/runner와 fixed-head reproduction, native/WASM supported-profile parity, failure atomicity, docs-only handoff.
- 후보 FILE_OWNER: `pack/v1_core_control_flow_evidence_rebase_w1/**`, `tests/run_v1_core_control_flow_evidence_rebase_w1.py`, `tests/run_v1_core_control_flow_wasm_parity_w1.mjs`, 전용 `work/codex/**`와 session delta.
- 실제 lease, 구현, 독립 PASS는 아직 발급·실행·선언하지 않았다.

## 8. 비주장

- FU01 targeted PASS 외 P1-A 전체 closure를 발급하지 않는다.
- 18/18 core surface, 4/4 execution contract, 9/9 automatic exclusions의 membership/readiness/PASS를 승격하지 않는다.
- VC08/10/13/14를 자동 편입하지 않는다.
- public executable 이름, command membership, stable profile spelling, Workbench default ingress를 결정하지 않는다.
- whole P0/P1/V1 readiness, P2~P6, RC, release, activation, legal, Owner Human Smoke/Human PASS, external-user success는 모두 OPEN이다.
