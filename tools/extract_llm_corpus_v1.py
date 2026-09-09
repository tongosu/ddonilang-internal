#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


FALLBACK_GRAMMAR_CARDS = [
    {
        "id": "grammar.runtime_status",
        "title": "grammar manifest runtime_status",
        "text": "runtime_status values are implemented, partial, designed, reserved.",
        "source": "tests/run_grammar_manifest_operation_check.py",
    },
    {
        "id": "grammar.output",
        "title": "보여주기 output statement",
        "text": "`값 보여주기.` emits a visible output line in many pack golden cases.",
        "source": "pack/*/golden.jsonl",
    },
    {
        "id": "grammar.pack_golden",
        "title": "pack golden contract",
        "text": "D-PACK golden rows fix command, expected stdout or expected metadata, and exit code.",
        "source": "tests/run_pack_golden.py",
    },
]

SSOT_TERM_CARDS = [
    {
        "id": "ssot_term.state_hash_boundary",
        "term": "state_hash",
        "title": "state_hash boundary",
        "text": "state_hash remains the runtime state truth and is not replaced by settings, view, trace, or 보개 hashes.",
        "source": "docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md",
    },
    {
        "id": "ssot_term.run_config_hash",
        "term": "run_config_hash",
        "title": "run_config_hash",
        "text": "run_config_hash is a candidate recording-layer digest for result-affecting settings, not a runtime state hash input.",
        "source": "docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V2_20260707.md",
    },
    {
        "id": "ssot_term.action_status",
        "term": "action_status",
        "title": "Nuri action_status",
        "text": "action_status values are 맞음, 가만히, 잘림, 거부; reject is excluded before merge but can remain visible to reward design.",
        "source": "pack/nurigym_shared_sync_action_pipeline_v1/contract.detjson",
    },
    {
        "id": "ssot_term.seulgi_no_authority",
        "term": "슬기 no-authority",
        "title": "Seulgi no-authority until sealed artifact",
        "text": "AI proposal text has no execution authority until a gate accepts it and a sealed artifact is produced.",
        "source": "pack/seulgi_gatekeeper_v1/contract.detjson",
    },
    {
        "id": "ssot_term.bogae_hash",
        "term": "bogae_hash",
        "title": "bogae_hash",
        "text": "bogae_hash is a payload or DrawList hash candidate; pixel hash is not treated as semantic truth.",
        "source": "pack/std_bogae_graph2d_v1/contract.detjson",
    },
]


def default_grammar_manifest_path() -> Path:
    return ROOT / "docs" / "ssot" / "pack" / "lang_grammar_capability_manifest_v1" / "expected" / "manifest.sample.detjson"


def default_out_path() -> Path:
    for base in (Path("I:/home/urihanl/ddn/codex/out"), Path("C:/ddn/codex/out"), ROOT / "out"):
        try:
            base.mkdir(parents=True, exist_ok=True)
            return base / "llm_corpus_v1.jsonl"
        except OSError:
            continue
    fallback = ROOT / "out"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback / "llm_corpus_v1.jsonl"


def read_text(path: Path, *, max_chars: int = 4000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except FileNotFoundError:
        return ""


def first_paragraph(markdown: str) -> str:
    lines = markdown.splitlines()
    chunks: list[str] = []
    started = False
    for line in lines:
        text = line.strip()
        if not text:
            if started:
                break
            continue
        if text.startswith("#"):
            continue
        started = True
        chunks.append(text)
    return " ".join(chunks).strip()


def compact_code(text: str, *, max_lines: int = 24) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    useful = [line for line in lines if line.strip()]
    return "\n".join(useful[:max_lines]).strip()


def load_first_golden_row(path: Path) -> dict:
    text = read_text(path, max_chars=12000)
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        return row if isinstance(row, dict) else {}
    return {}


def load_contract(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def grammar_cards_from_manifest(path: Path, *, limit: int = 8) -> list[dict]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return [{"kind": "grammar_card", **card} for card in FALLBACK_GRAMMAR_CARDS]

    items = manifest.get("items")
    if not isinstance(items, list):
        return [{"kind": "grammar_card", **card} for card in FALLBACK_GRAMMAR_CARDS]

    cards: list[dict] = [
        {
            "kind": "grammar_card",
            "id": "grammar_manifest.runtime_status",
            "title": "grammar manifest runtime_status",
            "text": "runtime_status values are implemented, partial, designed, reserved.",
            "source": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path),
        }
    ]
    for raw in sorted((item for item in items if isinstance(item, dict)), key=lambda item: str(item.get("id", ""))):
        item_id = str(raw.get("id", "")).strip()
        if not item_id:
            continue
        canon_name = str(raw.get("canon_name", "")).strip() or "-"
        runtime_status = str(raw.get("runtime_status", "")).strip() or "-"
        check_phase = str(raw.get("check_phase", "")).strip() or "-"
        pack_refs = raw.get("pack_refs", [])
        if not isinstance(pack_refs, list):
            pack_refs = []
        cards.append(
            {
                "kind": "grammar_card",
                "id": f"grammar_manifest.{item_id}",
                "title": f"{canon_name} grammar manifest card",
                "text": f"{item_id}: runtime_status={runtime_status}; check_phase={check_phase}; pack_refs={','.join(str(x) for x in pack_refs) or '-'}",
                "source": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path),
            }
        )
        if len(cards) >= limit:
            break
    return cards


def ssot_term_rows() -> list[dict]:
    return [{"kind": "ssot_term", **card} for card in SSOT_TERM_CARDS]


def diagnostic_card_rows(*, limit: int = 12) -> list[dict]:
    rows: list[dict] = []
    sources = [
        ROOT / "pack" / "education_physics_vertical_slice_g5_v1" / "diag_three_layer_fixture.detjson",
    ]
    for source_path in sources:
        try:
            fixture = json.loads(source_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            continue
        entries = fixture.get("entries")
        if not isinstance(entries, list):
            continue
        for entry in sorted((row for row in entries if isinstance(row, dict)), key=lambda row: str(row.get("id", ""))):
            entry_id = str(entry.get("id", "")).strip()
            if not entry_id:
                continue
            rows.append(
                {
                    "kind": "diagnostic_card",
                    "id": f"diagnostic.{entry_id}",
                    "title": entry_id,
                    "text": " / ".join(
                        [
                            f"무엇이: {str(entry.get('무엇이', '')).strip()}",
                            f"어디서: {str(entry.get('어디서', '')).strip()}",
                            f"어떻게: {str(entry.get('어떻게', '')).strip()}",
                        ]
                    ),
                    "source": source_path.relative_to(ROOT).as_posix() if source_path.is_relative_to(ROOT) else str(source_path),
                }
            )
            if len(rows) >= limit:
                return rows
    return rows


def select_example_file(pack_dir: Path) -> Path | None:
    preferred = [
        pack_dir / "input.ddn",
        pack_dir / "lesson.ddn",
        pack_dir / "main.ddn",
    ]
    for path in preferred:
        if path.exists():
            return path
    candidates = sorted(
        path
        for path in pack_dir.rglob("*.ddn")
        if "actual" not in path.parts and "out" not in path.parts
    )
    return candidates[0] if candidates else None


def pack_rows(pack_root: Path, *, limit: int) -> list[dict]:
    rows: list[dict] = []
    pack_count = 0
    for pack_dir in sorted(path for path in pack_root.iterdir() if path.is_dir()):
        readme = pack_dir / "README.md"
        golden = pack_dir / "golden.jsonl"
        example = select_example_file(pack_dir)
        if not readme.exists() or example is None:
            continue
        contract = load_contract(pack_dir / "contract.detjson")
        first_golden = load_first_golden_row(golden)
        contract_summary = {
            key: contract[key]
            for key in ("schema", "pack_id", "pack", "evidence_tier", "closure_claim", "closure_grade")
            if key in contract
        }
        readme_summary = first_paragraph(read_text(readme))
        summary_row = {
            "kind": "pack_summary",
            "pack": pack_dir.name,
            "path": pack_dir.relative_to(ROOT).as_posix(),
            "title": f"{pack_dir.name} pack summary",
            "text": readme_summary,
            "source": readme.relative_to(ROOT).as_posix(),
            "contract": contract_summary,
        }
        example_row = {
            "kind": "example",
            "pack": pack_dir.name,
            "path": pack_dir.relative_to(ROOT).as_posix(),
            "readme_summary": readme_summary,
            "example_path": example.relative_to(ROOT).as_posix(),
            "example": compact_code(read_text(example)),
            "golden": {
                key: first_golden[key]
                for key in ("id", "cmd", "stdout", "stdout_path", "exit_code")
                if key in first_golden
            },
            "contract": contract_summary,
        }
        rows.extend([summary_row, example_row])
        pack_count += 1
        if pack_count >= limit:
            break
    return rows


def stable_payload(row: dict) -> str:
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def with_digests(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for idx, row in enumerate(rows, start=1):
        payload = dict(row)
        payload["schema"] = "ddn.llm_corpus.row.v1"
        payload["row_index"] = idx
        digest_source = stable_payload(payload)
        payload["row_hash"] = "sha256:" + hashlib.sha256(digest_source.encode("utf-8")).hexdigest()
        out.append(payload)
    return out


def corpus_digest(rows: list[dict]) -> str:
    joined = "\n".join(stable_payload(row) for row in rows)
    return "sha256:" + hashlib.sha256(joined.encode("utf-8")).hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )


def write_manifest(path: Path, rows: list[dict], *, pack_root: Path, limit: int, grammar_manifest: Path) -> None:
    kind_counts = Counter(str(row.get("kind", "")) for row in rows)
    payload = {
        "schema": "ddn.llm_corpus.manifest.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows),
        "kind_counts": dict(sorted(kind_counts.items())),
        "corpus_hash": corpus_digest(rows),
        "pack_root": pack_root.relative_to(ROOT).as_posix() if pack_root.is_relative_to(ROOT) else str(pack_root),
        "limit": limit,
        "grammar_manifest": grammar_manifest.relative_to(ROOT).as_posix()
        if grammar_manifest.is_relative_to(ROOT)
        else str(grammar_manifest),
        "generation_policy": "deterministic_path_order_no_generated_summary",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract deterministic LLM corpus rows from DDN packs")
    parser.add_argument("--pack-root", default=str(ROOT / "pack"), help="pack root directory")
    parser.add_argument("--limit", type=int, default=120, help="maximum pack example rows")
    parser.add_argument("--grammar-manifest", default=str(default_grammar_manifest_path()), help="grammar manifest detjson path")
    parser.add_argument("--jsonl-out", default="", help="output JSONL path")
    parser.add_argument("--manifest-out", default="", help="optional manifest detjson path")
    args = parser.parse_args()

    pack_root = Path(args.pack_root)
    if not pack_root.is_absolute():
        pack_root = (ROOT / pack_root).resolve()
    limit = max(1, int(args.limit))
    out_path = Path(args.jsonl_out) if args.jsonl_out.strip() else default_out_path()
    if not out_path.is_absolute():
        out_path = (ROOT / out_path).resolve()

    grammar_manifest = Path(args.grammar_manifest)
    if not grammar_manifest.is_absolute():
        grammar_manifest = (ROOT / grammar_manifest).resolve()

    rows = grammar_cards_from_manifest(grammar_manifest)
    rows.extend(ssot_term_rows())
    rows.extend(diagnostic_card_rows())
    rows.extend(pack_rows(pack_root, limit=limit))
    rows = with_digests(rows)
    write_jsonl(out_path, rows)
    if args.manifest_out.strip():
        manifest_path = Path(args.manifest_out)
        if not manifest_path.is_absolute():
            manifest_path = (ROOT / manifest_path).resolve()
        write_manifest(manifest_path, rows, pack_root=pack_root, limit=limit, grammar_manifest=grammar_manifest)
    print(out_path)
    print(corpus_digest(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
