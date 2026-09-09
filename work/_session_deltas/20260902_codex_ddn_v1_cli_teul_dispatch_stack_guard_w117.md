# 2026-09-02 — DDN V1 CLI retained-dispatch stack guard W117

AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product implementation / internal QA
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: single product writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]

- Authority read-only: internal SSOT v25.50.0 / RD-001~551; public SPEC v0.6.0.
- Fixed product commit `9543297283c30b5533b01d71002966651bdd8f44`, direct parent `9e0ce0979dc54eb824b6e9dc07903aae0127041a`, tree `d96193949d435e6d4e6365951c54ddcaf9f965f7`, merge 0.
- Sole product path: `tools/teul-cli/src/main.rs`.  Retained dispatcher now uses a 32 MiB named worker stack; CLI spelling and public membership are unchanged.
- Existing retained `gaji plan` went from actual main-stack overflow RED to GREEN.  Existing gaji WASM parity, local-project graph native/WASM, focused gaji tests, and fresh offline teul check passed.
- Risk mutation 1 MiB stack: actual RED exit `-1073741571`; exact source restore SHA-256 `52BDC9F7A4B96E5BE7786FB27F197B59A306FF55781EFC8578C72B733D5481EB`; final GREEN and residue 0.
- New dependency/test pack/runner/meta-test/reviewer/worktree/branch: 0.  Tracked WASM/UI/SSOT/SPEC/publish changes: 0.
- C5 remains a concrete-detail gate because V1-required CI/script command membership is not versioned.  Broad teul semantic authority and physical retirement remain OPEN.
- Rights attribution is tracked separately; no publication/distribution/release/legal claim is made.
