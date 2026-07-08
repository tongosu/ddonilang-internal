#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "education_physics_vertical_slice_g5_v1"
sys.path.insert(0, str(ROOT / "tests" / "tools"))
import config_digest_proto  # noqa: E402

WASM_SMOKE_CMD = [sys.executable, "tests/run_seamgrim_wasm_web_smoke_contract_pack_check.py"]
INTEGRATOR_CHECK_CMD = [sys.executable, "tests/run_stdlib_l1_integrators_g1_check.py"]


def preferred_build_root() -> Path:
    primary = Path("I:/home/urihanl/ddn/codex/build")
    fallback = Path("C:/ddn/codex/build")
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    return ROOT / "build"


BUILD = preferred_build_root() / "education_physics_vertical_slice_g5"
REPORT = BUILD / "education_physics_vertical_slice_g5_check_report.detjson"


def fail(message: str) -> int:
    print(f"education_physics_vertical_slice_g5_check: FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def run(args: list[str], *, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def rounded(value: float) -> float:
    return float(f"{value:.10f}")


def simulate_series(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    params = fixture["parameters"]
    theta0 = float(params["theta0"])
    omega0 = float(params["omega0"])
    dt = float(params["dt"])
    steps = int(params["steps"])
    if dt <= 0:
        raise ValueError("dt must be positive")
    if steps < 1:
        raise ValueError("steps must be at least 1")

    series_rows: list[dict[str, Any]] = []
    for spec in fixture["integrators"]:
        theta = theta0
        omega = omega0
        points: list[list[float]] = []
        for step in range(steps + 1):
            points.append([float(step), rounded(theta)])
            if step == steps:
                break
            acceleration = -theta
            if spec["algorithm"] == "explicit_euler":
                next_theta = theta + omega * dt
                next_omega = omega + acceleration * dt
            elif spec["algorithm"] == "semi_implicit_euler":
                next_omega = omega + acceleration * dt
                next_theta = theta + next_omega * dt
            else:
                raise ValueError(f"unsupported integrator algorithm: {spec['algorithm']}")
            theta, omega = next_theta, next_omega
        series_rows.append(
            {
                "series_id": spec["series_id"],
                "source_label": spec["label"],
                "ddn_surface": spec["ddn_surface"],
                "algorithm": spec["algorithm"],
                "points": points,
            }
        )
    return series_rows


def lower_graph2d(fixture: dict[str, Any]) -> dict[str, Any]:
    graph = fixture["graph2d"]
    sorted_series = sorted(simulate_series(fixture), key=lambda row: row["series_id"])
    label_counts: Counter[str] = Counter()
    series_payload: list[dict[str, Any]] = []
    commands: list[dict[str, Any]] = [
        {"op": "axis", "axis": "x", "ticks": graph["ticks"]["x_values"]},
        {"op": "axis", "axis": "y", "ticks": graph["ticks"]["y_values"]},
    ]
    for series in sorted_series:
        label = series["source_label"]
        label_counts[label] += 1
        display_label = label if label_counts[label] == 1 else f"{label}#{label_counts[label]}"
        row = {
            "series_id": series["series_id"],
            "source_label": label,
            "display_label": display_label,
            "ddn_surface": series["ddn_surface"],
            "algorithm": series["algorithm"],
            "points": series["points"],
        }
        series_payload.append(row)
        commands.append(
            {
                "op": "polyline",
                "series_id": row["series_id"],
                "label": display_label,
                "points": row["points"],
            }
        )

    payload = {
        "schema": "ddn.education_physics_vertical_slice_g5.graph2d_payload.v1",
        "codec": "BDL1-payload-proto",
        "profile": graph["profile"],
        "source_pack": fixture["source_pack"],
        "domain": graph["domain"],
        "ticks": graph["ticks"],
        "series_order_rule": graph["series_order"]["rule"],
        "label_collision_policy_candidate": graph["label_collision"]["candidate_policy"],
        "label_collision_policy_finalized": graph["label_collision"]["finalized"],
        "series": series_payload,
        "commands": commands,
        "world_state_mutation": False,
        "pixel_hash_truth": False,
    }
    payload["bogae_hash"] = config_digest_proto.blake3_digest(canonical_bytes(payload))
    return payload


def check_diag_fixture() -> tuple[int, list[str]]:
    fixture = load_json(PACK / "diag_three_layer_fixture.detjson")
    required = set(fixture["required_layers"])
    missing: list[str] = []
    entries = fixture.get("entries", [])
    for entry in entries:
        for key in sorted(required):
            if not entry.get(key):
                missing.append(f"{entry.get('id', '<unknown>')}::{key}")
    return len(entries), missing


def write_blocker_report(proc: subprocess.CompletedProcess[str]) -> Path:
    blocker = BUILD / "wasm_delivery_blocker_report.detjson"
    blocker.write_text(
        json.dumps(
            {
                "schema": "ddn.education_physics_vertical_slice_g5.wasm_blocker.v1",
                "status": "blocked",
                "command": WASM_SMOKE_CMD,
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "fallback": "python tests/run_stdlib_l1_integrators_g1_check.py",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return blocker


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    for name in ["README.md", "contract.detjson", "diag_three_layer_fixture.detjson", "physics_graph2d_fixture.detjson"]:
        if not (PACK / name).exists():
            return fail(f"missing pack file: {name}")

    contract = load_json(PACK / "contract.detjson")
    if contract.get("closure_grade") != "닫힘-문서":
        return fail("contract must keep overall closure at 닫힘-문서")
    for key in ["parser_frontdoor_change", "runtime_semantics_change", "state_hash_change", "natural_language_direct_execution"]:
        if contract.get(key) is not False:
            return fail(f"contract {key} must be false")
    for rel_path in contract.get("linked_existing_evidence", []):
        if not (ROOT / rel_path).exists():
            return fail(f"missing linked evidence: {rel_path}")

    diag_count, diag_missing = check_diag_fixture()
    if diag_count < 5:
        return fail(f"diag fixture must contain at least 5 entries, got {diag_count}")
    if diag_missing:
        return fail(f"diag fixture missing layers: {diag_missing}")

    wasm_proc = run(WASM_SMOKE_CMD, timeout=180)
    wasm_blocker_path: str | None = None
    if wasm_proc.returncode != 0:
        wasm_blocker_path = write_blocker_report(wasm_proc).as_posix()

    integrator_proc = run(INTEGRATOR_CHECK_CMD, timeout=180)
    if integrator_proc.returncode != 0:
        return fail(integrator_proc.stderr.strip() or integrator_proc.stdout.strip() or "integrator check failed")

    fixture = load_json(PACK / "physics_graph2d_fixture.detjson")
    payload_a = lower_graph2d(fixture)
    payload_b = lower_graph2d(fixture)
    bytes_a = canonical_bytes(payload_a)
    bytes_b = canonical_bytes(payload_b)
    if bytes_a != bytes_b:
        return fail("graph2d payload bytes changed across identical lowering")
    if [row["series_id"] for row in payload_a["series"]] != ["explicit_euler_theta", "semi_implicit_euler_theta"]:
        return fail("integrator series order mismatch")
    first_steps = {row["algorithm"]: row["points"][1][1] for row in payload_a["series"]}
    if first_steps != {"explicit_euler": 0.2, "semi_implicit_euler": 0.198}:
        return fail(f"first-step physics bridge mismatch: {first_steps}")
    if [row["display_label"] for row in payload_a["series"]] != ["theta", "theta#2"]:
        return fail("label collision candidate did not apply")
    if payload_a.get("world_state_mutation") is not False or payload_a.get("pixel_hash_truth") is not False:
        return fail("graph payload must not claim world mutation or pixel truth")

    payload_path = BUILD / "physics_graph2d_payload.detjson"
    payload_path.write_text(
        json.dumps(payload_a, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    product_status = run(["git", "status", "--short", "--", "lang", "core", "tool", "tools/teul-cli/src"], timeout=30)
    if product_status.returncode != 0:
        return fail(product_status.stderr.strip())
    if product_status.stdout.strip():
        return fail(f"product path changed: {product_status.stdout.strip()}")

    report = {
        "schema": "ddn.education_physics_vertical_slice_g5.check_report.v1",
        "status": "PASS",
        "closure_grade": {
            "browser_delivery_smoke": "닫힘-동작" if wasm_proc.returncode == 0 else "blocker",
            "education_physics_payload_bridge": "닫힘-문서",
            "overall_vertical_slice": "닫힘-문서"
        },
        "wasm_browser_delivery_smoke": {
            "attempted": True,
            "passed": wasm_proc.returncode == 0,
            "command": WASM_SMOKE_CMD,
            "stdout": wasm_proc.stdout.strip(),
            "stderr": wasm_proc.stderr.strip(),
            "blocker_report": wasm_blocker_path
        },
        "cli_fallback": {
            "required_if_wasm_blocked": True,
            "passed": integrator_proc.returncode == 0,
            "command": INTEGRATOR_CHECK_CMD,
            "stdout": integrator_proc.stdout.strip(),
            "stderr": integrator_proc.stderr.strip()
        },
        "diag_three_layer_fixture_count": diag_count,
        "integrators_executed": [
            "적분.오일러",
            "적분.반암시적오일러"
        ],
        "graph2d_payload": payload_path.as_posix(),
        "graph2d_payload_bytes_identical": True,
        "bogae_hash": payload_a["bogae_hash"],
        "world_state_mutation": False,
        "pixel_hash_truth": False,
        "product_path_status": product_status.stdout.strip()
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("education_physics_vertical_slice_g5_check: PASS")
    print(f"report={REPORT.as_posix()}")
    print(f"payload={payload_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
