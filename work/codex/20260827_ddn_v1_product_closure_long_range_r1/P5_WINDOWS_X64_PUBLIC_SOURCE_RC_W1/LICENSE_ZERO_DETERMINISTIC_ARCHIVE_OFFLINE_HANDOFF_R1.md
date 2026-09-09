# P5 license-zero deterministic archive/offline handoff R1

## Product lineage

- baseline: `35fb9b496631d32c51978fff1281169d11c98639`
- Unit A: `4b07c4ff75510aaf4c56e5a703e3e0d22a3d2309`
- Unit B: `4a091407dc3b35cafca26ba548264d2ce2d643a1`
- Unit B fail-closed correction: `14bf2047fb46a63a34c79eab90255eb6b45fc527`
- final product tree: `86c92b8f88b87d5a76303ce9144d331d78f32a5f`
- merge commits: `0`

## Unit A — license metadata

`ddonirang-core`, `ddonirang-numeric`, `ddonirang-proof`, `ddonirang-symbolic`, and `ddonirang-tool` now each declare `license = "Apache-2.0"`. `ddonirang-lang` remains `MIT OR Apache-2.0` unchanged.

`cargo metadata --locked --offline` and the deterministic SBOM generator both pass: 117 rows, `UNKNOWN_REQUIRES_REVIEW = 0`, source-lock SHA-256 `69defff8a2c3e955fb0983db1b1327a2ebabfa302b60b8bb52a704cecf6c586e`, SBOM SHA-256 `097bba243b06b5aa719ad1ec93d450dd8e6ab4b5c48f8af31ceed897f37100e7`.

## Unit B — deterministic candidate archive

The existing offline Windows candidate build now creates `ddonirang-windows-x64-candidate.zip` using only Python standard library code. Entries use fixed ordering, POSIX names, fixed timestamps and permissions, and stored compression. A canonical archive manifest is placed in the deterministic ZIP comment; it binds all five archive entries without a self-hash cycle.

The clean result marker is `PASS` with candidate archive SHA-256 `a303971efbb8d0cac1e51fa8bc3d63ecf7f33a1671f2476a9f990fe24ebc6958` and artifact-manifest SHA-256 `b2fd116ead12c4506f07d989ddc6c2f30b69edb6aede9aeb2e40999c6db1d574`.

- archive repeat generation: byte-identical
- archive entries: `LICENSE`, `SBOM.detjson`, `ddonilang.exe`, `ddonirang.exe`, `또니랑.exe`
- host-path count / traversal entry count / teul artifact count: `0 / 0 / 0`
- missing or unmanifested executable: fail-closed

## Unit C — clean offline restore

The archive was expanded to a fresh build-root directory, then its payload hash manifest was verified. All three executable names produced byte-identical `--help`, V25 positive, and legacy negative output. Positive results include the state hash and WorkCost receipt. Legacy `=` exits nonzero with `E_V25_DEFINITION_MIGRATION_REQUIRED`, without state hash or success payload.

Task-local mutation copies produced RED then source-artifact unchanged GREEN:

1. withheld `LICENSE` → `E_WINDOWS_CANDIDATE_ARCHIVE_PAYLOAD_MISMATCH`.
2. tampered `SBOM.detjson` → `E_WINDOWS_CANDIDATE_ARCHIVE_PAYLOAD_MISMATCH`.
3. injected `unexpected.exe` → `E_WINDOWS_CANDIDATE_ARCHIVE_EXECUTABLE_SET`.

## Unit D — Workbench projection

`WORKBENCH_LAUNCH_SURFACE = OWNER_DECISION_REQUIRED`.

The current candidate archive deliberately contains only the five validated payload entries. The existing Workbench is served by `solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`, whose root-relative HTTP server consumes UI, WASM, lesson, schema, sample, and catalog resources. The tracked app also uses HTTP `fetch` for these resources. There is no existing public offline launcher/bundle contract that selects the exact resource set or specifies a distribution start action. Adding one would decide a public launcher/installation surface, so no UI/WASM/lesson projection was inferred or changed. Browser validation was not attempted for that unapproved surface.

## Boundaries

This handoff records a clean offline candidate and archive only. It does not close P5, authorize a release or publication, establish legal approval, create a Workbench public launcher, promote V1 readiness, activate a release, or establish Human PASS.
