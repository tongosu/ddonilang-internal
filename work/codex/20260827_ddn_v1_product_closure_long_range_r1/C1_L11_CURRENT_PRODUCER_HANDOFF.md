# C1-L11 current V25 project-run convergence handoff

## Fixed target

- Product commit: `9bb3e0c96e556d5acdeacb0c220a2b4c11678a8f`
- Parent: `d7792693e2f4c403c4284eabd9a752e6634bb73d`
- Tree: `3472f615f5c24e86e6d7c997fb304690a6261c16`
- Product paths: `tool/src/ddn_runtime.rs`, `tool/src/local_project.rs`,
  `tool/src/runtime_surface.rs`

## Product behavior

Current V25 Local Project source now retains its raw source epoch through the
shared runtime rather than entering legacy preprocessing.  A project whose
linked V25 source declares its selected `움직씨` target runs that exact typed
callable.  A body-only V25 project continues through the existing shared
wrapper, so it runs with the ordinary supported-profile update callable.

The sealed dataset edit emits a typed V25 definition:

```ddn
자료값:묶음 := (@"datasets/project-runtime/envelope.json") 자료.열기.
```

No legacy source lowering, teul invocation, public syntax, SSOT, or public
SPEC change is included.

## Direct evidence

- `sealed_dataset_binding_edit_uses_verified_handle_and_real_runtime_call`: PASS
- `structural_edit_plan_supports_add_module_duplicate_and_set_entry`: PASS
- `empty_project_current_callable_runs_through_the_shared_frontdoor`: PASS
- `cargo check -p ddonirang-tool --offline`: PASS (warnings only)
- `git diff --check`: PASS before fixed commit

## Boundaries and remaining work

- This target is `PRODUCT_FIXED_PENDING_REVIEW`, not an independent PASS.
- The required producer census, generated Workbench physics workflow, Native /
  WASM parity, and mutation evidence for the broader C1-L11 two-blocker goal
  remain open.
- The earlier strict current frontdoor target remains a separate fixed target;
  this handoff does not claim its review or closure.
- V1 readiness, release, activation, legal disposition, and Human PASS remain
  unclaimed.
