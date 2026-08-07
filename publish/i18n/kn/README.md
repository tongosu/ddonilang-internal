# Ddonilang (ಕನ್ನಡ)

> ಪುನರುತ್ಪಾದಿಸಬಹುದಾದ programs, simulations ಮತ್ತು learning experiments ಗಾಗಿ Korean-first ಭಾಷೆ ಮತ್ತು tools.

Translation status: **Starter translation; Human review open**

## ಒಂದು ನಿಮಿಷದ ಮೊದಲ run

~~~sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
~~~

Output ನಲ್ಲಿ 23, 15 ಮತ್ತು 8 ಇವೆ ಎಂದು ಪರಿಶೀಲಿಸಿ.

## ಪ್ರಸ್ತುತ status

- Public Language SPEC: **v0.5.0 / docs-first current**
- GitHub development trunk: **protected main**
- Public CI: code tests + public golden + SPEC seal + first example
- Full browser product + Human review: **OPEN by feature**
- Internal SSOT and public SPEC use separate version lineages.

## ಮುಖ್ಯ documents

- [Quick start](QUICKSTART.md)
- [Korean project introduction](../../../README.md)
- [Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md)
- [Public Language SPEC](../../spec/CURRENT.md)
- [All languages](../INDEX.md)

## Boundary

This starter translation helps navigation. It does not define DDN language semantics or promote
docs-first features to implemented product support. Keep DDN code, commands, paths, schema names,
and error codes canonical.
