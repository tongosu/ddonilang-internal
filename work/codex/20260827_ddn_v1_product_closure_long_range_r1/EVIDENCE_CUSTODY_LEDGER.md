# V1 census evidence custody ledger

이 대장은 기존 완료·검토·후보 evidence를 V1 census에서 잃거나 과대 일반화하지 않기 위한 1차 색인이다.

| track | target/evidence | current census use | successor impact |
|---|---|---|---|
| ForEach/current item | `a633c43f93299c3ec60151857e6aeb54c1d852ae` PASS | control-flow의 scoped evidence | UNAFFECTED, broad closure 아님 |
| field surface | `ab16db245f7ff7234cc604923e527355f5b7d53a` closure | Product field-access scoped evidence | UNAFFECTED |
| execution concurrency W1B | `0d8ca402...` PASS / `c61bdfef...` closure | shared async canon history | UNAFFECTED, public provider/rendezvous OPEN |
| W1C1 | `c8b0f3d4...` PASS / `eca2fbc5...` closure | route/internal provider scoped evidence | UNAFFECTED |
| W1D~F | `091a08d1...` PASS / `ccee4366...` closure | logical delivery/wait/outbox scoped evidence | UNAFFECTED |
| W1C2 I1/I2 | `3c1a8956...`, `433dd6e3...` PASS / `af7ad522...`, `40cd0473...` closure | internal typed provider/runtime dispatch | UNAFFECTED, public syntax/wire OPEN |
| Canonical View T5 | `905efb4a...` program closure; T5A~G predecessors | canonical payload scoped evidence | ADDITIVE; current T5F grid deferred |
| Workbench physics creator | `de9cb9ed...` G30 plain PASS | historical fixed-target product loop | REBASE_REQUIRED for current V25 frontdoor |
| RD-206 | `0e3de501...` handoff, later targeted PASS closure | receipt/replay scoped evidence | ADDITIVE; RD-207 wire OPEN |
| WorkCostV1 | `cdfb7d36...` closure | resource totality/standard-limits scoped evidence | UNAFFECTED |
| Definition/Binding PC01 | `b8530bd6...` fixed product, `daabc118...` final handoff | current local evidence | REBASE_REQUIRED until fresh verdict |
| G14 rejection parity | RELINT completion handoff | current local/detached evidence | REBASE_REQUIRED until fresh verdict |
| Tensor R1 | v25.8.2 docs-first SSOT lineage | semantic authority only | PRODUCT_OPEN |
| Generic/구실 | RD-232~238 docs-first + prior limited RD-204 evidence | semantic/scoped history | PRODUCT_OPEN |
| Morphology/multisurface | `lang/src/dialect.rs`, `term_map.rs`, canon packs | partial product inventory | UNKNOWN broad closure |
| Regex | proposal/legacy runtime paths | future horizon preservation | OPTIONAL V1 / required V1.5 candidate |
| Proof | `tool/src/proof/**`, AGE packs | experimental/scoped history | OPTIONAL V1 / product OPEN |
| State Machine | transition packs and legacy runtime | experimental history | DEFERRED V1 |
| dependency/lock | local project packs and RD-213/231 | partial product inventory | PRODUCT_OPEN |
| public projection | `c3c65ae2...`, `fab6315c...`, RELINT R2 receipt | deterministic candidate evidence | self-containment/rights OPEN |

`PASS`는 정확한 fixed target과 scope에만 결속한다. predecessor evidence가 있다는 이유로 현재 capability 전체를 `IMPLEMENTED_VERIFIED`로 올리지 않는다.
