#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


SCHEMA = "ddn.repository_duplicate_backrefs.v1"
EXECUTION_SCHEMA = "ddn.repository_p2a_execution_manifest.v1"
DEFAULT_EXECUTION_RECORD = Path(
    "work/codex/20260711_seamgrim_manim_promotion_governance/"
    "repository_p2a_execution_record_v1.detjson"
)
MAX_TEXT_BYTES = 8 * 1024 * 1024
EXPLICIT_ARCHIVE_CANDIDATES = (
    ("root_ddonirang", "또니랑/CLAUDE_OPINION_20260709_AI친화_탁월성_설계의견_V1.md"),
    ("root_ddonirang", "또니랑/CLAUDE_OPINION_20260709_STDLIB_MAXSET_PART0_총괄지도_V1.md"),
    ("root_ddonirang", "또니랑/CLAUDE_OPINION_20260709_STDLIB_MAXSET_PART1_수학자료글_V1.md"),
    ("root_ddonirang", "또니랑/CLAUDE_OPINION_20260709_STDLIB_MAXSET_PART2_통계공간도메인_V1.md"),
    ("root_ddonirang", "또니랑/CLAUDE_OPINION_20260709_교육선언시뮬_충분성점검_6공백_V1.md"),
    ("root_ddonirang", "또니랑/CLAUDE_OPINION_20260710_AI시대_언어의의_두기둥_V1.md"),
    ("root_ddonirang", "또니랑/CLAUDE_OPINION_20260710_보개_다섯층사다리_설계의견_V1.md"),
    ("root_ddonirang", "또니랑/CLAUDE_PLAN_20260710_온뭉치_100세계_말뭉치_기획안_V1.md"),
    ("session_delta", "work/_session_deltas/20260711_codex_korean_manim_reactive_knowledge_scene_v2.md"),
    ("session_delta", "work/_session_deltas/20260710_codex_seamgrim_ui_v2_screen_plan.md"),
    ("session_delta", "work/_session_deltas/20260711_codex_seamgrim_product_to_korean_manim_vertical.md"),
    ("session_delta", "work/_session_deltas/20260711_codex_korean_manim_wave1t_trace_evaluator.md"),
    ("session_delta", "work/_session_deltas/20260711_codex_seamgrim_wave2a_live_semantic_lesson.md"),
    ("session_delta", "work/_session_deltas/20260711_codex_seamgrim_wave2b_authoring_deploy_vertical.md"),
    ("session_delta", "work/_session_deltas/20260711_codex_wave2a_runtime_role_boundary_fix.md"),
)
GENERATED_PREFIXES = (
    "work/codex/20260711_repository_structure_registry/",
    "work/codex/20260711_seamgrim_manim_promotion_governance/",
    "work/claude/20260711_seamgrim_promotion_and_p2_review/",
)
GENERATED_PATHS = {
    "docs/reports/rationalization/REPOSITORY_STRUCTURE_P2_MOVE_PLAN_V1_20260711.md",
    "work/_session_deltas/20260711_codex_seamgrim_manim_promotion_governance.md",
}
LINK_TARGET_RE = re.compile(r"\(([^)]+)\)|`([^`]+)`")


@dataclass(frozen=True)
class Source:
    path: str
    sha256: str
    duplicate_group: str


@dataclass
class References:
    exact: list[str]
    relative_links: list[str]
    plain_mentions: list[str]

    @property
    def direct(self) -> list[str]:
        return sorted(set(self.exact + self.relative_links))


def normalize(value: str) -> str:
    return Path(value.replace("\\", "/")).as_posix().lstrip("./")


def load_registry(path: Path) -> list[dict[str, object]]:
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def load_texts(root: Path, entries: list[dict[str, object]]) -> dict[str, str]:
    texts: dict[str, str] = {}
    for entry in entries:
        rel = normalize(str(entry["path"]))
        if rel in GENERATED_PATHS or any(rel.startswith(prefix) for prefix in GENERATED_PREFIXES):
            continue
        path = root / rel
        try:
            if not path.is_file() or path.stat().st_size > MAX_TEXT_BYTES:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "\x00" not in text:
            texts[rel] = text
    return texts


def resolve_target(referrer: str, raw_target: str) -> str | None:
    target = raw_target.split("#", 1)[0].strip().strip("<>")
    if not target or re.match(r"^[a-z]+://", target, flags=re.IGNORECASE):
        return None
    if target.startswith("/"):
        return normalize(target[1:])
    return normalize(str(Path(referrer).parent / target))


def collect_references(
    member: str,
    group_paths: set[str],
    texts: dict[str, str],
) -> References:
    basename = Path(member).name
    exact: list[str] = []
    relative: list[str] = []
    plain: list[str] = []
    for referrer, text in texts.items():
        if referrer == member:
            continue
        if member in text:
            exact.append(referrer)
        if basename not in text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if basename not in line:
                continue
            resolved_group_target = False
            resolved_member = False
            for match in LINK_TARGET_RE.finditer(line):
                raw_target = match.group(1) or match.group(2) or ""
                if basename not in raw_target:
                    continue
                resolved = resolve_target(referrer, raw_target)
                if resolved in group_paths:
                    resolved_group_target = True
                if resolved == member:
                    relative.append(f"{referrer}:{line_number}")
                    resolved_member = True
            if not resolved_member and not resolved_group_target and member not in line:
                plain.append(f"{referrer}:{line_number}")
    return References(
        exact=sorted(set(exact)),
        relative_links=sorted(set(relative)),
        plain_mentions=sorted(set(plain)),
    )


def authority_weight(referrer: str) -> int:
    if referrer.startswith("docs/ssot/"):
        return 1000
    if referrer in {"AGENTS.md", "AGENT_WORKFLOW.md", "SSOT_POLICY.md", "ARTIFACT_POLICY.md"}:
        return 500
    if referrer.startswith("docs/decisions/") or referrer.startswith("docs/status/"):
        return 100
    if referrer.startswith(("docs/guides/", "docs/studio/", "docs/context/roadmap/")):
        return 30
    if referrer.startswith(("docs/reports/", "docs/context/")):
        return 10
    return 1


def semantic_home_score(path: str) -> int:
    score = 100
    if path.startswith("docs/context/tasks/"):
        score -= 40
    if path.startswith("docs/context/codex_tasks/"):
        score += 30
    if path.startswith("docs/context/notes/"):
        score -= 35
    if path.startswith("docs/notes/"):
        score += 25
    if path.startswith("docs/context/reference/"):
        score -= 30
    if path.startswith("docs/context/design/"):
        score += 10
    if path.startswith("docs/context/proposals/"):
        score -= 20
    if path.startswith(("docs/context/roadmap/", "docs/studio/")):
        score += 10
    if "PROPOSAL_DOCMGMT_pack_studio" in path:
        score += 20
    if "PROPOSAL_PACK_studio" in path:
        score -= 20
    return score


def representative_key(source: Source, refs: References) -> tuple[object, ...]:
    copy_name = bool(re.search(r" \(1\)\.md$", source.path))
    weighted = sum(authority_weight(ref.split(":", 1)[0]) for ref in refs.direct)
    return (
        copy_name,
        -weighted,
        -len(refs.direct),
        semantic_home_score(source.path),
        len(source.path),
        source.path,
    )


def archive_target(source: str) -> str:
    safe = re.sub(r'[:*?"<>|]', "_", source)
    return f"_archive/duplicates/20260711/{safe}"


def explicit_archive_target(category: str, source: str) -> str:
    name = Path(source).name
    if category == "root_ddonirang":
        return f"_archive/intake/또니랑/202607/{name}"
    date_match = re.match(r"work/_session_deltas/(\d{8})_", source)
    date = date_match.group(1) if date_match else "undated"
    return f"_archive/work/session_deltas/{date}/{name}"


def build_explicit_archive_items(
    root: Path,
    texts: dict[str, str],
    executed_sources: set[str],
) -> tuple[list[dict[str, object]], list[str]]:
    items: list[dict[str, object]] = []
    missing: list[str] = []
    for category, raw_source in EXPLICIT_ARCHIVE_CANDIDATES:
        source = normalize(raw_source)
        if not (root / source).is_file():
            if source in executed_sources:
                continue
            missing.append(source)
            continue
        refs = collect_references(source, {source}, texts)
        if refs.direct:
            status = "blocked_rewrite_required"
        elif refs.plain_mentions:
            status = "needs_manual_context_review"
        else:
            status = "clear_no_detected_refs"
        items.append(
            {
                "category": category,
                "source": source,
                "target": explicit_archive_target(category, source),
                "reverse_ref_status": status,
                "redirect_plan": (
                    "move_after_owner_approval"
                    if status == "clear_no_detected_refs"
                    else "rewrite_refs_or_leave_redirect_stub_before_move"
                ),
                "owner_decision": "pending",
                "execution_status": "planned_not_moved",
                "exact_path_refs": refs.exact,
                "resolved_source_link_refs": refs.relative_links,
                "unresolved_mentions": refs.plain_mentions,
            }
        )
    items.sort(key=lambda item: (str(item["category"]), str(item["source"])))
    return items, sorted(missing)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def build_execution_manifest(
    root: Path,
    duplicate_rows: list[dict[str, object]],
    archive_items: list[dict[str, object]],
) -> dict[str, object]:
    items: list[dict[str, object]] = []
    for row in duplicate_rows:
        if not str(row["reverse_ref_status"]).startswith("clear_"):
            continue
        items.append(
            {
                "category": "exact_duplicate",
                "source": row["source"],
                "target": row["target"],
                "sha256": row["sha256"],
                "representative": row["representative"],
                "reason": row["reason"],
                "reverse_ref_status": row["reverse_ref_status"],
                "redirect_plan": row["redirect_plan"],
                "owner_decision": "pending",
                "execution_status": "planned_not_moved",
                "rollback": row["rollback"],
            }
        )
    for row in archive_items:
        if row["reverse_ref_status"] != "clear_no_detected_refs":
            continue
        source = str(row["source"])
        items.append(
            {
                "category": row["category"],
                "source": source,
                "target": row["target"],
                "sha256": sha256_file(root / source),
                "representative": None,
                "reason": "reviewed_archive_candidate_with_no_detected_backrefs",
                "reverse_ref_status": row["reverse_ref_status"],
                "redirect_plan": row["redirect_plan"],
                "owner_decision": "pending",
                "execution_status": "planned_not_moved",
                "rollback": "move target back to source",
            }
        )

    items.sort(key=lambda item: (str(item["category"]), str(item["source"])))
    targets = [str(item["target"]) for item in items]
    target_collisions = sorted(
        target for target, count in Counter(targets).items() if count > 1
    )
    for item in items:
        source = root / str(item["source"])
        target = root / str(item["target"])
        item["preconditions"] = {
            "source_exists": source.is_file(),
            "target_absent": not target.exists(),
            "sha256_matches": source.is_file()
            and sha256_file(source) == str(item["sha256"]),
            "user_approval_required": True,
            "latest_registry_recheck_required": True,
        }
        item["postconditions"] = {
            "source_absent": True,
            "target_exists": True,
            "target_sha256_matches": True,
            "registry_regenerated": True,
            "link_check_passed": True,
        }

    return {
        "schema": EXECUTION_SCHEMA,
        "generated_on": "2026-07-11",
        "authority": "execution_plan_not_move_authorization",
        "candidate_count": len(items),
        "target_collisions": target_collisions,
        "all_owner_decisions_pending": all(
            item["owner_decision"] == "pending" for item in items
        ),
        "all_execution_statuses_planned": all(
            item["execution_status"] == "planned_not_moved" for item in items
        ),
        "items": items,
    }


def build_plan(
    root: Path,
    registry_path: Path,
    executed_sources: set[str],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    entries = load_registry(registry_path)
    texts = load_texts(root, entries)
    groups: dict[str, list[Source]] = defaultdict(list)
    for entry in entries:
        if normalize(str(entry["path"])) in executed_sources:
            continue
        group = entry.get("exact_duplicate_group")
        if group:
            groups[str(group)].append(
                Source(
                    path=normalize(str(entry["path"])),
                    sha256=str(entry["sha256"]),
                    duplicate_group=str(group),
                )
            )

    rows: list[dict[str, object]] = []
    details: list[dict[str, object]] = []
    for group, members in sorted(groups.items()):
        group_paths = {member.path for member in members}
        refs = {
            member.path: collect_references(member.path, group_paths, texts)
            for member in members
        }
        representative = min(members, key=lambda item: representative_key(item, refs[item.path]))
        representative_refs = refs[representative.path]
        for member in sorted(members, key=lambda item: item.path):
            if member.path == representative.path:
                continue
            member_refs = refs[member.path]
            if member_refs.direct:
                status = "blocked_rewrite_required"
            elif member_refs.plain_mentions:
                status = "needs_manual_context_review"
            elif representative_refs.direct:
                status = "clear_refs_resolve_to_representative"
            else:
                status = "clear_no_detected_refs"
            row = {
                "duplicate_group": group,
                "source": member.path,
                "target": archive_target(member.path),
                "representative": representative.path,
                "sha256": member.sha256,
                "reason": "exact_byte_duplicate",
                "reverse_ref_status": status,
                "redirect_plan": (
                    "representative_index_note"
                    if status.startswith("clear_")
                    else "rewrite_or_review_refs_before_move"
                ),
                "owner_decision": "pending",
                "execution_status": "planned_not_moved",
                "rollback": "move target back to source and restore index reference",
                "exact_path_ref_count": len(member_refs.exact),
                "resolved_source_link_count": len(member_refs.relative_links),
                "unresolved_mention_count": len(member_refs.plain_mentions),
                "reference_examples": ";".join(
                    (member_refs.direct + member_refs.plain_mentions)[:8]
                ),
            }
            rows.append(row)
            details.append(
                {
                    "duplicate_group": group,
                    "source": member.path,
                    "representative": representative.path,
                    "representative_authority_score": sum(
                        authority_weight(ref.split(":", 1)[0])
                        for ref in representative_refs.direct
                    ),
                    "sha256": member.sha256,
                    "reverse_ref_status": status,
                    "exact_path_refs": member_refs.exact,
                    "resolved_source_link_refs": member_refs.relative_links,
                    "unresolved_mentions": member_refs.plain_mentions,
                }
            )

    rows.sort(key=lambda item: (str(item["duplicate_group"]), str(item["source"])))
    details.sort(key=lambda item: (str(item["duplicate_group"]), str(item["source"])))
    status_counts = Counter(str(item["reverse_ref_status"]) for item in details)
    archive_items, missing_archive_candidates = build_explicit_archive_items(
        root,
        texts,
        executed_sources,
    )
    archive_status_counts = Counter(
        str(item["reverse_ref_status"]) for item in archive_items
    )
    payload = {
        "schema": SCHEMA,
        "generated_on": "2026-07-11",
        "authority": "audit_artifact_not_move_authorization",
        "representative_policy": "copy-name-guard_then_authority-weighted-direct-refs_then-semantic-home",
        "scan_scope": "source_registry_text_files_excluding_generated_current_p2_outputs",
        "executed_source_count": len(executed_sources),
        "scanned_source_count": len(texts),
        "group_count": len(groups),
        "candidate_count": len(details),
        "status_counts": dict(sorted(status_counts.items())),
        "items": details,
        "explicit_archive_candidate_count": len(archive_items),
        "explicit_archive_status_counts": dict(sorted(archive_status_counts.items())),
        "missing_explicit_archive_candidates": missing_archive_candidates,
        "explicit_archive_items": archive_items,
    }
    return rows, payload


def write_outputs(
    rows: list[dict[str, object]],
    payload: dict[str, object],
    execution_manifest: dict[str, object],
    out_dir: Path,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "repository_duplicate_p2_move_table_v1.csv"
    json_path = out_dir / "repository_duplicate_backrefs_v1.detjson"
    fieldnames = list(rows[0]) if rows else []
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with json_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
    execution_path = out_dir / "repository_p2a_execution_manifest_v1.detjson"
    with execution_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(
                execution_manifest,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a reference-aware duplicate archive move plan")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("work/codex/20260711_repository_structure_registry/repository_source_registry_ledger_v1.jsonl"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("work/codex/20260711_seamgrim_manim_promotion_governance"),
    )
    parser.add_argument(
        "--execution-record",
        type=Path,
        default=DEFAULT_EXECUTION_RECORD,
    )
    args = parser.parse_args()
    root = args.repo_root.resolve()
    registry = args.registry if args.registry.is_absolute() else root / args.registry
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    execution_record = (
        args.execution_record
        if args.execution_record.is_absolute()
        else root / args.execution_record
    )
    executed_sources: set[str] = set()
    if execution_record.is_file():
        record = json.loads(execution_record.read_text(encoding="utf-8"))
        if record.get("schema") != "ddn.repository_p2a_execution_record.v1":
            raise ValueError("repository_p2a_execution_record_schema_mismatch")
        executed_sources = {
            normalize(str(item["source"]))
            for item in record.get("items", [])
            if item.get("owner_decision") == "confirmed"
            and item.get("execution_status") == "moved"
        }
    rows, payload = build_plan(root, registry, executed_sources)
    execution_manifest = build_execution_manifest(
        root,
        rows,
        list(payload["explicit_archive_items"]),
    )
    write_outputs(rows, payload, execution_manifest, out_dir)
    print(
        "repository_duplicate_move_plan_v1: PASS "
        f"groups={payload['group_count']} candidates={payload['candidate_count']} "
        f"statuses={payload['status_counts']} "
        f"explicit_archive_candidates={payload['explicit_archive_candidate_count']} "
        f"archive_statuses={payload['explicit_archive_status_counts']} "
        f"p2a_candidates={execution_manifest['candidate_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
