# CLI/PathIR atomic artifact output W9 handoff

## Authority and lineage

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` (`active`, whole-goal blocker 0).
- Live internal authority: SSOT v25.45.0 / RD-001~536.
- Root CURRENT SHA-256: `965ddee47d2e6bedfffa09f90548463eccb4f462da9cb7ec8d03b78daace6dbc`.
- Internal CURRENT SHA-256: `d7e48af95b77f797b1c5a439e441813ea42c48d347320637b4df8716156e77ad`.
- Public Language SPEC: v0.6.0; CURRENT SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`.
- Baseline: `ce7985edb342245c3e8ad5f9e820e4042e7abbc3`.
- Product fixed: `685167b906f303f44cb07ea03d145222691690a9`.
- Fixed tree: `263f812677a30965b1694904290bdb0428f9fb36`.
- Direct parent exact; merge count 0.

The v25.45 successor has no incompatible semantic impact on this reversible
internal output-publication correction. It does not choose a public PathIR
wire, command membership, executable name, package name, legacy duration, or
diagnostic spelling.

## User workflow changed

Before this fixed commit, the existing `symbolic prove-eq --out` and proof
certificate/report/rewrite output paths wrote directly to the final target.
A failure during output publication could therefore damage the predecessor
artifact or expose partial bytes.

The fixed product has one shared native artifact-output owner. It creates the
parent directory, writes and syncs a unique same-directory temporary file, and
atomically replaces the final target. A write, sync, injected pre-replace, or
replace failure removes the temporary candidate and preserves the predecessor
target. Process id and nonce affect only the private temporary filename and do
not participate in semantic identity.

Existing consumers converged on the shared owner:

- symbolic equivalence certificate output;
- proof symbolic-equivalence certificate output;
- proof relation certificate output;
- proof rewrite-chain output;
- proof verify/replay report output.

No certificate, proof, report, receipt, CLI option, or diagnostic schema was
changed.

## Exact product diff

```text
solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson
tool/src/artifact_output.rs
tool/src/lib.rs
tools/teul-cli/src/cli/proof.rs
tools/teul-cli/src/cli/symbolic.rs
```

The tracked WASM binary, JS, d.ts, and package bytes are unchanged. The
official freshness tool updated only the manifest source inventory because the
new cfg-non-WASM Rust source is a tracked product input.

## Product evidence

- Product-facing initial RED: the direct-write implementation plus injected
  pre-replace failure changed an existing target from `old` to `new`; focused
  test exit 1.
- Fixed atomic helper tests: 2/2 PASS.
- `ddonirang-symbolic`: 17/17 PASS.
- `ddonirang-proof`: 18/18 PASS.
- `ddonirang-tool --lib`: 538/538 PASS.
- Existing `symbolic_rational_expr_v1` product runner: PASS.
- Actual built CLI: symbolic certificate, proof certificate, rewrite, verify,
  replay all PASS with nested parent creation.
- Repeated symbolic/proof output: byte-identical SHA-256
  `2d9a3800080c7859ed1a457c62ac00b8ee82a754105f72a46e915162f510f024`.
- CLI temporary artifact residue: 0.
- Official tracked-WASM freshness: initial manifest inventory RED, official
  manifest refresh, final PASS.
- `git diff --check`: PASS.

The final risk mutation bypassed the atomic candidate and wrote the final
target before returning the injected failure. It reproduced RED exit 1 and
the exact `new` versus `old` corruption. Exact source restore returned
`tool/src/artifact_output.rs` to SHA-256
`58a4178e4438a369caf37b0adb7299f99a8c8988f4bf4bc9078e5ede0488ea58`,
then focused tests were 2/2 GREEN and freshness was PASS. Mutation residue is
0. The exact external runtime directory created for direct product execution
was removed after its resolved path and zero-temp-residue state were checked.

## C0 through C8 actual impact

| Gate | Current bounded state |
|---|---|
| C0 | Historical 28 tool + 63 teul = 91 command inventory remains custody. |
| C1 | `ddn.project-run.v1` and existing candidate commands remain reachable. |
| C2 | Shared parser/canon/preprocess authority unchanged. |
| C3 | No public command membership or executable naming changed. |
| C4 | Symbolic/proof output publication now has one shared native owner; other INTERNAL/DEFERRED teul custody remains. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | Certificate/report output bytes remain deterministic; failed publication preserves the predecessor and publishes no partial artifact. |
| C7 | Existing native/WASM/Windows candidate custody remains; tracked WASM artifact bytes are unchanged and freshness is PASS. |
| C8 | Public projection still excludes teul; SPEC-link, rights/SBOM/NOTICE and final release gates remain OPEN. |

## Anti-meta and review boundary

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED: symbolic/proof users no longer risk partial or predecessor-damaging --out publication
REUSED_TEST_COUNT: 6 existing product test/frontdoor families
NEW_INLINE_PRODUCT_TEST_COUNT: 2
NEW_TEST_ARTIFACT_COUNT: 0
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED: include this atomic-output correction in the next coherent CLI/PathIR fixed-head review bundle
ACTIVE_REVIEW_TASK_COUNT: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: existing rolling reviewer 01a04b17-66bb-7fa3-b827-53ad450005b4 only
REVIEW_DISPATCHED: NO
```

## Open slice-specific gates and nonclaims

The v25.45 PathIR exact checker/profile/schema/wire and public assumption ingress
remain `CONCRETE_DETAIL_GAP_DETECTED` for that slice only. SPEC history,
public `test`/`view`/`repl` membership, VC17 exact landing, final teul physical
retirement/deletion, P6 rights/SBOM/NOTICE, release authorization, and Owner
Human Smoke remain separately OPEN. None is aggregated into a whole-goal
blocked state.

This is not PathIR P1/ERQ closure, C0~C8 closure, teul physical retirement,
whole P0~P6 closure, V1 membership/readiness, release/publication/activation,
legal approval, Owner Human Smoke, or Human PASS.
