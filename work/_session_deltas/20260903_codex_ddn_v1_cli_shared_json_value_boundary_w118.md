# DDN V1 CLI shared JSON value boundary W118

- Status: Reflected in product fixed `59f6d7d8edceef44928755087ca9960f17c14120`; handoff follows in the same linear lineage.
- Authority: v25.50.0/RD-001~551 and public SPEC v0.6.0 read-only.
- Scope: `tool/src/bin/ddonirang.rs` only.  The official binary now serializes the
  exact `ddonirang_tool::serde_json::Value` returned by shared runtime workflows.
- Product value: prevents a reused Cargo target from turning `project-run` and
  `currentline-run` into a compile-time `serde` trait-version failure.
- Reused verification: binary unit 10/10 and local-project G0--G8 CLI/WASM workflow PASS.
- Preserved custody: the four pre-existing untracked session-delta files remain
  unstaged and byte-untouched.  `docs/ssot/**` and `publish/spec/**` were unchanged.
- Rights/publication: UNAVAILABLE-3 attribution remains a separate release gate;
  it does not block this internal product fix.  `PUBLICATION_READY=NO` and
  `RELEASE_READY=NO` remain unchanged.
- Next safe task: select only an existing V1 required vertical whose exact physical
  product contract is already approved; PathIR public wire/raw ingress and
  GOER/SOURCE-COORD physical contracts remain slice-local OPEN gates.
