# nuri_madi_phase_trace_g1_v1

SSOT addendum G3용 누리 마디 phase/action record skeleton pack이다.

## Scope

- P0~P7 phase trace fixture를 제공한다.
- raw action, merged action, `action_status` 4종(`맞음/가만히/잘림/거부`) detjson fixture를 제공한다.
- `E_MADI_WRITE_CONFLICT` fatal 후보 fixture를 제공한다.

## Closure

- evidence tier: `pack_skeleton`
- closure grade: `닫힘-문서`
- product runtime/frontdoor behavior change: 없음
- `닫힘-동작` 주장 없음

기존 제품 경로의 action pipeline 증빙은 `pack/nurigym_shared_sync_action_pipeline_v1`와 `tools/teul-cli/src/cli/nurigym.rs`에 있다. 이 pack은 P0~P7 phase와 write conflict 계약 후보를 실행 구현으로 닫지 않고 fixture/checker로만 고정한다.
