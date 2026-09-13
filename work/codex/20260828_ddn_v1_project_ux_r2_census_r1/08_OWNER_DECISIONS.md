# Owner decisions and open gates

## No immediate Owner Gate A/B

The census found conflicts, but did not find evidence that `차림새/가지잠금/글판` is already a public stable irreversible compatibility contract. Therefore:

```yaml
OWNER_GATE_A_MASS_MIGRATION: NOT_TRIGGERED_YET
OWNER_GATE_B_PUBLIC_COMPATIBILITY_CONFLICT: NOT_TRIGGERED_YET
OWNER_DECISION_REQUIRED_FOR_CENSUS: NO
```

If later public compatibility inventory proves such a contract, stop before product mutation and issue the corresponding Owner packet.

## Decisions deferred to later authorized slices

These are not blockers for the census or FD02A targeted review, but must be decided before their product surface lands:

1. exact `차림새` physical filename/encoding/schema and compatibility reader.
2. exact semantic versus descriptive field set and canonical order.
3. exact `글판` values, defaulting and diagnostics.
4. exact public `가지잠금` schema/wire and relationship to `ddn.lock.v0-local`.
5. resource binary representation and explicit `곳간` membership rules.
6. RecoveryCheckpoint limits and GC grace/retention constants.
7. candidate-to-product migration for existing localStorage payloads.

## Boundaries retained

```yaml
SSOT_CHANGE: 0
PUBLIC_SPEC_CHANGE: 0
PRODUCT_IMPLEMENTATION: 0
UI_CHANGE: 0
TRACKED_WASM_REFRESH: 0
PUBLIC_STABLE_WIRE: OPEN
PUBLIC_V25_DEFAULT: NOT_AUTHORIZED
PUBLIC_RELEASE: NOT_AUTHORIZED
ACTIVATION: NOT_AUTHORIZED
HUMAN_PASS: NOT_CLAIMED
```

## SSOT impact proposals

These are `PROPOSAL` only and are not edits or promotion requests:

- document a future project semantic-config owner for `첫글` and `글판`.
- keep user-facing `차림새`, `곳간`, `가지잠금`, `씨` names non-stable until exact authority review.
- preserve the boundary between docs-first SourceEpoch meaning and product-owned selection.
- preserve `ddn.lock.v0-local` as a local candidate rather than public stable wire.

`SSOT_IMPACT_PROPOSALS: 4 / PROPOSAL_ONLY / SSOT_MUTATION_0`

## Product architecture deltas

1. current dual root/config owner → future semantic 차림새 owner plus explicit compatibility reader.
2. caller-selected epoch → project-owned Rust-validated epoch.
3. JS/local multi-authority identity → Rust semantic snapshot authority with explicit recovery compatibility.
4. monolithic snapshot object → file/resource blobs plus small manifest and reachability GC.
5. source-only run binding → source/config/epoch/lock/resource execution envelope.

## Review custody

- Editable I1 remains `IMPLEMENTED_PENDING_REVIEW` and is not merged.
- R3N-FU01 review target and review parent are not changed.
- Census results may be used to write a fresh FD02A impact/review packet only.

## 2026-08-29 authority and decision correction

The historical statement that no immediate Owner gate existed is superseded for the two exact
semantic choices below. This audit does not answer them on the Owner's behalf.

```yaml
CURRENT_SSOT: v25.16.1
PUBLIC_SPEC: v0.6.0
V25_17_INDEPENDENT_REVIEW: PASS_BOUND_AS_CANDIDATE_ONLY
V25_17_PROMOTION: PENDING_OWNER_FINAL_PROMOTION
V25_19_STATUS: NOT_CURRENT_PENDING_INDEPENDENT_REVIEW
EDITABLE_I1_REVIEW: PASS_WITH_FOLLOW_UP
EDITABLE_I1_ADOPTION_DISPOSITION: ADOPTABLE_WITH_TARGETED_CORRECTION
```

### Owner questions

1. **Declared resource form:** Is V1 formal-project resource membership file-only, with
   directory declarations rejected, or are directory declarations admitted? If admitted,
   exact recursion, missing descendant, duplicate logical membership and reparse-point rules
   must be selected.
2. **SourceEpoch state matrix:** Must every formal project declare SourceEpoch? Select exact
   behavior for new formal project, formal omission, legacy omission, pre-V25 migration and
   standalone DDN. Hidden current/default, content sniffing and public-SPEC-version inference
   remain forbidden.

### SSOT clarification proposals

These are proposals only; no `docs/ssot/**` mutation occurred.

1. enumerate which execution-semantic configuration families and effective target/profile
   fields enter ProjectSemanticConfiguration identity;
2. define one root/frontdoor invocation-context algorithm across CLI/WASM/Workbench;
3. state that save failure exposes only old-complete or new-complete project state;
4. state the authoritative reopen behavior when stored identity and recomputed content differ.

Product policy can independently retain expected-head CAS, host symlink containment, private
CAS layout and recovery presentation details, provided it does not cross these semantic gates.
