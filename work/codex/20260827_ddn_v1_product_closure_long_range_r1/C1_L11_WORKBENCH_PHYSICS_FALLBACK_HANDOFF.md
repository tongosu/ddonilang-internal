# C1 L11 Workbench physics-fallback handoff

## Fixed target

- Product commit: `cd64c065c4edb59e479136af471ec97f36c03a75`
- Parent: `d8239c3c0a813f21bb4cf70f2b7a83f0d73c4234`
- Product path: `solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`

## User workflow

When the official physics lessons cannot be fetched, Workbench now opens
pendulum and projectile fallback source expressed as executable V25 `:=`
callables.  The shared tracked WASM source-analysis frontdoor accepts both
fallback documents with the `v1-core-v25` profile.

## Evidence

- `node --check solutions/seamgrim_ui_mvp/ui/workbench/workbench.js`: PASS.
- Both fallback documents: tracked WASM source-analysis `ACCEPTED`.
- Mutation: changing the pendulum fallback to `채비 {` with `<-` produced
  `REJECTED` in the same frontdoor.
- Exact restore: SHA-256
  `5372aec1cb62bf33e07ce79c9990c750639a4830f6c6530217ed0f8bf9f33b00`,
  blob `e841009f0ab4cf90d3149afc22fbbbd75a6ca8cc`; frontdoor GREEN again.
- `git diff --check`: PASS before the product commit.

## Scope and nonclaims

This is a Workbench source-producer correction only.  It does not alter the
WASM binary, source-analysis ABI, public syntax, SSOT, public SPEC, release,
membership, readiness, or Human PASS.  Other legacy samples outside these
actual fallback workflows remain separate custody.
