# [DDN V1제품마감Codex -> Codex관리Work] P2 local-project saved-head run custody W1

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex local task
- AI_CAPABILITY: product single-writer implementation and evidence sealing
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: DDN V1 closure execution owner / file owner
- RETURN_LABEL: `[DDN V1제품마감Codex -> Codex관리Work]`
- DEEP_RESEARCH_CHECK: NOT_USE; fixed repository product and authority evidence determined the implementation.

## Result

At live CURRENT v25.35.0 / RD-001~490, the existing P2 local-project store and HTTP API now optionally bind Run creation to an expected saved project HEAD. The check occurs before Run insertion inside the existing immediate transaction. Stale expected HEAD fails closed with conflict, publishes no Run, and does not mutate the saved HEAD.

- baseline: `f08c25961bb89fd91ccee06efb59046123a9a382`
- fixed: `412d75de1adf1d2ecbb15832285775f9458c0532`
- fixed tree: `31979b71c08c765abac811ecc241cefaa6ca2f37`
- exact fixed paths: 4, all within the bounded P2 lease
- focused behavior runner: PASS
- mutation: expected-HEAD comparison bypass -> `E_PROJECT_RUN_STALE_HEAD_ACCEPTED` RED -> SHA-exact restore -> GREEN
- new test artifact/framework/meta-test: 0/0/0
- tracked WASM/UI/SSOT/SPEC diff: 0
- independent review dispatch: 0; management-owned rolling-review queue only

## Preserved custody

The four pre-existing task-owned untracked session/census files were not edited, staged, or committed. Shared dirty root and `docs/ssot/**` were not mutated. The P5 handoff at baseline remains predecessor custody.

## Nonclaims

Status is only `P2_LOCAL_PROJECT_RUN_HEAD_CUSTODY_IMPLEMENTED_UNDER_REVIEW`. Whole P2, Workbench behavior closure, full snapshot/receipt identity, exact schema/wire/storage semantics, P3~P6, V1 membership/readiness, release, activation, legal status, and Human PASS remain OPEN.
