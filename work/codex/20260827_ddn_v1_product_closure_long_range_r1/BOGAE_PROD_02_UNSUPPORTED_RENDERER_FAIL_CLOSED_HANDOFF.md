# Bogae PROD-02 — unsupported renderer fail-closed handoff

## Fixed target

- product fixed commit: `7d0b742ebaa1daed14136c92962968c3f390fb10`
- product tree: `4dfc3705533083fcd60a91cccb582962048cefea`
- direct parent: `02961ed3b15672835dcd47c0d231a3af1ab3a579`
- merge commits: `0`
- authority read-only at implementation: internal SSOT `v25.72.0 / RD-001~598`; public Language SPEC `v0.6.0`

## Product behavior

`buildSemanticRenderModel()` now accepts only the existing supported renderer
families (`line`, `pendulum`, `projectile`, and `grid`). An empty, unknown,
case-contaminated, or line-like unknown family returns the existing
`canonical_unsupported` projection-failure shape with the existing canonical
unsupported diagnostic code. It does not select `lineModel`, a default model,
or a success canvas projection.

The failure is projection-local: the supplied semantic payload remains
structurally unchanged, and successful supported-family rendering remains
unchanged. The renderer reports the failure through its existing non-ready
model path; it does not throw or convert the failure into an empty success.

## Changed paths

- `solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js`
- `tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`

No SSOT, public SPEC, payload producer, renderer identity, semantic IR, or
tracked WASM path changed.

## Evidence

- canonical primary gate: `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs` — PASS
- supported renderer and unknown-family behavior are exercised in that runner.
  The negative matrix includes unknown, empty, line-like, case/prefix/suffix,
  and unsupported capability tokens; it asserts deterministic typed failure,
  no line/default model fields, no success canvas projection, and deep payload
  immutability.
- applicable Workbench regression:
  `python tests/run_seamgrim_view_only_state_hash_invariant_check.py` — PASS
- JavaScript syntax:
  `node --check solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js` — PASS
  and `node --check tests/seamgrim_workbench_semantic_view_renderer_runner.mjs` — PASS
- `git diff --check` — PASS before product fixed commit.

## Mutation M1 — restore unknown-to-line fallback

- mutated hunk: final unknown-family branch in `buildSemanticRenderModel()`
  temporarily returned `lineModel(payload)`.
- RED command: `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs`
- RED observation: `"unknown_renderer" must fail as an unsupported projection`
- fixed renderer SHA-256: `e4c09f36dbc935ca1e8b5556601c891dff2cdb0eeca0e913c4edf237537533fb`
- fixed renderer Git blob: `6be407326532b25649cdccfc5edcd238d20d22ea`
- restore: byte-exact SHA-256 and Git blob both matched the fixed values.
- GREEN command: `node tests/seamgrim_workbench_semantic_view_renderer_runner.mjs` — PASS

## Custody and nonclaims

- author and committer: `tongosu <tongosu@myarts.kr>`
- task-owned tracked diff after fixed commit: `0`; staged: `0`; push: `NO`
- this handoff is ready for fixed-target independent review only.
- it does not claim broader Bogae conformance, Native/WASM/Workbench parity,
  V1 support/readiness/release, activation, legal clearance, or Human PASS.

## Next queued vertical

`BOGAE-PROD-01` remains separate: removal of hidden view/channel selection in
the semantic payload producer is not part of this target.
