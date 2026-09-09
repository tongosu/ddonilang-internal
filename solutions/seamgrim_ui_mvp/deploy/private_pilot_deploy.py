#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
DEPLOY_ROOT = ROOT / "solutions" / "seamgrim_ui_mvp" / "deploy"
sys.path.insert(0, str(DEPLOY_ROOT))

from private_pilot_backup import create_backup  # noqa: E402
from verify_private_pilot_release import ReleaseVerificationError, verify_manifest  # noqa: E402


POINTER_NAME = "current_release.detjson"
POINTER_SCHEMA = "seamgrim.private_pilot.current_release_pointer.v1"


class DeployError(RuntimeError):
    pass


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{time.time_ns()}.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise DeployError(f"{path}: JSON root must be object")
    return payload


def pointer_path(deploy_root: Path) -> Path:
    return deploy_root / POINTER_NAME


def read_pointer(deploy_root: Path) -> dict[str, Any] | None:
    path = pointer_path(deploy_root)
    if not path.is_file():
        return None
    payload = read_json(path)
    if payload.get("schema") != POINTER_SCHEMA:
        raise DeployError("current release pointer schema mismatch")
    return payload


def release_install_dir(deploy_root: Path, release_id: str) -> Path:
    return deploy_root / "releases" / release_id


def copy_release_artifact(manifest_path: Path, target_dir: Path) -> None:
    source_root = manifest_path.resolve().parent
    if target_dir.exists():
        verify_manifest(target_dir / "manifest.detjson")
        return
    tmp_dir = target_dir.with_name(f"{target_dir.name}.tmp.{time.time_ns()}")
    shutil.copytree(source_root, tmp_dir)
    verify_manifest(tmp_dir / "manifest.detjson")
    tmp_dir.replace(target_dir)


def plan_release(manifest_path: Path, deploy_root: Path, data_dir: Path, backup_root: Path) -> dict[str, Any]:
    manifest = verify_manifest(manifest_path)
    release_id = str(manifest.get("release_id"))
    current = read_pointer(deploy_root)
    return {
        "schema": "seamgrim.private_pilot.deploy_plan.v1",
        "status": "PASS",
        "release_id": release_id,
        "source_commit": manifest.get("source_commit"),
        "deploy_root": str(deploy_root.resolve()),
        "data_dir_redacted": f"<redacted>/{data_dir.resolve().name}",
        "backup_root_redacted": f"<redacted>/{backup_root.resolve().name}",
        "current_release_id": current.get("release_id") if current else "",
        "will_change_pointer": not current or current.get("release_id") != release_id,
        "data_restore_included": False,
    }


def apply_release(
    *,
    manifest_path: Path,
    deploy_root: Path,
    data_dir: Path,
    backup_root: Path,
) -> dict[str, Any]:
    manifest = verify_manifest(manifest_path)
    release_id = str(manifest.get("release_id"))
    current = read_pointer(deploy_root)
    if current and current.get("release_id") == release_id:
        return {
            "schema": "seamgrim.private_pilot.deploy_apply_result.v1",
            "status": "PASS",
            "release_id": release_id,
            "idempotent": True,
            "pointer_changed": False,
            "backup_manifest": "",
            "data_restore_included": False,
        }

    installed_dir = release_install_dir(deploy_root, release_id)
    copy_release_artifact(manifest_path, installed_dir)

    backup_dir = backup_root / f"pre-deploy-{release_id}-{int(time.time())}"
    backup = create_backup(
        data_dir=data_dir,
        backup_dir=backup_dir,
        source_commit=str(manifest.get("source_commit") or ""),
        release_manifest_sha256=str(manifest.get("deploy_config_sha256") or ""),
        sqlite_synchronous="FULL",
    )
    pointer = {
        "schema": POINTER_SCHEMA,
        "release_id": release_id,
        "release_dir": str(installed_dir),
        "manifest": str(installed_dir / "manifest.detjson"),
        "source_commit": manifest.get("source_commit"),
        "previous_release": current,
        "last_backup_manifest": backup.get("manifest"),
        "data_restore_included": False,
        "updated_at_unix": int(time.time()),
    }
    write_json_atomic(pointer_path(deploy_root), pointer)
    return {
        "schema": "seamgrim.private_pilot.deploy_apply_result.v1",
        "status": "PASS",
        "release_id": release_id,
        "idempotent": False,
        "pointer_changed": True,
        "backup_manifest": backup.get("manifest"),
        "data_restore_included": False,
    }


def rollback_release(deploy_root: Path) -> dict[str, Any]:
    current = read_pointer(deploy_root)
    if not current:
        raise DeployError("no current release pointer")
    previous = current.get("previous_release")
    if not isinstance(previous, dict) or not previous.get("release_id"):
        raise DeployError("no previous release pointer")
    previous["previous_release"] = None
    previous["rollback_of_release_id"] = current.get("release_id")
    previous["data_restore_included"] = False
    previous["updated_at_unix"] = int(time.time())
    verify_manifest(Path(str(previous.get("manifest"))))
    write_json_atomic(pointer_path(deploy_root), previous)
    return {
        "schema": "seamgrim.private_pilot.deploy_rollback_result.v1",
        "status": "PASS",
        "current_release_id": previous.get("release_id"),
        "rolled_back_from": current.get("release_id"),
        "data_restore_included": False,
    }


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_json(port: int, path: str, origin: str) -> dict[str, Any]:
    deadline = time.time() + 20
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            req = Request(f"http://127.0.0.1:{port}{path}", headers={"Host": "127.0.0.1", "Origin": origin})
            with urlopen(req, timeout=3) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            time.sleep(0.2)
    raise DeployError(f"canary did not become ready: {last_error}")


def verify_current_release(deploy_root: Path, data_dir: Path, *, port: int = 0) -> dict[str, Any]:
    current = read_pointer(deploy_root)
    if not current:
        raise DeployError("no current release pointer")
    release_dir = Path(str(current.get("release_dir"))).resolve()
    manifest = verify_manifest(release_dir / "manifest.detjson")
    if port <= 0:
        port = free_port()
    origin = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUNBUFFERED": "1",
            "SEAMGRIM_DEPLOY_PROFILE": "private-pilot",
            "SEAMGRIM_PROJECT_DATA_DIR": str(data_dir.resolve()),
            "SEAMGRIM_BUILD_DIR": str((data_dir.resolve().parent / "canary-tmp").resolve()),
            "SEAMGRIM_BACKUP_STAGING_DIR": str((data_dir.resolve().parent / "canary-backup").resolve()),
            "SEAMGRIM_LOG_DIR": str((data_dir.resolve().parent / "canary-logs").resolve()),
            "SEAMGRIM_RELEASE_COMMIT": str(manifest.get("source_commit") or ""),
            "SEAMGRIM_RELEASE_MANIFEST_SHA256": str(manifest.get("deploy_config_sha256") or ""),
            "SEAMGRIM_ALLOWED_HOSTS": "127.0.0.1,localhost",
            "SEAMGRIM_ALLOWED_ORIGINS": f"{origin},http://localhost:{port}",
            "SEAMGRIM_PUBLIC_BASE_URL": f"https://127.0.0.1:{port}",
            "SEAMGRIM_DATA_FILESYSTEM": "local",
            "SEAMGRIM_SQLITE_WAL_SAFETY_ATTESTATION": "local-checker-backport-attestation",
            "TEUL_CLI_BIN": str(release_dir / "bin" / ("teul-cli.exe" if os.name == "nt" else "teul-cli")),
        }
    )
    server_path = release_dir / "solutions" / "seamgrim_ui_mvp" / "tools" / "ddn_exec_server.py"
    proc = subprocess.Popen(
        [sys.executable, str(server_path), "--host", "127.0.0.1", "--port", str(port)],
        cwd=release_dir,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        try:
            health = wait_for_json(port, "/api/health", origin)
            readiness = wait_for_json(port, "/api/private/readiness", origin)
        except Exception as exc:
            if proc.poll() is not None:
                stdout, stderr = proc.communicate(timeout=2)
                raise DeployError(
                    f"canary process exited rc={proc.returncode} stdout={stdout[-800:]} stderr={stderr[-800:]}"
                ) from exc
            raise
        if health.get("ok") is not True or readiness.get("ok") is not True:
            raise DeployError(f"canary health/readiness failed: {health} {readiness}")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
    return {
        "schema": "seamgrim.private_pilot.deploy_verify_result.v1",
        "status": "PASS",
        "release_id": current.get("release_id"),
        "health_ok": health.get("ok") is True,
        "readiness_ok": readiness.get("ok") is True,
        "data_restore_included": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seamgrim private-pilot deploy/canary/rollback tool.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "apply"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--release-manifest", required=True)
        cmd.add_argument("--deploy-root", required=True)
        cmd.add_argument("--data-dir", required=True)
        cmd.add_argument("--backup-root", required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--deploy-root", required=True)
    verify.add_argument("--data-dir", required=True)
    verify.add_argument("--port", type=int, default=0)
    rollback = sub.add_parser("rollback")
    rollback.add_argument("--deploy-root", required=True)
    args = parser.parse_args(argv)

    if args.command == "plan":
        result = plan_release(Path(args.release_manifest), Path(args.deploy_root), Path(args.data_dir), Path(args.backup_root))
    elif args.command == "apply":
        result = apply_release(
            manifest_path=Path(args.release_manifest),
            deploy_root=Path(args.deploy_root),
            data_dir=Path(args.data_dir),
            backup_root=Path(args.backup_root),
        )
    elif args.command == "verify":
        result = verify_current_release(Path(args.deploy_root), Path(args.data_dir), port=int(args.port))
    else:
        result = rollback_release(Path(args.deploy_root))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (DeployError, ReleaseVerificationError) as exc:
        print(f"E_PRIVATE_PILOT_DEPLOY: {exc}", file=sys.stderr)
        raise SystemExit(1)
