# CLI shared run and AI-prompt authority W23+W24 handoff

## Outcome

This coherent milestone combines two nearby retained CLI authority reductions:

1. W23 makes shared-runtime `run --summary-json/--trace-json` publication atomic.
2. W24 removes the private teul AI-prompt selector/canonicalizer/hash implementation
   and makes both the tool CLI and retained teul adapter consume one
   `ddonirang_tool::ai_prompt` owner.

It changes real artifact-producing workflows and adds no command, public
membership, pack, runner, framework, or meta-test.

## Authority and review custody

```text
INTERNAL_CURRENT: v25.47.0 / RD-001~543
PUBLIC_LANGUAGE_SPEC: v0.6.0
SUCCESSOR_IMPACT: UNAFFECTED_WITH_ADDITIVE_OUT_OF_SCOPE_SUCCESSOR
GOAL_STATUS: ACTIVE
SSOT_CHANGE: 0
PUBLIC_SPEC_CHANGE: 0
```

Current pointer identities were reverified read-only:

- `docs/ssot/CURRENT.md`: `5c4fdea1f0a42a7f1315bcac44dd5249e77f1e6aa4fc78c7065ee69cd53d3b04`
- `docs/ssot/ssot/CURRENT.md`: `40b116735b834f0eecb2c252cc77f73a01a8be06b85421de1d53f2d1b9e534af`
- index: `2f827e7f55d23def55be590b57482e376b1d9c43cd7db2c9f72271e59c556838`
- aggregate: `d4d9bb661f1424ae5d16a6b70dc86a6bef22d13766820f6001c8f2b28f83b5e4`
- manifest: `d8a9fed64085efffefd9eac4573d7ab18975b59bebdea2009e3215a7b9268493`
- seal: `f1869520079909eed85f2737c27a0aada3b5d013ac6c5bb41a0c781a3e501f4d`
- public SPEC pointer: `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`

Review commits `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf` and
`bc84d81d4faa55974975bdb7ec60cb18d9a7ebda` are already ancestors. The
existing rolling reviewer handle is
`01a04b17-66bb-7fa3-b827-53ad450005b4`; no reviewer or review worktree was
created or dispatched by this writer.

## Exact lineage

```text
W23_BASELINE: ec050ebcfc0f2ea82f42755a434a8953b4568ce7
W23_PRODUCT_FIXED: 07ed3607066fb12e676484a6a6c097aba1de9576
W23_PRODUCT_TREE: 0e3f0d040265e3686b3708653e4074db79b75ef1
W23_HANDOFF: 37f276e63680e9f86a17c4b4c525cbb888c66a5b
W24_PRODUCT_FIXED: a4fc1e2399ebf48e92eed8c3cc0ddb796260e71e
W24_PRODUCT_TREE: 2766ac13ecf0ce4b1aa78950035d7b4527d6fef0
DIRECT_LINEAGE: YES
MERGE_COUNT: 0
```

W24 exact product paths:

- `tool/src/ai_prompt.rs`
- `tool/src/lib.rs`
- `tool/src/main.rs`
- `tools/teul-cli/src/ai_prompt.rs`

## W24 RED and authority convergence

Before W24, AI-prompt had two source implementations. The retained teul copy
was 510 lines and contained four private authority definitions covering run,
build, bundle selection, and bundle hashing. Its only local test covered the
hash vector, while the tool owner carried current-version mismatch, CRLF/lone-CR,
invariant, and golden checks.

After W24:

```text
SHARED_PRODUCT_OWNER_PATH: tool/src/ai_prompt.rs
TOOL_LIBRARY_EXPORT: ddonirang_tool::ai_prompt
TEUL_ADAPTER_LINES: 8
TEUL_PRIVATE_AUTHORITY_DEFINITIONS: 0
TEUL_SHARED_OWNER_IMPORTS: 2
TOOL_OWNER_RUN_DEFINITIONS: 1
TOOL_DIRECT_OUTPUT_WRITE_COUNT: 0
TOOL_SHARED_ATOMIC_OUTPUT_CALL_COUNT: 1
```

`AiPromptArgs` now uses typed `PathBuf` fields so both CLIs pass the same
physical path object to the shared owner without string sniffing or a private
conversion semantic.

## Product verification

Build and focused shared-owner gates:

```text
TOOL_BIN_CHECK: PASS
TEUL_BIN_CHECK: PASS
TOOL_BIN_BUILD: PASS
TEUL_BIN_BUILD: PASS
AI_PROMPT_BUNDLE_HASH: 1/1 PASS
AI_PROMPT_CRLF_LONE_CR: 1/1 PASS
AI_PROMPT_VERSION_MISMATCH_FAIL_CLOSED: 1/1 PASS
ATOMIC_PRESERVE_ON_FAILURE: 1/1 PASS
ATOMIC_REPLACE_NO_RESIDUE: 1/1 PASS
```

The two default-root/golden tests remain environment-dependent in this isolated
product worktree because `docs/ssot/**` is intentionally absent. They were not
misreported as product failures or rewritten. The real product frontdoors were
instead executed with the exact live v25.47 SSOT directory as explicit bundle
input.

Native tool/teul parity:

```text
TOOL_EXIT: 0
TEUL_EXIT: 0
OUTPUT_BYTES: 1246037
TOOL_SHA256:
  368adea6e6899da13b4a1be7e8911fd35961067cdec2d21a302c5e9f995efcec
TEUL_SHA256:
  368adea6e6899da13b4a1be7e8911fd35961067cdec2d21a302c5e9f995efcec
BYTE_EXACT_PARITY: PASS
CR_COUNT: 0
TEMP_RESIDUE: 0
```

Failure boundaries:

- directory-as-output: exit `1`, expected write diagnostic, child/partial output
  `0`, temp residue `0`;
- unknown profile: exit `1`, artifact `0`, explicit profile diagnostic.

AI-prompt is host/internal custody and is compiled out of the WASM library;
there is no applicable Workbench semantic consumer. W24 therefore does not
claim WASM/Workbench parity for a nonexistent surface and changes no existing
WASM or Workbench payload.

## Mutation

A private `build_ai_prompt` definition was reintroduced temporarily in the teul
adapter. The authority guard changed from private definition count `0` to `1`
and RED.

```text
MUTATED_TEUL_ADAPTER_SHA256:
  57aa9c6cacd7ab3a5b23e008e4f6162f080a7bca3d40052fb33d5a13fbfb47b5
RESTORED_TEUL_ADAPTER_SHA256:
  1afed938e7ac7831dbe287ff13a6567a150c484ca0de29e1340e21b72c550b06
RESTORED_PRIVATE_AUTHORITY_COUNT: 0
RESTORED_SHARED_IMPORT_COUNT: 2
RESTORED_FOCUSED_TEST: GREEN
MUTATION_RESIDUE: 0
```

## C0~C8 bounded state

| Gate | State after W24 |
|---|---|
| C0 | Historical 91-command registry stays custody; bulk promotion 0. |
| C1 | `ddn.project-run.v1` remains fixed; executable/package/alias naming OPEN. |
| C2 | Shared lang/tool and artifact-output authorities preserved; AI-prompt now has one tool owner. |
| C3 | AI-prompt/public test/view/repl membership unchanged and OPEN where applicable. |
| C4 | Migrated workflow private fallback 0; retained teul AI-prompt semantic authority reduced to 0. |
| C5 | Bounded V1-required build/test/pack/publish teul execution dependency remains 0. |
| C6 | W23 native run artifacts and W24 native AI-prompt frontdoors are deterministic and fail-closed. |
| C7 | Existing target-bound P5 PASS remains preserved; this product bundle awaits its own fixed-target review. |
| C8 | Physical crate/binary/package deletion and final retirement remain Owner-gated. |

## Anti-meta and review request

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  run artifacts publish atomically; tool and retained teul AI-prompt emit one exact shared result
REUSED_TEST_COUNT: 7 focused product gates plus 4 actual frontdoor cases
NEW_TEST_ARTIFACT_COUNT: 0
NEW_PACK: 0
NEW_RUNNER: 0
META_TEST_CREATED: 0
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
ACTIVE_REVIEW_TASK_COUNT: 0
REVIEW_BUNDLE_TARGET: W23 + W24
READY_FOR_EXISTING_ROLLING_REVIEWER: YES
```

The fixed-target review should verify W23 at `07ed3607`, W24 at `a4fc1e23`,
and this direct linear handoff, without deciding public command membership or
physical retirement.

## Slice-local blockers and nonclaims

SPEC history, PathIR public contract, public test/view/repl membership, and
VC17 exact landing remain slice-local frozen gates, not a whole-goal impasse.
PathIR/Proof P0 containment remains preserved; public P1/ERQ closure is not
claimed.

This milestone is `IMPLEMENTED_UNDER_REVIEW`. It does not claim whole C0~C8 or
P0~P6 closure, final teul retirement/deletion, V1 membership/readiness, final
RC/release, activation, legal approval, Owner Human Smoke, or Human PASS.
