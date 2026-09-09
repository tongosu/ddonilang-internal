# Project Self-Bootstrap Prompt

> repo-local 사본. 원본: `I:\dev\template\PROJECT_SELF_BOOTSTRAP_PROMPT.md` (ERQ-20260706-002 해결 시 편입, 2026-07-06)

아래 지시문을 새 프로젝트에서 Codex, Claude, Gemini, 또는 웹 AI에게 붙여넣으면, 해당 프로젝트가 자기 상황에 맞게 AI 협업 구조를 설계/생성하도록 유도할 수 있다.

---

You are helping bootstrap an AI collaboration workflow for this project.

Goal:
Create a lightweight project-specific structure for multi-AI collaboration, SSOT, session deltas, ERQ, outputs, and web-only AI handoff. Prefer adapting to the existing project over forcing a fixed folder layout.

First, inspect the project if you can access files. If you cannot access files, ask for a brief folder listing and README.

This workflow must support four folder-native AI environments with the same rules:

- Codex Windows app
- Codex VS Code/plugin
- Claude Windows/Desktop app
- Claude VS Code/plugin

These folder-native agents should read/write the same project files, especially `AGENT_WORKFLOW.md`, AI instruction files, `ssot/`, and `work/_session_deltas/`.

For AIs that cannot access the folder directly, use the web-only handoff mode:

- provide SSOT excerpts, current Session Delta, ERQ excerpts, and the task through `WEB_AI_CONTEXT_BUNDLE`
- receive their answer as Proposal text
- do not treat the answer as canonical until Codex/user merges it into SSOT/ERQ/Session Delta

Do not overwrite existing files without explicitly saying what would change. If files already exist, update them conservatively or propose a merge plan.

Create or propose these artifacts, adapting names to the project:

```text
AGENT_WORKFLOW.md
AGENTS.md
CLAUDE.md
GEMINI.md
AI_COLLABORATION_PLAYBOOK.md or link to the shared one
ssot/ or project-appropriate SSOT folder
  README.md
  MODULE_ROUTING.md
  ERQ_TEMPLATE.md
work/
  _session_deltas/
    README.md
  _templates/
    SESSION_DELTA_TEMPLATE.md
_inbox/
inputs/
_archive/
```

Do not assume `outputs/` is always the right final artifact folder. First classify the project and design an artifact policy.

Examples:

- Code repo: `dist/`, `build/`, `release/`, `docs/`, `artifacts/`, or existing CI output folders may already define artifact locations.
- Business/document workspace: use domain folders such as `발표/`, `사업지침/`, `마케팅/`, `영업/`, `제품자료/`, plus a delivery/export folder only for copies.
- Research project: use `papers/`, `experiments/`, `datasets/`, `figures/`, `reports/`.
- Design/content project: use `assets/`, `drafts/`, `published/`, `campaigns/`.

Create an `ARTIFACT_POLICY.md` or add an Artifact Policy section to `AGENT_WORKFLOW.md` explaining:

- where reusable project assets live
- where delivery/export copies live
- what is canonical vs temporary
- how generated files are reviewed and promoted

Rules to encode:

1. Important decisions are continuously appended to `work/_session_deltas/YYYYMMDD_agent_session-name.md`.
2. Delivery/export folders are for delivery/review/export copies, not canonical truth. Their name must be project-appropriate.
3. Original inputs go to `_inbox/` and are not edited directly.
4. Work on copies in `inputs/` or agent work folders.
5. Canonical project facts go to SSOT.
6. Unverified claims, numbers, prices, policies, customer commitments, compliance claims, or roadmap commitments go to ERQ until verified.
7. Web-only AI output is treated as Proposal, not canonical fact.
8. Before moving many files, create a move plan and log source path, target path, reason, and hash.
9. Do not delete uncertain files; archive them.
10. Keep instruction files short. Put detailed rules in playbooks or SSOT guides.

If the project is a code repo:

- Preserve existing `AGENTS.md`, `CLAUDE.md`, `.github/`, and README content.
- Add AI code governance only if appropriate: PR template, AI use disclosure, reviewer question requirement, level-based AI scope.
- Do not disrupt build/test/source folders.
- Respect existing artifact folders such as `dist/`, `build/`, `target/`, `out/`, `release/`, `docs/`, and CI output paths.

If the project is a document/business workspace:

- Add Source Vault pointer rules.
- Add domain folder guidance.
- Add delivery-copy-to-domain-folder rules for reusable deliverables.

If the project is Google Drive or web-only:

- Create a `WEB_AI_CONTEXT_BUNDLE.md` template.
- Use handoff bundles instead of assuming live folder access.
- Tell the user which files need to be re-uploaded or re-pasted when SSOT changes.

Required final response:

1. Existing structure summary.
2. Proposed AI collaboration structure.
3. Folder-native AI support plan for Codex/Claude app and VS Code/plugin.
4. Web-only AI handoff plan.
5. Files created or files that should be created.
6. Files that already existed and should not be overwritten.
7. First `SESSION_DELTA` content.
8. Next actions.

When possible, implement the structure directly. When not possible, provide exact file contents.
