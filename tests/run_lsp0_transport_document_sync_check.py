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
            assert_no_frame(process.frames)
        process.send(frame(lifecycle_messages()[-1]))
        assert process.frames.read_frame() == {"jsonrpc": "2.0", "id": 2, "result": None}
        assert process.process.poll() is None
        process.send(frame({"jsonrpc": "2.0", "method": "exit"}))
        assert process.wait() == 0
    print("I5_PERSISTENT_LIFECYCLE=PASS")


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
    assert len(responses) == 2
    assert_initialize(responses[0])
    assert responses[1] == {"jsonrpc": "2.0", "id": 2, "result": None}
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
    check_batch_eof_compatibility()
    check_truncated_eof()
    check_malformed_frame()
    print("LSP0_TRANSPORT_DOCUMENT_SYNC_CHECK=PASS")


if __name__ == "__main__":
    main()
