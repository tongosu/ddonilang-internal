# Future Grammar Atlas R2 W1-D~F logical oracle and product-evidence links

이 pack은 W1-D~F가 소유하는 65개 비중복 logical fixture다. `logical_oracle.jsonl`이 단일 oracle이며 `build_oracle.mjs`는 그 결정적 재생기다.

- group: G01 16, G02 12, G03 15, G04 3, G05 10, G06 7, G07 2
- 모든 case: workers `1/2/8`, same-tag `forward/reverse/shuffled`에서 동일 semantic digest
- 65행 전부 `LOGICAL_ORACLE_ONLY`: membership, cardinality, schema, case identity,
  description drift와 worker-thread metadata hash 재현만 검증한다.
- `PUBLIC_SOURCE_PRODUCT_CASE` 4건: W1-C1 official native/source-WASM/tracked-WASM
  runner가 실제 실행하는 P09/P10/N10/X20의 별도 제품 근거다.
- `INTERNAL_TYPED_PRODUCT_CASE` 3건: public capacity override 없이 Rust in-process typed
  runtime으로만 도달하는 P11/N11/X14의 별도 제품 근거다.
- `PRODUCT_UNSUPPORTED` 58건: 아직 제품 문법/runtime이 없는 temporal, structured
  concurrency, dependency, rendezvous, external effect 항목이다.

정적 description digest와 worker matrix는 제품 async 실행, FIFO/WAIT/outbox 동작,
worker-independent runtime execution 또는 native/WASM parity를 증명하지 않는다. 실제 제품
근거는 각 행의 `evidence_*`와 별도 product-evidence runner가 소유한다.

이 pack은 RD-207 stable public wire, W1-C2 공개 ReactionProvider 표면, rendezvous runtime 또는 W1 전체 닫힘을 주장하지 않는다.

재생:

```text
node pack/future_grammar_atlas_owner_closed_delta_r2_w1df/build_oracle.mjs
node tests/ddn_execution_concurrency_w1df_oracle_runner.mjs
set DDN_W1DF_CARGO_TARGET_DIR=<isolated workspace target>
set DDN_W1DF_TEUL_CARGO_TARGET_DIR=<isolated teul-cli target>
set DDN_W1C1_CLI=<isolated workspace target>\debug\ddonirang-tool.exe
set DDN_W1C1_WASM_DIR=<source-built Node.js WASM output directory>
set DDN_W1C1_TRACKED_WASM_DIR=<repository>\solutions\seamgrim_ui_mvp\ui\wasm
node tests/ddn_execution_concurrency_w1df_product_evidence_runner.mjs
```

`DDN_W1C1_CLI`는 W1-C1 공식 10-case runner가 실행할 source-built
`ddonirang-tool.exe` 파일이다. `DDN_W1C1_WASM_DIR`은 source-built Node.js WASM의
`ddonirang_tool.js`와 `ddonirang_tool_bg.wasm`이 있는 디렉터리이고,
`DDN_W1C1_TRACKED_WASM_DIR`은 저장소가 추적하는 Workbench WASM의 같은 두 파일이
있는 디렉터리다. 세 변수는 runner가 요구하는 서로 다른 identity를 명시하며, 누락이나
서로 바꾼 값에 대한 fallback은 없다.

`teul-cli`는 독립 lockfile을 소유하므로 두 Cargo target을 공유하지 않는다.
