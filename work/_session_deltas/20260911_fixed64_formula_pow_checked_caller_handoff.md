# Fixed64 checked formula-power caller handoff

- Product: `d20245102840ba26b861a958b9a2204e2007e79c`
- Tree: `a2b90fe7c2dc12388d5f2637b0406c1312557d7f`
- Parent: `baab85d23bf2ce73ff5839855eebab6c152bae79`
- Product path: `tool/src/ddn_runtime.rs`
- Fixed blob: `95b6128195f9de71069a3d2018504bf216c883eb`
- Fixed SHA-256: `89e3f6ababa349dbe6e28b26a4fd62eb6470b47fc1337aeeea91504a1cd6e824`

## Claim

The formula AST `^` evaluator no longer uses saturating `UnitValue::mul` for
positive integer powers.  Each multiplication now consumes `Fixed64` through
`checked_mul`, preserving dimension composition and emitting typed overflow.

## Gates and mutations

- Focused formula-power overflow test — PASS.
- Existing runtime `powi` overflow tests — PASS.
- Native and WASM offline tool-library checks — PASS.
- M1 restored `result.value * base.value`: focused formula power overflow
  test RED because it returned saturated `Fixed64::MAX`.
- M2 downgraded checked overflow through `unwrap_or(Fixed64::MAX)`: the same
  focused test RED.

After both mutations, source restored exactly to blob `95b61281…` and
SHA-256 `89e3f6ab…`, then focused gates GREENed.

## Review boundary

Ready for independent review: YES.  This target covers only formula AST
integer-power evaluation, not public f64 ingress, transcendentals, all callers,
release, or Human PASS.
