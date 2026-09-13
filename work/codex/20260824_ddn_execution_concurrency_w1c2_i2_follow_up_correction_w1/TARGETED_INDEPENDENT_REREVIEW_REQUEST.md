# DDN-W1C2-I2-FU01 targeted 독립 재검토 요청서

## 검토자와 경계

```text
REVIEWER: 독립검증ClaudeCode
REVIEW_MODE: FIXED_HEAD_READ_ONLY
VERDICT_AUTHORITY: PASS / PASS_WITH_FOLLOW_UP / REWORK
CODEX_PLAIN_PASS_AUTHORITY: NONE
```

검토자는 제품·테스트·문서·tracked WASM을 수정하지 않고 새 격리 worktree에서 직접
재현한다. 기존 `PASS_WITH_FOLLOW_UP` 원본과 commit을 다시 쓰지 않는다.

## 고정점

- starting parent/review commit: `c21c6820ba9ae936f029accaa3757490a4a80fa4`
- correction commit: `556f63d59963a7bf13b5d6b5425775dc00cf10e8`
- product/test fixed HEAD: `f6be35616418b748b7201f9fcfa48c2524c8bcd4`
- handoff commit: 이 요청서를 포함하는 문서 전용 successor commit
- prior report: 25,884 bytes / `6ddddaa226ed80a200bb1a068bdfff61c638d138cce81a61519518f43b987ff8`
- implementation handoff: `work/codex/20260824_ddn_execution_concurrency_w1c2_i2_follow_up_correction_w1/IMPLEMENTATION_HANDOFF.md`
- WASM matrix: `work/codex/20260824_ddn_execution_concurrency_w1c2_i2_follow_up_correction_w1/WASM_REPRODUCIBILITY_MATRIX.md`

## 표적 질문

1. 세 injection builder가 외부 crate에서 호출 불가능한 `pub(crate)` 이하이며 root,
   prelude, CLI, env, DDN source, WASM, UI ingress가 모두 0인가?
2. actual Korean DDN과 `DdnRunner::run_update`의 성공/provider 실패/merge conflict가
   precommit effect 0과 state/outbox/receipt/effect 원자성을 직접 검증하는가?
3. 요구 fault 6축이 각각 실제 source mutation에서 RED이고 복원 뒤 GREEN인가?
4. A/B/C/D/tracked가 승인된 remap 계약에서 5,509,880 bytes와
   `27d18e40...cbaa`로 byte-identical하며 freshness checker가 direct unremapped
   procedure를 지원하지 않는 계약으로 명시하는가?
5. Microsoft Edge에서 success/unhandled/ambiguity/exact reopen/PID swap과 served WASM
   hash가 재현되는가?
6. F4의 ai_prompt/SSOT/W1-C1 환경 문제를 완화·skip·I2 귀속하지 않고 OPEN으로
   분리했는가?
7. handoff successor의 product/test diff가 fixed HEAD 대비 0이고, SSOT/SPEC/UI source,
   official DB, activation, protected resources가 불변인가?

## 비주장

plain `PASS`가 실제로 발행·결속되기 전에는 I2 `CLOSED`, W1-C2/W1 full closure,
public syntax/wire/diagnostics, activation, release, Human PASS를 선언하지 않는다.
