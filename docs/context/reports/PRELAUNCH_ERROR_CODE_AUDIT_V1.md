# PRELAUNCH_ERROR_CODE_AUDIT_V1

- 작성일: 2026-07-08
- 범위: `tools/teul-cli/src/`, `lang/src/`
- 산출물 성격: 프리런치 동결 전 오류 코드 체계 실측 보고서
- SSOT 경계: `docs/ssot/**`는 읽기 전용 근거로만 취급하고 이 보고서는 SSOT를 수정하지 않는다.

## 요약

- 고유 오류 코드: 869건
- 카테고리 체계: 현재 SSOT에서 명시적으로 확정된 분류 체계를 확인하지 못했으므로, 아래 분류는 이번 스윕의 기계적 임시 분류이다.
- 카테고리 합계: 869건
- 미분류: 753건

| 카테고리 | 건수 | 기계 분류 규칙 |
|---|---:|---|
| 파서 | 42 | `parser.rs` 또는 `lexer.rs`에 정의 위치가 있는 코드 |
| 런타임 | 68 | 정의 위치 경로에 `/runtime/`이 포함된 코드 |
| 계약 | 5 | 코드명에 `contract`/`계약`/`물림`이 포함된 코드 |
| AGE게이트 | 1 | `E_AGE_NOT_AVAILABLE` 또는 `E_AGE_*` 코드 |
| 미분류 | 753 | 위 규칙에 걸리지 않은 코드 |

## 추출 방식

- 입력 경로 전체에서 오류 코드 토큰을 정규식 `(?<![A-Z0-9_])E_[A-Z0-9_]+(?![A-Z0-9_])`로 추출했다.
- 요청된 `E_[A-Z_]+` 기본 형태는 유지하되, 저장소에 `E_TENSOR_V0_*`처럼 숫자 세그먼트를 포함한 실제 코드가 있어 숫자를 포함했다.
- 경계 조건을 둔 이유는 `BUNDLE_PREFIX` 같은 문자열 내부의 부분 일치 `E_PREFIX`를 오류 코드로 오인하지 않기 위해서이다.
- 정의 위치는 `assert` 계열 라인이 아닌 첫 발생을 우선했고, 그런 발생이 없으면 첫 발생을 사용했다.
- 본 보고서는 코드명과 파일 경로만으로 분류한다. 의미 판단이나 SSOT 문구 결정을 하지 않는다.

## 검증

- 총 고유 코드 수 869건 = 카테고리 합계 869건
- 미분류 수: 753건
- `docs/ssot/**` 수정 없음

## 전체 코드 목록

| 코드 | 기계 분류 | 정의 위치 | 발생 수 |
|---|---|---|---:|
| `E_AGE_NOT_AVAILABLE` | AGE게이트 | `lang/src/age_gate.rs:44` | 3 |
| `E_ALRIM_JSON` | 미분류 | `tools/teul-cli/src/cli/alrim.rs:577` | 1 |
| `E_ALRIM_PARSE` | 미분류 | `tools/teul-cli/src/cli/alrim.rs:268` | 2 |
| `E_ALRIM_READ` | 미분류 | `tools/teul-cli/src/cli/alrim.rs:45` | 1 |
| `E_ALRIM_SCAN` | 미분류 | `tools/teul-cli/src/cli/alrim.rs:134` | 2 |
| `E_ALRIM_VARIANT_CONFLICT` | 미분류 | `tools/teul-cli/src/cli/alrim.rs:66` | 1 |
| `E_ALRIM_WRITE` | 미분류 | `tools/teul-cli/src/cli/alrim.rs:118` | 2 |
| `E_ASSET_MANIFEST` | 미분류 | `tools/teul-cli/src/main.rs:2093` | 1 |
| `E_BATANG_PREFIX_REMOVED` | 미분류 | `tools/teul-cli/src/cli/run.rs:143` | 5 |
| `E_BDL1_PACKET_INVALID` | 미분류 | `tools/teul-cli/src/core/bdl_packet.rs:22` | 1 |
| `E_BDL1_PACKET_TOO_LARGE` | 미분류 | `tools/teul-cli/src/core/bdl_packet.rs:21` | 1 |
| `E_BDL2_CMD_KIND` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2277` | 1 |
| `E_BDL2_FIXED_Q` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2083` | 1 |
| `E_BDL2_FLAGS` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2090` | 2 |
| `E_BDL2_MAGIC` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2067` | 1 |
| `E_BDL2_TRAILING` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2286` | 1 |
| `E_BDL2_TRUNCATED` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2747` | 1 |
| `E_BDL2_UTF8` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2828` | 1 |
| `E_BDL2_VERSION` | 미분류 | `tools/teul-cli/src/core/bogae.rs:2074` | 1 |
| `E_BLOCK_HEADER_COLON_FORBIDDEN` | 미분류 | `tools/teul-cli/src/canon.rs:2191` | 4 |
| `E_BOGAE_BAD_FIELD_TYPE` | 미분류 | `tools/teul-cli/src/core/bogae.rs:276` | 1 |
| `E_BOGAE_BUNDLE` | 미분류 | `tools/teul-cli/src/main.rs:2131` | 1 |
| `E_BOGAE_CHANNEL_TYPE_INVALID` | 미분류 | `tools/teul-cli/src/core/bogae.rs:280` | 1 |
| `E_BOGAE_CMD_CAP` | 미분류 | `tools/teul-cli/src/cli/run.rs:5820` | 2 |
| `E_BOGAE_CODEC_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/view.rs:29` | 1 |
| `E_BOGAE_COLOR_INVALID` | 미분류 | `tools/teul-cli/src/core/bogae.rs:283` | 1 |
| `E_BOGAE_COLOR_PACK_LOAD` | 미분류 | `tools/teul-cli/src/core/bogae.rs:281` | 1 |
| `E_BOGAE_COLOR_PACK_MISSING` | 미분류 | `tools/teul-cli/src/core/bogae.rs:282` | 1 |
| `E_BOGAE_COLOR_UNKNOWN` | 미분류 | `tools/teul-cli/src/core/bogae.rs:284` | 1 |
| `E_BOGAE_DETBIN_PARSE` | 미분류 | `tools/teul-cli/src/core/bogae.rs:285` | 1 |
| `E_BOGAE_EDIT` | 미분류 | `tools/teul-cli/src/main.rs:2114` | 1 |
| `E_BOGAE_ITEM_FIELD_MISSING` | 미분류 | `tools/teul-cli/src/core/bogae.rs:279` | 1 |
| `E_BOGAE_ITEM_KIND_INVALID` | 미분류 | `tools/teul-cli/src/core/bogae.rs:278` | 1 |
| `E_BOGAE_LIVE_MODE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3330` | 1 |
| `E_BOGAE_MISSING_FIELD` | 미분류 | `tools/teul-cli/src/core/bogae.rs:277` | 1 |
| `E_BOGAE_NON_INT_PIXEL` | 미분류 | `tools/teul-cli/src/core/bogae.rs:275` | 1 |
| `E_BOGAE_PLAYBACK_INFINITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3383` | 1 |
| `E_BUNDLE_ARTIFACT_HASH` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:97` | 1 |
| `E_BUNDLE_ARTIFACT_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:92` | 1 |
| `E_BUNDLE_CERT_MARK` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:222` | 1 |
| `E_BUNDLE_EVAL_REPORT_HASH` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:116` | 1 |
| `E_BUNDLE_EVAL_REPORT_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:107` | 1 |
| `E_BUNDLE_HASH_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:283` | 1 |
| `E_BUNDLE_INPUT_EMPTY` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:133` | 1 |
| `E_BUNDLE_INPUT_LEN` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:141` | 1 |
| `E_BUNDLE_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:126` | 1 |
| `E_BUNDLE_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:124` | 1 |
| `E_BUNDLE_INPUT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:129` | 1 |
| `E_BUNDLE_MANIFEST_FIELDS` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:218` | 1 |
| `E_BUNDLE_MANIFEST_PARSE` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:190` | 1 |
| `E_BUNDLE_MANIFEST_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:188` | 1 |
| `E_BUNDLE_MANIFEST_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:193` | 1 |
| `E_BUNDLE_MANIFEST_SOURCE_HASH` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:262` | 2 |
| `E_BUNDLE_MANIFEST_SOURCE_PROVENANCE` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:273` | 2 |
| `E_BUNDLE_MODEL_ACTIVATION` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:68` | 1 |
| `E_BUNDLE_MODEL_DIM` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:64` | 1 |
| `E_BUNDLE_MODEL_HASH` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:83` | 1 |
| `E_BUNDLE_MODEL_PARSE` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:57` | 1 |
| `E_BUNDLE_MODEL_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:53` | 1 |
| `E_BUNDLE_MODEL_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:60` | 1 |
| `E_BUNDLE_MODEL_UTF8` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:55` | 1 |
| `E_BUNDLE_WASM_HASH` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:157` | 1 |
| `E_BUNDLE_WASM_HASH_EMPTY` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:386` | 1 |
| `E_BUNDLE_WASM_HASH_FORMAT` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:390` | 1 |
| `E_BUNDLE_WASM_HASH_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:367` | 1 |
| `E_BUNDLE_WEIGHTS_COUNT` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:412` | 1 |
| `E_BUNDLE_WEIGHTS_LEN` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:407` | 1 |
| `E_BUNDLE_WEIGHTS_READ` | 미분류 | `tools/teul-cli/src/cli/seulgi_bundle.rs:77` | 1 |
| `E_CACHE_UNAVAILABLE_OFFLINE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2366` | 3 |
| `E_CALC_FREEVAR_AMBIGUOUS` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:15050` | 2 |
| `E_CALC_FREEVAR_NOT_FOUND` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14136` | 1 |
| `E_CALC_NUMERIC_BAD_ITERATION` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14538` | 1 |
| `E_CALC_NUMERIC_BAD_STEP` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14433` | 3 |
| `E_CALC_NUMERIC_BAD_VAR` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14422` | 4 |
| `E_CALC_NUMERIC_BRACKET_SIGN` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:15003` | 1 |
| `E_CALC_NUMERIC_DIALECT_UNSUPPORTED` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14592` | 1 |
| `E_CALC_NUMERIC_EVAL_FAIL` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14911` | 1 |
| `E_CALC_NUMERIC_FREEVAR_AMBIGUOUS` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14617` | 1 |
| `E_CALC_NUMERIC_FREEVAR_NOT_FOUND` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14608` | 1 |
| `E_CALC_TRANSFORM_BAD_ORDER` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14056` | 1 |
| `E_CALC_TRANSFORM_UNSUPPORTED_OPTION` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14036` | 3 |
| `E_CALL_TAIL_AMBIGUOUS` | 런타임 | `tools/teul-cli/src/runtime/error.rs:223` | 5 |
| `E_CALL_TAIL_MISSING_AFTER_ARGS` | 미분류 | `lang/src/canonicalizer.rs:709` | 1 |
| `E_CALL_TAIL_MISSING_STMT` | 미분류 | `lang/src/canonicalizer.rs:575` | 1 |
| `E_CALL_TAIL_NO_SEED` | 파서 | `lang/src/parser.rs:5766` | 1 |
| `E_CANON_ALRIM_EVENT_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:6078` | 1 |
| `E_CANON_ALRIM_PLAN_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:5898` | 1 |
| `E_CANON_BAD_ALIAS` | 미분류 | `tools/teul-cli/src/canon.rs:2923` | 4 |
| `E_CANON_BAD_ATOM` | 미분류 | `tools/teul-cli/src/canon.rs:628` | 2 |
| `E_CANON_BAD_BLOCK` | 미분류 | `tools/teul-cli/src/canon.rs:787` | 1 |
| `E_CANON_BAD_CHAR` | 미분류 | `tools/teul-cli/src/canon.rs:529` | 1 |
| `E_CANON_BAD_ESCAPE` | 미분류 | `tools/teul-cli/src/canon.rs:740` | 4 |
| `E_CANON_BAD_MAEGIM` | 미분류 | `tools/teul-cli/src/canon.rs:1942` | 1 |
| `E_CANON_BAD_NUMBER` | 미분류 | `tools/teul-cli/src/canon.rs:618` | 1 |
| `E_CANON_BAD_STRING` | 미분류 | `tools/teul-cli/src/canon.rs:661` | 1 |
| `E_CANON_BLOCK_EDITOR_PLAN_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:6131` | 1 |
| `E_CANON_CHECK_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/canon.rs:107` | 3 |
| `E_CANON_CHOOSE_NEEDS_ELSE` | 미분류 | `tools/teul-cli/src/canon.rs:3315` | 1 |
| `E_CANON_CONTRACT_MODE` | 계약 | `tools/teul-cli/src/canon.rs:3462` | 1 |
| `E_CANON_CONTRACT_NEEDS_ELSE` | 계약 | `tools/teul-cli/src/canon.rs:3239` | 1 |
| `E_CANON_DECL_HEADER_ONLY_CHAEVI` | 미분류 | `tools/teul-cli/src/canon.rs:1819` | 1 |
| `E_CANON_EXEC_POLICY_MAP_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:5913` | 2 |
| `E_CANON_EXPECTED_ATOM` | 미분류 | `tools/teul-cli/src/canon.rs:2800` | 1 |
| `E_CANON_EXPECTED_EQUALS` | 미분류 | `tools/teul-cli/src/canon.rs:3017` | 1 |
| `E_CANON_EXPECTED_EXPR` | 미분류 | `tools/teul-cli/src/canon.rs:2770` | 3 |
| `E_CANON_EXPECTED_FORMULA` | 미분류 | `tools/teul-cli/src/canon.rs:2810` | 1 |
| `E_CANON_EXPECTED_IDENT` | 미분류 | `tools/teul-cli/src/canon.rs:3787` | 1 |
| `E_CANON_EXPECTED_ILTTTAE` | 미분류 | `tools/teul-cli/src/canon.rs:1456` | 1 |
| `E_CANON_EXPECTED_LBRACE` | 미분류 | `tools/teul-cli/src/canon.rs:2234` | 1 |
| `E_CANON_EXPECTED_LITERAL` | 미분류 | `tools/teul-cli/src/canon.rs:3138` | 1 |
| `E_CANON_EXPECTED_RBRACE` | 미분류 | `tools/teul-cli/src/canon.rs:1840` | 5 |
| `E_CANON_EXPECTED_SEED_PARAM` | 미분류 | `tools/teul-cli/src/canon.rs:2846` | 1 |
| `E_CANON_EXPECTED_STRING` | 미분류 | `tools/teul-cli/src/canon.rs:2410` | 1 |
| `E_CANON_EXPECTED_TARGET` | 미분류 | `tools/teul-cli/src/canon.rs:1561` | 3 |
| `E_CANON_EXPECTED_TERMINATOR` | 미분류 | `tools/teul-cli/src/canon.rs:2017` | 3 |
| `E_CANON_EXPECTED_THUNK_CONDITION` | 미분류 | `tools/teul-cli/src/canon.rs:3500` | 1 |
| `E_CANON_EXPECTED_THUNK_SUFFIX` | 미분류 | `tools/teul-cli/src/canon.rs:3360` | 2 |
| `E_CANON_FIXIT_INPLACE` | 미분류 | `tools/teul-cli/src/cli/canon.rs:319` | 1 |
| `E_CANON_GUSEONG_FLATTEN_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:6041` | 1 |
| `E_CANON_GUSEONG_FLAT_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:5883` | 1 |
| `E_CANON_HOOK_EVERY_N_MADI_INTERVAL_INVALID` | 미분류 | `tools/teul-cli/src/canon.rs:2140` | 3 |
| `E_CANON_HOOK_EVERY_N_MADI_SUFFIX_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/canon.rs:2168` | 4 |
| `E_CANON_HOOK_EVERY_N_MADI_UNIT_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/canon.rs:2148` | 4 |
| `E_CANON_HOOK_SUFFIX` | 미분류 | `tools/teul-cli/src/canon.rs:2182` | 1 |
| `E_CANON_MAEGIM_CONTROL_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:6901` | 1 |
| `E_CANON_MAEGIM_CONTROL_PLAN_JSON` | 미분류 | `tools/teul-cli/src/canon.rs:5987` | 1 |
| `E_CANON_MAEGIM_GROUPED_VALUE_REQUIRED` | 미분류 | `tools/teul-cli/src/canon.rs:1908` | 3 |
| `E_CANON_MAEGIM_NESTED_FIELD_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/canon.rs:1988` | 3 |
| `E_CANON_MAEGIM_NESTED_SECTION_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/canon.rs:1967` | 3 |
| `E_CANON_MAEGIM_STEP_SPLIT_CONFLICT` | 미분류 | `tools/teul-cli/src/canon.rs:2002` | 5 |
| `E_CANON_OPEN_BLOCK` | 미분류 | `tools/teul-cli/src/canon.rs:2221` | 1 |
| `E_CANON_PROMPT_ELSE` | 미분류 | `tools/teul-cli/src/canon.rs:3388` | 1 |
| `E_CANON_RECEIVE_OUTSIDE_IMJA` | 미분류 | `tools/teul-cli/src/canon.rs:1725` | 3 |
| `E_CANON_ROOT_HIDE_UNDECLARED` | 미분류 | `tools/teul-cli/src/canon.rs:4311` | 2 |
| `E_CANON_TENSOR_SHAPE` | 미분류 | `tools/teul-cli/src/canon.rs:3055` | 3 |
| `E_CANON_TUPLE_INDEX_INVALID` | 미분류 | `tools/teul-cli/src/canon.rs:3570` | 1 |
| `E_CANON_UNEXPECTED_TOKEN` | 미분류 | `tools/teul-cli/src/canon.rs:1319` | 1 |
| `E_CANON_UNSUPPORTED_COMPOUND_TARGET` | 미분류 | `tools/teul-cli/src/canon.rs:1535` | 1 |
| `E_CANON_UNSUPPORTED_COMPOUND_UPDATE` | 미분류 | `tools/teul-cli/src/canon.rs:1506` | 1 |
| `E_CANON_UNTERM_BLOCK` | 미분류 | `tools/teul-cli/src/canon.rs:815` | 1 |
| `E_CANON_UNTERM_STRING` | 미분류 | `tools/teul-cli/src/canon.rs:691` | 3 |
| `E_CERT_CANON_BYTES_DRIFT` | 미분류 | `tools/teul-cli/src/cli/cert.rs:395` | 2 |
| `E_CERT_JSON_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:100` | 2 |
| `E_CERT_KEYGEN_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/cert.rs:44` | 1 |
| `E_CERT_KEY_ALGO` | 미분류 | `tools/teul-cli/src/cli/cert.rs:296` | 1 |
| `E_CERT_KEY_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:312` | 1 |
| `E_CERT_KEY_PARSE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:291` | 2 |
| `E_CERT_KEY_READ` | 미분류 | `tools/teul-cli/src/cli/cert.rs:289` | 1 |
| `E_CERT_KEY_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/cert.rs:293` | 1 |
| `E_CERT_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/cert.rs:447` | 1 |
| `E_CERT_OUT_WRITE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:456` | 1 |
| `E_CERT_SIGN_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/cert.rs:80` | 1 |
| `E_CERT_VERIFY_ALGO` | 미분류 | `tools/teul-cli/src/cli/cert.rs:337` | 1 |
| `E_CERT_VERIFY_FAIL` | 미분류 | `tools/teul-cli/src/cli/cert.rs:355` | 1 |
| `E_CERT_VERIFY_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/cert.rs:106` | 1 |
| `E_CERT_VERIFY_PARSE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:112` | 2 |
| `E_CERT_VERIFY_PUBKEY_FORMAT` | 미분류 | `tools/teul-cli/src/cli/cert.rs:340` | 1 |
| `E_CERT_VERIFY_PUBKEY_PARSE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:347` | 1 |
| `E_CERT_VERIFY_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/cert.rs:334` | 1 |
| `E_CERT_VERIFY_SIGNATURE_FORMAT` | 미분류 | `tools/teul-cli/src/cli/cert.rs:344` | 1 |
| `E_CERT_VERIFY_SIGNATURE_PARSE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:350` | 1 |
| `E_CHAEBI_IN_LOOP` | 미분류 | `tools/teul-cli/src/canon.rs:1826` | 14 |
| `E_CHECK_DUPLICATE_SYMBOL` | 미분류 | `tools/teul-cli/src/cli/check.rs:73` | 1 |
| `E_CHECK_TYPE_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/check.rs:67` | 1 |
| `E_CLI_AGE_TARGET` | 미분류 | `tools/teul-cli/src/cli/run.rs:1813` | 1 |
| `E_CLI_ARTIFACT` | 미분류 | `tools/teul-cli/src/main.rs:1523` | 1 |
| `E_CLI_BAD_PATH` | 미분류 | `tools/teul-cli/src/cli/canon.rs:418` | 1 |
| `E_CLI_BAD_SEED` | 미분류 | `tools/teul-cli/src/main.rs:1504` | 1 |
| `E_CLI_BOGAE_CMD_POLICY` | 미분류 | `tools/teul-cli/src/main.rs:1528` | 3 |
| `E_CLI_BOGAE_OVERLAY` | 미분류 | `tools/teul-cli/src/main.rs:1565` | 2 |
| `E_CLI_CANON` | 미분류 | `tools/teul-cli/src/cli/canon.rs:220` | 1 |
| `E_CLI_COMPAT_RELEASE_BLOCKED` | 미분류 | `tools/teul-cli/src/main.rs:1637` | 1 |
| `E_CLI_CONSOLE_GRID` | 미분류 | `tools/teul-cli/src/main.rs:1508` | 2 |
| `E_CLI_CONSOLE_PANEL` | 미분류 | `tools/teul-cli/src/main.rs:1510` | 2 |
| `E_CLI_MADI` | 미분류 | `tools/teul-cli/src/main.rs:1506` | 1 |
| `E_CLI_MISSING_OUT` | 미분류 | `tools/teul-cli/src/cli/canon.rs:413` | 1 |
| `E_CLI_READ` | 미분류 | `tools/teul-cli/src/cli/canon.rs:74` | 1 |
| `E_CLI_WRITE` | 미분류 | `tools/teul-cli/src/cli/canon.rs:351` | 17 |
| `E_CODE` | 미분류 | `tools/teul-cli/src/cli/diag.rs:23` | 4 |
| `E_CONTRACT_TIER_UNSUPPORTED` | 계약 | `tools/teul-cli/src/cli/run.rs:1745` | 5 |
| `E_CURRENTLINE_BRACE_MATCH` | 미분류 | `lang/src/currentline.rs:763` | 1 |
| `E_CURRENTLINE_CELL_READ` | 미분류 | `tools/teul-cli/src/main.rs:1756` | 1 |
| `E_CURRENTLINE_COMPILED_WRITE` | 미분류 | `tools/teul-cli/src/main.rs:1794` | 1 |
| `E_CURRENTLINE_CONTEXT_JSON` | 미분류 | `lang/src/currentline.rs:105` | 1 |
| `E_CURRENTLINE_CONTEXT_OUT_DIR` | 미분류 | `tools/teul-cli/src/main.rs:1861` | 1 |
| `E_CURRENTLINE_CONTEXT_READ` | 미분류 | `tools/teul-cli/src/main.rs:1768` | 1 |
| `E_CURRENTLINE_CONTEXT_WRITE` | 미분류 | `tools/teul-cli/src/main.rs:1871` | 1 |
| `E_CURRENTLINE_IMJA_BLOCK` | 미분류 | `lang/src/currentline.rs:709` | 1 |
| `E_DATASET_EMPTY` | 미분류 | `tools/teul-cli/src/cli/dataset.rs:48` | 2 |
| `E_DATASET_FORMAT` | 미분류 | `tools/teul-cli/src/cli/dataset.rs:20` | 1 |
| `E_DATASET_GEOUL_MANIFEST_AUDIT_HASH` | 미분류 | `tools/teul-cli/src/cli/dataset.rs:359` | 1 |
| `E_DATASET_GEOUL_MANIFEST_JSON` | 미분류 | `tools/teul-cli/src/cli/dataset.rs:342` | 1 |
| `E_DATASET_GEOUL_MANIFEST_READ` | 미분류 | `tools/teul-cli/src/cli/dataset.rs:335` | 1 |
| `E_DATASET_GEOUL_MANIFEST_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/dataset.rs:349` | 1 |
| `E_DET_TIER_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/run.rs:3224` | 1 |
| `E_DIAG_REPORT_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3718` | 1 |
| `E_DIAG_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3295` | 8 |
| `E_DOCSET_GOLDEN_EMPTY` | 미분류 | `tools/teul-cli/src/cli/docset.rs:126` | 1 |
| `E_DOCSET_GOLDEN_READ` | 미분류 | `tools/teul-cli/src/cli/docset.rs:119` | 1 |
| `E_DOCSET_HASH_READ` | 미분류 | `tools/teul-cli/src/cli/docset.rs:256` | 1 |
| `E_DOCSET_META_JSON` | 미분류 | `tools/teul-cli/src/cli/docset.rs:231` | 1 |
| `E_DOCSET_NONDETERMINISM` | 미분류 | `tools/teul-cli/src/cli/docset.rs:135` | 1 |
| `E_DOCSET_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/docset.rs:189` | 2 |
| `E_DOCSET_SOURCE_PROVENANCE_JSON` | 미분류 | `tools/teul-cli/src/cli/docset.rs:221` | 1 |
| `E_DOCSET_SOURCE_READ` | 미분류 | `tools/teul-cli/src/cli/docset.rs:200` | 1 |
| `E_DOCSET_WRITE` | 미분류 | `tools/teul-cli/src/cli/docset.rs:343` | 2 |
| `E_DOCTEST_FAIL` | 미분류 | `tools/teul-cli/src/cli/docset.rs:166` | 2 |
| `E_DOCTEST_MANIFEST_PARSE` | 미분류 | `tools/teul-cli/src/cli/docset.rs:149` | 1 |
| `E_DOCTEST_MANIFEST_READ` | 미분류 | `tools/teul-cli/src/cli/docset.rs:143` | 1 |
| `E_DOCTEST_MANIFEST_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/docset.rs:151` | 1 |
| `E_DOCTEST_SOURCE_READ` | 미분류 | `tools/teul-cli/src/cli/docset.rs:164` | 1 |
| `E_DOTBOGI_AFTER_STATE_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:140` | 1 |
| `E_DOTBOGI_CANON_JSON` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:177` | 1 |
| `E_DOTBOGI_CASE_DOTBOGI` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:42` | 1 |
| `E_DOTBOGI_CASE_EVENTS` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:55` | 1 |
| `E_DOTBOGI_CASE_INPUT` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:32` | 1 |
| `E_DOTBOGI_CASE_INPUT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:35` | 1 |
| `E_DOTBOGI_CASE_PARSE` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:21` | 1 |
| `E_DOTBOGI_CASE_READ` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:17` | 1 |
| `E_DOTBOGI_CASE_ROUNDTRIP` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:210` | 14 |
| `E_DOTBOGI_CASE_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:24` | 2 |
| `E_DOTBOGI_CASE_STATE` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:119` | 2 |
| `E_DOTBOGI_CASE_UTF8` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:19` | 1 |
| `E_DOTBOGI_CASE_VIEW_META` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:48` | 1 |
| `E_DOTBOGI_OUTPUT_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:135` | 1 |
| `E_DOTBOGI_REPORT_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:145` | 1 |
| `E_DOTBOGI_STATE_WRITE_FORBIDDEN` | 미분류 | `tools/teul-cli/src/cli/dotbogi.rs:59` | 3 |
| `E_DULTRA_REPLAY_SEED` | 미분류 | `tools/teul-cli/src/cli/dultra_replay.rs:23` | 2 |
| `E_DULTRA_REPLAY_SEED_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/dultra_replay.rs:95` | 1 |
| `E_ECO_ABM_SPATIAL` | 미분류 | `tools/teul-cli/src/cli/eco.rs:337` | 1 |
| `E_ECO_ABM_SPATIAL_DIR` | 미분류 | `tools/teul-cli/src/cli/eco.rs:394` | 1 |
| `E_ECO_ABM_SPATIAL_JSON` | 미분류 | `tools/teul-cli/src/cli/eco.rs:400` | 1 |
| `E_ECO_ABM_SPATIAL_READ` | 미분류 | `tools/teul-cli/src/cli/eco.rs:340` | 1 |
| `E_ECO_ABM_SPATIAL_SEED` | 미분류 | `tools/teul-cli/src/main.rs:2207` | 3 |
| `E_ECO_DIVERGENCE_DETECTED` | 미분류 | `tools/teul-cli/src/cli/eco.rs:566` | 7 |
| `E_ECO_MODEL_EXEC` | 미분류 | `tools/teul-cli/src/cli/eco.rs:457` | 1 |
| `E_ECO_NETWORK_FLOW` | 미분류 | `tools/teul-cli/src/cli/eco.rs:268` | 5 |
| `E_ECO_NETWORK_FLOW_DIR` | 미분류 | `tools/teul-cli/src/cli/eco.rs:313` | 1 |
| `E_ECO_NETWORK_FLOW_JSON` | 미분류 | `tools/teul-cli/src/cli/eco.rs:319` | 1 |
| `E_ECO_NETWORK_FLOW_READ` | 미분류 | `tools/teul-cli/src/cli/eco.rs:271` | 1 |
| `E_ECO_NETWORK_FLOW_SEED` | 미분류 | `tools/teul-cli/src/main.rs:2172` | 2 |
| `E_ECO_NETWORK_FLOW_THRESHOLD` | 미분류 | `tools/teul-cli/src/main.rs:2181` | 3 |
| `E_ECO_RUNNER_DIAG` | 미분류 | `tools/teul-cli/src/cli/eco.rs:108` | 2 |
| `E_ECO_RUNNER_DIR` | 미분류 | `tools/teul-cli/src/cli/eco.rs:254` | 1 |
| `E_ECO_RUNNER_MODEL_EXEC` | 미분류 | `tools/teul-cli/src/cli/eco.rs:443` | 1 |
| `E_ECO_RUNNER_MODEL_LEX` | 미분류 | `tools/teul-cli/src/cli/eco.rs:414` | 1 |
| `E_ECO_RUNNER_MODEL_PARSE` | 미분류 | `tools/teul-cli/src/cli/eco.rs:417` | 1 |
| `E_ECO_RUNNER_MODEL_READ` | 미분류 | `tools/teul-cli/src/cli/eco.rs:116` | 2 |
| `E_ECO_RUNNER_PARSE` | 미분류 | `tools/teul-cli/src/cli/eco.rs:98` | 1 |
| `E_ECO_RUNNER_READ` | 미분류 | `tools/teul-cli/src/cli/eco.rs:96` | 1 |
| `E_ECO_RUNNER_REF` | 미분류 | `tools/teul-cli/src/cli/eco.rs:514` | 5 |
| `E_ECO_RUNNER_REPORT_JSON` | 미분류 | `tools/teul-cli/src/cli/eco.rs:251` | 1 |
| `E_ECO_RUNNER_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/eco.rs:101` | 1 |
| `E_ECO_RUNNER_SHOCK` | 미분류 | `tools/teul-cli/src/cli/eco.rs:576` | 7 |
| `E_ECO_RUNNER_THRESHOLD` | 미분류 | `tools/teul-cli/src/cli/eco.rs:481` | 3 |
| `E_ECO_RUNNER_TICKS` | 미분류 | `tools/teul-cli/src/cli/eco.rs:105` | 2 |
| `E_EDU_ABS_TOL` | 미분류 | `tools/teul-cli/src/cli/edu.rs:59` | 2 |
| `E_EDU_CASE_LEN` | 미분류 | `tools/teul-cli/src/cli/edu.rs:88` | 1 |
| `E_EDU_DIV_ZERO` | 미분류 | `tools/teul-cli/src/cli/edu.rs:104` | 3 |
| `E_EDU_EMPTY` | 미분류 | `tools/teul-cli/src/cli/edu.rs:125` | 1 |
| `E_EDU_EPS` | 미분류 | `tools/teul-cli/src/cli/edu.rs:63` | 2 |
| `E_EDU_FORMULA` | 미분류 | `tools/teul-cli/src/cli/edu.rs:97` | 1 |
| `E_EDU_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/edu.rs:51` | 1 |
| `E_EDU_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/edu.rs:43` | 1 |
| `E_EDU_REL_TOL` | 미분류 | `tools/teul-cli/src/cli/edu.rs:61` | 2 |
| `E_EDU_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/edu.rs:54` | 1 |
| `E_EDU_SIM` | 미분류 | `tools/teul-cli/src/cli/edu.rs:99` | 1 |
| `E_EFFECT_IN_ISOLATED_MODE` | 미분류 | `tools/teul-cli/src/canon.rs:8187` | 2 |
| `E_EFFECT_IN_STRICT_MODE` | 미분류 | `tools/teul-cli/src/canon.rs:8185` | 2 |
| `E_EFFECT_SURFACE_ALIAS_FORBIDDEN` | 미분류 | `tools/teul-cli/src/canon.rs:2227` | 2 |
| `E_EVAL_ARTIFACT_PARSE` | 미분류 | `tools/teul-cli/src/cli/eval.rs:128` | 1 |
| `E_EVAL_ARTIFACT_READ` | 미분류 | `tools/teul-cli/src/cli/eval.rs:125` | 1 |
| `E_EVAL_ARTIFACT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/eval.rs:131` | 1 |
| `E_EVAL_CONFIG_PARSE` | 미분류 | `tools/teul-cli/src/cli/eval.rs:42` | 1 |
| `E_EVAL_CONFIG_READ` | 미분류 | `tools/teul-cli/src/cli/eval.rs:34` | 1 |
| `E_EVAL_MODEL_ACTIVATION` | 미분류 | `tools/teul-cli/src/cli/eval.rs:75` | 1 |
| `E_EVAL_MODEL_DIM` | 미분류 | `tools/teul-cli/src/cli/eval.rs:71` | 1 |
| `E_EVAL_MODEL_PARSE` | 미분류 | `tools/teul-cli/src/cli/eval.rs:64` | 1 |
| `E_EVAL_MODEL_READ` | 미분류 | `tools/teul-cli/src/cli/eval.rs:55` | 1 |
| `E_EVAL_MODEL_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/eval.rs:67` | 1 |
| `E_EVAL_MODEL_UTF8` | 미분류 | `tools/teul-cli/src/cli/eval.rs:62` | 1 |
| `E_EVAL_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/eval.rs:45` | 1 |
| `E_EVAL_SUITE` | 미분류 | `tools/teul-cli/src/cli/eval.rs:50` | 1 |
| `E_EVAL_WEIGHTS_READ` | 미분류 | `tools/teul-cli/src/cli/eval.rs:80` | 1 |
| `E_EVENT_SURFACE_ALIAS_FORBIDDEN` | 미분류 | `tools/teul-cli/src/canon.rs:1658` | 6 |
| `E_EVOLVE_BUDGET_INVALID` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:193` | 1 |
| `E_EVOLVE_CANON_FAIL` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:362` | 1 |
| `E_EVOLVE_GENERATED_WRITE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:144` | 1 |
| `E_EVOLVE_META_DIR_CREATE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:141` | 1 |
| `E_EVOLVE_META_PARSE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:179` | 1 |
| `E_EVOLVE_META_READ` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:178` | 1 |
| `E_EVOLVE_META_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:164` | 1 |
| `E_EVOLVE_META_WRITE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:167` | 1 |
| `E_EVOLVE_MUTATION_OPS_TOO_FEW` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:200` | 1 |
| `E_EVOLVE_MUTATION_OP_MISSING` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:212` | 1 |
| `E_EVOLVE_MUTATION_OP_UNKNOWN` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:308` | 1 |
| `E_EVOLVE_NO_CANDIDATE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:249` | 1 |
| `E_EVOLVE_OPERATOR` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:322` | 1 |
| `E_EVOLVE_OUT_DIR_CREATE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:98` | 2 |
| `E_EVOLVE_SPEC_CONSTANTS_EMPTY` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:187` | 2 |
| `E_EVOLVE_SPEC_PARSE` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:131` | 1 |
| `E_EVOLVE_SPEC_READ` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:127` | 1 |
| `E_EVOLVE_SPEC_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:184` | 1 |
| `E_EVOLVE_SPEC_STATEMENTS_EMPTY` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:190` | 1 |
| `E_EVOLVE_SPEC_UTF8` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:129` | 1 |
| `E_EVOLVE_TIMEOUT` | 미분류 | `tools/teul-cli/src/cli/evolve.rs:196` | 1 |
| `E_EVUNIV_CERT_PARSE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:96` | 1 |
| `E_EVUNIV_CERT_READ` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:94` | 1 |
| `E_EVUNIV_HASH_JSON` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:190` | 1 |
| `E_EVUNIV_OUT_DIR_CREATE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:40` | 1 |
| `E_EVUNIV_POLICY_PARSE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:48` | 1 |
| `E_EVUNIV_POLICY_READ` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:44` | 1 |
| `E_EVUNIV_POLICY_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:50` | 1 |
| `E_EVUNIV_POLICY_UTF8` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:46` | 1 |
| `E_EVUNIV_REPORT_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:162` | 1 |
| `E_EVUNIV_REPORT_WRITE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:166` | 1 |
| `E_EVUNIV_ROLLBACK_FAIL` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:110` | 1 |
| `E_EVUNIV_SUBJECT_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:82` | 1 |
| `E_EVUNIV_SUBJECT_WRITE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:85` | 1 |
| `E_EVUNIV_UNSAFE_RULE` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:67` | 1 |
| `E_EVUNIV_W89_PACK_NOT_FOUND` | 미분류 | `tools/teul-cli/src/cli/evolving_universe.rs:55` | 1 |
| `E_EXEC_ENUM_INVALID` | 미분류 | `tools/teul-cli/src/canon.rs:8153` | 4 |
| `E_EXEC_POLICY_DUPLICATE` | 미분류 | `tools/teul-cli/src/canon.rs:8155` | 3 |
| `E_EXPORT_BLOCK_DUPLICATE` | 파서 | `tools/teul-cli/src/lang/parser.rs:174` | 2 |
| `E_FLOW_CIRCULAR_REFERENCE` | 런타임 | `tools/teul-cli/src/runtime/error.rs:225` | 2 |
| `E_FLOW_MULTIPLE_SOURCE_CONFLICT` | 런타임 | `tools/teul-cli/src/runtime/error.rs:224` | 2 |
| `E_FORMULA_PARSE` | 런타임 | `tools/teul-cli/src/runtime/error.rs:242` | 1 |
| `E_FORMULA_UNDEFINED` | 런타임 | `tools/teul-cli/src/runtime/error.rs:243` | 1 |
| `E_FRONTDOOR` | 미분류 | `tools/teul-cli/src/cli/run.rs:175` | 2 |
| `E_FRONTDOOR_CUSTOM` | 미분류 | `tools/teul-cli/src/cli/run.rs:12056` | 2 |
| `E_FRONTDOOR_LANG_PARSER_GAP` | 미분류 | `tools/teul-cli/src/cli/frontdoor_parse.rs:71` | 7 |
| `E_FRONTDOOR_LEGACY_HEADER_FORBIDDEN` | 미분류 | `tools/teul-cli/src/canon.rs:4032` | 8 |
| `E_GAJI_JSON` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:757` | 2 |
| `E_GAJI_LOCK_FIELD` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:849` | 7 |
| `E_GAJI_LOCK_META` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:767` | 10 |
| `E_GAJI_LOCK_PACKAGES` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:843` | 3 |
| `E_GAJI_LOCK_PARSE` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:825` | 4 |
| `E_GAJI_LOCK_READ` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:823` | 2 |
| `E_GAJI_LOCK_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:832` | 3 |
| `E_GAJI_PATH` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:691` | 1 |
| `E_GAJI_READ` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:587` | 3 |
| `E_GAJI_SCAN` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:180` | 9 |
| `E_GAJI_SCAN_DEPTH` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:544` | 1 |
| `E_GAJI_TOML_VERSION` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:619` | 2 |
| `E_GAJI_VENDOR_CLEAN` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:305` | 4 |
| `E_GAJI_VENDOR_HASH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:341` | 3 |
| `E_GAJI_VENDOR_READ` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:634` | 2 |
| `E_GAJI_VENDOR_SRC` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:331` | 2 |
| `E_GAJI_VENDOR_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:307` | 8 |
| `E_GAJI_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:190` | 3 |
| `E_GATEWAY_ACCEPT` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:448` | 1 |
| `E_GATEWAY_INPUT_CONFLICT` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:72` | 1 |
| `E_GATEWAY_INPUT_FIELD` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:311` | 3 |
| `E_GATEWAY_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:214` | 6 |
| `E_GATEWAY_INPUT_PAYLOAD` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:284` | 4 |
| `E_GATEWAY_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:212` | 8 |
| `E_GATEWAY_INPUT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:229` | 2 |
| `E_GATEWAY_INVALID_PARAMS` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:106` | 1 |
| `E_GATEWAY_LISTEN` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:433` | 4 |
| `E_GATEWAY_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:91` | 2 |
| `E_GATEWAY_OVERFLOW` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:114` | 2 |
| `E_GATEWAY_REALMS` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:645` | 2 |
| `E_GATEWAY_REPORT_JSON` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:86` | 3 |
| `E_GATEWAY_SEND` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:570` | 2 |
| `E_GATEWAY_SEND_REQUIRES_LISTEN` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:77` | 1 |
| `E_GATEWAY_SEND_REQUIRES_MAX` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:81` | 1 |
| `E_GATEWAY_TIMEOUT` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:452` | 2 |
| `E_GATEWAY_WORLD_NOT_FOUND` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:63` | 1 |
| `E_GATEWAY_WORLD_READ` | 미분류 | `tools/teul-cli/src/cli/gateway.rs:65` | 1 |
| `E_GEOUL_EMPTY_LOG` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:162` | 1 |
| `E_GEOUL_ENTRY_MISSING` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:153` | 1 |
| `E_GEOUL_ENTRY_READ` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:39` | 2 |
| `E_GEOUL_ENTRY_WRITE` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:135` | 2 |
| `E_GEOUL_FINISH` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:242` | 2 |
| `E_GEOUL_FRAME_MADI_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:176` | 1 |
| `E_GEOUL_INIT` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:132` | 2 |
| `E_GEOUL_KEY_EMPTY` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:195` | 3 |
| `E_GEOUL_LEX` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:43` | 2 |
| `E_GEOUL_PARSE` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:46` | 2 |
| `E_GEOUL_RANGE` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:87` | 2 |
| `E_GEOUL_RECORD` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:227` | 1 |
| `E_GEOUL_RECORD_EMPTY` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:296` | 1 |
| `E_GEOUL_RECORD_FINISH` | 미분류 | `tools/teul-cli/src/cli/run.rs:3759` | 1 |
| `E_GEOUL_RECORD_HEADER` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:312` | 3 |
| `E_GEOUL_RECORD_HEADER_PARSE` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:301` | 1 |
| `E_GEOUL_RECORD_INIT` | 미분류 | `tools/teul-cli/src/cli/run.rs:3503` | 1 |
| `E_GEOUL_RECORD_PARSE` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:256` | 1 |
| `E_GEOUL_RECORD_READ` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:254` | 2 |
| `E_GEOUL_RECORD_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:259` | 2 |
| `E_GEOUL_RECORD_STEP` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:359` | 4 |
| `E_GEOUL_RECORD_STEP_KIND` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:366` | 1 |
| `E_GEOUL_RECORD_STEP_PARSE` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:351` | 1 |
| `E_GEOUL_RECORD_TIME` | 미분류 | `tools/teul-cli/src/cli/run.rs:3492` | 1 |
| `E_GEOUL_RUNTIME` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:65` | 2 |
| `E_GEOUL_SNAPSHOT_MADI_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:183` | 1 |
| `E_GOAP_ACTION` | 미분류 | `tools/teul-cli/src/cli/goal.rs:34` | 3 |
| `E_GOAP_ACTIONS` | 미분류 | `tools/teul-cli/src/cli/goal.rs:27` | 1 |
| `E_GOAP_INPUT` | 미분류 | `tools/teul-cli/src/cli/goap.rs:40` | 18 |
| `E_GUSEONG_INPUT_PORT_UNDECLARED` | 미분류 | `tools/teul-cli/src/canon.rs:9025` | 1 |
| `E_GUSEONG_INSTANCE_DUP` | 미분류 | `tools/teul-cli/src/canon.rs:8474` | 1 |
| `E_GUSEONG_INSTANCE_UNDECLARED` | 미분류 | `tools/teul-cli/src/canon.rs:8405` | 1 |
| `E_GUSEONG_LINK_CYCLE` | 미분류 | `tools/teul-cli/src/canon.rs:9410` | 1 |
| `E_GUSEONG_LINK_TOPLEVEL_ONLY` | 미분류 | `tools/teul-cli/src/canon.rs:8490` | 1 |
| `E_GUSEONG_OUTPUT_PORT_UNDECLARED` | 미분류 | `tools/teul-cli/src/canon.rs:9048` | 1 |
| `E_GUSEONG_PORT_DIR` | 미분류 | `tools/teul-cli/src/canon.rs:8511` | 1 |
| `E_GUSEONG_TUPLE_ACCESS_ON_SCALAR` | 미분류 | `tools/teul-cli/src/canon.rs:9105` | 1 |
| `E_GUSEONG_TUPLE_INDEX_INVALID` | 미분류 | `tools/teul-cli/src/canon.rs:9080` | 1 |
| `E_HEAL_CASE_ID_DUP` | 미분류 | `tools/teul-cli/src/cli/heal.rs:109` | 1 |
| `E_HEAL_CASE_ID_EMPTY` | 미분류 | `tools/teul-cli/src/cli/heal.rs:106` | 1 |
| `E_HEAL_INPUT_EMPTY` | 미분류 | `tools/teul-cli/src/cli/heal.rs:97` | 1 |
| `E_HEAL_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/heal.rs:89` | 1 |
| `E_HEAL_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/heal.rs:81` | 1 |
| `E_HEAL_INPUT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/heal.rs:93` | 1 |
| `E_HEAL_INPUT_UTF8` | 미분류 | `tools/teul-cli/src/cli/heal.rs:87` | 1 |
| `E_HEAL_LOOP` | 미분류 | `tools/teul-cli/src/cli/heal.rs:125` | 1 |
| `E_HEAL_NONREPLAYABLE` | 미분류 | `tools/teul-cli/src/cli/heal.rs:119` | 1 |
| `E_HEAL_NO_CHECKPOINT` | 미분류 | `tools/teul-cli/src/cli/heal.rs:113` | 1 |
| `E_HEAL_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/heal.rs:191` | 1 |
| `E_HEAL_OUT_WRITE` | 미분류 | `tools/teul-cli/src/cli/heal.rs:198` | 1 |
| `E_HEAL_REPORT_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/heal.rs:168` | 2 |
| `E_IMITATION_CONFIG_PARSE` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:38` | 1 |
| `E_IMITATION_CONFIG_READ` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:30` | 1 |
| `E_IMITATION_DIV_ZERO` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:345` | 2 |
| `E_IMITATION_EMPTY` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:61` | 2 |
| `E_IMITATION_ENV_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:68` | 1 |
| `E_IMITATION_MAX_EPOCHS` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:46` | 1 |
| `E_IMITATION_REPLAY_ENV` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:155` | 2 |
| `E_IMITATION_REPLAY_PARSE` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:145` | 1 |
| `E_IMITATION_REPLAY_READ` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:51` | 1 |
| `E_IMITATION_REPLAY_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:185` | 1 |
| `E_IMITATION_REPLAY_STEP` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:160` | 7 |
| `E_IMITATION_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/imitation.rs:41` | 1 |
| `E_IMPORT_ALIAS_DUPLICATE` | 파서 | `tools/teul-cli/src/lang/parser.rs:170` | 2 |
| `E_IMPORT_ALIAS_RESERVED` | 파서 | `tools/teul-cli/src/lang/parser.rs:171` | 2 |
| `E_IMPORT_PATH_INVALID` | 파서 | `tools/teul-cli/src/lang/parser.rs:172` | 2 |
| `E_IMPORT_VERSION_CONFLICT` | 파서 | `tools/teul-cli/src/lang/parser.rs:173` | 2 |
| `E_INFER_ACTIVATION` | 미분류 | `tools/teul-cli/src/cli/infer.rs:43` | 1 |
| `E_INFER_DIM` | 미분류 | `tools/teul-cli/src/cli/infer.rs:39` | 1 |
| `E_INFER_INPUT_LEN` | 미분류 | `tools/teul-cli/src/cli/infer.rs:61` | 1 |
| `E_INFER_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/infer.rs:53` | 1 |
| `E_INFER_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/infer.rs:51` | 1 |
| `E_INFER_INPUT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/infer.rs:56` | 1 |
| `E_INFER_MODEL_PARSE` | 미분류 | `tools/teul-cli/src/cli/infer.rs:32` | 1 |
| `E_INFER_MODEL_READ` | 미분류 | `tools/teul-cli/src/cli/infer.rs:28` | 1 |
| `E_INFER_MODEL_UTF8` | 미분류 | `tools/teul-cli/src/cli/infer.rs:30` | 1 |
| `E_INFER_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/infer.rs:35` | 1 |
| `E_INFER_WEIGHTS_COUNT` | 미분류 | `tools/teul-cli/src/cli/infer.rs:108` | 1 |
| `E_INFER_WEIGHTS_LEN` | 미분류 | `tools/teul-cli/src/cli/infer.rs:103` | 1 |
| `E_INFER_WEIGHTS_READ` | 미분류 | `tools/teul-cli/src/cli/infer.rs:48` | 1 |
| `E_INIT_STATE_FILE` | 미분류 | `tools/teul-cli/src/cli/run.rs:424` | 2 |
| `E_INIT_STATE_JSON_PARSE` | 미분류 | `tools/teul-cli/src/cli/run.rs:345` | 1 |
| `E_INIT_STATE_JSON_ROOT` | 미분류 | `tools/teul-cli/src/cli/run.rs:348` | 1 |
| `E_INIT_STATE_JSON_STATE` | 미분류 | `tools/teul-cli/src/cli/run.rs:354` | 1 |
| `E_INIT_STATE_JSON_VALUE` | 미분류 | `tools/teul-cli/src/cli/run.rs:358` | 2 |
| `E_INIT_STATE_LINE` | 미분류 | `tools/teul-cli/src/cli/run.rs:329` | 1 |
| `E_INIT_STATE_READ` | 미분류 | `tools/teul-cli/src/cli/run.rs:304` | 1 |
| `E_INPUTKEY_MISSING` | 런타임 | `tools/teul-cli/src/runtime/error.rs:261` | 2 |
| `E_INTENT_FIELD` | 미분류 | `tools/teul-cli/src/cli/intent.rs:93` | 12 |
| `E_INTENT_FIXED64` | 미분류 | `tools/teul-cli/src/cli/intent.rs:217` | 5 |
| `E_INTENT_JSON` | 미분류 | `tools/teul-cli/src/cli/intent.rs:90` | 1 |
| `E_INTENT_KIND` | 미분류 | `tools/teul-cli/src/cli/intent.rs:157` | 1 |
| `E_INTENT_MERGE` | 미분류 | `tools/teul-cli/src/main.rs:2458` | 1 |
| `E_INTENT_MISSING` | 미분류 | `tools/teul-cli/src/cli/intent.rs:20` | 1 |
| `E_INTENT_RECV_SEQ_DUPLICATE` | 미분류 | `tools/teul-cli/src/cli/intent.rs:105` | 2 |
| `E_INTENT_RECV_SEQ_REVERSE` | 미분류 | `tools/teul-cli/src/cli/intent.rs:113` | 2 |
| `E_IO_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:85` | 2 |
| `E_JJAIM_PORT_DECL_INVALID` | 미분류 | `tools/teul-cli/src/canon.rs:8921` | 3 |
| `E_JJAIM_PORT_DUP` | 미분류 | `tools/teul-cli/src/canon.rs:8937` | 3 |
| `E_JJAIM_PORT_TYPE_MISSING` | 미분류 | `tools/teul-cli/src/canon.rs:8927` | 2 |
| `E_JJAIM_SUBBLOCK_INVALID` | 미분류 | `tools/teul-cli/src/canon.rs:3912` | 1 |
| `E_JJAIM_TYPE_SCHEMA_CONFLICT` | 미분류 | `tools/teul-cli/src/canon.rs:8746` | 1 |
| `E_JJAIM_TYPE_TAG_REQUIRED` | 미분류 | `tools/teul-cli/src/canon.rs:8771` | 1 |
| `E_LANG_COMPAT_MATIC_ENTRY_DISABLED` | 파서 | `tools/teul-cli/src/lang/parser.rs:166` | 6 |
| `E_LEGACY_RANGE_SYNTAX` | 미분류 | `tools/teul-cli/src/cli/run.rs:160` | 5 |
| `E_LEX_BAD_ESCAPE` | 파서 | `tools/teul-cli/src/lang/lexer.rs:24` | 1 |
| `E_LEX_BAD_IDENT_START` | 파서 | `tools/teul-cli/src/lang/lexer.rs:25` | 1 |
| `E_LEX_UNEXPECTED_CHAR` | 파서 | `tools/teul-cli/src/lang/lexer.rs:26` | 1 |
| `E_LEX_UNTERM_ASSERTION` | 파서 | `tools/teul-cli/src/lang/lexer.rs:22` | 1 |
| `E_LEX_UNTERM_FORMULA` | 파서 | `tools/teul-cli/src/lang/lexer.rs:23` | 1 |
| `E_LEX_UNTERM_STRING` | 파서 | `tools/teul-cli/src/lang/lexer.rs:20` | 1 |
| `E_LEX_UNTERM_TEMPLATE` | 파서 | `tools/teul-cli/src/lang/lexer.rs:21` | 1 |
| `E_LINEAR_INEQUALITY_BAD_COMPARE` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14734` | 1 |
| `E_LINEAR_INEQUALITY_BAD_VAR` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14816` | 1 |
| `E_LINEAR_INEQUALITY_DIV_ZERO` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14719` | 1 |
| `E_LINEAR_INEQUALITY_NONLINEAR` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14841` | 1 |
| `E_LINT_COL` | 미분류 | `tools/teul-cli/src/cli/lint.rs:284` | 1 |
| `E_LINT_LINE` | 미분류 | `tools/teul-cli/src/cli/lint.rs:105` | 1 |
| `E_LINT_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/lint.rs:299` | 1 |
| `E_LINT_RANGE` | 미분류 | `tools/teul-cli/src/cli/lint.rs:291` | 1 |
| `E_LINT_READ` | 미분류 | `tools/teul-cli/src/cli/lint.rs:58` | 1 |
| `E_LINT_SKIP_AMBIGUOUS` | 미분류 | `tools/teul-cli/src/cli/lint.rs:121` | 1 |
| `E_LINT_SKIP_BLOCK` | 미분류 | `tools/teul-cli/src/cli/lint.rs:114` | 1 |
| `E_LINT_WRITE` | 미분류 | `tools/teul-cli/src/cli/lint.rs:151` | 1 |
| `E_MAP_DOT_KEY_MISSING` | 런타임 | `tools/teul-cli/src/runtime/error.rs:262` | 3 |
| `E_MATH_DIV_ZERO` | 런타임 | `tools/teul-cli/src/runtime/error.rs:219` | 1 |
| `E_MATH_DOMAIN` | 런타임 | `tools/teul-cli/src/runtime/error.rs:220` | 5 |
| `E_NUMERIC_DIV_ZERO` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:9797` | 1 |
| `E_NUMERIC_FACTOR_INPUT_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/numeric.rs:38` | 2 |
| `E_NUMERIC_FACTOR_JOB_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/numeric.rs:48` | 1 |
| `E_NUMERIC_FACTOR_JOB_READ` | 미분류 | `tools/teul-cli/src/cli/numeric.rs:33` | 1 |
| `E_NUMERIC_FACTOR_JOB_WRITE` | 미분류 | `tools/teul-cli/src/cli/numeric.rs:18` | 2 |
| `E_NUMERIC_FACTOR_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/numeric.rs:11` | 1 |
| `E_NUMERIC_FACTOR_RESULT_WRITE` | 미분류 | `tools/teul-cli/src/cli/numeric.rs:13` | 1 |
| `E_NUM_DIV0` | 미분류 | `tools/teul-cli/src/cli/run.rs:4937` | 1 |
| `E_NURIGYM_ACTIONS` | 미분류 | `tools/teul-cli/src/cli/nurigym.rs:354` | 3 |
| `E_NURIGYM_ACTION_INVALID` | 미분류 | `tools/teul-cli/src/cli/nurigym.rs:1467` | 1 |
| `E_NURIGYM_AGENTS` | 미분류 | `tools/teul-cli/src/cli/nurigym.rs:349` | 1 |
| `E_NURIGYM_ENV` | 미분류 | `tools/teul-cli/src/cli/nurigym.rs:247` | 3 |
| `E_NURIGYM_GRIDMAZE_LAYOUT` | 미분류 | `tools/teul-cli/src/cli/nurigym.rs:1429` | 1 |
| `E_NURIGYM_INPUT` | 미분류 | `tools/teul-cli/src/cli/nurigym.rs:197` | 1 |
| `E_NURIGYM_REWARD_WEIGHTS` | 미분류 | `tools/teul-cli/src/cli/nurigym.rs:1857` | 3 |
| `E_OPEN_BUNDLE_CONFLICT` | 미분류 | `tools/teul-cli/src/cli/run.rs:3256` | 1 |
| `E_OPEN_BUNDLE_META_JSON` | 미분류 | `tools/teul-cli/src/cli/run.rs:2817` | 1 |
| `E_OPEN_BUNDLE_META_TIME` | 미분류 | `tools/teul-cli/src/cli/run.rs:2795` | 1 |
| `E_OPEN_BUNDLE_META_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:2819` | 1 |
| `E_OPEN_BUNDLE_MODE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3262` | 1 |
| `E_OPEN_BUNDLE_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3301` | 1 |
| `E_OPEN_DENIED` | 미분류 | `tools/teul-cli/src/canon.rs:8190` | 5 |
| `E_OPEN_DIAG_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/run.rs:3316` | 1 |
| `E_OPEN_IO` | 런타임 | `tools/teul-cli/src/runtime/error.rs:257` | 1 |
| `E_OPEN_LOG_MISSING` | 런타임 | `tools/teul-cli/src/runtime/open.rs:84` | 1 |
| `E_OPEN_LOG_PARSE` | 런타임 | `tools/teul-cli/src/runtime/error.rs:255` | 2 |
| `E_OPEN_LOG_TAMPER` | 런타임 | `tools/teul-cli/src/runtime/error.rs:256` | 1 |
| `E_OPEN_POLICY` | 미분류 | `tools/teul-cli/src/cli/run.rs:3140` | 1 |
| `E_OPEN_REPLAY_MISS` | 미분류 | `tools/teul-cli/src/cli/run.rs:11291` | 4 |
| `E_OPEN_SITE_UNKNOWN` | 런타임 | `tools/teul-cli/src/runtime/error.rs:252` | 1 |
| `E_PACK` | 런타임 | `tools/teul-cli/src/runtime/error.rs:247` | 2 |
| `E_PARSE` | 미분류 | `tools/teul-cli/src/cli/run.rs:12048` | 5 |
| `E_PARSE_CALL_JOSA_AMBIGUOUS` | 파서 | `lang/src/parser.rs:6195` | 2 |
| `E_PARSE_CALL_PIN_DUPLICATE` | 파서 | `lang/src/parser.rs:6199` | 2 |
| `E_PARSE_CASE_COMPLETION_REQUIRED` | 파서 | `tools/teul-cli/src/lang/parser.rs:209` | 2 |
| `E_PARSE_CASE_ELSE_NOT_LAST` | 파서 | `tools/teul-cli/src/lang/parser.rs:210` | 2 |
| `E_PARSE_COMPAT_EQUAL_DISABLED` | 파서 | `tools/teul-cli/src/lang/parser.rs:165` | 1 |
| `E_PARSE_DEFERRED_ASSIGN_OUTSIDE_BEAT` | 파서 | `tools/teul-cli/src/lang/parser.rs:196` | 4 |
| `E_PARSE_EXPECTED_EXPR` | 파서 | `tools/teul-cli/src/lang/parser.rs:156` | 1 |
| `E_PARSE_EXPECTED_PATH` | 파서 | `tools/teul-cli/src/lang/parser.rs:157` | 1 |
| `E_PARSE_EXPECTED_RBRACE` | 파서 | `tools/teul-cli/src/lang/parser.rs:162` | 1 |
| `E_PARSE_EXPECTED_RPAREN` | 파서 | `tools/teul-cli/src/lang/parser.rs:161` | 1 |
| `E_PARSE_EXPECTED_TARGET` | 파서 | `tools/teul-cli/src/lang/parser.rs:158` | 1 |
| `E_PARSE_EXPECTED_UNIT` | 파서 | `tools/teul-cli/src/lang/parser.rs:163` | 1 |
| `E_PARSE_HOOK_EVERY_N_MADI_INTERVAL_INVALID` | 미분류 | `tools/teul-cli/src/cli/run.rs:7838` | 3 |
| `E_PARSE_HOOK_EVERY_N_MADI_SUFFIX_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/cli/run.rs:7874` | 3 |
| `E_PARSE_HOOK_EVERY_N_MADI_UNIT_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/cli/run.rs:7856` | 3 |
| `E_PARSE_IMMEDIATE_PROOF_IO_FORBIDDEN` | 파서 | `tools/teul-cli/src/lang/parser.rs:208` | 2 |
| `E_PARSE_IMMEDIATE_PROOF_MUTATION_FORBIDDEN` | 파서 | `tools/teul-cli/src/lang/parser.rs:203` | 2 |
| `E_PARSE_IMMEDIATE_PROOF_SHOW_FORBIDDEN` | 파서 | `tools/teul-cli/src/lang/parser.rs:206` | 1 |
| `E_PARSE_LIFECYCLE_NAME_DUPLICATE` | 파서 | `tools/teul-cli/src/lang/parser.rs:175` | 2 |
| `E_PARSE_MAEGIM_GROUPED_VALUE_REQUIRED` | 파서 | `tools/teul-cli/src/lang/parser.rs:178` | 2 |
| `E_PARSE_MAEGIM_NESTED_FIELD_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/cli/run.rs:7821` | 3 |
| `E_PARSE_MAEGIM_NESTED_SECTION_UNSUPPORTED` | 미분류 | `tools/teul-cli/src/cli/run.rs:7802` | 3 |
| `E_PARSE_MAEGIM_STEP_SPLIT_CONFLICT` | 미분류 | `tools/teul-cli/src/cli/run.rs:7784` | 4 |
| `E_PARSE_QUANTIFIER_IO_FORBIDDEN` | 파서 | `tools/teul-cli/src/lang/parser.rs:201` | 2 |
| `E_PARSE_QUANTIFIER_MUTATION_FORBIDDEN` | 파서 | `tools/teul-cli/src/lang/parser.rs:198` | 2 |
| `E_PARSE_QUANTIFIER_SHOW_FORBIDDEN` | 파서 | `tools/teul-cli/src/lang/parser.rs:200` | 2 |
| `E_PARSE_TENSOR_SHAPE` | 파서 | `tools/teul-cli/src/lang/parser.rs:164` | 1 |
| `E_PARSE_UNEXPECTED_TOKEN` | 파서 | `tools/teul-cli/src/lang/parser.rs:155` | 9 |
| `E_PARSE_UNSUPPORTED_COMPOUND_TARGET` | 파서 | `tools/teul-cli/src/lang/parser.rs:160` | 1 |
| `E_PATCH_ANCHOR` | 미분류 | `tools/teul-cli/src/cli/patch.rs:625` | 2 |
| `E_PATCH_APPROVAL` | 미분류 | `tools/teul-cli/src/cli/patch.rs:554` | 2 |
| `E_PATCH_APPROVE` | 미분류 | `tools/teul-cli/src/cli/patch.rs:229` | 3 |
| `E_PATCH_APPROVE_ABORT` | 미분류 | `tools/teul-cli/src/cli/patch.rs:238` | 1 |
| `E_PATCH_BEFORE_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/patch.rs:476` | 2 |
| `E_PATCH_BLOCK` | 미분류 | `tools/teul-cli/src/cli/patch.rs:640` | 1 |
| `E_PATCH_CANON_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/patch.rs:669` | 1 |
| `E_PATCH_CANON_PARSE` | 미분류 | `tools/teul-cli/src/cli/patch.rs:663` | 1 |
| `E_PATCH_COL` | 미분류 | `tools/teul-cli/src/cli/patch.rs:694` | 1 |
| `E_PATCH_JSON` | 미분류 | `tools/teul-cli/src/cli/patch.rs:365` | 17 |
| `E_PATCH_KIND` | 미분류 | `tools/teul-cli/src/cli/patch.rs:467` | 2 |
| `E_PATCH_LINE` | 미분류 | `tools/teul-cli/src/cli/patch.rs:161` | 1 |
| `E_PATCH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/patch.rs:709` | 1 |
| `E_PATCH_MODE` | 미분류 | `tools/teul-cli/src/cli/patch.rs:294` | 2 |
| `E_PATCH_PATH` | 미분류 | `tools/teul-cli/src/cli/patch.rs:284` | 1 |
| `E_PATCH_RANGE` | 미분류 | `tools/teul-cli/src/cli/patch.rs:701` | 1 |
| `E_PATCH_READ` | 미분류 | `tools/teul-cli/src/cli/patch.rs:126` | 9 |
| `E_PATCH_SKIP_AMBIGUOUS` | 미분류 | `tools/teul-cli/src/cli/patch.rs:177` | 1 |
| `E_PATCH_SKIP_BLOCK` | 미분류 | `tools/teul-cli/src/cli/patch.rs:170` | 1 |
| `E_PATCH_VERIFY` | 미분류 | `tools/teul-cli/src/cli/patch.rs:328` | 2 |
| `E_PATCH_VERIFY_FAIL` | 미분류 | `tools/teul-cli/src/cli/patch.rs:340` | 1 |
| `E_PATCH_VERIFY_TESTS` | 미분류 | `tools/teul-cli/src/cli/patch.rs:320` | 1 |
| `E_PATCH_WRITE` | 미분류 | `tools/teul-cli/src/cli/patch.rs:207` | 5 |
| `E_PRAGMA_REMOVED` | 미분류 | `tools/teul-cli/src/cli/run.rs:155` | 5 |
| `E_PROJECT_AGE_TARGET_INVALID` | 미분류 | `tools/teul-cli/src/cli/run.rs:2705` | 1 |
| `E_PROOF_AST_JSON` | 미분류 | `tools/teul-cli/src/cli/run.rs:6388` | 1 |
| `E_PROOF_CERT_FIELD_MISSING` | 미분류 | `tools/teul-cli/src/cli/run.rs:7061` | 3 |
| `E_PROOF_CERT_VERIFY_CERT_MANIFEST_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/cert.rs:141` | 1 |
| `E_PROOF_CERT_VERIFY_FIELD_MISSING` | 미분류 | `tools/teul-cli/src/cli/cert.rs:367` | 4 |
| `E_PROOF_CERT_VERIFY_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/cert.rs:124` | 1 |
| `E_PROOF_CERT_VERIFY_INPUT_UTF8` | 미분류 | `tools/teul-cli/src/cli/cert.rs:130` | 1 |
| `E_PROOF_CERT_VERIFY_PARSE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:132` | 1 |
| `E_PROOF_CERT_VERIFY_PUBKEY_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:154` | 1 |
| `E_PROOF_CERT_VERIFY_RUNTIME_ARTIFACT_CANDIDATE_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:191` | 1 |
| `E_PROOF_CERT_VERIFY_RUNTIME_ARTIFACT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/cert.rs:173` | 1 |
| `E_PROOF_CERT_VERIFY_RUNTIME_CANDIDATE_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/cert.rs:168` | 1 |
| `E_PROOF_CERT_VERIFY_RUNTIME_DIAG_COUNT_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:182` | 1 |
| `E_PROOF_CERT_VERIFY_RUNTIME_PROFILE_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:176` | 1 |
| `E_PROOF_CERT_VERIFY_RUNTIME_SUBJECT_HASH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:186` | 1 |
| `E_PROOF_CERT_VERIFY_RUNTIME_VERIFIED_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:179` | 1 |
| `E_PROOF_CERT_VERIFY_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/cert.rs:135` | 1 |
| `E_PROOF_CERT_VERIFY_SIGNATURE_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:157` | 1 |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_FIELD_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:230` | 1 |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_HASH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:205` | 1 |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_KIND_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:217` | 1 |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_PARSE` | 미분류 | `tools/teul-cli/src/cli/cert.rs:208` | 1 |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_READ` | 미분류 | `tools/teul-cli/src/cli/cert.rs:197` | 1 |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_SCHEMA_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:212` | 1 |
| `E_PROOF_CERT_VERIFY_SUBJECT_HASH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/cert.rs:151` | 1 |
| `E_PROOF_CHECK_FAILED` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:6318` | 10 |
| `E_PROOF_INCOMPLETE` | 런타임 | `tools/teul-cli/src/runtime/error.rs:251` | 2 |
| `E_PROOF_JSON` | 미분류 | `tools/teul-cli/src/cli/run.rs:6938` | 2 |
| `E_PROOF_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3666` | 4 |
| `E_REALM_INPUT` | 미분류 | `tools/teul-cli/src/cli/test.rs:34` | 2 |
| `E_REALM_OUTPUT` | 미분류 | `tools/teul-cli/src/cli/test.rs:73` | 1 |
| `E_RECEIVE_OUTSIDE_IMJA` | 파서 | `tools/teul-cli/src/lang/parser.rs:176` | 3 |
| `E_REG` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3832` | 2 |
| `E_REGEX_FLAGS_INVALID` | 런타임 | `tools/teul-cli/src/runtime/error.rs:258` | 2 |
| `E_REGEX_PATTERN_INVALID` | 런타임 | `tools/teul-cli/src/runtime/error.rs:259` | 2 |
| `E_REGEX_REPLACEMENT_INVALID` | 런타임 | `tools/teul-cli/src/runtime/error.rs:260` | 4 |
| `E_REG_` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3831` | 2 |
| `E_REG_ARCHIVE_SHA256_INVALID` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2500` | 2 |
| `E_REG_ARCHIVE_SHA256_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:893` | 7 |
| `E_REG_ARCHIVE_SHA256_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1585` | 4 |
| `E_REG_AUDIT_CHAIN_BROKEN` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1187` | 4 |
| `E_REG_AUDIT_EMPTY` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1219` | 2 |
| `E_REG_AUDIT_LAST_HASH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:470` | 7 |
| `E_REG_AUDIT_LAST_HASH_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:441` | 6 |
| `E_REG_AUDIT_PARSE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1099` | 6 |
| `E_REG_AUDIT_READ` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1084` | 3 |
| `E_REG_AUDIT_ROW_FIELD` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1112` | 4 |
| `E_REG_AUDIT_ROW_HASH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1167` | 5 |
| `E_REG_AUDIT_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1125` | 2 |
| `E_REG_AUDIT_VERIFY_LOG_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:459` | 8 |
| `E_REG_AUDIT_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3483` | 3 |
| `E_REG_AUTH_POLICY_PARSE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3331` | 8 |
| `E_REG_AUTH_POLICY_READ` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3323` | 11 |
| `E_REG_AUTH_POLICY_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3340` | 28 |
| `E_REG_AUTH_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3315` | 6 |
| `E_REG_AUTH_ROLE_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3402` | 1 |
| `E_REG_AUTH_SCOPE_FORBIDDEN` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3395` | 3 |
| `E_REG_AUTH_TOKEN_UNKNOWN` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3387` | 5 |
| `E_REG_CACHE_READ` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2344` | 1 |
| `E_REG_CACHE_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2480` | 2 |
| `E_REG_CONTRACT_MISMATCH` | 계약 | `tools/teul-cli/src/cli/gaji_registry.rs:938` | 5 |
| `E_REG_DEPENDENCIES_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:926` | 3 |
| `E_REG_DETMATH_SEAL_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:966` | 3 |
| `E_REG_DOWNLOAD_ARCHIVE_PATH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2884` | 2 |
| `E_REG_DOWNLOAD_HTTP_DISABLED` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2394` | 3 |
| `E_REG_DOWNLOAD_HTTP_FAILED` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2454` | 2 |
| `E_REG_DOWNLOAD_READ` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2378` | 1 |
| `E_REG_DOWNLOAD_UNPACK` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2820` | 2 |
| `E_REG_DOWNLOAD_URL_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:910` | 3 |
| `E_REG_DOWNLOAD_URL_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1577` | 1 |
| `E_REG_DOWNLOAD_URL_SCHEME` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2427` | 1 |
| `E_REG_DOWNLOAD_VENDOR_META` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2872` | 1 |
| `E_REG_DOWNLOAD_VENDOR_NAME` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2786` | 1 |
| `E_REG_DOWNLOAD_VENDOR_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2802` | 5 |
| `E_REG_DOWNLOAD_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1598` | 2 |
| `E_REG_FEDERATION_SOURCE_COUNT` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1471` | 2 |
| `E_REG_IMMUTABLE_EXISTS` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1731` | 8 |
| `E_REG_INDEX_FIELD` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:793` | 35 |
| `E_REG_INDEX_NOT_FOUND` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:860` | 22 |
| `E_REG_INDEX_PARSE` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:112` | 15 |
| `E_REG_INDEX_READ` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:104` | 16 |
| `E_REG_INDEX_ROOT_HASH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:998` | 8 |
| `E_REG_INDEX_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2144` | 9 |
| `E_REG_INDEX_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3290` | 2 |
| `E_REG_JSON` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1040` | 12 |
| `E_REG_LOCK_PACKAGES` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:731` | 5 |
| `E_REG_LOCK_PACKAGE_ID_INVALID` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:810` | 21 |
| `E_REG_LOCK_PARSE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:690` | 1 |
| `E_REG_LOCK_READ` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:682` | 1 |
| `E_REG_LOCK_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:702` | 3 |
| `E_REG_MIN_RUNTIME_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:952` | 3 |
| `E_REG_PUBLISH_ARCHIVE_PATH` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2681` | 2 |
| `E_REG_PUBLISH_ARCHIVE_READ` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2605` | 4 |
| `E_REG_PUBLISH_ARCHIVE_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1759` | 5 |
| `E_REG_PUBLISH_PACKAGE_DIR` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2574` | 1 |
| `E_REG_PUBLISH_PACKAGE_META` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2583` | 1 |
| `E_REG_REPORT_SOURCE_READ` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1331` | 1 |
| `E_REG_REPORT_WRITE` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:1049` | 12 |
| `E_REG_SCOPE_FORBIDDEN` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3455` | 6 |
| `E_REG_SEARCH_QUERY` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:2921` | 4 |
| `E_REG_SNAPSHOT_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:987` | 11 |
| `E_REG_SNAPSHOT_MISSING` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:147` | 18 |
| `E_REG_TRUST_ROOT_INVALID` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:1021` | 16 |
| `E_REG_UNKNOWN` | 미분류 | `tools/teul-cli/src/cli/gaji_registry.rs:3309` | 3 |
| `E_REG_VERIFY_INDEX_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:214` | 12 |
| `E_REG_YANKED_LOCKED` | 미분류 | `tools/teul-cli/src/cli/gaji.rs:314` | 11 |
| `E_REPLAY_BRANCH_AT_RANGE` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:54` | 1 |
| `E_REPLAY_BRANCH_EMPTY` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:98` | 1 |
| `E_REPLAY_BRANCH_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:234` | 1 |
| `E_REPLAY_BRANCH_RECORD_ORDER_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/replay_branch.rs:87` | 1 |
| `E_REPLAY_DIFF_MANIFEST` | 미분류 | `tools/teul-cli/src/cli/replay_diff.rs:96` | 7 |
| `E_REPLAY_DIFF_READ` | 미분류 | `tools/teul-cli/src/cli/replay_diff.rs:93` | 1 |
| `E_REPLAY_EMPTY_LOG` | 미분류 | `tools/teul-cli/src/cli/replay.rs:43` | 2 |
| `E_REPLAY_ENTRY_MISSING` | 미분류 | `tools/teul-cli/src/cli/replay.rs:35` | 2 |
| `E_REPLAY_ENTRY_READ` | 미분류 | `tools/teul-cli/src/cli/replay.rs:38` | 2 |
| `E_REPLAY_FRAME_MADI_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/replay.rs:66` | 2 |
| `E_REPLAY_LEX` | 미분류 | `tools/teul-cli/src/cli/replay.rs:89` | 2 |
| `E_REPLAY_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/replay.rs:138` | 1 |
| `E_REPLAY_PARSE` | 미분류 | `tools/teul-cli/src/cli/replay.rs:92` | 2 |
| `E_REPLAY_RUNTIME` | 미분류 | `tools/teul-cli/src/cli/replay.rs:127` | 2 |
| `E_REPLAY_SEEK_RANGE` | 미분류 | `tools/teul-cli/src/cli/replay.rs:56` | 1 |
| `E_REPLAY_SNAPSHOT_MADI_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/replay.rs:73` | 2 |
| `E_REPLAY_UNTIL_RANGE` | 미분류 | `tools/teul-cli/src/cli/replay.rs:49` | 1 |
| `E_REPRO_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3686` | 5 |
| `E_REWARD_CALL` | 미분류 | `tools/teul-cli/src/cli/reward.rs:392` | 5 |
| `E_REWARD_CALL_UNKNOWN` | 미분류 | `tools/teul-cli/src/cli/reward.rs:440` | 1 |
| `E_REWARD_DIV0` | 미분류 | `tools/teul-cli/src/cli/reward.rs:365` | 1 |
| `E_REWARD_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/reward.rs:55` | 1 |
| `E_REWARD_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/reward.rs:47` | 1 |
| `E_REWARD_LEX` | 미분류 | `tools/teul-cli/src/cli/reward.rs:632` | 1 |
| `E_REWARD_PARSE` | 미분류 | `tools/teul-cli/src/cli/reward.rs:669` | 4 |
| `E_REWARD_RESULT_TYPE` | 미분류 | `tools/teul-cli/src/cli/reward.rs:91` | 1 |
| `E_REWARD_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/reward.rs:58` | 1 |
| `E_REWARD_TYPE` | 미분류 | `tools/teul-cli/src/cli/reward.rs:343` | 4 |
| `E_REWARD_VAR` | 미분류 | `tools/teul-cli/src/cli/reward.rs:68` | 1 |
| `E_REWARD_VAR_MISSING` | 미분류 | `tools/teul-cli/src/cli/reward.rs:337` | 1 |
| `E_RUNTIME_BREAK_OUTSIDE_LOOP` | 런타임 | `tools/teul-cli/src/runtime/error.rs:248` | 2 |
| `E_RUNTIME_CONTINUE_OUTSIDE_FOREACH` | 런타임 | `tools/teul-cli/src/runtime/error.rs:249` | 3 |
| `E_RUNTIME_CONTRACT_MISMATCH` | 계약 | `tools/teul-cli/src/cli/run.rs:1771` | 2 |
| `E_RUNTIME_INVALID_PATH` | 런타임 | `tools/teul-cli/src/runtime/error.rs:217` | 1 |
| `E_RUNTIME_LIFECYCLE_CALL_TARGET_ARITY` | 런타임 | `tools/teul-cli/src/runtime/error.rs:191` | 2 |
| `E_RUNTIME_LIFECYCLE_CALL_TARGET_FAMILY_AMBIGUOUS` | 런타임 | `tools/teul-cli/src/runtime/error.rs:209` | 2 |
| `E_RUNTIME_LIFECYCLE_CALL_TARGET_FAMILY_CONFLICT` | 런타임 | `tools/teul-cli/src/runtime/error.rs:200` | 2 |
| `E_RUNTIME_LIFECYCLE_CALL_TARGET_UNKNOWN` | 런타임 | `tools/teul-cli/src/runtime/error.rs:182` | 2 |
| `E_RUNTIME_LIFECYCLE_NEXT_TARGET_ARITY` | 런타임 | `tools/teul-cli/src/runtime/error.rs:190` | 2 |
| `E_RUNTIME_LIFECYCLE_NEXT_TARGET_FAMILY_AMBIGUOUS` | 런타임 | `tools/teul-cli/src/runtime/error.rs:208` | 2 |
| `E_RUNTIME_LIFECYCLE_NEXT_TARGET_FAMILY_CONFLICT` | 런타임 | `tools/teul-cli/src/runtime/error.rs:199` | 2 |
| `E_RUNTIME_LIFECYCLE_NEXT_TARGET_UNKNOWN` | 런타임 | `tools/teul-cli/src/runtime/error.rs:181` | 2 |
| `E_RUNTIME_LIFECYCLE_START_TARGET_ARITY` | 런타임 | `tools/teul-cli/src/runtime/error.rs:189` | 2 |
| `E_RUNTIME_LIFECYCLE_START_TARGET_FAMILY_AMBIGUOUS` | 런타임 | `tools/teul-cli/src/runtime/error.rs:207` | 2 |
| `E_RUNTIME_LIFECYCLE_START_TARGET_FAMILY_CONFLICT` | 런타임 | `tools/teul-cli/src/runtime/error.rs:198` | 2 |
| `E_RUNTIME_LIFECYCLE_START_TARGET_UNKNOWN` | 런타임 | `tools/teul-cli/src/runtime/error.rs:180` | 2 |
| `E_RUNTIME_LIFECYCLE_TARGET_ARITY` | 런타임 | `tools/teul-cli/src/runtime/error.rs:192` | 1 |
| `E_RUNTIME_LIFECYCLE_TARGET_FAMILY_AMBIGUOUS` | 런타임 | `tools/teul-cli/src/runtime/error.rs:210` | 1 |
| `E_RUNTIME_LIFECYCLE_TARGET_FAMILY_CONFLICT` | 런타임 | `tools/teul-cli/src/runtime/error.rs:201` | 1 |
| `E_RUNTIME_LIFECYCLE_TARGET_UNKNOWN` | 런타임 | `tools/teul-cli/src/runtime/error.rs:183` | 1 |
| `E_RUNTIME_RETURN_OUTSIDE_SEED` | 런타임 | `tools/teul-cli/src/runtime/error.rs:250` | 1 |
| `E_RUNTIME_TYPE_MISMATCH` | 런타임 | `tools/teul-cli/src/runtime/error.rs:221` | 8 |
| `E_RUNTIME_UNDEFINED` | 런타임 | `tools/teul-cli/src/runtime/error.rs:216` | 1 |
| `E_RUN_MANIFEST_JSON` | 미분류 | `tools/teul-cli/src/cli/run.rs:5996` | 1 |
| `E_RUN_MANIFEST_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:5998` | 2 |
| `E_RUN_SUMMARY_WRITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:4008` | 2 |
| `E_SAFETY_INTENT` | 미분류 | `tools/teul-cli/src/cli/safety.rs:36` | 1 |
| `E_SAFETY_RULE` | 미분류 | `tools/teul-cli/src/cli/safety.rs:18` | 2 |
| `E_SALIM_REMOVED` | 미분류 | `tools/teul-cli/src/cli/geoul.rs:199` | 8 |
| `E_SAM_BAD_MADI_HZ` | 미분류 | `tools/teul-cli/src/cli/run.rs:954` | 2 |
| `E_SAM_DETJSON_FIELD` | 미분류 | `tools/teul-cli/src/cli/run.rs:1009` | 3 |
| `E_SAM_DETJSON_PARSE` | 미분류 | `tools/teul-cli/src/cli/run.rs:993` | 1 |
| `E_SAM_DETJSON_PAYLOAD` | 미분류 | `tools/teul-cli/src/cli/run.rs:1024` | 1 |
| `E_SAM_DETJSON_READ` | 미분류 | `tools/teul-cli/src/cli/run.rs:991` | 1 |
| `E_SAM_DETJSON_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/run.rs:1000` | 1 |
| `E_SAM_FINISH` | 미분류 | `tools/teul-cli/src/cli/run.rs:3690` | 1 |
| `E_SAM_INPUT_EOF` | 미분류 | `tools/teul-cli/src/cli/run.rs:1067` | 1 |
| `E_SAM_LIVE_BIND` | 미분류 | `tools/teul-cli/src/cli/sam_live.rs:246` | 1 |
| `E_SAM_LIVE_NONBLOCK` | 미분류 | `tools/teul-cli/src/cli/sam_live.rs:249` | 1 |
| `E_SAM_LIVE_RAW` | 미분류 | `tools/teul-cli/src/cli/sam_live.rs:164` | 1 |
| `E_SAM_MADI_HZ_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/run.rs:912` | 1 |
| `E_SAM_MADI_INFINITE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3345` | 1 |
| `E_SAM_MADI_RANGE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3374` | 1 |
| `E_SAM_MODE_CONFLICT` | 미분류 | `tools/teul-cli/src/cli/run.rs:879` | 2 |
| `E_SAM_RECORD_COUNT_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/run.rs:893` | 2 |
| `E_SAM_RECORD_MADI_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/run.rs:950` | 2 |
| `E_SAM_RECORD_ORDER_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/run.rs:931` | 1 |
| `E_SCAN_READ` | 미분류 | `tools/teul-cli/src/cli/scan.rs:10` | 2 |
| `E_SEED_NAME_CONFLICT_HA` | 파서 | `lang/src/parser.rs:4791` | 5 |
| `E_SELF_OUTSIDE_IMJA` | 런타임 | `tools/teul-cli/src/runtime/error.rs:218` | 3 |
| `E_SETTING_MADI_BAD_VALUE` | 미분류 | `tools/teul-cli/src/cli/run.rs:3124` | 2 |
| `E_SFC_IDENTITY_VIOLATION` | 미분류 | `tools/teul-cli/src/cli/eco.rs:309` | 14 |
| `E_SOCIAL_AGENTS_EMPTY` | 미분류 | `tools/teul-cli/src/cli/social.rs:129` | 1 |
| `E_SOCIAL_AGENT_DUPLICATE` | 미분류 | `tools/teul-cli/src/cli/social.rs:234` | 1 |
| `E_SOCIAL_AGENT_UNKNOWN` | 미분류 | `tools/teul-cli/src/cli/social.rs:294` | 4 |
| `E_SOCIAL_EVENT_FIELD` | 미분류 | `tools/teul-cli/src/cli/social.rs:280` | 9 |
| `E_SOCIAL_EVENT_KIND` | 미분류 | `tools/teul-cli/src/cli/social.rs:370` | 1 |
| `E_SOCIAL_EVENT_KIND_EMPTY` | 미분류 | `tools/teul-cli/src/cli/social.rs:148` | 1 |
| `E_SOCIAL_EVENT_STEP` | 미분류 | `tools/teul-cli/src/cli/social.rs:142` | 1 |
| `E_SOCIAL_EVENT_VALUE` | 미분류 | `tools/teul-cli/src/cli/social.rs:288` | 3 |
| `E_SOCIAL_EXPLOSION` | 미분류 | `tools/teul-cli/src/cli/social.rs:338` | 1 |
| `E_SOCIAL_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/social.rs:118` | 1 |
| `E_SOCIAL_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/social.rs:114` | 1 |
| `E_SOCIAL_INPUT_UTF8` | 미분류 | `tools/teul-cli/src/cli/social.rs:116` | 1 |
| `E_SOCIAL_OUT_DIR_CREATE` | 미분류 | `tools/teul-cli/src/cli/social.rs:213` | 1 |
| `E_SOCIAL_REPORT_SERIALIZE` | 미분류 | `tools/teul-cli/src/cli/social.rs:193` | 2 |
| `E_SOCIAL_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/social.rs:122` | 1 |
| `E_SOCIAL_SEED_PARSE` | 미분류 | `tools/teul-cli/src/cli/social.rs:251` | 2 |
| `E_SOCIAL_STEPS_INVALID` | 미분류 | `tools/teul-cli/src/cli/social.rs:126` | 1 |
| `E_STATE_UNDECLARED` | 파서 | `lang/src/parser.rs:4327` | 3 |
| `E_STR_INDEX_OOB` | 런타임 | `tools/teul-cli/src/runtime/error.rs:238` | 2 |
| `E_SWARM_ACTION_DUPLICATE` | 미분류 | `tools/teul-cli/src/cli/swarm.rs:105` | 1 |
| `E_SWARM_ACTION_UNKNOWN` | 미분류 | `tools/teul-cli/src/cli/swarm.rs:128` | 1 |
| `E_SWARM_AGENT_DUPLICATE` | 미분류 | `tools/teul-cli/src/cli/swarm.rs:90` | 1 |
| `E_SWARM_EMPTY` | 미분류 | `tools/teul-cli/src/cli/swarm.rs:84` | 1 |
| `E_SWARM_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/swarm.rs:51` | 1 |
| `E_SWARM_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/swarm.rs:49` | 1 |
| `E_SWARM_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/swarm.rs:54` | 1 |
| `E_SYMBOLIC_FORMULA_UNSUPPORTED` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14217` | 1 |
| `E_SYMBOLIC_PROOF_UNSUPPORTED` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:13071` | 2 |
| `E_SYMBOLIC_UNKNOWN_TRANSFORM` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:14182` | 1 |
| `E_SYMBOLIC_UNSUPPORTED_RELATION_SOLVE` | 런타임 | `tools/teul-cli/src/runtime/eval.rs:12366` | 3 |
| `E_TAG_DUPLICATE_IN_CONTEXT` | 파서 | `tools/teul-cli/src/lang/parser.rs:212` | 1 |
| `E_TEMPLATE` | 런타임 | `tools/teul-cli/src/runtime/error.rs:246` | 1 |
| `E_TENSOR_V0_CANON_JSON` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:257` | 1 |
| `E_TENSOR_V0_DENSE_DATA_LEN` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:145` | 1 |
| `E_TENSOR_V0_DENSE_DATA_TYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:142` | 1 |
| `E_TENSOR_V0_DENSE_VALUE_TYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:151` | 2 |
| `E_TENSOR_V0_DTYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:82` | 1 |
| `E_TENSOR_V0_INPUT_PARSE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:53` | 1 |
| `E_TENSOR_V0_INPUT_READ` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:51` | 1 |
| `E_TENSOR_V0_KIND` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:75` | 1 |
| `E_TENSOR_V0_OUT_DIR_CREATE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:31` | 1 |
| `E_TENSOR_V0_OUT_WRITE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:34` | 1 |
| `E_TENSOR_V0_ROOT_TYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:62` | 1 |
| `E_TENSOR_V0_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:68` | 1 |
| `E_TENSOR_V0_SHAPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:118` | 6 |
| `E_TENSOR_V0_SPARSE_DUP` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:203` | 1 |
| `E_TENSOR_V0_SPARSE_INDEX_OOB` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:190` | 1 |
| `E_TENSOR_V0_SPARSE_INDEX_RANK` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:182` | 1 |
| `E_TENSOR_V0_SPARSE_INDEX_TYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:180` | 2 |
| `E_TENSOR_V0_SPARSE_ITEMS_TYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:167` | 1 |
| `E_TENSOR_V0_SPARSE_ITEM_TYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:174` | 2 |
| `E_TENSOR_V0_SPARSE_ORDER` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:206` | 1 |
| `E_TENSOR_V0_SPARSE_VALUE_TYPE` | 미분류 | `tools/teul-cli/src/cli/tensor.rs:197` | 2 |
| `E_TEST_CWD` | 미분류 | `tools/teul-cli/src/cli/test.rs:98` | 1 |
| `E_TEST_FILE_CONFLICT` | 미분류 | `tools/teul-cli/src/main.rs:1964` | 1 |
| `E_TEST_FILE_REQUIRED` | 미분류 | `tools/teul-cli/src/main.rs:2001` | 1 |
| `E_TEST_GOLDEN_OPTION` | 미분류 | `tools/teul-cli/src/main.rs:1984` | 1 |
| `E_TEST_MODE_CONFLICT` | 미분류 | `tools/teul-cli/src/main.rs:1959` | 1 |
| `E_TEST_OPTION_INVALID` | 미분류 | `tools/teul-cli/src/main.rs:2006` | 1 |
| `E_TEST_RUNNER_FAILED` | 미분류 | `tools/teul-cli/src/cli/test.rs:132` | 1 |
| `E_TEST_RUNNER_MISSING` | 미분류 | `tools/teul-cli/src/cli/test.rs:119` | 1 |
| `E_TEST_RUNNER_SPAWN` | 미분류 | `tools/teul-cli/src/cli/test.rs:129` | 1 |
| `E_TEST_SMOKE_OPTION` | 미분류 | `tools/teul-cli/src/main.rs:1969` | 1 |
| `E_TEST_WORKSPACE_ROOT` | 미분류 | `tools/teul-cli/src/cli/test.rs:113` | 1 |
| `E_TIMELINE_JSON` | 미분류 | `tools/teul-cli/src/cli/timeline.rs:47` | 1 |
| `E_TRACE_TIER_MISMATCH` | 미분류 | `tools/teul-cli/src/cli/run.rs:3244` | 1 |
| `E_TRACE_TIER_REQUIRED` | 미분류 | `tools/teul-cli/src/cli/run.rs:3237` | 1 |
| `E_TRAIN_CONFIG_PARSE` | 미분류 | `tools/teul-cli/src/cli/train.rs:34` | 1 |
| `E_TRAIN_CONFIG_READ` | 미분류 | `tools/teul-cli/src/cli/train.rs:32` | 1 |
| `E_TRAIN_CONFIG_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/train.rs:43` | 1 |
| `E_TRAIN_MAX_EPOCHS` | 미분류 | `tools/teul-cli/src/cli/train.rs:51` | 1 |
| `E_TRAIN_SCHEMA` | 미분류 | `tools/teul-cli/src/cli/train.rs:46` | 1 |
| `E_TRAIN_THRESHOLD` | 미분류 | `tools/teul-cli/src/cli/train.rs:105` | 1 |
| `E_UNDECLARED_GLOBAL_WRITE` | 파서 | `tools/teul-cli/src/lang/parser.rs:159` | 1 |
| `E_UNIT_MISMATCH` | 런타임 | `tools/teul-cli/src/runtime/error.rs:240` | 1 |
| `E_UNIT_UNKNOWN` | 런타임 | `tools/teul-cli/src/runtime/error.rs:241` | 1 |
| `E_UNIVERSE_HASH_READ` | 미분류 | `tools/teul-cli/src/cli/universe.rs:213` | 1 |
| `E_UNIVERSE_PACK_INPUT_DIR` | 미분류 | `tools/teul-cli/src/cli/universe.rs:11` | 1 |
| `E_UNIVERSE_PACK_OUT_CREATE` | 미분류 | `tools/teul-cli/src/cli/universe.rs:28` | 1 |
| `E_UNIVERSE_PACK_OUT_DIR` | 미분류 | `tools/teul-cli/src/cli/universe.rs:18` | 1 |
| `E_UNIVERSE_PACK_PATH_INVALID` | 미분류 | `tools/teul-cli/src/cli/universe.rs:182` | 1 |
| `E_UNIVERSE_PACK_READ` | 미분류 | `tools/teul-cli/src/cli/universe.rs:44` | 1 |
| `E_UNIVERSE_PACK_READ_DIR` | 미분류 | `tools/teul-cli/src/cli/universe.rs:150` | 2 |
| `E_UNIVERSE_PACK_REL_PATH` | 미분류 | `tools/teul-cli/src/cli/universe.rs:161` | 1 |
| `E_UNIVERSE_PACK_ZIP_FINISH` | 미분류 | `tools/teul-cli/src/cli/universe.rs:55` | 1 |
| `E_UNIVERSE_PACK_ZIP_WRITE` | 미분류 | `tools/teul-cli/src/cli/universe.rs:50` | 2 |
| `E_UNIVERSE_UNPACK_COPY` | 미분류 | `tools/teul-cli/src/cli/universe.rs:134` | 1 |
| `E_UNIVERSE_UNPACK_INPUT_FILE` | 미분류 | `tools/teul-cli/src/cli/universe.rs:67` | 1 |
| `E_UNIVERSE_UNPACK_INPUT_OPEN` | 미분류 | `tools/teul-cli/src/cli/universe.rs:97` | 1 |
| `E_UNIVERSE_UNPACK_OUT_CREATE` | 미분류 | `tools/teul-cli/src/cli/universe.rs:88` | 1 |
| `E_UNIVERSE_UNPACK_OUT_FILE` | 미분류 | `tools/teul-cli/src/cli/universe.rs:127` | 1 |
| `E_UNIVERSE_UNPACK_OUT_NOT_EMPTY` | 미분류 | `tools/teul-cli/src/cli/universe.rs:81` | 1 |
| `E_UNIVERSE_UNPACK_OUT_PARENT` | 미분류 | `tools/teul-cli/src/cli/universe.rs:119` | 1 |
| `E_UNIVERSE_UNPACK_OUT_READ` | 미분류 | `tools/teul-cli/src/cli/universe.rs:74` | 1 |
| `E_UNIVERSE_UNPACK_PATH_INVALID` | 미분류 | `tools/teul-cli/src/cli/universe.rs:197` | 1 |
| `E_UNIVERSE_UNPACK_ZIP_ENTRY` | 미분류 | `tools/teul-cli/src/cli/universe.rs:109` | 1 |
| `E_UNIVERSE_UNPACK_ZIP_OPEN` | 미분류 | `tools/teul-cli/src/cli/universe.rs:103` | 1 |
| `E_WARP_INPUT` | 미분류 | `tools/teul-cli/src/cli/warp.rs:48` | 1 |
| `E_WARP_OUTPUT` | 미분류 | `tools/teul-cli/src/cli/warp.rs:73` | 1 |
| `E_WORKSHOP_MISSING` | 미분류 | `tools/teul-cli/src/cli/workshop.rs:32` | 1 |

## 미분류 목록

미분류는 SSOT 분류 확정 전까지 의미를 임의 배정하지 않은 코드이다.

| 코드 | 정의 위치 |
|---|---|
| `E_ALRIM_JSON` | `tools/teul-cli/src/cli/alrim.rs:577` |
| `E_ALRIM_PARSE` | `tools/teul-cli/src/cli/alrim.rs:268` |
| `E_ALRIM_READ` | `tools/teul-cli/src/cli/alrim.rs:45` |
| `E_ALRIM_SCAN` | `tools/teul-cli/src/cli/alrim.rs:134` |
| `E_ALRIM_VARIANT_CONFLICT` | `tools/teul-cli/src/cli/alrim.rs:66` |
| `E_ALRIM_WRITE` | `tools/teul-cli/src/cli/alrim.rs:118` |
| `E_ASSET_MANIFEST` | `tools/teul-cli/src/main.rs:2093` |
| `E_BATANG_PREFIX_REMOVED` | `tools/teul-cli/src/cli/run.rs:143` |
| `E_BDL1_PACKET_INVALID` | `tools/teul-cli/src/core/bdl_packet.rs:22` |
| `E_BDL1_PACKET_TOO_LARGE` | `tools/teul-cli/src/core/bdl_packet.rs:21` |
| `E_BDL2_CMD_KIND` | `tools/teul-cli/src/core/bogae.rs:2277` |
| `E_BDL2_FIXED_Q` | `tools/teul-cli/src/core/bogae.rs:2083` |
| `E_BDL2_FLAGS` | `tools/teul-cli/src/core/bogae.rs:2090` |
| `E_BDL2_MAGIC` | `tools/teul-cli/src/core/bogae.rs:2067` |
| `E_BDL2_TRAILING` | `tools/teul-cli/src/core/bogae.rs:2286` |
| `E_BDL2_TRUNCATED` | `tools/teul-cli/src/core/bogae.rs:2747` |
| `E_BDL2_UTF8` | `tools/teul-cli/src/core/bogae.rs:2828` |
| `E_BDL2_VERSION` | `tools/teul-cli/src/core/bogae.rs:2074` |
| `E_BLOCK_HEADER_COLON_FORBIDDEN` | `tools/teul-cli/src/canon.rs:2191` |
| `E_BOGAE_BAD_FIELD_TYPE` | `tools/teul-cli/src/core/bogae.rs:276` |
| `E_BOGAE_BUNDLE` | `tools/teul-cli/src/main.rs:2131` |
| `E_BOGAE_CHANNEL_TYPE_INVALID` | `tools/teul-cli/src/core/bogae.rs:280` |
| `E_BOGAE_CMD_CAP` | `tools/teul-cli/src/cli/run.rs:5820` |
| `E_BOGAE_CODEC_MISMATCH` | `tools/teul-cli/src/cli/view.rs:29` |
| `E_BOGAE_COLOR_INVALID` | `tools/teul-cli/src/core/bogae.rs:283` |
| `E_BOGAE_COLOR_PACK_LOAD` | `tools/teul-cli/src/core/bogae.rs:281` |
| `E_BOGAE_COLOR_PACK_MISSING` | `tools/teul-cli/src/core/bogae.rs:282` |
| `E_BOGAE_COLOR_UNKNOWN` | `tools/teul-cli/src/core/bogae.rs:284` |
| `E_BOGAE_DETBIN_PARSE` | `tools/teul-cli/src/core/bogae.rs:285` |
| `E_BOGAE_EDIT` | `tools/teul-cli/src/main.rs:2114` |
| `E_BOGAE_ITEM_FIELD_MISSING` | `tools/teul-cli/src/core/bogae.rs:279` |
| `E_BOGAE_ITEM_KIND_INVALID` | `tools/teul-cli/src/core/bogae.rs:278` |
| `E_BOGAE_LIVE_MODE` | `tools/teul-cli/src/cli/run.rs:3330` |
| `E_BOGAE_MISSING_FIELD` | `tools/teul-cli/src/core/bogae.rs:277` |
| `E_BOGAE_NON_INT_PIXEL` | `tools/teul-cli/src/core/bogae.rs:275` |
| `E_BOGAE_PLAYBACK_INFINITE` | `tools/teul-cli/src/cli/run.rs:3383` |
| `E_BUNDLE_ARTIFACT_HASH` | `tools/teul-cli/src/cli/seulgi_bundle.rs:97` |
| `E_BUNDLE_ARTIFACT_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:92` |
| `E_BUNDLE_CERT_MARK` | `tools/teul-cli/src/cli/seulgi_bundle.rs:222` |
| `E_BUNDLE_EVAL_REPORT_HASH` | `tools/teul-cli/src/cli/seulgi_bundle.rs:116` |
| `E_BUNDLE_EVAL_REPORT_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:107` |
| `E_BUNDLE_HASH_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:283` |
| `E_BUNDLE_INPUT_EMPTY` | `tools/teul-cli/src/cli/seulgi_bundle.rs:133` |
| `E_BUNDLE_INPUT_LEN` | `tools/teul-cli/src/cli/seulgi_bundle.rs:141` |
| `E_BUNDLE_INPUT_PARSE` | `tools/teul-cli/src/cli/seulgi_bundle.rs:126` |
| `E_BUNDLE_INPUT_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:124` |
| `E_BUNDLE_INPUT_SCHEMA` | `tools/teul-cli/src/cli/seulgi_bundle.rs:129` |
| `E_BUNDLE_MANIFEST_FIELDS` | `tools/teul-cli/src/cli/seulgi_bundle.rs:218` |
| `E_BUNDLE_MANIFEST_PARSE` | `tools/teul-cli/src/cli/seulgi_bundle.rs:190` |
| `E_BUNDLE_MANIFEST_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:188` |
| `E_BUNDLE_MANIFEST_SCHEMA` | `tools/teul-cli/src/cli/seulgi_bundle.rs:193` |
| `E_BUNDLE_MANIFEST_SOURCE_HASH` | `tools/teul-cli/src/cli/seulgi_bundle.rs:262` |
| `E_BUNDLE_MANIFEST_SOURCE_PROVENANCE` | `tools/teul-cli/src/cli/seulgi_bundle.rs:273` |
| `E_BUNDLE_MODEL_ACTIVATION` | `tools/teul-cli/src/cli/seulgi_bundle.rs:68` |
| `E_BUNDLE_MODEL_DIM` | `tools/teul-cli/src/cli/seulgi_bundle.rs:64` |
| `E_BUNDLE_MODEL_HASH` | `tools/teul-cli/src/cli/seulgi_bundle.rs:83` |
| `E_BUNDLE_MODEL_PARSE` | `tools/teul-cli/src/cli/seulgi_bundle.rs:57` |
| `E_BUNDLE_MODEL_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:53` |
| `E_BUNDLE_MODEL_SCHEMA` | `tools/teul-cli/src/cli/seulgi_bundle.rs:60` |
| `E_BUNDLE_MODEL_UTF8` | `tools/teul-cli/src/cli/seulgi_bundle.rs:55` |
| `E_BUNDLE_WASM_HASH` | `tools/teul-cli/src/cli/seulgi_bundle.rs:157` |
| `E_BUNDLE_WASM_HASH_EMPTY` | `tools/teul-cli/src/cli/seulgi_bundle.rs:386` |
| `E_BUNDLE_WASM_HASH_FORMAT` | `tools/teul-cli/src/cli/seulgi_bundle.rs:390` |
| `E_BUNDLE_WASM_HASH_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:367` |
| `E_BUNDLE_WEIGHTS_COUNT` | `tools/teul-cli/src/cli/seulgi_bundle.rs:412` |
| `E_BUNDLE_WEIGHTS_LEN` | `tools/teul-cli/src/cli/seulgi_bundle.rs:407` |
| `E_BUNDLE_WEIGHTS_READ` | `tools/teul-cli/src/cli/seulgi_bundle.rs:77` |
| `E_CACHE_UNAVAILABLE_OFFLINE` | `tools/teul-cli/src/cli/gaji_registry.rs:2366` |
| `E_CALL_TAIL_MISSING_AFTER_ARGS` | `lang/src/canonicalizer.rs:709` |
| `E_CALL_TAIL_MISSING_STMT` | `lang/src/canonicalizer.rs:575` |
| `E_CANON_ALRIM_EVENT_JSON` | `tools/teul-cli/src/canon.rs:6078` |
| `E_CANON_ALRIM_PLAN_JSON` | `tools/teul-cli/src/canon.rs:5898` |
| `E_CANON_BAD_ALIAS` | `tools/teul-cli/src/canon.rs:2923` |
| `E_CANON_BAD_ATOM` | `tools/teul-cli/src/canon.rs:628` |
| `E_CANON_BAD_BLOCK` | `tools/teul-cli/src/canon.rs:787` |
| `E_CANON_BAD_CHAR` | `tools/teul-cli/src/canon.rs:529` |
| `E_CANON_BAD_ESCAPE` | `tools/teul-cli/src/canon.rs:740` |
| `E_CANON_BAD_MAEGIM` | `tools/teul-cli/src/canon.rs:1942` |
| `E_CANON_BAD_NUMBER` | `tools/teul-cli/src/canon.rs:618` |
| `E_CANON_BAD_STRING` | `tools/teul-cli/src/canon.rs:661` |
| `E_CANON_BLOCK_EDITOR_PLAN_JSON` | `tools/teul-cli/src/canon.rs:6131` |
| `E_CANON_CHECK_MISMATCH` | `tools/teul-cli/src/cli/canon.rs:107` |
| `E_CANON_CHOOSE_NEEDS_ELSE` | `tools/teul-cli/src/canon.rs:3315` |
| `E_CANON_DECL_HEADER_ONLY_CHAEVI` | `tools/teul-cli/src/canon.rs:1819` |
| `E_CANON_EXEC_POLICY_MAP_JSON` | `tools/teul-cli/src/canon.rs:5913` |
| `E_CANON_EXPECTED_ATOM` | `tools/teul-cli/src/canon.rs:2800` |
| `E_CANON_EXPECTED_EQUALS` | `tools/teul-cli/src/canon.rs:3017` |
| `E_CANON_EXPECTED_EXPR` | `tools/teul-cli/src/canon.rs:2770` |
| `E_CANON_EXPECTED_FORMULA` | `tools/teul-cli/src/canon.rs:2810` |
| `E_CANON_EXPECTED_IDENT` | `tools/teul-cli/src/canon.rs:3787` |
| `E_CANON_EXPECTED_ILTTTAE` | `tools/teul-cli/src/canon.rs:1456` |
| `E_CANON_EXPECTED_LBRACE` | `tools/teul-cli/src/canon.rs:2234` |
| `E_CANON_EXPECTED_LITERAL` | `tools/teul-cli/src/canon.rs:3138` |
| `E_CANON_EXPECTED_RBRACE` | `tools/teul-cli/src/canon.rs:1840` |
| `E_CANON_EXPECTED_SEED_PARAM` | `tools/teul-cli/src/canon.rs:2846` |
| `E_CANON_EXPECTED_STRING` | `tools/teul-cli/src/canon.rs:2410` |
| `E_CANON_EXPECTED_TARGET` | `tools/teul-cli/src/canon.rs:1561` |
| `E_CANON_EXPECTED_TERMINATOR` | `tools/teul-cli/src/canon.rs:2017` |
| `E_CANON_EXPECTED_THUNK_CONDITION` | `tools/teul-cli/src/canon.rs:3500` |
| `E_CANON_EXPECTED_THUNK_SUFFIX` | `tools/teul-cli/src/canon.rs:3360` |
| `E_CANON_FIXIT_INPLACE` | `tools/teul-cli/src/cli/canon.rs:319` |
| `E_CANON_GUSEONG_FLATTEN_JSON` | `tools/teul-cli/src/canon.rs:6041` |
| `E_CANON_GUSEONG_FLAT_JSON` | `tools/teul-cli/src/canon.rs:5883` |
| `E_CANON_HOOK_EVERY_N_MADI_INTERVAL_INVALID` | `tools/teul-cli/src/canon.rs:2140` |
| `E_CANON_HOOK_EVERY_N_MADI_SUFFIX_UNSUPPORTED` | `tools/teul-cli/src/canon.rs:2168` |
| `E_CANON_HOOK_EVERY_N_MADI_UNIT_UNSUPPORTED` | `tools/teul-cli/src/canon.rs:2148` |
| `E_CANON_HOOK_SUFFIX` | `tools/teul-cli/src/canon.rs:2182` |
| `E_CANON_MAEGIM_CONTROL_JSON` | `tools/teul-cli/src/canon.rs:6901` |
| `E_CANON_MAEGIM_CONTROL_PLAN_JSON` | `tools/teul-cli/src/canon.rs:5987` |
| `E_CANON_MAEGIM_GROUPED_VALUE_REQUIRED` | `tools/teul-cli/src/canon.rs:1908` |
| `E_CANON_MAEGIM_NESTED_FIELD_UNSUPPORTED` | `tools/teul-cli/src/canon.rs:1988` |
| `E_CANON_MAEGIM_NESTED_SECTION_UNSUPPORTED` | `tools/teul-cli/src/canon.rs:1967` |
| `E_CANON_MAEGIM_STEP_SPLIT_CONFLICT` | `tools/teul-cli/src/canon.rs:2002` |
| `E_CANON_OPEN_BLOCK` | `tools/teul-cli/src/canon.rs:2221` |
| `E_CANON_PROMPT_ELSE` | `tools/teul-cli/src/canon.rs:3388` |
| `E_CANON_RECEIVE_OUTSIDE_IMJA` | `tools/teul-cli/src/canon.rs:1725` |
| `E_CANON_ROOT_HIDE_UNDECLARED` | `tools/teul-cli/src/canon.rs:4311` |
| `E_CANON_TENSOR_SHAPE` | `tools/teul-cli/src/canon.rs:3055` |
| `E_CANON_TUPLE_INDEX_INVALID` | `tools/teul-cli/src/canon.rs:3570` |
| `E_CANON_UNEXPECTED_TOKEN` | `tools/teul-cli/src/canon.rs:1319` |
| `E_CANON_UNSUPPORTED_COMPOUND_TARGET` | `tools/teul-cli/src/canon.rs:1535` |
| `E_CANON_UNSUPPORTED_COMPOUND_UPDATE` | `tools/teul-cli/src/canon.rs:1506` |
| `E_CANON_UNTERM_BLOCK` | `tools/teul-cli/src/canon.rs:815` |
| `E_CANON_UNTERM_STRING` | `tools/teul-cli/src/canon.rs:691` |
| `E_CERT_CANON_BYTES_DRIFT` | `tools/teul-cli/src/cli/cert.rs:395` |
| `E_CERT_JSON_SERIALIZE` | `tools/teul-cli/src/cli/cert.rs:100` |
| `E_CERT_KEYGEN_OUT_DIR` | `tools/teul-cli/src/cli/cert.rs:44` |
| `E_CERT_KEY_ALGO` | `tools/teul-cli/src/cli/cert.rs:296` |
| `E_CERT_KEY_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:312` |
| `E_CERT_KEY_PARSE` | `tools/teul-cli/src/cli/cert.rs:291` |
| `E_CERT_KEY_READ` | `tools/teul-cli/src/cli/cert.rs:289` |
| `E_CERT_KEY_SCHEMA` | `tools/teul-cli/src/cli/cert.rs:293` |
| `E_CERT_OUT_DIR` | `tools/teul-cli/src/cli/cert.rs:447` |
| `E_CERT_OUT_WRITE` | `tools/teul-cli/src/cli/cert.rs:456` |
| `E_CERT_SIGN_INPUT_READ` | `tools/teul-cli/src/cli/cert.rs:80` |
| `E_CERT_VERIFY_ALGO` | `tools/teul-cli/src/cli/cert.rs:337` |
| `E_CERT_VERIFY_FAIL` | `tools/teul-cli/src/cli/cert.rs:355` |
| `E_CERT_VERIFY_INPUT_READ` | `tools/teul-cli/src/cli/cert.rs:106` |
| `E_CERT_VERIFY_PARSE` | `tools/teul-cli/src/cli/cert.rs:112` |
| `E_CERT_VERIFY_PUBKEY_FORMAT` | `tools/teul-cli/src/cli/cert.rs:340` |
| `E_CERT_VERIFY_PUBKEY_PARSE` | `tools/teul-cli/src/cli/cert.rs:347` |
| `E_CERT_VERIFY_SCHEMA` | `tools/teul-cli/src/cli/cert.rs:334` |
| `E_CERT_VERIFY_SIGNATURE_FORMAT` | `tools/teul-cli/src/cli/cert.rs:344` |
| `E_CERT_VERIFY_SIGNATURE_PARSE` | `tools/teul-cli/src/cli/cert.rs:350` |
| `E_CHAEBI_IN_LOOP` | `tools/teul-cli/src/canon.rs:1826` |
| `E_CHECK_DUPLICATE_SYMBOL` | `tools/teul-cli/src/cli/check.rs:73` |
| `E_CHECK_TYPE_MISMATCH` | `tools/teul-cli/src/cli/check.rs:67` |
| `E_CLI_AGE_TARGET` | `tools/teul-cli/src/cli/run.rs:1813` |
| `E_CLI_ARTIFACT` | `tools/teul-cli/src/main.rs:1523` |
| `E_CLI_BAD_PATH` | `tools/teul-cli/src/cli/canon.rs:418` |
| `E_CLI_BAD_SEED` | `tools/teul-cli/src/main.rs:1504` |
| `E_CLI_BOGAE_CMD_POLICY` | `tools/teul-cli/src/main.rs:1528` |
| `E_CLI_BOGAE_OVERLAY` | `tools/teul-cli/src/main.rs:1565` |
| `E_CLI_CANON` | `tools/teul-cli/src/cli/canon.rs:220` |
| `E_CLI_COMPAT_RELEASE_BLOCKED` | `tools/teul-cli/src/main.rs:1637` |
| `E_CLI_CONSOLE_GRID` | `tools/teul-cli/src/main.rs:1508` |
| `E_CLI_CONSOLE_PANEL` | `tools/teul-cli/src/main.rs:1510` |
| `E_CLI_MADI` | `tools/teul-cli/src/main.rs:1506` |
| `E_CLI_MISSING_OUT` | `tools/teul-cli/src/cli/canon.rs:413` |
| `E_CLI_READ` | `tools/teul-cli/src/cli/canon.rs:74` |
| `E_CLI_WRITE` | `tools/teul-cli/src/cli/canon.rs:351` |
| `E_CODE` | `tools/teul-cli/src/cli/diag.rs:23` |
| `E_CURRENTLINE_BRACE_MATCH` | `lang/src/currentline.rs:763` |
| `E_CURRENTLINE_CELL_READ` | `tools/teul-cli/src/main.rs:1756` |
| `E_CURRENTLINE_COMPILED_WRITE` | `tools/teul-cli/src/main.rs:1794` |
| `E_CURRENTLINE_CONTEXT_JSON` | `lang/src/currentline.rs:105` |
| `E_CURRENTLINE_CONTEXT_OUT_DIR` | `tools/teul-cli/src/main.rs:1861` |
| `E_CURRENTLINE_CONTEXT_READ` | `tools/teul-cli/src/main.rs:1768` |
| `E_CURRENTLINE_CONTEXT_WRITE` | `tools/teul-cli/src/main.rs:1871` |
| `E_CURRENTLINE_IMJA_BLOCK` | `lang/src/currentline.rs:709` |
| `E_DATASET_EMPTY` | `tools/teul-cli/src/cli/dataset.rs:48` |
| `E_DATASET_FORMAT` | `tools/teul-cli/src/cli/dataset.rs:20` |
| `E_DATASET_GEOUL_MANIFEST_AUDIT_HASH` | `tools/teul-cli/src/cli/dataset.rs:359` |
| `E_DATASET_GEOUL_MANIFEST_JSON` | `tools/teul-cli/src/cli/dataset.rs:342` |
| `E_DATASET_GEOUL_MANIFEST_READ` | `tools/teul-cli/src/cli/dataset.rs:335` |
| `E_DATASET_GEOUL_MANIFEST_SCHEMA` | `tools/teul-cli/src/cli/dataset.rs:349` |
| `E_DET_TIER_REQUIRED` | `tools/teul-cli/src/cli/run.rs:3224` |
| `E_DIAG_REPORT_WRITE` | `tools/teul-cli/src/cli/run.rs:3718` |
| `E_DIAG_WRITE` | `tools/teul-cli/src/cli/run.rs:3295` |
| `E_DOCSET_GOLDEN_EMPTY` | `tools/teul-cli/src/cli/docset.rs:126` |
| `E_DOCSET_GOLDEN_READ` | `tools/teul-cli/src/cli/docset.rs:119` |
| `E_DOCSET_HASH_READ` | `tools/teul-cli/src/cli/docset.rs:256` |
| `E_DOCSET_META_JSON` | `tools/teul-cli/src/cli/docset.rs:231` |
| `E_DOCSET_NONDETERMINISM` | `tools/teul-cli/src/cli/docset.rs:135` |
| `E_DOCSET_OUT_DIR` | `tools/teul-cli/src/cli/docset.rs:189` |
| `E_DOCSET_SOURCE_PROVENANCE_JSON` | `tools/teul-cli/src/cli/docset.rs:221` |
| `E_DOCSET_SOURCE_READ` | `tools/teul-cli/src/cli/docset.rs:200` |
| `E_DOCSET_WRITE` | `tools/teul-cli/src/cli/docset.rs:343` |
| `E_DOCTEST_FAIL` | `tools/teul-cli/src/cli/docset.rs:166` |
| `E_DOCTEST_MANIFEST_PARSE` | `tools/teul-cli/src/cli/docset.rs:149` |
| `E_DOCTEST_MANIFEST_READ` | `tools/teul-cli/src/cli/docset.rs:143` |
| `E_DOCTEST_MANIFEST_SCHEMA` | `tools/teul-cli/src/cli/docset.rs:151` |
| `E_DOCTEST_SOURCE_READ` | `tools/teul-cli/src/cli/docset.rs:164` |
| `E_DOTBOGI_AFTER_STATE_SERIALIZE` | `tools/teul-cli/src/cli/dotbogi.rs:140` |
| `E_DOTBOGI_CANON_JSON` | `tools/teul-cli/src/cli/dotbogi.rs:177` |
| `E_DOTBOGI_CASE_DOTBOGI` | `tools/teul-cli/src/cli/dotbogi.rs:42` |
| `E_DOTBOGI_CASE_EVENTS` | `tools/teul-cli/src/cli/dotbogi.rs:55` |
| `E_DOTBOGI_CASE_INPUT` | `tools/teul-cli/src/cli/dotbogi.rs:32` |
| `E_DOTBOGI_CASE_INPUT_SCHEMA` | `tools/teul-cli/src/cli/dotbogi.rs:35` |
| `E_DOTBOGI_CASE_PARSE` | `tools/teul-cli/src/cli/dotbogi.rs:21` |
| `E_DOTBOGI_CASE_READ` | `tools/teul-cli/src/cli/dotbogi.rs:17` |
| `E_DOTBOGI_CASE_ROUNDTRIP` | `tools/teul-cli/src/cli/dotbogi.rs:210` |
| `E_DOTBOGI_CASE_SCHEMA` | `tools/teul-cli/src/cli/dotbogi.rs:24` |
| `E_DOTBOGI_CASE_STATE` | `tools/teul-cli/src/cli/dotbogi.rs:119` |
| `E_DOTBOGI_CASE_UTF8` | `tools/teul-cli/src/cli/dotbogi.rs:19` |
| `E_DOTBOGI_CASE_VIEW_META` | `tools/teul-cli/src/cli/dotbogi.rs:48` |
| `E_DOTBOGI_OUTPUT_SERIALIZE` | `tools/teul-cli/src/cli/dotbogi.rs:135` |
| `E_DOTBOGI_REPORT_SERIALIZE` | `tools/teul-cli/src/cli/dotbogi.rs:145` |
| `E_DOTBOGI_STATE_WRITE_FORBIDDEN` | `tools/teul-cli/src/cli/dotbogi.rs:59` |
| `E_DULTRA_REPLAY_SEED` | `tools/teul-cli/src/cli/dultra_replay.rs:23` |
| `E_DULTRA_REPLAY_SEED_SERIALIZE` | `tools/teul-cli/src/cli/dultra_replay.rs:95` |
| `E_ECO_ABM_SPATIAL` | `tools/teul-cli/src/cli/eco.rs:337` |
| `E_ECO_ABM_SPATIAL_DIR` | `tools/teul-cli/src/cli/eco.rs:394` |
| `E_ECO_ABM_SPATIAL_JSON` | `tools/teul-cli/src/cli/eco.rs:400` |
| `E_ECO_ABM_SPATIAL_READ` | `tools/teul-cli/src/cli/eco.rs:340` |
| `E_ECO_ABM_SPATIAL_SEED` | `tools/teul-cli/src/main.rs:2207` |
| `E_ECO_DIVERGENCE_DETECTED` | `tools/teul-cli/src/cli/eco.rs:566` |
| `E_ECO_MODEL_EXEC` | `tools/teul-cli/src/cli/eco.rs:457` |
| `E_ECO_NETWORK_FLOW` | `tools/teul-cli/src/cli/eco.rs:268` |
| `E_ECO_NETWORK_FLOW_DIR` | `tools/teul-cli/src/cli/eco.rs:313` |
| `E_ECO_NETWORK_FLOW_JSON` | `tools/teul-cli/src/cli/eco.rs:319` |
| `E_ECO_NETWORK_FLOW_READ` | `tools/teul-cli/src/cli/eco.rs:271` |
| `E_ECO_NETWORK_FLOW_SEED` | `tools/teul-cli/src/main.rs:2172` |
| `E_ECO_NETWORK_FLOW_THRESHOLD` | `tools/teul-cli/src/main.rs:2181` |
| `E_ECO_RUNNER_DIAG` | `tools/teul-cli/src/cli/eco.rs:108` |
| `E_ECO_RUNNER_DIR` | `tools/teul-cli/src/cli/eco.rs:254` |
| `E_ECO_RUNNER_MODEL_EXEC` | `tools/teul-cli/src/cli/eco.rs:443` |
| `E_ECO_RUNNER_MODEL_LEX` | `tools/teul-cli/src/cli/eco.rs:414` |
| `E_ECO_RUNNER_MODEL_PARSE` | `tools/teul-cli/src/cli/eco.rs:417` |
| `E_ECO_RUNNER_MODEL_READ` | `tools/teul-cli/src/cli/eco.rs:116` |
| `E_ECO_RUNNER_PARSE` | `tools/teul-cli/src/cli/eco.rs:98` |
| `E_ECO_RUNNER_READ` | `tools/teul-cli/src/cli/eco.rs:96` |
| `E_ECO_RUNNER_REF` | `tools/teul-cli/src/cli/eco.rs:514` |
| `E_ECO_RUNNER_REPORT_JSON` | `tools/teul-cli/src/cli/eco.rs:251` |
| `E_ECO_RUNNER_SCHEMA` | `tools/teul-cli/src/cli/eco.rs:101` |
| `E_ECO_RUNNER_SHOCK` | `tools/teul-cli/src/cli/eco.rs:576` |
| `E_ECO_RUNNER_THRESHOLD` | `tools/teul-cli/src/cli/eco.rs:481` |
| `E_ECO_RUNNER_TICKS` | `tools/teul-cli/src/cli/eco.rs:105` |
| `E_EDU_ABS_TOL` | `tools/teul-cli/src/cli/edu.rs:59` |
| `E_EDU_CASE_LEN` | `tools/teul-cli/src/cli/edu.rs:88` |
| `E_EDU_DIV_ZERO` | `tools/teul-cli/src/cli/edu.rs:104` |
| `E_EDU_EMPTY` | `tools/teul-cli/src/cli/edu.rs:125` |
| `E_EDU_EPS` | `tools/teul-cli/src/cli/edu.rs:63` |
| `E_EDU_FORMULA` | `tools/teul-cli/src/cli/edu.rs:97` |
| `E_EDU_INPUT_PARSE` | `tools/teul-cli/src/cli/edu.rs:51` |
| `E_EDU_INPUT_READ` | `tools/teul-cli/src/cli/edu.rs:43` |
| `E_EDU_REL_TOL` | `tools/teul-cli/src/cli/edu.rs:61` |
| `E_EDU_SCHEMA` | `tools/teul-cli/src/cli/edu.rs:54` |
| `E_EDU_SIM` | `tools/teul-cli/src/cli/edu.rs:99` |
| `E_EFFECT_IN_ISOLATED_MODE` | `tools/teul-cli/src/canon.rs:8187` |
| `E_EFFECT_IN_STRICT_MODE` | `tools/teul-cli/src/canon.rs:8185` |
| `E_EFFECT_SURFACE_ALIAS_FORBIDDEN` | `tools/teul-cli/src/canon.rs:2227` |
| `E_EVAL_ARTIFACT_PARSE` | `tools/teul-cli/src/cli/eval.rs:128` |
| `E_EVAL_ARTIFACT_READ` | `tools/teul-cli/src/cli/eval.rs:125` |
| `E_EVAL_ARTIFACT_SCHEMA` | `tools/teul-cli/src/cli/eval.rs:131` |
| `E_EVAL_CONFIG_PARSE` | `tools/teul-cli/src/cli/eval.rs:42` |
| `E_EVAL_CONFIG_READ` | `tools/teul-cli/src/cli/eval.rs:34` |
| `E_EVAL_MODEL_ACTIVATION` | `tools/teul-cli/src/cli/eval.rs:75` |
| `E_EVAL_MODEL_DIM` | `tools/teul-cli/src/cli/eval.rs:71` |
| `E_EVAL_MODEL_PARSE` | `tools/teul-cli/src/cli/eval.rs:64` |
| `E_EVAL_MODEL_READ` | `tools/teul-cli/src/cli/eval.rs:55` |
| `E_EVAL_MODEL_SCHEMA` | `tools/teul-cli/src/cli/eval.rs:67` |
| `E_EVAL_MODEL_UTF8` | `tools/teul-cli/src/cli/eval.rs:62` |
| `E_EVAL_SCHEMA` | `tools/teul-cli/src/cli/eval.rs:45` |
| `E_EVAL_SUITE` | `tools/teul-cli/src/cli/eval.rs:50` |
| `E_EVAL_WEIGHTS_READ` | `tools/teul-cli/src/cli/eval.rs:80` |
| `E_EVENT_SURFACE_ALIAS_FORBIDDEN` | `tools/teul-cli/src/canon.rs:1658` |
| `E_EVOLVE_BUDGET_INVALID` | `tools/teul-cli/src/cli/evolve.rs:193` |
| `E_EVOLVE_CANON_FAIL` | `tools/teul-cli/src/cli/evolve.rs:362` |
| `E_EVOLVE_GENERATED_WRITE` | `tools/teul-cli/src/cli/evolve.rs:144` |
| `E_EVOLVE_META_DIR_CREATE` | `tools/teul-cli/src/cli/evolve.rs:141` |
| `E_EVOLVE_META_PARSE` | `tools/teul-cli/src/cli/evolve.rs:179` |
| `E_EVOLVE_META_READ` | `tools/teul-cli/src/cli/evolve.rs:178` |
| `E_EVOLVE_META_SERIALIZE` | `tools/teul-cli/src/cli/evolve.rs:164` |
| `E_EVOLVE_META_WRITE` | `tools/teul-cli/src/cli/evolve.rs:167` |
| `E_EVOLVE_MUTATION_OPS_TOO_FEW` | `tools/teul-cli/src/cli/evolve.rs:200` |
| `E_EVOLVE_MUTATION_OP_MISSING` | `tools/teul-cli/src/cli/evolve.rs:212` |
| `E_EVOLVE_MUTATION_OP_UNKNOWN` | `tools/teul-cli/src/cli/evolve.rs:308` |
| `E_EVOLVE_NO_CANDIDATE` | `tools/teul-cli/src/cli/evolve.rs:249` |
| `E_EVOLVE_OPERATOR` | `tools/teul-cli/src/cli/evolve.rs:322` |
| `E_EVOLVE_OUT_DIR_CREATE` | `tools/teul-cli/src/cli/evolve.rs:98` |
| `E_EVOLVE_SPEC_CONSTANTS_EMPTY` | `tools/teul-cli/src/cli/evolve.rs:187` |
| `E_EVOLVE_SPEC_PARSE` | `tools/teul-cli/src/cli/evolve.rs:131` |
| `E_EVOLVE_SPEC_READ` | `tools/teul-cli/src/cli/evolve.rs:127` |
| `E_EVOLVE_SPEC_SCHEMA` | `tools/teul-cli/src/cli/evolve.rs:184` |
| `E_EVOLVE_SPEC_STATEMENTS_EMPTY` | `tools/teul-cli/src/cli/evolve.rs:190` |
| `E_EVOLVE_SPEC_UTF8` | `tools/teul-cli/src/cli/evolve.rs:129` |
| `E_EVOLVE_TIMEOUT` | `tools/teul-cli/src/cli/evolve.rs:196` |
| `E_EVUNIV_CERT_PARSE` | `tools/teul-cli/src/cli/evolving_universe.rs:96` |
| `E_EVUNIV_CERT_READ` | `tools/teul-cli/src/cli/evolving_universe.rs:94` |
| `E_EVUNIV_HASH_JSON` | `tools/teul-cli/src/cli/evolving_universe.rs:190` |
| `E_EVUNIV_OUT_DIR_CREATE` | `tools/teul-cli/src/cli/evolving_universe.rs:40` |
| `E_EVUNIV_POLICY_PARSE` | `tools/teul-cli/src/cli/evolving_universe.rs:48` |
| `E_EVUNIV_POLICY_READ` | `tools/teul-cli/src/cli/evolving_universe.rs:44` |
| `E_EVUNIV_POLICY_SCHEMA` | `tools/teul-cli/src/cli/evolving_universe.rs:50` |
| `E_EVUNIV_POLICY_UTF8` | `tools/teul-cli/src/cli/evolving_universe.rs:46` |
| `E_EVUNIV_REPORT_SERIALIZE` | `tools/teul-cli/src/cli/evolving_universe.rs:162` |
| `E_EVUNIV_REPORT_WRITE` | `tools/teul-cli/src/cli/evolving_universe.rs:166` |
| `E_EVUNIV_ROLLBACK_FAIL` | `tools/teul-cli/src/cli/evolving_universe.rs:110` |
| `E_EVUNIV_SUBJECT_SERIALIZE` | `tools/teul-cli/src/cli/evolving_universe.rs:82` |
| `E_EVUNIV_SUBJECT_WRITE` | `tools/teul-cli/src/cli/evolving_universe.rs:85` |
| `E_EVUNIV_UNSAFE_RULE` | `tools/teul-cli/src/cli/evolving_universe.rs:67` |
| `E_EVUNIV_W89_PACK_NOT_FOUND` | `tools/teul-cli/src/cli/evolving_universe.rs:55` |
| `E_EXEC_ENUM_INVALID` | `tools/teul-cli/src/canon.rs:8153` |
| `E_EXEC_POLICY_DUPLICATE` | `tools/teul-cli/src/canon.rs:8155` |
| `E_FRONTDOOR` | `tools/teul-cli/src/cli/run.rs:175` |
| `E_FRONTDOOR_CUSTOM` | `tools/teul-cli/src/cli/run.rs:12056` |
| `E_FRONTDOOR_LANG_PARSER_GAP` | `tools/teul-cli/src/cli/frontdoor_parse.rs:71` |
| `E_FRONTDOOR_LEGACY_HEADER_FORBIDDEN` | `tools/teul-cli/src/canon.rs:4032` |
| `E_GAJI_JSON` | `tools/teul-cli/src/cli/gaji.rs:757` |
| `E_GAJI_LOCK_FIELD` | `tools/teul-cli/src/cli/gaji.rs:849` |
| `E_GAJI_LOCK_META` | `tools/teul-cli/src/cli/gaji.rs:767` |
| `E_GAJI_LOCK_PACKAGES` | `tools/teul-cli/src/cli/gaji.rs:843` |
| `E_GAJI_LOCK_PARSE` | `tools/teul-cli/src/cli/gaji.rs:825` |
| `E_GAJI_LOCK_READ` | `tools/teul-cli/src/cli/gaji.rs:823` |
| `E_GAJI_LOCK_SCHEMA` | `tools/teul-cli/src/cli/gaji.rs:832` |
| `E_GAJI_PATH` | `tools/teul-cli/src/cli/gaji.rs:691` |
| `E_GAJI_READ` | `tools/teul-cli/src/cli/gaji.rs:587` |
| `E_GAJI_SCAN` | `tools/teul-cli/src/cli/gaji.rs:180` |
| `E_GAJI_SCAN_DEPTH` | `tools/teul-cli/src/cli/gaji.rs:544` |
| `E_GAJI_TOML_VERSION` | `tools/teul-cli/src/cli/gaji.rs:619` |
| `E_GAJI_VENDOR_CLEAN` | `tools/teul-cli/src/cli/gaji.rs:305` |
| `E_GAJI_VENDOR_HASH_MISMATCH` | `tools/teul-cli/src/cli/gaji.rs:341` |
| `E_GAJI_VENDOR_READ` | `tools/teul-cli/src/cli/gaji.rs:634` |
| `E_GAJI_VENDOR_SRC` | `tools/teul-cli/src/cli/gaji.rs:331` |
| `E_GAJI_VENDOR_WRITE` | `tools/teul-cli/src/cli/gaji.rs:307` |
| `E_GAJI_WRITE` | `tools/teul-cli/src/cli/gaji.rs:190` |
| `E_GATEWAY_ACCEPT` | `tools/teul-cli/src/cli/gateway.rs:448` |
| `E_GATEWAY_INPUT_CONFLICT` | `tools/teul-cli/src/cli/gateway.rs:72` |
| `E_GATEWAY_INPUT_FIELD` | `tools/teul-cli/src/cli/gateway.rs:311` |
| `E_GATEWAY_INPUT_PARSE` | `tools/teul-cli/src/cli/gateway.rs:214` |
| `E_GATEWAY_INPUT_PAYLOAD` | `tools/teul-cli/src/cli/gateway.rs:284` |
| `E_GATEWAY_INPUT_READ` | `tools/teul-cli/src/cli/gateway.rs:212` |
| `E_GATEWAY_INPUT_SCHEMA` | `tools/teul-cli/src/cli/gateway.rs:229` |
| `E_GATEWAY_INVALID_PARAMS` | `tools/teul-cli/src/cli/gateway.rs:106` |
| `E_GATEWAY_LISTEN` | `tools/teul-cli/src/cli/gateway.rs:433` |
| `E_GATEWAY_OUT_DIR` | `tools/teul-cli/src/cli/gateway.rs:91` |
| `E_GATEWAY_OVERFLOW` | `tools/teul-cli/src/cli/gateway.rs:114` |
| `E_GATEWAY_REALMS` | `tools/teul-cli/src/cli/gateway.rs:645` |
| `E_GATEWAY_REPORT_JSON` | `tools/teul-cli/src/cli/gateway.rs:86` |
| `E_GATEWAY_SEND` | `tools/teul-cli/src/cli/gateway.rs:570` |
| `E_GATEWAY_SEND_REQUIRES_LISTEN` | `tools/teul-cli/src/cli/gateway.rs:77` |
| `E_GATEWAY_SEND_REQUIRES_MAX` | `tools/teul-cli/src/cli/gateway.rs:81` |
| `E_GATEWAY_TIMEOUT` | `tools/teul-cli/src/cli/gateway.rs:452` |
| `E_GATEWAY_WORLD_NOT_FOUND` | `tools/teul-cli/src/cli/gateway.rs:63` |
| `E_GATEWAY_WORLD_READ` | `tools/teul-cli/src/cli/gateway.rs:65` |
| `E_GEOUL_EMPTY_LOG` | `tools/teul-cli/src/cli/geoul.rs:162` |
| `E_GEOUL_ENTRY_MISSING` | `tools/teul-cli/src/cli/geoul.rs:153` |
| `E_GEOUL_ENTRY_READ` | `tools/teul-cli/src/cli/geoul.rs:39` |
| `E_GEOUL_ENTRY_WRITE` | `tools/teul-cli/src/cli/replay_branch.rs:135` |
| `E_GEOUL_FINISH` | `tools/teul-cli/src/cli/replay_branch.rs:242` |
| `E_GEOUL_FRAME_MADI_MISMATCH` | `tools/teul-cli/src/cli/geoul.rs:176` |
| `E_GEOUL_INIT` | `tools/teul-cli/src/cli/replay_branch.rs:132` |
| `E_GEOUL_KEY_EMPTY` | `tools/teul-cli/src/cli/geoul.rs:195` |
| `E_GEOUL_LEX` | `tools/teul-cli/src/cli/geoul.rs:43` |
| `E_GEOUL_PARSE` | `tools/teul-cli/src/cli/geoul.rs:46` |
| `E_GEOUL_RANGE` | `tools/teul-cli/src/cli/geoul.rs:87` |
| `E_GEOUL_RECORD` | `tools/teul-cli/src/cli/replay_branch.rs:227` |
| `E_GEOUL_RECORD_EMPTY` | `tools/teul-cli/src/cli/geoul.rs:296` |
| `E_GEOUL_RECORD_FINISH` | `tools/teul-cli/src/cli/run.rs:3759` |
| `E_GEOUL_RECORD_HEADER` | `tools/teul-cli/src/cli/geoul.rs:312` |
| `E_GEOUL_RECORD_HEADER_PARSE` | `tools/teul-cli/src/cli/geoul.rs:301` |
| `E_GEOUL_RECORD_INIT` | `tools/teul-cli/src/cli/run.rs:3503` |
| `E_GEOUL_RECORD_PARSE` | `tools/teul-cli/src/cli/geoul.rs:256` |
| `E_GEOUL_RECORD_READ` | `tools/teul-cli/src/cli/geoul.rs:254` |
| `E_GEOUL_RECORD_SCHEMA` | `tools/teul-cli/src/cli/geoul.rs:259` |
| `E_GEOUL_RECORD_STEP` | `tools/teul-cli/src/cli/geoul.rs:359` |
| `E_GEOUL_RECORD_STEP_KIND` | `tools/teul-cli/src/cli/geoul.rs:366` |
| `E_GEOUL_RECORD_STEP_PARSE` | `tools/teul-cli/src/cli/geoul.rs:351` |
| `E_GEOUL_RECORD_TIME` | `tools/teul-cli/src/cli/run.rs:3492` |
| `E_GEOUL_RUNTIME` | `tools/teul-cli/src/cli/geoul.rs:65` |
| `E_GEOUL_SNAPSHOT_MADI_MISMATCH` | `tools/teul-cli/src/cli/geoul.rs:183` |
| `E_GOAP_ACTION` | `tools/teul-cli/src/cli/goal.rs:34` |
| `E_GOAP_ACTIONS` | `tools/teul-cli/src/cli/goal.rs:27` |
| `E_GOAP_INPUT` | `tools/teul-cli/src/cli/goap.rs:40` |
| `E_GUSEONG_INPUT_PORT_UNDECLARED` | `tools/teul-cli/src/canon.rs:9025` |
| `E_GUSEONG_INSTANCE_DUP` | `tools/teul-cli/src/canon.rs:8474` |
| `E_GUSEONG_INSTANCE_UNDECLARED` | `tools/teul-cli/src/canon.rs:8405` |
| `E_GUSEONG_LINK_CYCLE` | `tools/teul-cli/src/canon.rs:9410` |
| `E_GUSEONG_LINK_TOPLEVEL_ONLY` | `tools/teul-cli/src/canon.rs:8490` |
| `E_GUSEONG_OUTPUT_PORT_UNDECLARED` | `tools/teul-cli/src/canon.rs:9048` |
| `E_GUSEONG_PORT_DIR` | `tools/teul-cli/src/canon.rs:8511` |
| `E_GUSEONG_TUPLE_ACCESS_ON_SCALAR` | `tools/teul-cli/src/canon.rs:9105` |
| `E_GUSEONG_TUPLE_INDEX_INVALID` | `tools/teul-cli/src/canon.rs:9080` |
| `E_HEAL_CASE_ID_DUP` | `tools/teul-cli/src/cli/heal.rs:109` |
| `E_HEAL_CASE_ID_EMPTY` | `tools/teul-cli/src/cli/heal.rs:106` |
| `E_HEAL_INPUT_EMPTY` | `tools/teul-cli/src/cli/heal.rs:97` |
| `E_HEAL_INPUT_PARSE` | `tools/teul-cli/src/cli/heal.rs:89` |
| `E_HEAL_INPUT_READ` | `tools/teul-cli/src/cli/heal.rs:81` |
| `E_HEAL_INPUT_SCHEMA` | `tools/teul-cli/src/cli/heal.rs:93` |
| `E_HEAL_INPUT_UTF8` | `tools/teul-cli/src/cli/heal.rs:87` |
| `E_HEAL_LOOP` | `tools/teul-cli/src/cli/heal.rs:125` |
| `E_HEAL_NONREPLAYABLE` | `tools/teul-cli/src/cli/heal.rs:119` |
| `E_HEAL_NO_CHECKPOINT` | `tools/teul-cli/src/cli/heal.rs:113` |
| `E_HEAL_OUT_DIR` | `tools/teul-cli/src/cli/heal.rs:191` |
| `E_HEAL_OUT_WRITE` | `tools/teul-cli/src/cli/heal.rs:198` |
| `E_HEAL_REPORT_SERIALIZE` | `tools/teul-cli/src/cli/heal.rs:168` |
| `E_IMITATION_CONFIG_PARSE` | `tools/teul-cli/src/cli/imitation.rs:38` |
| `E_IMITATION_CONFIG_READ` | `tools/teul-cli/src/cli/imitation.rs:30` |
| `E_IMITATION_DIV_ZERO` | `tools/teul-cli/src/cli/imitation.rs:345` |
| `E_IMITATION_EMPTY` | `tools/teul-cli/src/cli/imitation.rs:61` |
| `E_IMITATION_ENV_MISMATCH` | `tools/teul-cli/src/cli/imitation.rs:68` |
| `E_IMITATION_MAX_EPOCHS` | `tools/teul-cli/src/cli/imitation.rs:46` |
| `E_IMITATION_REPLAY_ENV` | `tools/teul-cli/src/cli/imitation.rs:155` |
| `E_IMITATION_REPLAY_PARSE` | `tools/teul-cli/src/cli/imitation.rs:145` |
| `E_IMITATION_REPLAY_READ` | `tools/teul-cli/src/cli/imitation.rs:51` |
| `E_IMITATION_REPLAY_SCHEMA` | `tools/teul-cli/src/cli/imitation.rs:185` |
| `E_IMITATION_REPLAY_STEP` | `tools/teul-cli/src/cli/imitation.rs:160` |
| `E_IMITATION_SCHEMA` | `tools/teul-cli/src/cli/imitation.rs:41` |
| `E_INFER_ACTIVATION` | `tools/teul-cli/src/cli/infer.rs:43` |
| `E_INFER_DIM` | `tools/teul-cli/src/cli/infer.rs:39` |
| `E_INFER_INPUT_LEN` | `tools/teul-cli/src/cli/infer.rs:61` |
| `E_INFER_INPUT_PARSE` | `tools/teul-cli/src/cli/infer.rs:53` |
| `E_INFER_INPUT_READ` | `tools/teul-cli/src/cli/infer.rs:51` |
| `E_INFER_INPUT_SCHEMA` | `tools/teul-cli/src/cli/infer.rs:56` |
| `E_INFER_MODEL_PARSE` | `tools/teul-cli/src/cli/infer.rs:32` |
| `E_INFER_MODEL_READ` | `tools/teul-cli/src/cli/infer.rs:28` |
| `E_INFER_MODEL_UTF8` | `tools/teul-cli/src/cli/infer.rs:30` |
| `E_INFER_SCHEMA` | `tools/teul-cli/src/cli/infer.rs:35` |
| `E_INFER_WEIGHTS_COUNT` | `tools/teul-cli/src/cli/infer.rs:108` |
| `E_INFER_WEIGHTS_LEN` | `tools/teul-cli/src/cli/infer.rs:103` |
| `E_INFER_WEIGHTS_READ` | `tools/teul-cli/src/cli/infer.rs:48` |
| `E_INIT_STATE_FILE` | `tools/teul-cli/src/cli/run.rs:424` |
| `E_INIT_STATE_JSON_PARSE` | `tools/teul-cli/src/cli/run.rs:345` |
| `E_INIT_STATE_JSON_ROOT` | `tools/teul-cli/src/cli/run.rs:348` |
| `E_INIT_STATE_JSON_STATE` | `tools/teul-cli/src/cli/run.rs:354` |
| `E_INIT_STATE_JSON_VALUE` | `tools/teul-cli/src/cli/run.rs:358` |
| `E_INIT_STATE_LINE` | `tools/teul-cli/src/cli/run.rs:329` |
| `E_INIT_STATE_READ` | `tools/teul-cli/src/cli/run.rs:304` |
| `E_INTENT_FIELD` | `tools/teul-cli/src/cli/intent.rs:93` |
| `E_INTENT_FIXED64` | `tools/teul-cli/src/cli/intent.rs:217` |
| `E_INTENT_JSON` | `tools/teul-cli/src/cli/intent.rs:90` |
| `E_INTENT_KIND` | `tools/teul-cli/src/cli/intent.rs:157` |
| `E_INTENT_MERGE` | `tools/teul-cli/src/main.rs:2458` |
| `E_INTENT_MISSING` | `tools/teul-cli/src/cli/intent.rs:20` |
| `E_INTENT_RECV_SEQ_DUPLICATE` | `tools/teul-cli/src/cli/intent.rs:105` |
| `E_INTENT_RECV_SEQ_REVERSE` | `tools/teul-cli/src/cli/intent.rs:113` |
| `E_IO_WRITE` | `tools/teul-cli/src/cli/run.rs:85` |
| `E_JJAIM_PORT_DECL_INVALID` | `tools/teul-cli/src/canon.rs:8921` |
| `E_JJAIM_PORT_DUP` | `tools/teul-cli/src/canon.rs:8937` |
| `E_JJAIM_PORT_TYPE_MISSING` | `tools/teul-cli/src/canon.rs:8927` |
| `E_JJAIM_SUBBLOCK_INVALID` | `tools/teul-cli/src/canon.rs:3912` |
| `E_JJAIM_TYPE_SCHEMA_CONFLICT` | `tools/teul-cli/src/canon.rs:8746` |
| `E_JJAIM_TYPE_TAG_REQUIRED` | `tools/teul-cli/src/canon.rs:8771` |
| `E_LEGACY_RANGE_SYNTAX` | `tools/teul-cli/src/cli/run.rs:160` |
| `E_LINT_COL` | `tools/teul-cli/src/cli/lint.rs:284` |
| `E_LINT_LINE` | `tools/teul-cli/src/cli/lint.rs:105` |
| `E_LINT_MISMATCH` | `tools/teul-cli/src/cli/lint.rs:299` |
| `E_LINT_RANGE` | `tools/teul-cli/src/cli/lint.rs:291` |
| `E_LINT_READ` | `tools/teul-cli/src/cli/lint.rs:58` |
| `E_LINT_SKIP_AMBIGUOUS` | `tools/teul-cli/src/cli/lint.rs:121` |
| `E_LINT_SKIP_BLOCK` | `tools/teul-cli/src/cli/lint.rs:114` |
| `E_LINT_WRITE` | `tools/teul-cli/src/cli/lint.rs:151` |
| `E_NUMERIC_FACTOR_INPUT_REQUIRED` | `tools/teul-cli/src/cli/numeric.rs:38` |
| `E_NUMERIC_FACTOR_JOB_OUT_DIR` | `tools/teul-cli/src/cli/numeric.rs:48` |
| `E_NUMERIC_FACTOR_JOB_READ` | `tools/teul-cli/src/cli/numeric.rs:33` |
| `E_NUMERIC_FACTOR_JOB_WRITE` | `tools/teul-cli/src/cli/numeric.rs:18` |
| `E_NUMERIC_FACTOR_OUT_DIR` | `tools/teul-cli/src/cli/numeric.rs:11` |
| `E_NUMERIC_FACTOR_RESULT_WRITE` | `tools/teul-cli/src/cli/numeric.rs:13` |
| `E_NUM_DIV0` | `tools/teul-cli/src/cli/run.rs:4937` |
| `E_NURIGYM_ACTIONS` | `tools/teul-cli/src/cli/nurigym.rs:354` |
| `E_NURIGYM_ACTION_INVALID` | `tools/teul-cli/src/cli/nurigym.rs:1467` |
| `E_NURIGYM_AGENTS` | `tools/teul-cli/src/cli/nurigym.rs:349` |
| `E_NURIGYM_ENV` | `tools/teul-cli/src/cli/nurigym.rs:247` |
| `E_NURIGYM_GRIDMAZE_LAYOUT` | `tools/teul-cli/src/cli/nurigym.rs:1429` |
| `E_NURIGYM_INPUT` | `tools/teul-cli/src/cli/nurigym.rs:197` |
| `E_NURIGYM_REWARD_WEIGHTS` | `tools/teul-cli/src/cli/nurigym.rs:1857` |
| `E_OPEN_BUNDLE_CONFLICT` | `tools/teul-cli/src/cli/run.rs:3256` |
| `E_OPEN_BUNDLE_META_JSON` | `tools/teul-cli/src/cli/run.rs:2817` |
| `E_OPEN_BUNDLE_META_TIME` | `tools/teul-cli/src/cli/run.rs:2795` |
| `E_OPEN_BUNDLE_META_WRITE` | `tools/teul-cli/src/cli/run.rs:2819` |
| `E_OPEN_BUNDLE_MODE` | `tools/teul-cli/src/cli/run.rs:3262` |
| `E_OPEN_BUNDLE_WRITE` | `tools/teul-cli/src/cli/run.rs:3301` |
| `E_OPEN_DENIED` | `tools/teul-cli/src/canon.rs:8190` |
| `E_OPEN_DIAG_REQUIRED` | `tools/teul-cli/src/cli/run.rs:3316` |
| `E_OPEN_POLICY` | `tools/teul-cli/src/cli/run.rs:3140` |
| `E_OPEN_REPLAY_MISS` | `tools/teul-cli/src/cli/run.rs:11291` |
| `E_PARSE` | `tools/teul-cli/src/cli/run.rs:12048` |
| `E_PARSE_HOOK_EVERY_N_MADI_INTERVAL_INVALID` | `tools/teul-cli/src/cli/run.rs:7838` |
| `E_PARSE_HOOK_EVERY_N_MADI_SUFFIX_UNSUPPORTED` | `tools/teul-cli/src/cli/run.rs:7874` |
| `E_PARSE_HOOK_EVERY_N_MADI_UNIT_UNSUPPORTED` | `tools/teul-cli/src/cli/run.rs:7856` |
| `E_PARSE_MAEGIM_NESTED_FIELD_UNSUPPORTED` | `tools/teul-cli/src/cli/run.rs:7821` |
| `E_PARSE_MAEGIM_NESTED_SECTION_UNSUPPORTED` | `tools/teul-cli/src/cli/run.rs:7802` |
| `E_PARSE_MAEGIM_STEP_SPLIT_CONFLICT` | `tools/teul-cli/src/cli/run.rs:7784` |
| `E_PATCH_ANCHOR` | `tools/teul-cli/src/cli/patch.rs:625` |
| `E_PATCH_APPROVAL` | `tools/teul-cli/src/cli/patch.rs:554` |
| `E_PATCH_APPROVE` | `tools/teul-cli/src/cli/patch.rs:229` |
| `E_PATCH_APPROVE_ABORT` | `tools/teul-cli/src/cli/patch.rs:238` |
| `E_PATCH_BEFORE_MISMATCH` | `tools/teul-cli/src/cli/patch.rs:476` |
| `E_PATCH_BLOCK` | `tools/teul-cli/src/cli/patch.rs:640` |
| `E_PATCH_CANON_MISMATCH` | `tools/teul-cli/src/cli/patch.rs:669` |
| `E_PATCH_CANON_PARSE` | `tools/teul-cli/src/cli/patch.rs:663` |
| `E_PATCH_COL` | `tools/teul-cli/src/cli/patch.rs:694` |
| `E_PATCH_JSON` | `tools/teul-cli/src/cli/patch.rs:365` |
| `E_PATCH_KIND` | `tools/teul-cli/src/cli/patch.rs:467` |
| `E_PATCH_LINE` | `tools/teul-cli/src/cli/patch.rs:161` |
| `E_PATCH_MISMATCH` | `tools/teul-cli/src/cli/patch.rs:709` |
| `E_PATCH_MODE` | `tools/teul-cli/src/cli/patch.rs:294` |
| `E_PATCH_PATH` | `tools/teul-cli/src/cli/patch.rs:284` |
| `E_PATCH_RANGE` | `tools/teul-cli/src/cli/patch.rs:701` |
| `E_PATCH_READ` | `tools/teul-cli/src/cli/patch.rs:126` |
| `E_PATCH_SKIP_AMBIGUOUS` | `tools/teul-cli/src/cli/patch.rs:177` |
| `E_PATCH_SKIP_BLOCK` | `tools/teul-cli/src/cli/patch.rs:170` |
| `E_PATCH_VERIFY` | `tools/teul-cli/src/cli/patch.rs:328` |
| `E_PATCH_VERIFY_FAIL` | `tools/teul-cli/src/cli/patch.rs:340` |
| `E_PATCH_VERIFY_TESTS` | `tools/teul-cli/src/cli/patch.rs:320` |
| `E_PATCH_WRITE` | `tools/teul-cli/src/cli/patch.rs:207` |
| `E_PRAGMA_REMOVED` | `tools/teul-cli/src/cli/run.rs:155` |
| `E_PROJECT_AGE_TARGET_INVALID` | `tools/teul-cli/src/cli/run.rs:2705` |
| `E_PROOF_AST_JSON` | `tools/teul-cli/src/cli/run.rs:6388` |
| `E_PROOF_CERT_FIELD_MISSING` | `tools/teul-cli/src/cli/run.rs:7061` |
| `E_PROOF_CERT_VERIFY_CERT_MANIFEST_SCHEMA` | `tools/teul-cli/src/cli/cert.rs:141` |
| `E_PROOF_CERT_VERIFY_FIELD_MISSING` | `tools/teul-cli/src/cli/cert.rs:367` |
| `E_PROOF_CERT_VERIFY_INPUT_READ` | `tools/teul-cli/src/cli/cert.rs:124` |
| `E_PROOF_CERT_VERIFY_INPUT_UTF8` | `tools/teul-cli/src/cli/cert.rs:130` |
| `E_PROOF_CERT_VERIFY_PARSE` | `tools/teul-cli/src/cli/cert.rs:132` |
| `E_PROOF_CERT_VERIFY_PUBKEY_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:154` |
| `E_PROOF_CERT_VERIFY_RUNTIME_ARTIFACT_CANDIDATE_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:191` |
| `E_PROOF_CERT_VERIFY_RUNTIME_ARTIFACT_SCHEMA` | `tools/teul-cli/src/cli/cert.rs:173` |
| `E_PROOF_CERT_VERIFY_RUNTIME_CANDIDATE_SCHEMA` | `tools/teul-cli/src/cli/cert.rs:168` |
| `E_PROOF_CERT_VERIFY_RUNTIME_DIAG_COUNT_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:182` |
| `E_PROOF_CERT_VERIFY_RUNTIME_PROFILE_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:176` |
| `E_PROOF_CERT_VERIFY_RUNTIME_SUBJECT_HASH_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:186` |
| `E_PROOF_CERT_VERIFY_RUNTIME_VERIFIED_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:179` |
| `E_PROOF_CERT_VERIFY_SCHEMA` | `tools/teul-cli/src/cli/cert.rs:135` |
| `E_PROOF_CERT_VERIFY_SIGNATURE_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:157` |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_FIELD_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:230` |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_HASH_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:205` |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_KIND_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:217` |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_PARSE` | `tools/teul-cli/src/cli/cert.rs:208` |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_READ` | `tools/teul-cli/src/cli/cert.rs:197` |
| `E_PROOF_CERT_VERIFY_SOURCE_PROOF_SCHEMA_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:212` |
| `E_PROOF_CERT_VERIFY_SUBJECT_HASH_MISMATCH` | `tools/teul-cli/src/cli/cert.rs:151` |
| `E_PROOF_JSON` | `tools/teul-cli/src/cli/run.rs:6938` |
| `E_PROOF_WRITE` | `tools/teul-cli/src/cli/run.rs:3666` |
| `E_REALM_INPUT` | `tools/teul-cli/src/cli/test.rs:34` |
| `E_REALM_OUTPUT` | `tools/teul-cli/src/cli/test.rs:73` |
| `E_REG` | `tools/teul-cli/src/cli/gaji_registry.rs:3832` |
| `E_REG_` | `tools/teul-cli/src/cli/gaji_registry.rs:3831` |
| `E_REG_ARCHIVE_SHA256_INVALID` | `tools/teul-cli/src/cli/gaji_registry.rs:2500` |
| `E_REG_ARCHIVE_SHA256_MISMATCH` | `tools/teul-cli/src/cli/gaji_registry.rs:893` |
| `E_REG_ARCHIVE_SHA256_REQUIRED` | `tools/teul-cli/src/cli/gaji_registry.rs:1585` |
| `E_REG_AUDIT_CHAIN_BROKEN` | `tools/teul-cli/src/cli/gaji_registry.rs:1187` |
| `E_REG_AUDIT_EMPTY` | `tools/teul-cli/src/cli/gaji_registry.rs:1219` |
| `E_REG_AUDIT_LAST_HASH_MISMATCH` | `tools/teul-cli/src/cli/gaji.rs:470` |
| `E_REG_AUDIT_LAST_HASH_REQUIRED` | `tools/teul-cli/src/cli/gaji.rs:441` |
| `E_REG_AUDIT_PARSE` | `tools/teul-cli/src/cli/gaji_registry.rs:1099` |
| `E_REG_AUDIT_READ` | `tools/teul-cli/src/cli/gaji_registry.rs:1084` |
| `E_REG_AUDIT_ROW_FIELD` | `tools/teul-cli/src/cli/gaji_registry.rs:1112` |
| `E_REG_AUDIT_ROW_HASH_MISMATCH` | `tools/teul-cli/src/cli/gaji_registry.rs:1167` |
| `E_REG_AUDIT_SCHEMA` | `tools/teul-cli/src/cli/gaji_registry.rs:1125` |
| `E_REG_AUDIT_VERIFY_LOG_REQUIRED` | `tools/teul-cli/src/cli/gaji.rs:459` |
| `E_REG_AUDIT_WRITE` | `tools/teul-cli/src/cli/gaji_registry.rs:3483` |
| `E_REG_AUTH_POLICY_PARSE` | `tools/teul-cli/src/cli/gaji_registry.rs:3331` |
| `E_REG_AUTH_POLICY_READ` | `tools/teul-cli/src/cli/gaji_registry.rs:3323` |
| `E_REG_AUTH_POLICY_SCHEMA` | `tools/teul-cli/src/cli/gaji_registry.rs:3340` |
| `E_REG_AUTH_REQUIRED` | `tools/teul-cli/src/cli/gaji_registry.rs:3315` |
| `E_REG_AUTH_ROLE_MISMATCH` | `tools/teul-cli/src/cli/gaji_registry.rs:3402` |
| `E_REG_AUTH_SCOPE_FORBIDDEN` | `tools/teul-cli/src/cli/gaji_registry.rs:3395` |
| `E_REG_AUTH_TOKEN_UNKNOWN` | `tools/teul-cli/src/cli/gaji_registry.rs:3387` |
| `E_REG_CACHE_READ` | `tools/teul-cli/src/cli/gaji_registry.rs:2344` |
| `E_REG_CACHE_WRITE` | `tools/teul-cli/src/cli/gaji_registry.rs:2480` |
| `E_REG_DEPENDENCIES_MISMATCH` | `tools/teul-cli/src/cli/gaji_registry.rs:926` |
| `E_REG_DETMATH_SEAL_MISMATCH` | `tools/teul-cli/src/cli/gaji_registry.rs:966` |
| `E_REG_DOWNLOAD_ARCHIVE_PATH` | `tools/teul-cli/src/cli/gaji_registry.rs:2884` |
| `E_REG_DOWNLOAD_HTTP_DISABLED` | `tools/teul-cli/src/cli/gaji_registry.rs:2394` |
| `E_REG_DOWNLOAD_HTTP_FAILED` | `tools/teul-cli/src/cli/gaji_registry.rs:2454` |
| `E_REG_DOWNLOAD_READ` | `tools/teul-cli/src/cli/gaji_registry.rs:2378` |
| `E_REG_DOWNLOAD_UNPACK` | `tools/teul-cli/src/cli/gaji_registry.rs:2820` |
| `E_REG_DOWNLOAD_URL_MISMATCH` | `tools/teul-cli/src/cli/gaji_registry.rs:910` |
| `E_REG_DOWNLOAD_URL_REQUIRED` | `tools/teul-cli/src/cli/gaji_registry.rs:1577` |
| `E_REG_DOWNLOAD_URL_SCHEME` | `tools/teul-cli/src/cli/gaji_registry.rs:2427` |
| `E_REG_DOWNLOAD_VENDOR_META` | `tools/teul-cli/src/cli/gaji_registry.rs:2872` |
| `E_REG_DOWNLOAD_VENDOR_NAME` | `tools/teul-cli/src/cli/gaji_registry.rs:2786` |
| `E_REG_DOWNLOAD_VENDOR_WRITE` | `tools/teul-cli/src/cli/gaji_registry.rs:2802` |
| `E_REG_DOWNLOAD_WRITE` | `tools/teul-cli/src/cli/gaji_registry.rs:1598` |
| `E_REG_FEDERATION_SOURCE_COUNT` | `tools/teul-cli/src/cli/gaji_registry.rs:1471` |
| `E_REG_IMMUTABLE_EXISTS` | `tools/teul-cli/src/cli/gaji_registry.rs:1731` |
| `E_REG_INDEX_FIELD` | `tools/teul-cli/src/cli/gaji_registry.rs:793` |
| `E_REG_INDEX_NOT_FOUND` | `tools/teul-cli/src/cli/gaji_registry.rs:860` |
| `E_REG_INDEX_PARSE` | `tools/teul-cli/src/cli/gaji.rs:112` |
| `E_REG_INDEX_READ` | `tools/teul-cli/src/cli/gaji.rs:104` |
| `E_REG_INDEX_ROOT_HASH_MISMATCH` | `tools/teul-cli/src/cli/gaji.rs:998` |
| `E_REG_INDEX_SCHEMA` | `tools/teul-cli/src/cli/gaji_registry.rs:2144` |
| `E_REG_INDEX_WRITE` | `tools/teul-cli/src/cli/gaji_registry.rs:3290` |
| `E_REG_JSON` | `tools/teul-cli/src/cli/gaji_registry.rs:1040` |
| `E_REG_LOCK_PACKAGES` | `tools/teul-cli/src/cli/gaji_registry.rs:731` |
| `E_REG_LOCK_PACKAGE_ID_INVALID` | `tools/teul-cli/src/cli/gaji_registry.rs:810` |
| `E_REG_LOCK_PARSE` | `tools/teul-cli/src/cli/gaji_registry.rs:690` |
| `E_REG_LOCK_READ` | `tools/teul-cli/src/cli/gaji_registry.rs:682` |
| `E_REG_LOCK_SCHEMA` | `tools/teul-cli/src/cli/gaji_registry.rs:702` |
| `E_REG_MIN_RUNTIME_MISMATCH` | `tools/teul-cli/src/cli/gaji_registry.rs:952` |
| `E_REG_PUBLISH_ARCHIVE_PATH` | `tools/teul-cli/src/cli/gaji_registry.rs:2681` |
| `E_REG_PUBLISH_ARCHIVE_READ` | `tools/teul-cli/src/cli/gaji_registry.rs:2605` |
| `E_REG_PUBLISH_ARCHIVE_WRITE` | `tools/teul-cli/src/cli/gaji_registry.rs:1759` |
| `E_REG_PUBLISH_PACKAGE_DIR` | `tools/teul-cli/src/cli/gaji_registry.rs:2574` |
| `E_REG_PUBLISH_PACKAGE_META` | `tools/teul-cli/src/cli/gaji_registry.rs:2583` |
| `E_REG_REPORT_SOURCE_READ` | `tools/teul-cli/src/cli/gaji_registry.rs:1331` |
| `E_REG_REPORT_WRITE` | `tools/teul-cli/src/cli/gaji_registry.rs:1049` |
| `E_REG_SCOPE_FORBIDDEN` | `tools/teul-cli/src/cli/gaji_registry.rs:3455` |
| `E_REG_SEARCH_QUERY` | `tools/teul-cli/src/cli/gaji_registry.rs:2921` |
| `E_REG_SNAPSHOT_MISMATCH` | `tools/teul-cli/src/cli/gaji.rs:987` |
| `E_REG_SNAPSHOT_MISSING` | `tools/teul-cli/src/cli/gaji.rs:147` |
| `E_REG_TRUST_ROOT_INVALID` | `tools/teul-cli/src/cli/gaji.rs:1021` |
| `E_REG_UNKNOWN` | `tools/teul-cli/src/cli/gaji_registry.rs:3309` |
| `E_REG_VERIFY_INDEX_REQUIRED` | `tools/teul-cli/src/cli/gaji.rs:214` |
| `E_REG_YANKED_LOCKED` | `tools/teul-cli/src/cli/gaji.rs:314` |
| `E_REPLAY_BRANCH_AT_RANGE` | `tools/teul-cli/src/cli/replay_branch.rs:54` |
| `E_REPLAY_BRANCH_EMPTY` | `tools/teul-cli/src/cli/replay_branch.rs:98` |
| `E_REPLAY_BRANCH_MISMATCH` | `tools/teul-cli/src/cli/replay_branch.rs:234` |
| `E_REPLAY_BRANCH_RECORD_ORDER_MISMATCH` | `tools/teul-cli/src/cli/replay_branch.rs:87` |
| `E_REPLAY_DIFF_MANIFEST` | `tools/teul-cli/src/cli/replay_diff.rs:96` |
| `E_REPLAY_DIFF_READ` | `tools/teul-cli/src/cli/replay_diff.rs:93` |
| `E_REPLAY_EMPTY_LOG` | `tools/teul-cli/src/cli/replay.rs:43` |
| `E_REPLAY_ENTRY_MISSING` | `tools/teul-cli/src/cli/replay.rs:35` |
| `E_REPLAY_ENTRY_READ` | `tools/teul-cli/src/cli/replay.rs:38` |
| `E_REPLAY_FRAME_MADI_MISMATCH` | `tools/teul-cli/src/cli/replay.rs:66` |
| `E_REPLAY_LEX` | `tools/teul-cli/src/cli/replay.rs:89` |
| `E_REPLAY_MISMATCH` | `tools/teul-cli/src/cli/replay.rs:138` |
| `E_REPLAY_PARSE` | `tools/teul-cli/src/cli/replay.rs:92` |
| `E_REPLAY_RUNTIME` | `tools/teul-cli/src/cli/replay.rs:127` |
| `E_REPLAY_SEEK_RANGE` | `tools/teul-cli/src/cli/replay.rs:56` |
| `E_REPLAY_SNAPSHOT_MADI_MISMATCH` | `tools/teul-cli/src/cli/replay.rs:73` |
| `E_REPLAY_UNTIL_RANGE` | `tools/teul-cli/src/cli/replay.rs:49` |
| `E_REPRO_WRITE` | `tools/teul-cli/src/cli/run.rs:3686` |
| `E_REWARD_CALL` | `tools/teul-cli/src/cli/reward.rs:392` |
| `E_REWARD_CALL_UNKNOWN` | `tools/teul-cli/src/cli/reward.rs:440` |
| `E_REWARD_DIV0` | `tools/teul-cli/src/cli/reward.rs:365` |
| `E_REWARD_INPUT_PARSE` | `tools/teul-cli/src/cli/reward.rs:55` |
| `E_REWARD_INPUT_READ` | `tools/teul-cli/src/cli/reward.rs:47` |
| `E_REWARD_LEX` | `tools/teul-cli/src/cli/reward.rs:632` |
| `E_REWARD_PARSE` | `tools/teul-cli/src/cli/reward.rs:669` |
| `E_REWARD_RESULT_TYPE` | `tools/teul-cli/src/cli/reward.rs:91` |
| `E_REWARD_SCHEMA` | `tools/teul-cli/src/cli/reward.rs:58` |
| `E_REWARD_TYPE` | `tools/teul-cli/src/cli/reward.rs:343` |
| `E_REWARD_VAR` | `tools/teul-cli/src/cli/reward.rs:68` |
| `E_REWARD_VAR_MISSING` | `tools/teul-cli/src/cli/reward.rs:337` |
| `E_RUN_MANIFEST_JSON` | `tools/teul-cli/src/cli/run.rs:5996` |
| `E_RUN_MANIFEST_WRITE` | `tools/teul-cli/src/cli/run.rs:5998` |
| `E_RUN_SUMMARY_WRITE` | `tools/teul-cli/src/cli/run.rs:4008` |
| `E_SAFETY_INTENT` | `tools/teul-cli/src/cli/safety.rs:36` |
| `E_SAFETY_RULE` | `tools/teul-cli/src/cli/safety.rs:18` |
| `E_SALIM_REMOVED` | `tools/teul-cli/src/cli/geoul.rs:199` |
| `E_SAM_BAD_MADI_HZ` | `tools/teul-cli/src/cli/run.rs:954` |
| `E_SAM_DETJSON_FIELD` | `tools/teul-cli/src/cli/run.rs:1009` |
| `E_SAM_DETJSON_PARSE` | `tools/teul-cli/src/cli/run.rs:993` |
| `E_SAM_DETJSON_PAYLOAD` | `tools/teul-cli/src/cli/run.rs:1024` |
| `E_SAM_DETJSON_READ` | `tools/teul-cli/src/cli/run.rs:991` |
| `E_SAM_DETJSON_SCHEMA` | `tools/teul-cli/src/cli/run.rs:1000` |
| `E_SAM_FINISH` | `tools/teul-cli/src/cli/run.rs:3690` |
| `E_SAM_INPUT_EOF` | `tools/teul-cli/src/cli/run.rs:1067` |
| `E_SAM_LIVE_BIND` | `tools/teul-cli/src/cli/sam_live.rs:246` |
| `E_SAM_LIVE_NONBLOCK` | `tools/teul-cli/src/cli/sam_live.rs:249` |
| `E_SAM_LIVE_RAW` | `tools/teul-cli/src/cli/sam_live.rs:164` |
| `E_SAM_MADI_HZ_MISMATCH` | `tools/teul-cli/src/cli/run.rs:912` |
| `E_SAM_MADI_INFINITE` | `tools/teul-cli/src/cli/run.rs:3345` |
| `E_SAM_MADI_RANGE` | `tools/teul-cli/src/cli/run.rs:3374` |
| `E_SAM_MODE_CONFLICT` | `tools/teul-cli/src/cli/run.rs:879` |
| `E_SAM_RECORD_COUNT_MISMATCH` | `tools/teul-cli/src/cli/run.rs:893` |
| `E_SAM_RECORD_MADI_REQUIRED` | `tools/teul-cli/src/cli/run.rs:950` |
| `E_SAM_RECORD_ORDER_MISMATCH` | `tools/teul-cli/src/cli/run.rs:931` |
| `E_SCAN_READ` | `tools/teul-cli/src/cli/scan.rs:10` |
| `E_SETTING_MADI_BAD_VALUE` | `tools/teul-cli/src/cli/run.rs:3124` |
| `E_SFC_IDENTITY_VIOLATION` | `tools/teul-cli/src/cli/eco.rs:309` |
| `E_SOCIAL_AGENTS_EMPTY` | `tools/teul-cli/src/cli/social.rs:129` |
| `E_SOCIAL_AGENT_DUPLICATE` | `tools/teul-cli/src/cli/social.rs:234` |
| `E_SOCIAL_AGENT_UNKNOWN` | `tools/teul-cli/src/cli/social.rs:294` |
| `E_SOCIAL_EVENT_FIELD` | `tools/teul-cli/src/cli/social.rs:280` |
| `E_SOCIAL_EVENT_KIND` | `tools/teul-cli/src/cli/social.rs:370` |
| `E_SOCIAL_EVENT_KIND_EMPTY` | `tools/teul-cli/src/cli/social.rs:148` |
| `E_SOCIAL_EVENT_STEP` | `tools/teul-cli/src/cli/social.rs:142` |
| `E_SOCIAL_EVENT_VALUE` | `tools/teul-cli/src/cli/social.rs:288` |
| `E_SOCIAL_EXPLOSION` | `tools/teul-cli/src/cli/social.rs:338` |
| `E_SOCIAL_INPUT_PARSE` | `tools/teul-cli/src/cli/social.rs:118` |
| `E_SOCIAL_INPUT_READ` | `tools/teul-cli/src/cli/social.rs:114` |
| `E_SOCIAL_INPUT_UTF8` | `tools/teul-cli/src/cli/social.rs:116` |
| `E_SOCIAL_OUT_DIR_CREATE` | `tools/teul-cli/src/cli/social.rs:213` |
| `E_SOCIAL_REPORT_SERIALIZE` | `tools/teul-cli/src/cli/social.rs:193` |
| `E_SOCIAL_SCHEMA` | `tools/teul-cli/src/cli/social.rs:122` |
| `E_SOCIAL_SEED_PARSE` | `tools/teul-cli/src/cli/social.rs:251` |
| `E_SOCIAL_STEPS_INVALID` | `tools/teul-cli/src/cli/social.rs:126` |
| `E_SWARM_ACTION_DUPLICATE` | `tools/teul-cli/src/cli/swarm.rs:105` |
| `E_SWARM_ACTION_UNKNOWN` | `tools/teul-cli/src/cli/swarm.rs:128` |
| `E_SWARM_AGENT_DUPLICATE` | `tools/teul-cli/src/cli/swarm.rs:90` |
| `E_SWARM_EMPTY` | `tools/teul-cli/src/cli/swarm.rs:84` |
| `E_SWARM_INPUT_PARSE` | `tools/teul-cli/src/cli/swarm.rs:51` |
| `E_SWARM_INPUT_READ` | `tools/teul-cli/src/cli/swarm.rs:49` |
| `E_SWARM_SCHEMA` | `tools/teul-cli/src/cli/swarm.rs:54` |
| `E_TENSOR_V0_CANON_JSON` | `tools/teul-cli/src/cli/tensor.rs:257` |
| `E_TENSOR_V0_DENSE_DATA_LEN` | `tools/teul-cli/src/cli/tensor.rs:145` |
| `E_TENSOR_V0_DENSE_DATA_TYPE` | `tools/teul-cli/src/cli/tensor.rs:142` |
| `E_TENSOR_V0_DENSE_VALUE_TYPE` | `tools/teul-cli/src/cli/tensor.rs:151` |
| `E_TENSOR_V0_DTYPE` | `tools/teul-cli/src/cli/tensor.rs:82` |
| `E_TENSOR_V0_INPUT_PARSE` | `tools/teul-cli/src/cli/tensor.rs:53` |
| `E_TENSOR_V0_INPUT_READ` | `tools/teul-cli/src/cli/tensor.rs:51` |
| `E_TENSOR_V0_KIND` | `tools/teul-cli/src/cli/tensor.rs:75` |
| `E_TENSOR_V0_OUT_DIR_CREATE` | `tools/teul-cli/src/cli/tensor.rs:31` |
| `E_TENSOR_V0_OUT_WRITE` | `tools/teul-cli/src/cli/tensor.rs:34` |
| `E_TENSOR_V0_ROOT_TYPE` | `tools/teul-cli/src/cli/tensor.rs:62` |
| `E_TENSOR_V0_SCHEMA` | `tools/teul-cli/src/cli/tensor.rs:68` |
| `E_TENSOR_V0_SHAPE` | `tools/teul-cli/src/cli/tensor.rs:118` |
| `E_TENSOR_V0_SPARSE_DUP` | `tools/teul-cli/src/cli/tensor.rs:203` |
| `E_TENSOR_V0_SPARSE_INDEX_OOB` | `tools/teul-cli/src/cli/tensor.rs:190` |
| `E_TENSOR_V0_SPARSE_INDEX_RANK` | `tools/teul-cli/src/cli/tensor.rs:182` |
| `E_TENSOR_V0_SPARSE_INDEX_TYPE` | `tools/teul-cli/src/cli/tensor.rs:180` |
| `E_TENSOR_V0_SPARSE_ITEMS_TYPE` | `tools/teul-cli/src/cli/tensor.rs:167` |
| `E_TENSOR_V0_SPARSE_ITEM_TYPE` | `tools/teul-cli/src/cli/tensor.rs:174` |
| `E_TENSOR_V0_SPARSE_ORDER` | `tools/teul-cli/src/cli/tensor.rs:206` |
| `E_TENSOR_V0_SPARSE_VALUE_TYPE` | `tools/teul-cli/src/cli/tensor.rs:197` |
| `E_TEST_CWD` | `tools/teul-cli/src/cli/test.rs:98` |
| `E_TEST_FILE_CONFLICT` | `tools/teul-cli/src/main.rs:1964` |
| `E_TEST_FILE_REQUIRED` | `tools/teul-cli/src/main.rs:2001` |
| `E_TEST_GOLDEN_OPTION` | `tools/teul-cli/src/main.rs:1984` |
| `E_TEST_MODE_CONFLICT` | `tools/teul-cli/src/main.rs:1959` |
| `E_TEST_OPTION_INVALID` | `tools/teul-cli/src/main.rs:2006` |
| `E_TEST_RUNNER_FAILED` | `tools/teul-cli/src/cli/test.rs:132` |
| `E_TEST_RUNNER_MISSING` | `tools/teul-cli/src/cli/test.rs:119` |
| `E_TEST_RUNNER_SPAWN` | `tools/teul-cli/src/cli/test.rs:129` |
| `E_TEST_SMOKE_OPTION` | `tools/teul-cli/src/main.rs:1969` |
| `E_TEST_WORKSPACE_ROOT` | `tools/teul-cli/src/cli/test.rs:113` |
| `E_TIMELINE_JSON` | `tools/teul-cli/src/cli/timeline.rs:47` |
| `E_TRACE_TIER_MISMATCH` | `tools/teul-cli/src/cli/run.rs:3244` |
| `E_TRACE_TIER_REQUIRED` | `tools/teul-cli/src/cli/run.rs:3237` |
| `E_TRAIN_CONFIG_PARSE` | `tools/teul-cli/src/cli/train.rs:34` |
| `E_TRAIN_CONFIG_READ` | `tools/teul-cli/src/cli/train.rs:32` |
| `E_TRAIN_CONFIG_SCHEMA` | `tools/teul-cli/src/cli/train.rs:43` |
| `E_TRAIN_MAX_EPOCHS` | `tools/teul-cli/src/cli/train.rs:51` |
| `E_TRAIN_SCHEMA` | `tools/teul-cli/src/cli/train.rs:46` |
| `E_TRAIN_THRESHOLD` | `tools/teul-cli/src/cli/train.rs:105` |
| `E_UNIVERSE_HASH_READ` | `tools/teul-cli/src/cli/universe.rs:213` |
| `E_UNIVERSE_PACK_INPUT_DIR` | `tools/teul-cli/src/cli/universe.rs:11` |
| `E_UNIVERSE_PACK_OUT_CREATE` | `tools/teul-cli/src/cli/universe.rs:28` |
| `E_UNIVERSE_PACK_OUT_DIR` | `tools/teul-cli/src/cli/universe.rs:18` |
| `E_UNIVERSE_PACK_PATH_INVALID` | `tools/teul-cli/src/cli/universe.rs:182` |
| `E_UNIVERSE_PACK_READ` | `tools/teul-cli/src/cli/universe.rs:44` |
| `E_UNIVERSE_PACK_READ_DIR` | `tools/teul-cli/src/cli/universe.rs:150` |
| `E_UNIVERSE_PACK_REL_PATH` | `tools/teul-cli/src/cli/universe.rs:161` |
| `E_UNIVERSE_PACK_ZIP_FINISH` | `tools/teul-cli/src/cli/universe.rs:55` |
| `E_UNIVERSE_PACK_ZIP_WRITE` | `tools/teul-cli/src/cli/universe.rs:50` |
| `E_UNIVERSE_UNPACK_COPY` | `tools/teul-cli/src/cli/universe.rs:134` |
| `E_UNIVERSE_UNPACK_INPUT_FILE` | `tools/teul-cli/src/cli/universe.rs:67` |
| `E_UNIVERSE_UNPACK_INPUT_OPEN` | `tools/teul-cli/src/cli/universe.rs:97` |
| `E_UNIVERSE_UNPACK_OUT_CREATE` | `tools/teul-cli/src/cli/universe.rs:88` |
| `E_UNIVERSE_UNPACK_OUT_FILE` | `tools/teul-cli/src/cli/universe.rs:127` |
| `E_UNIVERSE_UNPACK_OUT_NOT_EMPTY` | `tools/teul-cli/src/cli/universe.rs:81` |
| `E_UNIVERSE_UNPACK_OUT_PARENT` | `tools/teul-cli/src/cli/universe.rs:119` |
| `E_UNIVERSE_UNPACK_OUT_READ` | `tools/teul-cli/src/cli/universe.rs:74` |
| `E_UNIVERSE_UNPACK_PATH_INVALID` | `tools/teul-cli/src/cli/universe.rs:197` |
| `E_UNIVERSE_UNPACK_ZIP_ENTRY` | `tools/teul-cli/src/cli/universe.rs:109` |
| `E_UNIVERSE_UNPACK_ZIP_OPEN` | `tools/teul-cli/src/cli/universe.rs:103` |
| `E_WARP_INPUT` | `tools/teul-cli/src/cli/warp.rs:48` |
| `E_WARP_OUTPUT` | `tools/teul-cli/src/cli/warp.rs:73` |
| `E_WORKSHOP_MISSING` | `tools/teul-cli/src/cli/workshop.rs:32` |
