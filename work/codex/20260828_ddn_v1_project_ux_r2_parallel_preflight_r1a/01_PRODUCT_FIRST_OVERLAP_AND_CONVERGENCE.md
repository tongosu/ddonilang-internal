# Product-first overlap and convergence audit

## Compared lineage

```yaml
R3N_FU01_FIXED: 9389563e752fcc63b0425e05671473e1adb42ced
EDITABLE_I1_FIXED: d0ff23389e27b8268fe9eead8d0138abd6d77b06
MERGE_BASE: 305dd9d3ec162e38329242a99c76ca854634629c
R3N_CHANGED_PATHS_FROM_MERGE_BASE: 111
I1_CHANGED_PATHS_FROM_MERGE_BASE: 104
OVERLAP_PATHS: 5
CENSUS_HEAD: a1327db9d049606eea0784597b6b16efd620f7bc
CENSUS_ROLE: DOCS_EVIDENCE_ONLY
```

The direct fixed-head corrections are orthogonal: R3N fixed modifies `tools/wasm_candidate_remap.py` and two tests; I1 fixed modifies only `tool/src/source_epoch.rs`. The five overlaps arise from their predecessor lineages and still have to be reconciled before product-first adoption.

## Exact overlap

| Path | merge-base blob | R3N blob | I1 blob | Symbols / semantic role | Classification |
|---|---|---|---|---|---|
| `scripts/build_wasm_tool.ps1` | `d9afa71d6c40ddca7eda3978c17b260667a74a21` | `8400eba5f9e6b07a0622586ee36e45dabca9a8cc` | `b82143ff15b4b442be4d0a981d220d52703e5aaa` | R3N: `SourceRemapMode`, candidate seal/remap. I1: `CanonicalCandidate`, `CandidateOutDir`, `Write-CanonicalCandidateReceipt`, isolated target/output. Three-way merge emits conflict markers in parameter, environment restore, and receipt-write regions. | `SEMANTIC_CONFLICT` |
| `tool/src/ddn_runtime.rs` | `56ce97701ac2271bb867dd65a60d4b98f64b8f8b` | `6bfc5836ecb9048075a485c73d516d3fd435aab3` | `29a283adad6ad565d570dfbe6dfe844a552d7ee8` | R3N lineage adjusts self-contained test inputs. I1 adds `DdnProgram::from_source_epoch_with_mode` and routes PreV25/V25 explicitly. | `TEXTUAL_OVERLAP` with orthogonal intent |
| `tool/src/lib.rs` | `d60290ff431e73a00317279faa38e193e02a2de9` | `98cb5005b0ce53c94963b31ae07d65cbaa07a788` | `83be4197e45d4815b96bf4af1bc6c81052412813` | R3N exports sealed-domain dataset modules; I1 wires private `source_epoch`. Distinct declarations. | `ORTHOGONAL` |
| `tool/src/runtime_surface.rs` | `b7330f93c34ead9a0f2ca963a831de9deefe8f57` | `1288936ee1d2e6743b6aaa1bb588525755bbbcf8` | `a087e7974786f70656a4306d6646382dc164e7f3` | R3N lineage changes a test expectation. I1 adds `prepare_source_for_execution_with_path_and_epoch`, `run_summary_from_source_with_internal_epoch`, and epoch-aware diagnostics. | `TEXTUAL_OVERLAP` with orthogonal production role |
| `tool/src/wasm_api.rs` | `3351253c1c24f8ffd2f59a918bda707f5e21cd7f` | `d461b8061946c28a6a715bc998b9f0ef2e9b7020` | `ee473e7197553b5f5e6aac8351619ab44957c6b8` | R3N switches a self-contained test fixture. I1 adds FD01A/B and editable revision candidate WASM functions. Three-way merge conflicts at a test fixture list, not at the candidate exports. | `TEXTUAL_OVERLAP` |

No overlap is `GENERATED` or `TEST_ONLY` as a whole. Generated tracked WASM changes exist on the product-first lineage but are outside this five-path set and are not authorized for refresh here.

## Safe convergence order

1. Keep the R3N/product-first successor as the integration base. Its current `PASS_WITH_FOLLOW_UP` remains an external gate; do not erase that finding.
2. After the Editable I1 verdict, extract its semantic requirements and exact product diff; do not merge or cherry-pick the full side lineage.
3. Manually combine the two candidate build contracts in `scripts/build_wasm_tool.ps1`: isolated candidate output/target plus R3N toolchain-root remap/source-identity seal. Preserve default build behavior and tracked-WASM write prohibition.
4. Reapply I1's private SourceEpoch and editable revision custody surfaces onto the resulting product-first source, retaining all R3N source-identity checks.
5. Rebuild only isolated candidate artifacts, then rerun native/WASM/Workbench, clean A/B, Edge, fault, and source-identity attacks at one fixed head.
6. Request independent review of the converged head.

## Minimum rereview scope

- all five overlap paths and their call edges;
- I1-owned `tool/src/source_epoch.rs`, `project_store.py`, `ddn_exec_server.py`, RuntimeBridge and Workbench adapters;
- R3N `tools/wasm_candidate_remap.py` source-identity binding and validation receipt generation;
- candidate A/B/C, path scan zero, editable envelope/receipt tamper checks, server expected-head CAS, Edge and clean A/B;
- tracked WASM diff/refresh remains separately gated.

```yaml
CHERRY_PICK_SAFE: NO
CONVERGENCE_DISPOSITION: MANUAL_CONVERGENCE_REQUIRED
REIMPLEMENT_REQUIRED: NO
SEMANTIC_CONFLICT_COUNT: 1
BOUNDED_TEXTUAL_OVERLAP_PATHS: 3
ORTHOGONAL_SAME_FILE_PATHS: 1
```

This is a bounded convergence finding, not a claim that either reviewed target may be rewritten or that the product-first successor is ready for release.
