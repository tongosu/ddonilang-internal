# CLI replay-diff shared atomic authority W28 handoff

AI_PROVIDER: OpenAI
AI_SURFACE: Codex local task
AI_CAPABILITY: product single-writer implementation and validation
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure execution owner / file owner
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]

## Fixed identity

- baseline and direct parent: `3ef1a26feef575b3af8a954ce288d7f459a614c5`
- product fixed commit: `9e7f88ea3375b8cfa909d96b06dfc14d87ccc84a`
- product fixed tree: `3bc551b654a7637bf18fb515ce62795f88839448`
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- merge count: 0

Exact product paths:

1. `tool/src/lib.rs`
2. `tool/src/replay_diff.rs` (new shared product owner)
3. `tools/teul-cli/src/cli/replay_diff.rs` (one-line adapter)

Product/test/pack/WASM/UI/SSOT/SPEC changes outside these paths: 0.

## Authority

Filesystem live CURRENT was read-only reverified as internal SSOT
`v25.47.0 / RD-001~543`, Owner final 2026-08-31. Public Language SPEC remains
`v0.6.0`. This successor is `ADDITIVE` for the shared replay-diff ownership
and output transaction; it does not promote any later internal meaning into the
public SPEC. `docs/ssot/**` and `publish/spec/**` diff: 0.

The already-bound CLI test review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
and P5 target-bound review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda`
are both ancestors of this fixed commit. Their target-bounded scopes are not
broadened.

## User workflow and product change

Workflow:

`replay diff --a <run-a> --b <run-b> --out <dir>`

Before this slice the teul command owned manifest parsing, semantic comparison,
report rendering, and direct file publication. If `diff.txt` was blocked by a
directory, it returned exit 1 after already publishing `diff.detjson`.

W28 moves that complete comparison/report authority into
`ddonirang_tool::replay_diff`. The retained teul command only re-exports and
invokes the shared owner. The output set is prepared and synced before commit;
predecessor files are backed up, failures roll the set back, and success removes
the backups.

Observed product RED before implementation:

- blocked `diff.txt` target
- CLI exit: 1
- published `diff.detjson`: 1 (unsafe partial publish)

Observed product GREEN after implementation:

- equal inputs: exit 0, exact 2 files
- divergent inputs: exit 0, `equal=false`, `first_diverge_madi=0`
- `--no-summary`: exit 0, exact 1 file
- blocked summary target: exit 1 with
  `E_REPLAY_DIFF_OUTPUT_TARGET_NOT_FILE`
- blocked target published `diff.detjson`: 0
- staging/backup residue in product output: 0
- pre/post successful `diff.detjson` SHA-256:
  `079de8feea84c2d02c3969d43bc615e5b85420915efea66eefd70882f7c9dc36`
  (byte parity preserved)

## Tests and mutation

- shared replay-diff focused tests: 2/2 PASS
- teul-cli offline build on isolated target: PASS
- real CLI equal/divergent/no-summary/blocked-target cases: 4/4 PASS
- tool full lib regression: 547 PASS + 2 FAIL
- the two failures are the pre-existing isolated-worktree environment event:
  `ai_prompt_output_invariants_hold` and
  `ai_prompt_output_matches_golden` cannot read absent
  `docs/ssot`; new regression: 0

Risk mutation:

- mutation: disable target-kind preflight
- result: focused blocked-target test RED (exit 101)
- exact restore SHA-256:
  `1deb8df6546cae5901cf4f662cee5042ba5912dd5337ec5b118471a356927e73`
- restored focused GREEN: 1/1
- source mutation residue: 0

TESTS_REUSED: existing CLI command, existing Cargo tool test target, existing
replay-diff wire/output contract.

NEW_TEST_ARTIFACT_COUNT: 0. Two focused unit cases live with the moved product
module; no pack, runner, checker, or meta-test was created.

META_TEST_CREATED: 0.

## C0 through C8 bounded state

| Gate | W28 state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody. |
| C1 | `ddn.project-run.v1` and executable/package/alias gates unchanged. |
| C2 | Replay-diff manifest/comparison/render/output authority now has one shared tool owner. |
| C3 | Public `test`/`view`/`repl` membership remains OPEN; replay-diff public membership is not inferred. |
| C4 | Replay-diff private teul parser/value/report/fallback authority is 0; other INTERNAL/DEFERRED physical custody remains nonzero. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Replay comparison bytes remain stable and failed two-file publication now has partial publish 0. |
| C7 | Existing P5 fixed/review identities remain target-bound; W25~W28 need the next coherent rolling review. |
| C8 | Teul public binary/package retirement and physical deletion remain Owner-gated. |

## Anti-meta and next gate

USER_WORKFLOW_CHANGED_OR_UNBLOCKED: replay-diff can no longer report failure
after publishing only half of its result set, and the semantic owner is reusable
outside teul.

CHANGED_V1_GATE: shared replay/receipt authority and failure atomicity advanced;
whole P4/P5/V1 closure did not.

REVIEW_BUNDLE_TARGET: W25 file metadata + W26 aggregate guard + W27 direct
language reexports + W28 replay-diff shared atomic authority, using only the
existing rolling reviewer when management dispatches it.

ACTIVE_REVIEW_TASK_COUNT: 0 observed in this execution surface.
NEW_REVIEW_TASK_COUNT: 0.
NEW_REVIEW_WORKTREE_COUNT: 0.

NEXT_PRODUCT_DECISION_ENABLED: management may send one coherent W25~W28 fixed
bundle to the existing rolling reviewer while the writer continues a
non-overlapping approved internal convergence slice.

## Nonclaims

This is `IMPLEMENTED_UNDER_REVIEW`. It is not public replay command membership,
whole C0~C8 closure, whole P4/P5 closure, teul physical retirement/deletion,
PathIR public contract closure, VC17 landing, V1 readiness/release/activation,
legal disposition, Owner Human Smoke, or Human PASS.
