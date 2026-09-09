# DDN-LONG-RELINT-PRODUCT-01 public parity prerequisite conflict packet

## verified conflict

```text
OWNER_DECISION_PC02: INVERSE_EXACT_04566A24_PATCH_IN_SUCCESSOR
OWNER_DECISION_D7: PRESERVE_EXACT_LEAF_AND_CURATED_PARITY_DURABILITY
T5_HANDOFF_CONTAINS_PC02: YES
PC02_CHANGED_T5F_TO_EXPLICIT_PRE_V25_SOURCE: YES
CURRENT_T5F_FOUR_FAMILY_RUNTIME: RED_AT_GRID_RESULT_SET
PUBLIC_PARITY_FRESHNESS: PASS
PUBLIC_PARITY_VIEW_ONLY_STATE_HASH: PASS
PUBLIC_PARITY_TRUE_EQUALITY: RED
```

The true-parity equality root fails in exactly three legacy-view cases:

```text
c09_boim_structured_view
c11_show_and_boim_split
c13_bogae_draw_madi_view_sugar
```

Both native CLI and WASM reject these inputs during preprocess with
`E_BOIM_LEGACY_REMOVED`. This is not a CLI/WASM disagreement; it is a stale success
expectation relative to the exact PC02-excluded product surface. The existing audit
therefore refuses to issue its equality PASS, as it should.

PC02 commit `04566a24...` introduced the explicit pre-V25 WASM constructor and changed
the T5F runner to call it. The reviewed T5 final handoff `905efb4a...` contains PC02 in
its ancestry. Exact inversion removes both those product bytes and their test adaptation.
No narrow subset was silently retained in the integration successor.

## decisions not made by implementer

The implementer did not:

- restore `fromPreV25Source` or any hidden compatibility ingress;
- reinterpret the three legacy cases as current-success cases;
- remove true-parity from the D7 aggregate;
- change a failure expectation merely to make the aggregate green;
- claim T5 standalone closure, public conformance PASS, or release readiness.

## exact Owner choices needed for later closure

```text
OPTION_A_PRESERVE_EXACT_PC02_EXCLUSION:
  keep current product and aggregate RED; authorize a separately reviewed successor
  conformance contract only if legacy rejection is the intended public meaning.

OPTION_B_AUTHORIZE_NARROW_EXPLICIT_COMPATIBILITY:
  identify exact PC02-independent compatibility bytes, public/nonpublic status, and
  diagnostics; requires new product implementation and independent review because it
  narrows the prior exact-inverse direction.

OPTION_C_DEFER_PUBLIC_PARITY_AND_T5_STANDALONE_CLAIMS:
  preserve current integrated candidate for PC01 review and other custody work, but do
  not advance public conformance or release gates.
```

No option is inferred by this packet. Until a later explicit direction, the current safe
state is Option C behavior: preserve evidence and keep the gates open.

## independent blockers

The following remain independent of this semantic conflict:

- fresh PC01 targeted independent plain PASS;
- PC01 five-file pack rights confirmation;
- projectile lesson rights confirmation;
- offline Playwright Node package custody for the public browser roots.

```text
BLOCKED_BY_PC02_EXCLUSION_VS_PUBLIC_TRUE_PARITY_CONTRACT
PUBLIC_CONFORMANCE_PASS_NOT_CLAIMED
T5_STANDALONE_CLAIM_OPEN
PRODUCT_BYTES_PRESERVED
```
