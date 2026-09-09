#!/usr/bin/env python3
"""Independent verifier for SSOT v24.17.1 and Language SPEC v0.3.0."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "docs" / "ssot" / "ssot"
REG = SSOT / "registries"
PUBLIC = ROOT / "publish" / "spec" / "v0.3.0"
VERSION = "v24.17.1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_rows(text: str):
    return re.findall(r"\| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{64})\x60 \|", text)


def active(text: str, path: Path) -> str:
    matches = re.findall(
        r"<!-- V24_17_1_ACTIVE_BEGIN -->(.*?)<!-- V24_17_1_ACTIVE_END -->",
        text,
        flags=re.S,
    )
    if len(matches) != 1:
        raise AssertionError(f"active boundary count {len(matches)}: {path}")
    return matches[0]


def main() -> int:
    failures: list[str] = []
    manifest = SSOT / "SSOT_ALL_MANIFEST_v24.17.1.md"
    seal = SSOT / "CURRENT_SHA256_v24.17.1.md"
    aggregate = SSOT / "SSOT_ALL_v24.17.1.md"
    current = SSOT / "CURRENT.md"
    public_manifest = PUBLIC / "SPEC_MANIFEST_v0.3.0.md"
    public_seal = PUBLIC / "SPEC_SHA256_v0.3.0.md"

    source_files = sorted(
        p for p in SSOT.glob("*_v24.17.1.md")
        if p.name not in {
            manifest.name,
            seal.name,
            aggregate.name,
        }
    )
    registry_files = sorted(REG.glob("*_v24.17.1.md"))
    if len(source_files) != 18:
        failures.append(f"non-manifest source count: {len(source_files)} != 18")
    if len(registry_files) != 12:
        failures.append(f"registry count: {len(registry_files)} != 12")

    for path in source_files + registry_files:
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            failures.append(f"UTF-8 BOM: {path}")
        if b"\r\n" in raw:
            failures.append(f"CRLF: {path}")
        try:
            block = active(raw.decode("utf-8"), path)
        except AssertionError as exc:
            failures.append(str(exc))
            continue
        if "(값들) 보임." in block:
            failures.append(f"stale boim tuple surface: {path}")
        if "deprecated legacy input" in block:
            failures.append(f"stale compat status: {path}")

    decisions = (SSOT / "SSOT_DECISIONS_v24.17.1.md").read_text(encoding="utf-8")
    for i in range(1, 43):
        marker = f"| RD-{i:03d} |"
        if decisions.count(marker) != 1:
            failures.append(f"decision row RD-{i:03d}: {decisions.count(marker)}")
    for i in range(1, 19):
        marker = f"| SV-D{i:02d} |"
        if decisions.count(marker) != 1:
            failures.append(f"standard-view decision row SV-D{i:02d}: {decisions.count(marker)}")

    manifest_text = manifest.read_text(encoding="utf-8")
    if "source_document_count: 19" not in manifest_text:
        failures.append("manifest source count declaration")
    if "generated_registry_count: 12" not in manifest_text:
        failures.append("manifest registry count declaration")
    if "previous_files_mutated: false" not in manifest_text:
        failures.append("previous mutation boundary")

    for rel, expected in hash_rows(seal.read_text(encoding="utf-8")):
        path = ROOT / rel
        if not path.exists():
            failures.append(f"internal sealed file missing: {rel}")
        elif digest(path) != expected:
            failures.append(f"internal seal mismatch: {rel}")

    aggregate_text = aggregate.read_text(encoding="utf-8")
    for path in source_files + registry_files:
        rel = path.relative_to(SSOT).as_posix()
        if aggregate_text.count(f"<!-- BEGIN {rel} -->") != 1:
            failures.append(f"aggregate begin marker: {rel}")
        if aggregate_text.count(f"<!-- END {rel} -->") != 1:
            failures.append(f"aggregate end marker: {rel}")

    if "v24.17.1" not in current.read_text(encoding="utf-8"):
        failures.append("internal CURRENT pointer")
    public_current = (ROOT / "publish" / "spec" / "CURRENT.md").read_text(encoding="utf-8")
    if "v0.3.0" not in public_current:
        failures.append("public CURRENT pointer")

    for rel, expected in hash_rows(public_seal.read_text(encoding="utf-8")):
        path = PUBLIC / rel
        if not path.exists():
            failures.append(f"public sealed file missing: {rel}")
        elif digest(path) != expected:
            failures.append(f"public seal mismatch: {rel}")

    allowed_legacy = {
        "SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.3.0.md",
        "SPEC_MANIFEST_v0.3.0.md",
        "SPEC_SHA256_v0.3.0.md",
    }
    for path in PUBLIC.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "(값들) 보임." in text:
            failures.append(f"public stale boim tuple: {path}")
        if path.name not in allowed_legacy and re.search(r"보임\s*\{", text):
            failures.append(f"public legacy boim example: {path}")

    walk_fixture = (
        ROOT / "docs" / "ssot" / "walks" / "gogae10"
        / "w100_public_observation_scene_composition" / "fixtures"
        / "representative_candidate.ddn"
    )
    if walk_fixture.read_text(encoding="utf-8").strip() != "(진자_공개상태: 진자_공개상태) 보임.":
        failures.append("WALK100 representative fixture")

    pointers = {
        "AGENTS.md": ("v24.17.1", "v0.3.0"),
        "CLAUDE.md": ("v24.17.1", "v0.3.0"),
        "AGENT_WORKFLOW.md": ("v24.17.1",),
        "SSOT_POLICY.md": ("v24.17.1",),
    }
    for rel, needles in pointers.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                failures.append(f"pointer {needle}: {rel}")

    if not public_manifest.exists() or not public_seal.exists():
        failures.append("public manifest/seal existence")

    if failures:
        print("INDEPENDENT CHECK FAILED")
        for item in failures:
            print(f"- {item}")
        return 1
    print("INDEPENDENT CHECK PASS")
    print(f"- internal source: {len(source_files) + 1}")
    print(f"- registry: {len(registry_files)}")
    print(f"- manifest sha256: {digest(manifest)}")
    print(f"- seal sha256: {digest(seal)}")
    print(f"- public manifest sha256: {digest(public_manifest)}")
    print(f"- public seal sha256: {digest(public_seal)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
