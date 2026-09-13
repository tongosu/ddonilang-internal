# BOGAE-PROD08B tracked WASM parity and freshness handoff

## Target

- Product commit: `a7f81d49b3eba4d4005c905036ba41c71f9d961b`
- Product tree: `5554bba68fb040f45e319e74a09a50e133092959`
- Product parent: `4f5fb1ddf7b01db9fbee34afc7f5df0f7ba5af84`
- Changed product path: `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
- Scope: tracked WASM freshness rematerialization after PROD08A's isolated-target build-input fix.

## Claim and primary gates

The tracked web WASM artifact and its deterministic manifest are bound to the
current source tree.  Existing Native, WASM, and Workbench shared-bridge paths
were exercised without a JavaScript source rewrite or a local success fallback.

- Official `scripts/build_wasm_tool.ps1 -Profile release -Target web -CopyToUi $true`
  ran with `CARGO_TARGET_DIR=I:\home\urihanl\ddn\codex\build\target-bogae-prod08`.
- `python tests/run_ddn_cli_wasm_freshness_check.py` passed after rematerialization.
- `node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs` passed: raw V25
  source/profile reaches `wasm_run_summary_with_source_profile_json` unchanged;
  missing shared export rejects instead of falling back locally.
- `node tests/ddn_current_public_rejection_parity_runner.mjs` passed for three
  current public legacy-rejection cases with Native/WASM exact diagnostic parity,
  zero state mutation, zero partial output/effect, and zero compatibility fallback.
- Direct current V25 execution of
  `pack/v1_core_supported_ingress_w1/fixtures/positive_definition_rebinding.ddn`
  succeeded under `ddonilang`, `또니랑`, and `ddonirang`.  The Native and tracked
  WASM summaries matched structurally for canonical source, source profile,
  output fields, state fields, receipt field, schema, and source path.

## Artifact binding

- `ddonirang_tool_bg.wasm` SHA-256:
  `ffc82a6e97ba5a3af72b090f222f7f808d982d63c4297bf075d16cfd334a9f83`
- Manifest raw SHA-256:
  `07cbc75a97d080530f739be1ffc1e4d01039345f87b74c98fa04f019cffc2ed1`
- Manifest Git blob after restore:
  `eb45383be3626d0ec62e23ac2a44389d26bab29d`
- Manifest source tree SHA-256:
  `0ca5649d2b63947a5da16dda4b9bb6d4df7b8024158c9792c8b1d899fbfa5c6a`

## Mutation evidence

All mutations were performed in the existing product paths and restored before
this product commit.

| Mutation | RED evidence | Exact restore | GREEN evidence |
| --- | --- | --- | --- |
| M-B1 stale/WASM binding | Replaced `wasm_sha256` with zeroes; freshness checker reported `wasm_sha256 mismatch`. | manifest SHA-256 `07cbc75a...ffc2ed1`, blob `eb45383...ab29d` | freshness checker PASS |
| M-B2 source-tree binding | Replaced `source_tree_sha256` with zeroes; freshness checker reported `source_tree_sha256 mismatch`. | manifest SHA-256 `07cbc75a...ffc2ed1`, blob `eb45383...ab29d` | freshness checker PASS |
| M-B3 bridge shared-export binding | Replaced `wasm_run_summary_with_source_profile_json` with the unprofiled export; bridge runner rejected with `E_WASM_RUN_SUMMARY_REQUIRED`. | runtime bridge SHA-256 `f80241dcfae381f7d7e6522e4ba8faaf793b64c60541fb035dd20c2fc15c2703`, blob `f91e663e3be9ffca26f5c706ed620000c109a176` | bridge runner PASS |

## Scope limits and nonclaims

- `tests/run_v1_core_supported_ingress_w1.py` reached its strict-selection case
  but the historical `차림` fixture now failed earlier with `E_EXECUTION_PARSE`.
  The fixture/semantic migration was not changed in this WASM-freshness unit.
- No SSOT, public SPEC, public ABI, wire, renderer identity, package, release,
  readiness, Human PASS, or independent PASS claim is made.
- This target is `PRODUCT_FIXED_PENDING_REVIEW`; independent review remains
  required.

## Review packet

```yaml
CLAIM: Current tracked WASM freshness and shared frontdoor parity are preserved.
TARGET_IDENTITY: a7f81d49b3eba4d4005c905036ba41c71f9d961b
PRIMARY_GATES:
  - official release WASM build with dedicated target
  - tests/run_ddn_cli_wasm_freshness_check.py
  - tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs
  - tests/ddn_current_public_rejection_parity_runner.mjs
MUTATIONS: M-B1, M-B2, M-B3 RED -> exact restore -> GREEN
STOP_CONDITION: Any mismatch of source-tree, artifact, or shared bridge binding.
NONCLAIMS: No independent review verdict and no V1 release/readiness claim.
```
