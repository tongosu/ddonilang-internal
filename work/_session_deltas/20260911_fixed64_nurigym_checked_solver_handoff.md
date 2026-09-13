# Fixed64 Nurigym checked solver handoff

## Fixed target

- Product commit: `063f510bd454e1713a3e6bc420239dbeb11a6ff5`
- Tree: `36616c13d1d71eda17e2accabd08b72f8af1e704`
- Parent: `c31dfcb71a903688823f0d9069478d7643e8bd8a`

CartPole and Pendulum now build complete candidate states through checked
Fixed64 operations, then replace the live state only after every operation
succeeds.  Overflow returns the existing arithmetic-overflow taxonomy as
`E_NURIGYM_ARITH_OVERFLOW`; it cannot advance the solver or publish a partial
step.

## Validation

- `cargo test -p ddonirang-core nurigym -- --nocapture`: PASS (6 tests).
- `cargo test -p ddonirang-core`: PASS (134 tests).
- `cargo check -p ddonirang-core --offline`: PASS.
- `git diff --check`: PASS.

## Mutation evidence

- M1 CartPole velocity/friction multiplication changed to saturation: RED;
  the overflow test received a success step.  Exact restore:
  `cartpole.rs` SHA-256
  `1C0C2DD75D2601889D7C6F6108AB97ED938D902C31CC2E8E6CD85EF9D3E255EB`,
  blob `35c64ec2e9124e15b6214e1bd01bc5262a7f2e81`; GREEN.
- M2 Pendulum theta/gravity multiplication changed to saturation: RED; the
  overflow test received a success step.  Exact restore:
  `pendulum.rs` SHA-256
  `28BD6D3D0107E40307A55E71AAE906B527FAF2BB6A1529EA759E5A53A65A7932`,
  blob `f9be0db157d30ffb7c1659249760565fe1517ed6`; GREEN.

## Nonclaim

This target covers the current Nurigym CartPole and Pendulum solver callers,
not every historical/deferred Fixed64 use, public release, or Human PASS.  It
is ready for independent review and has no self-issued verdict.
