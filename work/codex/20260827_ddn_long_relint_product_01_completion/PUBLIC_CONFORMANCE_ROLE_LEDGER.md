# Public-specific conformance exact 11-leaf role ledger

## 고정 멤버십

`tests/run_ddn_public_specific_conformance_check.py --check-files-only`의 Owner-approved
D7 Option B 멤버십을 그대로 사용한다. internal giant umbrella 두 개는 포함하지 않는다.

| exact leaf | role | 현재 판정 |
|---|---|---|
| `tests/run_seamgrim_public_default_route_check.py` | `DEPENDENCY_BLOCKED` | 실제 browser runner가 Playwright와 Workbench 제품 tree를 요구한다. sealed offline browser bundle이 없다. |
| `tests/run_seamgrim_public_physics_first_run_check.py` | `RIGHTS_BLOCKED` | selected projectile lesson과 Workbench embedded projectile bytes의 권리 확인 전 public 실행 멤버십 금지. browser dependency도 별도 OPEN. |
| `tests/run_seamgrim_one_file_ddn_create_run_check.py` | `DEPENDENCY_BLOCKED` | Workbench/browser dependency가 projection에서 의도적으로 제외됐다. |
| `tests/run_seamgrim_public_physics_change_storyboard_check.py` | `DEPENDENCY_BLOCKED` | Workbench/browser dependency가 projection에서 의도적으로 제외됐다. projectile public 성공 주장도 금지. |
| `tests/run_seamgrim_public_share_clone_reopen_check.py` | `DEPENDENCY_BLOCKED` | Workbench/browser 및 storage lifecycle dependency가 projection에서 제외됐다. |
| `tests/run_seamgrim_legacy_deeplink_compat_check.py` | `HISTORICAL_FIXED_TARGET` | historical compatibility evidence다. current 제품 성공이나 stable public surface로 승격하지 않는다. |
| `tests/run_seamgrim_public_single_node_serving_check.py` | `DEPENDENCY_BLOCKED` | browser/server 제품 tree와 sealed browser dependency가 필요하다. |
| `tests/run_seamgrim_public_four_viewport_quality_check.py` | `DEPENDENCY_BLOCKED` | browser 및 Workbench presentation tree가 필요하다. menu zoom Human 증거로 확대하지 않는다. |
| `tests/run_ddn_cli_wasm_freshness_check.py` | `PUBLIC_SOURCE_FILES_ONLY` | source/artifact manifest freshness를 검증한다. 전체 CLI/WASM 의미 parity 주장은 아니다. |
| `tests/run_ddn_cli_wasm_true_parity_successor_check.py` | `PUBLIC_SOURCE_EXECUTABLE` | current legacy 3건 expected rejection의 native/WASM exact parity다. 성공 semantics로 표시하지 않는다. |
| `tests/run_seamgrim_view_only_state_hash_invariant_check.py` | `INTERNAL_TYPED_EVIDENCE` | 제품 UI source invariant 증거지만 rights-excluded R2 projection에서는 Workbench dependency가 빠져 실행 불가하다. |

```text
EXACT_LEAF_COUNT: 11
EXACT_UNIQUE_COUNT: 11
PARITY_MEMBER_COUNT: 3
DURABILITY_MEMBER_COUNT: 3
INTERNAL_UMBRELLA_COUNT: 0
PC01_FIVE_FILE_PUBLIC_COPY: 0
PROJECTILE_PUBLIC_COPY: 0
LOGICAL_ORACLE_IS_PRODUCT_EXECUTION: NO
UNSUPPORTED_OR_MISSING_DEPENDENCY_REPORTED_AS_SUCCESS: NO
PUBLIC_AGGREGATE_ACTIVATED: NO
```

동일 leaf가 technical source custody에 포함되어도 그 사실은 public release membership,
rights confirmation, runtime activation 또는 Human PASS를 뜻하지 않는다.
