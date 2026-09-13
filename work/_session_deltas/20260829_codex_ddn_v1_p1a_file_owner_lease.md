# 2026-08-29 DDN V1 P1-A file-owner lease

- exclusive writer: DDN V1제품마감Codex / `01a04a01-b812-7840-a2a3-33208dd36e36`
- implementation baseline: `fe7c38c53cc3e1946b109b8002447983c185ba9b`
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- worktree reused; new worktree 0
- lease: six existing product paths, five conditional tracked-WASM paths, exact new P1-A pack/test/report paths
- non-lease: SSOT/SPEC, lang parser/lib, tool canon/main, WASM build script, visible Workbench and all unrelated P2~P6 product paths
- scope: VC01/VC02/VC03/VC18 + VD01 through one shared supported-profile API
- first gate: bounded RED before product implementation
- expansion rule: stop the affected sub-slice and return `FILE_OWNER_EXPANSION_REQUIRED` with RED evidence

```text
P1A_FILE_OWNER_LEASE_BOUND
P1A_PRODUCT_IMPLEMENTATION_NOT_YET_STARTED
V1_READINESS_NOT_CLAIMED
```
