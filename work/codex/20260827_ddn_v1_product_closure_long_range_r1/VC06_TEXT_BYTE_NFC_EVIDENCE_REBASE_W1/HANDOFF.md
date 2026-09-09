# VC06 Supported Canon / String Escape W1 — Consolidated Handoff

## Fixed identity

- baseline: `7921a4d7832f1e89b2380b9729b2072e4651d3cc`
- product/test fixed HEAD: `429c8dec3b1a8022005552f2eb1de050991c8e0e`
- fixed tree: `13d6eda851828cc70292f81cb228d1342345a30b`
- direct parent: baseline exactly
- merge count: `0`
- changed paths: exact 24 paths, all inside the issued product/WASM/evidence lease

## User workflow and implementation

The supported `v1-core-v25` ingress previously executed valid V25 source while the
official shared canon rejected the same source. The fixed vertical now:

1. resolves the explicit profile through `resolve_supported_source_profile`;
2. canonicalizes with `DdnProgram::from_supported_source_profile_with_mode`;
3. leaves `canonicalize_shared_source` and `wasm_canon_ddn` unchanged for legacy callers;
4. exposes the internal-candidate `wasm_canon_ddn_with_source_profile` consumer;
5. emits lexer-supported escapes for quote, backslash, LF, CR and tab without NFC-normalizing raw text.

No second parser, heuristic epoch detection, hidden PreV25 retry, global default
switch, public command decision, or model-path change was added.

## RED to GREEN

- accepted RED: `VC06_CLOSURE_RED red=3 product_gap=4`
- shared-canon rejection signature for T01~T03:
  `70ffe7650a4558bc92cd3d5f7522806fa9c92e49395824a58e9b10a1223fa72c`
- clean fixed-HEAD reproduction: `GREEN=7 / RED=0 / PRODUCT_GAP=4`
- T01/T02/T03: supported execution accepted, first/second canon accepted,
  canon identity equal, runtime canonical reparse accepted
- native/tracked-WASM full structured run payload equality: `11/11`
- deterministic repeats: `3`

## Regression and artifact identity

- `ddonirang-lang --lib`: `364/364 PASS`
- `ddonirang-tool --lib`: `524/524 PASS`
- WASM-feature supported-profile wrapper: `1/1 PASS`
- targeted string roundtrip: `1/1 PASS`
- targeted supported-profile canon: `1/1 PASS`
- official tracked-WASM freshness: `PASS`
- existing local-project CRLF unit: `PASS`
- `git diff --check`: `PASS`
- tracked WASM: `5,555,817 bytes` /
  `002dd40d743c6cb7d5a7d5073755de3d4f2b61967ab5c9a313906e91c3bcfae4`
- WASM manifest: `19,550 bytes` /
  `343d66ab1f626511277a79ae78fa0ae04cf6c713926eb2fcbb9ff03664b12df7`
- JS binding: `90,516 bytes` /
  `fdaede9f8b17f19c6a5719c06494afc677c2368bb79675a69cd3dc479adf96ee`
- Python runner: `12,613 bytes` /
  `cb09b83983cd4d798ada2209c725180230ef11f360462c5e4811962414ed8aef`
- WASM runner: `6,523 bytes` /
  `872954f8842980b4132a45da9d563a151127b7b0f9108fe14d036b028acfc351`

The refreshed WASM family is an internal candidate bound to this fixed source.
It is not a final tracked-WASM promotion, public API membership, or release artifact.

## Remaining gaps and nonclaims

- ordinary identifier NFC resolution/original-span custody: `PRODUCT_GAP`
- byte literal and explicit UTF-8 conversion surface: `PRODUCT_GAP`
- BOM-as-data ingress: `PRODUCT_GAP`
- invalid UTF-8 before the product String API: `PRODUCT_GAP`
- local-project raw-byte/InputSnapshot receipt surface: `PRODUCT_GAP`
- model string NFC: `OPEN / out of scope`
- stable public diagnostic spelling: `OPEN`

VC06 closure, P1/P1-A/V1 membership or readiness, stable public WASM API,
release, activation, legal status, and Human PASS are not claimed.

## Anti-meta and review consolidation

- `USER_WORKFLOW_CHANGED_OR_UNBLOCKED`: supported V25 parse -> canon -> parse
  and native/WASM profile-aware canon are now executable at one fixed head.
- `NEW_TEST_ARTIFACT_COUNT`: `2` runners plus one coherent pack, created before
  the stop rule and reused for the actual product vertical.
- `EXISTING_TEST_REUSED_COUNT`: `4` (lang lib, tool lib, freshness, CRLF unit).
- `META_TEST_CREATED`: `0`.
- receipt/hash-tamper suite: `0`; the pre-stop stale expected receipt was removed.
- `STOP_RULE_APPLIED`: yes.
- `NEXT_PRODUCT_DECISION_ENABLED`: management may bundle this fixed product
  vertical into the next coherent rolling-review milestone.
- `ACTIVE_REVIEW_TASK_COUNT`: `0` for this slice.
- `NEW_REVIEW_TASK_COUNT`: `0`.
- `NEW_REVIEW_WORKTREE_COUNT`: `0`.
- `REVIEW_BUNDLE_TARGET`: management-selected next coherent P1 product milestone.
- historical P0/P1A/VC11/VC09 review tasks are preserved without wake/duplication.
- `REVIEW_NEEDED_NOW`: yes for product-risk coverage (shared canon authority and
  a new internal-candidate WASM export), but dispatch is management-gated and was not performed.

## Protected custody

- protected server/port/browser/process start, stop, restart or kill commands: `0`
- current observed TCP 8787 listener: `0`
- current observed Node PIDs were read-only inventoried; no start baseline is claimed
- product worktree outside the exact lease, shared dirty root, SSOT and public SPEC were not modified

Status: `VC06_SUPPORTED_CANON_STRING_ESCAPE_IMPLEMENTED_UNDER_REVIEW_BUNDLE_PENDING`.
