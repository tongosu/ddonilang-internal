# DDN public repository Owner decision binding D1~D8

## binding authority

- FROM: Owner
- TO: Codex관리Work
- TASK: `DDN_PUBLIC_REPOSITORY_SUCCESSOR_R2`
- baseline: `c3c65ae27c598a78aae6123b4853532ed6351ed4`
- binding scope: repository model, public projection/release policy, contribution policy, rights custody separation
- not authorized: visibility change, repository creation, push, release, deletion, mass move, history rewrite

## D1 — repository identity

```text
PUBLIC_REPOSITORY_NAME: ddonilang
REPOSITORY_MODEL: INTERNAL_PRIVATE_PLUS_NEW_PUBLIC_PROJECTION
EXISTING_REPOSITORY_DISPOSITION: KEEP_AS_INTERNAL_AND_CHANGE_TO_PRIVATE_AFTER_REMOTE_AUDIT
```

## D2 — code license direction

```text
LICENSE_DIRECTION: OPEN_SOURCE
PREFERRED_CODE_LICENSE_CANDIDATE: Apache-2.0
LICENSE_DIRECTION_DECIDED: YES
LICENSE_FINALIZATION: OPEN_PENDING_CODE_ASSET_THIRD_PARTY_RIGHTS_AUDIT
```

Apache-2.0 text를 아직 제품/public tree에 착지하지 않는다. 코드 저작권자, 외부 기여, 생성물, 의존성, 문서와 asset 권리를 분리 감사한 뒤 Owner가 최종 확정한다.

## D3 — first public product scope

```text
LANGUAGE_RUNTIME
CLI
WORKBENCH
REQUIRED_WASM
WORKBENCH_RUNTIME
PUBLIC_SPEC
SELECTED_EXAMPLES
PUBLIC_CONFORMANCE_SUBSET
```

Workbench UI source만으로 범위를 충족했다고 보지 않는다. 실제 구동에 필요한 WASM binary/glue, local/server runtime frontdoor, 저장·재열기 최소 경로, 공개 conformance dependency closure가 함께 있어야 한다.

## D4 — projection/release source

```text
PUBLIC_PROJECTION_SOURCE: CLEAN_SEALED_INTEGRATION_COMMIT_ONLY
PUBLIC_RELEASE_SOURCE: PUBLIC_SOURCE_ONLY
DIRTY_WORKTREE_PUBLIC_AUTHORITY: NO
```

## D5 — GitHub operation timing

```text
LOCAL_PUBLIC_PROJECTION_DRYRUN: AUTHORIZED_NOW
EXISTING_GITHUB_REMOTE_AUDIT: AUTHORIZED_READ_ONLY
EXISTING_REPOSITORY_PRIVATE_CHANGE: NOT_AUTHORIZED_YET
NEW_PUBLIC_REPOSITORY_CREATION: NOT_AUTHORIZED_YET
PUBLIC_PUSH: NOT_AUTHORIZED_YET
PUBLIC_RELEASE: NOT_AUTHORIZED_YET
```

## D6 — contribution policy

```text
CONTRIBUTION_POLICY: DCO_FIRST
DCO_VERSION: 1.1
SIGNED_OFF_BY_REQUIRED: YES_FOR_EXTERNAL_CONTRIBUTIONS
CLA_REQUIRED_INITIAL_PUBLICATION: NO
CLA_RECONSIDERATION_GATE: ORGANIZATION_OR_HIGH_RISK_CONTRIBUTION_NEED
```

## D7 — public main and release separation

```text
PUBLIC_MAIN_POLICY: VALIDATED_PUBLIC_DEVELOPMENT_CHECKPOINT
RELEASE_TAG_POLICY: USER_RECOMMENDED_STABLE_CHECKPOINT
MAIN_IS_RELEASE: NO
RELEASE_REQUIRES_SEPARATE_RECEIPT: YES
```

public `main`은 검증된 개발 checkpoint다. 사용자가 권장할 stable checkpoint는 별도 tag/release receipt와 artifact identity를 가져야 한다.

## D8 — rights custody separation

```text
CODE_RIGHTS: SEPARATE_LEDGER
DOCS_RIGHTS: SEPARATE_LEDGER
ASSET_RIGHTS: PER_ASSET_LEDGER
THIRD_PARTY_RIGHTS: SBOM_AND_LICENSE_LEDGER
UNKNOWN_RIGHTS_DEFAULT: EXCLUDE_FROM_PUBLIC_PROJECTION
```

코드 license가 문서와 상표·logo·lesson/media asset의 이용 조건을 자동 결정하지 않는다.

## protected operations

```text
MASS_FOLDER_MOVE: NO
BRANCH_WORKTREE_DELETE: NO
HISTORY_REWRITE: NO_UNLESS_CONFIRMED_SENSITIVE_DATA_INCIDENT
```
