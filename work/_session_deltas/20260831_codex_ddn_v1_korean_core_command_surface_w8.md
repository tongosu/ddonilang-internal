# [DDN V1제품마감Codex -> DDN V1 관리 Chat] Korean core CLI surface W8

- Persistent goal: `DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1` retained; external
  blocked state was not replaced or completed.
- Authority: internal SSOT v25.42.0 / RD-001~534, public Language SPEC v0.6.0,
  all read-only. Successor impact is additive only for RD-529/RD-530 CLI
  spelling; prior fixed PASS is not promoted.
- Baseline: `e80682d08545680f331a504ad579c9f4a41418cb`, tree
  `db9fbbe6626bf1d637a458b7b97ad2a27c3ecad6`.
- Product fixed: `dc0a48a9767c3c96b2c8a9e6e0c79ff944a5ce12`, tree
  `05be0cbe751298d613785f4fa23918754edeac47`, direct parent, merge 0.
- Product paths: official CLI bin plus tracked path-clean WASM binary and its
  freshness manifest, exactly three paths.
- User workflow: `실행`, `검사`, `짓기`, `개발 정본`, `도움`/`--도움`,
  `판본`/`--판본` reach the same pre-existing command identities as their
  technical spellings. Unsupported RD-530 command families remain open.
- Base RED: `실행` exit 2 / `E_CLI_COMMAND_UNKNOWN 실행`; fixed GREEN:
  technical/Korean pairs 6/6 exact exit/stdout/stderr parity.
- Reused tests: bin 9/9, supported native 7/7, native/WASM 2/2, tracked WASM
  10/10 with repeats 4 and partial summary 0, freshness PASS.
- Mutation: `KOREAN_RUN_ALIAS_REMOVED` exit 101 RED -> exact source restore
  SHA-256 `7f5e53da19abbf64428fb5ced71968978e0add1236108455107fe75b83f6b5fa`
  -> focused/full GREEN; residue 0.
- Candidate WASM: 5,568,289 bytes / SHA-256
  `0826e5d91e07f79900a60fdca5255127eff7c04a6117c5dd174eb258a33e077c`;
  generated JS/d.ts/package remained byte-identical.
- New pack/runner/framework/meta-test/reviewer/worktree/branch: 0. New inline
  product test: 1.
- Four predecessor task-owned untracked custody files retained byte-for-byte
  and unstaged. Shared dirty root and `docs/ssot/**` were untouched.
- C0~C8: historical 91 custody preserved; prior 12/15 official workflow count
  unchanged; bounded required teul dependency remains 0; `view/test/repl`,
  public membership/naming, final teul physical retirement and browser/review
  gates remain open.
- PathIR/Proof: P0 containment preserved; P1 remains partial internal with
  physical registry and raw-DDN assumption ingress decisions open.
- Nonclaims: no whole P0~P6/P1/V1 PASS, membership/readiness, P5/release,
  activation, legal or Human transition.
