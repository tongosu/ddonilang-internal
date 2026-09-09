# CI and release authority audit

## 현행 내부 CI

`.github/workflows/seamgrim-ci.yml`은 Windows에서 teul-cli build, 여러 W49/W107/W109/W111 golden과 `tests/run_seamgrim_ci_gate.py`를 실행하도록 작성돼 있다. branch-protection candidate는 `seamgrim-gate`를 required context로 적는다.

그러나 R1 public preview는 이 workflow를 포함하지 않았다. 이유는 workflow가 전체 내부 tests/golden closure를 전제하며, R1 allowlist에 그대로 복사하면 public fresh clone에서 fail-closed하기 때문이다.

## public CI successor 권고

공개 CI는 개수 감소가 아니라 권위와 실제 실행 경로를 기준으로 새로 봉인한다.

1. Rust workspace build/test
2. public CLI build/test
3. public conformance suite
4. WASM official build + tracked/release artifact identity check
5. Workbench examples smoke
6. public SPEC/link validation
7. secret/private-path/forbidden-source dependency scan

각 step은 PUBLIC_SOURCE tree만 입력으로 사용해야 한다. 내부 `docs/ssot`, private pack, absolute path, pre-generated private artifact에 의존하면 실패해야 한다.

## release gate

```text
INTERNAL_EXPERIMENTAL_ARTIFACT: INTERNAL_WORK_BUILD_ALLOWED
PUBLIC_RELEASE_ARTIFACT: PUBLIC_SOURCE_ONLY_REQUIRED
CURRENT_PUBLIC_CI_PROMOTION: NOT_AUTHORIZED
GITHUB_BRANCH_PROTECTION_CHANGE: NOT_AUTHORIZED
GITHUB_RELEASE: NOT_AUTHORIZED
```
