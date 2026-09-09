# Editor Run hydration/order harness debt — Owner packet

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
AUDIT_HEAD: 9079d366a928907d6c1eed1f4df5a008b6ead8e8
SCOPE: EDITOR_RUN_HANDOFF_TEST_CONTRACT_ONLY
STATUS: BLOCKED_OWNER_EDITOR_RUN_HYDRATION_ORDER_CONTRACT
PRODUCT_CHANGE: 0
TEST_CHANGE: 0
```

## Reproduced facts

`seamgrim_editor_run_handoff_runner.mjs` and `seamgrim_editor_run_transaction_runner.mjs` contain two plainly stale preconditions:

1. the handoff fixture omits the current exact observation-manifest schema/version and therefore fails closed before producing the expected output row;
2. both runners search for exact `setScreen("run");`, while the product call is `setScreen("run", { shellSpace });` after `loadLesson` and `enqueueRunRequest`.

After correcting only those two preconditions locally, the handoff runner exposed a different contract conflict and remained RED:

```text
editor handoff: hydration must not block opening run screen
```

The current product awaits `lessonCanonHydrator.hydrateLessonCanon(baseLesson)` and only then calls `openRunWithLessonWithSource(hydratedLesson, ...)`. The historical runner expects Run to open first and hydration to proceed afterward. This is observable product sequencing, not a source-text formatting issue.

The two temporary test edits were restored exactly; current worktree residue is `0`.

## Owner decision required

Choose one behavior contract before this runner is corrected:

- `OPTION_A_AUTHORITATIVE_HYDRATION_BEFORE_OPEN`: preserve the current product sequence; update the runner to require completed authoritative hydration before Run handoff.
- `OPTION_B_IMMEDIATE_OPEN_ASYNC_HYDRATION`: preserve the historical non-blocking-open requirement; authorize a separate product change and browser/transaction verification for safe post-open hydration.

No recommendation is promoted here because the choice changes user-visible ordering and authority timing. Either option must continue to preserve the queued source snapshot, load/enqueue/screen order, failure visibility, and no retry-based auto-execute.

## Slice boundary

This Owner gate blocks only editor-run harness debt closure. It does not block T5G review custody, the already completed safe evidence corrections, or dependency-independent read-only audits. It does not authorize T5H product correction, SSOT/SPEC edits, Native implementation, or public ABI work.
