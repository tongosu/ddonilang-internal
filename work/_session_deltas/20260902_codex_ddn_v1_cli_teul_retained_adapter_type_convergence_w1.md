# DDN V1 CLI/teul retained adapter type convergence W1

- Status: Reflected in the paired product fixed commit and handoff successor.
- Product fixed: `133ebcdb888353efe92614a59c3427d0c5ec335a` /
  tree `2515712bd8a298c276bb77b88bcfe8c581aa8751`, direct parent
  `d02e1f6526eba5f337edfe5b7c0f815fbc8f0325`, merge 0.
- Authority: internal SSOT v25.50.0 / RD-001~551; public Language SPEC v0.6.0.
- Decision: repair nested-workspace Rust type identity drift by consuming the
  existing shared `ddonirang_tool` internal type identities at retained adapter
  boundaries.  New dependency, public spelling, wire schema, UI, SSOT, and
  public SPEC changes are zero.
- Evidence: original `teul-cli` test binary RED with 13 mismatched
  `serde_json`/`ddonirang_core` type errors; focused shared-run and snapshot
  tests GREEN; retained binary build/help GREEN; owner-bound `project-run`
  conflict test GREEN.
- Rights track: UNAVAILABLE-3 attribution remains separate and does not block
  internal product development.  No publication, release, distribution, or
  rights-cleared artifact claim is made.
- Next: retain this in the next coherent CLI/teul rolling review bundle; audit
  the next contract-fixed shared adapter without deciding public command
  membership or deleting `tools/teul-cli`.
