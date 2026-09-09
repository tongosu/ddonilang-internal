# P5 Seamgrim public-candidate self-contained handoff

## Fixed product target

- Base: `feb4b0468abe254c12d8d438a5c3e50ba3dae52f`
- Product fixed: `2a89750cc354d731bd674be9d09eddb2ab2174c6`
- Scope: release lesson projection only.

## Product change

The release `reps_only` allowlist had all fifteen required representative lessons
plus nine internal or deferred lessons.  The server therefore exposed an
overbroad release inventory.  The fixed target:

- reduces the allowlist to the exact fifteen required representatives;
- fails closed when the release allowlist is absent or incomplete; and
- serves `/lessons/index.json` through the same release projection as
  `/api/lessons/inventory`, preserving the source catalog as internal custody.

No checker was relaxed and no lesson source was deleted.

## Evidence

- `python -m py_compile solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py`: PASS
- `python solutions/seamgrim_ui_mvp/tools/ddn_exec_server_check.py --profile release --timeout-sec 15`:
  `ok: release_inventory=15 mode=reps_only`
- Direct server projection inspection: API/index ID sets equal, both unique, and
  the index projection is deterministic.
- M1 required-row removal: RED
  `representative_ids_missing:rep_cs_linear_search_timeline_v1`; exact restore
  SHA-256 `326dab6209e8f856eda3be8fa59484caec3d3aea2a179848ea665fea228d5cc4`; GREEN.
- M2 deferred-row insertion: RED
  `release_inventory_mismatch:missing=-:extra=elem_econ_allowance_budget`;
  exact restore to the same SHA-256; GREEN.
- Windows public-candidate run materialized exactly `ddonilang.exe`,
  `ddonirang.exe`, and `또니랑.exe`; each `--help` exited zero and no `teul`
  artifact was present.  The initial long build process detached from its
  command host before a terminal exit could be collected, so this handoff does
  not claim the full script verdict from that unobserved exit alone.

## Boundaries

- The known `include_str!("../../pack/..." )` occurrence is inside
  `#[cfg(test)]` in `tool/src/gaji_seal_workflow.rs`; it is not a public runtime
  build dependency.  No duplicate product asset was created.
- Browser validation remains `ENVIRONMENT_BLOCKED` (policy/browser automation
  unavailable).  It was not bypassed.
- P5 release, V1 readiness, activation, legal clearance, publication, and
  Human PASS remain open.
