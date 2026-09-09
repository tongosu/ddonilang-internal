# P5 self-consistent current-source candidate W13 handoff

## Authority and execution custody

```text
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: fixed-object release candidate materialization and validation
SESSION_NICKNAME: DDN V1제품마감Codex
PROJECT_ROLE: DDN V1 closure single writer
RETURN_LABEL: [DDN V1제품마감Codex -> Codex관리Work]
EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
FILE_OWNER: tests/test_wasm_candidate_remap.py; P5 projection source pin; external candidate roots
REVIEWER: existing rolling reviewer only, not dispatched here
ORIGIN_TASK_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
```

- Live internal CURRENT: v25.45.0 / RD-001~536.
- Public Language SPEC: v0.6.0.
- Persistent goal remains ACTIVE.
- Prior target-bound reviews `bc84d81...` and `18189658...` remain bound ancestors;
  they are not reused as a PASS for this successor target.

## Fixed lineage

```text
W11 handoff              52d693f428a3a14be2cfbd8193dd8e23faa86b7e
path-clean checker fixed 47aa649b16cc50dd706e321dd5bcdf271c5a68d7
W12 handoff              73cb2cc45034896de2f6ce2ba5a4a011170102ed
candidate manifest fixed 7cb0b8bea60bb0d6f751c18fd1774571a07fa148
manifest fixed tree      c0d9d2b6075658c1eedf177c3d2b0bbda432e79c
```

Every relation is direct and merge count is 0. The manifest fixed diff is exactly one
`source_commit` line, now binding checker fixed `47aa649b...`. Manifest bytes are
8,695 / SHA-256 `dcf72c299f9296bce7ec19f0643d001b1d90622304b144ef86fb3320efa9f036`.

The candidate source is intentionally `47aa649b...`, not a later docs-only commit. It
contains the current product code and the release-critical path-clean checker correction.

## Self-consistent projection, WASM, and Windows candidate

- Clean projection root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-47aa-projection-r4`.
- Exact source commit/tree: `47aa649b...` /
  `5834fec3ba2dee5017c8156854c773c980c8c633`.
- Files: 173.
- Initial projection tree:
  `sha256:180bcbc750a33a3be7b5369eefc5e82600048f10e93b7124459a5bd1ac49f4a6`.
- Final candidate-WASM tree:
  `sha256:7758f75c4d4c59439abe264ab9f04d3355e8fa398b037e7f99a910ab71854925`.
- Candidate WASM semantic identity:
  `sha256:e0bb6574263b705d7e87d246f665c0e1ae838b6660207826694f83b830606a1a`.
- Candidate WASM bytes SHA-256:
  `2b16ea041317b835bcf5a1574dd12e0427b5ce221005da733a7b63f8b800c9f6`.
- Validation receipt identity:
  `sha256:641ddd4be4bd46a982e643cc03279c8cf79f7235c7a0eab0fa1a2323cf282a2b`.
- Required roles 4/4; normal projection validation PASS.
- Windows root:
  `I:/home/urihanl/ddn/codex/build/candidates/v1-current-cli-47aa-windows-r4`.
- `ddonirang.exe`: 7,038,464 bytes / SHA-256
  `b356afb0fde8331c990b9725d52b3311dbe432b2c9ba0b48d7a04e6f37740554`.
- PE stack reserve 16,777,216; forbidden paths 0; teul path/package 0.

The first r3 projection was used to run its included Python validators and gained a
task-owned `__pycache__`, which the validator correctly rejected as an extra file. A
delete request was not broadened. The clean r4 projection was regenerated from the same
fixed Git object and was not executed in place. r3 remains external non-authoritative
task output; r4 is the fixed candidate custody.

## Product behavior and release-gate evidence

- Product-worktree projection/remap tests: 56/56 PASS.
- Public projection's included validator tests: 35/35 PASS before r3 residue; no test is
  run in clean r4 itself.
- `project-run` existing fixture: exit 0; 16,488 bytes; byte-exact expected output.
- positional start plus `--virtual`: exit 2 / `E_CLI_OPTION_CONFLICT`.
- explicit V1 canon remains reachable and fail-closed profile behavior is preserved.
- Public Cargo package teul count: 0; projection teul path count: 0.
- New pack/runner/checker/framework/meta-test: 0/0/0/0/0.
- Tracked WASM/product source/SSOT/SPEC/visible UI writes during W13: 0.

Strict `--require-spec-links` remains a precise RED for ten absent historical/candidate
SPEC manifests. Those files were not copied or invented. Public `test/view/repl`
membership, final executable/package naming, legacy duration, and physical teul deletion
remain separately frozen.

## Review target and nonclaims

Review bundle target is W11+W12+W13 as one coherent current CLI product-source P5
candidate at manifest fixed `7cb0b8be...`, using only the existing rolling reviewer after
management dispatch. New review task/worktree/branch count is 0.

Status is only:

```text
P5_SELF_CONSISTENT_CURRENT_SOURCE_CANDIDATE_IMPLEMENTED_UNDER_REVIEW
P5_STRICT_PUBLIC_SPEC_LINK_GATE_OPEN
```

This is not P5 closure, public-command membership, teul physical retirement, V1
readiness, release/publication/activation, legal approval, Owner Human Smoke, or Human PASS.
