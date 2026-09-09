#!/usr/bin/env python
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "seamgrim_runner_lifecycle_reliability_v1"
RUNNER = ROOT / "tests" / "seamgrim_workbench_run_archive_lineage_runner.mjs"
REQUIRED_IDENTITY_FIELDS = {
    "pid",
    "parent_pid",
    "creation_time",
    "executable_name",
    "command_fingerprint_sha256",
    "identity_sha256",
}


def fail(code: str, message: str) -> int:
    print(f"{code}: {message}")
    return 1


def run(cmd: list[str], *, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def parse_last_json(text: str) -> dict:
    start = text.rfind("\n{")
    if start >= 0:
        candidate = text[start + 1 :].strip()
    else:
        start = text.find("{")
        candidate = text[start:].strip() if start >= 0 else ""
    if not candidate:
        raise ValueError("no json object in output")
    return json.loads(candidate)


def require_no_secret_shape(payload: dict) -> str | None:
    raw = json.dumps(payload, ensure_ascii=False)
    forbidden = ["sg_cap=", "Authorization", "Bearer ", "설정 {", "C:\\Users\\", "I:\\dev\\", "I:/dev/"]
    for token in forbidden:
        if token in raw:
            return token
    return None


def require_owner_identity_shape(payload: dict, label: str, *, require_owned: bool = True) -> str | None:
    if payload.get("schema") != "seamgrim.workbench_run_archive_lineage.runner_result.v3":
        return f"{label}: schema={payload.get('schema')!r}"
    ownership = payload.get("ownership_basis") or {}
    if ownership.get("strategy") != "pre_stop_process_identity_snapshot":
        return f"{label}: ownership strategy={ownership.get('strategy')!r}"
    if ownership.get("global_process_diff_used") is not False:
        return f"{label}: global process diff used"
    if ownership.get("unrelated_process_termination_allowed") is not False:
        return f"{label}: unrelated termination allowed"
    fields = set(payload.get("process_identity_fields") or [])
    missing = sorted(REQUIRED_IDENTITY_FIELDS - fields)
    if missing:
        return f"{label}: missing identity fields {missing!r}"
    if require_owned and not payload.get("owned_process_identities"):
        return f"{label}: missing owned identity records"
    return None


def require_no_residual(payload: dict, label: str) -> str | None:
    teardown = payload.get("teardown", {})
    if teardown.get("residual_owned_pids"):
        return f"{label}: residual pids {teardown.get('residual_owned_pids')!r}"
    if teardown.get("residual_owned_processes"):
        return f"{label}: residual processes {teardown.get('residual_owned_processes')!r}"
    if teardown.get("residual_owned_sockets"):
        return f"{label}: residual sockets {teardown.get('residual_owned_sockets')!r}"
    return None


def main() -> int:
    required = [
        PACK / "README.md",
        PACK / "input.ddn",
        PACK / "golden.jsonl",
        PACK / "contract.detjson",
        RUNNER,
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_MISSING", json.dumps(missing, ensure_ascii=False))

    contract = json.loads((PACK / "contract.detjson").read_text(encoding="utf-8"))
    expected = {
        "pack": "seamgrim_runner_lifecycle_reliability_v1",
        "runner_instrumentation_change": True,
        "actual_container_claim": False,
        "private_idc_claim": False,
        "new_ddn_syntax": False,
        "state_hash_formula_change": False,
        "docs_ssot_change": False,
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_CONTRACT", f"{key}={contract.get(key)!r}")
    if contract.get("current_gate") not in {"G1", "G2", "G3", "G4"}:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_CONTRACT", f"current_gate={contract.get('current_gate')!r}")
    owner_contract = contract.get("owner_scoped_lifecycle_contract") or {}
    if owner_contract.get("process_identity_required") is not True:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_CONTRACT", "owner process identity is not required")
    if owner_contract.get("pid_only_residual_detection") is not False:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_CONTRACT", "pid-only residual detection is still allowed")

    golden = run([sys.executable, "tests/run_pack_golden.py", "seamgrim_runner_lifecycle_reliability_v1"], timeout=120)
    if golden.returncode:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_PACK", golden.stdout.strip())

    normal = run(["node", str(RUNNER.relative_to(ROOT))], timeout=180)
    if normal.returncode:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_NORMAL", normal.stdout.strip())
    normal_payload = parse_last_json(normal.stdout)
    identity_problem = require_owner_identity_shape(normal_payload, "normal")
    if identity_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_SCHEMA", identity_problem)
    assertions = normal_payload.get("assertions", {})
    for key in [
        "after_save_project_id_present",
        "after_save_head_revision_present",
        "edit_link_project_id_present",
        "edit_link_capability_present",
        "no_projects_double_slash_request",
        "temp_data_dir_removed",
    ]:
        if assertions.get(key) is not True:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_ASSERT", f"{key}={assertions.get(key)!r}")
    residual_problem = require_no_residual(normal_payload, "normal")
    if residual_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_RESIDUAL", residual_problem)
    leaked = require_no_secret_shape(normal_payload)
    if leaked:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_SECRET", leaked)

    expected_failures = {
        "empty-project-id": "E_TEST_PROJECT_ID_EMPTY",
        "no-ready": "E_TEST_SERVER_READY_TIMEOUT",
        "premature-run": "E_TEST_PROJECT_SAVE_PREREQUISITE",
    }
    for mode, code in expected_failures.items():
        proc = run(["node", str(RUNNER.relative_to(ROOT)), "--mode", mode], timeout=180)
        if proc.returncode == 0:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_NEGATIVE_PASS", mode)
        payload = parse_last_json(proc.stdout)
        if payload.get("failure", {}).get("code") != code:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_NEGATIVE_CODE", f"{mode}: {payload.get('failure')!r}")
        identity_problem = require_owner_identity_shape(payload, mode)
        if identity_problem:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_NEGATIVE_IDENTITY", identity_problem)
        residual_problem = require_no_residual(payload, mode)
        if residual_problem:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_NEGATIVE_RESIDUAL", residual_problem)
        leaked = require_no_secret_shape(payload)
        if leaked:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_NEGATIVE_SECRET", f"{mode}: {leaked}")
        if mode == "empty-project-id" and any("/projects//" in row.get("path", "") for row in payload.get("api_requests", [])):
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_DOUBLE_SLASH", "empty project id reached network")

    teardown = run(["node", str(RUNNER.relative_to(ROOT)), "--mode", "teardown-delay"], timeout=180)
    if teardown.returncode:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_TEARDOWN", teardown.stdout.strip())
    teardown_payload = parse_last_json(teardown.stdout)
    if teardown_payload.get("teardown", {}).get("escalated") is not True:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_TEARDOWN_ESCALATION", repr(teardown_payload.get("teardown")))
    identity_problem = require_owner_identity_shape(teardown_payload, "teardown-delay")
    if identity_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_TEARDOWN_IDENTITY", identity_problem)
    residual_problem = require_no_residual(teardown_payload, "teardown-delay")
    if residual_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_TEARDOWN_RESIDUAL", residual_problem)

    pid_reuse = run(["node", str(RUNNER.relative_to(ROOT)), "--mode", "pid-reuse-simulation"], timeout=60)
    if pid_reuse.returncode:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_PID_REUSE", pid_reuse.stdout.strip())
    pid_payload = parse_last_json(pid_reuse.stdout)
    if pid_payload.get("assertions", {}).get("pid_reuse_identity_mismatch_ignored") is not True:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_PID_REUSE_ASSERT", repr(pid_payload.get("assertions")))
    if not pid_payload.get("ignored_reused_pid_identities"):
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_PID_REUSE_IGNORED", repr(pid_payload))

    leak = run(["node", str(RUNNER.relative_to(ROOT)), "--mode", "owned-leak-injection"], timeout=60)
    if leak.returncode == 0:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_LEAK_PASS", leak.stdout.strip())
    leak_payload = parse_last_json(leak.stdout)
    if leak_payload.get("failure", {}).get("code") != "E_TEST_OWNED_PROCESS_RESIDUAL":
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_LEAK_CODE", repr(leak_payload.get("failure")))
    if not leak_payload.get("teardown", {}).get("residual_owned_processes"):
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_LEAK_RESIDUAL", repr(leak_payload.get("teardown")))

    ssot = run(["git", "status", "--short", "--", "docs/ssot"], timeout=60)
    if ssot.returncode or ssot.stdout.strip():
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_OBS_SSOT", ssot.stdout.strip())

    print("[seamgrim-runner-lifecycle-observation] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
