# PathIR/Proof public contract decisions required

## Preflight result

`CONCRETE_DETAIL_GAP_DETECTED`

Live internal authority is v25.44.0 / RD-001~536. RD-423 fixes the logical
identity and assumption/obligation firewall but explicitly leaves exact
schema, wire and hash prefix OPEN. Product search found the internal typed
`DeclaredAssumptionClosure`, `TransformationObligationSet`, request, checker,
report and receipt seam, but no versioned public registry owning the physical
contract.

Owner directions already bound here are:

1. use one sealed versioned request/result/report/receipt registry and project
   the same typed object into CLI, WASM and Workbench;
2. do not make legacy proof-verify JSON the new authority;
3. keep raw DDN checked-assumption input fail-closed until the structured
   registry independently passes;
4. after that PASS, project the same typed bundle through an existing
   morphology-compatible role without inventing syntax.

The following physical decisions remain required. Candidate strings below are
options only, not product or public names.

## CD-PATHIR-01 — registry physical identity

- Option A: a new versioned registry with one sealed request/result/report/
  receipt object and explicit required fields.
- Option B: extend legacy proof-verify JSON. This conflicts with the bound Owner
  direction and is not recommended.
- Option C: retain internal typed ingress only. Safe, but XP-02 public remains
  OPEN.
- Recommendation: A.
- Owner input needed: exact registry path/id, schema version spelling, physical
  field keys, required/optional matrix, serialization, identity-participation
  matrix and hash prefix.

## CD-PATHIR-02 — CLI structured transport

- Option A: one option that accepts the sealed versioned request document.
- Option B: the same document only through stdin.
- Option C: separate CLI flags for assumptions, provider, checker and profile.
- Recommendation: A, with stdin optionally additive later. It best preserves
  one semantic object and prevents field loss.
- Owner input needed: exact option spelling, stdin behavior, output/receipt
  destination and stable failure/exit mapping.

## CD-PATHIR-03 — WASM and Workbench projection

- Option A: one structured request/result transport field shared by native and
  WASM, with Workbench as a pure consumer.
- Option B: separate host fields mapped into the typed object.
- Option C: keep positive ingress unavailable.
- Recommendation: A.
- Owner input needed: exact WASM transport field, schema version behavior and
  Workbench display mapping. UI copy/layout remains outside this task.

## CD-PATHIR-04 — raw DDN projection and compatibility

- Option A: after structured-registry independent PASS, use an existing
  morphology-compatible typed-bundle role; exact role spelling is Owner-bound.
- Option B: reference a sealed project asset containing the same typed bundle.
- Option C: keep raw DDN positive ingress fail-closed.
- Recommendation: A after registry PASS, with C until then.
- Owner input needed: exact existing role/spelling, stable diagnostic code and
  any compatibility period. No new grammar is proposed.

## Impact and sequencing

- affected product paths after decisions: likely `proof`, official CLI/tool
  ingress, `tool/src/wasm_api.rs`, and existing Workbench structured-consumer
  bridge; exact FILE_OWNER must be issued after the physical registry is fixed;
- current safe behavior: raw DDN/CLI/WASM/Workbench positive checked-assumption
  ingress remains unavailable and fail-closed;
- remaining implementation verticals after Owner input: 3 coherent parts
  (registry+CLI, WASM+Workbench projection, raw-DDN projection) followed by one
  coherent fixed-target review;
- existing validation to reuse: 7 command/test groups plus the current corpus;
- ETA: `UNKNOWN` while four physical decision groups are open. Conditional
  engineering estimate after exact binding is 2-4 focused development days,
  medium confidence, excluding review and Owner response latency.

No SSOT, public SPEC, membership, readiness or release transition is made by
this packet.
