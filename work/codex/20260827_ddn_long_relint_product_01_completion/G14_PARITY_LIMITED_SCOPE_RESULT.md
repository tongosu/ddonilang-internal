# G14 current expected-rejection parity 제한 범위 결과

## 로컬·clean-detached 결과

- cases: `c09_boim_structured_view`, `c11_show_and_boim_split`, `c13_bogae_draw_madi_view_sugar`
- native/WASM exit: 모두 `1/1`
- exact diagnostic: `E_EXECUTION_PREPROCESS` / `E_BOIM_LEGACY_REMOVED` / phase `preprocess`
- state mutation, partial output, partial effect, compatibility fallback: 모두 `0`
- M1~M5: GREEN→RED→exact restore→GREEN, residue 0
- detached A/B at `b8530bd6...`: 각각 3/3 PASS와 WASM freshness PASS

## 범위 경계

T5F current grid는 이 판정에 포함하지 않는다. historical fixed target은 그대로 보존한다. G14 제품 의미는 직접 재현됐지만 별도 independent plain PASS가 아직 발행되지 않았으므로 closure는 주장하지 않는다.

```text
G14_LOCAL_FIXED_HEAD_RESULT: PASS
G14_INDEPENDENT_PLAIN_PASS: WAITING_FOR_EXTERNAL_INDEPENDENT_REVIEW
CURRENT_PUBLIC_REJECTION_PARITY_SCOPE_CLOSED: NO
```
