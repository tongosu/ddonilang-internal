# DDL Wave 2 callable identity roundtrip session delta

- Writer: `tongosu <tongosu@myarts.kr>`.
- Product fixed: `02e97c9281a3e7ce43fea74b0a7c14d36ec0dff4`, direct parent `fe7ba526132ccc5947769be74f75fa17dfe1bf26`, merge 0.
- Implemented an internal two-profile callable projection with ordered ParamPin, type, relation, result-type, callable-kind, and definition identity binding.
- Added one callable-focused integration test, reusing the existing lang test package; no pack, runner, dependency, runtime, CLI, WASM, or public-wire artifact was created.
- P01–P12, N01–N18, M1–M3 RED/exact-restore/GREEN, Wave 1 regression, full lang regression, cargo check, and diff check passed.
- Handoff is documentation-only custody. Next state is `PRODUCT_FIXED_READY_FOR_INDEPENDENT_REVIEW`; no broad DDL or V1 closure claim is made.
