# Owner decisions for successor

## 권고 기본안

```text
REPOSITORY_MODEL: INTERNAL_PRIVATE_PLUS_NEW_PUBLIC_PROJECTION
EXISTING_REPOSITORY_DISPOSITION: KEEP_AS_INTERNAL_AND_CHANGE_TO_PRIVATE_AFTER_REMOTE_AUDIT
PUBLIC_REPOSITORY_CREATION: DEFER_UNTIL_R2_R4_PASS
PUBLIC_PROJECTION_SOURCE: CLEAN_SEALED_INTEGRATION_COMMIT_ONLY
PUBLIC_RELEASE_SOURCE: PUBLIC_SOURCE_ONLY
MASS_FOLDER_MOVE: NO
BRANCH_WORKTREE_DELETE: NO
HISTORY_REWRITE: NO
```

## Owner가 정해야 할 항목

### D1. 공개 repository 이름

- A `ddonilang` — 가장 간결하고 사용자 친화적. 기존 URL 충돌/이관 감사 필요. 추천.
- B `ddonilang-public` — 내부/공개 구분이 명확하지만 브랜드 URL이 덜 예쁨.

### D2. License

- A 오픈소스 license 선택 — 외부 기여·재사용 가능, 권리 audit 필요.
- B source-available/custom terms — 통제력은 높지만 생태계 친화성이 낮음.
- C license 미발행 — 법적으로 재사용 허가가 불명확하므로 public launch 차단.

R1은 license를 추정하지 않는다. asset/third-party dependency 권리 audit와 함께 Owner가 결정해야 한다.

### D3. 첫 public product 범위

- A Workbench + CLI + public SPEC + selected examples — 제품 이해가 쉽고 추천.
- B Workbench only — 간단하지만 CLI/WASM 동등성과 언어 프로젝트 정체성이 약해짐.
- C source crates only — 개발자용이지만 시제품 체험성이 낮음.

### D4. release integration baseline

- A 최신 프로그램을 명시적으로 통합한 새 clean release commit — 추천.
- B `905efb4a...` 즉시 사용 — projection은 되지만 W1C2/수학/R10 계보를 대표하지 않아 비추천.
- C shared dirty root snapshot — 공식 authority로 금지.

### D5. GitHub operation 시점

- A R2~R4 plain PASS 뒤 — 추천.
- B 지금 visibility/new repo부터 변경 — recovery와 공개 내용 검증이 없어 비추천.

## 다음 승인 문구 제안

```text
DDN_PUBLIC_REPOSITORY_SUCCESSOR_DIRECTION:
OPTION_A_INTEGRATED_RELEASE_BASELINE_AND_NEW_PUBLIC_PROJECTION

EXISTING_GITHUB_REMOTE_AUDIT_AUTHORIZED: YES_READ_ONLY_NETWORK
EXISTING_REPOSITORY_PRIVATE_CHANGE_AUTHORIZED: NO
NEW_PUBLIC_REPOSITORY_CREATION_AUTHORIZED: NO
PUBLIC_PUSH_RELEASE_AUTHORIZED: NO

NEXT_TASK:
DDN_RELEASE_INTEGRATION_CHECKPOINT_AND_PUBLIC_SELF_CONTAINMENT_R2
```
