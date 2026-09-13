# 2026-09-02 DDN V1 P5/M1 local Cargo target-dir candidate guard

AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: single-writer product implementation and internal candidate QA
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: EXECUTION_OWNER / FILE_OWNER
RETURN_LABEL: DDN V1제품마감Codex

## Result

Fixed `8751dde809d8a1e033302a752ae06ce5462721ab` corrects the Windows
public-candidate Cargo configuration guard: the existing local target-dir
materialization is ignored only for semantic comparison, while portable
configuration identity and all remaining configuration semantics stay exact.

The fresh candidate artifact was `ddonirang.exe` only; direct startup, stack,
path-remap, and teul-artifact checks passed.  Cargo metadata establishes that
`teul-cli` is not a workspace member, so this candidate build has no teul
compile dependency.  This does not decide the separately missing versioned
V1-required test/pack/publish command map.

Existing task-owned untracked custody was preserved and unstaged.  No SSOT,
SPEC, publication, release, membership, or Human status changed.
