# P5 offline Workbench candidate implementation handoff R1

## Fixed product lineage

- base: `39fc67d5d1854a5c56b4732c7db0ad3f50091f40`
- implementation: `8c988c00112c0c737310533e816ec7880a784201`
- focused test successor: `436cbbfadd098695e6b1814ce9fce3b64bcb40d0`
- product tree: `877d390958489a9723b37286fa44b39e061e3dc9`
- authority read-only: internal SSOT v25.60.0 / RD-001~571; public Language SPEC v0.6.0.

## Implemented candidate behavior

`ddonilang workbench`, `또니랑 workbench`, and compatibility alias
`ddonirang workbench` share the same binary entry and start a loopback-only
host.  `--no-open` exposes an automation-only token in process stdout; normal
browser mode does not emit it.  The token is not written to this handoff,
Git, asset manifests, archives, or session deltas.

The host validates every declared file before binding `127.0.0.1:0`, rejects
unmanifested or symlink/reparse assets, checks byte length and SHA-256, serves
only declared paths, uses an HttpOnly session cookie after the initial token
request, and emits `Cache-Control: no-store` and `Referrer-Policy: no-referrer`.

The candidate builder projects the tracked Workbench UI/CSS/JS/WASM runtime and
the exact 15-item release allowlist.  It emits deterministic
`workbench/asset_manifest.detjson` entries with path, byte count, SHA-256,
content type, and role.  Candidate archive construction now includes recursive
payload paths and rejects an executable set other than the three permitted CLI
names.

## Evidence

- projected manifest: 277 files, 93 lesson-role files, 15 allowlisted lesson IDs,
  1 tracked WASM; 51,385 bytes;
  SHA-256 `f688fdad1a64a91f980e8c14c0f230ec85538d1da6ebf3cc3578672acc455ba8`.
- actual loopback HTTP verification: each of the three binary names served all
  277 manifest files with byte/hash equality and `no-store`; manifest identity
  was identical for all three.
- focused Rust host test: PASS (1 passed; 632 filtered), including denied
  request, manifest asset serving, cookie continuation, and no-store header.
- mutation: an unmanifested asset produced
  `E_WORKBENCH_ASSET_MANIFEST_COVERAGE`; a byte-tampered asset produced
  `E_WORKBENCH_ASSET_HASH_MISMATCH`; both were byte-restored and startup was
  green.  An added executable made archive construction fail with
  `E_WINDOWS_CANDIDATE_ARCHIVE_EXECUTABLE_SET`, then exact restore was green.
- deterministic offline ZIP: 281 entries, 278 under `workbench/`, 65,933,958
  bytes, SHA-256 `af35f2fc3bc54f673027edd018d81aa810f4ceb49f82c0f42a59dcab4c3d60d9`;
  the restored repeated build had the same SHA-256.

## Remaining gate

Actual browser visual/run evidence is not claimed.  Browser automation was
blocked by an in-app webview attach timeout and an Edge administrator policy
check for the local loopback URL.  No security bypass was attempted.  The next
safe action is to rerun the existing tracked-browser V25 Run and legacy
fail-closed flow when that policy gate is available, then verify Native/WASM
result, state-hash, profile, and WorkCost-receipt parity from the unpacked
candidate alone.

## Nonclaims

This is a P5 candidate implementation handoff only.  It does not claim P5 or
V1 closure, membership, readiness, release, publication, activation, legal
clearance, Owner Human Smoke, or Human PASS.
