# P5 clean offline license/SBOM handoff R1

## Fixed product lineage

- base handoff: `3aa88ee6d421164997110d65f3ff6f11a0f60b78`
- public-materialization product commit: `ae28ec1304fd28594575a60c11971580bfb21efa`
- SBOM host-path correction: `4744d5c23d03535ab74f0399f6d8e88c66c6fb68`
- product tree: `a2394d22ea807aa2c76b5277e987785755cdee24`
- merge commits: `0`

## Offline candidate result

The clean Windows candidate ran with the existing offline build policy and wrote its success marker only after artifact validation:

```text
schema: ddonirang.windows_public_candidate_result.v1
status: PASS
artifact manifest SHA-256: c186c6e2d5759705a50e062c2eda70b497e56102f6f5c98b2c4fe8a1fb3b8e18
artifact payload count: 5
```

Exact payload manifest:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `ddonilang.exe` | 7,143,936 | `41f1aee122cd241c31eb50ddfddd770a077f0ba2a07e64044ea07fcd1902d6ce` |
| `또니랑.exe` | 7,143,936 | `5d87f4beea695ba3dd380485260d89c1364b5c014cb64d62901909720c422f62` |
| `ddonirang.exe` | 7,143,936 | `067938469f045db02d916c550684ebb327041b62dbc315217602614f495dd0dc` |
| `LICENSE` | 11,357 | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `SBOM.detjson` | 24,706 | `b83546c5c9bc93e49961e55a07f6d7056010183bf9915dee19ab1330bb97a60b` |

`LICENSE` is the complete Apache-2.0 text. `SBOM.detjson` is deterministically generated from `cargo metadata --locked --offline` and `Cargo.lock`; it has 117 dependency rows, 5 `UNKNOWN_REQUIRES_REVIEW` license rows, and no host-absolute path. Those unknown rows remain a legal/release gate.

## Product-facing execution

The existing V25 fixture executed through all three artifact binaries with byte-identical output (`dc2f9f559bf6679e63a1d85bb07872a7c23f6701badd9c63c5153023ce078e4e`), including result state hash and WorkCost receipt. The existing legacy `=` fixture failed through all three with byte-identical diagnostic output (`272de60a881d7a9f705a75823e9f0d9970b2bfadc733b41fe5dd3e9b3f73ef2e`), exit `1`, `E_V25_DEFINITION_MIGRATION_REQUIRED`, and no state hash or success payload.

## Artifact fail-closed checks

- missing `ddonilang.exe`: RED; source artifact unchanged then GREEN.
- injected `teul-cli.exe`: RED; source artifact unchanged then GREEN.
- copied manifest tamper: RED; source manifest exact hash restored/unchanged then GREEN.

These checks used only task-local copies of the fixed artifact. No source, tracked artifact, or protected untracked worktree file was mutated.

## Boundaries

This is a P5 candidate-materialization handoff only. It does not claim P5 closure, Windows package approval, release readiness, publication authorization, dependency-license adjudication, V1 readiness, activation, or Human PASS. `tools/teul-cli` is not physically retired by this change.
