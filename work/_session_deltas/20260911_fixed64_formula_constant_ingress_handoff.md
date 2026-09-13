# Fixed64 formula constants — product handoff

## Fixed target

- Product commit: `1b72a012f632239bef225348b2c4c2bb73d9bcee`
- Product tree: `b2b81e92f675fbf41941ac25c87fba8b807dd2e1`
- Parent: `4f45d064407cd87d13bde105ba1d7b32bfa583f2`
- Claim: current formula identifiers `pi` and `e` use the shared checked,
  ties-to-even Q31.32 host-result ingress rather than a local lossy cast.

## Product paths

- `tool/src/ddn_runtime.rs`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

No SSOT/SPEC, syntax, public wire, new identity, CLI contract, or fallback
changed.

## Behavior

- Formula evaluation binds `pi` to raw `13_493_037_705` and `e` to raw
  `11_674_931_555`, the shared finite host ingress results.
- The formula evaluator keeps the existing `?` propagation from the checked
  boundary, so a future non-finite/out-of-range host result remains a typed
  runtime failure rather than a numeric default.

## Verification

- `cargo test -p ddonirang-tool formula_constants_use_the_checked_host_fixed64_ingress --lib --offline` — PASS.
- `cargo test -p ddonirang-tool --lib --offline` — 673 PASS; four inherited
  unrelated failures: isolated-worktree absent-SSOT `ai_prompt` pair,
  `project_authoring` BOM parse, and `runtime_surface` legacy-profile.
- `cargo check -p ddonirang-tool --offline --quiet` — PASS.
- `python tests/run_ddn_cli_wasm_freshness_check.py` — PASS after the official
  existing WASM builder and manifest regeneration.
- `git diff --check` — PASS before product commit.

## Mutation evidence

Fixed runtime source: SHA-256
`BBC9650070516283C11867DFDBBACCB3C6FBFEA5C3E59A528B7F46F482E0848A`,
Git blob `83aca541cbe130eabb800a5965a4c0564ede4145`.

1. M1 restored the local `from_f64_lossy` path. The focused formula test was
   RED: `pi` became raw `13_493_037_704`, one ULP below the required checked
   ingress result. Exact restore returned GREEN.
2. M2 bound `pi` to the `e` host value. The focused formula test was RED with
   raw `11_674_931_555` where the `pi` identity requires
   `13_493_037_705`. Exact restore returned GREEN.

Tracked artifact SHA-256:
`E9D8D601CF0C76455E2F86E6ABFBB1D034F7DBB033E882A70CEF0C30A60BCF20`.
Manifest SHA-256:
`C1CAA918CBE4969EC24A7F78C4A8070333E5C966EE05C4462A62FAC875B55B4F`.

## Review packet

Review exact product target `1b72a012f632239bef225348b2c4c2bb73d9bcee`.
Confirm the two current formula constants no longer bypass the shared owner,
their expected raw Q31.32 values are correct, errors propagate before runtime
publication, and the tracked artifact/manifest match the target tree.

Status: `PRODUCT_FIXED_PENDING_REVIEW`. Nonclaims: independent PASS, full
three-name CLI formula runtime parity, dynamic WASM formula-result parity,
V1 readiness, release, and Human PASS.
