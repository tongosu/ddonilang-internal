# 2026-07-11 Codex Session Delta - Wave 2A Independent Audit Fix

## Boundary

- Audited `34bf0c8..fc1d599` on `codex/queue-20260706`.
- Kept `docs/ssot/**`, DDN parser/runtime semantics, and `state_hash` formula unchanged.
- Preserved unrelated dirty and untracked files.

## Findings And Fixes

- `lesson_plan.v0` claimed save/reopen but only proved same-page screen navigation. Drafts are now stored per lesson, restored after a full page reload, and the browser runner proves that path.
- The semantic cursor used the full result-column height, leaving the selected graph below or outside its clipping parent. Desktop result layout now reserves a bounded semantic-cursor row and a visible graph row.
- Run comparison/history belonged to the graph panel and displaced the graph. It now lives in the `검증` panel.
- Lesson activity metadata exposed internal `obs.*` anchor IDs. The product surface now shows Korean observation labels while keeping IDs in the internal contract.
- Student-facing lesson copy no longer exposes camera policy IDs or `state_hash`; those details remain in the verification surface.
- Responsive evidence now includes 1280x720 and rejects a graph canvas outside either the result panel or its graph host.
- Pendulum camera evidence could race a still-advancing observation. The runner now waits for a stable paused draw payload and takes the camera baseline after the angle-visibility roundtrip.
- Semantic cursor readiness now includes the rendered kinetic-energy unit, removing a transient false pass/fail window.
- A follow-up review found that the hidden student/teacher switch DOM and handlers still existed. They are now structurally absent, the old switch pack is superseded, and G1 checks reject their reintroduction.

## Verified Closure

- Wave 2A product checkers and related pack goldens: PASS.
- Responsive workflow: PASS at 1440x900, 1280x720, 1024x768, and 390x844.
- Pendulum CLI frontdoor, `cargo check`, teul-cli check, and `core_lang` sanity: PASS.
- `docs/ssot/**`: clean.

Closure remains limited to the checked pendulum product vertical. General Korean Manim authoring, arbitrary live hooks, and language-runtime semantics are not claimed.
