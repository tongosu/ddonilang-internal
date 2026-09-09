# [셈그림Codex -> 셈그림검증ClaudeCode] T5G fixed-product review current-successor 재발행

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
REVIEW_SCOPE: T5G_SCENE_CURRICULUM_CANONICAL_VIEW_PAYLOAD_R1
PRODUCT_FIXED_HEAD: f3e93a154d97838ae1885bf512265836183b747c
REVIEW_REQUEST_BASELINE: 9883371763dc54c87f91956519e6fb20167fed68
REVIEW_REQUEST_COMMIT: THIS_DOCUMENT_COMMIT
EXPECTED_PRODUCT_DIFF_PRODUCT_FIXED_TO_REQUEST_COMMIT: 0
REVIEW_MODE: FIXED_PRODUCT_HEAD_READ_ONLY_FROM_CURRENT_LINEAR_SUCCESSOR
ALLOWED_VERDICTS: PASS / PASS_WITH_FOLLOW_UP / REWORK
```

## Custody rule

Review the product state at exact `PRODUCT_FIXED_HEAD`. The request commit is a linear successor containing dependency-independent packs, tests, and custody documents only; it must have product, SSOT, public SPEC, and tracked-WASM diff `0` from the product fixed HEAD.

If a review commit is created from this request, make this request commit its direct parent and change only one new `REVIEW_RESULT.md`. Preserve that review commit on a separate immutable review branch. Do not modify product, test, pack, existing handoff, SSOT, SPEC, or WASM files.

The implementation successor may continue dependency-independent evidence work after this request. In that case the review branch and implementation branch diverge intentionally: bind the verdict to the implementation successor with a new documentation-only provenance commit that records the review commit, direct parent, report bytes/hash, verdict, and fixed product HEAD. Do not claim that such a diverged review commit can be fast-forwarded into the already advanced implementation branch. If Git ancestry inclusion is separately required, issue a new request at the then-current successor and freeze that branch until the review commit lands.

## Required T5G determinations

1. `semantic_view_payload.js` remains the sole canonical owner with no third abstraction.
2. scene-summary consumes only exact explicit primary canonical payload and does not invent graph/timeline/layer meaning.
3. curriculum-semantic-scene uses exact nested canonical payload and validated lesson/world/control/observation identity.
4. presentation/session fields do not enter canonical identity.
5. missing identity, unsupported schema, malformed payload, duplicate anchor, nested identity mismatch, ambiguity, and unknown status fail closed.
6. representative product `no_view` stays honest while the authoritative fixture proves `available`.
7. golden `2/2`, status matrix `14/14`, ordering `3/3`, mutation `5/5`, browser, representative curriculum, and T5B–T5F regressions reproduce.
8. state hash and storage drift remain `0`.
9. product, SSOT, public SPEC, and tracked WASM diffs from the fixed product HEAD to the request commit are `0`.
10. public ABI, stable wire, SSOT promotion, Web S0, Native readiness, and Human PASS remain unclaimed.

## Reproduction

Use the existing commands in `INDEPENDENT_REVIEW_REQUEST.md`, plus:

```powershell
git diff --name-only f3e93a154d97838ae1885bf512265836183b747c..HEAD -- solutions core lang tool tools/teul-cli
git diff --name-only f3e93a154d97838ae1885bf512265836183b747c..HEAD -- docs/ssot publish/spec '*.wasm'
git rev-list --count --merges f3e93a154d97838ae1885bf512265836183b747c..HEAD
git diff --check
git status --short
```

The dependent T5H product correction remains forbidden unless the verdict is exact plain `PASS` for `PRODUCT_FIXED_HEAD`.
