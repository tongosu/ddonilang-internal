# SRE-U1 tracked WASM freshness R1.1 — custody correction handoff

## Immutable predecessor

```text
PRODUCT_COMMIT = be6e56cf5dda3afa38738cce8e19468e7920f5c1
PRODUCT_TREE = 1e9a6b38dde7facc0fec8eb305d3c7f635be5592
PRODUCT_PARENT = 4971b76c18a039f93fda01fbb744a80ed19100b1
PREDECESSOR_HANDOFF = ff8316046c9d7651bf2ec6d94acc6caa2000bc5b
```

The product commit, tracked artifact, and tracked manifest are unchanged. This
docs-only successor corrects one custody value in the predecessor handoff.

## Corrected identity

The predecessor handoff retained the correct manifest Git blob but recorded an
incorrect SHA-256 value. The raw bytes were independently recomputed from the
immutable product Git object.

| Path | Git blob | predecessor recorded SHA-256 | corrected raw Git blob SHA-256 |
| --- | --- | --- | --- |
| `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` | `7bdecd2206353557ce1b40465fec23bf78f42578` | `9193D07F0438056F111A17250E81F39312DEBAF92CCE8E26D7E8A7EE2DF9CAC2` | unchanged |
| `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson` | `f35010928a26e4bc3755e2089c725ae858183672` | `3A1E2409AB46F1A280724717EBD6C2DB7A2E205C3262F82743FBEE3AA873CCD6` | `CF4AE8F3B6D4DF60101101B029046772012058BDE4C4F31A6FDFE1A5ED7015E3` |

The correction was established by hashing the raw `git show
be6e56cf5dda3afa38738cce8e19468e7920f5c1:<path>` bytes. The manifest is
LF materialized and has 35,028 bytes.

## Re-review boundary

Re-review the same freshness-only claim:

- official release/web builder output equals the tracked WASM artifact;
- manifest source-tree and artifact binding pass the existing freshness checker;
- stale predecessor artifact and tampered source-tree manifest are rejected;
- the existing SRE-U1 source/runtime and WASM-library focused gates remain green.

No source semantics, public API, JavaScript lowering, tracked artifact bytes,
manifest content, SSOT, public SPEC, release, or V1 readiness claim changed.
