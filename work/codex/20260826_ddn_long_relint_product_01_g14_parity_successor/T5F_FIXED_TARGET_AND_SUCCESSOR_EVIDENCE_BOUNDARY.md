# T5F fixed-target와 current successor 증거 경계

## 보존된 역사 증거

- T5F fixed HEAD: `0abec54b30b26dbe99ce249aa3de5d7681907eab`
- T5F handoff: `7a83d5dd457b420570ecc0f1092fff7eab9bf946`
- fixed-target independent verdict: `PASS`
- 상태: `T5F_HISTORICAL_FIXED_TARGET_PASS_PRESERVED`

이 PASS는 그 고정 대상의 역사적 판정이다. PC02 exact inverse를 포함하는 현재
release-integration successor에 자동 상속하지 않는다.

## 현재 제품 확인

PC02 commit `04566a24...`가 T5F 경로에 도입했던
`fromPreV25Source` 사용은 exact inverse successor에서 제거된 상태다. 현재 제품
constructor는 `new DdnWasmVm`이고 `fromPreV25Source`는 존재하지 않는다.

현재 저장소의 `.ddn` 입력 가운데 grid successor의 두 의미 표식 `위치`와
`보개_그림판_목록`을 함께 가진 입력을 전수 검색한 결과 후보는 다음 1개뿐이었다.

`solutions/seamgrim_ui_mvp/lessons/rep_grid_game_state_drop_v1/lesson.ddn`

current constructor는 이 입력을 받아들이지만 initial 및 stepped
`view_meta.workbench.results.grid`는 모두 `null`이다. source-built WASM A/B에서도
같은 결과였다. 새 문법, 새 lowering, hidden compatibility 또는 새 제품 의미를
임의로 만들지 않았다.

## 결론

```text
T5F_CURRENT_GRID_SUCCESSOR_INPUT_OWNER_DECISION_REQUIRED
T5F_HISTORICAL_FIXED_TARGET_PASS_PRESERVED
PC02_EXACT_INVERSE_PRESERVED
```

Owner는 current V25 공개 입력과 constructor만으로 grid family를 생성할 exact
surface를 지정하거나, T5F current successor membership/범위를 별도로 결정해야
한다. 그 결정 전에는 T5F current-runtime PASS나 전체 targeted-review readiness를
주장할 수 없다.
