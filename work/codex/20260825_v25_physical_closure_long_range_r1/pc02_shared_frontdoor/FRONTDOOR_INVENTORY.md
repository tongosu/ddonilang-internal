# V25 PC-02 Frontdoor Inventory

| Surface | Before PC-02 | PC-02 authority | Migration boundary |
|---|---|---|---|
| shared language | PC-01 explicit `parse_v25*` only | `parse_v25_with_mode` + shared AST/canon | `parse_with_mode` remains pre-V25 only |
| tool runtime surface | pre-V25 reader behind shared preprocess | V25 prepare/canon/runtime by default | named `from_pre_v25_source*` only |
| official `ddonirang-tool` | general run/canon used historical authority | `run`, established `run-summary`, `canon`, and structural `v25-frontdoor` consume shared V25 authority | named Gate0/maze/eco commands remain explicitly pre-V25 |
| teul-cli | own parser/runtime and canon fallback | `run` and `canon` default `--source-epoch v25`, then call shared tool authority | `--source-epoch pre-v25`; no failure fallback |
| WASM | `DdnWasmVm` used historical reader | default constructor and V25 inspection export consume shared V25 authority | `DdnWasmVm.fromPreV25Source` only |
| Workbench | RuntimeBridge had no V25 assignment query | RuntimeBridge consumes `wasm_v25_assignment_frontdoor_json` | no JS rewrite, alias, or category diagnostic |

`source_analysis` remains the previously reviewed T4/T4h pre-V25 authority. PC-02
does not reinterpret that repair-proposal contract; it adds a dedicated V25
assignment query instead.
