# DDN V1 CLI gaji project-run teul test dependency W115

- Fixed `5ce709db1575585e1e4814e8588be39b3267f882` changes only the existing
  gaji lifecycle runner's `project-run` helper to the shared `ddonirang-tool`
  binary. `ddn.project-run.v1` and all public naming/membership remain fixed.
- Direct shared project-run succeeds; runner syntax and diff checks pass.
- Clean-target full runner is REBASE_REQUIRED before the changed helper because
  internal teul `gaji plan` exposes duplicate `ddonirang_core` and
  `ddonirang_lang` crate identities (`E0308`). No source workaround, semantic
  fallback, dependency addition, or test artifact was introduced.
- Current authority remains v25.50.0 / RD-001--551 and public SPEC v0.6.0;
  SSOT/SPEC mutation 0. W115 is not a CLI retirement or V1 closure claim.
