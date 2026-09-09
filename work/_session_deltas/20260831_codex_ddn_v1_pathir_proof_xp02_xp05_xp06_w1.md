# DDN PathIR/Proof XP02·XP05·XP06 W1 session delta

- Status: Pending
- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex Work
- AI_CAPABILITY: product single-writer implementation and fixed-head verification
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: V1 closure execution owner
- RETURN_LABEL: [DDN V1제품마감Codex -> DDN V1 관리 Chat]
- CONTROL_OWNER: Owner / DDN V1 관리 Chat
- MANAGER: DDN V1 관리 Chat
- EXECUTION_OWNER: thread 01a04a01-b812-7840-a2a3-33208dd36e36
- FILE_OWNER: proof/src/lib.rs; existing WASM freshness checker; tracked WASM binary/manifest
- REVIEWER: existing rolling reviewer only, not dispatched by writer
- ORIGIN_TASK_ID: DDN-PATHIR-PROOF-DEFINEDNESS-OBLIGATION-W1

## Fixed lineage

- base: `8c86fba3237f94bc3fcd18c309673d337e7dec41`
- product/test fixed: `477f888ef95747d14e2965851690658cd5edf181`
- tree: `66b77b85f14703d5840f82f0a0656caf7d495b3b`
- direct lineage: true
- merge count: 0

## Result

The internal checked-assumption product seam now binds
ProofProblem -> Certificate -> CheckExecution -> CheckResult -> Report -> Receipt.
Unknown internal request version and missing assumption fail closed. The
independent checker recomputes PathIR definedness. Successful pure proof publish
is result 1/state 0/outbox 0.

The existing WASM freshness checker had omitted proof/symbolic/numeric direct
dependencies. This release-critical fail-open was reproduced, corrected in the
existing checker, and closed by official tracked-WASM rebuild and manifest
refresh.

## Verification

- symbolic 17/17
- proof 12/12
- tool 532/532
- Symbolic v2 pack PASS
- M11 source mutation RED -> exact restore -> GREEN
- M12 internal assumption-loss mutation RED -> exact restore -> GREEN
- tracked WASM 5,571,041 bytes /
  `ac750ce56f9ee34200136147ba7dd6b3d9187c5e023b0817c4ab030dade35de2`
- repeated official WASM build byte-identical
- freshness PASS
- actual WASM raw DDN definedness fail-closed PASS
- new pack/runner/meta-test/reviewer/worktree/branch: 0

## Open gates

v25.44 RD-423 keeps exact schema/wire open. Public structured registry,
CLI option, WASM field, Workbench mapping, stable diagnostic and raw-DDN checked
assumption syntax were not invented. XP-02 public ingress and public M12 remain
Owner decisions. P1 PASS, ERQ closure, V1 readiness/release and Human PASS remain
OPEN.
