# DDN execution concurrency W1-B 독립 검토 요청

## 고정점

```text
SCOPE: W1B_SUCCESSOR_CANON_CLEAN_CUT_ONLY
PRODUCT_FIXED_HEAD: 7610e4bfda5c322e65cf6df9a5af45e58e0ab4bf
PRODUCT_FIXED_PARENT: 6e03e0cfcff64de8a578883cb8ccba15bdf17cee
PREDECESSOR_PRODUCT_FIXED_HEAD: aaf72e08498031feeabfabc6692316e42dcfdc42
PREDECESSOR_FIXED_PARENT: de9cb9ed95f71910bedd2b1bce0769a8257a7f27
PREDECESSOR_VERDICT: PASS / W1_FIRST_SAFE_ASYNC_VERTICAL_ONLY
```

검토자는 제품 코드를 수정하지 말고 fresh detached worktree와 별도 Cargo target/WASM
output을 사용해 직접 재현한다. Codex 보고서만으로 판정하지 않는다.

## 필수 검토

1. exact lineage, direct parent, merge count 0, predecessor report SHA를 확인한다.
2. default `~~>`가 모든 공통/teul parser에서 `MessageTransfer::Rendezvous`이며
   `HistoricalAsync` 또는 async queue로 들어가지 않는지 확인한다.
3. historical identity는 명시적 `HistoricalMigrationEvidence` API/command에서만
   생성되고 일반 run/canon/WASM VM에는 진입하지 못하는지 확인한다.
4. async/rendezvous successor canon과 historical tagged artifact가 분리되는지 확인한다.
5. rendezvous runtime이 `E_RENDEZVOUS_PRODUCT_OPEN`으로 fail-closed하고 실패 전후
   state/hash가 같은지 확인한다.
6. 13-case successor pack의 `PRODUCT_PASS`, `MIGRATION_PASS`,
   `PRODUCT_UNSUPPORTED` 분류와 golden을 직접 검사한다.
7. native CLI, source-built node WASM, clean-detached web release, tracked Workbench WASM의
   canon/migration/diagnostic/span/runtime disposition parity를 확인한다.
8. 네 fault injection이 실제 RED이고 원복 뒤 GREEN인지 독립적으로 반복한다.
9. historical corpus 39 files/95 `~~>`, 5 files/7 `<<-`와 source diff 0을 확인한다.
10. 공식 DB, PID 53196/start time, port 8787, SSOT/SPEC/UI source, activation 경계를 확인한다.

권장 명령:

```text
cargo test -p ddonirang-lang
cargo test -p ddonirang-tool --lib
cargo test --manifest-path tools/teul-cli/Cargo.toml
cargo check -p ddonirang-tool --target wasm32-unknown-unknown --lib
python tests/run_pack_golden.py future_grammar_atlas_owner_closed_delta_r2
node tests/ddn_execution_concurrency_w1b_native_wasm_parity_runner.mjs
python tests/run_ddn_cli_wasm_freshness_check.py
```

parity runner 환경:

```text
DDN_W1B_CLI=<fresh teul-cli>
DDN_W1B_WASM_DIR=<fresh nodejs wasm-pack dir>
DDN_W1B_TRACKED_WASM_DIR=<fixed HEAD tracked ui/wasm dir>
```

## 판정 경계

검토자가 선언할 수 있는 최대 판정:

```text
PASS
SCOPE: W1B_SUCCESSOR_CANON_CLEAN_CUT_ONLY
```

다음은 이 검토로 승인하지 않는다.

```text
W1_FULL_CLOSURE
W1C
RENDEZVOUS_RUNTIME
SSOT_CHANGE
PUBLIC_SPEC_CHANGE
DEPLOYMENT
ACTIVATION
HUMAN_PASS
```

판정 결과는 `PASS / PASS_WITH_FOLLOW_UP / REWORK` 중 하나로 별도 review artifact와
review-only commit에 발행한다.
