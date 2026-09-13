#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "solutions" / "seamgrim_ui_mvp" / "tools"
sys.path.insert(0, str(TOOLS))

from project_store import ProjectValidationError, SCHEMA_VERSION, SeamgrimProjectStore, stable_json  # noqa: E402


BACKUP_MANIFEST_NAME = "backup_manifest.detjson"
BACKUP_MANIFEST_SCHEMA = "seamgrim.private_pilot.backup_manifest.v1"


class BackupError(RuntimeError):
    pass


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(args: list[str], fallback: str) -> str:
    try:
        proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception:
        pass
    return fallback


def ensure_outside(source: Path, target: Path, label: str) -> None:
    source = source.resolve()
    target = target.resolve()
    try:
        target.relative_to(source)
    except ValueError:
        return
    raise BackupError(f"{label} must be outside source data directory")


def object_hashes(objects_dir: Path) -> dict[str, str]:
    if not objects_dir.is_dir():
        raise BackupError("backup objects directory missing")
    rows: dict[str, str] = {}
    for path in sorted(objects_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(objects_dir).as_posix()
        rows[rel] = sha256_file(path)
    return rows


def load_manifest(backup_dir: Path) -> dict[str, Any]:
    path = backup_dir / BACKUP_MANIFEST_NAME
    if not path.is_file():
        raise BackupError("backup manifest missing")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != BACKUP_MANIFEST_SCHEMA:
        raise BackupError("backup manifest schema mismatch")
    return payload


def verify_backup_manifest(backup_dir: Path) -> dict[str, Any]:
    backup_dir = backup_dir.resolve()
    manifest = load_manifest(backup_dir)
    db_path = backup_dir / "seamgrim_projects.sqlite3"
    objects_dir = backup_dir / "objects"
    if not db_path.is_file():
        raise BackupError("backup db missing")
    if not objects_dir.is_dir():
        raise BackupError("backup objects missing")
    if sha256_file(db_path) != manifest.get("db_sha256"):
        raise BackupError("backup db hash mismatch")
    expected_objects = manifest.get("object_sha256")
    if not isinstance(expected_objects, dict) or not expected_objects:
        raise BackupError("backup object hash manifest missing")
    actual_objects = object_hashes(objects_dir)
    if actual_objects != expected_objects:
        raise BackupError("backup object hash mismatch")
    return manifest


def build_manifest(
    *,
    backup_dir: Path,
    source_data_dir: Path,
    backup_result: dict[str, Any],
    source_commit: str,
    release_manifest_sha256: str,
) -> dict[str, Any]:
    db_path = backup_dir / "seamgrim_projects.sqlite3"
    objects_dir = backup_dir / "objects"
    audit = backup_result.get("audit") if isinstance(backup_result.get("audit"), dict) else {}
    return {
        "schema": BACKUP_MANIFEST_SCHEMA,
        "created_at": utc_now_iso(),
        "source_commit": source_commit,
        "source_tree_hash": git_value(["rev-parse", "HEAD^{tree}"], "operator-input-missing"),
        "release_manifest_sha256": release_manifest_sha256,
        "project_store_schema": SCHEMA_VERSION,
        "source_data_dir_redacted": f"<redacted>/{source_data_dir.name}",
        "db_file": db_path.name,
        "db_sha256": sha256_file(db_path),
        "object_sha256": object_hashes(objects_dir),
        "audit_before_backup": audit,
        "integrity_ok": bool(audit.get("ok")),
        "raw_live_db_copy_claim": False,
        "live_restore_automatic": False,
    }


def write_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def create_backup(
    *,
    data_dir: Path,
    backup_dir: Path,
    source_commit: str,
    release_manifest_sha256: str,
    sqlite_synchronous: str,
) -> dict[str, Any]:
    data_dir = data_dir.resolve()
    backup_dir = backup_dir.resolve()
    ensure_outside(data_dir, backup_dir, "backup destination")
    store = SeamgrimProjectStore(data_dir, sqlite_synchronous=sqlite_synchronous)
    backup_result = store.backup_to(backup_dir)
    manifest = build_manifest(
        backup_dir=backup_dir,
        source_data_dir=data_dir,
        backup_result=backup_result,
        source_commit=source_commit,
        release_manifest_sha256=release_manifest_sha256,
    )
    if not manifest["integrity_ok"]:
        raise BackupError("integrity audit failed before backup")
    write_manifest(backup_dir / BACKUP_MANIFEST_NAME, manifest)
    verified = verify_backup_manifest(backup_dir)
    return {
        "schema": "seamgrim.private_pilot.backup_result.v1",
        "status": "PASS",
        "backup_dir": str(backup_dir),
        "manifest": str(backup_dir / BACKUP_MANIFEST_NAME),
        "object_count": len(verified.get("object_sha256", {})),
    }


def restore_check(
    *,
    backup_dir: Path,
    restore_dir: Path,
    sqlite_synchronous: str,
) -> dict[str, Any]:
    backup_dir = backup_dir.resolve()
    restore_dir = restore_dir.resolve()
    if restore_dir.exists() and any(restore_dir.iterdir()):
        raise BackupError("restore target must be empty")
    restore_dir.mkdir(parents=True, exist_ok=True)
    manifest = verify_backup_manifest(backup_dir)
    restored = SeamgrimProjectStore.restore_from_backup(
        backup_dir,
        restore_dir,
        sqlite_synchronous=sqlite_synchronous,
    )
    audit = restored.audit_integrity()
    if not audit.get("ok"):
        raise BackupError("restored integrity audit failed")
    return {
        "schema": "seamgrim.private_pilot.restore_check_result.v1",
        "status": "PASS",
        "backup_manifest": manifest.get("schema"),
        "restore_dir": str(restore_dir),
        "audit_after_restore": audit,
        "live_restore_automatic": False,
    }


def plan_offhost_copy(backup_dir: Path, destination_label: str) -> dict[str, Any]:
    manifest = verify_backup_manifest(backup_dir.resolve())
    return {
        "schema": "seamgrim.private_pilot.offhost_copy_plan.v1",
        "status": "DRY_RUN_ONLY",
        "backup_manifest": BACKUP_MANIFEST_NAME,
        "source_commit": manifest.get("source_commit"),
        "destination_label": destination_label,
        "contains_secret": False,
        "executes_copy": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seamgrim private-pilot backup and empty-target restore tool.")
    sub = parser.add_subparsers(dest="command", required=True)
    backup = sub.add_parser("backup")
    backup.add_argument("--data-dir", required=True)
    backup.add_argument("--backup-dir", required=True)
    backup.add_argument("--source-commit", default=os.environ.get("SEAMGRIM_RELEASE_COMMIT", "operator-input-missing"))
    backup.add_argument(
        "--release-manifest-sha256",
        default=os.environ.get("SEAMGRIM_RELEASE_MANIFEST_SHA256", "operator-input-missing"),
    )
    backup.add_argument("--sqlite-synchronous", default="FULL")

    restore = sub.add_parser("restore-check")
    restore.add_argument("--backup-dir", required=True)
    restore.add_argument("--restore-dir", required=True)
    restore.add_argument("--sqlite-synchronous", default="FULL")

    offhost = sub.add_parser("plan-offhost-copy")
    offhost.add_argument("--backup-dir", required=True)
    offhost.add_argument("--destination-label", default="operator-offhost-target")

    args = parser.parse_args(argv)
    if args.command == "backup":
        result = create_backup(
            data_dir=Path(args.data_dir),
            backup_dir=Path(args.backup_dir),
            source_commit=str(args.source_commit),
            release_manifest_sha256=str(args.release_manifest_sha256),
            sqlite_synchronous=str(args.sqlite_synchronous),
        )
    elif args.command == "restore-check":
        result = restore_check(
            backup_dir=Path(args.backup_dir),
            restore_dir=Path(args.restore_dir),
            sqlite_synchronous=str(args.sqlite_synchronous),
        )
    else:
        result = plan_offhost_copy(Path(args.backup_dir), str(args.destination_label))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BackupError, ProjectValidationError) as exc:
        print(f"E_PRIVATE_PILOT_BACKUP: {exc}", file=sys.stderr)
        raise SystemExit(1)
