# Seamgrim official CLI run convergence handoff

## Fixed target

- Implementation base: `166adc3e3daa6ee447d726429a1f3142280206a0`
- Product fixed: `86ab59b6977684b359ad3ab42629bb81e48068d9`
- Product tree: `a56915843059e9fc4432c336e6a69506d94a1cf5`
- Parent: `166adc3e3daa6ee447d726429a1f3142280206a0`
- Merge count: `0`

## Product behavior

`/api/run` now writes the received raw V25 text unchanged to its temporary input and calls the one shared `run_ddonilang(...)` adapter.  The adapter resolves only `DDONILANG_BIN`, project/common-build `ddonilang`, or PATH `ddonilang`; it has no teul fallback.  It invokes `ddonilang run <input> --source-profile v1-core-v25` and carries a positive `madi` as `--madi <N>`.

The server consumes structured official `output_log_texts`, not legacy line output.  It carries the official profile identity, state hash, and WorkCost receipt in its existing runtime summary.  Legacy `=` input fails as `E_V25_DEFINITION_MIGRATION_REQUIRED` with HTTP 500, `ok=false`, and no graph.

## Evidence

- Actual HTTP V25 fixture with `madi=1`: `ok=true`, profile `v1-core-v25`, one output, state hash and receipt present.
- Repeat of that exact request: output/state/profile/receipt equality `true`.
- Actual legacy fixture: HTTP `500`, `ok=false`, no graph, diagnostic `E_V25_DEFINITION_MIGRATION_REQUIRED`.
- Isolated teul-only resolver environment: `E_DDONILANG_BIN_NOT_FOUND`; no teul process was started.
- `python -m py_compile` on the two product modules: PASS.
- `python tests/run_seamgrim_export_graph_preprocess_check.py`: PASS.
- Existing broad gate `python tests/run_seamgrim_ddn_exec_server_gate_check.py --profile release`: existing `index_markup_missing detail=title_or_canvas`; it did not exercise or contradict this `/api/run` change.

## Mutations

All were applied to the changed product sources, produced RED, then restored byte-exactly before focused GREEN.

1. teul resolver fallback insertion: RED (`official resolver contains teul fallback`).
2. source-profile removal: RED (`explicit v1-core-v25 profile binding missing`).
3. active teul preprocessing insertion: RED (`active teul preprocessing remained`).
4. nonzero execution error changed to HTTP 200: actual legacy HTTP response became `200`; restore returned it to `500` with no graph.

Restored SHA-256 values before the product commit were `295fc32c285b41c84da9974bae909bbb93e20677aaf7d5b3cf8fb418e265f9e0` for `export_graph.py` and `6d2e3698c40acf2af8cb775e92491b8bcf9ef8b4846dc18cd386f60b8e6d54ac` for `ddn_exec_server.py`.

## Boundary

This is `SEAMGRIM_LOCAL_API_RUN_OFFICIAL_CLI=PRODUCT_IMPLEMENTED_PENDING_REVIEW` only.  It does not retire `tools/teul-cli`, migrate standalone historical exporters, change deployment artifacts, close P0--P6, establish V1 readiness/release/publication/activation/legal status, or assert Human PASS.
