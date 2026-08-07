# Erster Lauf in einer Minute — Ddonilang

> Starter-Übersetzung; Human review open

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

Prüfen Sie, dass die Ausgabe 23, 15 und 8 enthält.

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
