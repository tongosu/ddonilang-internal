# CLI check/build shared legacy custody W103 handoff

Date: 2026-09-02
Status: IMPLEMENTED_PENDING_COHERENT_REVIEW

## Fixed identity

- Live authority: internal SSOT v25.49.0 / RD-001~543, Owner final 2026-09-01, product-open.
- Public Language SPEC: v0.6.0.
- Branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`.
- Direct parent: `043f329b61b823c3a8987121753c57e9a2009631`.
- Product/test fixed HEAD: `f9f85fe5a94a9ee90fae443f70c0286d0f79a691`.
- Fixed tree: `816a7d12f0e166838aa91979c5580845d32e8177`.
- Merge count: 0.

The later live CURRENT is additive for this internal physical convergence. No
new public meaning, command membership, executable/package name, alias period,
SSOT or public SPEC surface is inferred.

## User workflow and exact product diff

`teul-cli check --legacy-internal` and `teul-cli build --legacy-internal`
retain their internal/deferred custody behavior, but their parser, type/schema
validation and atomic schema publication now execute in the shared
`ddonirang_tool::source_frontdoor_workflow` authority. The teul module is a
four-line adapter and no longer imports the private teul AST, parser, runtime
error formatter, value type inference or schema writer.

The fixed commit changes exactly:

1. `tool/src/source_frontdoor_workflow.rs`
2. `tools/teul-cli/src/cli/check.rs`
3. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

The tracked WASM binary is byte-identical to its predecessor at 5,579,392
bytes / SHA-256
`6e62b09e7c1d7e312453d55d4a5f23e3c09681bb387844c53ff3892d322b068e`.
Only its source-freshness manifest changed because the shared Rust owner moved.
Product code outside the two Rust files, tests/packs, visible UI,
`docs/ssot/**` and `publish/spec/**` diff are zero.

## RED, GREEN and deterministic product evidence

- Parent RED: `tools/teul-cli/src/cli/check.rs` contained five direct private
  authority families (`frontdoor_parse`, private AST, private runtime error,
  local type inference and local schema publication). Fixed count: 0.
- Existing W03 check/build corpus: 3/3 PASS. The three unrelated W03 run cases
  remain the same existing failures and are not promoted.
- Actual `check` and `build` success, repeated three times: 6/6 PASS.
- Schema output is byte-stable across three executions:
  `a5b3cd84cabc492cfee81791cc7d9ab795f80f133c5d17ec1e39d583e6c30dae`.
- Duplicate symbol and type-flip failures: 2/2 exit 1, artifact count 0.
- Shared tool focused tests: 3/3 PASS.
- Shared tool full regression: 609 PASS + 2 environment failures. Both failures
  require the intentionally absent isolated-worktree `docs/ssot` directory in
  `ai_prompt` and are not product regressions.
- teul full regression: 1024 PASS + the same 9 pre-existing failures; new drift
  0. One schema-path unit moved from the teul adapter to the shared tool owner.
- Official tracked-WASM freshness: expected source-tree RED before refresh,
  then PASS after official build and manifest refresh.
- `git diff --check`: PASS.

Risk mutation: bypassing the duplicate-symbol guard produced actual unit RED
(exit 101). The source was restored byte-exact to SHA-256
`499eb8c0638269d9ddfef263e9f0a6a1b51476e3ef05c125bcfba675205e6cd3`
before the later cleanup-only test helper adjustment, and the final focused
suite was GREEN 3/3. Mutation residue is 0 and failure artifact publication is
0.

## C0-C8 actual status

| Gate | Current fixed-head status |
|---|---|
| C0 | Historical registry custody remains 28 tool + 63 teul = 91 identities; no bulk public promotion. |
| C1 | The audited core set remains 15. `ddn.project-run.v1` stays independent of executable/package naming. |
| C2 | Shared lang/tool parser, type/schema and atomic artifact owners are used for both check/build routes. |
| C3 | The official candidate remains reachable for 12/15 audited workflows. Public `test/view/repl` membership remains slice-local frozen. |
| C4 | Check/build private teul parser/runtime/value/schema fallback is 0. Other internal/deferred teul source families remain physical custody. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0; historical references remain custody. |
| C6 | Check/build success/failure/schema parity is PASS, deterministic repeat is PASS and partial publish is 0. |
| C7 | P5 fixed target remains `PASS_TARGET_BOUND`; W103 awaits a coherent current-source review bundle. |
| C8 | Public projection still excludes teul binary/package. Physical deletion and final retirement remain Owner-gated. |

Current bounded private teul consumer inventory is nonzero outside this slice:
`frontdoor_parse` 2 files, private parser module references 8, private AST 3,
private runtime 6, private core/value 12 and private canon 2. These overlap and
are inventory counts, not unique deletion targets or required dependencies.

## Anti-meta, review and nonclaims

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: check/build internal custody no longer enters a teul-private parser/type/schema authority.
NEW_TEST_ARTIFACT_COUNT: 0
NEW_TEST_CASE_COUNT: 2 focused product-risk cases; 1 existing schema-path case relocated to its shared owner
META_TEST_CREATED: 0
EXISTING_TEST_REUSED_COUNT: 7 evidence groups
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: W102 doc-build plus W103 check/build current-source CLI authority convergence
```

Slice-local frozen gates remain SPEC history, PathIR public physical contract,
public `test/view/repl` membership, VC17 exact landing, legal/signing/
distribution and physical `tools/teul-cli` deletion. They are not a whole-goal
impasse.

This handoff does not claim repository-wide teul semantic authority 0,
physical retirement, whole C0-C8 or P0-P6 closure, V1 membership/readiness,
release, activation, legal approval, Owner Human Smoke or Human PASS.
