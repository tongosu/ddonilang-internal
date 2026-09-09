# DDN-LONG-RELINT-PRODUCT-01 public conformance bounded closure checkpoint

이 문서는 R2 public manifest의 `PUBLIC_CONFORMANCE_SUBSET` 13개 root를 대상으로 한
읽기 전용 정적 감사 결과다. manifest, projection, 제품, 테스트, SSOT, public SPEC는
수정하지 않았다.

## 선행 수치 교정

기존 G21의 46-path / projection missing 32는 `tests/...` 문자열 참조만 재귀한
하한선이었다. 실행 파일 import, 저장소 경로, 실제 pack tree까지 포함한 폐쇄성이
아니므로 최종 conformance closure로 사용하지 않는다.

새 bounded audit 결과:

```text
ROOTS: 13
SCRIPT_CLOSURE: 82
PACK_ROOTS: 43
REQUIRED_FILES: 433
REQUIRED_RAW_BYTES: 3310511
MISSING_IN_SOURCE: 0
MISSING_IN_PROJECTION: 381
UNRESOLVED_DYNAMIC_REFERENCES: 0
STATIC_COMPLETENESS_CLAIM: false
STATUS: FAIL_CLOSED
```

역할별 파일 수:

```text
BUILD_OR_VALIDATION_SCRIPT: 2
CONFORMANCE_FIXTURE_OR_ORACLE: 316
CONFORMANCE_SCRIPT_OR_RUNNER: 82
LANGUAGE_RUNTIME_OR_CLI_SOURCE: 6
WORKBENCH_PRODUCT_SOURCE: 27
```

정적 분석에서 unresolved 동적 참조가 0이라는 사실은 실행 폐쇄성을 증명하지 않는다.
fresh public repository에서 실제 실행해야 완전성을 검증할 수 있다.

## umbrella root 영향

13개 root 중 다음 두 파일이 큰 내부 집합을 끌어온다.

| root | script closure |
|---|---:|
| `tests/run_ddn_cli_wasm_sync_gate_check.py` | 43 |
| `tests/run_seamgrim_workbench_durable_quality_gate_check.py` | 30 |

두 umbrella root를 임시로 제외한 진단용 leaf candidate는 다음과 같다.

```text
LEAF_ROOTS: 11
LEAF_SCRIPT_CLOSURE: 23
LEAF_PACK_ROOTS: 1
LEAF_REQUIRED_FILES: 56
LEAF_MISSING_IN_PROJECTION: 26
LEAF_UNRESOLVED_DYNAMIC_REFERENCES: 0
```

이 candidate는 Owner-bound manifest 변경이 아니다. 특히 umbrella gate가 제공하던
CLI/WASM freshness·parity와 Workbench durability 의미를 자동 폐기하지 않는다.

## Owner 결정 필요

다음 중 하나는 public conformance membership을 바꾸므로 구현자가 정할 수 없다.

- A: 현행 umbrella root를 유지하고 433-file closure를 공개 conformance 범위로 결속
- B: public-specific aggregate를 만들고 exact leaf 및 선별된 parity/durability case만
  새 공개 root로 결속

권고는 B다. giant internal test tree를 그대로 공개 표면으로 만드는 대신 기존 public
요구 의미를 명시적인 작은 aggregate와 curated fixture로 보존할 수 있기 때문이다.

```text
D7_PUBLIC_CONFORMANCE_ROOT_POLICY:
OPTION_B_PUBLIC_SPECIFIC_AGGREGATE_WITH_EXACT_LEAF_AND_CURATED_PARITY_DURABILITY_CASES
```

Owner 승인 전 manifest rewrite, test copy, pack copy, aggregate 구현은 시작하지 않는다.

## custody

```text
AUDIT_TOOL: audit_public_conformance_closure.py
LEDGER: PUBLIC_CONFORMANCE_BOUNDED_CLOSURE_AUDIT.detjson
LEDGER_BYTES: 185891
LEDGER_SHA256: 3486773d80d0ebe488eb918712186095c011c1e3ec5cf0a7e1d25c854e728568
SOURCE_HEAD: 905efb4a1601b764e0f4f2554bef3fbd433172a3
PROJECTION: I:/home/urihanl/ddn/codex/build/public-projection-r1/tree-a
MANIFEST: I:/home/urihanl/ddn/codex/build/worktrees/ddn-public-repository-successor-r2-20260826/work/codex/20260826_ddn_public_repository_successor_owner_binding_r2/PUBLIC_PRODUCT_SCOPE_MANIFEST.detjson
NETWORK_ACCESS: 0
```
