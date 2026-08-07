# Downloads — Ddonilang

> Başlangıç çevirisi; Human review open

## Current distribution boundary

- A stable end-user binary release is not claimed by this document.
- Until a verified GitHub Release is published, build and run from source using
  [QUICKSTART.md](QUICKSTART.md).
- Do not treat planned platform names or archive examples as released products.

## Source build

~~~sh
cargo build --manifest-path tools/teul-cli/Cargo.toml
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- --help
~~~

## Future release requirements

A public binary release should provide an OS/architecture label, a version, SHA-256 checksums,
license and notice files, and verification notes. Repository source and release binaries have
separate publication gates.

[Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md)
