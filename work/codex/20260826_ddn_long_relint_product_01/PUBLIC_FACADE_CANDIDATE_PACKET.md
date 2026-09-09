# Public facade candidate packet — not landed

```text
STATUS: CANDIDATE_ONLY
ROOT_PUBLIC_FILES_CHANGED: 0
LICENSE_FINAL_LANDING: NOT_AUTHORIZED
```

## README / QUICKSTART

Existing files remain inputs. A future public successor must verify that commands use only public-source paths, public CLI names, included WASM/runtime files, and selected examples. Internal build, official-store, SSOT and worktree paths are forbidden.

R1 projection의 facade reproducibility audit는 다음을 확인했다.

```text
BROKEN_ROOT_IMAGE_LINK: 1
MISSING_QUICKSTART_RUNNERS: 5
PRIVATE_PATH_AFFECTED_BUILD_OR_SERVER_COMMANDS: YES
DCO_POLICY_COMPLETE: NO
CURRENT_RELEASE_WORDING_ACCURATE: NO
```

정확한 path와 successor 요구는 `PUBLIC_FACADE_REPRODUCIBILITY_AUDIT.md`에 있다.

## LICENSE candidate gate

Preferred code license candidate is Apache-2.0. Do not create the root `LICENSE` until:

- code authorship and contribution origin are owner-attested;
- selected third-party licenses and notices are resolved;
- docs/assets/lesson licenses are separated;
- patent/trademark boundary is recorded;
- Owner authorizes final landing.

## NOTICE candidate inputs

- product copyright holder statement — OPEN
- bundled third-party packages actually present in release artifacts — OPEN
- required attribution/notice text — OPEN
- generated WASM/bindings provenance — OPEN
- wordmark and lesson/sample notices — OPEN

## SECURITY candidate inputs

- supported public versions — OPEN
- private reporting contact/channel — OWNER INPUT REQUIRED
- response expectation and disclosure policy — OWNER INPUT REQUIRED
- no secret or private fixture in public conformance/projected source

## CONTRIBUTING candidate policy

```text
CONTRIBUTION_POLICY: DCO_FIRST
DCO_VERSION: 1.1
SIGNED_OFF_BY_REQUIRED: YES
CLA_REQUIRED_INITIAL_PUBLICATION: NO
```

Contribution documentation must require public-source-only build/test reproduction and must not grant access or authority over internal SSOT, private evidence, activation, release, trademark or rights ledgers.

## SUPPORT candidate inputs

- support channel — OWNER INPUT REQUIRED
- supported product checkpoint versus stable release distinction
- security reports routed to SECURITY policy, not public issue by default
- no Human PASS or service-level promise inferred from tests

## CODE_OF_CONDUCT

Not required by the current owner-bound public scope manifest, but absent. Exact policy and enforcement contact remain Owner decisions.
