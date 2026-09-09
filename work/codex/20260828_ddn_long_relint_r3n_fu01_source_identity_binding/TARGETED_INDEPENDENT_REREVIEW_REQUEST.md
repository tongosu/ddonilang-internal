# R3N FU01 targeted independent rereview 요청

## 대상

```text
TASK: DDN-P-LONG-RELINT-R3N-FU01-SOURCE-IDENTITY-BINDING
PRODUCT_TEST_FIXED_HEAD: 9389563e752fcc63b0425e05671473e1adb42ced
PRODUCT_TEST_FIXED_TREE: bb48137289d0a2907039f902451764ad0a61e060
REQUIRED_REVIEW_PARENT: 이 문서를 담은 handoff commit
PREDECESSOR_REVIEW_COMMIT: 614d1b5f5ee77036fa84077bd18d899e1a6d5839
PREDECESSOR_VERDICT: PASS_WITH_FOLLOW_UP
```

review-report parent와 product execution target은 서로 다른 개념이다. Reviewer는 이
문서 commit이 아니라 `PRODUCT_TEST_FIXED_HEAD`의 clean-detached checkout에서 candidate와
projection을 모두 생성해야 한다. Handoff/review 문서 commit에서 candidate를 빌드해 fixed
product projection에 주입하지 않는다.

## 필수 검토

1. `substitute-projection`이 어떤 projection output에도 쓰기 전에 candidate/projection
   source commit과 source tree를 exact 결속하는지 확인한다.
2. artifact bytes가 같은 docs-only successor, candidate/projection commit/tree 변조,
   missing/malformed identity, semantic receipt 변조를 직접 공격한다.
3. mismatch 진단과 artifact/manifest/tree/receipt/partial-output 원자성 0을 확인한다.
4. official entrypoint로 fixed HEAD candidate A/B/C를 만들고 artifact set과 receipt identity
   A == B == C, internal path 0을 확인한다.
5. `R3N_FU01_115_OFFSET_BIJECTION.detjson`의 115행을 원본 WASM byte offset/slice hash와
   전수 대조하고 candidate occurrence 1, unknown 0을 확인한다.
6. `tests/run_r3n_fu01_cli_attacks.py`가 15개 각각을 실제 subprocess로 호출하는지 감사하고
   15/15 RED→exact restore→GREEN을 독립 실행한다.
7. FU01 manifest로 product fixed HEAD projection을 생성하고 같은 HEAD candidate만 주입해
   895/895, role 18, unscanned 0 및 A/B tree/receipt identity를 확인한다.
8. Python 61/61, source/projection lib 517/517, binary 405 PASS + 동일 ai-prompt RED 2,
   G14 3/3, SPEC raw blob 29/29를 재현한다.
9. R3L ledger/NOTICE bytes와 tracked WASM/UI/SSOT/SPEC/official DB 보호 경계를 확인한다.

## 봉인 입력

- result: `R3N_FU01_SOURCE_IDENTITY_BINDING_RESULT.md`
- projection manifest: `PUBLIC_PROJECTION_R3N_FU01_MANIFEST.detjson`
- offset ledger: `R3N_FU01_115_OFFSET_BIJECTION.detjson`
- CLI ledger: `R3N_FU01_DIRECT_CLI_ATTACKS.detjson`

허용 verdict는 `PASS / PASS_WITH_FOLLOW_UP / REWORK`다. plain PASS 전에는 R3K/R3L/R3N
제한 범위 closure, tracked refresh, public membership, publication, release, activation 또는
Human PASS를 발급하지 않는다.
