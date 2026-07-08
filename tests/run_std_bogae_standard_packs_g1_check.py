#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests" / "tools"))
import config_digest_proto  # noqa: E402


PACK_IDS = ["std_bogae_core_v1", "std_bogae_grid2d_v1", "std_bogae_graph2d_v1"]


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "std_bogae_standard_packs_g1"
REPORT = BUILD / "std_bogae_standard_packs_g1_check_report.detjson"


def fail(message: str) -> int:
    print(f"std_bogae_standard_packs_g1_check: FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def inclusive_ticks(start: int, end: int, step: int) -> list[int]:
    if step <= 0:
        raise ValueError("tick step must be positive")
    values = []
    current = start
    while current <= end:
        values.append(current)
        current += step
    return values


def lower_graph2d(fixture: dict[str, Any]) -> dict[str, Any]:
    x0, x1 = fixture["domain"]["x"]
    y0, y1 = fixture["domain"]["y"]
    x_ticks = inclusive_ticks(int(x0), int(x1), int(fixture["ticks"]["x_step"]))
    y_ticks = inclusive_ticks(int(y0), int(y1), int(fixture["ticks"]["y_step"]))
    sorted_series = sorted(fixture["series"], key=lambda row: row["series_id"])
    label_counts: Counter[str] = Counter()
    series_payload = []
    commands = [
        {"op": "axis", "axis": "x", "ticks": x_ticks},
        {"op": "axis", "axis": "y", "ticks": y_ticks},
    ]
    for series in sorted_series:
        label = series["label"]
        label_counts[label] += 1
        display_label = label if label_counts[label] == 1 else f"{label}#{label_counts[label]}"
        points = sorted(series["points"], key=lambda point: (point[0], point[1]))
        series_row = {
            "series_id": series["series_id"],
            "source_label": label,
            "display_label": display_label,
            "points": points,
        }
        series_payload.append(series_row)
        commands.append(
            {
                "op": "polyline",
                "series_id": series["series_id"],
                "label": display_label,
                "points": points,
            }
        )
    payload = {
        "schema": "ddn.std_bogae_graph2d.payload.v1",
        "codec": "BDL1-payload-proto",
        "profile": "graph2d",
        "domain": {"x": [x0, x1], "y": [y0, y1]},
        "ticks": {"x": x_ticks, "y": y_ticks},
        "series_order_rule": fixture["series_order"]["rule"],
        "label_collision_policy_candidate": fixture["label_collision"]["candidate_policy"],
        "label_collision_policy_finalized": fixture["label_collision"]["finalized"],
        "series": series_payload,
        "commands": commands,
        "world_state_mutation": False,
        "pixel_hash_truth": False,
    }
    payload["bogae_hash"] = config_digest_proto.blake3_digest(canonical_bytes(payload))
    return payload


def run(args: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    contracts: dict[str, dict[str, Any]] = {}
    for pack_id in PACK_IDS:
        pack = ROOT / "pack" / pack_id
        if not pack.exists():
            return fail(f"missing pack {pack_id}")
        contract_path = pack / "contract.detjson"
        if not contract_path.exists():
            return fail(f"missing contract for {pack_id}")
        contract = load_json(contract_path)
        contracts[pack_id] = contract
        if contract.get("evidence_tier") != "pack_skeleton":
            return fail(f"{pack_id} must remain pack_skeleton")
        if contract.get("closure_grade") != "닫힘-문서":
            return fail(f"{pack_id} closure grade mismatch")
        for key in ["behavior_closure_claim", "rendering_smoke_claim", "parser_frontdoor_change", "runtime_semantics_change", "world_state_mutation"]:
            if contract.get(key) is not False:
                return fail(f"{pack_id}.{key} must be false")
        hash_truth = contract.get("hash_truth", {})
        if hash_truth.get("bogae_hash_source") != "payload_or_DrawList_bytes":
            return fail(f"{pack_id} hash source mismatch")
        if hash_truth.get("pixel_hash_truth") is not False:
            return fail(f"{pack_id} must not use pixel hash as truth")

    for linked in contracts["std_bogae_grid2d_v1"].get("linked_existing_grid2d_evidence", []):
        if not (ROOT / linked).exists():
            return fail(f"missing linked grid2d evidence {linked}")

    fixture_path = ROOT / "pack" / "std_bogae_graph2d_v1" / "graph2d_lowering_fixture.detjson"
    fixture = load_json(fixture_path)
    payload_a = lower_graph2d(fixture)
    payload_b = lower_graph2d(fixture)
    bytes_a = canonical_bytes(payload_a)
    bytes_b = canonical_bytes(payload_b)
    if bytes_a != bytes_b:
        return fail("same graph2d input did not produce identical payload bytes")
    if [row["series_id"] for row in payload_a["series"]] != ["alpha", "beta"]:
        return fail(f"series order mismatch: {payload_a['series']}")
    if payload_a["ticks"]["x"] != [0, 1, 2] or payload_a["ticks"]["y"] != [0, 1, 2, 3, 4]:
        return fail(f"tick lowering mismatch: {payload_a['ticks']}")
    if [row["display_label"] for row in payload_a["series"]] != ["value", "value#2"]:
        return fail(f"label collision lowering mismatch: {payload_a['series']}")
    if not str(payload_a.get("bogae_hash", "")).startswith("blake3:"):
        return fail("bogae_hash must be blake3 over payload bytes")
    if payload_a.get("pixel_hash_truth") is not False or payload_a.get("world_state_mutation") is not False:
        return fail("payload must not claim pixel truth or world mutation")

    out_payload = BUILD / "graph2d_payload.detjson"
    out_payload.write_text(json.dumps(payload_a, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    product_status = run(["git", "status", "--short", "--", "lang", "core", "tool", "tools/teul-cli/src"], timeout=30)
    if product_status.returncode != 0:
        return fail(product_status.stderr.strip())
    if product_status.stdout.strip():
        return fail(f"product path changed: {product_status.stdout.strip()}")

    report = {
        "schema": "ddn.std_bogae_standard_packs_g1.check_report.v1",
        "status": "PASS",
        "closure_grade": "닫힘-문서",
        "packs": PACK_IDS,
        "graph2d_payload": out_payload.as_posix(),
        "graph2d_payload_bytes_identical": True,
        "bogae_hash": payload_a["bogae_hash"],
        "hash_truth": "payload_or_DrawList_bytes",
        "pixel_hash_truth": False,
        "world_state_mutation": False,
        "product_path_status": product_status.stdout.strip(),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("std_bogae_standard_packs_g1_check: PASS")
    print(f"report={REPORT.as_posix()}")
    print(f"payload={out_payload.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
