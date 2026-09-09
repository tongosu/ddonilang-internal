# P5/M1 local Cargo target-dir candidate guard handoff

## Fixed identity

- Product fixed commit: `8751dde809d8a1e033302a752ae06ce5462721ab`
- Direct parent: `b91fedd6da7f9ecf1445c5bdbf9ec5db907c5d98`
- Fixed tree: `3f2ec54cc335c9ff9acb33d85a1c5c4b26d06b6a`
- Changed product path: `scripts/build_windows_x64_public_candidate.ps1` only

## Product change

The Windows x64 public-candidate builder now accepts the repository's local
`[build].target-dir` protection as a local materialization difference.  It
still requires the portable public Cargo configuration's exact SHA-256 and
requires every remaining effective configuration line to match.  A missing
portable configuration, a changed portable hash, or any non-target-dir
configuration difference remains `E_WINDOWS_CANDIDATE_PUBLIC_CONFIG_MISMATCH`.

This is a candidate-build custody correction.  It neither changes the
official executable/package name nor authorizes publication or release.

## Direct evidence

- The local configuration SHA-256 was
  `dfeeeb4dcb04816ea5de68a8b004b19cc79bfbf9c687a9f180939475bd56615e`.
- The portable configuration SHA-256 was the required
  `454a4ba886da1e98d2d44bf85d91babd1a6a3d3178ae381195b759750404ede5`.
- After removal of only the local target-dir materialization, effective
  configuration equality was true.
- `cargo metadata --no-deps` found no `teul-cli` package and no `teul-cli`
  workspace member.  This proves the candidate script's `--workspace` build
  does not require `teul-cli`; it does not settle the separately open
  versioned V1-required CI/test/pack/publish command map.
- Fresh candidate output:
  `I:/home/urihanl/ddn/codex/build/v1-public-candidate-config-guard-green-20260902`
  contained `artifact/ddonirang.exe` only, 7,045,632 bytes, SHA-256
  `489ca650b32166e1de0cfb7eb65c63d90d8fd908797d8bff8f7b170c93bbd2b5`.
- Artifact postcheck: `--help` exit 0; stack reserve 16,777,216; forbidden
  source/build/cargo/sysroot path occurrences 0; teul-named artifacts 0.

## Boundaries and next gate

- Source, tests, packs, tracked WASM, UI, SSOT, public SPEC, membership, and
  release transitions outside the one script are 0.
- The existing Cargo PDB collision warning for `ddonirang-tool`'s internal
  bin/lib names was observed during the full workspace candidate build.  It
  did not produce a teul artifact and is not altered by this slice.
- `V1_BUILD_REQUIRED_TEUL_DEPENDENCY=0` is established for this candidate
  build only.  V1-wide required test/pack/publish dependency status remains
  `CONCRETE_DETAIL_GAP_DETECTED` until the versioned required-command map is
  supplied.
- Review is not dispatched here.  Any future review uses the existing rolling
  reviewer at a coherent milestone only.

## Nonclaims

This is not P5 or Windows RC closure, V1 readiness, publication, release,
activation, legal clearance, or Human PASS.
