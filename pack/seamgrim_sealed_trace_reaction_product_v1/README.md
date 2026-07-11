# seamgrim_sealed_trace_reaction_product_v1

Stage H product gate for Korean Manim Wave 1.

This pack fixes the minimum product behavior for a sealed observation trace reaction layer:

- the lesson loads `seamgrim.sealed_trace_reactions.v1` from a lesson-local product path;
- the run screen replays edge and level predicate states from the sealed trace;
- the sealed schedule replays precomputed event labels for zero crossing, sign change, extremum, and tolerance entry at their recorded ticks;
- V1 does not calculate those four conditions from observation samples and does not claim a live or offline condition evaluator;
- resolved actions are view-layer only: highlight, visibility, and camera-focus marker;
- the runtime emits `seamgrim.resolved_scene_trace.v1` without creating a StagePlan;
- same-target/same-property/same-priority conflicts produce `E_TRACE_REACTION_CONFLICT` instead of implicit last-write-wins;
- no live online reaction claim is made;
- parser/runtime semantics and `state_hash` formula are unchanged.

The browser runner opens the real 셈그림 UI, runs the pendulum lesson through the product frontdoor, and verifies the DDN -> WASM -> observation -> view -> sealed reaction replay path.
