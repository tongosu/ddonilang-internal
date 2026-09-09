# DDN execution concurrency W1-D~F 독립 검토 요청

## fixed point

```text
BASELINE: eca2fbc50cd5cd50af299aad4fd87f33683c575a
PRODUCT_AND_TEST_FIXED_HEAD: d8a4b2ab5b7c5fe68b1738f955d2d3d5b2b86ad1
CORE_COMMIT: e46f653dae14b5b36564a7d1732aa5198f37a815
WASM_REPRO_CORRECTION: e9647e2ad39a30c7c8b19be118f1d0a2bfe23887
REVIEW_MODE: CLEAN_DETACHED_READ_ONLY
ALLOWED_VERDICT: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

검토자는 fixed HEAD를 격리된 clean-detached worktree에서 읽기 전용으로 재현한다.
제품, pack, oracle, 기대값과 구현 보고서를 수정하지 않는다.

## 필수 검토

1. baseline이 W1-C1 plain PASS closure의 직접 successor이고 merge commit이 0인지 확인한다.
2. `LogicalAsyncQueue`가 FIFO tail/no direct reentry를 지키며 bounded full에서 envelope를
   소유한 WAIT node를 만들고 silent drop·즉시 성공·hard failure로 바꾸지 않는지 확인한다.
3. wait identity가 logical material/ordinal로 도출되고 physical worker/source span/vector
   order를 포함하지 않는지, cancel이 정확히 한 waiter만 지우는지 확인한다.
4. sealed internal deadlock과 external authored wait가 구조적으로 구분되는지 확인한다.
5. nested outbox가 handler 성공 후에만 publish되고 handler failure에서 state, trace,
   pending message와 partial result가 남지 않는지 확인한다.
6. tool과 teul-cli가 같은 shared authority를 소비하며 top-level sender fallback,
   legacy bypass와 unsupported downgrade가 없는지 확인한다.
7. 65 oracle rows와 owner identity가 모두 고유하고, group cardinality 16/12/15/3/10/7/2,
   `PRODUCT_PASS=7`, `PRODUCT_UNSUPPORTED=58`인지 확인한다.
8. 실제 Node workers 1/2/8 × same-tag forward/reverse/shuffled 9회가 같은 result digest로
   수렴하며 injected digest drift가 RED인지 확인한다.
9. source-built native/WASM/tracked Workbench parity와 clean-detached WASM raw byte identity를
   직접 재현한다. 최종 bytes/hash는 5,482,770 /
   `fbccef544253e2ffe1c05abda1826ce34e785a4de193bfe59dec48d7898dde05`다.
10. `docs/ssot/**`, public SPEC, UI source, historical packs, Malhimnuri R2, official DB,
    PID/port와 activation 경계가 보존됐는지 확인한다.

## 핵심 명령

```text
cargo test -p ddonirang-lang delivery --lib
cargo test -p ddonirang-tool successor_async --lib
cargo test --manifest-path tools/teul-cli/Cargo.toml successor_async
node tests/ddn_execution_concurrency_w1df_oracle_runner.mjs
python tests/run_ddn_cli_wasm_freshness_check.py
python tests/run_ddn_wasm_source_tracked_byte_identity_check.py --fresh-a <clean-a-wasm> --fresh-b <clean-b-wasm> --tracked solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
git diff --check
```

W1-C1 parity runner는 source-built `ddonirang-tool.exe`, nodejs WASM, tracked WASM 경로를
환경 변수로 지정해 실행한다. WASM source builds는 tracked
`scripts/build_wasm_tool.ps1`의 stable source path remap을 사용해야 한다.

## 판정 경계

plain `PASS`라도 W1-D~F 제한 구현 범위만 판정한다. W1-C2 public ReactionProvider,
Workbench UI 진단 전파, rendezvous, persistent dependency, RD-207, W1 full closure,
activation과 Human PASS는 닫지 않는다. `PASS_WITH_FOLLOW_UP` 또는 `REWORK`이면 우회나
기대값 완화 없이 중단한다.
