#!/usr/bin/env python3
"""Mutation checks for the public projection validator."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "validate_public_projection.py"


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


class ValidationMutationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="ddn-public-validation-")
        self.base = Path(self.temp.name)
        self.projection = self.base / "projection"
        self.receipts = self.base / "receipts"
        self.files = {
            "publish/spec/CURRENT.md": (b"[current](./v0.6.0/SPEC_MANIFEST_v0.6.0.md)\n", "PUBLIC_SPEC_CURRENT"),
            "publish/spec/v0.6.0/SPEC_MANIFEST_v0.6.0.md": (b"# manifest\n", "PUBLIC_SPEC_EXACT_V0_6_0"),
            "solutions/ui/wasm/ddonirang_tool_bg.wasm": (b"wasm", "TRACKED_WASM_FAMILY"),
            "solutions/ui/wasm_vm_runtime.js": (b"export const runtime = true;\n", "WORKBENCH_RUNTIME"),
            "tests/conformance.py": (b"print('ok')\n", "PUBLIC_CONFORMANCE_RUNNER"),
            "tool/src/lib.rs": (b"pub fn public() {}\n", "PRODUCT_SOURCE"),
            "tools/validate_public_projection.py": (TOOL.read_bytes(), "PROJECTION_VALIDATOR"),
        }
        self.seal()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def seal(self) -> None:
        if self.projection.exists():
            for path in sorted(self.projection.rglob("*"), reverse=True):
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()
        self.projection.mkdir(parents=True, exist_ok=True)
        manifest_files: dict[str, object] = {}
        for relative, (data, role) in self.files.items():
            path = self.projection / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            manifest_files[relative] = {
                "bytes": len(data), "role": role, "sha256": hashlib.sha256(data).hexdigest(), "source": relative
            }
        rows = b"".join(
            f"{path}\t{entry['bytes']}\t{entry['sha256']}\n".encode()
            for path, entry in sorted(manifest_files.items())
        )
        identity = "sha256:" + hashlib.sha256(rows).hexdigest()
        tree = {"file_count": len(manifest_files), "files": manifest_files, "public_tree_identity": identity,
                "schema": "ddn.public_tree_manifest.v1"}
        receipt = {"included_path_role_closure_identity": identity, "output_public_tree_identity": identity,
                   "schema": "ddn.public_projection_receipt.v1", "source_commit": "a" * 40}
        self.receipts.mkdir(parents=True, exist_ok=True)
        (self.receipts / "PUBLIC_TREE_MANIFEST.detjson").write_bytes(canonical(tree))
        (self.receipts / "PUBLIC_PROJECTION_RECEIPT.detjson").write_bytes(canonical(receipt))

    def run_validator(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--projection", str(self.projection), "--receipt-dir", str(self.receipts),
             "--require-role", "TRACKED_WASM_FAMILY", "--require-role", "WORKBENCH_RUNTIME",
             "--require-role", "PUBLIC_CONFORMANCE_RUNNER", "--require-spec-links", *extra],
            text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )

    def assert_red(self, code: str) -> None:
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(code, result.stdout)

    def test_green(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_validation_receipt_proves_total_security_scan(self) -> None:
        result = self.run_validator("--write-validation-receipt")
        self.assertEqual(result.returncode, 0, result.stdout)
        receipt = json.loads(
            (self.receipts / "PUBLIC_VALIDATION_RECEIPT.detjson").read_text(encoding="utf-8")
        )
        self.assertEqual(receipt["TOTAL_PROJECTED_FILES"], len(self.files))
        self.assertEqual(receipt["SECURITY_SCANNED_FILES"], len(self.files))
        self.assertEqual(receipt["SCANNED_ROLE_COUNT"], len({role for _, role in self.files.values()}))
        self.assertEqual(receipt["UNSCANNED_SECURITY_RELEVANT_FILES"], 0)

    def test_spec_current_marker_mutation_is_red(self) -> None:
        self.files["publish/spec/CURRENT.md"] = (b"[bad](./v9/MISSING.md)\n", "PUBLIC_SPEC_CURRENT")
        self.seal(); self.assert_red("E_PUBLIC_SPEC_CURRENT_LINK")

    def test_required_wasm_missing_is_red(self) -> None:
        del self.files["solutions/ui/wasm/ddonirang_tool_bg.wasm"]
        self.seal(); self.assert_red("E_PUBLIC_PROJECTION_REQUIRED_ROLE")

    def test_workbench_runtime_missing_is_red(self) -> None:
        del self.files["solutions/ui/wasm_vm_runtime.js"]
        self.seal(); self.assert_red("E_PUBLIC_PROJECTION_REQUIRED_ROLE")

    def test_conformance_dependency_missing_is_red(self) -> None:
        del self.files["tests/conformance.py"]
        self.seal(); self.assert_red("E_PUBLIC_PROJECTION_REQUIRED_ROLE")

    def test_retired_teul_cli_projection_is_red(self) -> None:
        self.files["tools/teul-cli/Cargo.toml"] = (
            b"[package]\nname = \"teul-cli\"\n",
            "CLI_SOURCE",
        )
        self.seal(); self.assert_red("E_PUBLIC_TEUL_CLI_RETIRED")

        del self.files["tools/teul-cli/Cargo.toml"]
        self.files["bin/teul-cli.exe"] = (b"MZ", "CLI_BINARY")
        self.seal(); self.assert_red("E_PUBLIC_TEUL_CLI_RETIRED")

    def test_internal_absolute_path_reinsertion_is_red(self) -> None:
        attack = b'const P: &str = "' + b'I:' + b'/home/urihanl/ddn/private";\n'
        self.files["tool/src/lib.rs"] = (attack, "PRODUCT_SOURCE")
        self.seal(); self.assert_red("E_PUBLIC_INTERNAL_ABSOLUTE_PATH")

    def test_private_fixture_include_reinsertion_is_red(self) -> None:
        attack = b'const P: &str = include_' + b'str!("../../pack/private.ddn");\n'
        self.files["tool/src/lib.rs"] = (attack, "PRODUCT_SOURCE")
        self.seal(); self.assert_red("E_PUBLIC_PRIVATE_FIXTURE_INCLUDE")

    def test_private_ssot_include_reinsertion_is_red(self) -> None:
        attack = b'const P: &str = include_' + b'str!("../../docs/ssot/private.md");\n'
        self.files["tests/conformance.py"] = (attack, "PUBLIC_CONFORMANCE_RUNNER")
        self.seal(); self.assert_red("E_PUBLIC_PRIVATE_FIXTURE_INCLUDE")

    def test_previously_omitted_product_metadata_windows_drive_is_red(self) -> None:
        attack = b'{"path":"' + b'C:' + b'\\\\private\\\\tool.exe"}\n'
        self.files["ddn.project.json"] = (attack, "PRODUCT_METADATA")
        self.seal(); self.assert_red("E_PUBLIC_INTERNAL_ABSOLUTE_PATH")

    def test_previously_omitted_public_spec_unc_path_is_red(self) -> None:
        slash = bytes([92])
        attack = b"# source " + slash * 2 + b"server" + slash + b"share" + slash + b"private\n"
        self.files["publish/spec/v0.6.0/SPEC_MANIFEST_v0.6.0.md"] = (
            attack, "PUBLIC_SPEC_EXACT_V0_6_0"
        )
        self.seal(); self.assert_red("E_PUBLIC_INTERNAL_ABSOLUTE_PATH")

    def test_binary_backslash_bytes_are_not_a_unc_path(self) -> None:
        slash = bytes([92])
        binary = b"wasm" + slash * 2 + bytes([0x17, 0x00, 0x10]) + slash + b"payload"
        self.files["solutions/ui/wasm/ddonirang_tool_bg.wasm"] = (
            binary, "TRACKED_WASM_FAMILY"
        )
        self.seal()
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_sealed_spec_external_provenance_token_is_not_runtime_path(self) -> None:
        slash = bytes([92])
        custody = b"| `external:D:" + slash + b"sealed-backup.7z` | hash |\n"
        self.files["publish/spec/v0.6.0/SPEC_MANIFEST_v0.6.0.md"] = (
            custody, "PUBLIC_SPEC_EXACT_V0_6_0"
        )
        self.seal()
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_sealed_spec_non_provenance_windows_path_is_red(self) -> None:
        slash = bytes([92])
        attack = b"runtime path D:" + slash + b"private" + slash + b"tool.exe\n"
        self.files["publish/spec/v0.6.0/SPEC_MANIFEST_v0.6.0.md"] = (
            attack, "PUBLIC_SPEC_EXACT_V0_6_0"
        )
        self.seal(); self.assert_red("E_PUBLIC_INTERNAL_ABSOLUTE_PATH")

    def test_previously_omitted_tracked_wasm_file_url_is_red(self) -> None:
        attack = b'wasm\x00' + b'file:' + b'///C:/private/build'
        self.files["solutions/ui/wasm/ddonirang_tool_bg.wasm"] = (
            attack, "TRACKED_WASM_FAMILY"
        )
        self.seal(); self.assert_red("E_PUBLIC_INTERNAL_ABSOLUTE_PATH")

    def test_previously_omitted_product_asset_device_path_is_red(self) -> None:
        attack = b'{"path":"' + b'\\\\\\\\?\\\\C:\\\\private"}\n'
        self.files["tool/assets/config.json"] = (attack, "PRODUCT_ASSET")
        self.seal(); self.assert_red("E_PUBLIC_INTERNAL_ABSOLUTE_PATH")

    def test_previously_omitted_compile_support_private_include_is_red(self) -> None:
        attack = b'const P: &str = include_' + b'bytes!("../../work/private.bin");\n'
        self.files["tool/tests/support.rs"] = (attack, "COMPILE_TIME_UNIT_TEST_SUPPORT")
        self.seal(); self.assert_red("E_PUBLIC_PRIVATE_FIXTURE_INCLUDE")

    def test_previously_omitted_projection_test_official_store_path_is_red(self) -> None:
        attack = b'path = "../' + b'official_store/db.sqlite"\n'
        self.files["tests/projector.py"] = (attack, "PROJECTION_TOOL_TEST")
        self.seal(); self.assert_red("E_PUBLIC_OFFICIAL_STORE_PATH")

    def test_validator_negative_fixtures_are_structurally_distinct(self) -> None:
        self.files["tests/test_validate_public_projection.py"] = (
            Path(__file__).read_bytes(),
            "PROJECTION_VALIDATOR_TEST",
        )
        self.seal()
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rust_cfg_test_negative_fixture_is_not_product_path(self) -> None:
        source = (
            b"pub fn product() {}\n"
            b"#[cfg(test)]\nmod tests {\n"
            b"    #[test]\n    fn rejects_absolute() {\n"
            b'        let path = "' + b'C:' + b'\\\\private\\\\fixture";\n'
            b"        assert!(!path.is_empty());\n    }\n}\n"
        )
        self.files["tool/src/lib.rs"] = (source, "PRODUCT_SOURCE")
        self.seal()
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_artifact_hash_mutation_is_red(self) -> None:
        (self.projection / "tool/src/lib.rs").write_bytes(b"tampered\n")
        self.assert_red("E_PUBLIC_PROJECTION_ARTIFACT_HASH")

    def test_dirty_source_authority_is_red(self) -> None:
        receipt_path = self.receipts / "PUBLIC_PROJECTION_RECEIPT.detjson"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["source_commit"] = "WORKTREE"
        receipt_path.write_bytes(canonical(receipt))
        self.assert_red("E_PUBLIC_PROJECTION_SOURCE_COMMIT")

    def test_projection_receipt_missing_is_red(self) -> None:
        (self.receipts / "PUBLIC_PROJECTION_RECEIPT.detjson").unlink()
        self.assert_red("E_PUBLIC_PROJECTION_RECEIPT_MISSING")

    def test_validation_receipt_roundtrip_is_green(self) -> None:
        written = self.run_validator("--write-validation-receipt")
        self.assertEqual(written.returncode, 0, written.stdout)
        validation_path = self.receipts / "PUBLIC_VALIDATION_RECEIPT.detjson"
        validation_bytes = validation_path.read_bytes()
        projection_receipt = json.loads(
            (self.receipts / "PUBLIC_PROJECTION_RECEIPT.detjson").read_text(encoding="utf-8")
        )
        self.assertEqual(
            projection_receipt["validation_receipt_identity"],
            "sha256:" + hashlib.sha256(validation_bytes).hexdigest(),
        )
        required = self.run_validator("--require-validation-receipt")
        self.assertEqual(required.returncode, 0, required.stdout)

    def test_validation_receipt_missing_is_red(self) -> None:
        written = self.run_validator("--write-validation-receipt")
        self.assertEqual(written.returncode, 0, written.stdout)
        (self.receipts / "PUBLIC_VALIDATION_RECEIPT.detjson").unlink()
        result = self.run_validator("--require-validation-receipt")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("E_PUBLIC_VALIDATION_RECEIPT_MISSING", result.stdout)


if __name__ == "__main__":
    unittest.main()
