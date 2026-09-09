# DDN-LONG-RELINT-PRODUCT-01 G8~G13 integration result

## authority and lineage

```text
GOAL: DDN_LONG_RELINT_PRODUCT_01
RESUME_BASELINE: a930f0c227cf73c640a49c09a634398c9bedbd85
PC02_INVERSE_COMMIT: 0dd73ab9
REVIEWED_T5_W1_COMPOSITION: 26891ccd
W1_PREREQUISITE_BINDING: 235a4aa8
W1_RUNTIME_AND_OFFICIAL_WASM_BINDING: f80c69b8
PUBLIC_SPEC_V0_5_0_EXACT_BINDING: a2e23fd4
MERGE_COMMIT_COUNT_FROM_RESUME_BASELINE: 0
```

The exact patch of PC02 commit `04566a2426b56084f4449b363530192aa1166d2a`
was inverted in a linear successor. PC01 is not promoted into release membership by
this result. The reviewed T5 and W1 scopes are composed with their stated prerequisite
boundaries; standalone T5, R10, PC01, and release claims remain open where recorded.

## W1 product convergence

The teul CLI run owner is the exact blob from merge tree
`15ebb606ca0f4d9ea76ca971f7528b679893caa5`. Native canon uses the shared Rust
canonicalizer; the W1B harness distinguishes the canonical body from the native
terminal-LF presentation without duplicating semantic expectations.

Verified:

- W1B native/source-WASM/tracked-WASM parity: PASS.
- W1C1 public cases: PASS, 10 cases, public provider surface still OPEN.
- W1C2 I1 internal typed suite: PASS, 23/23 in an isolated Cargo target.
- W1C2 I2 focused suite: PASS, 15/15.
- W1DF capacity evidence: PASS, 1/1.
- The earlier duplicate-crate compile failure disappears in an isolated target and is
  classified as shared Cargo target cross-worktree artifact contamination.
- teul full test compilation remains blocked by the pre-existing private compile-time
  `docs/ssot/pack/edu_phys_p001_05_projectile_xy/lesson.ddn` dependency. No SSOT
  substitute or hidden fallback was added.

## combined-source official WASM custody

Offline official web A/B builds were produced from `235a4aa8...` in separate clean
worktrees. The subsequent CLI and harness corrections are outside the WASM source
inventory, and the tracked freshness checker remains PASS.

```text
A_DIR: I:/home/urihanl/ddn/codex/build/relint-wasm-custody-235a4aa8/A
B_DIR: I:/home/urihanl/ddn/codex/build/relint-wasm-custody-235a4aa8/B
A_B_FILE_PARITY: 4/4
WASM_BYTES: 5541127
WASM_SHA256: 14deea06dd4f6d1ea72ff1460e68f938c636fb3cd697afabed5296ef95a490b6
JS_SHA256: 16b4de4cac8bfebbc7d7f881ab1241b0d22d652ff8ad00b9045f40c81d7c90a9
TRACKED_MANIFEST_SHA256: 0c66ca8053f471f1478d848675ca313758133c8dae983a7a31a8fe25458a0e1d
FRESHNESS_CHECK: PASS
```

## T5 regression boundary after exact PC02 exclusion

The T5B console/graph, T5C space2d, T5D table/text/structure, T5E
console-grid/grid2d, T5G scene/curriculum, T5H status-totality, and T5I native
readiness audits pass on the integrated tree. T5I still reports 14/14 serializable,
deterministic, and renderer-independent families.

The T5F four-family runtime runner does not pass with the exact PC02 inverse:
`grid: Rust result-set schema missing`. The reviewed T5 successor had PC02 as an
ancestor, and PC02 changed that runner from the constructor to explicit
`fromPreV25Source`. The Owner ordered the complete exact inverse of PC02 and separately
ordered standalone T5 claims to remain open. The excluded compatibility ingress was not
silently restored. This result therefore preserves the failure as a prerequisite gap;
it is not a T5 standalone re-closure claim.

## public Language SPEC custody

Exactly the 18 files below `publish/spec/v0.5.0/**` were bound from sealed commit
`6974eda43a5256dd5fea2803761a3503068f6fc0`. All 18 working-tree blob OIDs match that
commit (`MISMATCH=0`). No v0.5.0 content was edited. In accordance with the exact
18-file-only boundary, `publish/spec/CURRENT.md` was not changed as a nineteenth file;
release-facade pointer activation remains outside this binding.

## PC01 custody and next gate

The current composition still carries PC01 dependency bytes. Before release membership,
a fresh fixed-HEAD independent review is required. Local pre-review evidence at this
composition is:

```text
RUST_PACK: PASS 3/3
MUTATION: baseline GREEN; M1 RED; M2 RED; M3 RED; restored GREEN
MUTATION_RESIDUE: 0
PC01_RELEASE_MEMBERSHIP: PENDING_FRESH_TARGETED_PLAIN_PASS
PC01_PUBLIC_FIVE_FILE_COPY: 0
```

PC01 pack rights and projectile lesson rights are still Owner-confirmation gates. No
rights-sensitive public copy was made.

## D7 public-specific aggregate candidate

`tests/run_ddn_public_specific_conformance_check.py` binds the exact 11 leaf roots from
the bounded closure audit. It explicitly preserves three parity members and three
durability members while excluding only the two internal umbrella gates. PC01 and the
new projectile public copy remain pending rather than being silently included.

```text
MEMBERSHIP_CHECK: PASS / exact leaf roots 11 / unique 11
PARITY_MEMBERS: 3
DURABILITY_MEMBERS: 3
INTERNAL_UMBRELLAS_EXCLUDED: 2
FULL_EXECUTION: FAIL_CLOSED_AT_FIRST_ROOT
FULL_EXECUTION_REASON: local playwright Node package absent; network install forbidden
PUBLIC_AGGREGATE_ACTIVATED: NO
```

The missing local package is an execution-environment gap, not a substituted PASS. The
aggregate remains candidate until it is reproduced in a sealed public-source environment
with its declared offline dependencies.

Direct execution of the three parity members produced `freshness=PASS`,
`view-only-state-hash=PASS`, and `true-parity-equality=RED`. The true-parity root rejects
legacy view cases c09/c11/c13 with `E_BOIM_LEGACY_REMOVED` after the exact PC02 inverse.
This semantic prerequisite conflict is sealed in
`PUBLIC_PARITY_PREREQUISITE_CONFLICT_PACKET.md`; no oracle or product gate was weakened.

## protected state

```text
DOCS_SSOT_DIFF: 0
OFFICIAL_DB_BYTES: 573440
OFFICIAL_DB_SHA256: 3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0
PID_53196: ABSENT
127.0.0.1:8787: NOT_LISTENING
OFFICIAL_WRITE: 0
ACTIVATION_CALL: 0
NETWORK_DOWNLOAD: 0
```

## honest state

```text
G8_G13_ISOLATED_INTEGRATION_IMPLEMENTED
COMBINED_SOURCE_OFFICIAL_WASM_A_B_BYTE_IDENTICAL
PUBLIC_SPEC_V0_5_0_EXACT_18_FILE_BYTES_BOUND
PC01_FRESH_TARGETED_INDEPENDENT_REVIEW_REQUIRED
PC01_PACK_RIGHTS_CONFIRMATION_REQUIRED
PROJECTILE_LESSON_RIGHTS_CONFIRMATION_REQUIRED
T5_STANDALONE_CLAIM_OPEN_AFTER_EXACT_PC02_EXCLUSION
PUBLIC_RELEASE_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```
