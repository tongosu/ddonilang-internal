# 2026-09-01 DDN V1 CLI workshop shared atomic authority W37

- Persistent goal active; same branch, Worktree, and single writer. New goal/task/worktree/branch/reviewer 0.
- Authority: internal v25.47.0 / RD-001~543; public SPEC v0.6.0. Successor impact is additive with public transition 0.
- Baseline `4819d422c16d64851add2fd2b078c346a3e19726`, tree `855e2d3942a03a463f96395cda89750475aaf0fa`.
- Fixed `af4a922dad8d4f34aae06cffc231823c4a4dcde5`, tree `3a9bf3003d381565a9c175ca63b9cfa452677f1f`, direct parent and merge 0.
- Exact product diff: new shared tool workshop workflow, tool module export, teul consumer adapter.
- User workflow changed: `workshop gen` no longer replaces manifest when paired HTML publication cannot succeed; `workshop apply` publishes atomically.
- Baseline RED replaced the 11-byte predecessor manifest before the directory-valued second target failed. Fixed execution preserves it byte-exact, partial publish 0, residue 0.
- Baseline/fixed positive manifest and HTML hashes are identical; visible copy/layout byte diff 0.
- Deterministic repeat: manifest `e45399839adaaa3068058824864e94cbbe8c3f20d761dbdc3e193fcafec62325`, index `cffac76da61a595a9dec7f9172f899c74d56a178b7e947288dcb7e2c9ce6be98`.
- Apply/open workflow exits 0/0; input and applied patch SHA-256 both `b337d3a24e4256db8c4322f3a4874fb1abe169e31e753510f05914b78b8fa475`; missing index remains exit 1 and `E_WORKSHOP_MISSING`.
- Shared artifact-output tests 5/5 PASS. Tool library 560/562 with the same two missing-SSOT ai_prompt environment failures and new regression 0.
- Existing W54 golden is blocked before workshop by the pre-existing unsupported legacy run option. Exact workshop frontdoors were verified directly; golden mutation 0.
- New pack/runner/checker/meta-test 0. Existing product/helper tests reused; no test-of-test.
- Native workshop workflow GREEN. WASM has no applicable ingress transition. Workbench-consumable HTML/manifest bytes are unchanged; browser/Human PASS is not claimed.
- Private teul workshop authority 0 for this workflow; other INTERNAL/DEFERRED custody remains nonzero.
- Four protected untracked session files remain byte-identical and unstaged.
- SSOT/SPEC/tracked-WASM/visible-UI/membership/release/Human transition 0.
- Review bundle target: existing rolling reviewer, management dispatch only; active/new review task created here 0/0.
