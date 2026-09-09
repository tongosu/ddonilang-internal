# 2026-09-02 DDN V1 product closure — CLI/teul profile setting authority W1

AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: single-writer product implementation and internal QA
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: EXECUTION_OWNER / FILE_OWNER
RETURN_LABEL: DDN V1제품마감Codex
DEEP_RESEARCH_CHECK: NOT_USE — current repository authority and executable
regression were sufficient.

`279b347b3f6b1807136f6fcb465aa9fb40d3d3bd` is a linear product successor of
`5ed9592a64e2896be7319bf20161167a6036b247`, merge 0.  It owns only
`tools/teul-cli/src/cli/run.rs` and removes the duplicate textual
`설정.마디수` authority from the explicit supported-profile path.  The shared
typed runtime remains the owner; legacy/internal extraction is retained.

Evidence: an existing supported-profile run test was extended for a V25 source
with `마디수: 2`; a temporary private-parser sentinel created RED exit 101 on
the former path; exact restoration gave focused GREEN.  Existing tracked WASM
parity passed 11 cases with five deterministic repeats and zero partial
summary.  No test framework, pack, runner, dependency, tracked WASM refresh,
SSOT/SPEC/UI/public naming, or physical teul retirement was introduced.

Authority v25.50.0 / RD-001~551 and public SPEC v0.6.0 were read-only.
Rights/publication remain an independent unresolved track; no release or
rights-cleared artifact assertion is made.  Existing protected untracked
session custody remains untouched and unstaged.  No reviewer was created.
