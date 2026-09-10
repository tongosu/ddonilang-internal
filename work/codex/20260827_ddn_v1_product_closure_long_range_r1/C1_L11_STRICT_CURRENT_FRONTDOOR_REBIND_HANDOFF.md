# C1-L11 strict-current frontdoor rebind handoff

## Immutable predecessor custody

`764a5b4a4a5319ae2183bfda433170aacf3aebdb` is retained unchanged. Its
body records the parser-only fixed predecessor `269460066f1f7030e0552437bf003423a1a1613b`.
That predecessor remains valid evidence for the lexical strict-rejection guard,
but it is not the final product target after the source-built WASM projection.

## Current Blocker 2 fixed binding

- Product commit: `23f1a319553a0b8ac333aaae3dad4451eaef9209`
- Product tree: `5193995c792158d9a1df4e04dcff891b72a55c7d`
- Product parent: `72b78f078967251e84ab311b4a6a83cd4533166d`
- Handoff predecessor: `764a5b4a4a5319ae2183bfda433170aacf3aebdb`
- Merge commits: `0`

The fixed target preserves the lexer-backed strict V25 rejection of brace-form
`쓰임 {}`, `드러냄 {}`, and `공개 {}` before current project graph/linking;
it also rematerializes the tracked WASM and manifest from the same source tree.
The parenthesized RD-457 directive path remains the current accepted path.

## Current revalidation

- `v25_current_frontdoor_rejects_legacy_l11_brace_blocks_without_lexical_false_positives`: PASS.
- `current_project_run_rejects_legacy_l11_before_runtime_publication`: PASS.
- Both evidence paths reject with `E_V25_DEFINITION_MIGRATION_REQUIRED`.
- String/comment occurrences remain non-semantic and do not trigger rejection.

## Current successor relationship

The later Workbench product correction is
`126f730b396f5817c646f255ab1cc9b95c8c4fa5`, followed by its direct
handoff `559a00452592c657520a970c6c576be4b61b030f`. It does not replace
the Blocker 2 target: it aligns Workbench project preflight and VM execution
with the already-fixed strict current frontdoor.

## Nonclaims

This rebind corrects target identity only. It is not independent review or a
claim of C1-L11 closure, V1 readiness, release, activation, legal clearance,
or Human PASS.

READY_FOR_INDEPENDENT_REVIEW=YES
