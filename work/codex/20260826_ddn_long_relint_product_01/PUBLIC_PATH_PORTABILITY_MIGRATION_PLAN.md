# DDN-LONG-RELINT-PRODUCT-01 G20 public path portability migration plan

```text
STATUS: CANDIDATE_ONLY
PRODUCT_SOURCE_CHANGED: 0
PUBLIC_MANIFEST_CHANGED: 0
PUBLIC_PROJECTION_CHANGED: 0
```

R1 projection의 최초 marker 15 files와 broader security preflight가 추가로 찾은 13
files, 총 28 files를 실제 사용 역할별로 분류했다. 단순 문자열 match를 곧바로 제품
결함이나 삭제 대상으로 해석하지 않는다.

## P1 — public product portability correction required

| path | marker 역할 | successor 처리 |
|---|---|---|
| `.cargo/config.toml` | private Cargo target 기본값 | public projection에서는 private absolute `target-dir`를 제거하고 fresh repo 기본 또는 명시적 portable target을 사용 |
| `solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py` | Workbench runtime state/build root 기본값 | 기존 `SEAMGRIM_BUILD_DIR` override를 보존하고 private I:/C: fallback을 portable default로 교체 |
| `tool/src/paths.rs` | tool의 build/out 기본 owner | private I:/C: probe를 제거하고 platform-independent owner를 사용 |
| `tools/teul-cli/src/cli/paths.rs` | CLI의 build/out 기본 owner | tool과 같은 portable policy로 수렴 |
| `ddn.project.json` | private binary 및 stale SSOT 20.12.0 root config | explicit public role이 아니므로 그대로 투영하지 않음; public sample config가 필요하면 current authority로 별도 생성·검증 |
| `tool/src/wasm_api.rs` | test가 private SSOT lesson path 5개를 runtime read | public conformance에서 필요하면 공개 역할 fixture로 전환; private SSOT fallback 금지 |
| `tools/teul-cli/src/cli/frontdoor_parse.rs` | test가 live projectile SSOT path를 compile-time include | D6 승인 exact public example path로 전환; 미승인 시 fail-closed |

Cargo target과 runtime output 위치 변경은 언어 의미가 아니다. 그러나 CLI 기본 output과
Workbench durability에 영향을 줄 수 있으므로 G8 이후 CLI/WASM/Workbench 실제 경로와
fault injection으로 검증한다. hidden private fallback은 남기지 않는다.

## P2 — internal utility excluded from public role

다음 4 files는 first public product scope의 runtime/build/conformance role이 아니라 internal
maintenance/private-pilot utility다. 광범위 tree copy로 들어온 것이며 public projection
allowlist에서는 제외한다.

```text
scripts/seamgrim_manage_lesson_backups.py
solutions/seamgrim_ui_mvp/deploy/build_private_pilot_release.py
solutions/seamgrim_ui_mvp/tools/extract_study_guide_ddn.py
solutions/seamgrim_ui_mvp/tools/repair_study_guide_markdown_ddn.py
```

내부 원본은 수정·삭제하지 않는다. `solutions/seamgrim_ui_mvp/tools/README.md`도 internal
operating path를 설명하는 maintenance 문서이며 required Workbench runtime member가
아니므로 projection에서 제외하고 원본은 보존한다.

## P3 — D7 conformance membership dependent

```text
tests/_run_pack_golden_impl.py
tests/run_ddn_cli_wasm_true_parity_equality_check.py
tools/teul-cli/tests/golden/W91/W91_G01_ai_prompt_invariants/ai.prompt.txt
tools/teul-cli/tests/golden/W91/W91_G02_ai_prompt_snapshot/ai.prompt.golden.txt
tools/teul-cli/tests/golden/W91/W91_G02_ai_prompt_snapshot/ai.prompt.txt
```

두 test file은 private build/target 후보를 포함하고, 세 AI prompt golden은 historical
private SSOT snapshot 내용을 포함한다. D7에서 public-specific aggregate를 승인하면
해당 aggregate가 portable env/temporary target을 명시적으로 소유하고 historical prompt
golden은 public conformance에서 제외한다. 현행 umbrella root 전체 공개를 승인하면 다섯
파일 모두 별도 portability/privacy 교정이 필요하다.

## P4 — public documentation successor

`publish/ddonirang_grammar_full.md`의 `docs/ssot/ssot/**` 문자열은 실행 path가 아니라
v20.6.0 역사 정본 안내다. 현재 Owner-bound scope가 요구하는 public SPEC entrypoint는
exact v0.5.0 family이며 이 역사 문서는 required member가 아니다. 따라서 G25 projection
allowlist에서 제외하고 v0.5.0 exact family만 포함한다. 기존 역사 문서를 제자리 수정하지
않고, 향후 공개 history role이 필요하면 별도 Owner-authorized scope로 다룬다.

## P5 — historical `pack_public` docs excluded

broader scanner가 찾은 `pack_public/**` 10개 README/WARNING file은 스스로 legacy/support
snapshot이며 새 작업이나 closure 근거가 아니라고 명시한다. Owner-bound first public
scope의 selected examples 또는 D7 conformance root도 아니다. 내부 `pack/**` 및 private
`docs/ssot/**`를 참조하므로 G25 allowlist에서 제외한다. 원본 10 files는 변경하지 않는다.

## gate result

```text
INITIAL_MARKER_FILES: 15
BROADER_MARKER_FILES: 28
PRODUCT_PORTABILITY_OR_PRIVATE_FIXTURE: 7
INTERNAL_UTILITY_OR_DOC_EXCLUDE: 5
D7_CONFORMANCE_DEPENDENT: 5
PUBLIC_DOC_CUSTODY: 1
HISTORICAL_PACK_PUBLIC_EXCLUDE: 10
UNCLASSIFIED: 0
PUBLIC_PATH_PORTABILITY_IMPLEMENTATION: NOT_STARTED_PENDING_G8
```
