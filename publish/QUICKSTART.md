# 빠른 시작

> 처음에는 CLI에서 작은 프로그램 하나를 실행합니다. 전체 문법과 셈그림 작업실은
> 그 다음에 필요할 때 확인하세요.

## 1. 준비

필요한 도구:

- Rust와 Cargo
- 저장소를 내려받을 Git
- 선택 사항: 셈그림 작업실용 Python 3

CLI를 빌드하고 도움말을 확인합니다.

```sh
cargo build --manifest-path tools/teul-cli/Cargo.toml
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- --help
```

## 2. 1분 첫 실행

저장소에 포함된 첫 예제를 실행합니다.

```sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
```

예제 내용:

```ddn
x <- 15.
y <- 8.
합 <- (x + y).

"첫 결과" 보여주기.
합 보여주기.
x 보여주기.
y 보여주기.
```

출력에서 `23`, `15`, `8`을 확인합니다. 숫자를 바꾸고 다시 실행해 결과가 바뀌는지
확인하면 첫 단계가 끝납니다.

이 단계에서는 이름, 값, 계산, `<-`, 문장 끝 `.`, `보여주기`만 알면 됩니다.
씨자리·이름씨·계약·구실·모형·풀이기는 아직 몰라도 됩니다.

## 3. 셈그림 작업실 열기(선택)

로컬 서버를 시작합니다.

```sh
python solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
```

브라우저에서 다음 주소를 엽니다.

```text
http://localhost:8787/
```

작업실에는 여러 예제와 보기 경로가 있지만, 모든 docs-first 문법이 기본 브라우저
제품에 구현됐다는 뜻은 아닙니다. 실행 전 [현재 제품 지원 상태](PRODUCT_SUPPORT_CURRENT.md)를
확인하세요.

## 4. 개발자용 공개 검사

GitHub `main`의 필수 공개 검사는 코드·공개 golden·공개 SPEC seal·첫 예제를
검증합니다.

```sh
python tools/check_public_language_spec.py
python tools/check_public_docs.py
```

전체 Workbench browser·Human 검토와 private SSOT 기반 제품 관문은 별도입니다.

## 5. 다음 문서

- [0~5층 학습 지도](LEARNING_PATH.md)
- [현재 제품 지원 상태](PRODUCT_SUPPORT_CURRENT.md)
- [공개 Language SPEC](spec/CURRENT.md)
- [다국어 시작 문서](i18n/INDEX.md)
- [다운로드 안내](DOWNLOADS.md)

공개 바이너리가 GitHub Releases에 올라오기 전에는 소스 실행이 기준입니다.
