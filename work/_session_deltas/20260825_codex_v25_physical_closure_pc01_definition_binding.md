# [언어물리Codex -> 제품구조Chat] V25 PC-01 Definition / Binding session delta

- Program: `DDN_V25_PHYSICAL_CLOSURE_LONG_RANGE_R1`
- PC-00 custody commit: `55f57623ab419d9ccb99b9e0527efa912eaccee3`
- PC-01 implementation: `cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6`
- Test-format successor: `3ac1cefbffa4c00857f99debad3b1aad24ed08ea`
- Result: Definition `:=` and Binding/Rebinding `<-` now have distinct shared
  lexer/AST/parser/canon identities and an explicit V25 runtime reader.
- Evidence: lang 263+3 PASS, runtime 1 PASS, workspace check PASS, mutations
  3 RED→GREEN with residue 0.
- Default product frontdoors remain unchanged; PC-02 is blocked on independent
  plain PASS.
- SSOT/SPEC/tracked WASM changes: 0.
- Deep Research: `NOT_USE`; the live internal authority and product source were sufficient.
