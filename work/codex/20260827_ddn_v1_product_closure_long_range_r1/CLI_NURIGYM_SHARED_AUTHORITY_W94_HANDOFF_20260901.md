# [DDN V1제품마감Codex -> Codex관리Work] CLI NURIGYM SHARED AUTHORITY W94 — handoff

## Fixed identity

- baseline: `798ca52d6ca882664c326497b9144bd3d581d336`
- product fixed: `7532393a5aa99b112caa89459acb8d88d515a3ff`
- fixed tree: `64f67587594a7fe107719fea0a7bbbd9cd0689b5`
- direct parent: exact
- merge count: 0
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`

Live authority was rechecked read-only as internal SSOT v25.49.0 / RD-001~543
and public Language SPEC v0.6.0. The successor impact is `UNAFFECTED`: this
vertical introduces no language meaning, public command membership, executable
name, wire spelling, SSOT or SPEC transition.

## Product change and user value

The real NuriGym spec/view/episode orchestration, deterministic action merge,
step projection and artifact generation authority moved from the private
`teul-cli` module into the shared host-side `tool` product. The historical CLI
now consumes it through a one-line adapter. Existing core NuriGym environment
semantics and physical command spelling are unchanged.

Exact product/test paths:

- `tool/src/nurigym_workflow.rs` (shared owner; 74,699 bytes; SHA-256 `00c042872b0e16f62a9df3970ecc9c25bfa8b2f05a9528b2e02575bd830a12b1`)
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/nurigym.rs` (45-byte adapter; SHA-256 `cb18fe34027b086dd2fe8d59a8d4727f4885f8b60f1b54902693a94c560e176e`)
- `tests/run_creator_gaji_round4_fixed64_boundary_check.py` (existing source-owner assertion rebound)
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` (source custody only; SHA-256 `12a8171638ec2d06d4a744837ee2c8b19d71324a24bdbf5a1412dedee552eecb`)

This is reversible internal/deferred authority convergence. It does not promote
NuriGym into V1 public membership and does not add a WASM export. The host-only
module is excluded from wasm32 compilation while its source custody remains in
the tracked manifest.

## RED, GREEN and mutation

- baseline authority RED: 74 KB orchestration and 12 executable tests existed
  only in `tools/teul-cli`; shared `tool` had no NuriGym episode workflow owner.
- shared tool tests: 12/12 PASS after move.
- actual historical `teul-cli nurigym run` workflow: PASS; dataset hash
  `sha256:23338c8a83d4f72f46d228f353facc23d4327fd7dfec5b7abbb3169c2e640835`.
- repeat determinism: five emitted artifact files were byte-identical across
  two executions.
- shared-sync priority/tiebreak existing pack checker: PASS.
- `teul-cli` build: PASS.
- wasm32 shared tool check: PASS; host-only NuriGym module excluded.
- tracked-WASM freshness: source custody RED, manifest rebind, PASS.

Risk mutation `NURIGYM_PRIORITY_ORDER_REVERSED` inverted the stable smallest
`agent_id` precedence. The exact shared test failed with actual `1`, expected
`-1`. It was restored byte-exact to SHA-256
`00c042872b0e16f62a9df3970ecc9c25bfa8b2f05a9528b2e02575bd830a12b1`,
then the shared suite returned 12/12 GREEN. Mutation residue is 0.

Existing evidence drift remains separate:

- `nuri_gym_bandit_v1`: two stale expected dataset hashes; current outputs are
  deterministic but the historical golden is `REBASE_REQUIRED`.
- `nurigym_shared_sync_action_pipeline_v1`: stale expected hash,
  `REBASE_REQUIRED`.
- public-schema checker: Windows output decoding adds replacement characters;
  environment/runner drift, not attributed to the line-for-line authority move.

## C0-C8 bounded state

| Gate | Actual state after W94 |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 identity custody remains; no bulk promotion. |
| C1 | `ddn.project-run.v1` remains neutral and unchanged; executable naming OPEN. |
| C2 | Shared canon/preprocess/runtime/value/artifact owners remain; NuriGym orchestration is now an additional shared tool owner. |
| C3 | V1 required shared frontdoors remain; NuriGym is internal/deferred, not newly public. |
| C4 | Migrated required workflows retain private fallback 0; NuriGym teul implementation is now adapter-only. |
| C5 | Bounded V1 build/test/pack/publish required teul execution dependency remains 0; historical/internal packs still invoke teul. |
| C6 | wasm32 compile and tracked-WASM freshness PASS; no NuriGym WASM export was invented. |
| C7 | P5 fixed `3e205ce8...` review `bc84d81d...` and test-workflow review `18189658...` remain target-bound ancestors; W90-W94 source awaits coherent review. |
| C8 | Public projection excludes teul binary/package; physical deletion and final retirement remain Owner-gated. |

## Anti-meta, review and nonclaims

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: NuriGym deterministic episode/spec/view generation is reusable from shared tool without teul-private orchestration authority.
REUSED_TEST_COUNT: 12 Rust + 1 priority pack + actual CLI workflow + wasm compile/freshness
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
REVIEW_BUNDLE_TARGET: W90-W94 shared CLI authority and Windows/release custody successor source
```

`bogae_web` remains slice-local frozen because it is coupled to the 107 KB
private Bogae core/value conversion owner. PathIR public physical registry,
public `test/view/repl` membership, VC17 exact landing, legal/signing/
distribution and physical teul deletion remain their own gates.

This handoff does not claim NuriGym V1 membership, whole C0-C8 closure,
repository-wide teul semantic authority 0, physical retirement, P0-P6 closure,
V1 readiness/release, activation, legal approval, Owner Human Smoke or Human PASS.
