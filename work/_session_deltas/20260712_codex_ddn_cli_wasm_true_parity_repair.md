# 2026-07-12 Codex Session Delta - DDN CLI/WASM True Bounded Parity Repair

## 시작 상태

- Goal: `docs/context/roadmap/CODEX_LONG_GOAL_DDN_CLI_WASM_TRUE_PARITY_REPAIR_V1_20260712.md`
- Branch: `codex/queue-20260706`
- Start HEAD recorded by goal: `2ddfe46`
- R7 pre-close HEAD: `e7fd3fd`
- Boundary:
  - `docs/ssot/**` read-only; no staged or committed SSOT changes.
  - No new DDN syntax.
  - No `state_hash`, `trace_hash`, or `bogae_hash` formula change.
  - No test-only source rewriting as closure evidence.
  - Existing unrelated dirty/untracked files were preserved and not staged.

## 수리 전 기준선

The independent review captured in the goal document reported the true parity blockers at `2ddfe46`:

- Runtime 13:
  - Accepted normal cases: 12.
  - State hash mismatch: 12/12 accepted normal cases.
  - The old checker allowed `domain_mismatch_reported` as successful evidence.
  - Canonical/output subset checks were present but did not cover the full bounded result surface.
- Foundation12:
  - Canonical DDN comparison: 12/12 `domain_mismatch_reported`.
  - State hash mismatch: 12/12.
  - Output row mismatches: at least 5 lessons.
  - Pendulum output log mismatch was explicitly reported.
  - The old checker used CLI subset comparison and did not enforce equal final rows/output rows/logs.
- First divergence classification:
  - Runtime representative: tick 0 `state_hash`, classification `hash_domain`.
  - Foundation representative: tick 0 `canonical_ddn`, classification `preprocess/canon`, followed by state/output projection mismatches.

## 구현 요약

- R0/R1 separated audit evidence from equality closure. `domain_mismatch_reported` remains valid audit data but cannot satisfy equality.
- R2 moved execution source preparation/canonicalization into the shared product frontdoor and removed JS-side source rewriting from parity runners.
- R3 aligned execution envelope fields: source/preprocessed/canonical hashes, configured/requested/effective ticks, frame/input metadata, and runtime schema.
- R4 aligned common state hash inputs through the shared Rust runtime surface without changing the hash formula.
- R5 made structured output equality explicit for bounded runtime/Foundation evidence: output log, output rows, final row, and value JSON where exposed.
- R6 closed the 13+12 equality gate with negative controls for hash, canonical, envelope, final row, and output row mismatches.
- R7 upgraded the integrated sync gate to require true equality, kept freshness/diagnostic/browser checks, and separated strict equality packs from `report_only` audit packs.
- R8 refreshed `tests/toolchain_golden/ai_prompt_lean.txt` from the deterministic product command because `cargo test -p ddonirang-tool` exposed an SSOT bundle hash drift. This did not modify `docs/ssot/**`.

## 커밋 목록

- `8885a04 test(runtime): expose cli wasm parity divergences` - R0.
- `f93542f test(runtime): separate parity audit from equality` - R1.
- `fb809dd fix(runtime): unify cli wasm preprocess and canon` - R2.
- `422e910 fix(runtime): align cli wasm execution envelope` - R3.
- `c76e559 fix(runtime): unify cli wasm state hash inputs` - R4.
- `ae4a598 fix(runtime): align cli wasm observations and outputs` - R5.
- `e7fd3fd test(runtime): close bounded cli wasm equality` - R6.
- `ceb1797 test(runtime): require true parity in sync gate` - R7.
- `docs(runtime): record true bounded cli wasm parity` - R8, this commit.
- Follow-up authoring-canon repair: this commit.

## 최종 결과

Report directory: `I:/home/urihanl/ddn/codex/build/true_parity_r0`

- `runtime13.raw.detjson`
  - schema: `ddn.seamgrim.wasm_cli_runtime_parity.report.v1`
  - cases: 13 total, 12 accepted normal + 1 reject.
  - accepted state hash mismatches: 0.
  - canonical mismatches: 0.
  - execution envelope mismatches: 0.
  - output row mismatches: 0.
  - output log mismatches: 0.
  - final row mismatches: 0.
  - `domain_mismatch_reported` rows: 0.
- `foundation12.raw.detjson`
  - schema: `seamgrim.foundation12.cli_raw_wasm_parity.report.v1`
  - lessons: 12.
  - state hash mismatches: 0.
  - canonical mismatches: 0.
  - execution envelope mismatches: 0.
  - final row mismatches: 0.
  - output row mismatches: 0.
  - output log mismatches: 0.
- `true_parity_equality_result.detjson`
  - `audit_ok=true`
  - `parity_equal=true`
  - `closure_claim=bounded_behavioral_parity`
  - `failure_count=0`
  - `unchecked=[]`
- `ddn_cli_wasm_sync_gate_report.detjson`
  - stages: 11/11 PASS.
  - includes freshness, ABI/web smoke, runtime 13 strict parity, Vol.4 audit parity, post-WASM high-risk parity, Foundation12 parity, true equality, diagnostic parity, representative 4-world browser smoke, and related pack golden.

## Hash 표본

Runtime 13:

- `c01_console_grid_scalar`: `blake3:daa54fe5d101e9e0e0c055f2f24d57b7a73fc68c44dcc4c16fe6d7a2742dcace`
- `c02_moyang_space2d`: `blake3:e92f3caf78d95fef02eb5fe9794cbfff96d3424ccf3ddf3755e2b7715b24d0a6`
- `c03_symbolic_simplify`: `blake3:05d7724e7ff2509285191a88daad05ba065cdffacaca693c83421cca9fd1cad0`
- `c04_proof_tactic_equivalence`: `blake3:b4c10952066383e184c879119629e31d028ce37b0bce47771a253e4df13d3b58`

Foundation12:

- `elem_math_number_line`: `blake3:f2f580bc7357d79b15029909686266d5806f669883b78c583d9db491749f8503`
- `elem_math_fraction_line`: `blake3:69b9b926ee213297b5a91b972008e9832c392a6cb5a52d4f0f046e84fd4808a9`
- `elem_math_rectangle_area`: `blake3:264e3c00f5eeccb85fa571d47222417537758ca4d5012c3c542bf1e87987bc86`
- `elem_science_daily_temperature`: `blake3:3d196cb07a812a24c1c64a6534261e87d2e68d3188ded760963fa75cc33e9347`

## Foundation12 목록

- `elem_math_number_line`
- `elem_math_fraction_line`
- `elem_math_rectangle_area`
- `elem_science_daily_temperature`
- `elem_econ_allowance_budget`
- `elem_econ_store_stock`
- `rep_math_function_line_v1`
- `rep_phys_pendulum_wave1_v1`
- `rep_phys_projectile_xy_v1`
- `rep_econ_supply_demand_tax_v1`
- `rep_phys_damped_oscillation_v1`
- `high_math_derivative`

## Not Exposed / Unchecked

- `runtime13.trace_hash`: WASM runner does not expose `trace_hash`.
- `runtime13.bogae_hash`: WASM runner does not expose `bogae_hash`.
- `runtime13.view_hash`: CLI summary keeps view hash outside the state hash parity denominator.
- `foundation12.view_hash`: browser/view-only hash is outside the state hash parity denominator.
- `unchecked`: none in the bounded 13+12 equality result.

## 검증 로그

- PASS: `cargo check`
- PASS: `cargo check --manifest-path tools/teul-cli/Cargo.toml`
- Initial FAIL: `cargo test -p ddonirang-tool`
  - Failure: `ai_prompt::tests::ai_prompt_output_matches_golden`.
  - Cause: deterministic `ai prompt --profile lean` output bundle hash drift in `tests/toolchain_golden/ai_prompt_lean.txt`.
  - Repair: regenerated that golden with `cargo run -q -p ddonirang-tool -- ai prompt --profile lean --out tests/toolchain_golden/ai_prompt_lean.txt`.
- PASS: `cargo test -p ddonirang-tool` after the golden refresh.
- PASS: `python tests/run_ddn_cli_wasm_freshness_check.py`
- PASS: `python tests/run_seamgrim_wasm_cli_runtime_parity_check.py`
- PASS: `python tests/run_seamgrim_foundation12_cli_raw_wasm_parity_check.py`
- PASS: `python tests/run_ddn_cli_wasm_post_wasm_shared_changes_check.py`
- PASS: `python tests/run_seamgrim_wasm_cli_diag_parity_check.py`
- PASS: `python tests/run_seamgrim_wasm_web_smoke_contract_pack_check.py`
- PASS: `python tests/run_ddn_cli_wasm_true_parity_equality_check.py`
- PASS: `python tests/run_seamgrim_wasm_sealed_runtime_binding_check.py`
- PASS: `python tests/run_ddn_cli_wasm_sync_gate_check.py --report I:/home/urihanl/ddn/codex/build/true_parity_r0/ddn_cli_wasm_sync_gate_report.detjson`
- FAIL in dirty worktree: `python tests/run_ci_sanity_gate.py --profile core_lang`
  - Failure code: `E_CI_SANITY_AGE3_COMPLETION_GATE_FAIL`.
  - Failing checks: `block_editor_roundtrip_check`, `seamgrim_vol4_runtime_track_check`.
  - This was reproduced while unrelated pre-existing Seamgrim UI/workbench dirty files were present.
- FAIL in temporary clean worktree at `75736b0` before local document copy:
  - `E_SSOT_SYNC_VERSION_SSOT_DIR_MISSING`, because `docs/ssot/**` is local/untracked and not materialized by `git worktree add`.
- FAIL in temporary clean worktree at `75736b0` after copying local `docs/ssot`, `docs/context`, and `docs/reports`:
  - Failure code: `E_CI_SANITY_AGE3_COMPLETION_GATE_FAIL`.
  - Failing checks: `bogae_backend_profile_smoke`, `block_editor_roundtrip_check`, `seamgrim_vol4_runtime_track_check`.
  - Additional cause: some Seamgrim lesson preview/schema files are local/untracked and absent from the clean worktree unless `solutions/**` is also copied.
- Local targeted reproduction in the original worktree after R8:
  - PASS: `python tests/run_bogae_backend_profile_smoke_check.py`
  - FAIL: `python tests/run_block_editor_roundtrip_check.py`
    - `block_editor_roundtrip_v1: block editor roundtrip mismatch`.
  - FAIL: `python tests/run_seamgrim_vol4_runtime_track_check.py`
    - `block_editor_screen_vol4_event_dispatch_smoke_v1: block editor screen smoke mismatch`.
- Repair after the targeted reproduction:
  - `wasm_canon_ddn`, `wasm_preprocess_source`, and execution envelope APIs keep using the shared execution surface for CLI/WASM runtime parity.
  - WASM authoring/inspection APIs now use the flat canon path: `wasm_canon_maegim_plan`, `wasm_canon_alrim_plan`, `wasm_canon_exec_policy_map`, and `wasm_canon_block_editor_plan`.
  - User-facing canon diagnostic prefix stays `WASM canon 실패`, preserving existing block-editor golden wording.
  - Added a Rust-side guard that block editor plan generation preserves `(시작)할때` and `(매마디)마다` as authoring hooks instead of runtime `seed_def` lowering.
- PASS after repair:
  - `python tests/run_block_editor_roundtrip_check.py`
  - `python tests/run_seamgrim_vol4_runtime_track_check.py`
  - `python tests/run_bogae_backend_profile_smoke_check.py`
  - `python tests/run_ci_sanity_gate.py --profile core_lang`
- PASS: `git diff --check` (line-ending warnings only).
- PASS: `git status --short -- docs/ssot` produced no output.

## Generated Byproducts

- Restored sanity-generated open logs:
  - `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
  - `pack/open_end_to_end/open.log.jsonl`
- Preserved pre-existing unrelated dirty logs:
  - `pack/seamgrim_exec_policy_effect_diag_v1/c09_exec_policy_record_file_read_success/open.log.jsonl`
  - `pack/seamgrim_exec_policy_effect_diag_v1/c14_exec_policy_record_open_io_EXPECT_FAIL/open.log.jsonl`

## 독립 검토 요청

Please attack the closure with these negative controls:

1. Put two different runtime state hashes into the equality report; closure must fail.
2. Change one canonical DDN byte; equality must fail.
3. Remove one output row; equality must fail.
4. Insert `domain_mismatch_reported`; audit may remain useful but equality must fail.
5. Confirm Foundation12 uses raw product CLI/WASM frontdoors, not test-only source transforms.
6. Confirm the same tick/state envelope is compared.
7. Confirm this report does not claim full DDN language, all-pack, all-gaji, trace/view/bogae hash, Korean Manim, release, IDC, or cloud parity.

Recommended review verdict options: `PASS`, `PASS_WITH_FOLLOW_UP`, `BLOCK_NEXT_PRODUCT_WAVE`.

## 남은 범위

- Full DDN language CLI/WASM equivalence.
- All pack/gaji CLI/WASM parity.
- `trace_hash`, `view_hash`, and `bogae_hash` formula integration.
- Full Korean Manim/Seamgrim release readiness.
- Server, login, IDC, cloud, account, and deployment scope.
