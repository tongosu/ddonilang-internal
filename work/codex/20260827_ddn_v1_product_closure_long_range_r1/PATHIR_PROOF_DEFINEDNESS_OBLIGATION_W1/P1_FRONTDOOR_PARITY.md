# PathIR/Proof XP02·XP05·XP06 successor frontdoor parity

| Frontdoor | Successor status |
|---|---|
| symbolic library/API | checked closure and obligation generation PASS |
| proof library/API | typed request, independent checker, execution/check/report/receipt chain PASS_INTERNAL |
| official CLI | P0 fail-closed preserved; positive checked-assumption ingress OPEN |
| raw DDN | P0 fail-closed preserved; authorized checked-assumption syntax absent |
| tracked WASM | rebuilt/fresh/deterministic; raw fail-closed PASS; positive assumption transport OPEN |
| Workbench project-run | existing structured consumer unchanged; positive assumption mapping OPEN |

No JS/Python layer reconstructs assumptions or obligations. No diagnostic text,
environment variable, host option, global mutable context or source sniffing is
used as checked evidence.

Current counters:

```text
SEMANTIC_FIELD_LOSS_INTERNAL_TYPED_CHAIN: 0
SEMANTIC_FIELD_LOSS_PUBLIC_FRONTDOORS: NOT_PROVEN
JS_SEMANTIC_RECONSTRUCTION: 0
HIDDEN_ASSUMPTION_FALLBACK: 0
PARTIAL_RESULT_PUBLISH: 0
PARTIAL_STATE_PUBLISH: 0
FAILED_OUTBOX_RELEASE: 0
```

## Exact physical decision gates

### OD-PATHIR-P1-01 — structured registry and frontdoor projection

Options:

1. One sealed versioned request/result/report/receipt registry, then project the
   same typed object into CLI/WASM/Workbench. Recommended: clearest authority
   and identity boundary.
2. Extend the legacy proof verify JSON schema. Lower file count, but mixes old
   verifier semantics with checked-obligation authority and raises migration
   risk.
3. Keep internal-only. Safest immediate compatibility, but XP-02/public parity
   remains blocked.

Required exact decisions: registry path/version, field spellings,
required/optional fields, identity participation, failure diagnostic, CLI option,
WASM transport field and Workbench mapping.

### OD-PATHIR-P1-02 — raw DDN assumption surface

Options:

1. Keep raw DDN fail-closed until the structured registry is reviewed.
   Recommended.
2. After registry approval, project the same typed bundle through an existing
   morphology-compatible source role.
3. Introduce a new raw syntax now. Not recommended because the exact syntax,
   migration and diagnostic contract are OPEN.

Affected current paths include
`tools/teul-cli/src/cli/symbolic.rs`,
`tools/teul-cli/src/cli/proof.rs`, `tool/src/wasm_api.rs` and the existing
Workbench structured consumer. No changes were made to them.
