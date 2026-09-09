# DDL Wave 3 Product/Sum OwnedBranch handoff

- Product fixed: `c10a27a8096dd223e85183d7aa54cbe0a8524643`
- Parent: `24e6535f4ec527f53d4c4874bb21b310f9192a0f`
- Scope: internal `.ddl`/`.옮김` AST and canonical projection only; runtime, CLI, WASM, wire, IDE, SSOT and public SPEC are unchanged.
- The two fixed profiles bind `DDL.TYPE.DIRECTION.R1` and the left/right OwnedBranch identities. Section and authored branch order remain presentation-only and canon preserves them.
- Green: Wave 1 11/11, Wave 2 5/5, Wave 3 2/2; `cargo check -p ddonirang-lang`; `git diff --check`.
- Open: mutation evidence and the broader negative matrix require the next focused continuation; this handoff does not claim independent review or closure.
