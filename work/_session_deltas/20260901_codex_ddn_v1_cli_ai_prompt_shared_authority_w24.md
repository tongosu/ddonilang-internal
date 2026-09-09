# 2026-09-01 DDN V1 CLI AI-prompt shared authority W24

## Identity

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex local task
AI_CAPABILITY: product single-writer implementation and verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure execution owner / file owner
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
GOAL_STATUS: ACTIVE
```

## Change

- Reused the existing branch/worktree; new goal/task/branch/worktree/reviewer 0.
- Exported the host-only tool AI-prompt implementation as
  `ddonirang_tool::ai_prompt`.
- Made the tool binary and retained teul adapter consume that single owner.
- Replaced the teul 510-line private implementation with an 8-line adapter.
- Changed shared arguments to typed `PathBuf` custody.
- Routed file output through the shared atomic artifact writer.

## Fixed identity and evidence

```text
BASE: 37f276e63680e9f86a17c4b4c525cbb888c66a5b
PRODUCT_FIXED: a4fc1e2399ebf48e92eed8c3cc0ddb796260e71e
PRODUCT_TREE: 2766ac13ecf0ce4b1aa78950035d7b4527d6fef0
CHANGED_PRODUCT_PATHS: 4
DIRECT_LINEAGE: YES
MERGE_COUNT: 0
```

Both native frontdoors emitted 1,246,037 identical bytes with SHA-256
`368adea6e6899da13b4a1be7e8911fd35961067cdec2d21a302c5e9f995efcec`.
Unknown profile and invalid output target failed closed with artifact/temp
residue 0. Five focused shared-owner/atomic tests passed. One private-authority
mutation RED was restored byte-exact to GREEN with residue 0.

## Custody and nonclaims

Current authority is internal SSOT v25.47.0/RD-001~543 and public SPEC v0.6.0,
read-only. Four pre-existing task-owned untracked deltas remain byte-identical
and unstaged. Shared dirty root, `docs/ssot/**`, and `publish/spec/**` were not
modified.

W23+W24 are ready for the existing rolling reviewer as one coherent bundle.
No public command membership, executable/package naming, PathIR public closure,
VC17 landing, physical teul retirement, V1 readiness/release/activation/legal
or Human PASS transition is claimed.
