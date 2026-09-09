# 공개 source 빠른 시작 후보

## 전제

- source는 sealed public projection의 clean commit이어야 한다.
- Rust와 Cargo dependency는 lockfile 기준으로 로컬에 이미 있어야 한다.
- network download 없이 offline 명령이 성공해야 한다.
- Workbench/browser 단계는 현재 R3J 범위에 없으므로 실행 성공을 주장하지 않는다.

## Rust workspace

    cargo build --workspace --locked --offline

## CLI

    cargo build --locked --offline --manifest-path tools/teul-cli/Cargo.toml
    cargo run --locked --offline --manifest-path tools/teul-cli/Cargo.toml -- --help

## WASM candidate

PowerShell에서 과업 전용 build 경로를 먼저 지정한다.

    $env:DDN_BUILD_DIR = "<absolute task-owned build directory>"
    powershell -ExecutionPolicy Bypass -File scripts/build_wasm_tool.ps1 -Profile release -Target web -CopyToUi:$false

이 명령은 기존 tracked WASM을 덮어쓰지 않는다. 출력 hash를 projection receipt와
별도로 봉인한 뒤에만 artifact 후보로 사용할 수 있다.

## 공개 검사

    python -m unittest tests.test_project_public_source tests.test_validate_public_projection

R3J의 full SPEC link와 WORKBENCH_RUNTIME role 검사는 의도적으로 fail-closed한다.
누락을 fallback으로 우회하지 않는다.
