#!/usr/bin/env python
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_OUT = Path(r"I:\home\urihanl\ddn\codex\out")
FALLBACK_OUT = Path(r"C:\ddn\codex\out")


def main() -> int:
    out_root = PRIMARY_OUT
    try:
        out_root.mkdir(parents=True, exist_ok=True)
    except OSError:
        out_root = FALLBACK_OUT
        out_root.mkdir(parents=True, exist_ok=True)

    temp_root = Path(tempfile.mkdtemp(prefix="wasm_build_failure_", dir=out_root))
    try:
        fake_wasm_pack = temp_root / "wasm-pack.cmd"
        fake_wasm_pack.write_text("@echo off\r\nexit /b 37\r\n", encoding="utf-8")
        env = dict(os.environ)
        env["PATH"] = f"{temp_root}{os.pathsep}{env.get('PATH', '')}"
        env["CARGO_NET_OFFLINE"] = "true"
        proc = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts" / "build_wasm_tool.ps1"),
                "-Profile",
                "release",
                "-Target",
                "web",
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        combined = f"{proc.stdout}\n{proc.stderr}"
        if proc.returncode == 0:
            raise AssertionError("failed wasm-pack command was reported as success")
        if "wasm-pack build failed with exit code 37" not in combined:
            raise AssertionError(f"missing propagated exit code: {combined.strip()}")
        if "WASM build complete" in combined:
            raise AssertionError("failed build printed completion marker")
        print("wasm_build_failure_propagation: PASS")
        return 0
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
