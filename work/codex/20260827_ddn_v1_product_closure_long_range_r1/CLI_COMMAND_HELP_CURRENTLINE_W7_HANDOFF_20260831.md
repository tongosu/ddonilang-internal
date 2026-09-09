# CLI command help current-line W7 handoff

## Authority and lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`active`).
- Live internal authority: SSOT v25.45.0 / RD-001~536.
- Root CURRENT SHA-256: `965ddee47d2e6bedfffa09f90548463eccb4f462da9cb7ec8d03b78daace6dbc`.
- Internal CURRENT SHA-256: `d7e48af95b77f797b1c5a439e441813ea42c48d347320637b4df8716156e77ad`.
- Public Language SPEC: v0.6.0; CURRENT SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- Baseline: `21ea100e13ece3eb66d40549a8eb0bb102f3c414`.
- Product fixed: `e55216cea383bbdfc582faf79a8bebe3da008cd1`.
- Fixed tree: `d044473fee7773146cc13b26be827d67e44f05ce`.
- Direct parent exact; merge count 0.

The v25.45 successor affects this slice additively: no public command
membership, executable name, legacy duration, SSOT, or public SPEC meaning was
selected.

## User workflow corrected

Before this fixed commit, the current candidate executable rejected an
existing command followed by an existing help flag. For example,
`ddonirang run --help` returned exit 2 with `E_CLI_OPTION_UNKNOWN --help`.

The fixed parser recognizes the already-existing `--help`, `--도움`, and `-h`
flags immediately after every already-existing candidate command and returns
the existing global help response. The nested existing `개발 정본 --help`
route is covered as well. Unknown commands remain fail-closed with
`E_CLI_COMMAND_UNKNOWN`.

This changes exactly:

```text
tool/src/bin/ddonirang.rs
```

It creates no command, public wording, public membership, executable name,
runner, pack, registry, or semantic authority.

## Evidence

- Focused binary unit suite: 10/10 PASS.
- Direct built candidate help matrix: 40/40 PASS.
- Unknown command plus help: exit 2, `E_CLI_COMMAND_UNKNOWN unknown`.
- V1 supported ingress: native 7, native/WASM exact 2, tracked WASM 10,
  official CLI positive 4 and negative 4 PASS.
- Seamgrim workflow contract: PASS.
- Seamgrim deploy artifacts check: PASS.
- `git diff --check`: PASS.

Risk mutation added `unknown` to the help allowlist. The focused test returned
RED because `unknown --help` was incorrectly accepted as `Help`. Exact restore
returned the source to SHA-256
`fa19239ae193141f571120e75c6620c7382e97bebc9e5231d27ee51ac7eec03a`,
then the focused test returned GREEN. Mutation residue is 0.

The broader workspace run reached product suites but the historical
`ddonirang-tool` binary suite retained two `ai_prompt` failures because this
isolated product worktree does not contain the read-only `docs/ssot` material
those tests load. No SSOT bytes were copied or modified to mask the environment
event. The focused product and frontdoor checks above are GREEN.

## C0 through C8 actual impact

| Gate | Current bounded state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody. |
| C1 | `ddn.project-run.v1` and existing candidate commands remain reachable; command help is now reachable. |
| C2 | Shared parser/canon/preprocess authority unchanged. |
| C3 | Candidate frontdoor usability improved; public `test`/`view`/`repl` membership remains OPEN. |
| C4 | INTERNAL/DEFERRED physical teul custody unchanged. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Existing source/diagnostic/state/artifact parity evidence unchanged. |
| C7 | Existing bounded native/WASM/Windows candidate evidence remains custody; this slice adds native CLI behavior only. |
| C8 | Public projection excludes teul; strict SPEC-link, rights/SBOM/NOTICE and final release gates remain OPEN. |

## Product value and review boundary

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: users can request help for every existing candidate command without a false option error
REUSED_TEST_COUNT: 4 product test families plus direct candidate execution
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED: validate the coherent CLI/CI/release-custody current line at one fixed head
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: W2-W7 coherent CLI/CI/release-custody bundle on existing rolling reviewer 01a04b17-66bb-7fa3-b827-53ad450005b4 only
REVIEW_DISPATCHED: NO
```

## Open slice-specific gates and nonclaims

The following remain locally frozen rather than being aggregated into a whole
goal blocker: SPEC history/link ownership, PathIR public wire/ingress contract,
public `test`/`view`/`repl` membership, VC17 exact landing, P6 rights/SBOM/NOTICE,
release authorization, and Owner Human Smoke.

This is not C0~C8 closure, teul physical retirement or deletion, whole P0~P6
closure, V1 membership/readiness, release/publication/activation, legal
approval, Owner Human Smoke, or Human PASS.
