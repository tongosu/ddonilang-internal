# 2026-08-29 DDN V1 VC12 language-core collection authority W1

- Session: DDN V1제품마감Codex
- Role: existing V1 product single writer
- Authority: internal CURRENT v25.22.0 / RD-001~469; public SPEC v0.6.0
- Baseline: `7079dd0ff378e88eee7967f71a8f2435b14a506a`
- Fixed product/test HEAD: `2a83ec409fedd00b9f7642362fe55bf72f00b583`
- Fixed tree: `495be98ee6e5f35dd29b970bae151207f9b0ff6a`

## Result

VC12 was implemented with the Owner-approved internal placement. `Call` and the public spellings remain unchanged. `lang::runtime::list_new` is the construction authority; stdlib signatures keep syntax visibility without retaining provider ownership, tool execution consumes the shared helper, and work-cost registry custody follows the language-core group.

The existing P1-A supported-ingress pack/runner was extended by one user fixture. No new runner, checker, framework, or reviewer was created. The tracked WASM family was refreshed only after native GREEN and official freshness passed.

## Evidence

- RED-first provider ownership test: exit 1, `목록` remained in `list_function_sigs`.
- Registry fail-closed RED: `E_WORK_COST_REGISTRY_MISSING_CANDIDATE` until the provider group was represented in the sealed ledger.
- lang 365/365; tool 524/524.
- supported ingress native 6 / native-WASM exact 2 / tracked-WASM 9 / repeats 4 / partial summary 0.
- VC06 existing workflow: GREEN 7 / RED 0 / PRODUCT_GAP 4; exact native-WASM 11; repeats 3; freshness/local CRLF PASS.
- fixed-head focused authority 1/1, registry 1/1, freshness PASS, tracked-WASM parity PASS.

## Boundaries

- Fixed commit exact product/evidence paths: 10.
- SSOT diff 0; public SPEC diff 0; visible UI diff 0; public spelling diff 0.
- VC17 uncommitted custody was not modified or staged.
- New review task/worktree/branch: 0/0/0.
- Review bundle target: VC06 + VC12 + VC04 at one coherent fixed head.
- Status is implementation under review, not closure or membership/readiness/release/Human PASS.
