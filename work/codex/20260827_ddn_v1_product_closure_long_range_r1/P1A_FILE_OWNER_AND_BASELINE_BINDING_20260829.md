# P1-A V1-Core supported ingress W1 file-owner and baseline binding

## Execution identity

```text
TASK: DDN-P-V1-P1A-CORE-SUPPORTED-INGRESS-W1
EXCLUSIVE_WRITER: DDN V1제품마감Codex
WRITER_THREAD: 01a04a01-b812-7840-a2a3-33208dd36e36
WORKTREE: I:/home/urihanl/ddn/codex/build/worktrees/ddn-p-v1-project-ux-r2-census-r1-20260828
BRANCH: codex/ddn-v1-p1a-core-supported-ingress-w1-20260829
P1A_IMPLEMENTATION_BASELINE: fe7c38c53cc3e1946b109b8002447983c185ba9b
P0_LIMITED_CLOSURE_PARENT: 5ef7e8163ac2833fdf5b952767f52bf799605130
NEW_WORKTREE_CREATED: false
FILE_OWNER_LEASE_STATUS: BOUND
```

이 lease는 P1-A 첫 vertical에만 유효하다. P2/P3/P4/P5/P6 ownership, whole V1 membership,
public release 또는 Human gate로 확장되지 않는다.

## Leased existing product paths

- `tool/src/ddn_runtime.rs`
- `tool/src/runtime_surface.rs`
- `tool/src/source_analysis.rs`
- `tool/src/wasm_api.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/run.rs`

## Conditional tracked WASM refresh paths

Official freshness가 실제로 요구할 때에만 다음을 갱신할 수 있다.

- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.js`
- `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.d.ts`
- `solutions/seamgrim_ui_mvp/ui/wasm/package.json`

## Leased new evidence paths

- `pack/v1_core_supported_ingress_w1/**`
- `tests/run_v1_core_supported_ingress_w1.py`
- `tests/run_v1_core_supported_ingress_wasm_parity_w1.mjs`
- `tests/run_v1_core_supported_ingress_fault_injection_w1.py`
- `work/codex/20260827_ddn_v1_product_closure_long_range_r1/P1A_*`
- `work/_session_deltas/20260829_codex_ddn_v1_p1a_*`

## Explicitly not leased

- `docs/ssot/**`
- `publish/spec/**`
- `lang/src/parser.rs`
- `lang/src/lib.rs`
- `tool/src/canon.rs`
- `tool/src/main.rs`
- `scripts/build_wasm_tool.ps1`
- Workbench HTML/CSS/visible copy/layout
- any P2/P3/P4/P5/P6 product path outside the leased list

비임대 경로가 실제로 필요하면 해당 sub-slice를 멈추고 RED evidence와 함께
`FILE_OWNER_EXPANSION_REQUIRED`를 반환한다. 권한을 추정하지 않는다.

## First vertical scope

```text
VC01: Korean raw source
VC02: Definition :=
VC03: Binding/Rebinding <-
VC18: structured diagnostics
VD01: direct/mutual recursion explicit unsupported
```

하나의 shared supported-profile product API를 native/WASM applicable frontdoors가 소비한다.
Hidden PreV25 retry/fallback, 557-lesson global default switch, 새 parser/canon semantic authority,
private teul semantics는 금지한다. teul은 consumer adapter일 뿐이다.

## Required first RED gate

1. valid V25 `:=`/`<-` raw source가 current supported ingress에서 거부되거나 PreV25로 해석됨
2. V25 legacy `=`가 exact migration diagnostic을 내지 못함
3. direct/mutual recursion이 deterministic explicit unsupported diagnostic을 내지 못함
4. unknown/omitted profile과 hidden PreV25 retry mutation이 fail-closed하지 못함

RED를 먼저 고정한 뒤 minimal product implementation, native/WASM byte/diagnostic parity,
failure atomicity, mutation RED→restore→GREEN, clean fixed-target reproduction, product/test fixed HEAD,
docs-only handoff와 independent review request 순서로 진행한다.

## Nonclaims

- P1-A implementation or PASS: not yet established
- V1 membership/readiness: not promoted
- whole P0 closure: not claimed
- SSOT/SPEC change: not authorized
- release/activation/Human PASS: not claimed
