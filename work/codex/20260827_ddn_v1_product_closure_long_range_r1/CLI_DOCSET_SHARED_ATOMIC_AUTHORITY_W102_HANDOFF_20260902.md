# [DDN V1제품마감Codex -> Codex관리Work] CLI DOCSET SHARED ATOMIC AUTHORITY W102 — handoff

## Execution custody

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex local product worktree
AI_CAPABILITY: product single-writer implementation and verification
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure single writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
CONTROL_OWNER: Owner / Codex관리Work
MANAGER: Codex관리Work
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: tool/src/docset_workflow.rs, tool/src/lib.rs, tools/teul-cli/src/cli/docset.rs, tracked WASM binary/manifest freshness family
REVIEWER: existing rolling reviewer 01a04b17-66bb-7fa3-b827-53ad450005b4; not dispatched by writer
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Authority and lineage

- Live internal CURRENT: SSOT v25.49.0 / RD-001~543.
- Shared-root CURRENT SHA-256: `bc508d45e053d8c8a84b08e8c1657bc6eec5e82c1ad4a04d12d7daf22dfec6fa`.
- Internal CURRENT pointer SHA-256: `18152cc386483481fdbba0efb0f9c57644c84f2b731c076b22fbc6b41dd312bb`.
- Public Language SPEC: v0.6.0; CURRENT SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- Baseline: `52c44f093fc00a5e4a1bc9fc7097c30fdb024cdb`.
- Product fixed: `cc6e15217d8e1bb0420b5c248fa2bf4a0d85e2f6`.
- Fixed tree: `87842e99a4da9fdc2ceeb2a473c35579dffe629e`.
- Direct parent: exact. Merge count: 0.

The v25.49 successor adds no relevant semantic change to this internal docset
artifact workflow. Existing review commits `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
and `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` are already ancestors of the
baseline. The latter binds P5 target `3e205ce816e47d29f6488bd86d029750e6afaaf5`
and handoff `ccaa7132e9192a26f003917ae4f2795482c4e74f` with
`PASS_TARGET_BOUND`, blocking finding 0. Reviewer-handle absence is therefore
not a current whole-goal blocker.

## Product change and user value

The actual `doc build` workflow previously kept its source registry, stable
entry naming, provenance, canonical JSON and hash calculation privately in
`tools/teul-cli`. It also created the final output directory and `entries/`
before reading all sources, so a missing source published a partial artifact.

W102 moves that complete build authority into host-only
`ddonirang_tool::docset_workflow`. The retained teul command is a consumer.
Publication now uses the existing shared
`write_directory_artifact_atomic` authority: all source reads and file writes
complete in a sibling staging directory before the final directory replacement.
The existing command spelling, schema, metadata, source list, entry naming and
successful output remain unchanged.

Exact product paths:

1. `tool/src/docset_workflow.rs` — new shared docset build/provenance/hash owner.
2. `tool/src/lib.rs` — host-only module export.
3. `tools/teul-cli/src/cli/docset.rs` — shared build consumer; historical
   doctest execution remains private custody.
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` — official
   source-custody refresh; no new docset WASM export.
5. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` —
   official source/artifact inventory refresh.

No new public command membership, executable name, package name, wire schema,
parser/canonicalizer meaning, visible UI, SSOT or public SPEC was introduced.

## RED, GREEN, parity and determinism

Baseline product-facing RED used the real retained command with the repository's
absent historical guide source:

- exit: 1, `E_DOCSET_SOURCE_READ`;
- final target existed after failure: YES;
- leaked material: `entries/` directory.

Fixed result for the same command and failure:

- exit: 1, same `E_DOCSET_SOURCE_READ`;
- final target exists: NO;
- staging residue: 0;
- partial result/state/outbox publish: 0.

A controlled 14-source fixture used tracked public documentation bytes only as
test inputs. Baseline and fixed successful artifacts were byte-identical for all
16 output files. Both reported
`sha256:74860334820c3cd6aa50109410912b97902804767e5b3c00ba1b72659170efb7`.
Three fixed repeats produced the same identity and left staging residue 0.

Risk mutation `DOCSET_PRECREATE_FINAL_TARGET` reintroduced final target
creation before staging. The real missing-source command returned exit 1 but
left the final target present (RED). The product source was restored byte-exact
to SHA-256
`1a057fb94418ea29dc3a825a92279e730cdd0fa4559a783f9de7f5779be5121b`;
the same command returned GREEN for the containment contract (target absent,
staging residue 0). Mutation residue is 0.

## Reused verification

- teul CLI build/check: PASS.
- shared directory artifact tests: 3/3 PASS.
- full private teul suite: 1025 PASS + the same 9 known predecessor failures;
  new failure 0.
- official tracked-WASM freshness: initial expected RED on source inventory,
  official build/manifest refresh, final PASS.
- controlled successful output parity: 16/16 exact; repeat determinism 3/3.
- `git diff --check`: PASS.
- new test/pack/runner/meta-test artifacts: 0.

Tracked refreshed WASM is 5,579,392 bytes with SHA-256
`6e62b09e7c1d7e312453d55d4a5f23e3c09681bb387844c53ff3892d322b068e`.
Fixed manifest Git blob `e2cc7c6de6cb40e1086da1943c441759bb603627`
is 28,916 bytes with SHA-256
`24463799e592e923378ea15ade2faa49815ef69c46be469a6bf9118a69aca159`.

## C0-C8 bounded status

| Gate | Actual state after W102 |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command identities remain bounded custody; no bulk promotion. |
| C1 | `ddn.project-run.v1` remains the neutral semantic identity; executable/package naming remains OPEN. |
| C2 | Shared canon/preprocess/runtime/value/artifact authority remains; docset build/provenance/hash is now an additional shared tool owner. |
| C3 | Approved required workflows remain reachable; public `test/view/repl` and doc command membership remain slice-local OPEN. |
| C4 | Migrated required workflows retain private teul fallback 0. Docset build private authority is 0; historical doc verify/doctest runtime custody remains. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. Historical/internal pack references remain custody. |
| C6 | Successful output parity is 16/16, failure partial publish is 0, and tracked-WASM freshness is PASS; no docset WASM surface was added. |
| C7 | P5 fixed target review is PASS_TARGET_BOUND. W102 remains IMPLEMENTED_PENDING_REVIEW until a coherent current-source bundle is assigned. |
| C8 | Public projection excludes teul binary/package; physical deletion and final package retirement remain Owner-gated. |

## Anti-meta and remaining gates

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: doc build failure is atomic and its build authority is reusable outside teul.
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
EXISTING_TEST_REUSED_COUNT: 5 gates (shared artifact tests, teul full suite, actual CLI failure, successful parity/repeats, official freshness)
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
REVIEW_BUNDLE_TARGET: current-source CLI/teul authority-zero convergence after management selects a coherent target
```

Slice-local frozen gates are unchanged: PathIR public physical contract, public
`test/view/repl` membership, VC17 exact provider landing, SPEC history,
legal/signing/distribution, and physical `tools/teul-cli` deletion. None is
reclassified as a whole-goal impasse.

This handoff does not claim whole C0-C8 closure, repository-wide teul semantic
authority 0, physical retirement, P0-P6 closure, V1 readiness/release,
activation, legal approval, Owner Human Smoke or Human PASS.
