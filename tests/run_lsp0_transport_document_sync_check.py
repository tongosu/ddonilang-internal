"""Black-box LSP-0 streaming transport/document-sync smoke and pack check."""

from __future__ import annotations

import json
import os
import queue
import subprocess
import threading
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "pack" / "lsp0_transport_document_sync_v1"
TARGET = Path(
    os.environ.get(
        "CARGO_TARGET_DIR",
        "I:/home/urihanl/ddn/codex/build/lsp0-transport-document-sync-r1",
    )
)
BINARY = TARGET / "debug" / ("ddonirang-lsp.exe" if os.name == "nt" else "ddonirang-lsp")
READ_CHUNK_SIZE = 4096
READ_TIMEOUT = 5.0
MAX_HEADER_SECTION_BYTES = 16 * 1024
MAX_CONTENT_LENGTH_BYTES = 16 * 1024 * 1024


def frame(message: dict) -> bytes:
    body = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body


def decode_frames(payload: bytes) -> list[dict]:
    result: list[dict] = []
    cursor = 0
    while cursor < len(payload):
        separator = payload.find(b"\r\n\r\n", cursor)
        if separator < 0:
            raise AssertionError("missing frame separator")
        header = payload[cursor:separator].decode("ascii")
        fields = [line for line in header.split("\r\n") if line]
        lengths = [
            line.split(":", 1)[1].strip()
            for line in fields
            if line.lower().startswith("content-length:")
        ]
        if len(lengths) != 1:
            raise AssertionError("invalid content length")
        size = int(lengths[0])
        start = separator + 4
        end = start + size
        if end > len(payload):
            raise AssertionError("truncated output frame")
        result.append(json.loads(payload[start:end].decode("utf-8")))
        cursor = end
    return result


class PipeReader:
    def __init__(self, pipe) -> None:
        self._queue: queue.Queue[bytes | BaseException | None] = queue.Queue()
        self._captured = bytearray()
        self._pipe = pipe
        self._thread = threading.Thread(target=self._read, daemon=True)
        self._thread.start()

    def _read(self) -> None:
        try:
            while True:
                read1 = getattr(self._pipe, "read1", self._pipe.read)
                chunk = read1(READ_CHUNK_SIZE)
                if not chunk:
                    break
                self._captured.extend(chunk)
                self._queue.put(chunk)
        except BaseException as error:
            self._queue.put(error)
        finally:
            self._queue.put(None)

    def next_item(self, timeout: float) -> bytes | BaseException | None:
        return self._queue.get(timeout=timeout)

    def join(self) -> None:
        self._thread.join(timeout=READ_TIMEOUT)

    def captured(self) -> bytes:
        self.join()
        return bytes(self._captured)


class FrameReader:
    def __init__(self, stream: PipeReader) -> None:
        self._stream = stream
        self._buffer = bytearray()
        self._eof = False

    def _take_frame(self) -> dict | None:
        separator = self._buffer.find(b"\r\n\r\n")
        if separator < 0:
            return None
        header = bytes(self._buffer[:separator]).decode("ascii")
        fields = [line for line in header.split("\r\n") if line]
        lengths = [
            line.split(":", 1)[1].strip()
            for line in fields
            if line.lower().startswith("content-length:")
        ]
        if len(lengths) != 1:
            raise AssertionError("invalid output Content-Length")
        size = int(lengths[0])
        start = separator + 4
        end = start + size
        if len(self._buffer) < end:
            return None
        body = bytes(self._buffer[start:end])
        del self._buffer[:end]
        return json.loads(body.decode("utf-8"))

    def read_frame(self, timeout: float = READ_TIMEOUT) -> dict:
        deadline = time.monotonic() + timeout
        while True:
            message = self._take_frame()
            if message is not None:
                return message
            if self._eof:
                raise AssertionError("stdout closed before a complete frame")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("timed out waiting for JSON-RPC frame")
            try:
                item = self._stream.next_item(remaining)
            except queue.Empty as error:
                raise TimeoutError("timed out waiting for JSON-RPC frame") from error
            if isinstance(item, BaseException):
                raise AssertionError(f"stdout reader failed: {item}") from item
            if item is None:
                self._eof = True
            else:
                self._buffer.extend(item)


class LspProcess:
    def __init__(self) -> None:
        self.process = subprocess.Popen(
            [str(BINARY)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        assert self.process.stdin is not None
        assert self.process.stdout is not None
        assert self.process.stderr is not None
        self.stdout_stream = PipeReader(self.process.stdout)
        self.stderr_stream = PipeReader(self.process.stderr)
        self.frames = FrameReader(self.stdout_stream)
        self.stdin_closed = False

    def send(self, payload: bytes) -> None:
        if self.process.stdin is None or self.stdin_closed:
            raise AssertionError("stdin is closed")
        self.process.stdin.write(payload)
        self.process.stdin.flush()

    def close_stdin(self) -> None:
        if self.process.stdin is not None and not self.stdin_closed:
            self.process.stdin.close()
            self.stdin_closed = True

    def wait(self, timeout: float = READ_TIMEOUT) -> int:
        try:
            return self.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            self.kill_exact_child()
            raise AssertionError("LSP child did not exit within bounded timeout") from error

    def kill_exact_child(self) -> None:
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait(timeout=READ_TIMEOUT)

    def output(self) -> tuple[bytes, bytes]:
        return self.stdout_stream.captured(), self.stderr_stream.captured()

    def __enter__(self) -> "LspProcess":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.process.poll() is None:
            self.close_stdin()
            self.kill_exact_child()
        self.output()


def build_binary() -> None:
    environment = os.environ.copy()
    environment["CARGO_TARGET_DIR"] = str(TARGET)
    result = subprocess.run(
        [
            "cargo",
            "build",
            "--offline",
            "--quiet",
            "--manifest-path",
            str(ROOT / "tool" / "Cargo.toml"),
            "--bin",
            "ddonirang-lsp",
        ],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert BINARY.exists(), BINARY


def initialize_message(message_id: int = 1, client_name: str = "lsp0-client") -> dict:
    return {
        "jsonrpc": "2.0",
        "id": message_id,
        "method": "initialize",
        "params": {
            "clientInfo": {"name": client_name},
            "capabilities": {"general": {"positionEncodings": ["utf-16", "utf-8"]}},
        },
    }


def assert_initialize(response: dict, message_id: int = 1) -> None:
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == message_id
    capabilities = response["result"]["capabilities"]
    assert capabilities["positionEncoding"] == "utf-16"
    assert capabilities["textDocumentSync"] == {"openClose": True, "change": 1}


def lifecycle_messages() -> list[dict]:
    return [
        {"jsonrpc": "2.0", "method": "initialized", "params": {}},
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///hangul.ddn",
                    "languageId": "ddn",
                    "version": 1,
                    "text": "한글 원문\n",
                }
            },
        },
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didChange",
            "params": {
                "textDocument": {"uri": "file:///hangul.ddn", "version": 2},
                "contentChanges": [{"text": "변경된 원문\n"}],
            },
        },
        {
            "jsonrpc": "2.0",
            "method": "textDocument/didClose",
            "params": {"textDocument": {"uri": "file:///hangul.ddn"}},
        },
        {"jsonrpc": "2.0", "id": 2, "method": "shutdown"},
    ]


def assert_no_frame(reader: FrameReader, timeout: float = 0.1) -> None:
    try:
        message = reader.read_frame(timeout)
    except TimeoutError:
        return
    raise AssertionError(f"unexpected early response: {message}")


def assert_publish_diagnostics(reader: FrameReader, *, empty: bool | None = None) -> dict:
    message = reader.read_frame()
    assert message["jsonrpc"] == "2.0"
    assert message["method"] == "textDocument/publishDiagnostics"
    diagnostics = message["params"]["diagnostics"]
    assert isinstance(diagnostics, list)
    if empty is not None:
        assert bool(diagnostics) is (not empty)
    return message


def check_initialize_before_eof() -> None:
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        assert_initialize(process.frames.read_frame())
        assert process.process.poll() is None
        assert not process.stdin_closed
        process.send(frame({"jsonrpc": "2.0", "id": 2, "method": "shutdown"}))
        assert process.frames.read_frame()["id"] == 2
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 0
        _, stderr = process.output()
        assert b"panic" not in stderr.lower()
    print("I1_INITIALIZE_BEFORE_EOF=PASS")


def check_fragmented_header() -> None:
    raw = frame(initialize_message(client_name="fragmented-header"))
    with LspProcess() as process:
        for chunk in (raw[:3], raw[3:11], raw[11:-1]):
            process.send(chunk)
            assert_no_frame(process.frames)
        process.send(raw[-1:])
        assert_initialize(process.frames.read_frame())
        process.send(frame({"jsonrpc": "2.0", "id": 2, "method": "shutdown"}))
        assert process.frames.read_frame()["id"] == 2
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 0
    print("I2_FRAGMENTED_HEADER=PASS")


def check_fragmented_utf8_body() -> None:
    raw = frame(initialize_message(client_name="한글🙂"))
    separator = raw.index(b"\r\n\r\n") + 4
    hangul = raw.index("한".encode("utf-8"), separator)
    split = hangul + 1
    with LspProcess() as process:
        process.send(raw[:split])
        assert_no_frame(process.frames)
        process.send(raw[split:])
        assert_initialize(process.frames.read_frame())
        process.send(frame({"jsonrpc": "2.0", "id": 2, "method": "shutdown"}))
        assert process.frames.read_frame()["id"] == 2
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 0
    print("I3_FRAGMENTED_UTF8_BODY=PASS")


def check_multiple_frames_single_write() -> None:
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        assert_initialize(process.frames.read_frame())
        process.send(b"".join(frame(message) for message in lifecycle_messages()))
        assert_publish_diagnostics(process.frames, empty=False)
        assert_publish_diagnostics(process.frames, empty=False)
        assert_publish_diagnostics(process.frames, empty=True)
        assert process.frames.read_frame() == {"jsonrpc": "2.0", "id": 2, "result": None}
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 0
    print("I4_MULTI_FRAME_SINGLE_WRITE=PASS")


def check_persistent_lifecycle() -> None:
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        assert_initialize(process.frames.read_frame())
        for message in lifecycle_messages()[:-1]:
            process.send(frame(message))
            if message["method"] == "initialized":
                assert_no_frame(process.frames)
            elif message["method"] == "textDocument/didOpen":
                assert_publish_diagnostics(process.frames, empty=False)
            elif message["method"] == "textDocument/didChange":
                assert_publish_diagnostics(process.frames, empty=False)
            else:
                assert_publish_diagnostics(process.frames, empty=True)
        process.send(frame(lifecycle_messages()[-1]))
        assert process.frames.read_frame() == {"jsonrpc": "2.0", "id": 2, "result": None}
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 0
    print("I5_PERSISTENT_LIFECYCLE=PASS")


def check_pull_diagnostics_before_eof() -> None:
    uri = "file:///pull-diagnostics.ddn"
    legacy = "🙂검산:움직씨 = {\n}\n"
    valid = "검산:움직씨 := {\n}\n"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        provider = initialize["result"]["capabilities"]["diagnosticProvider"]
        assert provider["identifier"] == "ddonirang-v25"
        assert provider["workspaceDiagnostics"] is True

        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "languageId": "ddn",
                            "version": 1,
                            "text": legacy,
                        }
                    },
                }
            )
        )
        push = assert_publish_diagnostics(process.frames, empty=False)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 201,
                    "method": "textDocument/diagnostic",
                    "params": {"textDocument": {"uri": uri, "version": 1}},
                }
            )
        )
        full = process.frames.read_frame()
        assert full["id"] == 201
        assert full["result"]["kind"] == "full"
        assert full["result"]["items"] == push["params"]["diagnostics"]
        result_id = full["result"]["resultId"]
        assert isinstance(result_id, str) and result_id.endswith(
            push["params"]["data"]["snapshotIdentity"]
        )

        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 202,
                    "method": "textDocument/diagnostic",
                    "params": {
                        "textDocument": {"uri": uri, "version": 1},
                        "previousResultId": result_id,
                    },
                }
            )
        )
        unchanged = process.frames.read_frame()
        assert unchanged["result"] == {"kind": "unchanged", "resultId": result_id}

        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didChange",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "contentChanges": [{"text": valid}],
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 203,
                    "method": "textDocument/diagnostic",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "previousResultId": result_id,
                    },
                }
            )
        )
        refreshed = process.frames.read_frame()
        assert refreshed["result"]["kind"] == "full"
        assert refreshed["result"]["items"] == []
        assert refreshed["result"]["resultId"] != result_id

        for extra_uri in ("file:///b-pull.ddn", "file:///a-pull.ddn"):
            process.send(
                frame(
                    {
                        "jsonrpc": "2.0",
                        "method": "textDocument/didOpen",
                        "params": {
                            "textDocument": {
                                "uri": extra_uri,
                                "languageId": "ddn",
                                "version": 1,
                                "text": legacy,
                            }
                        },
                    }
                )
            )
            assert_publish_diagnostics(process.frames, empty=False)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 204,
                    "method": "workspace/diagnostic",
                    "params": {},
                }
            )
        )
        workspace = process.frames.read_frame()
        assert [item["uri"] for item in workspace["result"]["items"]] == [
            "file:///a-pull.ddn",
            "file:///b-pull.ddn",
            uri,
        ]

        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {"textDocument": {"uri": "file:///a-pull.ddn"}},
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 205,
                    "method": "workspace/diagnostic",
                    "params": {},
                }
            )
        )
        after_close = process.frames.read_frame()
        assert "file:///a-pull.ddn" not in [
            item["uri"] for item in after_close["result"]["items"]
        ]

        process.send(
            frame({"jsonrpc": "2.0", "method": "$/cancelRequest", "params": {"id": 206}})
        )
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 206,
                    "method": "workspace/diagnostic",
                    "params": {},
                }
            )
        )
        cancelled = process.frames.read_frame()
        assert cancelled["error"]["code"] == -32800
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("ST23_BLACKBOX_PULL_DIAGNOSTICS_BEFORE_EOF=PASS")


def batch_payload() -> bytes:
    messages = [initialize_message(), *lifecycle_messages(), {"jsonrpc": "2.0", "method": "exit"}]
    return b"".join(frame(message) for message in messages)


def run_batch(payload: bytes) -> subprocess.CompletedProcess[bytes]:
    process = subprocess.Popen(
        [str(BINARY)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        stdout, stderr = process.communicate(input=payload, timeout=READ_TIMEOUT)
    except subprocess.TimeoutExpired as error:
        process.kill()
        process.communicate()
        raise AssertionError("batch LSP child timed out") from error
    return subprocess.CompletedProcess(process.args, process.returncode, stdout, stderr)


def check_batch_eof_compatibility() -> tuple[bytes, bytes]:
    first = run_batch(batch_payload())
    second = run_batch(batch_payload())
    assert first.returncode == 0, first.stderr.decode("utf-8", errors="replace")
    assert second.returncode == 0, second.stderr.decode("utf-8", errors="replace")
    assert first.stderr == second.stderr
    assert first.stdout == second.stdout
    responses = decode_frames(first.stdout)
    assert len(responses) == 5
    assert_initialize(responses[0])
    assert all(response["method"] == "textDocument/publishDiagnostics" for response in responses[1:4])
    assert responses[1]["params"]["diagnostics"]
    assert responses[2]["params"]["diagnostics"]
    assert responses[3]["params"]["diagnostics"] == []
    assert responses[4] == {"jsonrpc": "2.0", "id": 2, "result": None}
    assert b"panic" not in first.stderr.lower()
    print("I6_BATCH_EOF_COMPATIBILITY=PASS")
    print("PROTOCOL_REPEAT=BYTE_STABLE")
    return first.stdout, first.stderr


def check_truncated_eof() -> None:
    with LspProcess() as process:
        process.send(b"Content-Length: 100\r\n\r\n{}")
        process.close_stdin()
        assert process.wait() != 0
        stdout, stderr = process.output()
        assert stdout == b""
        assert b"panic" not in stderr.lower()
        assert b"TruncatedBody" in stderr or "잘렸습니다".encode("utf-8") in stderr
    print("I7_TRUNCATED_EOF=FAIL_CLOSED")


def check_malformed_frame() -> None:
    malformed = [
        b"Content-Length: 2\r\nContent-Length: 3\r\n\r\n{}",
        frame({"jsonrpc": "2.0", "id": 9}),
    ]
    for payload in malformed:
        with LspProcess() as process:
            process.send(payload)
            process.close_stdin()
            assert process.wait() != 0
            stdout, stderr = process.output()
            assert stdout == b""
            assert b"panic" not in stderr.lower()
    print("I8_MALFORMED_FRAME=FAIL_CLOSED")


def assert_resource_rejection(process: LspProcess) -> None:
    assert process.wait() != 0
    stdout, stderr = process.output()
    assert stdout == b""
    assert b"panic" not in stderr.lower()
    assert stderr


def check_endless_header_limit() -> None:
    with LspProcess() as process:
        process.send(b"x" * (MAX_HEADER_SECTION_BYTES + 1))
        assert_resource_rejection(process)
    print("RB06_BLACKBOX_ENDLESS_HEADER=FAIL_CLOSED")


def check_oversized_declared_body_limit() -> None:
    payload = (
        f"Content-Length: {MAX_CONTENT_LENGTH_BYTES + 1}\r\n\r\n".encode("ascii")
    )
    with LspProcess() as process:
        process.send(payload)
        assert_resource_rejection(process)
    print("RB08_BLACKBOX_OVERSIZED_DECLARED_BODY=FAIL_CLOSED")


def check_hover_before_eof() -> None:
    source = "첫함수:셈씨 := { 1 돌려줘. }\n둘함수:셈씨 := { 첫함수. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        assert_initialize(process.frames.read_frame())
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-hover.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/hover",
                    "params": {
                        "textDocument": {"uri": "file:///lsp-hover.ddn", "version": 1},
                        "position": {"line": 0, "character": 0},
                    },
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        assert response["result"]["data"]["definitionIdentity"] == "definition:local:첫함수"
        assert response["result"]["data"]["documentVersion"] == 1
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("H12_BLACKBOX_HOVER_BEFORE_EOF=PASS")


def check_definition_before_eof() -> None:
    source = "첫함수:셈씨 := { 1 돌려줘. }\n둘함수:셈씨 := { 첫함수. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["definitionProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-definition.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/definition",
                    "params": {
                        "textDocument": {"uri": "file:///lsp-definition.ddn", "version": 1},
                        "position": {"line": 1, "character": 12},
                    },
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        assert response["result"]["uri"] == "file:///lsp-definition.ddn"
        assert response["result"]["range"] == {
            "start": {"line": 0, "character": 0},
            "end": {"line": 0, "character": 3},
        }
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("G12_BLACKBOX_DEFINITION_BEFORE_EOF=PASS")


def check_document_symbol_before_eof() -> None:
    source = "새값:이름씨 := 2.\n첫함수:셈씨 := { \"🙂\" 보여주기. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["documentSymbolProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-document-symbol.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/documentSymbol",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-document-symbol.ddn",
                            "version": 1,
                        }
                    },
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        symbols = response["result"]
        assert [symbol["name"] for symbol in symbols] == ["새값", "첫함수"]
        assert [symbol["kind"] for symbol in symbols] == [13, 12]
        assert symbols[0]["selectionRange"] == {
            "start": {"line": 0, "character": 0},
            "end": {"line": 0, "character": 2},
        }
        assert symbols[1]["selectionRange"] == {
            "start": {"line": 1, "character": 0},
            "end": {"line": 1, "character": 3},
        }
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("S13_BLACKBOX_DOCUMENT_SYMBOL_BEFORE_EOF=PASS")


def check_workspace_symbol_before_eof() -> None:
    source_a = "첫함수:셈씨 := { 1 돌려줘. }\n"
    source_b = "둘함수:셈씨 := { \"🙂\" 보여주기. }\n"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["workspaceSymbolProvider"] is True
        for uri, version, source in [
            ("file:///workspace-a.ddn", 1, source_a),
            ("file:///workspace-b.ddn", 2, source_b),
        ]:
            process.send(
                frame(
                    {
                        "jsonrpc": "2.0",
                        "method": "textDocument/didOpen",
                        "params": {
                            "textDocument": {
                                "uri": uri,
                                "languageId": "ddn",
                                "version": version,
                                "text": source,
                            }
                        },
                    }
                )
            )
            assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "workspace/symbol",
                    "params": {"query": "함수"},
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        assert [item["location"]["uri"] for item in response["result"]] == [
            "file:///workspace-a.ddn",
            "file:///workspace-b.ddn",
        ]
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("WS21_BLACKBOX_WORKSPACE_SYMBOL_BEFORE_EOF=PASS")


def check_formatting_before_eof() -> None:
    source = '첫함수 : 셈씨 := {\n"🙂" 보여주기.\n}\n문자 : 글 := "🙂".'
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["documentFormattingProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-formatting.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/formatting",
            "params": {
                "textDocument": {
                    "uri": "file:///lsp-formatting.ddn",
                    "version": 1,
                },
                "options": {},
            },
        }
        process.send(frame(request))
        first = process.frames.read_frame()
        assert first["id"] == 2
        assert len(first["result"]) == 1
        assert first["result"][0]["range"]["start"] == {"line": 0, "character": 0}
        assert first["result"][0]["newText"] != source
        repeated = dict(request)
        repeated["id"] = 3
        process.send(frame(repeated))
        second = process.frames.read_frame()
        assert second["id"] == 3
        assert second["result"] == first["result"]
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("F13_BLACKBOX_FORMATTING_BEFORE_EOF=PASS")


def check_references_before_eof() -> None:
    source = "(문자:글) 첫함수:셈씨 := { 1 돌려줘. }\n둘함수:셈씨 := { (\"🙂\") 첫함수. }\n셋함수:셈씨 := { 첫함수. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["referencesProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-references.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/references",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-references.ddn",
                            "version": 1,
                        },
                        "position": {"line": 0, "character": 7},
                        "context": {"includeDeclaration": True},
                    },
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        references = response["result"]
        assert len(references) == 3
        assert references[0]["uri"] == "file:///lsp-references.ddn"
        assert references[0]["range"]["start"] == {"line": 0, "character": 7}
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("R14_BLACKBOX_REFERENCES_BEFORE_EOF=PASS")


def check_signature_help_before_eof() -> None:
    source = "(왼:수, 오른:수) 더하:셈씨 := { 0 돌려줘. }\n호출:셈씨 := { (1, 2) 더하. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["signatureHelpProvider"] == {
            "triggerCharacters": ["(", ","]
        }
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-signature-help.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/signatureHelp",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-signature-help.ddn",
                            "version": 1,
                        },
                        "position": {"line": 1, "character": 12},
                    },
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        assert response["result"]["activeParameter"] == 0
        assert response["result"]["data"]["definitionIdentity"] == "definition:local:더하"
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("SH15_BLACKBOX_SIGNATURE_HELP_BEFORE_EOF=PASS")


def check_inlay_hint_before_eof() -> None:
    source = "(왼:수, 오른:수) 더하:셈씨 := { 0 돌려줘. }\n호출:셈씨 := { (1, 2) 더하. }"
    uri = "file:///lsp-inlay-hint.ddn"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["inlayHintProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/inlayHint",
            "params": {
                "textDocument": {"uri": uri, "version": 1},
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 1, "character": 30},
                },
            },
        }
        process.send(frame(request))
        response = process.frames.read_frame()
        assert response["id"] == 2
        hints = response["result"]
        assert [hint["label"] for hint in hints] == ["왼:", "오른:"]
        assert [hint["position"] for hint in hints] == [
            {"line": 1, "character": 12},
            {"line": 1, "character": 15},
        ]
        assert hints[0]["data"]["definitionIdentity"] == "definition:local:더하"
        process.send(frame({**request, "id": 3}))
        repeated = process.frames.read_frame()
        assert repeated["result"] == hints

        changed = "(왼:수, 오른:수) 더하:셈씨 := { 0 돌려줘. }\n호출:셈씨 := { (1, 2) 더하. }"
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didChange",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "contentChanges": [{"text": changed}],
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "textDocument/inlayHint",
                    "params": {
                        "textDocument": {"uri": uri, "version": 1},
                        "range": request["params"]["range"],
                    },
                }
            )
        )
        stale = process.frames.read_frame()
        assert stale["id"] == 4
        assert stale["error"]["code"] == -32801
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "textDocument/inlayHint",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "version": 2,
                            "snapshotIdentity": "snapshot:forged",
                        },
                        "range": request["params"]["range"],
                    },
                }
            )
        )
        stale_snapshot = process.frames.read_frame()
        assert stale_snapshot["id"] == 5
        assert stale_snapshot["error"]["code"] == -32802
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {"textDocument": {"uri": uri}},
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 6,
                    "method": "textDocument/inlayHint",
                    "params": {"textDocument": {"uri": uri}},
                }
            )
        )
        closed = process.frames.read_frame()
        assert closed["id"] == 6
        assert closed["result"] == []
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("IH23_BLACKBOX_INLAY_HINT_BEFORE_EOF=PASS")


def check_rename_before_eof() -> None:
    source_a = "첫함수:셈씨 := { 1 돌려줘. }\n"
    source_b = "둘함수:셈씨 := { (\"🙂\") 첫함수. }\n"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["renameProvider"] is True
        for uri, version, source in [
            ("file:///lsp-rename-a.ddn", 1, source_a),
            ("file:///lsp-rename-b.ddn", 2, source_b),
        ]:
            process.send(
                frame(
                    {
                        "jsonrpc": "2.0",
                        "method": "textDocument/didOpen",
                        "params": {
                            "textDocument": {
                                "uri": uri,
                                "languageId": "ddn",
                                "version": version,
                                "text": source,
                            }
                        },
                    }
                )
            )
            assert_publish_diagnostics(process.frames, empty=True)
        position = {"line": 0, "character": 19}
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/prepareRename",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-rename-b.ddn",
                            "version": 2,
                        },
                        "position": position,
                    },
                }
            )
        )
        prepared = process.frames.read_frame()
        assert prepared["id"] == 2
        assert prepared["result"]["placeholder"] == "첫함수"
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "textDocument/rename",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-rename-b.ddn",
                            "version": 2,
                        },
                        "position": position,
                        "newName": "새함수",
                    },
                }
            )
        )
        renamed = process.frames.read_frame()
        assert renamed["id"] == 3
        changes = renamed["result"]["documentChanges"]
        assert [change["textDocument"]["uri"] for change in changes] == [
            "file:///lsp-rename-a.ddn",
            "file:///lsp-rename-b.ddn",
        ]
        assert all(len(change["edits"]) == 1 for change in changes)
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("SH16_BLACKBOX_RENAME_BEFORE_EOF=PASS")


def check_document_highlight_before_eof() -> None:
    source = "첫함수:셈씨 := { 1 돌려줘. }\n둘함수:셈씨 := { 첫함수. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["documentHighlightProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-document-highlight.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/documentHighlight",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-document-highlight.ddn",
                            "version": 1,
                        },
                        "position": {"line": 1, "character": 12},
                    },
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        assert len(response["result"]) == 2
        assert response["result"][0]["kind"] == 3
        assert response["result"][1]["kind"] == 2
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("HL17_BLACKBOX_DOCUMENT_HIGHLIGHT_BEFORE_EOF=PASS")


def check_semantic_tokens_before_eof() -> None:
    source = "첫함수:셈씨 := { 1 돌려줘. }\n둘함수:셈씨 := { 첫함수. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        provider = initialize["result"]["capabilities"]["semanticTokensProvider"]
        assert provider["full"]["delta"] is True
        assert provider["legend"]["tokenTypes"][0] == "function"
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-semantic-tokens.ddn",
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/semanticTokens/full",
                    "params": {
                        "textDocument": {
                            "uri": "file:///lsp-semantic-tokens.ddn",
                            "version": 1,
                        }
                    },
                }
            )
        )
        response = process.frames.read_frame()
        assert response["id"] == 2
        assert response["result"]["data"]
        assert len(response["result"]["data"]) % 5 == 0
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("ST18_BLACKBOX_SEMANTIC_TOKENS_BEFORE_EOF=PASS")


def check_semantic_tokens_delta_before_eof() -> None:
    source = "첫함수:셈씨 := { 1 돌려줘. }\n둘함수:셈씨 := { 첫함수. }"
    changed = "첫함수:셈씨 := { 2 돌려줘. }\n둘함수:셈씨 := { 첫함수. }\n셋함수:셈씨 := { 첫함수. }"
    uri = "file:///lsp-semantic-tokens-delta.ddn"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["semanticTokensProvider"]["full"]["delta"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/semanticTokens/full",
                    "params": {"textDocument": {"uri": uri, "version": 1}},
                }
            )
        )
        full = process.frames.read_frame()["result"]
        previous_id = full["resultId"]
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "textDocument/semanticTokens/full/delta",
                    "params": {
                        "textDocument": {"uri": uri, "version": 1},
                        "previousResultId": previous_id,
                    },
                }
            )
        )
        unchanged = process.frames.read_frame()["result"]
        assert unchanged["edits"] == []
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didChange",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "contentChanges": [{"text": changed}],
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "textDocument/semanticTokens/full/delta",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "previousResultId": previous_id,
                    },
                }
            )
        )
        changed_delta = process.frames.read_frame()["result"]
        assert changed_delta["edits"]
        assert changed_delta["resultId"] != previous_id
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "textDocument/semanticTokens/full/delta",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "previousResultId": "sha256:forged",
                    },
                }
            )
        )
        forged = process.frames.read_frame()["result"]
        assert isinstance(forged["data"], list)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {"textDocument": {"uri": uri}},
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 6,
                    "method": "textDocument/semanticTokens/full/delta",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "previousResultId": previous_id,
                    },
                }
            )
        )
        closed = process.frames.read_frame()["result"]
        assert closed["data"] == []
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("ST19_BLACKBOX_SEMANTIC_TOKENS_DELTA_BEFORE_EOF=PASS")


def check_open_document_navigation_before_eof() -> None:
    declaration = "공유함수:셈씨 := { 1 돌려줘. }"
    reference = "호출함수:셈씨 := { () 공유함수. }"
    uri_a = "file:///a-declaration.ddn"
    uri_b = "file:///b-reference.ddn"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["definitionProvider"] is True
        assert initialize["result"]["capabilities"]["referencesProvider"] is True
        assert initialize["result"]["capabilities"]["callHierarchyProvider"] is True
        for uri, text in ((uri_a, declaration), (uri_b, reference)):
            process.send(
                frame(
                    {
                        "jsonrpc": "2.0",
                        "method": "textDocument/didOpen",
                        "params": {
                            "textDocument": {
                                "uri": uri,
                                "languageId": "ddn",
                                "version": 1,
                                "text": text,
                            }
                        },
                    }
                )
            )
            assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "textDocument/definition",
                    "params": {
                        "textDocument": {"uri": uri_b, "version": 1},
                        "position": {"line": 0, "character": 16},
                    },
                }
            )
        )
        definition = process.frames.read_frame()
        assert definition["result"]["uri"] == uri_a
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "textDocument/references",
                    "params": {
                        "textDocument": {"uri": uri_b, "version": 1},
                        "position": {"line": 0, "character": 16},
                        "context": {"includeDeclaration": True},
                    },
                }
            )
        )
        references = process.frames.read_frame()
        assert [item["uri"] for item in references["result"]] == [uri_a, uri_b]
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 6,
                    "method": "textDocument/prepareCallHierarchy",
                    "params": {
                        "textDocument": {"uri": uri_a, "version": 1},
                        "position": {"line": 0, "character": 0},
                    },
                }
            )
        )
        declaration_item = process.frames.read_frame()["result"]
        assert declaration_item["data"]["callableIdentity"] == "definition:local:공유함수"
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 7,
                    "method": "textDocument/prepareCallHierarchy",
                    "params": {
                        "textDocument": {"uri": uri_b, "version": 1},
                        "position": {"line": 0, "character": 16},
                    },
                }
            )
        )
        assert process.frames.read_frame()["result"] == declaration_item
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 8,
                    "method": "callHierarchy/incomingCalls",
                    "params": {"item": declaration_item},
                }
            )
        )
        incoming = process.frames.read_frame()
        assert [item["from"]["uri"] for item in incoming["result"]] == [uri_b]
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 9,
                    "method": "textDocument/prepareCallHierarchy",
                    "params": {
                        "textDocument": {"uri": uri_b, "version": 1},
                        "position": {"line": 0, "character": 0},
                    },
                }
            )
        )
        caller_item = process.frames.read_frame()["result"]
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 10,
                    "method": "callHierarchy/outgoingCalls",
                    "params": {"item": caller_item},
                }
            )
        )
        outgoing = process.frames.read_frame()
        assert outgoing["result"][0]["to"] == declaration_item
        changed = "호출함수:셈씨 := { (\"🙂\") 공유함수. }"
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didChange",
                    "params": {
                        "textDocument": {"uri": uri_b, "version": 2},
                        "contentChanges": [{"text": changed}],
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 11,
                    "method": "textDocument/definition",
                    "params": {
                        "textDocument": {"uri": uri_b, "version": 1},
                        "position": {"line": 0, "character": 20},
                    },
                }
            )
        )
        stale = process.frames.read_frame()
        assert stale["id"] == 11
        assert stale["error"]["code"] == -32801
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {"textDocument": {"uri": uri_a}},
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 12,
                    "method": "textDocument/definition",
                    "params": {
                        "textDocument": {"uri": uri_b, "version": 2},
                        "position": {"line": 0, "character": 20},
                    },
                }
            )
        )
        assert process.frames.read_frame()["result"] is None
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 13,
                    "method": "callHierarchy/incomingCalls",
                    "params": {"item": declaration_item},
                }
            )
        )
        assert process.frames.read_frame()["result"] == []
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("ST20_BLACKBOX_OPEN_DOCUMENT_NAVIGATION_BEFORE_EOF=PASS")


def check_type_definition_before_eof() -> None:
    type_uri = "file:///a-type-definition.ddn"
    use_uri = "file:///b-type-use.ddn"
    type_source = "새값:이름씨 := 2."
    use_source = "(값:새값) 사용하는함수:셈씨 := { 1 돌려줘. }"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["typeDefinitionProvider"] is True
        for uri, text in ((type_uri, type_source), (use_uri, use_source)):
            process.send(
                frame(
                    {
                        "jsonrpc": "2.0",
                        "method": "textDocument/didOpen",
                        "params": {
                            "textDocument": {
                                "uri": uri,
                                "languageId": "ddn",
                                "version": 1,
                                "text": text,
                            }
                        },
                    }
                )
            )
            assert_publish_diagnostics(process.frames, empty=True)
        request = {
            "jsonrpc": "2.0",
            "id": 40,
            "method": "textDocument/typeDefinition",
            "params": {
                "textDocument": {"uri": use_uri, "version": 1},
                "position": {"line": 0, "character": 3},
            },
        }
        process.send(frame(request))
        result = process.frames.read_frame()
        assert result["result"]["uri"] == type_uri
        assert result["result"]["range"]["start"] == {"line": 0, "character": 0}
        assert result["result"]["data"]["typeIdentity"] == "type:local:새값"
        process.send(frame({**request, "id": 41}))
        assert process.frames.read_frame()["result"] == result["result"]
        process.send(
            frame(
                {
                    **request,
                    "id": 42,
                    "params": {
                        **request["params"],
                        "textDocument": {"uri": use_uri, "version": 0},
                    },
                }
            )
        )
        stale = process.frames.read_frame()
        assert stale["error"]["code"] == -32801
        process.send(
            frame(
                {
                    **request,
                    "id": 43,
                    "params": {
                        **request["params"],
                        "textDocument": {
                            "uri": use_uri,
                            "version": 1,
                            "snapshotIdentity": "snapshot:forged",
                        },
                    },
                }
            )
        )
        stale_snapshot = process.frames.read_frame()
        assert stale_snapshot["error"]["code"] == -32802
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {"textDocument": {"uri": type_uri}},
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(frame({**request, "id": 44}))
        assert process.frames.read_frame()["result"] is None
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("ST23_BLACKBOX_TYPE_DEFINITION_BEFORE_EOF=PASS")


def check_folding_range_before_eof() -> None:
    uri = "file:///folding.ddn"
    source = "공유함수:셈씨 := {\n1 돌려줘.\n}\n"
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["foldingRangeProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 14,
                    "method": "textDocument/foldingRange",
                    "params": {"textDocument": {"uri": uri, "version": 1}},
                }
            )
        )
        ranges = process.frames.read_frame()
        assert ranges["id"] == 14
        assert len(ranges["result"]) == 2
        assert ranges["result"][0]["startLine"] == 0
        assert ranges["result"][0]["endLine"] == 2
        assert ranges["result"][1]["startCharacter"] == 11
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didChange",
                    "params": {
                        "textDocument": {"uri": uri, "version": 2},
                        "contentChanges": [{"text": "공유함수:셈씨 := { 1 돌려줘. }"}],
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 15,
                    "method": "textDocument/foldingRange",
                    "params": {"textDocument": {"uri": uri, "version": 1}},
                }
            )
        )
        stale = process.frames.read_frame()
        assert stale["id"] == 15
        assert stale["error"]["code"] == -32801
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {"textDocument": {"uri": uri}},
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 16,
                    "method": "textDocument/foldingRange",
                    "params": {"textDocument": {"uri": uri, "version": 2}},
                }
            )
        )
        assert process.frames.read_frame()["result"] == []
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("ST21_BLACKBOX_FOLDING_RANGE_BEFORE_EOF=PASS")


def check_selection_range_before_eof() -> None:
    uri = "file:///selection.ddn"
    source = '공유함수:셈씨 := { "🙂" 보여주기. }\n호출함수:셈씨 := { () 공유함수. }\n'
    with LspProcess() as process:
        process.send(frame(initialize_message()))
        initialize = process.frames.read_frame()
        assert_initialize(initialize)
        assert initialize["result"]["capabilities"]["selectionRangeProvider"] is True
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didOpen",
                    "params": {
                        "textDocument": {
                            "uri": uri,
                            "languageId": "ddn",
                            "version": 1,
                            "text": source,
                        }
                    },
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 17,
                    "method": "textDocument/selectionRange",
                    "params": {
                        "textDocument": {"uri": uri, "version": 1},
                        "positions": [
                            {"line": 0, "character": 0},
                            {"line": 0, "character": 15},
                            {"line": 99, "character": 0},
                        ],
                    },
                }
            )
        )
        result = process.frames.read_frame()
        assert result["id"] == 17
        assert len(result["result"]) == 3
        assert result["result"][0]["range"]["start"] == {"line": 0, "character": 0}
        assert result["result"][2] is None
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 18,
                    "method": "textDocument/selectionRange",
                    "params": {
                        "textDocument": {"uri": uri, "version": 0},
                        "positions": [{"line": 0, "character": 0}],
                    },
                }
            )
        )
        stale = process.frames.read_frame()
        assert stale["id"] == 18
        assert stale["error"]["code"] == -32801
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "method": "textDocument/didClose",
                    "params": {"textDocument": {"uri": uri}},
                }
            )
        )
        assert_publish_diagnostics(process.frames, empty=True)
        process.send(
            frame(
                {
                    "jsonrpc": "2.0",
                    "id": 19,
                    "method": "textDocument/selectionRange",
                    "params": {
                        "textDocument": {"uri": uri, "version": 1},
                        "positions": [{"line": 0, "character": 0}],
                    },
                }
            )
        )
        assert process.frames.read_frame()["result"] == []
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 1
    print("ST22_BLACKBOX_SELECTION_RANGE_BEFORE_EOF=PASS")


def main() -> None:
    build_binary()
    golden = PACK / "golden.jsonl"
    cases = [json.loads(line) for line in golden.read_text(encoding="utf-8").splitlines() if line]
    case_ids = [case["case"] for case in cases]
    assert len(case_ids) == 17 and len(set(case_ids)) == 17
    assert all(case["expected"] == "pass" for case in cases)
    contract = json.loads((PACK / "contract.detjson").read_text(encoding="utf-8"))
    assert contract["semantic_authority_added"] is False
    assert set(contract["position_encodings"]) == {"utf-8", "utf-16", "utf-32"}

    check_initialize_before_eof()
    check_fragmented_header()
    check_fragmented_utf8_body()
    check_multiple_frames_single_write()
    check_persistent_lifecycle()
    check_pull_diagnostics_before_eof()
    check_batch_eof_compatibility()
    check_truncated_eof()
    check_malformed_frame()
    check_endless_header_limit()
    check_oversized_declared_body_limit()
    check_hover_before_eof()
    check_definition_before_eof()
    check_document_symbol_before_eof()
    check_workspace_symbol_before_eof()
    check_formatting_before_eof()
    check_references_before_eof()
    check_signature_help_before_eof()
    check_inlay_hint_before_eof()
    check_rename_before_eof()
    check_document_highlight_before_eof()
    check_semantic_tokens_before_eof()
    check_semantic_tokens_delta_before_eof()
    check_open_document_navigation_before_eof()
    check_type_definition_before_eof()
    check_folding_range_before_eof()
    check_selection_range_before_eof()
    print("LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS")


if __name__ == "__main__":
    main()
