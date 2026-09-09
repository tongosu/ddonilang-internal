#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL_TEXT = "P2-A 15개 이동을 승인합니다."
MANIFEST = ROOT / (
    "work/codex/20260711_seamgrim_manim_promotion_governance/"
    "repository_p2a_execution_manifest_v1.detjson"
)
RECORD = ROOT / (
    "work/codex/20260711_seamgrim_manim_promotion_governance/"
    "repository_p2a_execution_record_v1.detjson"
)
REGISTRY = ROOT / (
    "work/codex/20260711_repository_structure_registry/"
    "repository_source_registry_ledger_v1.jsonl"
)
GOVERNANCE_PREFIXES = (
    "work/codex/20260711_repository_structure_registry/",
    "work/codex/20260711_repository_structure_p2b/",
    "work/codex/20260711_seamgrim_manim_promotion_governance/",
    "work/claude/20260711_repository_p2a_rereview/",
    "work/claude/20260711_seamgrim_promotion_and_p2_review/",
)
GOVERNANCE_PATHS = {
    "docs/reports/rationalization/REPOSITORY_STRUCTURE_P2_MOVE_PLAN_V1_20260711.md",
    "work/_session_deltas/20260711_codex_seamgrim_manim_promotion_governance.md",
}


def sha256_bytes(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def within(path: Path, parent: Path) -> bool:
    return os.path.commonpath([str(path), str(parent)]) == str(parent)


def resolve_relative(root: Path, value: object) -> Path:
    raw = str(value or "").replace("\\", "/")
    candidate = Path(raw)
    if not raw or candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe_relative_path:{raw}")
    resolved = (root / candidate).resolve()
    if not within(resolved, root):
        raise ValueError(f"path_outside_repo:{raw}")
    return resolved


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"json_object_required:{path}")
    return payload


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    temp.replace(path)


def validate_manifest(root: Path, manifest_path: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    manifest = load_json(manifest_path)
    if manifest.get("schema") != "ddn.repository_p2a_execution_manifest.v1":
        raise ValueError("execution_manifest_schema_mismatch")
    items = list(manifest.get("items", []))
    if manifest.get("candidate_count") != 15 or len(items) != 15:
        raise ValueError(f"execution_manifest_expected_15:{len(items)}")
    categories = [str(item.get("category")) for item in items]
    if categories.count("exact_duplicate") != 11:
        raise ValueError("execution_manifest_exact_duplicate_count")
    if categories.count("root_ddonirang") != 3:
        raise ValueError("execution_manifest_root_ddonirang_count")
    if categories.count("session_delta") != 1:
        raise ValueError("execution_manifest_session_delta_count")
    if manifest.get("target_collisions") != []:
        raise ValueError("execution_manifest_target_collision")

    archive_root = (root / "_archive").resolve()
    seen_targets: set[Path] = set()
    for item in items:
        if item.get("owner_decision") != "pending":
            raise ValueError(f"unexpected_owner_state:{item.get('source')}")
        if item.get("execution_status") != "planned_not_moved":
            raise ValueError(f"unexpected_execution_state:{item.get('source')}")
        if not str(item.get("reverse_ref_status", "")).startswith("clear_"):
            raise ValueError(f"unclear_reverse_ref:{item.get('source')}")
        source = resolve_relative(root, item.get("source"))
        target = resolve_relative(root, item.get("target"))
        if within(source, (root / "docs/ssot").resolve()):
            raise ValueError(f"ssot_source_forbidden:{item.get('source')}")
        if not within(target, archive_root):
            raise ValueError(f"archive_target_required:{item.get('target')}")
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"source_file_required:{item.get('source')}")
        if target.exists() or target in seen_targets:
            raise ValueError(f"target_must_be_absent_unique:{item.get('target')}")
        seen_targets.add(target)
        if sha256_file(source) != item.get("sha256"):
            raise ValueError(f"source_sha256_mismatch:{item.get('source')}")
        representative = item.get("representative")
        if representative:
            representative_path = resolve_relative(root, representative)
            if not representative_path.is_file():
                raise ValueError(f"representative_missing:{representative}")
            if sha256_file(representative_path) != item.get("sha256"):
                raise ValueError(f"representative_sha256_mismatch:{representative}")
    return manifest, items


def execute(root: Path, manifest_path: Path, record_path: Path, approval: str) -> int:
    if approval != APPROVAL_TEXT:
        raise ValueError("exact_user_approval_required")
    if record_path.exists():
        raise ValueError(f"execution_record_already_exists:{record_path}")
    manifest, items = validate_manifest(root, manifest_path)
    moved: list[tuple[Path, Path]] = []
    try:
        for item in items:
            source = resolve_relative(root, item["source"])
            target = resolve_relative(root, item["target"])
            target.parent.mkdir(parents=True, exist_ok=True)
            source.replace(target)
            moved.append((source, target))

        record_items: list[dict[str, object]] = []
        for item in items:
            source = resolve_relative(root, item["source"])
            target = resolve_relative(root, item["target"])
            digest = sha256_file(target)
            if source.exists() or not target.is_file() or digest != item["sha256"]:
                raise ValueError(f"post_move_verification_failed:{item['source']}")
            record_items.append(
                {
                    **item,
                    "owner_decision": "confirmed",
                    "execution_status": "moved",
                    "postconditions": {
                        "source_absent": True,
                        "target_exists": True,
                        "target_sha256_matches": True,
                    },
                }
            )
        record = {
            "schema": "ddn.repository_p2a_execution_record.v1",
            "authority": "user_approved_archive_execution_record",
            "approval_text": approval,
            "executed_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_manifest": manifest_path.relative_to(root).as_posix(),
            "source_manifest_sha256": sha256_file(manifest_path),
            "candidate_count": len(record_items),
            "verification": {
                "active_plan_excludes_sources": False,
                "finalized": False,
                "link_check_passed": False,
                "registry_regenerated": False,
            },
            "items": record_items,
        }
        write_json_atomic(record_path, record)
    except Exception:
        if record_path.exists():
            record_path.unlink()
        for source, target in reversed(moved):
            if target.exists() and not source.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                target.replace(source)
        raise
    print(f"repository_p2a_execute_v1: MOVED count={len(items)}")
    return 0


def finalize(root: Path, record_path: Path, registry_path: Path, manifest_path: Path) -> int:
    record = load_json(record_path)
    if record.get("schema") != "ddn.repository_p2a_execution_record.v1":
        raise ValueError("execution_record_schema_mismatch")
    registry_text = registry_path.read_text(encoding="utf-8")
    active_entries = [
        json.loads(line)
        for line in registry_text.splitlines()
        if line.strip()
    ]
    active_manifest = load_json(manifest_path)
    active_sources = {str(item.get("source")) for item in active_manifest.get("items", [])}
    for item in record.get("items", []):
        source_text = str(item["source"])
        source = resolve_relative(root, source_text)
        target = resolve_relative(root, item["target"])
        if source.exists() or not target.is_file():
            raise ValueError(f"execution_record_move_state_invalid:{source_text}")
        if sha256_file(target) != item["sha256"]:
            raise ValueError(f"execution_record_target_sha_invalid:{source_text}")
        if source_text in registry_text:
            raise ValueError(f"executed_source_still_in_registry:{source_text}")
        if source_text in active_sources:
            raise ValueError(f"executed_source_reproposed:{source_text}")
        source_name = Path(source_text).name
        representative_name = Path(str(item.get("representative") or "")).name
        check_basename = item.get("category") != "exact_duplicate" or source_name != representative_name
        for entry in active_entries:
            active_rel = str(entry.get("path") or "")
            if active_rel in GOVERNANCE_PATHS or any(
                active_rel.startswith(prefix) for prefix in GOVERNANCE_PREFIXES
            ):
                continue
            active_path = root / active_rel
            if not active_path.is_file() or active_path.stat().st_size > 8 * 1024 * 1024:
                continue
            try:
                active_text = active_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if source_text in active_text:
                raise ValueError(
                    f"executed_source_path_still_referenced:{source_text}:{entry.get('path')}"
                )
            if check_basename and source_name in active_text:
                raise ValueError(
                    f"executed_source_name_still_referenced:{source_name}:{entry.get('path')}"
                )
    record["verification"] = {
        "active_plan_excludes_sources": True,
        "finalized": True,
        "link_check_passed": True,
        "registry_regenerated": True,
    }
    record["finalized_at_utc"] = datetime.now(timezone.utc).isoformat()
    write_json_atomic(record_path, record)
    print(f"repository_p2a_execute_v1: FINALIZED count={record['candidate_count']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute or finalize the approved P2-A archive batch")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--record", type=Path, default=RECORD)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--approval", default="")
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    manifest = args.manifest if args.manifest.is_absolute() else root / args.manifest
    record = args.record if args.record.is_absolute() else root / args.record
    registry = args.registry if args.registry.is_absolute() else root / args.registry
    if args.finalize:
        return finalize(root, record, registry, manifest)
    return execute(root, manifest, record, args.approval)


if __name__ == "__main__":
    raise SystemExit(main())
