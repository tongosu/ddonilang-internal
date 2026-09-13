# Fixed64 moving-average checked-arithmetic handoff

- Product: `7540a5900fcd18b2cd7bb0959d5b4557624158d3`
- Tree: `7ff0d43f43b1d4571d2184d6828877ff276371ee`
- Parent: `66c701a02675fe7dc6c6f543aeb7d7cd23c36e67`
- Product path: `tool/src/ddn_runtime.rs`

The active `필터.이동평균` builtin now uses checked Fixed64 accumulation.
An overflow before averaging is returned as `E_RUNTIME_ARITH_OVERFLOW`; the
runtime returns no successful update output.

Evidence:

- focused moving-average overflow test — PASS
- normal filter regression was retained in `stdlib_l1_filter_builtins`
- `git diff --check` — PASS before product commit

Mutation M1 restored saturating accumulation. The overflow fixture then produced
a success output, making the focused test RED. The checked operation was restored
before the product commit.

Nonclaims: this is one active caller slice only; it is not a full Fixed64 caller
audit, a tracked-WASM freshness result, or independent review verdict.
