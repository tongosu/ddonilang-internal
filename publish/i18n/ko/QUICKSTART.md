# 1분 첫 실행 — 또니랑

> 한국어 기준 안내

## 1. Requirements

- Rust + Cargo
- Git
- Optional for Seamgrim workspace: Python 3

## 2. Build the CLI

~~~sh
cargo build --manifest-path tools/teul-cli/Cargo.toml
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- --help
~~~

## 3. Run the first DDN example

~~~sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
~~~

출력에서 23, 15, 8을 확인하세요.

## 4. Optional Seamgrim workspace

~~~sh
python solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
~~~

Open: http://localhost:8787/

The workspace contains multiple examples, but not every docs-first language surface is implemented
in the default browser product. Check the [product support matrix](../../PRODUCT_SUPPORT_CURRENT.md).

## 5. Next

- [Localized introduction](README.md)
- [Korean learning path](../../LEARNING_PATH.md)
- [Public Language SPEC](../../spec/CURRENT.md)
