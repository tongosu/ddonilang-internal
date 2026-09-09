# 2026-07-12 Codex Session Delta - Seamgrim Wave 3A Curriculum

## Scope

- Goal source: `C:\Users\ddongosu\.codex\attachments\2b7e3fd5-55a4-4ad2-9cd1-d944c3fdf184\pasted-text-1.txt`.
- Goal: `셈그림 교과 제작 체계와 대표 5세계 Wave 3A V1`, G0~G8.
- Branch: `codex/queue-20260706`.
- Start HEAD: `728ad6a fix(seamgrim): harden durable project service`.
- Boundary: `docs/ssot/**` read-only, no new DDN syntax, no runtime `state_hash` formula change, no AI auto-apply, no login/cloud/server expansion.
- Existing dirty/untracked at start: preserved; product and new Wave3A target paths were clean.

## Read Before Work

- `AGENTS.md`
- `AGENT_WORKFLOW.md`
- `SSOT_POLICY.md`
- `ARTIFACT_POLICY.md`
- `docs/context/all/DEV_SUMMARY.md`
- `docs/context/roadmap/SEAMGRIM_DDONIRANG_K12_UNIVERSITY_STEM_CURRICULUM_MASTERPLAN_V1_20260712.md`
- `docs/ssot/ssot/SSOT_INDEX_v24.12.9.md`
- Relevant SSOT notes in `README_v24.12.9.md` and `SSOT_DECISIONS_v24.12.9.md`: Seamgrim lesson/project/package is product shell/source-management layer; Korean Manim and education closure claims require product evidence.

## G0 Baseline And Inventory

Implementation:

- Added deterministic baseline pack `pack/seamgrim_curriculum_wave3a_baseline_v1`.
- Added `tests/run_seamgrim_curriculum_wave3a_baseline_check.py`.
- The checker reads `solutions/seamgrim_ui_mvp/lessons/index.json`, `active_allowlist.detjson`, and the 217 lesson directories.
- The baseline records lesson id, prefix, subject, grade-band candidate/source, required views, primary view, view roles, file presence, active allowlist membership, and pack evidence.
- Representative start points are fixed:
  - `rep_math_function_line_v1`
  - `rep_phys_pendulum_wave1_v1`
  - `rep_phys_projectile_xy_v1`
  - damping source start: `ssot_edu_phys_p011_01_underdamped_xt`, target representative id pending as `rep_phys_damped_oscillation_v1`
  - `rep_econ_supply_demand_tax_v1`
- Quantity, grade-band candidates, and product closure are kept separate. No national curriculum alignment or global curriculum completion claim is made.

Evidence:

- `python tests/run_seamgrim_curriculum_wave3a_baseline_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_curriculum_wave3a_baseline_v1` -> PASS.
- `git diff --check -- tests/run_seamgrim_curriculum_wave3a_baseline_check.py pack/seamgrim_curriculum_wave3a_baseline_v1` -> PASS.
- `git status --short -- docs/ssot` -> clean.

Status:

- Docs/evidence closed: Wave 3A G0 inventory and representative start-point baseline.
- Behavior closed: none; G0 is read-only inventory.
- Pending: G1 curriculum crosswalk/card V0 and product lesson detail connection.

## G1 Curriculum Crosswalk And Lesson Cards

Implementation:

- Added product data files:
  - `solutions/seamgrim_ui_mvp/lessons/curriculum_crosswalk.v0.detjson`
  - `solutions/seamgrim_ui_mvp/lessons/lesson_cards.v0.detjson`
- Added UI loader/validator `solutions/seamgrim_ui_mvp/ui/curriculum_cards.js`.
- `loadCatalogLessons()` now merges valid lesson cards into catalog lessons after existing meta enrichment.
- Browse lesson detail now shows a student-facing `교육과정 연결` section with grade band, core concepts, inquiry actions, prediction prompt, and experiment prompt.
- Internal axes such as `status_axes`, evidence refs, and candidate status stay in the data artifact and are not rendered in the student-facing detail text.
- The bundle keeps canonical curriculum alignment and external student success claims false.

Evidence:

- `python tests/run_seamgrim_curriculum_cards_check.py` -> PASS.
- `python tests/run_pack_golden.py seamgrim_curriculum_cards_v0` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/screens/browse.js` -> PASS.
- `git diff --check -- <G1 paths>` -> PASS with CRLF normalization warnings only.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: product lesson detail consumes `lesson_card.v0` and exposes student-facing curriculum card rows in the browser.
- Docs/evidence closed: `curriculum_crosswalk.v0` and `lesson_card.v0` candidate data for the five Wave 3A worlds.
- Pending: G2 existing three-world curriculum workflows.

## G2 Three Representative Curriculum Workflows

Implementation:

- Added `solutions/seamgrim_ui_mvp/ui/curriculum_inquiry.js`.
- Added a product `교과 탐구` panel to the run screen with stable selectors for prediction, explanation, card summary, and artifact status.
- `RunScreen` now builds deterministic `seamgrim.curriculum_inquiry_artifact.v0` from the lesson card, student prediction, run hash, completed lesson-plan activities, and explanation.
- `project_snapshot.v0` now includes optional `curriculum_inquiry_artifact` when present. The field is additive and does not change runtime `state_hash`.
- Project save/reopen/clone/restore paths preserve the artifact and reattach the catalog curriculum card by lesson id.
- Added pack/checker/browser runner:
  - `pack/seamgrim_curriculum_workflow_three_worlds_v1`
  - `tests/seamgrim_curriculum_workflow_three_worlds_runner.mjs`
  - `tests/run_seamgrim_curriculum_workflow_three_worlds_check.py`

Scope boundary:

- G2 targets the already active three-world workflow set: `rep_math_function_line_v1`, `rep_phys_pendulum_wave1_v1`, `rep_econ_supply_demand_tax_v1`.
- Projectile and damping promotion remain G3.
- No canonical curriculum alignment, external student success, role toggle, new syntax, or `state_hash` formula claim is made.

Evidence:

- `python tests/run_seamgrim_curriculum_workflow_three_worlds_check.py` -> PASS.
- `node tests/seamgrim_curriculum_workflow_three_worlds_runner.mjs` -> PASS.
- `python tests/run_pack_golden.py seamgrim_curriculum_workflow_three_worlds_v1` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/app.js` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/project_snapshot.js` -> PASS.
- `node tests/seamgrim_project_snapshot_runner.mjs` -> PASS.
- `git diff --check -- <G2 paths>` -> PASS with CRLF normalization warnings only.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: prediction/run/explanation/save/reopen workflow for the three active representative lessons.
- Docs/evidence closed: `seamgrim_curriculum_workflow_three_worlds_v1` pack/checker.
- Pending: G3 projectile and damping promotion.

## G3 Projectile And Damping Promotion

Implementation:

- Kept `rep_phys_projectile_xy_v1` as the existing projectile representative lesson and added it to the G3 promotion workflow pack.
- Added promoted damping representative lesson `rep_phys_damped_oscillation_v1` under `solutions/seamgrim_ui_mvp/lessons/`.
- Added damping lesson product files: `lesson.ddn`, `meta.toml`, `text.md`, preset input, and checklist.
- Added `rep_phys_damped_oscillation_v1` to active lesson allowlist and catalog index.
- Updated the Wave 3A lesson card damping row from source id `ssot_edu_phys_p011_01_underdamped_xt` to promoted representative id `rep_phys_damped_oscillation_v1`.
- Added pack/checker/browser runner:
  - `pack/seamgrim_projectile_damping_promotion_v1`
  - `tests/seamgrim_projectile_damping_promotion_runner.mjs`
  - `tests/run_seamgrim_projectile_damping_promotion_check.py`

Scope boundary:

- The source lesson `ssot_edu_phys_p011_01_underdamped_xt` is not deleted or edited.
- The promoted representative is product/catalog evidence only; no SSOT update, new DDN syntax, or `state_hash` formula change.
- No five-lesson completion claim yet; G4~G8 remain pending.

Evidence:

- `python tests/run_seamgrim_projectile_damping_promotion_check.py` -> PASS.
- `node tests/seamgrim_projectile_damping_promotion_runner.mjs` -> PASS.
- `python tests/run_pack_golden.py seamgrim_projectile_damping_promotion_v1` -> PASS.
- `python tests/run_pack_golden.py seamgrim_curriculum_cards_v0` -> PASS.
- `python tests/run_seamgrim_curriculum_cards_check.py` -> PASS through G3 checker.

Status:

- Behavior closed: projectile and promoted damping lessons can run through product route, curriculum inquiry artifact, save, and reopen workflow.
- Docs/evidence closed: `seamgrim_projectile_damping_promotion_v1` pack/checker.
- Pending: G4 prediction/experiment/explanation artifact unification.

## G4 Prediction/Experiment/Explanation Artifact Bundle

Implementation:

- Added `solutions/seamgrim_ui_mvp/ui/curriculum_artifact_bundle.js`.
- RunScreen now emits `seamgrim.curriculum_artifact_bundle.v0` from the existing curriculum inquiry artifact.
- The bundle contains exactly three artifact kinds: `prediction`, `experiment`, `explanation`.
- The experiment artifact uses product run evidence (`runtime_hash`, status, observations) and keeps state-hash participation false.
- `project_snapshot.v0` now includes optional `curriculum_artifact_bundle` alongside `curriculum_inquiry_artifact`.
- Added product selector `data-curriculum-artifact-bundle`.
- Added pack/checker/browser runner:
  - `pack/seamgrim_curriculum_artifact_bundle_v1`
  - `tests/seamgrim_curriculum_artifact_bundle_runner.mjs`
  - `tests/run_seamgrim_curriculum_artifact_bundle_check.py`

Evidence:

- `python tests/run_seamgrim_curriculum_artifact_bundle_check.py` -> PASS.
- `node tests/seamgrim_curriculum_artifact_bundle_runner.mjs` -> PASS.
- `python tests/run_pack_golden.py seamgrim_curriculum_artifact_bundle_v1` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/curriculum_artifact_bundle.js` -> PASS.
- `node --check solutions/seamgrim_ui_mvp/ui/screens/run.js` -> PASS.
- `node tests/seamgrim_project_snapshot_runner.mjs` -> PASS through G4 checker.

Status:

- Behavior closed: five Wave 3A representative lessons produce unified prediction/experiment/explanation artifact bundle in product browser workflow.
- Pending: G5 explicit/declarative model comparison teaching surface.

## G5 Explicit/Declarative Model Comparison Teaching

Implementation:

- Added `solutions/seamgrim_ui_mvp/ui/curriculum_model_comparison.js`.
- RunScreen now emits `seamgrim.curriculum_model_comparison.v0` for each representative lesson.
- Projectile uses the existing `rep_phys_projectile_xy_v1/representation_pair.detjson` explicit tick vs `세움` teaching pair.
- Other representative lessons show explicit runtime model as landed and declarative comparison as a candidate boundary.
- `project_snapshot.v0` now optionally includes `curriculum_model_comparison`.
- Added product selector `data-curriculum-model-comparison`.
- Added pack/checker/browser runner:
  - `pack/seamgrim_model_comparison_teaching_v1`
  - `tests/seamgrim_model_comparison_teaching_runner.mjs`
  - `tests/run_seamgrim_model_comparison_teaching_check.py`

Evidence:

- `python tests/run_seamgrim_model_comparison_teaching_check.py` -> PASS.
- `node tests/seamgrim_model_comparison_teaching_runner.mjs` -> PASS.
- `python tests/run_pack_golden.py seamgrim_model_comparison_teaching_v1` -> PASS.
- `node tests/seamgrim_projectile_representation_pair_runner.mjs` -> PASS through G5 checker.

Status:

- Behavior closed: five representative lessons expose explicit/declarative model comparison teaching surface without claiming declarative runtime completion.
- Pending: G6 semantic scenes across five lessons.

## G6 Semantic Scenes Across Five Lessons

Implementation:

- Added `solutions/seamgrim_ui_mvp/ui/curriculum_semantic_scene.js`.
- RunScreen now emits `seamgrim.curriculum_semantic_scene.v0` from each lesson card's controls, observations, concept labels, primary view, and prompts.
- The semantic scene is exposed in the product run screen through `data-curriculum-semantic-scene` and `window.__SEAMGRIM_CURRICULUM_SEMANTIC_SCENE__`.
- `project_snapshot.v0` now optionally includes `curriculum_semantic_scene`; save/reopen/clone/restore paths preserve it.
- Added pack/checker/browser runner:
  - `pack/seamgrim_semantic_scenes_five_lessons_v1`
  - `tests/seamgrim_semantic_scenes_five_lessons_runner.mjs`
  - `tests/run_seamgrim_semantic_scenes_five_lessons_check.py`

Scope boundary:

- The semantic scene is a teaching overlay only.
- Anchors have accessible labels and `state_hash_participation:false`.
- No view object is stored in world state.
- No semantic runtime completion, new DDN syntax, or `state_hash` formula change is claimed.

Evidence:

- `python tests/run_seamgrim_semantic_scenes_five_lessons_check.py` -> PASS.
- `node tests/seamgrim_semantic_scenes_five_lessons_runner.mjs` -> PASS through G6 checker.
- `python tests/run_pack_golden.py seamgrim_semantic_scenes_five_lessons_v1` -> PASS through G6 checker.
- `node --check solutions/seamgrim_ui_mvp/ui/curriculum_semantic_scene.js` -> PASS through G6 checker.
- `node --check tests/seamgrim_semantic_scenes_five_lessons_runner.mjs` -> PASS through G6 checker.
- `node tests/seamgrim_project_snapshot_runner.mjs` -> PASS through G6 checker.
- `git diff --check -- <G6 paths>` -> PASS with CRLF normalization warnings only.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: five representative lessons expose semantic-scene teaching overlays in product browser workflow and preserve them in project snapshots.
- Pending: G7 representative curriculum product gate.

## G7 Representative Curriculum Product Gate

Implementation:

- Added `pack/seamgrim_representative_curriculum_product_gate_v1`.
- Added `tests/seamgrim_representative_curriculum_product_gate_runner.mjs`.
- Added `tests/run_seamgrim_representative_curriculum_product_gate_check.py`.
- The G7 runner opens all five representative lessons in the product browser route and verifies:
  - curriculum inquiry artifact,
  - prediction/experiment/explanation bundle,
  - explicit/declarative model comparison surface,
  - semantic scene overlay,
  - project snapshot preservation for all four product artifacts,
  - no runtime student/teacher role toggle leak.
- Hardened `tests/seamgrim_curriculum_workflow_three_worlds_runner.mjs` to check the saved artifact hash is actually present at save time and that a runtime hash remains present after reopen, instead of relying on an earlier auto-run timing sample.
- Narrow product fix: restored curriculum inquiry artifact runtime hash is preserved after project reopen until the user edits prediction/explanation text. Fresh authoring still uses the current runtime hash.

Evidence:

- `python tests/run_seamgrim_representative_curriculum_product_gate_check.py` -> PASS.
- `node tests/seamgrim_representative_curriculum_product_gate_runner.mjs` -> PASS through G7 checker.
- `python tests/run_pack_golden.py seamgrim_representative_curriculum_product_gate_v1` -> PASS through G7 checker.
- `python tests/run_seamgrim_curriculum_cards_check.py` -> PASS through G7 checker.
- `python tests/run_seamgrim_curriculum_workflow_three_worlds_check.py` -> PASS through G7 checker.
- `python tests/run_seamgrim_projectile_damping_promotion_check.py` -> PASS through G7 checker.
- `python tests/run_seamgrim_curriculum_artifact_bundle_check.py` -> PASS through G7 checker.
- `python tests/run_seamgrim_model_comparison_teaching_check.py` -> PASS through G7 checker.
- `python tests/run_seamgrim_semantic_scenes_five_lessons_check.py` -> PASS through G7 checker.
- `git diff --check -- <G7 paths>` -> PASS with CRLF normalization warnings only.
- `git status --short -- docs/ssot` -> clean.

Status:

- Behavior closed: five representative lessons pass the integrated product gate for Wave 3A curriculum cards, inquiry artifacts, artifact bundle, model comparison surface, semantic scene overlay, and snapshot preservation.
- Pending: G8 pilot packet and final regression gate.

## G8 Pilot Packet And Final Gate

Implementation:

- Added `docs/context/reports/SEAMGRIM_WAVE3A_FIVE_LESSON_CURRICULUM_PILOT_PACKET_V1_20260712.md`.
- Added `tests/run_seamgrim_wave3a_pilot_packet_check.py`.
- Added `tests/seamgrim_wave3a_representative_viewport_gate_runner.mjs`.
- Added `tests/run_seamgrim_wave3a_representative_viewport_gate_check.py`.
- The pilot packet includes:
  - representative 5-lesson teacher review checklist,
  - 20/45/90 minute operation plans,
  - expected misconceptions and teacher questions,
  - student reading test,
  - accessibility checklist,
  - pilot log form,
  - known limitations and closure grades.
- The viewport gate checks 1440x900, 1280x800, 1024x768, and 390x844 for all five representative lessons.
- The viewport gate verifies product artifact schemas, DDN source accessibility, snapshot artifact presence, tooltip/ARIA basics, horizontal overflow absence, and visible primary view evidence. Canvas-based surfaces use nonblank canvas evidence; graph-primary surfaces use visible graph host plus runtime hash evidence.

Evidence:

- `python tests/run_seamgrim_wave3a_pilot_packet_check.py` -> PASS.
- `python tests/run_seamgrim_wave3a_representative_viewport_gate_check.py` -> PASS through G8 checker and standalone before final gate.
- `python tests/run_seamgrim_representative_curriculum_product_gate_check.py` -> PASS through G8 checker.
- `python tests/run_pack_golden.py seamgrim_curriculum_wave3a_baseline_v1 seamgrim_curriculum_cards_v0 seamgrim_curriculum_workflow_three_worlds_v1 seamgrim_projectile_damping_promotion_v1 seamgrim_curriculum_artifact_bundle_v1 seamgrim_model_comparison_teaching_v1 seamgrim_semantic_scenes_five_lessons_v1 seamgrim_representative_curriculum_product_gate_v1` -> PASS.
- `cargo check` -> PASS with existing warnings only.
- `cargo check --manifest-path tools/teul-cli/Cargo.toml` -> PASS.
- `python tests/run_ci_sanity_gate.py --profile core_lang` -> PASS.
- `git diff --check` -> PASS with CRLF normalization warnings only on pre-existing dirty files.
- `git status --short -- docs/ssot` -> clean.

Verification cleanup:

- `python tests/run_ci_sanity_gate.py --profile core_lang` updated open-log artifacts:
  - `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl`
  - `pack/open_end_to_end/open.log.jsonl`
- Both were restored to the pre-run tracked state before commit staging.

Status:

- Behavior closed: G0-G7 product gates for the checked representative 5-lesson Wave 3A vertical.
- Docs closed: G8 teacher review and pilot preparation packet.
- Not claimed: actual pilot success, canonical curriculum alignment, full Korean Manim completion, new DDN syntax, runtime `state_hash` formula change, server/cloud/login deployment.

## Final Commit List

- `e67101a chore(seamgrim): record curriculum wave3a baseline`
- `3e0248f feat(seamgrim): connect curriculum cards to lesson detail`
- `c75445b feat(seamgrim): close three representative curriculum workflows`
- `6cf4a44 feat(seamgrim): promote projectile and damping lessons`
- `905a82a feat(seamgrim): unify prediction experiment and explanation artifacts`
- `772bb5c feat(seamgrim): teach explicit and declarative model comparison`
- `80ea951 feat(seamgrim): apply semantic scenes across five lessons`
- `80f055e test(seamgrim): close representative curriculum product gate`
- G8: this commit, `docs(seamgrim): prepare five lesson curriculum pilot packet`
