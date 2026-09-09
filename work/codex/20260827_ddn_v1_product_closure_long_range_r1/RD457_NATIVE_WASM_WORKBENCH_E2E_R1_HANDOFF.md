# RD-457 Native/WASM/Workbench carrier handoff R1

## Fixed target

- Parent: `d5c93b98d969b19fd2f65e8f4804235b3cc4823d`
- Scope: additive internal versioned carrier only.
- Public source-analysis v1 is unchanged.

## Delivered behavior

- Native and tracked WASM accept a typed module registry supplied by the caller.
- The lexer-backed RD-457 frontdoor returns import/export metadata with UTF-8 byte spans.
- Missing registry evidence and brace-form legacy directives fail closed with no metadata or canonical-source success payload.
- The Workbench physics project now generates parenthesized RD-457 directives and routes its explicitly declared registry through the same WASM carrier.
- No generated physics template contains `채비 {`.

## Verification

- Native module carrier focused tests: 3/3 PASS.
- Direct tracked-WASM carrier call with emoji import and byte-span assertion: PASS.
- WASM freshness manifest rewrite and freshness check: PASS.
- JavaScript syntax checks for runtime bridge and Workbench modules: PASS.
- `run_ddn_project_workbench_boundary_matrix_check.py`: existing `running_file_change_fake_summary` assertion failed; it is outside this carrier's request/response path and is not used as a success claim.

## Mutations

- Registry-bypass mutation: RED; exact source restore SHA-256 `2ad2b734bc367783f23b239aa4ce015b57e8ed244979d1d88b02b5c895e551b3`; focused GREEN.

## Nonclaims

- This is an `INTERNAL_VERSIONED_PRODUCT_ABI_CANDIDATE`, not public WASM support, Language SPEC promotion, V1 readiness, release, or Human PASS.
