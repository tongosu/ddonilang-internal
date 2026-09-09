# DDL Wave 1 coverage correction handoff

## Target

- Original product fixed: `2809a7a1b0489d164bf6a418c8cbf5de59c6dfb9`
- Original review: `FAIL_TARGET_BOUND`, one blocking finding
- Correction product fixed: `f3507fd9591baba7f91bcf6f1a28cbdbdebd4e1c`
- Parent: `99862e5147cb29ad34f7db0eb6c7712d2fd8d371`
- Scope: exact DDL Wave 1 assertion coverage correction

## Correction

The parser now accepts a fixed internal `DdlWave1Context` for registry
integrity validation. It remains a Rust-side context only: no DDL wire, CLI,
WASM, runtime, ordinary parser, or public registry surface changed.

The DDL test adds actual assertions for P06 UTF-8 byte spans, P10
presentation-only section ordering, and N05/N11/N12/N13/N14/N18/N19.

## Evidence

- Positive coverage: 10/10
- Negative coverage: 20/20
- Focused DDL test: 11/11 PASS
- Clean snapshot language regression: 372 unit + 11 DDL integration + 4 V25 integration PASS
- Clean snapshot `cargo check -p ddonirang-lang`: PASS
- DDL-path `rustfmt --check`: PASS
- Product diff check: PASS
- CM1 character-offset span mutation: RED -> exact restore -> GREEN
- CM2 section-order-derived identity mutation: RED -> exact restore -> GREEN

The validation snapshot was derived from `99862e...` and received only this
DDL-owned diff. Shared LSP and other dirty language paths were neither
modified nor staged.

## Boundaries

This is ready for rereview of the original Wave 1 target plus this successor.
It does not claim full DDL, public DDL, CLI/WASM/wire/IDE support, P0-P6,
V1 readiness, release, activation, legal approval, or Human PASS.
