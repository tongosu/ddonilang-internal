# Targeted independent review request — public non-browser self-containment FU01

## 고정점

```text
BASELINE: 799ac30a2cff8ecb0b93379840bb7faee50eefef
PRODUCT_TEST_FIXED_HEAD: 91e56e597a920a8346e18bf68fa80afadf92d3aa
R3L_CUSTODY_FIXED_HEAD: eeda9a9da30be91b3d504ed5828af670590b7fb1
REVIEW_SCOPE: NON_BROWSER_TECHNICAL_FOLLOW_UP_ONLY
OVERALL_PUBLIC_SELF_CONTAINMENT: OPEN
```

독립검증ClaudeCode는 clean detached worktree에서 제품 코드를 수정하지 않고 다음을
직접 재현한다.

1. 선형 ancestry와 merge 0.
2. private compile-time `pack/**`, `work/**`, `docs/ssot/**` include 0.
3. public build path에 fixed internal absolute path 0.
4. projection tool 6 tests, validator 12 tests와 exact blob-byte/mutation coverage.
5. R3K A/B 894-file tree, concrete validation receipt, fresh Git commit/tree identity와
   public SPEC 29/29 seal.
6. root workspace no-run, tool lib 517/517, G14 3/3.
7. official source-built WASM A/B byte identity와 tracked artifact mismatch의 OPEN 보존.
8. `ddonirang-tool` full 407 tests가 source/projection 모두 405 PASS/2 ai-prompt RED이고,
   R3J projection-only runtime fixture RED 17건이 R3K에서 0인지.
9. exact CURRENT link 10개 누락·shared root untracked custody, Workbench/browser/rights와
   actual full-product G30/G31 OPEN이 숨겨지지 않았는지.
10. G23/G24 원장 세 개가 clean detached `a4d103ad...`에서 A/B byte-identical이고
    R3J four-path rights delta가 `b88d7a90...`까지 정확한지,
    199행 의존성·5개 material 누락·rights provenance와 모든 release/legal claim OPEN이
    정확히 보존되는지.
11. R3H/R3I checkout-relative tool identity 실패 후보가 PASS 근거에서 제외됐고 R3J가
    projected exact blob identity로 교정됐는지.
12. G22 facade 8종이 non-operative candidate인지, LICENSE/NOTICE/public membership
    또는 release readiness를 발행하지 않는지.
13. SSOT/UI/tracked WASM/official DB/activation diff 0.

허용 판정은 `PASS / PASS_WITH_FOLLOW_UP / REWORK`다. plain PASS라도 위 제한 기술
scope에만 적용되며 전체 goal closure, publication readiness, Human PASS가 아니다.

## R3L Owner-direction successor addendum

Owner 방향은 publication 재개가 아니라 independent review와 read-only custody만
재개했다. 검토자는 successor handoff에서 다음을 추가 확인한다.

1. D1 `ai-prompt`가 first publication membership에서 제외됐고 두 RED를 우회하거나
   public SPEC/SSOT 대체로 성공시키지 않았는지.
2. D2의 10개 history tree가 tracked review-bound commit 전에는 계속 제외되는지.
3. PC01 five-file, projectile lesson, `gaji/std_math`, unknown-rights path가 포함되지 않았는지.
4. R3L NOTICE가 199행·missing material 5개를 보존하며 license selection, required notice,
   legal approval, release inclusion을 주장하지 않는지.
5. tracked WASM diff가 0이고 candidate refresh/final promotion이 수행되지 않았는지.
6. Workbench candidate 107-path ledger와 manifest hash
   `74226b6ba784ec7ed2f0e5b499733a7656309860d14f9f61aa82587cfe84e0f4`가 fixed product
   HEAD bytes에서 재생성되는지.
7. root lock은 Playwright 1.44.0인데 현지 exact module은 없고, local cache의 1.62.1 및
   1.63 alpha와 browser revisions가 sealed release authority로 승격되지 않았는지.
8. public membership, G31, release, activation, Human PASS가 계속 미발행인지.

이 addendum의 read-only custody 문서도 제품 코드 변경이 아니며 독립 판정을 대신하지
않는다.

검토 fixed HEAD는 `eeda9a9da30be91b3d504ed5828af670590b7fb1`이고 direct parent는
`51f85622cd745dd19ea8e08041f835d7de4f6f74`다. 뒤따르는 handoff commit은 제품 diff가
없는 custody 문서이며 verdict 대상 제품 bytes를 바꾸지 않는다.
