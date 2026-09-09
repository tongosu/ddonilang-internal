# CLI evolving-universe atomic directory authority W73 handoff

## Status and product value

- status: `CLI_EVOLVING_UNIVERSE_ATOMIC_DIRECTORY_AUTHORITY_W73_IMPLEMENTED_UNDER_REVIEW`
- user workflow: an `evolving-universe run` failure can no longer publish a partial W89 program, subject, certificate, or report into the requested output directory.
- this is an existing INTERNAL/DEFERRED versioned workflow; no public command membership or release promotion is inferred.

## Authority and exact lineage

- internal CURRENT: v25.47.0 / RD-001~543, read-only
- public Language SPEC: v0.6.0, read-only
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- baseline: `961e9da1402c08d072604da4a46769ab884f5f85`
- product fixed: `fdd2acda1b0e4129812bcda6b9b3bd0f015dd1c0`
- product fixed tree: `8dc0821ba0d3e1f3043b72b4142440ee80c5d44e`
- direct lineage: yes
- merge count: 0

Exact product paths:

- `tools/teul-cli/src/cli/evolving_universe.rs`
  - blob `7bbe782110af5d9a862b43b2df5d1dc552dfd2bd`
  - 8,946 checkout bytes
  - SHA-256 `e131a1c8ab8eaec93e3b17cc928ec3965d4f5418b9ac0d8f092db5345f5294cd`
- `tools/teul-cli/src/cli/cert.rs`
  - blob `689535713df3cbfec9bd35824b5d32ca8ee6583a`
  - 19,086 checkout bytes
  - SHA-256 `72a956825da5ddc3ae060fde0fc25dc9f3315e6312263566134e0b0db58b2951`

## Implementation boundary

The command now constructs the complete existing W99 result in a sibling staging directory through `ddonirang_tool::artifact_output::write_directory_artifact_atomic`. Only after evolution, policy evaluation, subject generation, deterministic seeded key generation, signing, certificate verification, recovery disposition, and report generation all succeed is the output directory replaced.

The cert adapter now separates physical staging paths from final logical identity/output paths. Existing direct cert callers retain their old behavior. The evolving-universe path seals and reports the final published subject/certificate path, so staging nonce paths do not enter the certificate bytes or stdout.

Unchanged:

- W99 policy schema, report schema, certificate schema and fields
- command and option spelling
- evolution/evaluation/certificate/recovery meanings
- public membership and executable/package identity
- docs/ssot, public SPEC, WASM and visible UI

## Product RED and fixed GREEN

Baseline fault: an existing output contained a blocking `cert` file. The command failed at key-directory creation after publishing:

- `w89/generated.ddn`: present
- `w89/evolve_meta.json`: present
- `change_subject.detjson`: present
- final report: absent
- result: partial publish

Fixed failure using the existing policy surface with an unattainable score threshold:

- exit 1 / `E_EVUNIV_UNSAFE_RULE`
- predecessor `previous.txt`: preserved
- W89 partial output: absent
- subject/certificate/report partial output: absent
- staging/backup residue: 0

Fixed success, same output path, two consecutive executions:

- exit: 0 / 0
- complete files: 7
- complete file hash set equality: exact
- stdout equality: exact
- final report and semantic identities: exact
- predecessor removed only on successful complete replacement
- staging/backup residue: 0

Stable file hashes:

- `cert/cert_private.key`: `a42451328fd562e6bc20462735e363aa313ffb32903be3630cb52514f55b342b`
- `cert/cert_public.key`: `96c22616e2570ea987d6beca88b12af4154b9e0ec6c7a10de9e72eb1f9071636`
- `change_subject.cert.json`: `9710a29bd2a4f108c02b77c3820dcd83844875264fb6ad52d0e2c5000c25cb9b`
- `change_subject.detjson`: `be0069097590855ec41ea81ad884524a9a8b58f5e3c49e694f438da69fbfc1c2`
- `evolving_universe_report.detjson`: `f928bacd735626aca2fd364377739430138d5b2c7b5a51f2666f36abe87bcf40`
- `w89/evolve_meta.json`: `d43b4bf6d53c3646df02279084d02d5d381cd579baeb2e9ad526fdb176118358`
- `w89/generated.ddn`: `b1f39f695c33ae9b72689be11aa4e15cdea74aeb4bfe1dbeea124cf9954e724a`

## Tests, mutation, and existing-gap classification

- product CLI build: PASS
- existing W95 certificate pack: 2/2 PASS
- actual cert verify on W73 output: PASS
- W73 success repeat bytes/stdout: PASS
- W73 fixed fault and clean fixed-head fault: PASS
- existing W99 report fields `new_rules`, `new_entities`, and `final_state_hash`: match current golden

Risk mutation: bypass staging by directing the existing builder to the final output directory.

- RED: `E_EVUNIV_UNSAFE_RULE` after `w89/generated.ddn` partial publication
- exact restore: evolving-universe source SHA-256 restored to `f861679362011b980baeef4ac29177b8bb37ac8ee48cff6247d9ab642865353a`
- GREEN: predecessor preserved, partial output 0, residue 0

The existing W99 runner is not reported PASS. Its generated source still uses the historical `=` definition surface, while current ingress requires an explicit profile and V25 `:=`; it stops at `E_SOURCE_PROFILE_REQUIRED`, and explicit v1-core-v25 then returns `E_V25_DEFINITION_MIGRATION_REQUIRED`. Its stored `evolving_universe_report_hash` is also stale relative to the current product result. These are pre-existing W99 migration/evidence gaps and are not rewritten or hidden by W73.

## Anti-meta, C0~C8, and review

- `NEW_PACK`: 0
- `NEW_RUNNER`: 0
- `META_TEST_CREATED`: 0
- existing test/corpus families reused: W95, W99, actual W99 product pack
- C2/C4: the retained adapter consumes the shared directory-artifact authority; no new private fallback
- C5: bounded V1-required teul dependency0 remains unchanged
- C6: this exact directory writer now has failure atomicity and deterministic complete output/stdout
- C8: physical teul source/binary/package custody remains; deletion approval not inferred
- native filesystem frontdoor: PASS for this seam
- WASM/Workbench: not applicable to this INTERNAL/DEFERRED filesystem writer; no parity claim
- new reviewer/task/worktree/branch: 0
- review bundle target: next coherent retained-CLI atomicity/authority milestone using the existing rolling reviewer only after management selection

## Nonclaims

This handoff does not claim W99 V25 migration closure, W99 golden promotion, independent PASS, public command membership, whole C0~C8 closure, teul physical retirement, P0~P6 closure, V1 membership/readiness/release, activation, legal approval, Owner Human Smoke, or Human PASS.
