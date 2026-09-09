# CLI state/trace hash 공유 권위 W61 인계

- goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` ACTIVE
- authority: internal SSOT v25.47.0 / RD-001~543, public SPEC v0.6.0
- baseline: `e4a698fae5119c5e0c7646023db354268f3aab29`
- product fixed: `0b4667fc1f17cebde8aaa8eee668fff3e725ed8c`
- fixed tree: `b08407cfd13fa14cf52222c694f1327ec99e629d`
- direct parent exact, merge count 0

`blake3:<hex>` state/trace wire identity와 기존 runtime profile custody constant `20.6.6`을 `ddonirang-tool::state_trace_wire`로 이동했다. teul `core/hash.rs`는 shared wire encoder와 hash authority를 소비하는 `State`/`Trace` adapter다. Historical runtime identity를 live SSOT version으로 오인해 변경하지 않았으며 hash prefix/algorithm/bytes도 보존했다.

변경 경로는 `tool/src/state_trace_wire.rs`, `tools/teul-cli/src/core/hash.rs` 두 개다. shared exact byte/hash test 1/1, existing run consumer 1/1, teul cargo check PASS, full regression 1043 PASS / 기존 동일 9 FAIL이다. `blake3:` prefix 제거 mutation은 actual RED exit101, 0/1이었고 source SHA-256 `35568e4088ea56ada2a2e5072b334074e3b908ed15998b9f587fb1d253967f48`로 exact restore 후 GREEN, residue0이다.

W58~W61은 Geoul reader, writer, state/trace wire, wire hash의 네 인접 authority family를 shared tool로 수렴한 coherent review bundle이다. 새 pack/runner/framework/meta-test/reviewer/worktree/branch 0, tracked WASM/UI/SSOT/SPEC/public membership diff 0이다.

Direct `Value` convergence는 teul과 lang의 variant/canon 차이 때문에 `CONFLICT_OR_OWNER_DECISION`이 아니라 안전한 product-seam 부재로 이번 bundle 밖에 동결했다. Existing code를 semantic authority로 승격하지 않는다.

Status is `IMPLEMENTED_PENDING_REVIEW`. Whole CLI convergence, teul authority/dependency 0 전체, physical retirement, V1 closure/readiness/release/activation/Human PASS를 주장하지 않는다.
