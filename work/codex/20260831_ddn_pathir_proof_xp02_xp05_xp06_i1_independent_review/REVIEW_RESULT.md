# [DDN V1 rolling reviewer -> 마감지기 Chat] DDN-PATHIR-PROOF-XP02-XP05-XP06-I1 — fixed-target 독립검토 결과

## 판정

`FAIL`

blocking finding은 1건이다. 정상 internal execution은 result/state/outbox publish
count를 `1/0/0`으로 만들지만, public Rust helper
`seal_definedness_receipt`는 `check_completed_before_publish=true`만 검사한다.
따라서 state publish 1, outbox release 1, 변경된 post-state를 넣어도 성공
`DefinednessReceipt`를 발급한다. 이 상태에서는 XP-06 receipt chain과
`partial publish 0`을 fail-closed contract로 승인할 수 없다.

XP-05 checker recomputation, XP-02 internal typed request, M11/M12, freshness,
tracked WASM 재현성과 기존 회귀는 모두 통과했다. 이 PASS surface들은 blocking
receipt defect를 상쇄하지 않으며 public contract나 P1 closure로 승격하지 않는다.

## 검토 계약

- `CLAIM`: XP-02 internal typed request, XP-05 provider-independent checker,
  XP-06 identity/report/receipt chain의 fixed-target 독립 판정
- `TARGET_IDENTITY`: product `477f888ef95747d14e2965851690658cd5edf181` /
  tree `66b77b85f14703d5840f82f0a0656caf7d495b3b`
- canonical primary Gate: checker PASS 뒤 exact pure-result publish와
  state/outbox partial publish 0을 receipt가 fail closed하는가
- `CLOSURE_EVIDENCE`: direct Git identity, Rust unit regressions, actual source
  mutation, freshness mutation, actual tracked WASM, official build two repeats
- `STOP_CONDITION`: invalid partial-publish evidence로 성공 receipt 발급 재현
- `DEEP_RESEARCH_CHECK`: `NOT_USE`

## Reviewer custody

- reused worktree:
  `I:\home\urihanl\ddn\codex\build\worktrees\review-ddn-v1-vc09-named-callable-evidence-rebase-i1-20260829`
- 시작 historical reviewer branch:
  `review/ddn-v1-vc09-named-callable-evidence-rebase-i1-20260829`
- 시작 HEAD: `5b0f786ee4465bac0efcbceb3cf7ac9bbf07313a`
- 시작 상태: clean / staged 0 / untracked 0 / merge 0
- historical branch는 handoff와 merge-base `6220e4c9...`에서 분기되어 있어
  force-move/rebase하지 않았다.
- 같은 clean review worktree를 handoff
  `e4df04887b3ddf4d0706fc9cda201b64b0768162`에 detached 고정했다.
- 새 reviewer/task/worktree/branch: 0
- producer worktree write/stage/reset/clean/stash: 0

## Live authority

shared Work root에서 read-only로 다음 raw SHA-256을 재계산했다.

| authority | bytes | SHA-256 | 결과 |
|---|---:|---|---|
| `SSOT_INDEX_v25.44.0.md` | 141,362 | `ec4550a420fad0e7ab23269a1f05b1ce26ea3168bfd2b4bc9cc9ae0b6b9598d7` | MATCH |
| `SSOT_ALL_v25.44.0.md` | 4,637,151 | `6eae7af1c337280faae449b026acaa7230e56917c4e0e6d18214cdace2a0344f` | MATCH |
| `SSOT_ALL_MANIFEST_v25.44.0.md` | 5,276 | `9defeac715df7fd8d02b5f5cc9550a11199e688f46be100e3dc82b9f614e1d5d` | MATCH |
| `CURRENT_SHA256_v25.44.0.md` | 15,762 | `90831242d5a20c64caf0f895403983eaf97b4c9b4a905812b2e8e55a8f9ecc47` | MATCH |
| `publish/spec/CURRENT.md` | 2,758 | `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0` | MATCH |

internal live current는 `v25.44.0 / RD-001~536`, public Language SPEC은 별도
current `v0.6.0`이다. RD-417·421·423의 logical contract와 exact physical
schema/wire `PRODUCT-OPEN` 경계를 분리했다.

## Fixed identity와 changed-path boundary

- base: `8c86fba3237f94bc3fcd18c309673d337e7dec41`
- product: `477f888ef95747d14e2965851690658cd5edf181`
- product tree: `66b77b85f14703d5840f82f0a0656caf7d495b3b`
- product direct parent: exact base
- product parent count 1 / merge 0
- document handoff: `e4df04887b3ddf4d0706fc9cda201b64b0768162`
- handoff direct parent: exact product
- handoff parent count 1 / merge 0
- `git diff --check`: PASS

product diff는 다음 4경로뿐이다.

1. `proof/src/lib.rs`
2. `tests/run_ddn_cli_wasm_freshness_check.py`
3. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
4. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

`docs/ssot/**`, public SPEC, core/lang/numeric/symbolic/tool/teul-cli, pack,
Workbench JS/HTML/CSS, unrelated UI와 public export diff는 0이다.

## Blocking finding B-01 — partial publish evidence가 receipt로 성공 봉인됨

### Exact location

- `proof/src/lib.rs:1092-1094`: `check_completed_before_publish` false만 거부
- `proof/src/lib.rs:1124-1126`: result/state/outbox count는 identity material에
  넣지만 허용값 검증은 없음
- `proof/src/lib.rs:1132`: 위 invalid evidence에도 `Ok(DefinednessReceipt)` 반환

### Reproduction

fixed source에 reviewer-only temporary unit assertion을 넣어 다음 순서로 실행했다.

1. 정상 problem → certificate → check execution/result → report를 생성했다.
2. `check_completed_before_publish=true`, `result_publish_count=1`,
   `state_publish_count=1`, `outbox_release_count=1`을 전달했다.
3. `pre_state_hash=sha256:state`,
   `post_state_hash=sha256:changed-state`를 전달했다.
4. fail-closed error를 기대했지만 receipt
   `sha256:a934a53f46415bbbec5655e1b7d4eae55fb80fc0087399b5769dc8c543de537d`
   를 성공 발급했다.

같은 temporary assertion에서 wrong provider와 wrong checker, forged
CheckExecutionIdentity는 각각 지정된 internal error로 먼저 거부됐다. 실패는
partial-publish guard assertion에서만 발생했다. 임시 test는 제거했고
`proof/src/lib.rs`를 44,995 bytes / SHA-256
`03a2fa7678d1b1a8c3fd51bf8975ca1b683a508cd7c46ba63775410e8d5da176`
으로 exact 복원했다.

### Impact

정상 high-level `execute_definedness_checked_internal` 경로 자체는 `1/0/0`과
동일 pre/post state를 생성한다. 그러나 성공 receipt를 만드는 public Rust
helper가 반대 증거를 거부하지 않으므로, caller가 partial state/outbox publish를
성공 proof receipt로 봉인할 수 있다. identity가 invalid count를 hash한다는 사실은
fail-closed validation을 대신하지 않는다.

### Minimum correction

`seal_definedness_receipt`에서 receipt identity 생성 전에 다음을 요구한다.

1. `result_publish_count == 1`;
2. `state_publish_count == 0`;
3. `outbox_release_count == 0`;
4. 이 pure-proof profile에서 `pre_state_hash == post_state_hash`;
5. 위 반례의 permanent negative unit test와 fixed-target rereview.

향후 state/outbox publish가 허용된다면 이 internal pure-proof contract를 조용히
넓히지 말고 별도 versioned execution/report profile로 결정해야 한다.

## 통과한 XP-02·XP-05·XP-06 surface

### XP-05 checker

- provider boolean이나 provider canonical-success flag를 입력으로 받지 않는다.
- source를 다시 parse하고 obligation set, closure discharge, candidate result의
  definedness와 polynomial relation을 재계산한다.
- wrong provider/profile/checker/certificate, cross-closure certificate와 forged
  result/check execution을 fail closed한다.
- CAS/simplifier가 만든 `x + 1` forged result는
  `E_PATHIR_REWRITE_SEMANTICS_MISMATCH_INTERNAL`로 거부된다.

### XP-06 identity chain

다음 chain의 forward binding과 deterministic identity를 확인했다.

`ProofProblemIdentity → CertificateIdentity → CheckExecutionIdentity → CheckResultIdentity → ReportIdentity → ReceiptIdentity`

problem/certificate/check/report predecessor가 다르면 receipt를 만들 수 없고,
result hash도 certificate result에서 재계산한다. 다만 B-01 때문에 publish-evidence
부분까지 포함한 XP-06 전체 PASS는 승인하지 않는다.

### XP-02 internal typed request

- assumption closure와 transformation obligation set은 별도 object/identity다.
- unknown request version은 fallback 없이 거부된다.
- checked assumption이 누락되면 `nonzero(x)` pending으로 checker/report/receipt에
  도달하지 않는다.
- serialized public request, public field spelling과 frontdoor는 만들지 않았다.

## Mutation 재현

| mutation | RED | exact restore | GREEN |
|---|---|---|---|
| M11 version guard disable | unknown version이 full `DefinednessExecution` 성공, focused test exit 101 | proof source SHA `03a2fa...176` | focused test PASS + proof 12/12 |
| M12 internal closure field loss | 정상 checked request가 `nonzero(x)` error, focused test exit 101 | proof source SHA `03a2fa...176` | focused test PASS + proof 12/12 |

M11 source mutation 동안 freshness checker도 `source_tree_sha256 mismatch`와
`source_files mismatch`로 RED였다. exact restore 뒤 freshness는 GREEN이다.
public M12 frontdoor mutation은 physical public field가 없으므로 `NOT_RUN`이다.

## Regression, WASM와 residue

| 검증 | 결과 |
|---|---|
| `ddonirang-symbolic --lib` | 17/17 PASS |
| `ddonirang-proof --lib` | 12/12 PASS |
| `ddonirang-tool --lib` | 532/532 PASS |
| existing Symbolic v2 pack checker | PASS |
| fixed manifest freshness | PASS |
| actual tracked WASM raw DDN cancellation | fail closed / `E_RUNTIME_EXECUTION` with `E_SYMBOLIC_DEFINEDNESS_OBLIGATION_REQUIRED_INTERNAL nonzero(x - 1)` |
| official release WASM build repeat 1 | 5,571,041 bytes / `ac750ce56f9ee34200136147ba7dd6b3d9187c5e023b0817c4ab030dade35de2` |
| official release WASM build repeat 2 | exact same bytes/SHA |
| generated WASM vs tracked WASM | exact match |
| tracked WASM refresh | 0 |

freshness source roots는 `core/src, lang/src, numeric/src, proof/src,
symbolic/src, tool/src`, file count 102, source-tree SHA-256
`362229b4cfb5633cc270263f5ed0832c15708fdfc07a3b23fa14670f1f237c29`다.
review-only build/cargo directories는 검증 뒤 recoverable Recycle Bin cleanup했고
original paths residue는 0이다.

## Public contract OPEN과 nonclaims

- public XP-02 ingress/wire PASS: 아님
- public M12 frontdoor parity: 아님 / NOT RUN
- raw DDN assumption surface, CLI option, WASM transport, Workbench mapping: OPEN
- public stable diagnostic/schema/hash prefix: OPEN
- XP-05/06 internal 부분 통과를 P1 또는 ERQ closure로 승격: 금지
- P1 PASS, ERQ closure, V1 membership/support/readiness, release, activation,
  Human PASS: 승인 0

이 FAIL은 fixed product를 수정하지 않는다. B-01 최소 correction의 새 fixed
successor와 같은 rolling reviewer의 targeted rereview가 필요하다.
