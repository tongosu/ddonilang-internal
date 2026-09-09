# DDN V1 CLI tool binary shared-input binding W112

AI_PROVIDER: OpenAI

AI_SURFACE: Codex Work

AI_CAPABILITY: existing single-writer product implementation

SESSION_NICKNAME: DDN V1제품마감Codex

PROJECT_ROLE: EXECUTION_OWNER / FILE_OWNER

RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]

DEEP_RESEARCH_CHECK: NOT_USE — fixed local product evidence decided the repair.

## Product value

The official native tool binary had become non-compilable after shared input
authority was made a `ddn_runtime` dependency.  W112 reconnects that binary to
the existing shared modules, so its existing user workflows can start again.

## Fixed product identity

- Parent: `52bb7bb8d885cb3096d4ee9373107ff78f807d06`
- Fixed: `a28f52590ff77f0494c32090848cecfac82fbb4b`
- Tree: `6239c7937027f114c4ca91584b066869edf05f48`
- Changed product path: `tool/src/main.rs` only.

## Verification

- Existing binary regression reused: 368/368 PASS.
- New runner/pack/meta-test: 0.
- Product-facing compile RED -> GREEN confirmed.
- One missing-module mutation: RED exit 101 -> byte-exact restore -> GREEN.
- Missing project-policy build-schema invocation: existing fail-closed exit 1;
  artifact publish 0.

## Boundaries

No dependency was added.  `docs/ssot/**`, `publish/spec/**`, tracked WASM,
visible UI, public command/executable membership, and `tools/teul-cli/**` were
unchanged.  Rights attribution, publication, and distribution remain an
independent blocked track and do not authorize release claims.

## Next safe product work

Continue a non-overlapping CLI/shared-authority convergence vertical from the
existing C0-C8 inventory.  `geoul`, replay, eco, and public test/view/repl
membership remain frozen where their physical/public contracts are unresolved.
