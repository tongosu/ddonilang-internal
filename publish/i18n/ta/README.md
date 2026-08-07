# Ddonilang (தமிழ்)

> மீண்டும் உருவாக்கக்கூடிய programs, simulations மற்றும் learning experiments க்கான Korean-first மொழி மற்றும் tools.

Translation status: **Starter translation; Human review open**

## ஒரு நிமிட முதல் run

~~~sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
~~~

Output இல் 23, 15, 8 இருப்பதை உறுதிப்படுத்தவும்.

## தற்போதைய status

- Public Language SPEC: **v0.5.0 / docs-first current**
- GitHub development trunk: **protected main**
- Public CI: code tests + public golden + SPEC seal + first example
- Full browser product + Human review: **OPEN by feature**
- Internal SSOT and public SPEC use separate version lineages.

## முக்கிய documents

- [Quick start](QUICKSTART.md)
- [Korean project introduction](../../../README.md)
- [Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md)
- [Public Language SPEC](../../spec/CURRENT.md)
- [All languages](../INDEX.md)

## Boundary

This starter translation helps navigation. It does not define DDN language semantics or promote
docs-first features to implemented product support. Keep DDN code, commands, paths, schema names,
and error codes canonical.
