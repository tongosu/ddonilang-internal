# 빠른 시작

> 처음 배우는 사용자는 작업실을 연 뒤 `3. 10분 첫 실행`만 먼저 따라하면 됩니다.
> 전체 문법은 [학습 지도](LEARNING_PATH.md)의 0~5층에서 필요한 때 순서대로 배웁니다.

## 1. 소스 빌드

필요: Rust + Cargo

```sh
cargo build --release
```

CLI 확인:

```sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- --help
```

## 2. 셈그림 작업실 실행

로컬 서버를 시작합니다.

```sh
python solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
```

브라우저에서 엽니다.

```txt
http://localhost:8787/
```

작업실에서는 `예제` 탭에서 다음 rail을 바로 열 수 있습니다.

- console-grid 최소 예제
- space2d 진자/평면 공 튕김 실험
- console-grid 테트리스
- 수식 정리, 세움 동치 증명, 람다 저장/반환

예제 목록은 `solutions/seamgrim_ui_mvp/samples/index.json`에 있습니다.

## 3. 10분 첫 실행

1. 작업실의 DDN 편집기에 다음 코드를 넣습니다.

```ddn
x <- 15.
y <- 8.
합 <- (x + y).

"첫 결과" 보여주기.
합 보여주기.
x 보여주기.
y 보여주기.
```

2. `실행`을 누르고 결과 로그에서 `23`, `15`, `8`을 확인합니다.
3. `x <- 15.`의 `15`를 다른 숫자로 바꾸고 다시 실행합니다.

이 단계에서는 이름, 값, 계산, `<-`, 문장 끝 `.`, `보여주기`만 배웁니다.
씨자리·이름씨·계약·구실은 아직 몰라도 됩니다.

파일로 실행하려면 [`examples/00_first_result.ddn`](examples/00_first_result.ddn)을 사용합니다.
반복되는 구조화 결과를 공개하는 `보임`은 학습 지도 1층입니다. 현재 기본 배포 포함 여부는
[현재 제품 지원 상태](PRODUCT_SUPPORT_CURRENT.md)를 확인합니다.

## 4. 제품 회귀 확인

대표 제품 smoke:

```sh
python tests/run_seamgrim_product_stabilization_smoke_check.py
```

grid/space2d 예제 runner:

```sh
node tests/seamgrim_sample_grid_space_runner.mjs
```

작업실 레이아웃/실행바 계약:

```sh
node tests/seamgrim_studio_layout_contract_runner.mjs
node tests/seamgrim_run_toolbar_compact_runner.mjs
```

4권 current-line raw bundle parity:

```sh
python tests/run_ddonirang_vol4_bundle_cli_wasm_parity_check.py
```

## 5. 바이너리 실행

GitHub Releases에 배포된 바이너리가 있는 경우 OS에 맞는 파일을 내려받아 실행합니다.

예시:

- Windows: `.\ddonirang-tool.exe --help`
- macOS/Linux: `chmod +x ./ddonirang-tool` 후 `./ddonirang-tool --help`

체크섬이 제공되면 검증합니다.

```sh
sha256sum -c SHA256SUMS.txt
```

## 관련 문서

- 공개 언어 스펙: `publish/spec/CURRENT.md`
- 문서 인덱스: `publish/INDEX.md`
- 단계별 학습 지도: `publish/LEARNING_PATH.md`
- 현재 제품 지원 상태: `publish/PRODUCT_SUPPORT_CURRENT.md`
- 개발 구조: `publish/DDONIRANG_DEV_STRUCTURE.md`
