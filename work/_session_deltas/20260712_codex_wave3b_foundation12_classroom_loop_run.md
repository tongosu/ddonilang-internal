# 2026-07-12 Codex Wave3B Foundation12 Classroom Loop

## 경계

- Branch: `codex/queue-20260706`
- Start head requirement: `7e9500b`
- `docs/ssot/**`: read-only, direct edits prohibited.
- New DDN syntax, `state_hash` formula changes, login/account/cloud/auto-grading: out of scope.
- Runtime role toggle restoration: prohibited.
- Existing unrelated dirty/untracked files are preserved and not staged.

## 진행 로그

- G0 started: fixed 12-world baseline audit pack/checker added.
- G0 baseline generated and verified:
  - `python tests/run_seamgrim_wave3b_foundation12_baseline_check.py --write` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_baseline_check.py` PASS
  - `python tests/run_pack_golden.py seamgrim_wave3b_foundation12_baseline_v1` PASS
  - `git diff --check -- tests/run_seamgrim_wave3b_foundation12_baseline_check.py pack/seamgrim_wave3b_foundation12_baseline_v1 docs/reports/impl/SEAMGRIM_WAVE3B_FOUNDATION12_BASELINE_V1_20260712.md work/_session_deltas/20260712_codex_wave3b_foundation12_classroom_loop_run.md` PASS
  - `git status --short -- docs/ssot` clean

## G0 기준선 요약

- Target worlds: 12
- CLI `teul-cli run --madi 2 --no-open`: 10 PASS / 2 FAIL
- FAIL:
  - E1 `elem_math_number_line`: `E_PARSE_UNEXPECTED_TOKEN`
  - H2 `high_math_derivative`: `E_PARSE_COMPAT_EQUAL_DISABLED`
- Allowlisted targets: 5
- Existing dirty/untracked rows captured: 101
- Product dirty overlap: 0
- `high_math_derivative` used; `high_physics_energy` substitution not used.

## G1 결과

- Product changes:
  - `elem_math_number_line`: one-line multi-assignment condition blocks split for CLI parser compatibility.
  - `high_math_derivative`: removed stale compat `=` formula row and expanded `x^3` to `x * x * x` for current frontdoor.
  - `elem_econ_store_stock`: split one-line condition bodies and renamed internal pending-order variables for CLI/WASM parity.
  - `run.js`: observation contract fallback now turns `보임` output rows into UI observation payload rows when observation channels are absent.
  - `index.html`: stable `data-testid="lesson-observe-output-body"` selector added to the existing output body.
- Verification:
  - `node --check tests/seamgrim_wave3b_foundation12_model_alignment_runner.mjs` PASS
  - `python tests/run_pack_golden.py seamgrim_wave3b_foundation12_model_alignment_v1` PASS
  - `node tests/seamgrim_wave3b_foundation12_model_alignment_runner.mjs` PASS (`observation_payloads=[11,11,10,13,16,16,8,19,11,12,14,3]`)
  - `python tests/run_seamgrim_wave3b_foundation12_model_alignment_check.py` PASS
  - `git status --short -- docs/ssot` clean
- Boundary:
  - G1 browser validation uses `tab=studio&catalog_mode=full&lesson=<lesson_id>`.
  - Active catalog promotion remains G2.
  - No new DDN syntax and no `state_hash` formula change.

## G2 결과

- Product changes:
  - 12개 Foundation cohort를 `lesson_cards.v0.detjson`에 연결하고 active product allowlist에 승격.
  - 초등 6개와 `high_math_derivative`의 curriculum refs, prompts, controls, observations, misconception refs, display labels 추가.
  - `high_math_derivative`에 제품 조절값(`시작x`, `끝x`, `간격`)을 추가해 카드의 allowed controls와 실제 frontdoor를 맞춤.
  - Browse detail card에 학생에게 필요한 `허용 조절값`과 `관찰값`을 표시하되 internal `status_axes`/candidate/evidence fields는 노출하지 않음.
  - G1 runner를 실제 제품 흐름처럼 조절 탭을 열고 visible control을 조작하도록 보정.
- Verification:
  - `python tests/run_seamgrim_wave3b_foundation12_curriculum_cohort_check.py` PASS
  - `python tests/run_seamgrim_curriculum_cards_check.py` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_model_alignment_check.py` PASS
  - `python tests/run_pack_golden.py seamgrim_wave3b_foundation12_model_alignment_v1 seamgrim_wave3b_foundation12_curriculum_cohort_v1` PASS
  - `git diff --check -- <G2 scoped files>` PASS
  - `git status --short -- docs/ssot` clean
- Evidence:
  - `seamgrim_wave3b_foundation12_curriculum_cohort_v1` rejects missing card field, nonexistent control, nonexistent observation, and bad primary view in negative controls.
  - Browser runner verifies default Browse catalog exposes all 12, grade/subject filters work, and each card opens the real run route with blake3 hash and observation payload.
- Boundary:
  - Curriculum alignment remains candidate-level; no canonical national-curriculum claim.
  - No new DDN syntax, no `state_hash` formula change, no runtime role toggle.

### G2 verification update

- Removed stale `view_plan_path` rows from Foundation12 meta files whose
  `view_plan.detjson` is not tracked in the G2 commit. G3 will reconnect the
  explicit 12-world view plans in one dedicated gate.
- Kept tracked view-plan references for the existing pendulum/damped assets.
- Re-ran G1 regression with workspace-local cargo target:
  - `CARGO_TARGET_DIR=I:\dev\ddonilang\codex\build\cargo-target-wave3b`
  - `GIT_CONFIG_COUNT=2` with `safe.directory` and `core.excludesfile`
    overrides for sandbox-owned git status.
- Verification after stale-reference cleanup:
  - `python tests/run_seamgrim_wave3b_foundation12_model_alignment_check.py` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_curriculum_cohort_check.py` PASS
  - `python tests/run_pack_golden.py seamgrim_wave3b_foundation12_curriculum_cohort_v1` PASS

## G3 result

- Product changes:
  - Connected explicit `view_plan.v1` files to all Foundation12 lessons through
    lesson meta paths and catalog `meta_path` rows.
  - Added the 10 missing Foundation12 view-plan files and normalized the two
    existing tracked representative view plans to include `primary_view_target`,
    required anchors, and anchor accessibility names.
  - Added graph-primary view-plan support through output-row graph synthesis so
    graph lessons do not fall back to console/grid presentation.
  - Added a product-side view-plan observation merge that keeps `보임` output
    rows available to semantic anchors across transient empty frames without
    changing runtime state or `state_hash`.
  - Exposed resolved view-plan anchors in the runtime report for graph and
    space2d views while keeping view data out of `state_hash`.
- Verification:
  - `python tests/run_seamgrim_wave3b_foundation12_view_plan_check.py` PASS (`checks=48`, `worlds=12` through runner)
  - `python tests/run_pack_golden.py seamgrim_wave3b_foundation12_view_plan_v1` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_model_alignment_check.py` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_curriculum_cohort_check.py` PASS
  - `git diff --check -- <G3 scoped JS/test files>` PASS
  - `git status --short -- docs/ssot` clean
- Browser coverage:
  - 12 lessons x 4 viewports: `1440x900`, `1280x800`, `1024x768`, `390x844`.
  - Each route verifies `viewPlanRuntime=1`, resolved anchors with units and
    source provenance, nonblank graph/space2d primary view evidence, and view
    hash stability across reload and visible scrub controls.
- Boundary:
  - No new DDN syntax.
  - No `state_hash` formula change.
  - View plans remain product-side metadata and are not stored in world state.

## G4 result

- Product changes:
  - Added Foundation12-aware `lesson_plan.v0` root fields for classroom
    authoring: lesson question, prediction, explanation, misconception refs,
    reading check, rubric, deployment profile lock, allowed controls, control
    ranges, primary view, and secondary views.
  - Added product editor controls for selecting any of the 12 foundation
    worlds, editing root classroom prompts, editing activities, switching
    list/code views, saving drafts, and reopening the saved plan.
  - Generated default classroom lesson plans from current lesson catalog/card
    metadata when no bundled plan exists, while keeping the DDN world source
    separate from the lesson plan code.
  - Added responsive classroom authoring layout and stable `data-testid`
    selectors for browser validation.
- Verification:
  - `python tests/run_seamgrim_wave3b_foundation12_classroom_authoring_check.py` PASS (`behavior-closed`)
  - `python tests/run_pack_golden.py seamgrim_wave3b_foundation12_classroom_authoring_v1` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_semantic_view_plans_check.py` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_curriculum_cohort_check.py` PASS
- Browser coverage:
  - 12 lessons x 2 viewports: `1280x800`, `390x844`.
  - Each route enters the real product run screen, switches to Create, opens
    the lesson-plan editor, verifies the 12-world selector, root classroom
    fields, list/code semantic roundtrip, local save/reopen, and separate DDN
    source tab.
- Boundary:
  - No new DDN syntax.
  - No `state_hash` formula change.
  - No runtime student/teacher role toggle.
  - Product workflow stops at local authoring and draft persistence; classroom
    assignment/distribution remains later work.

## G5 result

- Product changes:
  - Added `classroom_exchange.v0` lesson-bundle envelopes to the existing local
    package payload path, including `kind=lesson_bundle`, `exchange_id`,
    `lesson_id`, `origin_hash`, `payload_hash`, deployment profile ref/hash,
    project snapshot, curriculum artifact summary, run evidence slot, lineage,
    local label, sequence, and local-only boundaries.
  - Added validation for missing/wrong exchange schema, wrong kind, exchange
    payload hash mismatch, oversized exchange payload, deployment profile hash
    mismatch, and package hash mismatch.
  - Added Publish-space product controls for exporting the current lesson as a
    sealed classroom bundle while preserving the existing representative course
    bundle buttons.
  - Import keeps the exchange hash/profile hash on imported lesson rows and
    opens the package in the existing student onboarding run path.
- Verification:
  - `python tests/run_seamgrim_wave3b_classroom_exchange_check.py` PASS (`behavior-closed`)
  - `python tests/run_pack_golden.py seamgrim_wave3b_classroom_exchange_v1` PASS
  - `python tests/run_seamgrim_wave3b_foundation12_classroom_authoring_check.py` PASS
  - `git status --short -- docs/ssot` clean
- Browser coverage:
  - Teacher opens a Foundation12 lesson, switches to Publish, edits the
    deployment profile draft, exports the current lesson bundle, and imports it
    in a fresh browser context.
  - Tampered exchange schema, exchange payload hash, deployment profile hash,
    package hash, and oversized payload are rejected with Korean diagnostics.
  - Rejected diagnostics are checked for no internal error code, absolute URL,
    Windows path, or stack-prefix leakage.
  - Deployment profile editor is absent from the imported run screen.
- Boundary:
  - No new DDN syntax.
  - No `state_hash` formula change.
  - No runtime student/teacher role toggle.
  - No account/cloud/public upload or cryptographic signature claim.

## G6 result

- Product changes:
  - Preserved Foundation curriculum card data inside local lesson-bundle rows
    and restored it on import so student assignments expose question,
    prediction, explanation, and artifact panels.
  - Added deployment-profile control enforcement for imported assignments:
    only profile `allowed_controls` are shown, and their min/max/step bounds
    are applied to the product slider panel.
  - Added local `seamgrim.student_assignment_version.v0` save/restore for
    imported assignments. The snapshot records lesson/package/exchange hashes,
    prediction/explanation text, run evidence hash, control snapshot,
    observation refs, DDN source, local label, and lineage.
  - Added a student-facing "내 버전 저장" action in the run delivery area,
    with localStorage restore when the same bundle is reopened.
- Verification:
  - `python tests/run_seamgrim_wave3b_student_assignment_check.py` PASS (`behavior-closed`, 12 lessons)
  - `python tests/run_pack_golden.py seamgrim_wave3b_student_assignment_v1` PASS
  - `python tests/run_seamgrim_wave3b_classroom_exchange_check.py` PASS
  - `git status --short -- docs/ssot` clean
- Browser coverage:
  - For all 12 Foundation lessons: teacher export current lesson bundle,
    student import, prediction entry, run, profile-limited control change,
    reset/re-run, explanation entry, DDN source availability, student version
    save, and reopen restore in a new page.
  - Each saved student version has one profile-limited control snapshot and a
    runtime hash linked to the imported bundle exchange hash.
- Boundary:
  - No new DDN syntax.
  - No `state_hash` formula change.
  - No runtime student/teacher role toggle.
  - Student version persistence is local browser storage only; submission
    exchange is G7.

## G7 result

- Product changes:
  - Added `classroom_exchange.v0` student-submission envelopes on top of the
    local assignment flow. The payload records response text, run evidence,
    profile-limited control snapshot, observation refs, the student project
    snapshot, lineage, local label, local-only boundaries, an evidence binding
    hash, and a deterministic payload hash.
  - Added student-facing product actions to copy/download the submission JSON
    after an imported assignment has a run hash and student label.
  - Added import handling for standalone student submissions. A submission
    reopens as a reviewable local package lesson, restores the student response
    and run evidence, and keeps the original bundle/project snapshot available
    without executing uploaded script or markup.
  - Added validation for wrong schema/kind, oversized submissions, missing run
    evidence, and payload hash mismatch with Korean diagnostics.
  - Hardened the assignment browser runner wait point so imported assignments
    fail with product state diagnostics instead of a generic disabled-button
    timeout.
- Verification:
  - `python tests/run_seamgrim_wave3b_student_submission_check.py` PASS
    (`behavior-closed`)
  - `python tests/run_pack_golden.py seamgrim_wave3b_student_submission_v1`
    PASS
  - `python tests/run_seamgrim_wave3b_student_assignment_check.py` PASS
  - `git status --short -- docs/ssot` clean
- Browser coverage:
  - Teacher exports a Foundation lesson bundle, student imports it, writes a
    prediction, runs the world, changes an allowed control, re-runs, writes an
    explanation, saves a local student version, and exports a student
    submission.
  - Editing the explanation changes both payload and evidence-binding hashes.
  - A fresh browser context imports the submission and verifies the restored
    lesson id, response text, run evidence, local label, and no injected image
    from malicious explanation text.
  - Wrong schema, bad payload hash, and oversized submission payloads are
    rejected by the product import path.
- Boundary:
  - No new DDN syntax.
  - No `state_hash` formula change.
  - No runtime student/teacher role toggle.
  - No account/cloud/public upload, auto-grading, or cryptographic signature
    claim.

## G8 result

- Product changes:
  - Added a Publish-space local student submission archive that collects
    `classroom_exchange.v0 kind=student_submission` payloads without creating a
    new exchange schema.
  - Added review records with local label, lesson/origin scope, prediction and
    explanation presence, run evidence hash, observation ref count, control
    diffs against the submitted origin baseline, integrity status, version
    status, duplicate status, and reopen availability.
  - Added deterministic duplicate detection, same lesson/origin enforcement,
    Korean diagnostics for rejected additions, submission reopen through the
    existing product import path, and local archive export with
    `auto_score_claim=false`.
  - Added additive `origin_control_baseline` to student assignment snapshots so
    new submissions can show control diffs against the original assignment
    control values. Older submissions without the field remain importable and
    display missing-baseline status.
- Verification:
  - `python tests/run_seamgrim_wave3b_submission_inbox_check.py` PASS
    (`behavior-closed`)
  - `python tests/run_seamgrim_wave3b_teacher_submission_archive_check.py`
    PASS (`behavior-closed`)
  - `python tests/run_pack_golden.py seamgrim_wave3b_teacher_submission_archive_v1 seamgrim_wave3b_student_submission_v1`
    PASS
  - `python tests/run_seamgrim_wave3b_student_submission_check.py` PASS
  - `python tests/run_seamgrim_wave3b_student_assignment_check.py` PASS
  - `git status --short -- docs/ssot` clean
- Browser coverage:
  - Teacher exports one Foundation lesson bundle; three separate student
    contexts import it, run the world, change one allowed control, write
    prediction/explanation, and export distinct student submissions.
  - Publish archive accepts the three same-origin submissions, renders row
    summaries and changed-control diffs, rejects a duplicate, rejects a valid
    different-lesson submission, exports the result list, and reopens one
    submission for project/graph/observation/code review.
- Boundary:
  - No new DDN syntax.
  - No `state_hash` formula change.
  - No runtime student/teacher role toggle.
  - No automatic scoring, account identity, cloud sync, public upload, or
    cryptographic signature claim.

## G9 result

- Product changes:
  - Added a product quality gate pack/checker that composes the existing
    Foundation12 four-viewport view-plan runner, 12-world student assignment
    runner, teacher submission archive runner, and a dedicated keyboard/a11y
    smoke runner.
  - Fixed a real mobile Publish overflow found by the G9 runner by making the
    Publish panel, deployment profile grid, and submission archive rows collapse
    to a single column below 640px.
- Verification:
  - `python tests/run_seamgrim_wave3b_product_quality_gate_check.py` PASS
    (`behavior-closed`)
  - Included by the G9 checker:
    - `python tests/run_seamgrim_wave3b_foundation12_view_plan_check.py` PASS
    - `python tests/run_seamgrim_wave3b_student_assignment_check.py` PASS
    - `python tests/run_seamgrim_wave3b_teacher_submission_archive_check.py` PASS
    - `node tests/seamgrim_wave3b_product_quality_gate_runner.mjs` PASS
    - `python tests/run_pack_golden.py seamgrim_wave3b_product_quality_gate_v1` PASS
  - `git status --short -- docs/ssot` clean
- Browser coverage:
  - Existing G3 runner covers 12 Foundation lessons x 4 viewports for primary
    view size/nonblank evidence, semantic binding, source availability, and
    view hash stability.
  - Existing G6/G8 runners cover teacher bundle export/import, student
    assignment open/run/control/explain/save, student submission export/import,
    and teacher archive collect/compare/reopen/export.
  - New G9 runner checks keyboard activation of the run button, DDN source
    access, control accessible names, shell tab labels, publish keyboard paste
    toggle, submission archive accessible name, disabled empty archive export,
    and horizontal overflow at `1440x900`, `1280x800`, `1024x768`, and
    `390x844`.
- Boundary:
  - No new DDN syntax.
  - No `state_hash` formula change.
  - No runtime student/teacher role toggle.
  - No automatic scoring, account identity, cloud sync, public upload,
    education-effect, or national-curriculum correctness claim.

## G10 result

- Product/doc changes:
  - Added the Round 0 packet report at
    `docs/context/reports/SEAMGRIM_WAVE3B_FOUNDATION12_ROUND0_PACKET_V1_20260712.md`.
  - Added integration pack `seamgrim_wave3b_foundation12_round0_packet_v1`
    and checker `tests/run_seamgrim_wave3b_round0_packet_check.py`.
  - The packet records G0~G9 commit evidence, the 12-world matrix,
    teacher self-review checklist, external student pilot prep, independent
    review request, allowed claims, and non-claims.
- Verification:
  - `python tests/run_seamgrim_wave3b_foundation12_model_alignment_check.py`
    PASS
  - `python tests/run_seamgrim_wave3b_round0_packet_check.py` PASS
  - `python tests/run_pack_golden.py seamgrim_wave3b_foundation12_round0_packet_v1 seamgrim_wave3b_product_quality_gate_v1 seamgrim_wave3b_teacher_submission_archive_v1`
    PASS
  - `python tests/run_seamgrim_wave3b_product_quality_gate_check.py` PASS
  - `cargo check` PASS (existing warnings only)
  - `cargo check --manifest-path tools/teul-cli/Cargo.toml` PASS
  - `python tests/run_ci_sanity_gate.py --profile core_lang` PASS
  - `git diff --check` PASS
  - `git status --short -- docs/ssot` clean
- Cleanup:
  - Restored sanity-generated tracked open-log outputs:
    `pack/open_bundle_artifact/run_bundle/geoul.diag.jsonl` and
    `pack/open_end_to_end/open.log.jsonl`.
- Boundary:
  - No `docs/ssot/**` changes.
  - No new DDN syntax.
  - No `state_hash` formula change.
  - No runtime student/teacher role toggle.
  - No education-effect, IDC, account, cloud, public upload, national
    curriculum correctness, Korean Manim overall completion, or AI automatic
    assessment claim.
