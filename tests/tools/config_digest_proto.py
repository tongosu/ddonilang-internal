#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BUILD = Path("I:/home/urihanl/ddn/codex/build/config_digest_proto")
if not BUILD.drive:
    BUILD = ROOT / "build" / "config_digest_proto"
TARGET_DEPS = Path("I:/home/urihanl/ddn/codex/target/debug/deps")
if not TARGET_DEPS.exists():
    TARGET_DEPS = ROOT / "target" / "debug" / "deps"

SECTION_ALIASES = {
    "doc": "문서",
    "document": "문서",
    "meta": "문서",
    "문서": "문서",
    "run": "실행",
    "runtime": "실행",
    "execution": "실행",
    "실행": "실행",
    "view": "보개",
    "bogae": "보개",
    "보개": "보개",
    "world": "누리",
    "nuri": "누리",
    "누리": "누리",
    "sam": "샘",
    "샘": "샘",
    "geoul": "거울",
    "mirror": "거울",
    "거울": "거울",
    "seulgi": "슬기",
    "ai": "슬기",
    "슬기": "슬기",
    "story": "이야기",
    "이야기": "이야기",
}

KEY_ALIASES = {
    "title": ("문서", "제목"),
    "name": ("문서", "제목"),
    "이름": ("문서", "제목"),
    "제목": ("문서", "제목"),
    "description": ("문서", "설명"),
    "desc": ("문서", "설명"),
    "설명": ("문서", "설명"),
    "lang": ("문서", "말씨"),
    "language": ("문서", "말씨"),
    "말씨": ("문서", "말씨"),
    "madi": ("실행", "마디수"),
    "madi_count": ("실행", "마디수"),
    "ticks": ("실행", "마디수"),
    "마디수": ("실행", "마디수"),
    "seed": ("누리", "시앗"),
    "시앗": ("누리", "시앗"),
    "seed_bag": ("누리", "시앗묶음"),
    "seed_streams": ("누리", "시앗묶음"),
    "시앗묶음": ("누리", "시앗묶음"),
    "entry": ("이야기", "들머리"),
    "들머리": ("이야기", "들머리"),
    "view_kind": ("보개", "보개종류"),
    "bogae_kind": ("보개", "보개종류"),
    "보개종류": ("보개", "보개종류"),
}


@dataclass(frozen=True)
class Token:
    kind: str
    text: str


class ConfigDigestError(ValueError):
    pass


def fail(message: str) -> int:
    print(f"config_digest_proto: FAIL: {message}", file=sys.stderr)
    return 1


def extract_settings_block(source: str) -> str:
    match = re.search(r"설정\s*\{", source)
    if not match:
        raise ConfigDigestError("missing 설정 { block")
    open_index = source.find("{", match.start())
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(source)):
        ch = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return source[open_index + 1 : index]
    raise ConfigDigestError("unterminated 설정 block")


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    index = 0
    while index < len(text):
        ch = text[index]
        if ch.isspace():
            index += 1
            continue
        if ch in "{}:.":
            tokens.append(Token(ch, ch))
            index += 1
            continue
        if ch == '"':
            end = index + 1
            escaped = False
            while end < len(text):
                current = text[end]
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == '"':
                    end += 1
                    break
                end += 1
            if end > len(text) or text[end - 1] != '"':
                raise ConfigDigestError("unterminated string literal")
            tokens.append(Token("string", text[index:end]))
            index = end
            continue
        match = re.match(r"[A-Za-z_가-힣ㄱ-ㅎㅏ-ㅣ][A-Za-z0-9_가-힣ㄱ-ㅎㅏ-ㅣ-]*", text[index:])
        if match:
            value = match.group(0)
            tokens.append(Token("ident", value))
            index += len(value)
            continue
        match = re.match(r"-?\d+(?:\.\d+)?", text[index:])
        if match:
            value = match.group(0)
            tokens.append(Token("number", value))
            index += len(value)
            continue
        raise ConfigDigestError(f"unsupported token near {text[index:index + 20]!r}")
    return tokens


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def peek(self) -> Token | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def take(self) -> Token:
        token = self.peek()
        if token is None:
            raise ConfigDigestError("unexpected end of settings block")
        self.index += 1
        return token

    def parse(self) -> dict[str, Any]:
        obj = self.parse_object(until=None)
        if self.peek() is not None:
            raise ConfigDigestError(f"trailing token {self.peek().text!r}")
        return obj

    def parse_object(self, until: str | None) -> dict[str, Any]:
        obj: dict[str, Any] = {}
        while self.peek() is not None:
            if until and self.peek().kind == until:
                self.take()
                break
            name = self.take()
            if name.kind != "ident":
                raise ConfigDigestError(f"expected key or section, got {name.text!r}")
            marker = self.take()
            if marker.kind == "{":
                value = self.parse_object(until="}")
                obj[name.text] = value
                if self.peek() is not None and self.peek().kind == ".":
                    self.take()
                continue
            if marker.kind != ":":
                raise ConfigDigestError(f"expected ':' or '{{' after {name.text!r}")
            value_tokens: list[Token] = []
            while self.peek() is not None and self.peek().kind != ".":
                if self.peek().kind in "{}:":
                    raise ConfigDigestError(f"unsupported scalar token {self.peek().text!r}")
                value_tokens.append(self.take())
            if self.peek() is None:
                raise ConfigDigestError(f"missing '.' after {name.text!r}")
            self.take()
            obj[name.text] = parse_scalar(value_tokens)
        return obj


def parse_scalar(tokens: list[Token]) -> Any:
    if len(tokens) != 1:
        raise ConfigDigestError("prototype scalar parser accepts one literal per key")
    token = tokens[0]
    if token.kind == "string":
        return json.loads(token.text)
    if token.kind == "number":
        if "." in token.text:
            number = float(token.text)
            return int(number) if number.is_integer() else number
        return int(token.text)
    if token.kind == "ident":
        if token.text in {"참", "true"}:
            return True
        if token.text in {"거짓", "false"}:
            return False
        return token.text
    raise ConfigDigestError(f"unsupported scalar literal {token.text!r}")


def put_path(root: dict[str, Any], section: str, key: str, value: Any) -> None:
    bucket = root.setdefault(section, {})
    if not isinstance(bucket, dict):
        raise ConfigDigestError(f"section collision: {section}")
    if key in bucket and bucket[key] != value:
        raise ConfigDigestError(f"conflicting duplicate key: {section}.{key}")
    bucket[key] = value


def canonicalize_object(obj: dict[str, Any], current_section: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for raw_key, value in obj.items():
        if isinstance(value, dict):
            section = SECTION_ALIASES.get(raw_key, raw_key)
            nested = canonicalize_object(value, current_section=section)
            for nested_key, nested_value in nested.items():
                if isinstance(nested_value, dict):
                    target_section = nested_key
                    bucket = out.setdefault(target_section, {})
                    if not isinstance(bucket, dict):
                        raise ConfigDigestError(f"section collision: {target_section}")
                    bucket.update(nested_value)
                else:
                    put_path(out, section, nested_key, nested_value)
            continue

        section, key = KEY_ALIASES.get(raw_key, (current_section or "문서", raw_key))
        if current_section is not None and raw_key not in KEY_ALIASES:
            section = current_section
        put_path(out, section, key, value)
    return sort_nested(out)


def sort_nested(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: sort_nested(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [sort_nested(item) for item in value]
    return value


def canonical_payload(source: str) -> dict[str, Any]:
    block = extract_settings_block(source)
    parsed = Parser(tokenize(block)).parse()
    settings = canonicalize_object(parsed)
    return {
        "schema": "ddn.config_digest_proto.canonical.v1",
        "settings": settings,
    }


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def ensure_blake3_helper() -> Path:
    BUILD.mkdir(parents=True, exist_ok=True)
    exe = BUILD / ("blake3_stdin.exe" if os.name == "nt" else "blake3_stdin")
    src = BUILD / "blake3_stdin.rs"
    source = (
        "use std::io::{self, Read};\n"
        "fn main() {\n"
        "    let mut buf = Vec::new();\n"
        "    io::stdin().read_to_end(&mut buf).unwrap();\n"
        "    println!(\"blake3:{}\", blake3::hash(&buf).to_hex());\n"
        "}\n"
    )
    if exe.exists() and src.exists() and src.read_text(encoding="utf-8") == source:
        return exe
    src.write_text(source, encoding="utf-8")
    rlibs = sorted(TARGET_DEPS.glob("libblake3-*.rlib"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not rlibs:
        subprocess.run(["cargo", "build", "-q", "-p", "ddonirang-core"], cwd=ROOT, check=True)
        rlibs = sorted(TARGET_DEPS.glob("libblake3-*.rlib"), key=lambda path: path.stat().st_mtime, reverse=True)
    last_error = ""
    for rlib in rlibs:
        proc = subprocess.run(
            [
                "rustc",
                str(src),
                "--edition=2021",
                "-L",
                f"dependency={TARGET_DEPS}",
                "--extern",
                f"blake3={rlib}",
                "-o",
                str(exe),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode == 0:
            return exe
        last_error = proc.stderr.strip()
    raise ConfigDigestError(f"failed to compile BLAKE3 helper: {last_error}")


def blake3_digest(data: bytes) -> str:
    helper = ensure_blake3_helper()
    proc = subprocess.run(
        [str(helper)],
        input=data,
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return proc.stdout.decode("utf-8").strip()


def classify_key(section: str, key: str) -> str:
    if section in RESULT_AFFECTING_KEYS and key in RESULT_AFFECTING_KEYS[section]:
        return "result_affecting"
    if section in RUN_SECTIONS:
        return "candidate_result_affecting_unclassified"
    if section in VIEW_SECTIONS:
        return "view_affecting"
    if section in DOC_SECTIONS:
        return "doc_affecting"
    return "unclassified"


def classified_rows(settings: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for section, values in settings.items():
        if not isinstance(values, dict):
            rows.append({"path": section, "class": "unclassified", "reason": "non-section scalar"})
            continue
        for key in values:
            cls = classify_key(section, key)
            rows.append(
                {
                    "path": f"{section}.{key}",
                    "class": cls,
                    "reason": f"{CLASSIFIER_VERSION}; tooling prototype, not SSOT final",
                }
            )
    return sorted(rows, key=lambda row: row["path"])


def select_settings(settings: dict[str, Any], classes: set[str]) -> dict[str, Any]:
    selected: dict[str, Any] = {}
    for section, values in settings.items():
        if not isinstance(values, dict):
            continue
        for key, value in values.items():
            if classify_key(section, key) in classes:
                put_path(selected, section, key, value)
    return sort_nested(selected)


def digest_named_payload(schema: str, payload: dict[str, Any]) -> dict[str, Any]:
    sealed = {"schema": schema, **payload}
    return {
        "schema": schema,
        "digest": blake3_digest(canonical_bytes(sealed)),
        "canonical": sealed,
    }


def stream_names(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw = re.split(r"[,;]", value)
        return sorted({item.strip() for item in raw if item.strip()})
    return [str(value)]


def seed_stream_fixture(settings: dict[str, Any]) -> dict[str, Any]:
    nuri = settings.get("누리", {})
    if not isinstance(nuri, dict):
        nuri = {}
    root_seed = nuri.get("시앗")
    names = stream_names(nuri.get("시앗묶음"))
    streams = []
    for name in names:
        seed_payload = {
            "schema": "ddn.seed_stream_derivation.fixture.v1",
            "stage": "before_InputSnapshot",
            "root_seed": root_seed,
            "stream_name": name,
            "stream_name_canonicalization": "trim + comma/semicolon split; draft only",
        }
        streams.append(
            {
                "stream_name": name,
                "derived_seed": blake3_digest(canonical_bytes(seed_payload)),
                "input_snapshot_written": False,
                "derivation_payload": seed_payload,
            }
        )
    return {
        "schema": "ddn.seed_stream_derivation.fixture_set.v1",
        "draft_only": True,
        "root_seed": root_seed,
        "streams": streams,
        "input_snapshot_written": False,
        "runtime_schema_touched": False,
    }


def hash_report(payload: dict[str, Any]) -> dict[str, Any]:
    settings = payload["settings"]
    run_settings = select_settings(
        settings,
        {"result_affecting", "candidate_result_affecting_unclassified"},
    )
    view_settings = select_settings(settings, {"view_affecting"})
    doc_settings = select_settings(settings, {"doc_affecting"})
    run_hash = digest_named_payload(
        "ddn.config_digest_proto.run_config_hash.v1",
        {"classifier_version": CLASSIFIER_VERSION, "settings": run_settings},
    )
    view_hash = digest_named_payload(
        "ddn.config_digest_proto.view_config_hash.v1",
        {"classifier_version": CLASSIFIER_VERSION, "settings": view_settings},
    )
    doc_hash = digest_named_payload(
        "ddn.config_digest_proto.doc_config_hash.v1",
        {"classifier_version": CLASSIFIER_VERSION, "settings": doc_settings},
    )
    envelope_payload = {
        "classifier_version": CLASSIFIER_VERSION,
        "run_config_hash": run_hash["digest"],
        "view_config_hash": view_hash["digest"],
        "doc_config_hash": doc_hash["digest"],
    }
    settings_hash = digest_named_payload(
        "ddn.config_digest_proto.settings_hash_envelope.v1",
        envelope_payload,
    )
    return {
        "algo": "blake3",
        "digest": settings_hash["digest"],
        "hashes": {
            "run_config_hash": run_hash["digest"],
            "view_config_hash": view_hash["digest"],
            "doc_config_hash": doc_hash["digest"],
            "settings_hash": settings_hash["digest"],
        },
        "hash_inputs": {
            "run_config_hash": run_hash["canonical"],
            "view_config_hash": view_hash["canonical"],
            "doc_config_hash": doc_hash["canonical"],
            "settings_hash": settings_hash["canonical"],
        },
        "result_affecting_classifier": {
            "version": CLASSIFIER_VERSION,
            "draft_only": True,
            "rows": classified_rows(settings),
        },
        "seed_stream_fixture": seed_stream_fixture(settings),
        "state_hash_touched": False,
        "parser_touched": False,
        "runtime_schema_touched": False,
    }


SELFTEST_PAIRS = [
    (
        '설정 { 제목: "데모". 마디수: 12. 시앗: 7. }.',
        '설정 {   title : "데모".   실행 { seed: 7. madi: 12. }. }.',
    ),
    (
        '설정 { 문서 { 이름: "실험". 설명: "A". }. 실행 { 마디수: 3. }. }.',
        '설정 { doc { title: "실험". desc: "A". }. run { ticks: 3. }. }.',
    ),
    (
        '설정 { 보개 { 보개종류: "console-grid". }. 문서 { 말씨: "ko". }. }.',
        '설정 { view { view_kind: "console-grid". }. meta { language: "ko". }. }.',
    ),
]

CLASSIFIER_VERSION = "draft-20260708-ssot-addendum-tooling-only"
RUN_SECTIONS = {"실행", "누리", "샘", "슬기"}
VIEW_SECTIONS = {"보개", "거울"}
DOC_SECTIONS = {"문서", "이야기"}
RESULT_AFFECTING_KEYS = {
    "실행": {
        "차림새",
        "마디수",
        "결정갈래",
        "마디맺음갈래",
        "행동모음갈래",
        "동점다룸",
        "걷기갈래",
        "마디틈갈래",
        "속마디수",
        "속틈",
        "공정성갈래",
    },
    "누리": {
        "환경ID",
        "시앗",
        "시앗묶음",
        "세계갈래",
        "크기",
        "경계다룸",
        "첫상태참조",
        "규칙묶음",
        "계산단위계",
    },
    "샘": {
        "입력원천",
        "주입방식",
        "슬롯정의",
        "입력틈",
        "늦은입력다룸",
    },
    "슬기": {
        "정책",
        "지연마디",
        "늦은제안다룸",
        "제안한도",
        "관찰범위",
        "승인갈래",
        "재연갈래",
    },
}


def run_selftest() -> int:
    rows = []
    for index, (left, right) in enumerate(SELFTEST_PAIRS, start=1):
        left_payload = canonical_payload(left)
        right_payload = canonical_payload(right)
        if left_payload != right_payload:
            return fail(f"selftest pair {index} canonical mismatch: {left_payload} != {right_payload}")
        left_report = hash_report(left_payload)
        right_report = hash_report(right_payload)
        if left_report["hashes"] != right_report["hashes"]:
            return fail(f"selftest pair {index} digest mismatch")
        required_hashes = {"run_config_hash", "view_config_hash", "doc_config_hash", "settings_hash"}
        if set(left_report["hashes"]) != required_hashes:
            return fail(f"selftest pair {index} missing split hashes: {left_report['hashes']}")
        rows.append(
            {
                "pair": index,
                "digest": left_report["digest"],
                "hashes": left_report["hashes"],
                "canonical": left_payload,
            }
        )
    seed_source = '설정 { 누리 { 시앗: 7. 시앗묶음: "physics,policy". }. 실행 { 마디수: 3. }. }.'
    seed_report = hash_report(canonical_payload(seed_source))
    seed_fixture = seed_report["seed_stream_fixture"]
    if seed_fixture["input_snapshot_written"] is not False:
        return fail("seed stream fixture must stop before InputSnapshot")
    stream_names_found = [row["stream_name"] for row in seed_fixture["streams"]]
    if stream_names_found != ["physics", "policy"]:
        return fail(f"seed stream fixture mismatch: {stream_names_found}")
    if not all(str(row["derived_seed"]).startswith("blake3:") for row in seed_fixture["streams"]):
        return fail("seed stream derived seed must be BLAKE3")
    if seed_report["hashes"]["run_config_hash"] == seed_report["hashes"]["view_config_hash"]:
        return fail("run_config_hash and view_config_hash should be separate hash values")
    print("config_digest_proto: PASS")
    print(
        json.dumps(
            {
                "schema": "ddn.config_digest_proto.selftest.v2",
                "pairs": rows,
                "seed_stream_fixture": seed_fixture,
                "result_affecting_classifier": seed_report["result_affecting_classifier"],
                "runtime_schema_touched": False,
                "state_hash_touched": False,
                "parser_touched": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="DDN file containing a 설정 {} block; stdin is used when omitted")
    parser.add_argument("--json-out", help="write digest report detjson")
    parser.add_argument("--selftest", action="store_true", help="run alias/whitespace equivalence selftests")
    args = parser.parse_args()

    try:
        if args.selftest:
            return run_selftest()
        source = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
        payload = canonical_payload(source)
        data = canonical_bytes(payload)
        hashes = hash_report(payload)
        report = {
            "schema": "ddn.config_digest_proto.report.v1",
            "algo": hashes["algo"],
            "digest": hashes["digest"],
            "hashes": hashes["hashes"],
            "hash_inputs": hashes["hash_inputs"],
            "canonical": payload,
            "canonical_utf8_len": len(data),
            "result_affecting_classifier": hashes["result_affecting_classifier"],
            "seed_stream_fixture": hashes["seed_stream_fixture"],
            "runtime_schema_touched": False,
            "state_hash_touched": False,
            "parser_touched": False,
        }
        if args.json_out:
            out = Path(args.json_out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (ConfigDigestError, subprocess.CalledProcessError) as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
