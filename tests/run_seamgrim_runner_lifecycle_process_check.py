#!/usr/bin/env python
from __future__ import annotations

import concurrent.futures
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tests" / "seamgrim_workbench_run_archive_lineage_runner.mjs"
SERVER = ROOT / "solutions" / "seamgrim_ui_mvp" / "tools" / "ddn_exec_server.py"
PACK_CONTRACT = ROOT / "pack" / "seamgrim_runner_lifecycle_reliability_v1" / "contract.detjson"
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


def run_node(mode: str = "normal", *, timeout: int = 180) -> tuple[int, dict, str]:
    cmd = ["node", str(RUNNER.relative_to(ROOT))]
    if mode != "normal":
        cmd += ["--mode", mode]
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
    payload = parse_last_json(proc.stdout)
    return proc.returncode, payload, proc.stdout


def parse_last_json(text: str) -> dict:
    start = text.rfind("\n{")
    candidate = text[start + 1 :].strip() if start >= 0 else text[text.find("{") :].strip()
    if not candidate:
        raise ValueError(f"missing json output: {text[-1000:]}")
    return json.loads(candidate)


def check_clean_payload(payload: dict, label: str) -> str | None:
    if payload.get("teardown", {}).get("residual_owned_pids"):
        return f"{label}: residual pids {payload['teardown']['residual_owned_pids']!r}"
    if payload.get("teardown", {}).get("residual_owned_processes"):
        return f"{label}: residual process identities {payload['teardown']['residual_owned_processes']!r}"
    if payload.get("teardown", {}).get("residual_owned_sockets"):
        return f"{label}: residual socket count {payload['teardown']['residual_owned_sockets']!r}"
    if "C:\\Users\\" in json.dumps(payload, ensure_ascii=False):
        return f"{label}: leaked absolute temp path"
    if any("/projects//" in row.get("path", "") for row in payload.get("api_requests", [])):
        return f"{label}: network request included /projects//"
    return None


def require_identity_payload(payload: dict, label: str, *, require_owned: bool = True) -> str | None:
    ownership = payload.get("ownership_basis") or {}
    if ownership.get("strategy") != "pre_stop_process_identity_snapshot":
        return f"{label}: ownership strategy={ownership.get('strategy')!r}"
    if ownership.get("global_process_diff_used") is not False:
        return f"{label}: global process diff was allowed"
    if ownership.get("unrelated_process_termination_allowed") is not False:
        return f"{label}: unrelated process termination was allowed"
    fields = set(payload.get("process_identity_fields") or [])
    missing = sorted(REQUIRED_IDENTITY_FIELDS - fields)
    if missing:
        return f"{label}: missing identity fields {missing!r}"
    if require_owned and not payload.get("owned_process_identities"):
        return f"{label}: missing owned process identity records"
    for row in payload.get("owned_process_identities") or []:
        missing_row = [field for field in REQUIRED_IDENTITY_FIELDS if field not in row]
        if missing_row:
            return f"{label}: owned identity missing {missing_row!r}"
        if row.get("run_owner_id") != payload.get("run_owner_id"):
            return f"{label}: owned identity run_owner_id mismatch"
    return None


def helper_alive(proc: subprocess.Popen[str]) -> bool:
    if proc.poll() is not None:
        return False
    try:
        proc.wait(timeout=0.05)
        return False
    except subprocess.TimeoutExpired:
        return True


def run_unrelated_helper_overlap() -> tuple[int, dict, str]:
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    helper = subprocess.Popen(
        ["node", "-e", "setInterval(() => {}, 1000)"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=flags,
    )
    try:
        time.sleep(0.2)
        code, payload, output = run_node("normal", timeout=240)
        if not helper_alive(helper):
            return 98, payload, "unrelated helper was terminated during runner execution"
        return code, payload, output
    finally:
        if helper_alive(helper):
            helper.terminate()
            try:
                helper.wait(timeout=3)
            except subprocess.TimeoutExpired:
                helper.kill()
                helper.wait(timeout=3)


def main() -> int:
    missing = [path for path in [RUNNER, SERVER, PACK_CONTRACT] if not path.exists()]
    if missing:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_MISSING", ",".join(str(path.relative_to(ROOT)) for path in missing))

    server_text = SERVER.read_text(encoding="utf-8")
    for token in ["SEAMGRIM_SERVER_READY", "server.server_address", "port < 0 or port > 65535"]:
        if token not in server_text:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_SERVER_READY", token)

    runner_text = RUNNER.read_text(encoding="utf-8")
    for token in [
        "requested_port = 0",
        "waitForReadyRecord",
        "actual_bound_port",
        "windowsHide: true",
        "ownership_basis",
        "process_identity_fields",
        "pre_stop_owned_identities",
        "residual_owned_sockets",
        "pid-reuse-simulation",
        "owned-leak-injection",
    ]:
        if token not in runner_text:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_RUNNER_TOKEN", token)
    if "const port = await freePort();" in runner_text:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_TOCTOU", "runner still closes a free port before server bind")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(run_node, "normal", timeout=240) for _ in range(4)]
        rows = [future.result() for future in futures]

    bound_ports: list[int] = []
    owner_ids: set[str] = set()
    for idx, (code, payload, output) in enumerate(rows):
        label = f"parallel-{idx}"
        if code:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_PARALLEL", f"{label}: {output[-2000:]}")
        if payload.get("requested_port") != 0:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_REQUESTED_PORT", f"{label}: {payload.get('requested_port')!r}")
        port = int(payload.get("actual_bound_port") or 0)
        if port <= 0:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_BOUND_PORT", f"{label}: {port!r}")
        bound_ports.append(port)
        owner = str(payload.get("run_owner_id") or "")
        if not owner:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_OWNER", label)
        owner_ids.add(owner)
        assertions = payload.get("assertions", {})
        if assertions.get("temp_data_dir_removed") is not True:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_TEMP", f"{label}: {assertions.get('temp_data_dir_removed')!r}")
        problem = check_clean_payload(payload, label)
        if problem:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_PAYLOAD", problem)
        identity_problem = require_identity_payload(payload, label)
        if identity_problem:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_IDENTITY", identity_problem)
    if len(set(bound_ports)) != len(bound_ports):
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_PORT_COLLISION", repr(bound_ports))
    if len(owner_ids) != 4:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_OWNER_COLLISION", repr(owner_ids))

    expected_failures = {
        "empty-project-id": "E_TEST_PROJECT_ID_EMPTY",
        "premature-run": "E_TEST_PROJECT_SAVE_PREREQUISITE",
        "no-ready": "E_TEST_SERVER_READY_TIMEOUT",
    }
    for mode, expected_code in expected_failures.items():
        code, payload, output = run_node(mode, timeout=180)
        if code == 0:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_NEGATIVE_PASS", f"{mode}: {output[-2000:]}")
        if payload.get("failure", {}).get("code") != expected_code:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_NEGATIVE_CODE", f"{mode}: {payload.get('failure')!r}")
        problem = check_clean_payload(payload, mode)
        if problem:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_NEGATIVE_PAYLOAD", problem)
        identity_problem = require_identity_payload(payload, mode)
        if identity_problem:
            return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_NEGATIVE_IDENTITY", identity_problem)

    code, payload, output = run_node("teardown-delay", timeout=180)
    if code:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_TEARDOWN", output[-2000:])
    if payload.get("teardown", {}).get("escalated") is not True:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_TEARDOWN_ESCALATION", repr(payload.get("teardown")))
    problem = check_clean_payload(payload, "teardown-delay")
    if problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_TEARDOWN_PAYLOAD", problem)
    identity_problem = require_identity_payload(payload, "teardown-delay")
    if identity_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_TEARDOWN_IDENTITY", identity_problem)

    code, payload, output = run_node("pid-reuse-simulation", timeout=60)
    if code:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_PID_REUSE", output[-2000:])
    if payload.get("assertions", {}).get("pid_reuse_identity_mismatch_ignored") is not True:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_PID_REUSE_ASSERT", repr(payload.get("assertions")))
    if not payload.get("ignored_reused_pid_identities"):
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_PID_REUSE_IGNORED", repr(payload))
    identity_problem = require_identity_payload(payload, "pid-reuse-simulation")
    if identity_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_PID_REUSE_IDENTITY", identity_problem)

    code, payload, output = run_node("owned-leak-injection", timeout=60)
    if code == 0:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_LEAK_NEGATIVE_PASS", output[-2000:])
    if payload.get("failure", {}).get("code") != "E_TEST_OWNED_PROCESS_RESIDUAL":
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_LEAK_NEGATIVE_CODE", repr(payload.get("failure")))
    if not payload.get("teardown", {}).get("residual_owned_processes"):
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_LEAK_NEGATIVE_IDENTITY", repr(payload.get("teardown")))
    identity_problem = require_identity_payload(payload, "owned-leak-injection")
    if identity_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_LEAK_IDENTITY", identity_problem)

    code, payload, output = run_unrelated_helper_overlap()
    if code:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_UNRELATED_OVERLAP", output[-2000:])
    problem = check_clean_payload(payload, "unrelated-helper-overlap")
    if problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_UNRELATED_PAYLOAD", problem)
    identity_problem = require_identity_payload(payload, "unrelated-helper-overlap")
    if identity_problem:
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_UNRELATED_IDENTITY", identity_problem)

    ssot = subprocess.run(
        ["git", "status", "--short", "--", "docs/ssot"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    if ssot.returncode or ssot.stdout.strip():
        return fail("E_SEAMGRIM_RUNNER_LIFECYCLE_PROCESS_SSOT", ssot.stdout.strip())

    print("[seamgrim-runner-lifecycle-process] PASS parallel=4 residual_owned=0 owner_identity=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
