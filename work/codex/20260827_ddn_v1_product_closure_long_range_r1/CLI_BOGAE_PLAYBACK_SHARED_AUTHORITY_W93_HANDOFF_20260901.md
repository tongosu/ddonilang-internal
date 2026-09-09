# [DDN V1제품마감Codex -> Codex관리Work] CLI BOGAE PLAYBACK SHARED AUTHORITY W93 — handoff

## Fixed identity

- baseline: `52eaf5429214668b97c43ccec1bef1dfa9a3a0db`
- product fixed: `a9ce24fddf3af06217730464d1916bb493d953c5`
- fixed tree: `fc4a23d8ebf534ec08930e1fae30ba599831069c`
- direct parent: exact
- merge count: 0
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`

Live authority was rechecked read-only as internal SSOT v25.49.0 / RD-001~543
and public Language SPEC v0.6.0. The v25.49 successor impact on this vertical is
`UNAFFECTED`: the change introduces no language meaning, public spelling, command
membership, wire schema or SSOT/SPEC transition.

## Product change and value

The real Bogae playback manifest/viewer asset generator and `OverlayConfig`
authority moved from `tools/teul-cli` into the host-only shared `tool` product
module. `teul-cli` now consumes the shared implementation through a one-line
adapter. The existing generated HTML/JavaScript/manifest bodies were moved
line-for-line; visible copy and layout were not redesigned.

Exact product paths:

- `tool/src/bogae_playback_workflow.rs` (new shared owner)
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/bogae.rs`
- `tools/teul-cli/src/cli/bogae_playback.rs` (adapter only)
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

This is a reversible internal/deferred product-authority convergence. It does
not decide whether Bogae playback is a V1 public command. It reduces one real
49 KB private teul output/value/canonical asset authority to zero while
preserving the historical physical command custody.

## RED, mutation and GREEN

Baseline authority RED was concrete: the shared `tool` product had no
`bogae_playback_workflow` owner while the working generator and four executable
tests lived only under `tools/teul-cli`.

After the move:

- shared tool playback tests: 4/4 PASS
- retained teul live playback writer test: 1/1 PASS
- `teul-cli` test target compile (`--no-run`): PASS
- full `tool --lib`: 590 PASS + 2 pre-existing isolated-worktree environment
  failures because this worktree intentionally has no `docs/ssot` directory
- wasm32 tool check with `--features wasm`: PASS; the host-only module is not
  compiled into the WASM product
- official tracked-WASM freshness: initial RED on source file count/tree/list,
  manifest rebind, then PASS

Risk mutation `PLAYBACK_TITLE_AUTHORITY_BYPASS` changed the shared generated
title from `Bogae Playback Viewer` to `Broken Playback Viewer`. The exact shared
product test failed at the generated output assertion. After a stable LF
materialization baseline was established, the mutation was restored byte-exact
to SHA-256
`31751d0f2fb7db16804d9dc2a8edc88930d91fadb68a684e33a23150f154fb76`
and the exact test returned GREEN. Mutation residue is 0.

The existing three playback pack invocations were also run. They fail before
the moved generator is reached: two use legacy `run` options rejected with
`E_SHARED_RUNTIME_OPTION_UNSUPPORTED`, and one V25 source is rejected during
canonicalization for the historical prohibited term. These three fixtures are
`REBASE_REQUIRED`; they are not counted as product GREEN and are not attributed
to this line-for-line authority move.

## C0-C8 bounded status

| Gate | Actual state after W93 |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 identities remain custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` remains on the neutral lang/tool artifact; executable naming remains OPEN. |
| C2 | Shared canon/preprocess/runtime/value/artifact authority remains; Bogae playback asset authority is now an additional shared tool owner. |
| C3 | Approved required workflows remain reachable; public `test/view/repl` membership remains slice-local OPEN. |
| C4 | Migrated required workflows keep private teul fallback 0; this internal/deferred playback generator is now adapter-only in teul. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. Historical/internal packs still reference teul. |
| C6 | wasm32 compile and tracked-WASM freshness are GREEN; this host-only output module has no WASM semantic delta. |
| C7 | Prior P5 fixed `3e205ce8...` review `bc84d81d...` is `PASS_TARGET_BOUND`; W90-W93 successor source requires its own coherent target review. |
| C8 | Public projection/binary teul exclusion remains; physical teul deletion and final package retirement remain Owner-gated. |

## Anti-meta and review

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: Bogae playback output generation is now reusable from the shared tool product without teul private asset authority.
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
EXISTING_TEST_REUSED_COUNT: 5 focused Rust tests + tool regression + wasm compile/freshness
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
REVIEW_BUNDLE_TARGET: W90-W93 current-source coordinate/Windows custody plus shared Bogae playback authority
```

## Slice-local gates and nonclaims

- PathIR public physical registry/field/CLI spelling: frozen only for that slice.
- public `test/view/repl` membership: Owner gate.
- VC17 exact provider landing: Owner/adjudication gate.
- SPEC history alignment, legal, signing and distribution: respective gates.
- physical `tools/teul-cli` deletion: not authorized.

This handoff does not claim whole C0-C8 closure, repository-wide teul semantic
authority 0, physical retirement, P0-P6 closure, V1 readiness/release,
activation, legal approval, Owner Human Smoke or Human PASS.
