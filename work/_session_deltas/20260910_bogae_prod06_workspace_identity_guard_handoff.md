# BOGAE-PROD-06 Local Workspace identity guard handoff

- Product: `165ada5b7ebb41a484eb21daf142580bb6d5dda9`
- Tree: `f38a0d032775a52d164fd56c24240143ef8f2c6a`
- Parent: `681881f5fb43bf2a924bc9cbea85a99ba1763f50`
- Scope: existing `project.id` is carried as `committed_frame.workspace_identity`
  in the internal semantic-view candidate payload and is required before
  renderer projection.

The pre-implementation focused runner observed RED at `committed frame did not
bind the existing Local Workspace identity`. A mutation removed the workspace
identity check and reproduced RED at `missing Local Workspace identity must
fail before projection`. The renderer was restored byte-exactly to SHA-256
`1e25d080653057fc6c0eb132318e33821049be783c819a31acc0444ccc9085bc`, Git
blob `e93e87473a9b5fa4be244b0891c25e382669bd86`, then GREEN.

GREEN gates:

- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js`
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js`
- `git diff --check`

This is a partial PROD-06 guard, not the complete Local Workspace/View/Bogae/
world hash-and-receipt firewall. It is not yet offered as a full Unit A review
target and makes no readiness, release, SSOT, public SPEC, or Human claim.
