# PG-CLI-04 WASM freshness correction handoff

## Target

- Failed product: `604717bb29102b70a05e64809b29908b8ace32de`
- Independent finding: tracked WASM freshness failed because the manifest binds `lang/src` and `tool/src`, both changed by PG-CLI-04.
- Correction product: `d3c7af3c47d8bc0b73c267de8643c8789ec155f3`
- Correction tree: `59c57c929ce7712a2167d80776886f231fc8b3e9`
- Correction parent: `ab312853c850805f02a09f1f8b6d382d9a9cbaec`

## Changed product paths

- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The official `scripts/build_wasm_tool.ps1 -Profile release -Target web` entrypoint rebuilt the artifact using dedicated build and Cargo target directories. The generated artifact hash is `3C1F5232377D02D9F416CE89B026600E89A5AA01D8D990B1366AF4F8C8C7574B`; the refreshed manifest SHA-256 is `6975FC36886DD5BDCAE8972B28914CC115B84B4E3F4CF1BE5C848437286E692D`.

## Gates

- `python tests/run_ddn_cli_wasm_freshness_check.py` — PASS
- Direct tracked-WASM execution of `tool/tests/fixtures/pg_cli_pure_callable.ddn` — PASS, `output_log_texts=["34"]`
- Existing PG-CLI-04 language focused test — PASS before correction; no source behavior changed by this correction.
- `git diff --check` — PASS before product commit.

## Mutation and exact restore

`source_tree_sha256` was changed to sixty-four zeroes. The official checker failed with `source_tree_sha256 mismatch`. It was restored byte-exactly to fixed manifest blob `f1eb35877a9ed8aa88ba8afc8d50238c64318dc6`, then the checker passed.

## Review request and nonclaims

Please rereview the direct correction target for artifact/manifest source binding, official freshness, and direct tracked-WASM pure-callable execution. This handoff does not claim an independent PASS, public support, release readiness, or a new language/public-WASM contract.
