# Fixed64 Realm atomic-batch restore-evidence correction

This is a docs-only correction to the handoff at
`a4a2ca0a6de02ce4c93cead8addbf907e569b407`. It does not alter the immutable
Realm product target or its behavior.

## Correct target binding

- Product commit: `4306c0f6009b17fa43af8201bd96da825caf02b5`
- Tree: `a959833f979fda117d6756d083b856577ff81e35`
- Parent: `bf22e4823721a4a86d7cec898089b1c0d3a3347c`
- Product path: `core/src/realms.rs`
- Exact target blob: `7484f4fb94fb140d97630d19a88b0244a82f3e84`
- Exact target-file SHA-256: `1E33740BBAAEBA2A0E1B2DFDE3A603D28DE8B94420ACC779BAE1AADC606825AB`

The earlier handoff's quoted restore blob and SHA-256 did not identify the
immutable target bytes. They are superseded only for restore-evidence custody
by the values above. The original handoff remains preserved unchanged.

## Re-review request

The independent reviewer has already verified the code and tests for the
target: focused Realm tests 3/3 PASS, full `ddonirang-core` 137/137 PASS, and
`git diff --check` PASS. Re-review is limited to confirming this exact raw
target binding and the existing M1/M2 mutation claims; it is not a request to
broaden Fixed64, V1, release, or Human claims.
