# トニラン (Ddonilang) (日本語)

> 韓国語を中心に、再現可能なプログラム・シミュレーション・学習実験を作る言語とツールです。

Translation status: **スターター翻訳・Human review open**

## 1分で最初の実行

~~~sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
~~~

出力に 23、15、8 が含まれることを確認してください。

## 現在の状態

- Public Language SPEC: **v0.5.0 / docs-first current**
- GitHub development trunk: **protected main**
- Public CI: code tests + public golden + SPEC seal + first example
- Full browser product + Human review: **OPEN by feature**
- Internal SSOT and public SPEC use separate version lineages.

## 主な文書

- [Quick start](QUICKSTART.md)
- [Korean project introduction](../../../README.md)
- [Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md)
- [Public Language SPEC](../../spec/CURRENT.md)
- [All languages](../INDEX.md)

## Boundary

This starter translation helps navigation. It does not define DDN language semantics or promote
docs-first features to implemented product support. Keep DDN code, commands, paths, schema names,
and error codes canonical.
