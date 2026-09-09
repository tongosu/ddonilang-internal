# R3M tracked WASM embedded absolute path — Owner decision packet

## 결정이 필요한 이유

R3M 전 파일 scanner가 유일한 실제 finding으로 tracked
`solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` 내부의 Cargo registry/Rustup
source path 115건을 검출했다. 현재 공식 clean A/B build도 tracked artifact와
byte-identical하며 같은 115건을 포함한다.

다음은 Codex가 임의로 선택할 수 없다.

- first public non-browser projection에 tracked WASM family를 계속 포함할지
- dependency/toolchain source path까지 remap하는 새 official build contract를 만들지
- binary embedded provenance를 제한적으로 허용할지

## 선택지

### Option A — dependency/toolchain root까지 deterministic remap

official entrypoint가 repo root뿐 아니라 Cargo registry와 Rust toolchain source root도
stable virtual roots로 remap하도록 build contract를 교정한다.

- 장점: tracked WASM public membership을 유지하면서 absolute path 0을 목표로 할 수 있다.
- 위험: Rust/Cargo/wasm-pack 조합에서 실제 remap 범위와 재현성을 새로 입증해야 한다.
- 비용: 중간~높음. clean A/B, section audit, tracked candidate refresh와 별도 independent review 필요.
- 가역성: 높음. candidate output만 만들고 tracked artifact는 승인 전 유지 가능.

### Option B — first non-browser projection에서 tracked WASM family 제외

source-built native/CLI 범위만 first projection membership으로 두고 browser/WASM family를
sealed offline browser successor로 이월한다.

- 장점: security gate를 완화하지 않고 public source projection을 좁게 닫을 수 있다.
- 위험: 현재 projection의 WASM parity·Workbench/browser 범위가 명시적으로 OPEN이 된다.
- 비용: 낮음~중간. manifest/membership/claim 재결속과 independent review 필요.
- 가역성: 높음. successor에서 WASM을 다시 포함할 수 있다.

### Option C — exact binary provenance 예외

tracked WASM 한 파일의 Cargo/Rustup source path를 non-secret build provenance로 분류하고
exact artifact hash에만 예외를 둔다.

- 장점: artifact 교체 없이 현재 membership 유지 가능.
- 위험: user-specific absolute path 0이라는 기존 gate 의미를 약화하고, binary allowlist가
  새 권위 계약이 된다.
- 비용: 낮음.
- 가역성: 중간. 이후 제거할 수 있지만 public security precedent가 남는다.

## 권고

`Option A`를 권고한다. tracked WASM family를 public projection에 유지한다면 gate를
완화하는 대신 official build의 remap completeness를 닫는 편이 현재 보안·재현성 원칙과
가장 잘 맞는다. remap이 toolchain 제약으로 불가능하다는 bounded 증거가 나오면
`Option B`로 전환한다. `Option C`는 gate 의미를 바꾸므로 권고하지 않는다.

## Owner 반환 필드

```text
R3M_TRACKED_WASM_EMBEDDED_PATH_DECISION:
OPTION_A_REMAP_TOOLCHAIN_ROOTS
or OPTION_B_EXCLUDE_TRACKED_WASM_FIRST_PROJECTION
or OPTION_C_EXACT_HASH_PROVENANCE_EXCEPTION

TRACKED_WASM_CANDIDATE_REFRESH_AUTHORIZED: YES/NO
PUBLIC_NON_BROWSER_WASM_MEMBERSHIP: INCLUDE/EXCLUDE/OPEN
RESUME_FROM: R3M_F2
```

Owner 결정과 그 결정의 별도 검증 전 상태:

```text
BLOCKED_BY_R3M_TRACKED_WASM_EMBEDDED_ABSOLUTE_PATH
TARGETED_REREVIEW_NOT_READY
TRACKED_WASM_REFRESH: 0
FINAL_PROMOTION: NOT_AUTHORIZED
```
