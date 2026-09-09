# 2026-09-02 DDN V1 product closure — ai prompt explicit shared-root W1

AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: single-writer product implementation and internal QA
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: EXECUTION_OWNER / FILE_OWNER
RETURN_LABEL: DDN V1제품마감Codex
DEEP_RESEARCH_CHECK: NOT_USE — the live repository and approved local authority
were sufficient.

Current authority was read-only: internal SSOT v25.50.0 / RD-001~551 and
public Language SPEC v0.6.0.  The rights/publication attribution lane remains
independent; it did not block this source implementation and is not resolved
by it.

Fixed product commit `f10ae697362a9912c56fa9ec4c48fd9da65c330b` is the direct
successor of `478834d3cc399011e5d9741a1d574edf8a57eb60`, merge count 0.  It
changes only `tool/src/ai_prompt.rs` and `tool/src/main.rs`: an explicit
runtime `DDN_BUILD_REPO_ROOT` binding for the linked-worktree source read, and
nonzero `ai prompt` failure exits.  No source-root scan, fallback, public
command naming, or dependency addition was introduced.

Verification recorded in the paired handoff: unbound root RED with output
publish 0; restored explicit root GREEN with deterministic SHA-256
`4D88803E11ABB3BFC490561BC60712EB893E87561FEC2231799D292B2FB9A8B7`; focused
existing invariant test PASS; no-root binary build PASS.  The historical
static golden is REBASE_REQUIRED against current SSOT and was preserved.

No independent reviewer was created or dispatched.  Four pre-existing
untracked custody files remain untouched and unstaged.  SSOT/SPEC,
membership/readiness/release/activation/Human PASS, PathIR/Proof public
closure, and teul physical retirement remain open nonclaims.
