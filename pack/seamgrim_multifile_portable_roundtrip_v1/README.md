# seamgrim_multifile_portable_roundtrip_v1

G11 pack for DDN AST project Workbench Wave 2.

This pack fixes the product contract that a multi-file local project authored in the Seamgrim editor is saved inside the existing `seamgrim.project_snapshot_artifact.v0` wrapper without collapsing to `lesson.ddn`.

The behavior gate is the browser runner:

- editor project tree authoring and WASM project run summary
- snapshot artifact `local_package_payload.kind == seamgrim.local_project_tree.v0`
- server save, edit-link reopen, view-link clone
- workbench portable import preview/open/save/reopen with multi-file tree preserved
- run lineage preservation across export/import/reopen/clone
- same local project data dir server restart reopen smoke
- corrupt and old wrapper import rejection without state loss

Non-claims: no public registry, no Git resolver, no new DDN grammar, no runtime `state_hash` formula change.
