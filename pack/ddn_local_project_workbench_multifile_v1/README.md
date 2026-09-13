# ddn_local_project_workbench_multifile_v1

G9 local project workbench pack. This pack fixes the same virtual project tree used by the browser workflow: an entry file imports a helper DDN file, protected root/lock/vendor files stay read-only, and the project-run product frontdoor returns a deterministic summary.

Browser behavior is checked by `tests/ddn_local_project_workbench_multifile_runner.mjs`; this pack golden keeps the CLI product summary for the same source tree reproducible.
