function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function toFiniteNumber(value, fallback = NaN) {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
}

function stableCanonicalJson(value) {
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableCanonicalJson(item)).join(",")}]`;
  }
  if (isObject(value)) {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableCanonicalJson(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function fnv1a32(text = "") {
  let hash = 0x811c9dc5;
  for (let index = 0; index < text.length; index += 1) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 0x01000193);
  }
  return (hash >>> 0).toString(16).padStart(8, "0");
}

function buildHashCandidate(value, label = "sealed_observation_trace") {
  return `candidate:fnv1a32:${label}:${fnv1a32(stableCanonicalJson(value))}`;
}

function readValue(values, key) {
  if (!isObject(values)) return NaN;
  return toFiniteNumber(values[key]);
}

function normalizeTraceSample(raw, index = 0) {
  const row = isObject(raw) ? raw : {};
  const values = isObject(row.values) ? row.values : row;
  const tick = toFiniteNumber(values.tick_id ?? row.tick_id ?? row.index ?? index);
  const sample = {
    tick_id: Math.max(0, Math.trunc(Number.isFinite(tick) ? tick : index)),
    t: readValue(values, "t"),
    theta: readValue(values, "theta"),
    omega: readValue(values, "omega"),
  };
  return sample;
}

function normalizeCurrentObservationSample(observation, fallbackTick = 0) {
  const values = isObject(observation?.all_values)
    ? observation.all_values
    : isObject(observation?.values)
      ? observation.values
      : {};
  return normalizeTraceSample({
    index: fallbackTick,
    tick_id: fallbackTick,
    values,
  }, fallbackTick);
}

function isSameTraceSample(left, right) {
  if (!isObject(left) || !isObject(right)) return false;
  for (const key of ["t", "theta", "omega"]) {
    if (!Number.isFinite(Number(left[key])) || !Number.isFinite(Number(right[key]))) return false;
    if (Math.abs(Number(left[key]) - Number(right[key])) > 1e-12) return false;
  }
  return true;
}

export function buildSealedObservationTraceArtifact({
  lessonId = "",
  timelineSamples = [],
  currentObservation = null,
  source = "seamgrim_wasm_dotbogi_timeline",
  requiredValues = ["tick_id", "t", "theta", "omega"],
  rules = null,
} = {}) {
  const rows = [];
  const sourceRows = Array.isArray(timelineSamples) ? timelineSamples : [];
  sourceRows.forEach((sample, index) => {
    rows.push(normalizeTraceSample(sample, index));
  });
  if (currentObservation) {
    const current = normalizeCurrentObservationSample(currentObservation, rows.length);
    const sameSampleIndex = rows.findIndex((row) => isSameTraceSample(row, current));
    const existingIndex = sameSampleIndex >= 0
      ? sameSampleIndex
      : rows.findIndex((row) => row.tick_id === current.tick_id);
    if (existingIndex >= 0) {
      rows[existingIndex] = { ...current, tick_id: rows[existingIndex].tick_id };
    } else {
      rows.push(current);
    }
  }
  const samples = rows
    .filter((row) => (
      Number.isFinite(row.tick_id)
      && Number.isFinite(row.t)
      && Number.isFinite(row.theta)
      && Number.isFinite(row.omega)
    ))
    .sort((left, right) => left.tick_id - right.tick_id)
    .map((row, index) => ({
      sample_index: index,
      tick_id: row.tick_id,
      t: row.t,
      theta: row.theta,
      omega: row.omega,
    }));
  const traceCore = {
    lesson_id: String(lessonId ?? "").trim(),
    source: String(source ?? "").trim() || "seamgrim_wasm_dotbogi_timeline",
    required_values: requiredValues,
    sample_count: samples.length,
    samples,
    rules: isObject(rules) ? rules : null,
  };
  return {
    schema: "seamgrim.sealed_observation_trace.v1",
    sealed: true,
    state_hash_participation: false,
    runtime_semantics_claim: false,
    provenance: {
      source: traceCore.source,
      lesson_id: traceCore.lesson_id,
      frontdoor: "seamgrim_product_wasm",
      timeline_owner: "dotbogi",
      console_string_parse: false,
    },
    ...traceCore,
    trace_hash_candidate: buildHashCandidate(traceCore, "sealed_observation_trace"),
  };
}

export const __test__ = {
  stableCanonicalJson,
  buildHashCandidate,
};
