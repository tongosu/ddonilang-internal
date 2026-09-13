# P5 current CLI product-source candidate W11 handoff

## Custody

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: product single-writer implementation, fixed-object validation, handoff
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure single writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
CONTROL_OWNER: Owner / Codex관리Work
MANAGER: Codex관리Work
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: P5 public projection manifest source_commit; external candidate roots
REVIEWER: existing rolling reviewer only; not dispatched by this milestone
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

## Authority, goal, and reviewed predecessors

- Live internal CURRENT: v25.45.0 / RD-001~536.
- Public Language SPEC: v0.6.0.
- Persistent goal status: ACTIVE. A frozen SPEC-history slice, PathIR public contract,
  public test/view/repl membership, or VC17 exact landing is not a whole-goal blocker.
- P5 review `bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` and CLI shared-authority
  review `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` are both ancestors of this
  branch. Their target-bound PASS remains narrow and is not promoted.
- Product source fixed: `87a5d2dba04f0f63023215fe79919ca06a0acf63`, tree
  `e1133ef347da620231c6afedf5b6a8b0acad8234`.
- Predecessor handoff: `3bb5c81a8a4568fb2ebf4780cfb97fc136c06ce9`.
- Manifest fixed: `535219c44477948c0aeaba3830d01fea9d999685`, tree
  `4e995040ccc850e2ca3fb07497b86ea8af7d8348`, direct parent `3bb5c81a...`,
  merge 0.
- Fixed diff: exactly one manifest `source_commit` line, from `873d3cb2...` to
  `87a5d2db...`.
- Fixed manifest: 8,695 bytes / SHA-256
  `d71592301f538b0862d048ee07042ed117869a6d1a53454bfa3678a8865e0ad5`.

The rebind is required because the old candidate source predates the W9 atomic
artifact output and W10 shared supported-profile canon convergence. It changes a
release decision: the candidate now represents the current implemented CLI source.

## Candidate evidence

- Projection root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-87a-projection-r1`.
- Projection source: exact Git object `87a5d2db...`; projected files: 173.
- Initial tree: `sha256:180bcbc750a33a3be7b5369eefc5e82600048f10e93b7124459a5bd1ac49f4a6`.
- Candidate-WASM substituted tree:
  `sha256:8277058de943b241b6252cd0680e8af2d02c164f1ca4924c173bfb900bf1d09d`.
- Candidate WASM semantic identity:
  `sha256:cc283abef92b1b2df5b97ed5f527d3b7337b6236d3076c70cdcfffddae062974`.
- Candidate WASM bytes SHA-256:
  `2b16ea041317b835bcf5a1574dd12e0427b5ce221005da733a7b63f8b800c9f6`.
- Remap policy: `sha256:d80fdb94b79cbab3ac4fd580c701a0dc5947676706964cf0252111237ed6646a`.
- Validation receipt identity:
  `sha256:eebce06911086e4bd1b5ab9e47525d1ec23b526a8a7d7c2d48bfb4d9406ebcc4`.
- Required projection roles: 4/4; normal validation PASS.
- Windows root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-87a-windows-r1`.
- Windows artifact: `ddonirang.exe`, 7,038,464 bytes, SHA-256
  `b356afb0fde8331c990b9725d52b3311dbe432b2c9ba0b48d7a04e6f37740554`.
- PE stack reserve: 16,777,216 bytes; forbidden path occurrences: 0; startup/help PASS.
- Artifact executable count: 1; executable `teul-cli` ASCII occurrences: 0.
- Public Cargo package list contains six shared product crates and teul packages 0.
- Projection teul path matches: 0. Three source-text mentions are guard/provenance
  references in `test_project_public_source.py`, `tool/src/bin/ddonirang.rs`, and
  `tool/src/preprocess.rs`; they are not a package, executable, or semantic dependency.

## User workflows and fail-closed checks

- Existing `project_run_physics_v1` workflow: exit 0, 16,488 output bytes, exact
  expected SHA-256 `f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578`.
- `project-run` positional start plus `--virtual`: exit 2 with
  `E_CLI_OPTION_CONFLICT`.
- Candidate `canon --source-profile v1-core-v25`: exit 0 and preserves V25 `:=`/`<-`.
- Candidate canon omitted profile: exit 2 / `E_SOURCE_PROFILE_REQUIRED`.
- Candidate canon unknown profile: exit 1 / `E_SOURCE_PROFILE_UNSUPPORTED`.
- First WASM candidate built from the docs-only manifest commit was rejected by the
  substitution guard because its source identity did not equal product fixed `87a5d2db...`.
  An exact `87a5d2db...` LF materialization was then built; substitution and validation
  returned GREEN. No tracked source or tracked WASM was written.

Existing projection/remap tests were reused: 55/56 PASS. The one failure is an old
assertion requiring tracked-WASM internal path count 115; the current tracked binary
reports 0. This is successor evidence assertion drift, not a candidate build or path-clean
failure. No new runner, pack, checker, framework, or meta-test was created.

## Open gates and nonclaims

Strict `--require-spec-links` remains fail-closed for ten absent historical/candidate
SPEC manifests. No historical or candidate SPEC was copied into the projection. Public
`test`, `view`, and `repl` membership remains OPEN. Physical `tools/teul-cli` deletion,
executable/package naming, and legacy duration remain Owner-gated.

Status is only:

```text
P5_CURRENT_CLI_PRODUCT_SOURCE_CANDIDATE_IMPLEMENTED_UNDER_REVIEW
P5_STRICT_PUBLIC_SPEC_LINK_GATE_OPEN
```

This does not claim P5 closure, V1 membership/readiness, release/publication,
activation, legal approval, Owner Human Smoke, or Human PASS.
