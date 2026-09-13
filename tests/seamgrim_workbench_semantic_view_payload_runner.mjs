#!/usr/bin/env node

import { extractCanonicalViewAuthorityInputsFromState } from "../solutions/seamgrim_ui_mvp/ui/seamgrim_runtime_state.js";
import {
  buildCanonicalConsoleViewPayload,
  buildCanonicalSpace2dViewPayload,
  buildCanonicalViewPayloadSet,
  buildCanonicalWorkbenchViewPayload,
  buildCommittedSemanticViewPayload,
  orderedObservationsFromWasmState,
  stableSemanticJson,
} from "../solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const resultOnlyIdentity = buildCanonicalConsoleViewPayload({
  identity: { result_identity: "result:without-committed-state" },
  projection: {
    status: "available",
    entries: [{ tick: 0, line_no: 1, kind: "output", text: "must not publish" }],
  },
});
assert(
  resultOnlyIdentity.status === "unavailable" && resultOnlyIdentity.content === null,
  "result identity without committed state identity was accepted for projection",
);
const whitespaceStateIdentity = buildCanonicalConsoleViewPayload({
  identity: { state_hash: "  ", result_identity: "result:blank-state" },
  projection: {
    status: "available",
    entries: [{ tick: 0, line_no: 1, kind: "output", text: "must not publish" }],
  },
});
assert(
  whitespaceStateIdentity.status === "unavailable" && whitespaceStateIdentity.content === null,
  "blank state identity was accepted for projection",
);
const sourceLessSpace2dIdentity = buildCanonicalSpace2dViewPayload({
  identity: { state_hash: "blake3:committed-state" },
  projection: {
    status: "available",
    space2d: { drawlist: [{ kind: "circle", x: 1, y: 2, r: 0.5 }] },
  },
});
assert(
  sourceLessSpace2dIdentity.status !== "available" && sourceLessSpace2dIdentity.content === null,
  "source-less space2d entity received a derived identity",
);

function wasmState(tick, theta, omega, energy) {
  const length = 2;
  const bobX = length * Math.sin(theta);
  const bobY = -length * Math.cos(theta);
  return {
    tick_id: tick,
    state_hash: `blake3:state_${tick}`,
    channels: [
      { key: "theta", dtype: "num", role: "state" },
      { key: "omega", dtype: "num", role: "state" },
      { key: "energy", dtype: "num", role: "state" },
    ],
    row: [theta, omega, energy],
    view_meta: {
      workbench: {
        schema: "seamgrim.workbench.authoritative_result_set.v1_candidate",
        producer: "ddonirang_tool.wasm_runtime",
        provenance: "native_authoritative_structured_result",
        results: {
          pendulum: {
            schema: "seamgrim.workbench.pendulum_result.v1_candidate",
            family: "pendulum",
            status: "available",
            producer: "ddonirang_tool.wasm_runtime",
            provenance: "native_authoritative_structured_result",
            content: {
              current: {
                theta,
                omega,
                energy,
                kinetic_energy: null,
                potential_energy: null,
                length,
                physical_bob: { x: bobX, y: bobY },
                normalized_bob: { x: bobX / length, y: -bobY / length },
              },
            },
          },
        },
      },
    },
  };
}

const run = {
  run_id: "run_semantic",
  source_hash: "sha256:source",
  shared_runtime_result: {
    schema: "ddn.runtime.run_summary.v1_candidate",
    source_profile_identity: "v1-core-v25",
    source_identity: "sha256:source",
    state_hash: "blake3:state_1",
  },
  work_cost_receipt: { schema: "ddonirang.work_cost.v1-candidate" },
  frames: [
    {
      frame_id: 0,
      madi: 0,
      state_hash: "blake3:state_0",
      source_hash: "sha256:source",
      wasm_state: wasmState(0, 0.5, 0, 1.2),
    },
    {
      frame_id: 1,
      madi: 1,
      state_hash: "blake3:state_1",
      source_hash: "sha256:source",
      wasm_state: wasmState(1, 0.48, -0.1, 1.2),
    },
  ],
};

const project = { id: "pendulum", primaryView: "pendulum" };
const primaryConfig = { primary_view: "pendulum", role: "primary", mode: "ddn-main" };
const canonicalViewHistory = run.frames.map((frame) => {
  const inputs = extractCanonicalViewAuthorityInputsFromState(frame.wasm_state);
  inputs.identity = {
    ...inputs.identity,
    state_hash: frame.state_hash,
    source_hash: frame.source_hash,
    tick_id: frame.madi,
  };
  return {
    frame_id: frame.frame_id,
    madi: frame.madi,
    state_hash: frame.state_hash,
    canonical_views: buildCanonicalViewPayloadSet(inputs),
  };
});
const canonicalViewPayloads = canonicalViewHistory.at(-1).canonical_views;
const payloadArgs = {
  project,
  run,
  frame: run.frames[1],
  viewConfig: primaryConfig,
  canonicalViewPayloads,
  canonicalViewHistory,
};
const first = buildCommittedSemanticViewPayload(payloadArgs);
const repeated = buildCommittedSemanticViewPayload(payloadArgs);

assert(stableSemanticJson(first) === stableSemanticJson(repeated), "same frame and view config must produce byte-equivalent semantic payloads");
assert(first.semantic_payload_hash === repeated.semantic_payload_hash, "same frame and view config hash mismatch");
assert(first.committed_frame.run_id === "run_semantic", "committed run identity missing");
assert(first.committed_frame.frame_id === 1 && first.committed_frame.madi === 1, "committed frame identity mismatch");
assert(first.committed_frame.state_hash === "blake3:state_1", "committed state hash mismatch");
assert(first.execution_receipt.state_hash === first.committed_frame.state_hash, "shared execution receipt state binding mismatch");
assert(first.ordered_observations.map((row) => row.name).join(",") === "theta,omega,energy", "observation order changed");
assert(first.view_binding.resolved_channels.length === 0, "raw channel binding remained active");
assert(first.view_binding.resolution === "canonical_workbench_result", "pendulum canonical binding resolution mismatch");
assert(first.committed_trajectory.length === 2, "committed trajectory did not include both frames");

// BIC-WORKBENCH-02: a single explicit typed owner/binding is the only
// successful selection authority.  Runtime observations remain evidence, not
// a view-family selector, and the committed frame identity is unchanged.
const committedFrameBeforeSelection = stableSemanticJson(first.committed_frame);
const numericObservationOnly = buildCommittedSemanticViewPayload({
  project: { ...project, primaryView: "line" },
  run,
  frame: run.frames[1],
  viewConfig: {},
  canonicalViewPayloads: {},
  canonicalViewHistory,
});
assert(numericObservationOnly.ordered_observations.length === 3, "BIC-WORKBENCH-02 fixture lost numeric observations");
assert(numericObservationOnly.view_config.primary_view === "", "project/UI default selected a view without an explicit binding");
assert(numericObservationOnly.view_binding.view_family === "", "numeric observations selected a view family");
assert(numericObservationOnly.view_binding.resolution === "canonical_workbench_result_unavailable", "numeric-only selection did not fail closed");
assert(stableSemanticJson(numericObservationOnly.committed_frame) === committedFrameBeforeSelection, "view selection changed committed frame/state identity");

// BIC-UNSUPPORTED-01: even one typed candidate remains unresolved when the
// explicit requested family is absent or mismatched.
const unresolved = buildCommittedSemanticViewPayload({
  ...payloadArgs,
  viewConfig: { ...primaryConfig, primary_view: "line" },
});
assert(unresolved.view_binding.view_family === "line", "unresolved explicit family identity was not preserved for typed failure");
assert(unresolved.view_binding.canonical_payload_key === "workbench_line", "unresolved view failure lost its exact requested key");
assert(unresolved.view_binding.canonical_payload_status !== "available", "unresolved view retained an available projection");
assert(unresolved.view_binding.resolution === "canonical_workbench_result_unresolved", "unresolved view did not fail closed");
assert(stableSemanticJson(unresolved.committed_frame) === committedFrameBeforeSelection, "unresolved selection changed committed frame/state identity");

// BIC-MULTIVIEW-02: two exact typed candidates are ambiguous regardless of
// object/source order.  There is no first/last/default winner.
const availableLine = buildCanonicalWorkbenchViewPayload({
  identity: canonicalViewPayloads.workbench_pendulum.identity,
  family: "line",
  projection: {
    status: "available",
    result_set: {
      schema: "seamgrim.workbench.authoritative_result_set.v1_candidate",
      producer: "ddonirang_tool.wasm_runtime",
      provenance: "native_authoritative_structured_result",
      results: {
        line: {
          schema: "seamgrim.workbench.line_result.v1_candidate",
          family: "line",
          status: "available",
          producer: "ddonirang_tool.wasm_runtime",
          provenance: "native_authoritative_structured_result",
          content: { current: { x: 2, y: 5 }, equation: { a: 2, b: 1 } },
        },
      },
    },
  },
});
assert(availableLine.status === "available", "BIC-MULTIVIEW-02 second typed fixture was not canonical");
const multiviewA = buildCommittedSemanticViewPayload({
  ...payloadArgs,
  canonicalViewPayloads: {
    workbench_pendulum: canonicalViewPayloads.workbench_pendulum,
    workbench_line: availableLine,
  },
});
const multiviewB = buildCommittedSemanticViewPayload({
  ...payloadArgs,
  canonicalViewPayloads: {
    workbench_line: availableLine,
    workbench_pendulum: canonicalViewPayloads.workbench_pendulum,
  },
});
for (const ambiguous of [multiviewA, multiviewB]) {
  assert(ambiguous.view_binding.view_family === "", "ambiguous typed views selected a family");
  assert(ambiguous.view_binding.canonical_payload_key === "", "ambiguous typed views retained a projection key");
  assert(ambiguous.view_binding.resolution === "canonical_workbench_result_ambiguous", "multiple typed views did not fail closed");
  assert(stableSemanticJson(ambiguous.committed_frame) === committedFrameBeforeSelection, "ambiguous selection changed committed frame/state identity");
}
assert(stableSemanticJson(multiviewA.view_binding) === stableSemanticJson(multiviewB.view_binding), "candidate/source order became selection authority");

const overlay = buildCommittedSemanticViewPayload({
  project,
  run,
  frame: run.frames[1],
  viewConfig: { ...primaryConfig, role: "overlay" },
  canonicalViewPayloads,
  canonicalViewHistory,
});
assert(overlay.semantic_payload_hash !== first.semantic_payload_hash, "view config change did not change semantic payload hash");
assert(overlay.committed_frame.state_hash === first.committed_frame.state_hash, "view config changed runtime state hash");
assert(overlay.view_config.participates_in_state_hash === false, "view config must remain outside runtime state hash");

const observations = orderedObservationsFromWasmState(wasmState(2, 0.4, -0.2, 1.19));
assert(observations.every((row) => row.state_hash_participation === true), "runtime observations must be marked state-derived");

console.log("seamgrim_workbench_semantic_view_payload: ok");
