# lang_connect_diag_v1

G4 diagnostic pack for connect desugar artifacts.

The sidecar SolvePlan fixes three diagnostic codes:

- `E_CONNECT_NO_PORT`
- `E_CONNECT_CHANNEL_MISMATCH`
- `E_CONNECT_UNSUPPORTED_RULE`

The no-port source is still rejected by the parser; `--solveplan-out` writes the diagnostic sidecar before returning the existing parse error.
