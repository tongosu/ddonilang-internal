#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSONS_ROOT = ROOT / "solutions" / "seamgrim_ui_mvp" / "lessons"
CARDS_PATH = LESSONS_ROOT / "lesson_cards.v0.detjson"
INDEX_PATH = LESSONS_ROOT / "index.json"
PACK = ROOT / "pack" / "seamgrim_wave3b_foundation12_view_plan_v1"
TARGETS = [
    "elem_math_number_line",
    "elem_math_fraction_line",
    "elem_math_rectangle_area",
    "elem_science_daily_temperature",
    "elem_econ_allowance_budget",
    "elem_econ_store_stock",
    "rep_math_function_line_v1",
    "rep_phys_pendulum_wave1_v1",
    "rep_phys_projectile_xy_v1",
    "rep_econ_supply_demand_tax_v1",
    "rep_phys_damped_oscillation_v1",
    "high_math_derivative",
]
ALLOWED_VIEWS = {"graph", "space2d", "table", "text"}


def fail(code: str, detail: str) -> int:
    print(f"{code}: {detail}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(cmd: list[str], timeout: int = 120) -> tuple[int, str]:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout


def parse_simple_toml_string(path: Path, key: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*\"([^\"]+)\"", text)
    return match.group(1).strip() if match else ""


def token_occurs(source: str, token: str) -> bool:
    return bool(token and re.search(rf"(?<!\w){re.escape(token)}(?!\w)", source))


def source_ref_tokens(anchor: dict) -> list[str]:
    ref = anchor.get("source_ref") if isinstance(anchor.get("source_ref"), dict) else {}
    kind = str(ref.get("kind", "")).strip()
    if kind == "observation":
        return [str(ref.get("key", "")).strip()]
    if kind == "point2":
        return [str(ref.get("x_key", "")).strip(), str(ref.get("y_key", "")).strip()]
    return []


def validate_view_plan(lesson_id: str, card_primary_view: str, index_meta_path: str) -> list[str]:
    diagnostics: list[str] = []
    lesson_dir = LESSONS_ROOT / lesson_id
    plan_path = lesson_dir / "view_plan.detjson"
    meta_path = lesson_dir / "meta.toml"
    lesson_path = lesson_dir / "lesson.ddn"
    if not plan_path.exists():
        return [f"E_VIEW_PLAN_MISSING:{lesson_id}"]
    if not meta_path.exists() or not lesson_path.exists():
        return [f"E_VIEW_PLAN_LESSON_ASSET_MISSING:{lesson_id}"]
    meta_view_path = parse_simple_toml_string(meta_path, "view_plan_path")
    expected_view_path = f"solutions/seamgrim_ui_mvp/lessons/{lesson_id}/view_plan.detjson"
    if meta_view_path != expected_view_path:
        diagnostics.append(f"E_VIEW_PLAN_META_PATH:{lesson_id}:{meta_view_path}")
    expected_meta_path = f"solutions/seamgrim_ui_mvp/lessons/{lesson_id}/meta.toml"
    if index_meta_path != expected_meta_path:
        diagnostics.append(f"E_VIEW_PLAN_INDEX_META_PATH:{lesson_id}:{index_meta_path}")
    plan = load_json(plan_path)
    source = lesson_path.read_text(encoding="utf-8")
    if plan.get("schema") != "seamgrim.view_plan.v1":
        diagnostics.append(f"E_VIEW_PLAN_SCHEMA:{lesson_id}")
    if plan.get("lesson_id") != lesson_id:
        diagnostics.append(f"E_VIEW_PLAN_LESSON_ID:{lesson_id}")
    if plan.get("binding_mode") != "explicit":
        diagnostics.append(f"E_VIEW_PLAN_BINDING_MODE:{lesson_id}")
    if plan.get("runtime_surface") != "ddn.original.product_frontdoor":
        diagnostics.append(f"E_VIEW_PLAN_RUNTIME_SURFACE:{lesson_id}")
    primary = str(plan.get("primary_view_target", "")).strip()
    if primary not in ALLOWED_VIEWS:
        diagnostics.append(f"E_VIEW_PLAN_PRIMARY_TARGET:{lesson_id}:{primary}")
    if primary != card_primary_view:
        diagnostics.append(f"E_VIEW_PLAN_CARD_PRIMARY_MISMATCH:{lesson_id}:{primary}:{card_primary_view}")
    anchors = plan.get("anchors") if isinstance(plan.get("anchors"), list) else []
    required = [str(item).strip() for item in plan.get("required_anchor_ids", [])] if isinstance(plan.get("required_anchor_ids"), list) else []
    anchor_ids = [str(anchor.get("anchor_id", "")).strip() for anchor in anchors if isinstance(anchor, dict)]
    if len(anchor_ids) < 2:
        diagnostics.append(f"E_VIEW_PLAN_ANCHOR_COUNT:{lesson_id}:{len(anchor_ids)}")
    if len(anchor_ids) != len(set(anchor_ids)):
        diagnostics.append(f"E_VIEW_PLAN_DUPLICATE_ANCHOR:{lesson_id}")
    if len(required) < 2 or not set(required).issubset(set(anchor_ids)):
        diagnostics.append(f"E_VIEW_PLAN_REQUIRED_ANCHORS:{lesson_id}:{required}")
    for anchor in anchors:
        anchor_id = str(anchor.get("anchor_id", "")).strip()
        if not anchor_id:
            diagnostics.append(f"E_VIEW_PLAN_ANCHOR_ID:{lesson_id}")
            continue
        if not str(anchor.get("unit", "")).strip():
            diagnostics.append(f"E_VIEW_PLAN_ANCHOR_UNIT:{lesson_id}:{anchor_id}")
        if not str(anchor.get("accessibility_name", "")).strip():
            diagnostics.append(f"E_VIEW_PLAN_ANCHOR_A11Y:{lesson_id}:{anchor_id}")
        provenance = anchor.get("provenance") if isinstance(anchor.get("provenance"), dict) else {}
        if provenance.get("path") != f"solutions/seamgrim_ui_mvp/lessons/{lesson_id}/lesson.ddn":
            diagnostics.append(f"E_VIEW_PLAN_ANCHOR_PATH:{lesson_id}:{anchor_id}")
        span = str(provenance.get("source_span", "")).strip()
        if not span:
            diagnostics.append(f"E_VIEW_PLAN_ANCHOR_SPAN:{lesson_id}:{anchor_id}")
        else:
            parts = [part.strip() for part in span.split(";") if part.strip()]
            if span not in source and (not parts or not all(part in source for part in parts)):
                diagnostics.append(f"E_VIEW_PLAN_ANCHOR_SPAN_NOT_IN_SOURCE:{lesson_id}:{anchor_id}:{span}")
        for token in source_ref_tokens(anchor):
            if token and not token_occurs(source, token):
                diagnostics.append(f"E_VIEW_PLAN_ANCHOR_SOURCE_TOKEN:{lesson_id}:{anchor_id}:{token}")
    graph_cursor = plan.get("graph_cursor") if isinstance(plan.get("graph_cursor"), dict) else {}
    if primary == "graph":
        if graph_cursor.get("x_anchor") not in anchor_ids or graph_cursor.get("y_anchor") not in anchor_ids:
            diagnostics.append(f"E_VIEW_PLAN_GRAPH_CURSOR:{lesson_id}")
    camera = plan.get("camera")
    if primary == "graph" and camera is not None:
        diagnostics.append(f"E_VIEW_PLAN_GRAPH_CAMERA:{lesson_id}")
    if isinstance(camera, dict) and camera.get("state_hash_participation") is not False:
        diagnostics.append(f"E_VIEW_PLAN_CAMERA_STATE_HASH:{lesson_id}")
    hash_policy = plan.get("hash_policy") if isinstance(plan.get("hash_policy"), dict) else {}
    if hash_policy.get("state_hash_participation") is not False:
        diagnostics.append(f"E_VIEW_PLAN_HASH_POLICY:{lesson_id}")
    if hash_policy.get("view_plan_hash_candidate") is not True:
        diagnostics.append(f"E_VIEW_PLAN_HASH_CANDIDATE:{lesson_id}")
    return diagnostics


def validate_all(cards: dict, index: dict) -> list[str]:
    card_by_id = {
        str(row.get("lesson_id", "")).strip(): row
        for row in cards.get("cards", [])
        if isinstance(row, dict)
    }
    index_by_id = {
        str(row.get("id", "")).strip(): row
        for row in index.get("lessons", [])
        if isinstance(row, dict)
    }
    diagnostics: list[str] = []
    for lesson_id in TARGETS:
        card = card_by_id.get(lesson_id) or {}
        row = index_by_id.get(lesson_id) or {}
        diagnostics.extend(validate_view_plan(
            lesson_id,
            str(card.get("primary_view", "")).strip(),
            str(row.get("meta_path", "")).strip(),
        ))
    return diagnostics


def main() -> int:
    for required in ["README.md", "contract.detjson", "input.ddn", "golden.jsonl"]:
        if not (PACK / required).exists():
            return fail("E_WAVE3B_G3_PACK_MISSING", required)
    cards = load_json(CARDS_PATH)
    index = load_json(INDEX_PATH)
    diagnostics = validate_all(cards, index)
    if diagnostics:
        return fail("E_WAVE3B_G3_STATIC", json.dumps(diagnostics, ensure_ascii=False))

    damaged_path = LESSONS_ROOT / TARGETS[0] / "view_plan.detjson"
    damaged = load_json(damaged_path)
    damaged["anchors"] = damaged["anchors"][:1]
    tmp_cards = deepcopy(cards)
    if len(damaged.get("anchors", [])) >= 2:
        return fail("E_WAVE3B_G3_NEGATIVE", "damaged fixture did not damage anchor count")

    for cmd, timeout, code in [
        (["node", "--check", "tests/seamgrim_wave3b_foundation12_view_plan_runner.mjs"], 60, "E_WAVE3B_G3_NODE_CHECK"),
        (["node", "tests/seamgrim_wave3b_foundation12_view_plan_runner.mjs"], 360, "E_WAVE3B_G3_BROWSER"),
        (["python", "tests/run_pack_golden.py", "seamgrim_wave3b_foundation12_view_plan_v1"], 120, "E_WAVE3B_G3_GOLDEN"),
        (["git", "-c", "safe.directory=I:/dev/ddonilang/codex", "-c", "core.excludesfile=I:/dev/ddonilang/codex/.git/info/exclude", "status", "--short", "--", "docs/ssot"], 60, "E_WAVE3B_G3_SSOT"),
    ]:
        rc, output = run(cmd, timeout=timeout)
        if rc != 0:
            return fail(code, output.strip())
        if code == "E_WAVE3B_G3_SSOT" and output.strip():
            return fail("E_WAVE3B_G3_SSOT_DIRTY", output.strip())

    print("[seamgrim-wave3b-foundation12-view-plan-v1] OK behavior-closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
