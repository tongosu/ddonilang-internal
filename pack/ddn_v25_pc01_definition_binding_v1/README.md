# DDN V25 PC01 Definition / Binding pack

This executable pack seals the V25 source-epoch distinction between Definition
(`:=`) and Binding/Rebinding (`<-`). The pack is consumed by the production
`ddonirang-lang` lexer, parser, canonicalizer, and normalizer through
`lang/tests/v25_definition_binding_pack.rs`.

- `positive_definition_binding.ddn`: a Definition followed by a Rebinding.
- `negative_old_equals.ddn`: pre-V25 top-level `=` must not silently enter V25.
- `negative_binding_as_definition.ddn`: `<-` cannot introduce a `채비` name.
- `expected.jsonl`: the single case/result oracle used by the Rust test.

The historical `parse` entrypoint remains a pre-V25 reader for migration
custody during PC01. V25 programs must enter through `parse_v25`; PC02 owns the
shared product-frontdoor switch.
