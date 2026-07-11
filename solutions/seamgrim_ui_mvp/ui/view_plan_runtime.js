const EPSILON = 1e-9;

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

export function buildViewHashCandidate(value, label = "view") {
  return `candidate:fnv1a32:${label}:${fnv1a32(stableCanonicalJson(value))}`;
}

function readObservationValue(observation, key) {
  const normalizedKey = String(key ?? "").trim();
  if (!normalizedKey) return NaN;
  const directCandidates = [
    observation?.all_values?.[normalizedKey],
    observation?.values?.[normalizedKey],
    observation?.row?.[normalizedKey],
    observation?.channels?.[normalizedKey]?.value,
  ];
  for (const candidate of directCandidates) {
    const number = toFiniteNumber(candidate);
    if (Number.isFinite(number)) return number;
  }
  return NaN;
}

function resolveAnchorValue(anchor, observation) {
  const sourceRef = anchor?.source_ref;
  if (!isObject(sourceRef)) return { ok: false, value: null };
  const kind = String(sourceRef.kind ?? "").trim();
  if (kind === "observation") {
    const value = readObservationValue(observation, sourceRef.key);
    return { ok: Number.isFinite(value), value };
  }
  if (kind === "constant") {
    return { ok: true, value: sourceRef.value ?? null };
  }
  if (kind === "point2") {
    const x = readObservationValue(observation, sourceRef.x_key);
    const y = readObservationValue(observation, sourceRef.y_key);
    return { ok: Number.isFinite(x) && Number.isFinite(y), value: { x, y } };
  }
  return { ok: false, value: null };
}

function resolveSemanticBindings(viewPlan, observation) {
  const anchors = Array.isArray(viewPlan?.anchors) ? viewPlan.anchors : [];
  const byId = new Map();
  const diagnostics = [];
  for (const anchor of anchors) {
    const anchorId = String(anchor?.anchor_id ?? "").trim();
    if (!anchorId) continue;
    const resolved = resolveAnchorValue(anchor, observation);
    const row = {
      anchor_id: anchorId,
      label: String(anchor?.label ?? anchorId).trim() || anchorId,
      unit: String(anchor?.unit ?? "").trim(),
      value_type: String(anchor?.value_type ?? "").trim(),
      source_ref: anchor?.source_ref ?? null,
      provenance: anchor?.provenance ?? null,
      ok: Boolean(resolved.ok),
      value: resolved.value,
    };
    byId.set(anchorId, row);
    if (!resolved.ok) {
      diagnostics.push({
        code: "W_VIEW_PLAN_ANCHOR_UNRESOLVED",
        severity: "warning",
        message: `${anchorId} 관찰값을 아직 찾지 못했습니다.`,
        anchor_id: anchorId,
      });
    }
  }
  return { anchors: byId, diagnostics };
}

function readPoint(binding) {
  const value = binding?.value;
  if (!isObject(value)) return null;
  const x = toFiniteNumber(value.x);
  const y = toFiniteNumber(value.y);
  return Number.isFinite(x) && Number.isFinite(y) ? { x, y } : null;
}

function vectorLength(x, y) {
  return Math.hypot(Number(x) || 0, Number(y) || 0);
}

function unitVectorFromPoints(from, to, fallback = { x: 0, y: -1 }) {
  const dx = (to?.x ?? 0) - (from?.x ?? 0);
  const dy = (to?.y ?? 0) - (from?.y ?? 0);
  const length = vectorLength(dx, dy);
  if (length <= EPSILON) return fallback;
  return { x: dx / length, y: dy / length };
}

function normalizeAngleSweep(theta) {
  const value = toFiniteNumber(theta, 0);
  return Math.max(-Math.PI * 1.5, Math.min(Math.PI * 1.5, value));
}

function buildArcPolyline({ pivot, radius, theta, id, stroke }) {
  const sweep = normalizeAngleSweep(theta);
  const steps = Math.max(6, Math.min(48, Math.ceil(Math.abs(sweep) / (Math.PI / 32))));
  const points = [];
  const baseAngle = -Math.PI / 2;
  for (let index = 0; index <= steps; index += 1) {
    const ratio = steps === 0 ? 0 : index / steps;
    const angle = baseAngle + sweep * ratio;
    points.push({
      x: pivot.x + Math.cos(angle) * radius,
      y: pivot.y + Math.sin(angle) * radius,
    });
  }
  return {
    id,
    kind: "polyline",
    role: "angle_measure_arc",
    group_id: "measure.angle.theta",
    points,
    stroke,
    width: 2,
  };
}

function formatAngleLabel(theta) {
  const value = toFiniteNumber(theta, 0);
  return `θ ${value.toFixed(3)} rad`;
}

function buildAngleMeasureShapes({ viewPlan, bindings, diagnostics }) {
  const measures = Array.isArray(viewPlan?.measures) ? viewPlan.measures : [];
  const measure = measures.find((item) => String(item?.kind ?? "").trim() === "angle") ?? null;
  if (!measure) return { shapes: [], meta: null };
  const pivot = readPoint(bindings.get(String(measure.pivot_anchor ?? "").trim()));
  const bob = readPoint(bindings.get(String(measure.end_anchor ?? "").trim()));
  const thetaBinding = bindings.get(String(measure.value_anchor ?? "").trim());
  const theta = toFiniteNumber(thetaBinding?.value, NaN);
  if (!pivot || !bob || !Number.isFinite(theta)) return { shapes: [], meta: null };

  const expectedUnit = String(measure.unit ?? "").trim();
  const actualUnit = String(thetaBinding?.unit ?? "").trim();
  if (expectedUnit && actualUnit && expectedUnit !== actualUnit) {
    diagnostics.push({
      code: String(measure?.diagnostics?.unit_mismatch ?? "E_VIEW_PLAN_UNIT_MISMATCH"),
      severity: "error",
      message: `각도재기 단위가 맞지 않습니다: ${actualUnit} 값을 ${expectedUnit} 눈금에 연결했습니다.`,
      measure_id: String(measure.measure_id ?? ""),
    });
  }

  const style = isObject(measure.style) ? measure.style : {};
  const ref = measure.reference_direction ?? { x: 0, y: -1 };
  const refUnit = unitVectorFromPoints({ x: 0, y: 0 }, { x: ref.x, y: ref.y }, { x: 0, y: -1 });
  const bobUnit = unitVectorFromPoints(pivot, bob, refUnit);
  const length = Math.max(0.25, vectorLength(bob.x - pivot.x, bob.y - pivot.y));
  const baselineEnd = {
    x: pivot.x + refUnit.x * length,
    y: pivot.y + refUnit.y * length,
  };
  const currentEnd = {
    x: pivot.x + bobUnit.x * length,
    y: pivot.y + bobUnit.y * length,
  };
  const arcRadius = Math.max(0.18, Math.min(0.46, length * 0.32));
  const midAngle = -Math.PI / 2 + normalizeAngleSweep(theta) / 2;
  const labelRadius = arcRadius + 0.12;
  const labelPoint = {
    x: pivot.x + Math.cos(midAngle) * labelRadius,
    y: pivot.y + Math.sin(midAngle) * labelRadius,
  };

  const shapes = [
    {
      id: "measure.angle.theta.baseline",
      kind: "line",
      role: "angle_measure_baseline",
      group_id: "measure.angle.theta",
      x1: pivot.x,
      y1: pivot.y,
      x2: baselineEnd.x,
      y2: baselineEnd.y,
      stroke: String(style.baseline_color ?? "#94a3b8"),
      width: 1.4,
    },
    {
      id: "measure.angle.theta.current",
      kind: "line",
      role: "angle_measure_current_line",
      group_id: "measure.angle.theta",
      x1: pivot.x,
      y1: pivot.y,
      x2: currentEnd.x,
      y2: currentEnd.y,
      stroke: String(style.current_color ?? "#0ea5e9"),
      width: 1.6,
    },
    buildArcPolyline({
      pivot,
      radius: arcRadius,
      theta,
      id: "measure.angle.theta.arc",
      stroke: String(style.arc_color ?? "#ef4444"),
    }),
    {
      id: "measure.angle.theta.label",
      kind: "text",
      role: "angle_measure_label",
      group_id: "measure.angle.theta",
      x: labelPoint.x,
      y: labelPoint.y,
      text: formatAngleLabel(theta),
      color: String(style.label_color ?? "#991b1b"),
      size: 12,
    },
  ];
  return {
    shapes,
    meta: {
      measure_id: String(measure.measure_id ?? "measure.angle.theta"),
      pivot,
      bob,
      value: theta,
      unit: expectedUnit || actualUnit,
      label: formatAngleLabel(theta),
      object_ids: shapes.map((shape) => shape.id),
      bounds: computeBounds([...shapes, { kind: "point", x: pivot.x, y: pivot.y }, { kind: "point", x: bob.x, y: bob.y }]),
    },
  };
}

function computeBounds(shapes) {
  const xs = [];
  const ys = [];
  const add = (x, y) => {
    const nx = toFiniteNumber(x);
    const ny = toFiniteNumber(y);
    if (Number.isFinite(nx) && Number.isFinite(ny)) {
      xs.push(nx);
      ys.push(ny);
    }
  };
  for (const shape of Array.isArray(shapes) ? shapes : []) {
    if (Array.isArray(shape?.points)) {
      shape.points.forEach((point) => add(point?.x, point?.y));
      continue;
    }
    add(shape?.x, shape?.y);
    add(shape?.cx, shape?.cy);
    add(shape?.x1, shape?.y1);
    add(shape?.x2, shape?.y2);
  }
  if (!xs.length || !ys.length) {
    return { x_min: -1, x_max: 1, y_min: -1, y_max: 1 };
  }
  return {
    x_min: Math.min(...xs),
    x_max: Math.max(...xs),
    y_min: Math.min(...ys),
    y_max: Math.max(...ys),
  };
}

function expandBounds(bounds, padding = 0.2, minSpan = 1.0) {
  const xMin = toFiniteNumber(bounds?.x_min, -1);
  const xMax = toFiniteNumber(bounds?.x_max, 1);
  const yMin = toFiniteNumber(bounds?.y_min, -1);
  const yMax = toFiniteNumber(bounds?.y_max, 1);
  const xMid = (xMin + xMax) / 2;
  const yMid = (yMin + yMax) / 2;
  const xSpan = Math.max(minSpan, Math.abs(xMax - xMin) + padding * 2);
  const ySpan = Math.max(minSpan, Math.abs(yMax - yMin) + padding * 2);
  return {
    x_min: xMid - xSpan / 2,
    x_max: xMid + xSpan / 2,
    y_min: yMid - ySpan / 2,
    y_max: yMid + ySpan / 2,
  };
}

function resolveCameraPolicy(viewPlan, policyId, bindings, bounds, diagnostics) {
  const policies = Array.isArray(viewPlan?.camera?.policies) ? viewPlan.camera.policies : [];
  const defaultPolicy = String(viewPlan?.camera?.default_policy ?? "").trim();
  const requested = String(policyId ?? "").trim() || defaultPolicy || "fit";
  let policy = policies.find((item) => String(item?.policy_id ?? "").trim() === requested) ?? null;
  if (!policy) {
    policy = policies.find((item) => String(item?.policy_id ?? "").trim() === defaultPolicy) ?? policies[0] ?? null;
    diagnostics.push({
      code: String(viewPlan?.camera?.conflict_diagnostic ?? "W_VIEW_CAMERA_POLICY_CONFLICT"),
      severity: "warning",
      message: `카메라 정책 ${requested}을 찾지 못해 기본 정책을 사용했습니다.`,
      requested_policy: requested,
    });
  }
  const mode = String(policy?.mode ?? policy?.policy_id ?? "fit").trim() || "fit";
  if (mode === "fixed" && isObject(policy?.range)) {
    return { policy_id: String(policy.policy_id ?? "fixed"), mode, range: policy.range };
  }
  if (mode === "follow") {
    const target = readPoint(bindings.get(String(policy?.target_anchor ?? "").trim())) ?? { x: 0, y: 0 };
    const span = policy?.span ?? {};
    const xSpan = Math.max(0.5, toFiniteNumber(span.x, 1.8));
    const ySpan = Math.max(0.5, toFiniteNumber(span.y, 1.8));
    return {
      policy_id: String(policy?.policy_id ?? "follow"),
      mode,
      range: {
        x_min: target.x - xSpan / 2,
        x_max: target.x + xSpan / 2,
        y_min: target.y - ySpan / 2,
        y_max: target.y + ySpan / 2,
      },
    };
  }
  return {
    policy_id: String(policy?.policy_id ?? "fit"),
    mode: "fit",
    range: expandBounds(bounds, toFiniteNumber(policy?.padding, 0.24), toFiniteNumber(policy?.min_span, 1.2)),
  };
}

function buildPendulumBaseShapes(bindings) {
  const pivot = readPoint(bindings.get("obs.pivot"));
  const bob = readPoint(bindings.get("obs.bob"));
  if (!pivot || !bob) return [];
  return [
    {
      id: "pendulum.rod",
      kind: "line",
      role: "pendulum_rod",
      x1: pivot.x,
      y1: pivot.y,
      x2: bob.x,
      y2: bob.y,
      stroke: "#475569",
      width: 2,
    },
    {
      id: "pendulum.bob",
      kind: "circle",
      role: "pendulum_bob",
      cx: bob.x,
      cy: bob.y,
      r: 0.08,
      fill: "#38bdf8",
      stroke: "#0ea5e9",
      width: 2,
    },
    {
      id: "pendulum.pivot",
      kind: "point",
      role: "pendulum_pivot",
      x: pivot.x,
      y: pivot.y,
      size: 0.05,
      color: "#f59e0b",
    },
  ];
}

function enrichGraphWithCursor(graph, viewPlan, bindings, observation) {
  const cursor = viewPlan?.graph_cursor;
  if (!isObject(cursor)) return graph;
  const xBinding = bindings.get(String(cursor.x_anchor ?? "").trim());
  const yBinding = bindings.get(String(cursor.y_anchor ?? "").trim());
  const x = toFiniteNumber(xBinding?.value);
  const y = toFiniteNumber(yBinding?.value);
  if (!Number.isFinite(x) || !Number.isFinite(y)) return graph;
  const next = isObject(graph) ? { ...graph } : {};
  next.meta = {
    ...(isObject(next.meta) ? next.meta : {}),
    current_point: {
      cursor_id: String(cursor.cursor_id ?? "graph.current"),
      series_id: String(cursor.series_id ?? ""),
      x,
      y,
      x_unit: String(xBinding?.unit ?? ""),
      y_unit: String(yBinding?.unit ?? ""),
      label: String(cursor.label ?? "현재점"),
      tick_id: toFiniteNumber(observation?.values?.tick_id ?? observation?.tick_id, 0),
    },
  };
  return next;
}

export function buildSeamgrimViewPlanRuntime({ viewPlan, observation, views, cameraPolicyId, angleMeasureVisible = true } = {}) {
  if (!isObject(viewPlan) || String(viewPlan.schema ?? "") !== "seamgrim.view_plan.v1") {
    return null;
  }
  const showAngleMeasure = angleMeasureVisible !== false;
  const diagnostics = [];
  const resolved = resolveSemanticBindings(viewPlan, observation ?? {});
  diagnostics.push(...resolved.diagnostics);
  const bindings = resolved.anchors;
  const baseShapes = buildPendulumBaseShapes(bindings);
  const angle = buildAngleMeasureShapes({ viewPlan, bindings, diagnostics });
  const shapes = [...baseShapes, ...(showAngleMeasure ? angle.shapes : [])];
  const shapeBounds = computeBounds(shapes);
  const camera = resolveCameraPolicy(viewPlan, cameraPolicyId, bindings, shapeBounds, diagnostics);
  const tickId = toFiniteNumber(observation?.values?.tick_id ?? observation?.tick_id, 0);
  const theta = toFiniteNumber(bindings.get("obs.theta")?.value, 0);
  const omega = toFiniteNumber(bindings.get("obs.angular_velocity")?.value, 0);
  const time = toFiniteNumber(bindings.get("obs.time")?.value, 0);
  const graph = enrichGraphWithCursor(views?.graph ?? null, viewPlan, bindings, observation ?? {});
  const shapePayloadForHash = shapes.map((shape) => ({
    ...shape,
    points: Array.isArray(shape.points) ? shape.points.map((point) => ({ x: point.x, y: point.y })) : undefined,
  }));
  const space2d = {
    schema: "seamgrim.space2d.v0",
    source: "view_plan",
    camera: {
      x_min: camera.range.x_min,
      x_max: camera.range.x_max,
      y_min: camera.range.y_min,
      y_max: camera.range.y_max,
      policy_id: camera.policy_id,
      mode: camera.mode,
    },
    shapes,
    meta: {
      source: "view_plan",
      binding_mode: "explicit",
      view_roles: [
        "semantic_binding",
        ...(showAngleMeasure ? ["angle_measure"] : []),
        "same_tick_graph_cursor",
        "camera_policy",
      ],
      axes: ["x", "y"],
      camera_policy: camera.policy_id,
      camera_mode: camera.mode,
      state_hash_participation: false,
      tick_id: tickId,
      angle_measure: angle.meta,
      angle_measure_visible: showAngleMeasure,
      graph_current_point: graph?.meta?.current_point ?? null,
      view_plan_hash: buildViewHashCandidate({ viewPlan, cameraPolicyId: camera.policy_id, angleMeasureVisible: showAngleMeasure }, "view_plan"),
      world_draw_payload_hash_candidate: buildViewHashCandidate(shapePayloadForHash, "world_draw_payload"),
      observation_snapshot: {
        theta,
        angular_velocity: omega,
        time,
      },
    },
  };
  return {
    views: {
      ...(isObject(views) ? views : {}),
      space2d,
      graph,
      view_plan: {
        schema: "seamgrim.view_plan.runtime.v1",
        lesson_id: String(viewPlan.lesson_id ?? ""),
        binding_mode: "explicit",
        state_hash_participation: false,
        camera_policy: camera.policy_id,
        angle_measure_visible: showAngleMeasure,
        diagnostics,
        anchors: Array.from(bindings.values()),
        angle_measure: angle.meta,
        graph_current_point: graph?.meta?.current_point ?? null,
        view_plan_hash: space2d.meta.view_plan_hash,
        world_draw_payload_hash_candidate: space2d.meta.world_draw_payload_hash_candidate,
        same_tick: {
          tick_id: tickId,
          time,
          theta,
          angular_velocity: omega,
        },
      },
    },
    report: {
      schema: "seamgrim.view_plan.runtime.v1",
      lesson_id: String(viewPlan.lesson_id ?? ""),
      binding_mode: "explicit",
      camera_policy: camera.policy_id,
      diagnostics,
      tick_id: tickId,
      theta,
      angular_velocity: omega,
      time,
      angle_label: angle.meta?.label ?? "",
      angle_measure_visible: showAngleMeasure,
      graph_current_point: graph?.meta?.current_point ?? null,
      view_plan_hash: space2d.meta.view_plan_hash,
      world_draw_payload_hash_candidate: space2d.meta.world_draw_payload_hash_candidate,
      state_hash_participation: false,
    },
  };
}
