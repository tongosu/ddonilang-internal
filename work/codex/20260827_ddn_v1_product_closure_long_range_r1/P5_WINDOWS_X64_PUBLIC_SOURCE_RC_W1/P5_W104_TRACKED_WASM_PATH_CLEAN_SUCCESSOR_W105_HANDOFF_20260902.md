# P5 W104 tracked-WASM path-clean successor W105 handoff

## Fixed identity

- Internal CURRENT: v25.49.0 / RD-001~543.
- Public Language SPEC: v0.6.0.
- Source/handoff parent: `bd0522876252d9e55e6721650afffb100ff5c4c3`.
- Artifact fixed: `a3d45c0fa296da360e25c9d4ae41b2ccc75cef8c`.
- Fixed tree: `8fb7fd37f844dae40a240b6c596ea37ac79de992`.
- Direct parent relation: yes; merge count: 0.
- Successor impact: `ADDITIVE_ARTIFACT_CORRECTION`; no semantic RD or public SPEC change.

## Product/release blocker corrected

After W104, the existing path-clean inventory test reproduced a real tracked
artifact regression: 62/63 projection/remap tests passed and
`test_tracked_inventory_is_path_clean` failed with
`internal_absolute_path_count=115`. The exact fixed-source candidate built by
the existing official entrypoint had counts `0/0/0/0` for
internal/private/official/unknown host paths.

The official candidate copy path replaced only the tracked WASM binary; the
official freshness writer then refreshed the existing manifest. JS, TypeScript
declarations, package metadata, product source, test, pack, SSOT, SPEC and
visible UI bytes changed 0.

## Exact fixed diff

1. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` — 5,576,576 bytes / SHA-256 `00f574305c6d10b77b7a262e02d9cec677c4e79015d9ddd603eaf30e13abca11`.
2. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` — 29,964 bytes / SHA-256 `b03f09b07070a6ebdfb970e3aabd3e2970ce9d586e2b9249119a97ab787d1995`.

Candidate source receipt:

- source commit: `bd0522876252d9e55e6721650afffb100ff5c4c3`
- source tree: `022a463022502eef8a6c1b4bc8c4c8d9b60e9b48`
- semantic identity: `sha256:1bca6b486d9f40665e0793b38af22ca3ebb63051947fa5b44c87ebf0e91ea0f0`
- receipt: 2,470 bytes / SHA-256 `45b54f14db220da502f471b300c18a5d549fa9b8617aa139b99a6b1998b4e291`
- tracked writes performed by candidate builder: 0

## Verification

- Existing projection/remap/source-materialization tests: initial 62 PASS + 1
  RED at path count 115; after correction 63/63 PASS.
- Direct tracked artifact path scan: internal/private/official/unknown
  `0/0/0/0`; virtual roots `/ddn-src`, `/ddn-cargo-registry`, and
  `/ddn-rust-toolchain` only.
- Official tracked-WASM freshness: PASS.
- Candidate/tracked WASM exact equality: PASS.
- Product semantic source change: 0.
- New test/pack/runner/framework/meta-test: 0.
- New review task/worktree/branch: 0.

## Review and nonclaims

The earlier P5 review at `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`
remains PASS_TARGET_BOUND to its fixed target. W105 is a successor artifact and
does not inherit that PASS. It is queued with W102-W104 and the next exact
current-source Windows A/B projection for the existing rolling reviewer after
management dispatch.

This does not close P5, Windows package/archive/installer, SBOM/notices,
rights/license/signing/distribution, physical teul retirement, V1
membership/readiness/release/activation, or Owner Human Smoke/Human PASS.
