# ddn_local_project_cli_wasm_parity_v1

G1 pack for DDN local project graph Wave 1.

This pack fixes the bounded `VirtualProjectSource` normalization contract before
project graph execution lands. The product requirement is that CLI and WASM call
the same Rust normalization code and return byte-identical normalized manifest
JSON for the same virtual project source.

Non-claims:

- This pack does not claim project graph execution.
- This pack does not claim module linking or local gaji lock verification.
- This pack does not change `state_hash`.
