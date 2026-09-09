#!/usr/bin/env python
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tests" / "tools" / "extract_llm_corpus_v1.py"
OUT_DIR = Path("I:/home/urihanl/ddn/codex/out")
OUT_JSONL = OUT_DIR / "llm_corpus_v1.jsonl"
OUT_MANIFEST = OUT_DIR / "llm_corpus_v1.manifest.detjson"


def fail(message: str) -> int:
    print(f"llm_corpus_v1_dayrun_check: FAIL: {message}", file=sys.stderr)
    return 1


def run_extract(jsonl: Path, manifest: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--limit",
            "120",
            "--jsonl-out",
            str(jsonl),
            "--manifest-out",
            str(manifest),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if not TOOL.exists():
        return fail(f"missing extractor: {TOOL.relative_to(ROOT).as_posix()}")

    with tempfile.TemporaryDirectory(prefix="llm_corpus_dayrun_") as temp_dir:
        temp = Path(temp_dir)
        a_jsonl = temp / "a.jsonl"
        a_manifest = temp / "a.manifest.detjson"
        b_jsonl = temp / "b.jsonl"
        b_manifest = temp / "b.manifest.detjson"
        for jsonl, manifest in [(a_jsonl, a_manifest), (b_jsonl, b_manifest)]:
            proc = run_extract(jsonl, manifest)
            if proc.returncode != 0:
                return fail(proc.stderr.strip() or proc.stdout.strip() or "extract failed")

        bytes_a = a_jsonl.read_bytes()
        bytes_b = b_jsonl.read_bytes()
        if bytes_a != bytes_b:
            return fail("two JSONL extracts are not byte-identical")

        rows = load_jsonl(a_jsonl)
        if len(rows) < 100:
            return fail(f"row_count below 100: {len(rows)}")
        if not any(row.get("kind") == "grammar_card" for row in rows):
            return fail("grammar_card rows missing")
        if not any(str(row.get("id", "")).startswith("grammar_manifest.") for row in rows):
            return fail("grammar manifest based cards missing")

        for idx, row in enumerate(rows, start=1):
            if row.get("schema") != "ddn.llm_corpus.row.v1":
                return fail(f"row schema mismatch at {idx}")
            if row.get("row_index") != idx:
                return fail(f"row index mismatch at {idx}")
            if not str(row.get("row_hash", "")).startswith("sha256:"):
                return fail(f"row hash missing at {idx}")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        proc = run_extract(OUT_JSONL, OUT_MANIFEST)
        if proc.returncode != 0:
            return fail(proc.stderr.strip() or proc.stdout.strip() or "final extract failed")
        if OUT_JSONL.read_bytes() != bytes_a:
            return fail("final out/llm_corpus_v1.jsonl differs from deterministic temp extract")

    manifest = json.loads(OUT_MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("row_count") != len(load_jsonl(OUT_JSONL)):
        return fail("manifest row_count mismatch")

    print("llm_corpus_v1_dayrun_check: PASS")
    print(f"rows={manifest.get('row_count')}")
    print(f"jsonl={OUT_JSONL.as_posix()}")
    print(f"sha256={sha256_file(OUT_JSONL)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
