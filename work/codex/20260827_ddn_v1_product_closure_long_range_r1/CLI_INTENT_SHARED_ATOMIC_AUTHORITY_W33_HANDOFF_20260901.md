# CLI intent shared atomic authority W33 handoff

## Fixed identity

- Authority: internal SSOT v25.47.0 / RD-001~543; public Language SPEC v0.6.0.
- Baseline: `6157cdd9f6ee0ddfe6367a59171d7d7f396b17c6`.
- Product fixed commit: `ca32887cc0e88040c583d53e88e16055f3c92b02`.
- Product fixed tree: `b5e5ada882d083dc4ff6fa7fe30e400bcc5a616f`.
- Direct parent: yes. Merge count: 0.

## Product workflow

The existing `intent inspect`, `intent mock`, and `intent merge` workflows now consume one product-owned `ddonirang_tool::intent_workflow` implementation. The teul module is a three-symbol adapter only. Parsing, fixed-point conversion, receive-sequence monotonicity, canonical intent-bundle construction, and artifact publication no longer live as private teul authority for these commands.

The existing command spelling and payloads are preserved. No public command membership, schema, alias, executable/package name, parser, runtime, value, or fallback authority was added.

Exact product paths:

- `tool/src/intent_workflow.rs`
- `tool/src/lib.rs`
- `tools/teul-cli/src/cli/intent.rs`

## Existing evidence reused

- `pack/gogae5_w45_intent_bundle` inspect: exact golden bundle 1/1 PASS.
- Merge of the same fixed intent JSONL: exact bundle parity 1/1 PASS.
- Mock from the existing external-intent source: exact agent/madi/recv-seq/kind/text identity 1/1 PASS.
- Existing duplicate and reverse `recv_seq` tests, moved with the authority: 2/2 PASS.
- Directory-target fail-closed: inspect/mock/merge 3/3 exit 1 with the shared non-file-target diagnostic; published entries 0.
- Tool lib regression: 554 PASS plus unchanged two isolated-checkout missing-`docs/ssot` environment failures in `ai_prompt`; new regression 0.
- `teul-cli` offline build: PASS.
- `git diff --check`: PASS.

New pack: 0. New runner: 0. Meta-test: 0.

## Mutation evidence

No duplicate mutation was created. These outputs consume the exact shared target guard verified immediately in W32: guard inversion RED, byte-exact restore SHA-256 `9abdfe9426519552cba0227ce50d08e1bb333f78e2282a2463f0a8ba081805f7`, rebuild GREEN, residue 0. The helper remained byte-identical in this fixed commit.

## Gate impact and nonclaims

- Private teul semantic authority for intent inspect/mock/merge: 0.
- Native fixed-target payload and failure behavior: PASS.
- WASM/Workbench: no new public projection or JS/UI reconstruction; tracked WASM and visible UI diff 0.
- Repository-wide required teul dependency, public command membership, executable/package retirement, and physical deletion remain OPEN.
- Ready to join the existing coherent CLI convergence rolling-review bundle; new review task/worktree/reviewer 0.

This does not claim C0~C8 closure, V1 membership/readiness, P0~P6 closure, release, activation, legal approval, or Human PASS.
