#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORK_DIR = ROOT / "work" / "codex" / "20260710_ganada_intake_audit"
DEFAULT_JUDGEMENTS = DEFAULT_WORK_DIR / "ganada_intake_judgements_v1.detjson"
DEFAULT_ARCHIVE_EXECUTION_RECORD = ROOT / (
    "work/codex/20260711_seamgrim_manim_promotion_governance/"
    "repository_p2a_execution_record_v1.detjson"
)

SOURCE_CATALOG = (
    ("proposal", "docs/context/proposals", "decision"),
    ("context_note", "docs/context/notes", "decision"),
    ("docs_note", "docs/notes", "decision"),
    ("session_delta", "work/_session_deltas", "decision"),
    ("root_ddonirang", "또니랑", "decision"),
    ("ganada_roadmap", "docs/context/roadmap", "decision"),
    ("design", "docs/context/design", "decision"),
    ("brief", "docs/context/briefs", "decision"),
    ("decision", "docs/decisions", "decision"),
    ("request", "docs/context/requests", "decision"),
    ("manuscript", "docs/context/manuscripts", "decision"),
    ("context_report", "docs/context/reports", "evidence"),
    ("report", "docs/reports", "evidence"),
    ("status", "docs/status", "evidence"),
    ("step", "docs/steps", "evidence"),
    ("guide", "docs/guides", "reference"),
    ("studio", "docs/studio", "reference"),
    ("publish", "publish", "reference"),
    ("queue", "docs/context/queue", "reference"),
    ("task", "docs/context/tasks", "reference"),
    ("codex_task", "docs/context/codex_tasks", "reference"),
    ("ticket", "docs/context/tickets", "reference"),
    ("reference", "docs/context/reference", "reference"),
    ("ssot", "docs/ssot/ssot", "authority"),
)

PROFILE_LANES = {
    "decision_sources": {"decision", "authority"},
    "evidence_sources": {"evidence", "authority"},
    "reference_and_artifacts": {"reference", "authority"},
    "all_metadata": {"decision", "evidence", "reference", "authority"},
}

TEXT_SUFFIXES = {
    ".csv",
    ".detjson",
    ".json",
    ".jsonl",
    ".md",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}

FROZEN_TAGS = (
    "declarative_modeling",
    "ai_audit",
    "multilang_curriculum",
    "manim",
    "nurigym_game",
    "freeze",
    "governance",
)

ALLOWED_OVERLAYS = (
    "seamgrim_public_wedge",
    "learning_spine_index",
)

TAG_PATTERNS: dict[str, tuple[str, ...]] = {
    "declarative_modeling": (
        "세움",
        "선언형",
        "modelica",
        "solveplan",
        "prime",
        "막음",
        "막기",
        "다시놓기",
        "미분",
        "ode",
    ),
    "ai_audit": (
        "ai",
        "슬기",
        "world_diff",
        "뜻차이",
        "질문카드",
        "말본카드",
        "gatekeeper",
        "agent_report",
        "teul-mcp",
    ),
    "multilang_curriculum": (
        "교착어",
        "다언어",
        "방언",
        "dialect",
        "한국어",
        "교육",
        "교재",
        "python",
        "rust",
        "javascript",
        "modelica",
    ),
    "manim": (
        "manim",
        "보개마당",
        "scene binding",
        "formula transform",
        "object morph",
        "camera/layer",
    ),
    "nurigym_game": (
        "nurigym",
        "누리짐",
        "gymnasium",
        "게임",
        "rpg",
        "보상",
        "step_record",
    ),
    "freeze": (
        "동결",
        "freeze",
        "reserved",
        "e-code",
        "schema version",
        "출시 전",
    ),
    "governance": (
        "ssot",
        "owner",
        "승인",
        "decision",
        "거버넌스",
        "ledger",
        "장부",
        "open issue",
    ),
}

OVERLAY_PATTERNS: dict[str, tuple[str, ...]] = {
    "seamgrim_public_wedge": (
        "셈그림",
        "seamgrim",
        "wasm",
        "playground",
        "첫 기쁨",
        "물리 차시",
        "온뭉치",
        "보개계획",
    ),
    "learning_spine_index": (
        "학습 줄기",
        "learning spine",
        "교과 연결",
        "교육과정",
        "python/rust/js/modelica",
        "입문 교재",
    ),
}

OI_RE = re.compile(r"\bOI-[A-Z0-9][A-Z0-9-]*\b")
PACK_RE = re.compile(r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+){1,}_v\d+(?:\.\d+)?\b")
SSOT_REF_RE = re.compile(
    r"\b(?:docs/ssot/ssot/)?(?:GATE0|README|SSOT)_[A-Z0-9_]+_v\d+\.\d+\.\d+\.md(?::\d+)?"
)
DATE_FILE_RE = re.compile(r"(?<!\d)(20\d{2})(\d{2})(\d{2})(?!\d)")
DATE_TEXT_RE = re.compile(r"(?<!\d)(20\d{2})-(\d{2})-(\d{2})(?!\d)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^(?:상태|Status)\s*:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)

MANUAL_FIELDS = {
    "source_status",
    "reflection_status",
    "implementation_status",
    "owner_decision",
    "assessment_status",
    "ssot_refs",
    "product_path_refs",
    "verification_evidence",
    "pack_or_equivalent_refs",
    "user_decision_ref",
    "primary_ganada_cells",
    "support_ganada_cells",
    "tags",
    "overlays",
    "next_action",
    "assessment",
    "absence_claim",
    "target_home",
    "superseded_by",
}


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(path: Path, data: bytes) -> str:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return ""
    return data.decode("utf-8-sig", errors="replace")


def extract_date(path: Path, text: str) -> str | None:
    match = DATE_FILE_RE.search(path.name)
    if match is None:
        match = DATE_TEXT_RE.search(text[:4000])
    if match is None:
        return None
    year, month, day = match.groups()
    return f"{year}-{month}-{day}"


def extract_title(path: Path, text: str) -> str:
    match = HEADING_RE.search(text[:20000])
    if match:
        return match.group(1).strip()
    if path.suffix.lower() in {".json", ".detjson"}:
        try:
            payload = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            payload = None
        if isinstance(payload, dict) and isinstance(payload.get("schema"), str):
            return payload["schema"]
    return path.name


def classify_kind(collection: str, path: Path, title: str) -> str:
    upper = f"{path.name} {title}".upper()
    if collection == "ssot":
        return "ssot"
    if "PROPOSAL" in upper or "제안" in title:
        return "proposal"
    if "OPINION" in upper or "의견" in title:
        return "opinion"
    if "HANDOFF" in upper or "인수인계" in title:
        return "handoff"
    if "DAYRUN" in upper or "DEVGOALS" in upper or "목표지시" in title:
        return "work_instruction"
    if "PLAN" in upper or "계획" in title:
        return "plan"
    if "REPORT" in upper or "감사" in title or "보고" in title:
        return "report"
    if "INDEX" in upper or "목차" in title or "색인" in title:
        return "index"
    if path.suffix.lower() != ".md":
        return "data"
    return "note"


def infer_authority_class(collection: str, lane: str) -> str:
    if collection == "ssot":
        return "ssot_candidate_authority"
    if lane == "evidence":
        return "implementation_evidence"
    if lane == "reference":
        return "reference_or_history"
    return "noncanonical_decision_input"


def infer_target_home(collection: str, lane: str) -> str:
    if collection == "ssot":
        return "docs/ssot/** (SSOT manager owned)"
    if collection == "context_report":
        return "docs/reports/{audit|impl|rationalization} (classification required)"
    if collection == "report":
        return "current_path"
    if collection == "session_delta":
        return "work/_session_deltas/{pending|_merged}"
    if collection == "root_ddonirang":
        return "{pending intake|_archive/intake/root_ddonirang}"
    if collection in {"queue", "task", "codex_task", "ticket"}:
        return "{active projection|_archive/task_history}"
    if lane == "decision":
        return "current_path_or_owner_decision"
    if lane == "evidence":
        return "current_evidence_home"
    return "current_reference_home"


def infer_source_status(collection: str, kind: str, title: str, text: str) -> str:
    first_lines = "\n".join(text.splitlines()[:8])
    marker = f"{title}\n{first_lines}".lower()
    if collection == "ssot":
        return "ssot_candidate_source"
    if "흡수됨" in marker or "superseded" in marker or "대체됨" in marker:
        return "superseded_candidate"
    if "draft" in marker or "초안" in marker or "승인 전 실행 금지" in marker:
        return "draft_candidate"
    if kind in {"handoff", "work_instruction"}:
        return "work_instruction"
    if kind in {"data", "index"}:
        return "reference_material"
    return "docs_first_candidate"


def count_patterns(text: str, patterns: tuple[str, ...]) -> int:
    lowered = text.lower()
    count = 0
    for pattern in patterns:
        normalized = pattern.lower()
        if normalized.isascii():
            token = re.compile(
                rf"(?<![a-z0-9_]){re.escape(normalized)}(?![a-z0-9_])",
                re.IGNORECASE,
            )
            count += len(token.findall(lowered))
        else:
            count += lowered.count(normalized)
    return count


def line_anchors(corpus: list[tuple[str, str]], needle: str, limit: int = 8) -> list[str]:
    if not needle:
        return []
    anchors: list[str] = []
    for path, text in corpus:
        for line_number, line in enumerate(text.splitlines(), start=1):
            if needle in line:
                anchors.append(f"{path}:{line_number}")
                if len(anchors) >= limit:
                    return anchors
    return anchors


def load_judgements(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "ddn.ganada.intake_judgements.v1":
        raise ValueError(f"unexpected judgement schema: {payload.get('schema')}")
    if tuple(payload.get("frozen_tags", [])) != FROZEN_TAGS:
        raise ValueError("judgement frozen_tags must match generator")
    if tuple(payload.get("allowed_overlays", [])) != ALLOWED_OVERLAYS:
        raise ValueError("judgement allowed_overlays must match generator")
    entries = payload.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("judgement entries must be an object keyed by path")
    for source_path, override in entries.items():
        if not isinstance(override, dict):
            raise ValueError(f"judgement entry must be an object: {source_path}")
        unknown = set(override) - MANUAL_FIELDS
        if unknown:
            raise ValueError(f"unknown manual fields for {source_path}: {sorted(unknown)}")
    return entries


def validate_entry(entry: dict[str, Any]) -> None:
    path = entry["path"]
    unknown_tags = set(entry.get("tags", [])) - set(FROZEN_TAGS)
    if unknown_tags:
        raise ValueError(f"unknown tags for {path}: {sorted(unknown_tags)}")
    unknown_overlays = set(entry.get("overlays", [])) - set(ALLOWED_OVERLAYS)
    if unknown_overlays:
        raise ValueError(f"unknown overlays for {path}: {sorted(unknown_overlays)}")

    if entry.get("reflection_status") == "reflected":
        refs = entry.get("ssot_refs", [])
        if not refs or not all(
            re.fullmatch(r"docs/ssot/ssot/.+_v24\.12\.9\.md:\d+", ref) for ref in refs
        ):
            raise ValueError(f"reflected entry requires v24.12.9 SSOT file:line refs: {path}")

    if entry.get("implementation_status") == "landed":
        evidence = entry.get("verification_evidence", [])
        kinds = {item.get("kind") for item in evidence if isinstance(item, dict)}
        passed = all(item.get("result") == "PASS" for item in evidence if isinstance(item, dict))
        if (
            not entry.get("product_path_refs")
            or not evidence
            or not passed
            or not kinds.intersection({"runtime", "cli", "browser", "tooling"})
            or not entry.get("pack_or_equivalent_refs")
        ):
            raise ValueError(f"landed entry lacks product PASS evidence: {path}")

    if entry.get("owner_decision") == "confirmed" and not entry.get("user_decision_ref"):
        raise ValueError(f"confirmed owner decision requires a decision ref: {path}")

    absence = entry.get("absence_claim")
    if absence:
        if absence.get("level") not in {"not_found_in_scope", "verified_absent"}:
            raise ValueError(f"invalid absence level: {path}")
        if not absence.get("scope"):
            raise ValueError(f"absence claim requires scope: {path}")
        if absence.get("level") == "verified_absent":
            required = {"command", "aliases_checked", "prior_versions_checked", "independent_review_ref"}
            if not required.issubset(absence):
                raise ValueError(f"verified_absent claim lacks exhaustive evidence: {path}")


def source_roots_for_profile(profile: str) -> tuple[tuple[str, str, str], ...]:
    lanes = PROFILE_LANES[profile]
    return tuple(item for item in SOURCE_CATALOG if item[2] in lanes)


def load_archived_sources(root: Path, record_path: Path) -> set[str]:
    if not record_path.is_file():
        return set()
    payload = json.loads(record_path.read_text(encoding="utf-8"))
    if payload.get("schema") != "ddn.repository_p2a_execution_record.v1":
        raise ValueError("archive execution record schema mismatch")
    archived: set[str] = set()
    for item in payload.get("items", []):
        if item.get("owner_decision") != "confirmed" or item.get("execution_status") != "moved":
            continue
        source = str(item.get("source") or "")
        target = str(item.get("target") or "")
        if source and target and not (root / source).exists() and (root / target).is_file():
            archived.add(source)
    return archived


def build_entries(
    root: Path,
    judgements_path: Path,
    profile: str,
    archived_sources: set[str],
) -> list[dict[str, Any]]:
    raw_sources: list[dict[str, Any]] = []
    ssot_corpus: list[tuple[str, str]] = []

    source_roots = source_roots_for_profile(profile)
    for collection, source_root, lane in source_roots:
        absolute_root = root / source_root
        if not absolute_root.is_dir():
            raise FileNotFoundError(f"missing source root: {source_root}")
        for path in sorted(item for item in absolute_root.rglob("*") if item.is_file()):
            data = path.read_bytes()
            text = read_text(path, data)
            source_path = relpath(path, root)
            item = {
                "collection": collection,
                "consumer_lane": lane,
                "path": source_path,
                "data": data,
                "text": text,
            }
            raw_sources.append(item)
            if collection == "ssot":
                ssot_corpus.append((source_path, text))

    ssot_text = "\n".join(text for _, text in ssot_corpus)
    ssot_oi_ids = set(OI_RE.findall(ssot_text))
    ssot_pack_ids = set(PACK_RE.findall(ssot_text))
    content_hash_counts = Counter(sha256_bytes(item["data"]) for item in raw_sources)
    content_hash_groups: dict[str, list[str]] = defaultdict(list)
    for item in raw_sources:
        content_hash_groups[sha256_bytes(item["data"])].append(item["path"])

    judgements = load_judgements(judgements_path)
    source_paths = {item["path"] for item in raw_sources}
    unknown_judgement_paths = set(judgements) - source_paths - archived_sources
    # A single judgement source feeds every profile. Profile-specific builds
    # ignore judgements owned by other lanes; the full registry still rejects
    # paths that are absent from the complete source catalog.
    if unknown_judgement_paths and profile == "all_metadata":
        raise ValueError(f"judgements reference missing sources: {sorted(unknown_judgement_paths)}")

    entries: list[dict[str, Any]] = []
    for item in raw_sources:
        path = Path(item["path"])
        text = item["text"]
        digest = sha256_bytes(item["data"])
        title = extract_title(path, text)
        kind = classify_kind(item["collection"], path, title)
        oi_ids = sorted(set(OI_RE.findall(text)))
        pack_ids = sorted(set(PACK_RE.findall(text)))
        tag_scores = {tag: count_patterns(text, patterns) for tag, patterns in TAG_PATTERNS.items()}
        tags = sorted(tag for tag, score in tag_scores.items() if score > 0)
        overlay_scores = {
            overlay: count_patterns(text, patterns) for overlay, patterns in OVERLAY_PATTERNS.items()
        }
        overlay_candidates = sorted(overlay for overlay, score in overlay_scores.items() if score > 0)

        filename_anchors = (
            line_anchors(ssot_corpus, path.name)
            if item["collection"] != "ssot" and path.name in ssot_text
            else []
        )
        title_anchors = (
            line_anchors(ssot_corpus, title)
            if item["collection"] != "ssot" and title in ssot_text
            else []
        )
        exact_anchors = sorted(set(filename_anchors + title_anchors))
        shared_oi_ids = sorted(set(oi_ids) & ssot_oi_ids)
        shared_pack_ids = sorted(set(pack_ids) & ssot_pack_ids)
        if item["collection"] == "ssot":
            reflection_status = "source_of_truth"
        elif exact_anchors:
            reflection_status = "reference_found_in_ssot"
        elif shared_oi_ids or shared_pack_ids:
            reflection_status = "anchor_overlap_in_ssot"
        else:
            reflection_status = "not_assessed"

        status_match = STATUS_RE.search(text[:20000])
        declared_date = extract_date(path, text)
        recent_bonus = 5 if declared_date and declared_date >= "2026-07-06" else 0
        priority_score = (
            min(overlay_scores["seamgrim_public_wedge"], 20) * 4
            + min(tag_scores["declarative_modeling"], 20) * 2
            + min(tag_scores["ai_audit"], 20)
            + min(tag_scores["multilang_curriculum"], 20)
            + recent_bonus * 5
        )
        entry: dict[str, Any] = {
            "schema": "ddn.ganada.intake_ledger_entry.v1",
            "source_id": "SRC-" + hashlib.sha256(item["path"].encode("utf-8")).hexdigest()[:16],
            "path": item["path"],
            "collection": item["collection"],
            "consumer_lane": item["consumer_lane"],
            "authority_class": infer_authority_class(item["collection"], item["consumer_lane"]),
            "source_kind": kind,
            "source_status": infer_source_status(item["collection"], kind, title, text),
            "declared_date": declared_date,
            "title": title,
            "declared_status_text": status_match.group(1).strip() if status_match else None,
            "sha256": f"sha256:{digest}",
            "bytes": len(item["data"]),
            "exact_duplicate_group": f"sha256:{digest}" if content_hash_counts[digest] > 1 else None,
            "exact_duplicate_paths": sorted(content_hash_groups[digest]) if content_hash_counts[digest] > 1 else [],
            "oi_ids": oi_ids,
            "pack_ids": pack_ids,
            "declared_ssot_refs": sorted(set(SSOT_REF_RE.findall(text))),
            "ssot_anchor_matches": exact_anchors,
            "shared_ssot_oi_ids": shared_oi_ids,
            "shared_ssot_pack_ids": shared_pack_ids,
            "tag_scores": tag_scores,
            "tags": tags,
            "overlay_candidate_scores": overlay_scores,
            "overlay_candidates": overlay_candidates,
            "overlays": [],
            "priority_score": priority_score,
            "assessment_status": "shallow_scanned",
            "reflection_status": reflection_status,
            "implementation_status": "not_assessed",
            "owner_decision": "pending",
            "ssot_refs": [],
            "product_path_refs": [],
            "verification_evidence": [],
            "pack_or_equivalent_refs": [],
            "user_decision_ref": None,
            "primary_ganada_cells": [],
            "support_ganada_cells": [],
            "next_action": "lazy_deep_review",
            "target_home": infer_target_home(item["collection"], item["consumer_lane"]),
            "superseded_by": None,
            "assessment": None,
            "absence_claim": None,
        }
        override = judgements.get(item["path"])
        if override:
            entry.update(override)
            entry["tags"] = sorted(set(entry.get("tags", [])))
            entry["overlays"] = sorted(set(entry.get("overlays", [])))
            entry["primary_ganada_cells"] = sorted(set(entry.get("primary_ganada_cells", [])))
            entry["support_ganada_cells"] = sorted(set(entry.get("support_ganada_cells", [])))
        validate_entry(entry)
        entries.append(entry)

    return sorted(entries, key=lambda entry: entry["path"])


def build_summary(
    entries: list[dict[str, Any]],
    judgements_path: Path,
    profile: str,
    archived_sources: set[str],
) -> dict[str, Any]:
    duplicate_groups = sorted(
        {
            entry["exact_duplicate_group"]
            for entry in entries
            if entry.get("exact_duplicate_group") is not None
        }
    )
    priority_entries = sorted(
        (entry for entry in entries if entry["collection"] != "ssot"),
        key=lambda entry: (-entry["priority_score"], entry["path"]),
    )[:50]
    return {
        "schema": "ddn.ganada.intake_ledger_summary.v1",
        "profile": profile,
        "source_roots": [source_root for _, source_root, _ in source_roots_for_profile(profile)],
        "frozen_tags": list(FROZEN_TAGS),
        "allowed_overlays": list(ALLOWED_OVERLAYS),
        "judgements_path": relpath(judgements_path, ROOT),
        "archived_source_count": len(archived_sources),
        "source_count": len(entries),
        "collection_counts": dict(sorted(Counter(entry["collection"] for entry in entries).items())),
        "consumer_lane_counts": dict(
            sorted(Counter(entry["consumer_lane"] for entry in entries).items())
        ),
        "authority_class_counts": dict(
            sorted(Counter(entry["authority_class"] for entry in entries).items())
        ),
        "source_kind_counts": dict(sorted(Counter(entry["source_kind"] for entry in entries).items())),
        "source_status_counts": dict(sorted(Counter(entry["source_status"] for entry in entries).items())),
        "reflection_status_counts": dict(
            sorted(Counter(entry["reflection_status"] for entry in entries).items())
        ),
        "implementation_status_counts": dict(
            sorted(Counter(entry["implementation_status"] for entry in entries).items())
        ),
        "owner_decision_counts": dict(sorted(Counter(entry["owner_decision"] for entry in entries).items())),
        "assessment_status_counts": dict(
            sorted(Counter(entry["assessment_status"] for entry in entries).items())
        ),
        "tag_counts": {
            tag: sum(tag in entry["tags"] for entry in entries) for tag in FROZEN_TAGS
        },
        "overlay_counts": {
            overlay: sum(overlay in entry["overlays"] for entry in entries)
            for overlay in ALLOWED_OVERLAYS
        },
        "overlay_candidate_counts": {
            overlay: sum(overlay in entry["overlay_candidates"] for entry in entries)
            for overlay in ALLOWED_OVERLAYS
        },
        "deep_reviewed_count": sum(entry["assessment_status"] == "deep_reviewed" for entry in entries),
        "exact_duplicate_group_count": len(duplicate_groups),
        "exact_duplicate_source_count": sum(bool(entry["exact_duplicate_group"]) for entry in entries),
        "sources_with_ssot_reference_signal": sum(
            entry["reflection_status"] in {"reference_found_in_ssot", "anchor_overlap_in_ssot", "reflected"}
            for entry in entries
        ),
        "top_priority_candidates": [
            {
                "path": entry["path"],
                "priority_score": entry["priority_score"],
                "overlay_candidates": entry["overlay_candidates"],
                "tags": entry["tags"],
                "assessment_status": entry["assessment_status"],
            }
            for entry in priority_entries
        ],
    }


def write_outputs(
    entries: list[dict[str, Any]],
    summary: dict[str, Any],
    out_dir: Path,
    output_prefix: str,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = out_dir / f"{output_prefix}_ledger_v1.jsonl"
    summary_path = out_dir / f"{output_prefix}_summary_v1.detjson"
    ledger_text = "".join(
        json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for entry in entries
    )
    ledger_path.write_text(ledger_text, encoding="utf-8", newline="\n")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Ganada intake ledger V1")
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--judgements", type=Path, default=DEFAULT_JUDGEMENTS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_WORK_DIR)
    parser.add_argument("--profile", choices=sorted(PROFILE_LANES), default="decision_sources")
    parser.add_argument("--output-prefix", default="ganada_intake")
    parser.add_argument(
        "--archive-execution-record",
        type=Path,
        default=DEFAULT_ARCHIVE_EXECUTION_RECORD,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.repo_root.resolve()
    judgements_path = args.judgements.resolve()
    archive_record = args.archive_execution_record.resolve()
    archived_sources = load_archived_sources(root, archive_record)
    entries = build_entries(root, judgements_path, args.profile, archived_sources)
    summary = build_summary(entries, judgements_path, args.profile, archived_sources)
    write_outputs(entries, summary, args.out_dir.resolve(), args.output_prefix)
    print(
        "ganada_intake_ledger_v1: PASS "
        f"profile={args.profile} "
        f"sources={summary['source_count']} "
        f"deep={summary['deep_reviewed_count']} "
        f"duplicates={summary['exact_duplicate_group_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
