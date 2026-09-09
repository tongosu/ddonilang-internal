# seamgrim_semantic_scenes_five_lessons_v1

Wave 3A G6 semantic scene pack.

The product run screen exposes `seamgrim.curriculum_semantic_scene.v0` for the five representative lessons. The overlay binds card controls to the actual slider DOM, card observations to committed `seamgrim.observation_payload.v1` rows, and the declared primary view to its rendered host. It does not store view objects in world state and does not participate in runtime `state_hash`.

This pack closes only the control/observation/primary-view binding scope. It does not claim that every lesson has every Korean-Manim measurement, camera, vector, or trajectory component.
