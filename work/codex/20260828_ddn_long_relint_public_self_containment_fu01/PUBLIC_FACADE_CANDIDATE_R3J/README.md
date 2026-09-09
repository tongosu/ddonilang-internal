# 또니랑 공개 저장소 첫 화면 후보

또니랑은 한국어 중심 프로그래밍 언어와 Rust 실행 도구, CLI, WASM 및 셈그림
Workbench를 함께 개발하는 프로젝트다.

이 문서는 공개 배포본이 아니라 G22 facade candidate다. 현재 검증된 R3J는
language/runtime, CLI, required/tracked WASM, public Language SPEC v0.6.0과 제한된
conformance closure를 포함하는 non-browser projection이다.

현재 공개 projection에 아직 포함되지 않은 항목:

- Workbench와 Workbench runtime 전체
- selected examples와 projectile lesson
- sealed offline browser dependency bundle
- public SPEC CURRENT가 연결하는 역사·후보 tree 10개
- 확정 LICENSE, NOTICE와 권리 결속

따라서 이 후보는 public release, stable default, Human PASS 또는 사용 허가를
발행하지 않는다. 언어 공개 권위 진입점은 publish/spec/CURRENT.md이며, source와
artifact의 검증 고정점은 함께 제공되는 projection receipt를 따른다.

## 제한 후보에서 가능한 확인

    cargo build --workspace --locked --offline
    cargo run --locked --offline --manifest-path tools/teul-cli/Cargo.toml -- --help

WASM build는 scripts/build_wasm_tool.ps1을 사용하되 로컬 Rust target과 wasm-pack 또는
wasm-bindgen이 이미 설치돼 있어야 한다. tracked WASM은 source-built artifact와 현재
다르므로 release artifact로 승격되지 않았다.

## 상태

- public main과 stable release는 서로 다른 관문이다.
- public syntax, stable wire, SSOT promotion은 이 facade가 결정하지 않는다.
- Workbench browser workflow는 full-scope projection과 실제 Edge 검증 전까지 OPEN이다.
- 권리와 license가 UNKNOWN인 path는 public projection에서 제외한다.
