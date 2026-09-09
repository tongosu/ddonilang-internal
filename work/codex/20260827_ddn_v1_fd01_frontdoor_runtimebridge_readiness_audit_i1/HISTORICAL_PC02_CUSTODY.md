# historical PC02 보관·비승격 경계

## 계보

```text
IMPLEMENTATION_COMMIT: 04566a2426b56084f4449b363530192aa1166d2a
TITLE: feat(v25): converge assignment frontdoors
CHANGED_PATHS: 28
DIFF: +878 / -89
STATUS_AT_HANDOFF: IMPLEMENTED_PENDING_INDEPENDENT_REVIEW
INDEPENDENT_PLAIN_PASS: NONE

EXACT_INVERSE_COMMIT: 0dd73ab9
TITLE: revert(v25): exclude unreviewed PC02 frontdoor slice
OWNER_DISPOSITION: EXCLUDED_BY_EXACT_INVERSE_OWNER_BOUND
```

PC02는 tool/CLI/teul/WASM/Workbench의 기본 입력을 V25로 수렴시키고 명시적
pre-V25 constructor를 추가한 큰 vertical이었다. 그러나 독립 plain PASS를 받기 전에
후속 통합에서 exact inverse로 제외됐다.

## 현재 재사용할 수 없는 이유

1. 독립검토가 완료되지 않았다.
2. current lesson 557개 중 V25 parser 통과가 0이다.
3. PC02의 7-case pack은 전체 lesson·current Workbench migration을 대표하지 않는다.
4. 현재 제품·SSOT는 PC02 시점 이후 변했다.
5. exact inverse는 단순 사고가 아니라 명시적 Owner 결속이었다.
6. PC02에 의존하던 T5F runner 조정과 current V25 grid 의미를 분리해야 한다.

## 보존할 지식

- 명시적 pre-V25 migration entrypoint라는 방향
- CLI/WASM/Workbench가 같은 epoch 계약을 써야 한다는 요구
- 전환 시 touched path와 회귀 범위
- pack과 mutation 구조

## 금지

```text
BLIND_REAPPLY_PC02_COMMIT
CHERRY_PICK_PC02_AS_REVIEWED_PRODUCT
INHERIT_PC02_PASS
USE_T5_HISTORICAL_PASS_AS_CURRENT_V25_GRID_PASS
```

후속 구현은 PC02를 되살리는 작업이 아니라, current authority와 557-case inventory를
바탕으로 새 successor를 만드는 작업이어야 한다.

