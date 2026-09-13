# DDN-W1C2-I2-FU01A targeted 독립 재검토 요청서

```text
REVIEWER: 독립검증ClaudeCode
REVIEW_MODE: FIXED_HEAD_READ_ONLY
PRODUCT_TEST_FIXED_HEAD: 6d39254b6d2d6116b5839a3afffddb6ab40ce1ce
REQUIRED_REVIEW_PARENT: THIS_DOCUMENT_CONTAINING_HANDOFF_COMMIT
VERDICT_AUTHORITY: PASS / PASS_WITH_FOLLOW_UP / REWORK
CODEX_PLAIN_PASS_AUTHORITY: NONE
```

`REQUIRED_REVIEW_PARENT`는 이 요청서가 들어 있는 최종 문서 전용 commit 자체다.
그 exact hash는 commit 생성 후 Work 반환값으로 함께 전달하며, 검토자는 해당 commit을
직접 parent로 하는 읽기 전용 review commit만 만든다.

## 고정 artifact

- starting parent: `cb801ed576d2c7d4872b1b890e70b40edacc369e`
- prior product/test fixed: `f6be35616418b748b7201f9fcfa48c2524c8bcd4`
- evidence correction/product-test fixed:
  `6d39254b6d2d6116b5839a3afffddb6ab40ce1ce`
- original independent review: 25,884 bytes,
  `6ddddaa226ed80a200bb1a068bdfff61c638d138cce81a61519518f43b987ff8`
- evidence:
  `work/codex/20260824_ddn_execution_concurrency_w1c2_i2_follow_up_correction_w1/FU01A_TARGETED_REREVIEW_EVIDENCE.md`
- original FU01 handoff와 WASM matrix는 역사 artifact로 그대로 보존한다.

## 표적 검토

1. exact fault 12축이 각각 GREEN→실제 RED→raw 복원→GREEN인가?
2. 외부 Rust consumer가 injection builder에서 `E0624` compile-fail하고 외부 API와
   crate-root re-export가 0인가?
3. `c8fdd4...`와 `3fbf028...`가 서로 다른 절대 DB 경로라는 custody가 직접
   재현되며 task-owned official write가 0인가?
4. PID/port 단절이 FU01 시작 전 external drift이고 FU01/FU01A가 보호 process를
   종료하지 않았다는 command/code custody가 성립하는가?
5. UI source, tracked WASM, manifest, user-visible behavior diff가 각각 0인가?
6. ai_prompt 2건, canon LF, v24.44.1 bundle 부재가 baseline/current exact evidence로
   분리되고 live v24.53.0을 임의 대체재로 쓰지 않았는가?
7. handoff commit은 docs-only이고 선형이며 clean/staged 0, merge commit 0인가?

제품·테스트·문서·WASM·DB를 수정하지 않고 고정 HEAD에서만 재현한다. plain PASS가
발행되기 전 I2 CLOSED, W1 full closure, public stable surface/wire, activation, release,
Human PASS를 선언하지 않는다.
