# V1 official CLI integration and teul-cli retirement W1 handoff

Date: 2026-08-30

## Disposition

```text
STATUS: V1_OFFICIAL_CLI_CANDIDATE_IMPLEMENTED_UNDER_REVIEW
PUBLIC_PRODUCT_TEUL_BINARY_RETIREMENT_CANDIDATE: IMPLEMENTED_UNDER_REVIEW
PHYSICAL_TOOLS_TEUL_CLI_SOURCE_RETIREMENT: OPEN
WHOLE_CLI_COMMAND_MEMBERSHIP: OPEN
```

This vertical adds one small native V1 CLI candidate backed only by the shared
`ddonirang-tool` language/runtime surfaces and changes the bounded Windows
public-source candidate from two executables to one `ddonirang.exe`. The
historical `tools/teul-cli` source and goldens remain intact and compiling as
internal migration custody. This is therefore a real public-product binary
retirement step, not a claim that all private source or 63 historical commands
have been deleted or migrated.

## Authority and lineage

The task was requested against v25.35, but the read-only Owner-approved live
CURRENT pointers had advanced and agreed on internal SSOT v25.40.0 / RD-001~515.
Public Language SPEC remains v0.6.0.

```text
INTERNAL_CURRENT: v25.40.0 / RD-001~515
ROOT_CURRENT_SHA256: 91fc1cbf89f6782e581dec8070b0798d0714029b69be42de16210a7df4d05ed5
SSOT_CURRENT_SHA256: 077d62cb5237e7a6ae57aba55b72c23a95dc6036c5a7ca784f1d92fd8884de81
SSOT_INDEX_SHA256: 01588eb9b3de4c1420db8489c14d78b125185457f79436fbccc4e3e7fe8351ec
SSOT_AGGREGATE_SHA256: 9b6f64628cbb1bb176caeb95fddcb77756890e4c5803704e1bb92195dbfd4e61
SSOT_MANIFEST_SHA256: 23cbd9f58f26f3e52ab26d3aac829c0fa9c160de058fa3f1c2f6da03094dae80
SSOT_SEAL_SHA256: 26770b32f516acfe11af0c678bec3c3ece019b1a5e5327b980147a3dd653e5b1
PUBLIC_SPEC_CURRENT_SHA256: 6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0
BASELINE: ee9d28bb45e04c9d7b7247d790509dbe0d4bd799
PRODUCT_TEST_FIXED: 274183623f43c526975c7402ffa0fdf6e0d11e66
PRODUCT_TEST_TREE: 64b4457e561b39461ca6755bc90f011b9b2bee39
PRODUCT_TEST_PARENT: ee9d28bb45e04c9d7b7247d790509dbe0d4bd799
PUBLIC_PROJECTION_CONTRACT_FIXED: 31f00c58993dd7ba153de7839c5c1a99dbede023
PUBLIC_PROJECTION_CONTRACT_TREE: 393163b41ffc51d54808140c01a5e5990422dc36
PUBLIC_PROJECTION_CONTRACT_PARENT: 274183623f43c526975c7402ffa0fdf6e0d11e66
MERGE_COUNT: 0
```

v25.40 RD-215 keeps one shared lang/runtime native/WASM direction, forbids a
legacy compatibility alias when external users are zero, and requires needed
commands/goldens to migrate before source deletion. RD-249 keeps the separate
`teul-cli run` evaluator from becoming a permanent semantic family. The
current `teul-cli run` path already consumes shared runtime; this slice does
not recreate a private parser/runtime or hidden fallback.

## Product change

The product fixed commit changes exactly:

- `tool/src/bin/ddonirang.rs`
- `tests/run_v1_core_supported_ingress_w1.py`
- `scripts/build_windows_x64_public_candidate.ps1`

The new CLI candidate exposes only `run`, `check`, `canon`, help and version.
Every source command requires an explicit supported source-profile identity.
Omitted/unknown profiles, unknown options and legacy V25 `=` definition input
fail closed. `run`, `check` and `canon` consume the existing shared
`runtime_surface`, `source_analysis` and supported-profile canon authority.

The Windows builder now collects only `ddonirang.exe`; it no longer builds or
copies `teul-cli.exe` as a public candidate artifact. The public projection
contract removes the entire `tools/teul-cli` tree and its obsolete path
replacement. Its fixed identity is:

```text
MANIFEST_PATH: work/codex/20260827_ddn_v1_product_closure_long_range_r1/P5_WINDOWS_X64_PUBLIC_SOURCE_RC_W1/PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson
MANIFEST_BYTES: 8695
MANIFEST_SHA256: ddb5de5c60ce20b6d40b3297e164596c814bf6e1bbaded9bdb80569307a41293
MANIFEST_SOURCE_COMMIT: 274183623f43c526975c7402ffa0fdf6e0d11e66
```

The historical filename is retained as custody; its schema/status now bind the
v25.40 official-CLI retirement candidate.

## RED, GREEN and regression

Pre-change product RED:

```text
cargo run -q -p ddonirang-tool --bin ddonirang -- --help
exit 101: no bin target named `ddonirang`
```

Post-change verification:

```text
cargo test -p ddonirang-tool --bin ddonirang: 2/2 PASS
python tests/run_v1_core_supported_ingress_w1.py:
  native 7 PASS
  native/WASM exact 2 PASS
  tracked-WASM cases 10 PASS, repeats 4
  official CLI positive 3 PASS / negative 3 PASS
cargo test -p ddonirang-tool --lib: 527/527 PASS
cargo check --locked --manifest-path tools/teul-cli/Cargo.toml: PASS
public projection/remap/validator unit tests: 61/61 PASS
Windows build script PowerShell parse: PASS
git diff --check: PASS
```

No new pack, runner or checker was created. The existing supported-ingress
runner was extended. No mutation harness was added: concrete omitted-profile,
unknown-profile and legacy-definition invocations already exercise the
fail-open risk directly, so the anti-meta stop rule ended additional mutation.

The tracked-WASM freshness manifest is already stale against the baseline
before this CLI vertical: its recorded build-script SHA-256 is
`33b2db4e...`, while the unchanged baseline/current `build_wasm_tool.ps1`
canonical SHA-256 is `4b1e0fe9...`. The new bin also adds one file to the
broad source fingerprint. This pre-existing rebase-required tracked artifact
was not silently promoted or rewritten. Instead a clean fixed-product-head,
candidate-only WASM was built without tracked writes:

```text
WASM_CANDIDATE_SEMANTIC_IDENTITY: sha256:c49ccf3ad6048a31abc1faba026a0cd1f57a2cdd523c5f043ef67c09e253bec6
WASM_BYTES: 5559604
WASM_SHA256: 017e43e8a6a3fdb5ef383629ed4e9394efcc6ba37eeda1e2662f2eafb4e66eab
WASM_RECEIPT_BYTES: 2470
WASM_RECEIPT_SHA256: 39f1203e9cdd173fd1635f20a863b2fdf41f2dd25210841250270406b7ca7840
TRACKED_WASM_WRITE: 0
```

## Public-source and Windows A/B result

The bounded projection from exact product fixed commit contains 169 files.
It has `tools/teul-cli` source count 0 and contains the new official CLI
candidate source. After candidate-WASM substitution it validates cleanly.

```text
PUBLIC_PROJECTION_DIR: I:/home/urihanl/ddn/codex/out/ddn-v1-cli-retirement-public-projection-27418362-r1
PUBLIC_RECEIPT_DIR: I:/home/urihanl/ddn/codex/out/ddn-v1-cli-retirement-public-receipts-27418362-r1
PROJECTED_FILE_COUNT: 169
BEFORE_PUBLIC_TREE: sha256:4bf139ae449e0d9de032f33d4e6185378fe97cab23423c906cf01a4228c8bb45
AFTER_PUBLIC_TREE: sha256:b45e716d9fb83f232aa01369802f49bd16908adc6c7a8dc32559a0ed3b644d2f
PROJECTION_RECEIPT: 1461 bytes / f6a959401a9329df12775fed05bcee663dda40979b5489e7dc11d45152a4b18e
PUBLIC_TREE_MANIFEST: 33961 bytes / e78bbeeda2adc4239dbe26b216601cd2f8ee1d2b2088223f49ecfdde4e4fea8f
SUBSTITUTION_RECEIPT: 818 bytes / 4ad66ed6971860d83f72e6dcbbfb6b656a446c630d8540fd87065e82554d3f97
VALIDATION_RECEIPT: 654 bytes / 8581cb71cf8a5c68ef9bb4514a198f3a2cb125de875a74ea387ffb02956b230e
PUBLIC_PROJECTION_VALIDATION: PASS
TEUL_SOURCE_COUNT: 0
```

Two offline builds used separate target/output roots:

```text
WINDOWS_A: I:/home/urihanl/ddn/codex/out/ddn-v1-cli-retirement-windows-x64-a-27418362
WINDOWS_B: I:/home/urihanl/ddn/codex/out/ddn-v1-cli-retirement-windows-x64-b-27418362
ARTIFACT_COUNT: A 1 / B 1
ARTIFACT: ddonirang.exe
BYTES: 6221312
SHA256: 2807d72cf59d5a43b5f6af2e9cbeda06c6699da6dfb0a69705b0c104231711e4
A_EQUALS_B: true
TEUL_ARTIFACT_COUNT: 0
FORBIDDEN_PATH_OCCURRENCES: 0
PE_STACK_RESERVE_BYTES: 16777216
STARTUP: PASS
RELEASE_CHECK_PAYLOAD_A_EQUALS_B: true
RELEASE_CANON_PAYLOAD_A_EQUALS_B: true
RELEASE_RUN_PAYLOAD_A_EQUALS_B: true
CHECK_PAYLOAD_SHA256: 91b5435080c7cb4db9fdaf5a2023800df6e19c20ef08ca17f53d111c2404108b
RUN_PAYLOAD_SHA256: 50f07c707e1b97a0d525157dd5dd9fbcd37dc73f02d21e1393550528d5b91267
```

## Product value and review queue

```text
USER_WORKFLOW_CHANGED_OR_UNBLOCKED:
  A user can check, canonicalize and run Korean V25 source through one small
  shared-authority CLI candidate, while the Windows public candidate no longer
  ships the private teul-cli executable or source tree.
NEW_TEST_ARTIFACT_COUNT: 0
EXISTING_TEST_REUSED_COUNT: 5 verification surfaces plus 61 existing unit tests
META_TEST_CREATED: 0
STOP_RULE_APPLIED: YES
NEXT_PRODUCT_DECISION_ENABLED:
  management can review and bind the single public CLI candidate, then select
  the remaining KEEP/MOVE/DROP command and golden migration set before physical
  teul source deletion.
ACTIVE_REVIEW_TASK_COUNT: 0 in this execution session
NEW_REVIEW_TASK_COUNT: 0
NEW_REVIEW_WORKTREE_COUNT: 0
REVIEW_BUNDLE_TARGET: existing management-owned rolling V1 reviewer
REVIEW_NEEDED_NOW: YES, because executable identity and public-source contents changed
```

## Open gates and nonclaims

- exact final public executable/installer alias approval remains an Owner gate;
  `ddonirang.exe` is the fixed candidate name under review
- exact KEEP/MOVE/DROP command membership and golden migration remain OPEN
- `tools/teul-cli` physical source deletion and historical archive disposition
  remain OPEN until selected commands/goldens have full parity
- tracked-WASM current-head refresh remains REBASE_REQUIRED; this handoff binds
  only the candidate artifact, not tracked promotion
- whole P0/P1/P5 closure, V1 membership/readiness, rights/license, signing,
  distribution, release, activation and Owner Human Smoke/Human PASS remain OPEN

No SSOT, public SPEC, visible UI, tracked WASM or external service was changed.

