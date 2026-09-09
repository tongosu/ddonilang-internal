# CLI preprocessing authority W25-W27 coherent handoff

## Fixed lineage

- Authority: internal SSOT v25.47.0 / RD-001~543
- Public Language SPEC: v0.6.0
- W25 product: `3c09c7e41d2d6c9b5c4cf101e272c01f7d1f75e5`
- W25 handoff: `4ff914348644da96e1c3340f6da854d5196255da`
- W26 product: `f0f0755c535117fdb2054c73db89e2488d668586`
- W26 handoff: `2b407a36605dc1bbe734896f3da1c7091531f211`
- W27 product fixed: `e845e72b3f3a48bc96fed0926765b6ca16032180`
- W27 tree: `955b26e687a86732cc16d9a7b881c7c26db31fd5`
- Direct lineage: yes
- Merge count: 0

## Coherent product outcome

1. W25 made file metadata parsing/formatting a single `ddonirang-tool`
   authority and reduced the retained teul file-meta module to an adapter.
2. W26 moved aggregate legacy-frontdoor validation and metadata-aware canon
   input preparation into the shared tool preprocessing surface; retained teul
   consumes it without a private implementation.
3. W27 removed eight pass-through wrapper bodies from tool preprocess/canon.
   Legacy detection and language frontdoor preprocessing are now direct
   `ddonirang-lang` re-exports, while tool owns only the product-level aggregate
   ordering and metadata-aware preparation role.

Exact W27 product paths:

- `tool/src/preprocess.rs`
- `tool/src/canon.rs`

Private language preprocess/legacy wrapper count after W27: 0.

## Verification

- tool legacy boim rejection: PASS
- tool legacy hash-header canon rejection: PASS
- retained teul legacy root rejection through shared aggregate: PASS
- W26 supported-profile atomic canon: PASS
- W26 clean isolated `ddonirang` build: PASS
- W26 clean teul-only binary build: PASS
- new tests/packs/runners/meta-tests: 0

The attempted WASM-only test filter selected zero host tests and is not counted
as evidence. Existing tracked-WASM/P5 target-bound evidence is preserved but
not re-promoted by this bundle.

## Mutation

W27 temporarily reintroduced the private tool canon preprocessing wrapper.

- mutation SHA-256: `488c2b586beeed1b17e79d13babaf9d5b605d47fd5fc68c81a051803bec1551b`
- RED: `PRIVATE_LANG_PREPROCESS_AUTHORITY_REINTRODUCED`, count 1
- exact restore SHA-256: `e2598a2707ef8ee5645af541d97b5b946aaa04faf3bbdc58924fdea51a35b787`
- final private wrapper count: 0
- restored focused GREEN: PASS
- residue: 0

## Review request

- Existing rolling reviewer: `01a04b17-66bb-7fa3-b827-53ad450005b4`
- New reviewer/task/worktree/branch: 0
- Review target: W25-W27 preprocessing authority bundle at product fixed
  `e845e72b3f3a48bc96fed0926765b6ca16032180` and this handoff successor.
- Scope: owner counts, direct call graph, focused behavior, clean-target builds,
  mutation restore, product/protected diff boundaries.

## Gate impact and nonclaims

C2/C4 advance narrowly: migrated file metadata and frontdoor preprocessing
private semantic authority is 0. Bounded V1-required build/test/pack/publish
teul execution dependency remains 0. Public command membership, executable or
package naming, alias duration, test/view/repl public status, and physical teul
deletion remain OPEN.

This bundle is IMPLEMENTED_UNDER_REVIEW. It does not claim C0-C8 closure,
P0-P6 closure, PathIR public P1/ERQ closure, V1 membership/readiness/release,
activation, legal approval, Owner Human Smoke, or Human PASS.
