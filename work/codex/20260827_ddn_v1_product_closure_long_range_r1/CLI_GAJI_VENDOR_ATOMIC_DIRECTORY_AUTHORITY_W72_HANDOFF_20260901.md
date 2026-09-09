# CLI gaji vendor atomic directory authority W72 handoff

## Status

- `CLI_GAJI_VENDOR_ATOMIC_DIRECTORY_AUTHORITY_W72_IMPLEMENTED_UNDER_REVIEW`
- whole CLI convergence, teul-cli retirement, V1 readiness, release, activation, and Human PASS remain open.

## Authority and lineage

- live internal authority: v25.47.0 / RD-001~543 (read-only)
- public Language SPEC: v0.6.0 (read-only)
- branch: `codex/ddn-v1-p1a-core-supported-ingress-w1-20260829`
- baseline/handoff parent: `16f8d9ebfd4ab29bcee223a9239343057e22b298`
- product fixed commit: `92083d52bf5d8f7c1e28868c7e5543d82f4223a5`
- product fixed tree: `1741f98ae42fe1afba65c949432057e1a6acadfe`
- direct parent relation: yes
- merge count: 0

## Product value and exact diff

The existing `gaji vendor` workflow deleted the predecessor vendor directory before every locked package had been validated. A hash failure in a later package therefore destroyed the last complete artifact and left an earlier package partially published.

The fixed workflow now:

1. validates every locked package and source hash before publication;
2. rejects unsafe package paths before joining them to source or output roots;
3. copies the complete vendor set into a sibling staging directory;
4. verifies copied-package hashes;
5. publishes the directory as one atomic replacement with predecessor rollback;
6. leaves no partial vendor directory or staging/backup residue on failure.

Exact product paths:

- `tool/src/artifact_output.rs`
- `tools/teul-cli/src/cli/gaji.rs`

Source custody:

- `tool/src/artifact_output.rs`: Git blob `3b2f3cea7159d65dffa5cdafd81a3e8a793f25ef`, checkout 18,604 bytes, SHA-256 `619a663b02c376e369829777793d4ecb3145625cd8f0397b9108ded97ff7511a`
- `tools/teul-cli/src/cli/gaji.rs`: Git blob `70818becd155ff07f42adc8fc174ee431072cd6d`, checkout 122,152 bytes, SHA-256 `23b0b6cac588919a7c3b64e0e86038ec7fd47b8dcf28e44f968b609ba73ff572`

## RED, GREEN, and determinism

Baseline product-facing RED with two locked packages (`demo/a`, `demo/b`), a deliberately stale `demo/b` source, and an existing `vendor/previous.txt`:

- exit 1 / `E_GAJI_VENDOR_HASH_MISMATCH`
- predecessor survived: no
- partial `vendor/a`: yes
- index: absent

Fixed-head fault reproduction with the same semantic input:

- exit 1 / `E_GAJI_VENDOR_HASH_MISMATCH`
- predecessor survived: yes
- partial `vendor/a`: no
- staging/backup residue: 0

Fixed-head success reproduction:

- two consecutive vendor publications: exit 0 / exit 0
- published files: 5
- repeat hash set equality: exact
- predecessor removed only after complete success
- staging/backup residue: 0
- `a/gaji.toml`: `8063d39ef875cb0a0422fcf81a7ae9363f353527735a3c449df4592533881720`
- `a/main.ddn`: `0107b8782beef66c3f762a70b79e5e8900e49950689085001ec5aa52c7bcdcb2`
- `b/gaji.toml`: `f4e1d37f51b964bcfb07350ef926ad14997d59342fbb1a252e83cd2588772bd1`
- `b/main.ddn`: `f349c93fd363c3ccbd1829efbeaa75d53720b7bab8d2eab1dfb0d60a15a08ead`
- `ddn.vendor.index.json`: `831ad3d93ae3b161506b87f4327025f8fcbc2ea48aad629c4bc8fa7a8805c226`

Path containment:

- locked package path `../escape`: exit 1 / existing `E_GAJI_PATH`
- predecessor survived: yes
- escaped output: absent
- partial publish and staging residue: 0

## Tests and mutation

- reused artifact-output test module: 8/8 PASS (5 existing tests plus 3 product-unit cases in the same source module)
- reused `gaji_vendor_main_cli` focused suite: 34/34 PASS; 1,018 filtered
- fixed product binary build: PASS
- new pack: 0
- new runner: 0
- meta-test: 0

Risk-relevant mutation: reinsert destructive `remove_dir_all(out)` before validation.

- RED: hash mismatch destroyed `vendor/previous.txt` and removed the vendor directory
- exact restore: source restored byte-for-byte
- GREEN: hash mismatch preserved predecessor, partial package 0, staging residue 0
- mutation residue: 0

## Frontdoor and custody boundary

- Native CLI filesystem workflow: GREEN
- WASM: not applicable to this native directory publication seam
- Workbench: not applicable to this direct `gaji vendor` filesystem seam
- semantic parser/runtime/canon authority change: 0
- docs/ssot diff: 0
- public SPEC diff: 0
- public command membership/naming change: 0
- physical `tools/teul-cli` deletion: 0

## Anti-meta checkpoint

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: a failed vendor refresh no longer destroys the last complete offline dependency artifact or publishes a partial set.
- `NEW_TEST_ARTIFACT_COUNT`: 0
- `EXISTING_TEST_REUSED_COUNT`: 2 focused families
- `META_TEST_CREATED`: 0
- `STOP_RULE_APPLIED`: yes; no receipt/hash-tamper framework or new pack/runner was created.
- `NEXT_PRODUCT_DECISION_ENABLED`: the shared atomic-directory primitive can now replace remaining approved native directory artifact writers without accepting teul-private partial-publish authority.

## Review and nonclaims

- review bundle target: next coherent CLI/teul authority-and-required-dependency milestone
- writer-dispatched new reviewer/task/worktree: 0/0/0
- existing rolling reviewer handle is preserved and is not dispatched by this handoff.
- This handoff does not claim independent PASS, whole C0~C8 closure, teul-cli public retirement, P0~P6 closure, V1 membership/readiness, Windows/public release, activation, legal status, Owner Human Smoke, or Human PASS.
