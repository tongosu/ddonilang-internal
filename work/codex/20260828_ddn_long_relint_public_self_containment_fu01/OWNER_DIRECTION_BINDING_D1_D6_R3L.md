# Public self-containment Owner direction binding — R3L

## 권위와 범위

```text
PERSISTENT_GOAL: DDN-LONG-RELINT-PRODUCT-01
PREDECESSOR_HANDOFF: 51f85622cd745dd19ea8e08041f835d7de4f6f74
PRODUCT_TEST_FIXED_HEAD: 91e56e597a920a8346e18bf68fa80afadf92d3aa
OWNER_DIRECTION_DATE: 2026-08-28
RESUME_SCOPE: INDEPENDENT_REVIEW_AND_READ_ONLY_CUSTODY_ONLY
PRODUCT_PUBLICATION_GATES_RESUMED: NO
PUBLIC_RELEASE_AUTHORIZED: NO
HUMAN_PASS_CLAIM_AUTHORIZED: NO
```

새 goal이나 새 의미 계보를 만들지 않는다. 이 문서는 `OWNER_DECISION_PACKET.md`의
D1~D6에 대한 Owner 입력을 기존 R3K 계보에 결속한다.

## 결속된 결정

| 항목 | Owner 결정 | 현재 집행 |
|---|---|---|
| D1 AI prompt | 첫 publication surface에서 제외. sealed public authority bundle은 successor로 이월 | R3K의 두 `ai-prompt` RED를 우회하지 않고 공개 membership에서 제외한다. 기능 재설계나 SSOT 대체는 하지 않는다. |
| D2 SPEC history | exact linked history를 tracked review-bound commit 뒤 포함 | 현재 10개 untracked history tree를 authority로 쓰지 않는다. 해당 commit 전까지 OPEN이다. |
| D3 rights membership | PC01 five-file, projectile lesson, `gaji/std_math`, unknown rights 모두 제외 | R3K projection에 추가하지 않는다. `gaji/std_math` 실제-package parity RED를 기대값 변경이나 synthetic fixture로 숨기지 않는다. |
| D4 license/NOTICE | draft inventory·notice만 허용. 법률 선택·release 승인은 별도 | 199행 inventory와 material 5개 누락을 그대로 보존한 draft만 작성한다. selected license와 required notice를 정하지 않는다. |
| D5 tracked WASM | full membership와 independent PASS 이후 candidate refresh만 허용 | 현재 refresh 0. final promotion은 계속 금지다. |
| D6 Workbench/browser | exact path·rights·offline bundle read-only audit만 허용 | R3L custody 원장을 작성하되 public membership, bundle seal, G31, publication을 발행하지 않는다. local cache는 release authority가 아니다. |

## 결정 뒤에도 남는 관문

```text
D2_TRACKED_REVIEW_BOUND_HISTORY_COMMIT: OPEN
D4_MISSING_LOCAL_LICENSE_MATERIAL: 5_OPEN
D4_LEGAL_SELECTION_AND_RELEASE_APPROVAL: REQUIRED
D5_FULL_MEMBERSHIP_AND_INDEPENDENT_PASS: OPEN
D6_PUBLIC_MEMBERSHIP: NOT_AUTHORIZED
D6_SEALED_OFFLINE_BROWSER_BUNDLE: OPEN
INDEPENDENT_REVIEW_VERDICT: NOT_ISSUED
PUBLIC_RELEASE: NOT_AUTHORIZED
HUMAN_PASS: NOT_CLAIMED
```
