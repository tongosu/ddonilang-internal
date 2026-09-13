# RD-457 shared product frontdoor handoff

## Fixed target

- Implementation base: `39915946971bef8df479169d8fef450e89982c90`.
- Product fixed: `e8ad0e815a2090d2628cb84c9641d17b3cc9ef95`.
- Product parent: `69414f2a52245d3a9740830ab7acd6d09a5cd7ea`.

## Delivered product behavior

`parse_module_directive_frontdoor_with_mode` is now the shared language
frontdoor for RD-457 module source. It preprocesses through the existing
frontdoor, uses lexer-backed directive parsing, preserves typed import/export
metadata, and parses only the remaining declaration tail through the existing
typed V25 parser. Directives do not enter the declaration AST or runtime-call
dispatch.

The product path is fail-closed: an invalid V25 declaration tail returns no
frontdoor result, and legacy brace directives are not converted.

## Evidence

- RD-457 focused tests: 6/6 PASS.
- Full `ddonirang-lang`: 374 unit + 11 DDL + 6 RD-457 + 4 V25 tests PASS.
- Offline language check and `git diff --check`: PASS.
- M1 metadata-drop mutation: RED → exact restore → GREEN.
- M2 legacy-brace silent-conversion mutation: RED → exact restore → GREEN.

## Open product-detail boundary

`tool::source_analysis` and its existing WASM endpoint use a versioned
structured request that has no approved module-registry input or module-metadata
output field. Routing an RD-457 success through that request would either drop
the metadata or add a new public wire field. Both are forbidden here.

`CONCRETE_DETAIL_GAP_DETECTED`: the owner of that versioned structured request
must provide an approved registry/metadata carrier before Native/WASM source
analysis can project this success. Runtime execution, receipt publication, new
CLI options, and a new WASM wire are unchanged in this unit.

## Next action

Do not change the Workbench generator until the structured Native/WASM contract
can carry the typed metadata. Its current legacy `쓰임 {}` / `드러냄 {}` output
therefore remains unmodified. This handoff is ready for independent review of
the bounded lang frontdoor behavior only.
