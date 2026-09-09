import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

const positives = [
  ["P01", "G01", "COMPLETE_BEFORE_START(문잠금,출발)"],
  ["P02", "G01", "DURING(걷기,살피기) owns cleanup/join"],
  ["P03", "G01", "UNTIL chooses minimum trigger/completion boundary"],
  ["P04", "G01", "after/every/inclusive logical deadline"],
  ["P05", "G01", "composite success commits before successor start"],
  ["P06", "G02", "FIRST_SUCCESS preserves full minimum success cohort"],
  ["P07", "G02", "retry uses same Work and distinct Attempt identities"],
  ["P08", "G03", "structured cancel reaches terminal cleanup/join"],
  ["P09", "G03", "passive async sender-filter selects one EndpointRoute"],
  ["P10", "G03", "one consuming route then two distinct internal providers"],
  ["P11", "G03", "bounded-full async send WAITs then resumes FIFO"],
  ["P12", "G04", "deferred expansion preflights all children before start"],
  ["P13", "G05", "coherent settle lets dependent observe new A and B once"],
  ["P14", "G05", "explicit Capability close owns lifecycle receipt"],
  ["P15", "G06", "committed effect release failure keeps world committed"],
  ["P16", "G06", "external sensor wait remains open until authored boundary"],
  ["P17", "G07", "zero-config and named preset expand to same contract"],
];

// Four redundant negative descriptions from the audit are represented by their
// stronger cross-composition fixtures: N07->X09, N14->X24, N15->X25,
// N21->the worker-permutation matrix on every row. This keeps 65 unique cases.
const negatives = [
  ["N01", "G01", "zero logical duration", "E_LOGICAL_DURATION_INVALID_CANDIDATE"],
  ["N02", "G01", "source-token reversal changes BEFORE relation", "E_RELATION_NORMALIZATION_CANDIDATE"],
  ["N03", "G01", "DURING child detached before parent completion", "E_STRUCTURED_LIFETIME_CANDIDATE"],
  ["N04", "G01", "same-boundary completion overwritten by cancel", "E_TERMINAL_MONOTONICITY_CANDIDATE"],
  ["N05", "G01", "physical callback chosen as race winner", "E_DETERMINISM_CANDIDATE"],
  ["N06", "G02", "same-tag cohort truncated to one member", "E_COHORT_TRUNCATION_CANDIDATE"],
  ["N08", "G02", "retry attempts share identity or RNG stream", "E_ATTEMPT_IDENTITY_CANDIDATE"],
  ["N09", "G03", "cancel implemented as kill or PAUSE alias", "E_CLEANUP_JOIN_CANDIDATE"],
  ["N10", "G03", "ambiguous receive chooses declaration-order first", "E_ASYNC_ENDPOINT_AMBIGUOUS_CANDIDATE"],
  ["N11", "G03", "bounded-full async silently drops", "E_ASYNC_CAPACITY_POLICY_CANDIDATE"],
  ["N19", "G03", "external wait misclassified as closed deadlock", "E_WAIT_CLASSIFICATION_CANDIDATE"],
  ["N12", "G04", "deferred child starts before admission preflight", "E_ADMISSION_ATOMICITY_CANDIDATE"],
  ["N13", "G05", "host RAM or GC timing enters semantic identity", "E_SEMANTIC_PHYSICAL_SEPARATION_CANDIDATE"],
  ["N16", "G05", "GC finalizer performs semantic effect", "E_RECLAMATION_PURITY_CANDIDATE"],
  ["N17", "G06", "external release occurs before internal commit", "E_EFFECT_STAGING_CANDIDATE"],
  ["N18", "G06", "release failure rewinds committed world", "E_PHASE_MONOTONICITY_CANDIDATE"],
  ["N20", "G07", "receipt seals preset label without expanded contract", "E_EXPANDED_CONTRACT_SEAL_CANDIDATE"],
];

const crosses = [
  ["X01", "G01", "DURING child failure cancels counterpart; group patch/outbox zero"],
  ["X02", "G01", "DURING rendezvous preserves only completed handoff boundary"],
  ["X03", "G01", "UNTIL external wait remains open before trigger"],
  ["X04", "G01", "same-boundary UNTIL completion preserves result and trigger"],
  ["X05", "G01", "deadline accepts completion inside target closure"],
  ["X06", "G01", "deadline rejects completion after target publish"],
  ["X07", "G02", "race failure preserves full minimum terminal cohort"],
  ["X08", "G02", "simultaneous first successes are all preserved"],
  ["X09", "G02", "quorum overshoot preserves full same-tag cohort"],
  ["X10", "G02", "retry RNG identity includes attempt ordinal"],
  ["X11", "G02", "retry Capability receipts are attempt-scoped"],
  ["X12", "G02", "failed-attempt external intent is not rereleased"],
  ["X13", "G02", "retry checks remaining logical deadline before admission"],
  ["X31", "G02", "partial failure cannot retain unowned committed members"],
  ["X14", "G03", "cancel before commit discards staged async outbox"],
  ["X15", "G03", "cancel does not erase completed rendezvous occurrence"],
  ["X16", "G03", "cancel discards unreleased effect intent"],
  ["X17", "G03", "Capability transfer receipt fixes cancel ownership"],
  ["X18", "G03", "closed bounded-WAIT cycle is deterministic deadlock"],
  ["X19", "G03", "waiting send remains owned until cleanup/join"],
  ["X20", "G03", "sender predicates apply before ambiguity cardinality"],
  ["X21", "G04", "huge deferred expansion admission failure starts zero children"],
  ["X22", "G05", "dependency settle emits no direct-reentry event"],
  ["X23", "G05", "dependency patch candidates merge before atomic publish"],
  ["X24", "G05", "dependency change and message envelope identities stay distinct"],
  ["X25", "G05", "zero-delay dependency cycle fails with prior world preserved"],
  ["X26", "G05", "GC creates no Capability ownership transition"],
  ["X27", "G05", "only explicit lifecycle releases external resource"],
  ["X28", "G06", "release failure after publish keeps committed world"],
  ["X29", "G06", "sealed receipt replay performs zero provider calls"],
  ["X30", "G06", "external wait remains open through logical deadline boundary"],
];

const evidenceFixedHead = "d8a4b2ab5b7c5fe68b1738f955d2d3d5b2b86ad1";

// The logical fixture is not product execution evidence. These seven entries
// bind separately reviewed product evidence without relabelling the logical
// description digest as a runtime result.
const productEvidence = new Map([
  ["P09", {
    evidence_class: "PUBLIC_SOURCE_PRODUCT_CASE",
    evidence_frontdoor: "W1C1_OFFICIAL_NATIVE_SOURCE_WASM_TRACKED_WASM_RUNNER",
    evidence_test_ids: [
      "w1c1:01_exact_sender_success",
      "w1c1:02_sender_mismatch_unhandled",
    ],
    evidence_scope: "sender-filter selects exactly one typed EndpointRoute; mismatch is unhandled",
  }],
  ["P10", {
    evidence_class: "PUBLIC_SOURCE_PRODUCT_CASE",
    evidence_frontdoor: "W1C1_OFFICIAL_RUNNER_PLUS_SHARED_RUST_PROVIDER_AUTHORITY",
    evidence_test_ids: [
      "w1c1:00_any_sender_builtin_success",
      "cargo:ddonirang-lang:delivery_occurrence_gates_provider_resolution_and_fans_out_distinct_keys",
    ],
    evidence_scope: "public route crosses route-first occurrence authority; distinct internal providers fan out in shared Rust",
  }],
  ["N10", {
    evidence_class: "PUBLIC_SOURCE_PRODUCT_CASE",
    evidence_frontdoor: "W1C1_OFFICIAL_NATIVE_SOURCE_WASM_TRACKED_WASM_RUNNER",
    evidence_test_ids: ["w1c1:07_duplicate_route_ambiguity"],
    evidence_scope: "duplicate matching routes fail as ambiguity instead of choosing declaration order",
  }],
  ["X20", {
    evidence_class: "PUBLIC_SOURCE_PRODUCT_CASE",
    evidence_frontdoor: "W1C1_OFFICIAL_NATIVE_SOURCE_WASM_TRACKED_WASM_RUNNER",
    evidence_test_ids: ["w1c1:03_sender_type_matrix_success"],
    evidence_scope: "sender and payload predicates filter candidates before route cardinality",
  }],
  ["P11", {
    evidence_class: "INTERNAL_TYPED_PRODUCT_CASE",
    evidence_frontdoor: "RUST_IN_PROCESS_TYPED_RUNTIME_TESTS",
    evidence_test_ids: [
      "cargo:ddonirang-tool:successor_async_bounded_full_wait_resumes_fifo_without_drop",
      "cargo:ddonirang-tool-integration:successor_async_capacity_two_multiple_waiters_resume_fifo_without_drop",
      "cargo:teul-cli:successor_async_bounded_full_wait_resumes_fifo_without_drop",
      "cargo:teul-cli:successor_async_capacity_two_multiple_waiters_resume_fifo_with_receipts",
    ],
    evidence_scope: "internal capacity hook reaches bounded WAIT and FIFO resume; no public capacity override",
  }],
  ["N11", {
    evidence_class: "INTERNAL_TYPED_PRODUCT_CASE",
    evidence_frontdoor: "RUST_IN_PROCESS_TYPED_RUNTIME_TESTS",
    evidence_test_ids: [
      "cargo:ddonirang-tool:successor_async_bounded_full_wait_resumes_fifo_without_drop",
      "cargo:ddonirang-tool-integration:successor_async_capacity_two_multiple_waiters_resume_fifo_without_drop",
      "cargo:teul-cli:successor_async_bounded_full_wait_resumes_fifo_without_drop",
      "cargo:teul-cli:successor_async_capacity_two_multiple_waiters_resume_fifo_with_receipts",
    ],
    evidence_scope: "internal bounded-full path preserves every envelope and records WAIT/RESUME",
  }],
  ["X14", {
    evidence_class: "INTERNAL_TYPED_PRODUCT_CASE",
    evidence_frontdoor: "RUST_IN_PROCESS_TYPED_RUNTIME_TESTS",
    evidence_test_ids: [
      "cargo:ddonirang-lang:staged_outbox_commits_nested_fifo_and_aborts_without_leak",
      "cargo:teul-cli:successor_async_handler_failure_rolls_back_state_and_staged_outbox",
    ],
    evidence_scope: "failed or cancelled delivery discards staged async outbox without state or trace leak",
  }],
]);

function digest(caseId, expectation) {
  return `sha256:${crypto.createHash("sha256").update(`fga2-w1df\0${caseId}\0${expectation}`, "utf8").digest("hex")}`;
}

function row(caseId, group, kind, expectation, diagnostic = "NONE") {
  const semanticDigest = digest(caseId, expectation);
  const evidence = productEvidence.get(caseId);
  const waits = /WAIT|wait|deadline|rendezvous|cleanup\/join/u.test(expectation);
  const aborts = kind === "negative" || /failure|fails|rejects|discards|deadlock/u.test(expectation);
  return {
    case_id: `FGA2-${caseId}`,
    group: `FGA2-${group}`,
    owner_delta_id: `FG-${caseId}`,
    predecessor_case_links: [],
    migration_evidence_links: caseId === "P09" ? ["SC-03", "SC-04", "SC-05"] : [],
    source_status: evidence ? "CURRENT_PRODUCT_EVIDENCE_LINKED" : "LOGICAL_CANDIDATE",
    logical_oracle_class: "LOGICAL_ORACLE_ONLY",
    normalized_relation_graph: expectation,
    expanded_execution_contract: "FGA2_OWNER_CLOSED_DELTA_R2_INTERNAL_CANDIDATE",
    logical_boundary_trace: ["admit", "start", "settle", aborts ? "terminal:abort" : "terminal:complete", "cleanup_join", "publish"],
    canonical_cohorts: [],
    identity_receipts: { stable_semantic_identity: semanticDigest, excludes_physical_order: true },
    wait_graph_and_openness: waits ? "SEALED_WAIT_GRAPH_REQUIRED" : "NO_WAIT_EDGE",
    resource_unit_ledger: { counting: "LOGICAL_UNITS_ONLY", host_bytes_semantic: false },
    patch_outbox_effect_candidates: { staged: /outbox|effect|release|publish/u.test(expectation), partial_commit_forbidden: true },
    expected_commit_abort_cancel: aborts ? "ABORT_OR_FAIL_CLOSED" : "COMMIT",
    expected_semantic_digests: { workers_1: semanticDigest, workers_2: semanticDigest, workers_8: semanticDigest },
    worker_permutations: [1, 2, 8],
    same_tag_permutations: ["forward", "reverse", "shuffled"],
    replay_external_call_count: /sealed receipt replay/u.test(expectation) ? 0 : "NOT_APPLICABLE_OR_AUTHORED",
    expected_diagnostic_family: diagnostic,
    evidence_class: evidence?.evidence_class ?? "PRODUCT_UNSUPPORTED",
    evidence_frontdoor: evidence?.evidence_frontdoor ?? "NONE",
    evidence_test_ids: evidence?.evidence_test_ids ?? [],
    evidence_fixed_head: evidence ? evidenceFixedHead : "NONE",
    evidence_scope: evidence?.evidence_scope ?? "NO_CURRENT_PRODUCT_EVIDENCE",
    stable_public_wire: "OPEN",
  };
}

const rows = [
  ...positives.map(([id, group, expectation]) => row(id, group, "positive", expectation)),
  ...negatives.map(([id, group, expectation, diagnostic]) => row(id, group, "negative", expectation, diagnostic)),
  ...crosses.map(([id, group, expectation]) => row(id, group, "cross", expectation)),
].sort((a, b) => a.group.localeCompare(b.group) || a.case_id.localeCompare(b.case_id, "en", { numeric: true }));

if (rows.length !== 65 || new Set(rows.map((item) => item.case_id)).size !== 65) {
  throw new Error(`oracle cardinality mismatch: ${rows.length}`);
}

fs.writeFileSync(path.join(here, "logical_oracle.jsonl"), `${rows.map((item) => JSON.stringify(item)).join("\n")}\n`, "utf8");
console.log(`w1df oracle generated: ${rows.length}`);
