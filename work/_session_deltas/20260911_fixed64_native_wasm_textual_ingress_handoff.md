# Fixed64 Native/WASM textual-ingress convergence handoff

- Product: `5949d228be2e1cd7be12338d3a6bf857885dc3d1`
- Tree: `4ed39b7740f98d390332caad1ef049685359037f`
- Parent: `cb36af65b1db17ac0071c612ca711d718ba32cfa`
- Product path: `tool/src/wasm_api.rs`
- Fixed blob: `0dcbcfa4c75601efe518f3b7f391ac0a506c1db2`
- Fixed SHA-256: `7a813bdb396d8fa81a3b59d5da48024fc6df2f3cf73fb67bc924b278163d6942`

## Claim

WASM no longer owns a copy of the strict Fixed64 JSON textual-admission
algorithm.  It re-exports the existing `unit_wire::json_to_fixed64` owner, so
Native and WASM consume the same exact string/raw-i64 admission and reject
JSON binary numbers from one implementation.  No public ABI or wire shape
changed.

## Gates

- `native_and_wasm_carriers_share_the_strict_fixed64_boundary` with `wasm`
  feature — PASS.
- Native unit-wire binary-number rejection/textual exact-value test — PASS.
- Offline WASM tool-library check — PASS.
- `git diff --check` — PASS before product commit.

## Mutations

- M1 reintroduced a WASM-local number path using `as_f64` and
  `Fixed64::from_f64_lossy`; the parity test RED because WASM accepted JSON
  number `0.5` while Native rejected it.
- M2 replaced the re-export with a local `None -> Fixed64::ZERO` fallback; the
  same parity test RED because the rejected binary input became a successful
  zero value.
- M3 changed the shared textual-string admission to `Fixed64::ZERO`; the
  parity test RED because the exact three-half-ULP text no longer produced raw
  value `2`.

Each scratch mutation was removed and the WASM product source restored to
blob `0dcbcfa4…` / SHA-256 `7a813b…`; focused parity GREENed.  M3 restored the
shared owner exactly and was not committed.

## Review boundary

Ready for independent review: YES.  This closes only the duplicated strict
textual-ingress owner.  Public f64 setter/snapshot compatibility, all Fixed64
operations, release, and Human PASS remain out of scope.
