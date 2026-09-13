# BOGAE-PROD-06 stale canonical view-binding guard handoff

- Product: `5391517c6e38b4c358de85d79a338f0771367f56`
- Tree: `b07771b5bf99f49db31985fba01b3fbe861eb37f`
- Parent: `a932574d231ddef53aa1fa082b51116b15de0b87`
- Scope: the existing `view_binding.canonical_payload_status` must equal the
  current canonical payload status before renderer projection.

A hash-valid payload whose binding said `unavailable` while its canonical line
payload was available previously rendered successfully. The focused runner
observed RED at `stale canonical view-binding status must fail before
projection`. Mutation M-A2 removed the status equality and reproduced that
RED. The renderer was restored byte-exactly to SHA-256
`f83bceb208dfbdb6dfe17a295c4e0c3a918cd0584ed72093c84ed1f59fb482d3`, Git
blob `5b6467d8c95b72d83a014f7d1d0918d815cd1192`, then GREEN.

GREEN gates:

- `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`
- `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js`
- `git diff --check`

This is partial PROD-06 stale-binding evidence. Full workspace/view/Bogae/
world hash and receipt closure remains open; no readiness, release, SSOT,
public SPEC, or Human claim is made.
