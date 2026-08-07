# Ddonilang (Deutsch)

> Eine koreanisch ausgerichtete Sprache und Werkzeugkette für reproduzierbare Programme, Simulationen und Lernexperimente.

Translation status: **Starter-Übersetzung; Human review open**

## Erster Lauf in einer Minute

~~~sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
~~~

Prüfen Sie, dass die Ausgabe 23, 15 und 8 enthält.

## Aktueller Status

- Public Language SPEC: **v0.5.0 / docs-first current**
- GitHub development trunk: **protected main**
- Public CI: code tests + public golden + SPEC seal + first example
- Full browser product + Human review: **OPEN by feature**
- Internal SSOT and public SPEC use separate version lineages.

## Hauptdokumente

- [Quick start](QUICKSTART.md)
- [Korean project introduction](../../../README.md)
- [Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md)
- [Public Language SPEC](../../spec/CURRENT.md)
- [All languages](../INDEX.md)

## Boundary

This starter translation helps navigation. It does not define DDN language semantics or promote
docs-first features to implemented product support. Keep DDN code, commands, paths, schema names,
and error codes canonical.
