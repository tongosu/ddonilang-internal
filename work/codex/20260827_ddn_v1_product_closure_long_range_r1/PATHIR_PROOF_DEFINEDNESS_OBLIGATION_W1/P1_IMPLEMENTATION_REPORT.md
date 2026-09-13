# PathIR/Proof XP02·XP05·XP06 successor implementation report

## Authority and fixed lineage

- Live internal authority: v25.44.0 / RD-001~536.
- Index SHA-256: `ec4550a420fad0e7ab23269a1f05b1ce26ea3168bfd2b4bc9cc9ae0b6b9598d7`.
- Aggregate SHA-256: `6eae7af1c337280faae449b026acaa7230e56917c4e0e6d18214cdace2a0344f`.
- Manifest SHA-256: `9defeac715df7fd8d02b5f5cc9550a11199e688f46be100e3dc82b9f614e1d5d`.
- Seal SHA-256: `90831242d5a20c64caf0f895403983eaf97b4c9b4a905812b2e8e55a8f9ecc47`.
- Public Language SPEC: v0.6.0, pointer SHA-256
  `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- Semantic owners: RD-417, RD-421, RD-423.
- Successor impact from v25.42: `ADDITIVE_NO_RELEVANT_SEMANTIC_CONFLICT`.
  RD-535/536 do not alter this PathIR contract.
- Base: `8c86fba3237f94bc3fcd18c309673d337e7dec41`.
- Product/test fixed: `477f888ef95747d14e2965851690658cd5edf181`.
- Fixed tree: `66b77b85f14703d5840f82f0a0656caf7d495b3b`.
- Direct parent relation: yes. Merge count: 0.

## User workflow changed

The existing Rust product API now accepts one explicit typed checked-assumption
request and completes this domain-separated internal chain:

`ProofProblem -> Certificate -> CheckExecution -> CheckResult -> Report -> Receipt`.

The request version, provider, checker and kernel profile fail closed. The
checker recomputes the PathIR rewrite and definedness relation rather than
trusting a provider boolean or canonical result. The report is bound into the
receipt, and a successful pure proof publishes exactly one result with state
publish 0 and outbox release 0.

This representation is intentionally internal and non-serialized. It does not
choose the OPEN public registry path, field spelling, CLI option, WASM transport
field, Workbench mapping or raw-DDN syntax.

## Exact fixed diff

1. `proof/src/lib.rs`
   - internal typed request;
   - `CheckExecutionIdentity` and `ReportIdentity`;
   - check-result participation by check-execution identity;
   - report/result identity validation;
   - receipt participation by check-execution and report identities;
   - unknown-version and assumption-loss fail-closed cases.
2. `tests/run_ddn_cli_wasm_freshness_check.py`
   - existing release-critical checker now fingerprints direct tool dependencies
     `numeric/src`, `proof/src`, `symbolic/src` and their Cargo manifests.
3. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
   - rebuilt with the official release entrypoint; no new export.
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
   - source roots/file ledger and artifact hash refreshed.

New pack: 0. New runner/framework: 0. New public export: 0. UI visual/copy/layout
change: 0. SSOT/SPEC change: 0.

## Physical contract preflight

v25.44 RD-423 remains `EXACT-SCHEMA-WIRE-OPEN / PRODUCT-OPEN`. The repository
has no Owner-approved PathIR checked-assumption product registry. Current
teul-cli symbolic/proof commands accept expressions but no checked assumption
object; WASM and Workbench expose no approved assumption/obligation mapping.

Therefore:

- public structured wire: `CONCRETE_DETAIL_GAP_DETECTED`;
- positive CLI ingress: `OWNER_DECISION_REQUIRED`;
- positive WASM transport: `OWNER_DECISION_REQUIRED`;
- Workbench structured field mapping: `OWNER_DECISION_REQUIRED`;
- raw DDN checked-assumption surface: `OWNER_SURFACE_DECISION_REQUIRED`;
- stable diagnostic spelling: OPEN.

## Status

- P0 containment: PRESERVED.
- P1 obligation vertical: `PARTIAL_IMPLEMENTED_UNDER_REVIEW`.
- XP-02: `PARTIAL_WITH_EXACT_PUBLIC_INGRESS_BLOCKER`.
- XP-05: `PASS_INTERNAL_IMPLEMENTED_UNDER_REVIEW`.
- XP-06: `PASS_INTERNAL_CHAIN / PARTIAL_PUBLIC_PROJECTION`.
- ERQ-20260825-001: OPEN.
- V1 membership/readiness/release/activation/Human transition: 0.
