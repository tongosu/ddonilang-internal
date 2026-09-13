# PG-CLI-01 manifest custody correction

This docs-only successor corrects a handoff evidence typo found by the independent
review of product `f9261848bd90c6554952e80a1ffb1dcbed24158e` (tree
`caf1a8f777d48efb52d6ec46980a98030632810a`). No product path or product byte
changes in this commit.

The tracked `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
at that exact product target hashes to:

`00BCF3BD7612C56AAC5FD34996EA5BC851FF7F72EE20BF5F4D7F0B982F8FA2E0`

The prior handoff mistakenly recorded `A252CDF8F6D2ACF85D95DF1333FCA6052E50AB0854645020BF1112D4D55C013D`.
The WASM artifact hash remains correctly recorded as
`37BD0588B55A9742A82C993A0B51E0ACA1F61B3749EC284C288F193F25A335DB`.

Independent review rerun is requested against the same immutable product target
and this correction handoff. The review finding concerns custody evidence only;
it does not authorize a self-issued product PASS.
