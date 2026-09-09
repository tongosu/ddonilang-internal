# Canonical View non-dependent evidence housekeeping — implementation result

```text
PROGRAM_ID: DDN_PRODUCT_LONG_RANGE_CANONICAL_VIEW_CONVERGENCE_R1
BASELINE_HEAD: f90c3d08cc8a665341214c3b34bf23f768c06618
EVIDENCE_FIXED_HEAD: dc0b4129f4ce5c6ebd8a4a61d80c4f112984c6fd
DEEP_RESEARCH_CHECK: NOT_USE
PRODUCT_SOURCE_CHANGE: 0
SSOT_SPEC_WASM_CHANGE: 0
```

## Corrected evidence gaps

### T5D unsupported text-format golden

The prior independent T5D review found a non-blocking golden coverage gap: the product already rejected `seamgrim.text.v0` with `format: "html"`, but the exact result was not owned by the pack.

- classification: `EVIDENCE_GAP`
- added exact golden: `expected/text_unsupported_format.payload.detjson`
- exact status: `invalid`
- exact code: `E_CANONICAL_TEXT_INVALID_CANDIDATE`
- exact reason: `text_format_invalid`
- mutation M4 changes the golden reason and proves `GREEN -> RED -> GREEN`
- product meaning change: `0`

### T4f mutation-runner newline precondition

The T4f product runner was already green. Its mutation runner used an LF-only source anchor and therefore failed before mutation on a Windows CRLF checkout.

- classification: `HARNESS_PRECONDITION`
- correction: derive the anchor and mutation newline from the checked-out source
- source newline observed: `CRLF`
- mutation RED: semantic-synthesis mutant detected
- compile errors counted as RED: `false`
- restore: byte-identical SHA-256 `3e5a4a6987579ce6fe9e7816542c0a1097672483cd2a4ae65a724d37e16f1de0`
- residue: `0`

## Verification

```text
T5D golden runner: PASS / unsupported_text_format_golden=1
T5D mutation runner: PASS / 4 mutations / residue 0
T4f product runner: PASS
T4f mutation runner: PASS / CRLF / RED -> restore GREEN / residue 0
T5H aggregate: PASS / 13 of 13
T5I payload-shape pre-audit: PASS / 14 of 14
git diff --check: PASS
clean-detached dc0b4129: PASS
```

The first detached invocation used the repository root rather than the detached worktree as `cwd`; runners that intentionally bind `process.cwd()` therefore reported a missing fixture. It was classified `HARNESS_PRECONDITION`, and the same fixed HEAD passed when invoked with the documented worktree cwd. No artifact or expected value was changed in response.

## Boundary

This correction does not close T5G, authorize T5H product changes, implement Native rendering, or define a public ABI. It is ready for a narrow read-only targeted review of the two test/evidence corrections.
