# [DDN V1 rolling reviewer -> 마감지기 Chat] DDN-PATHIR-PROOF-XP06-B01-W1 — targeted rereview 결과

## 판정

`PASS`

blocking finding은 0건이다. correction fixed target에서
`seal_definedness_receipt`는 receipt identity를 계산하기 전에 checker 완료,
result publish 정확히 1회, state publish 0회, outbox release 0회와 pure-proof
pre/post state identity를 직접 fail closed한다. 각 단일축과 이전 reviewer의 복합
반례를 모두 거부했고, 두 guard mutation은 실제 RED를 낸 뒤 fixed source bytes로
정확히 복원되어 proof 18/18 GREEN과 residue 0을 확인했다.

이 PASS는 `c44279d4...`의 B-01 internal receipt correction만 닫는다. public
XP-02/schema/wire/raw DDN positive ingress, public M12, whole P1, ERQ, V1
membership/readiness, release, activation과 Human PASS는 닫지 않는다.

## 검토 계약

- `CLAIM`: pure-proof receipt가 partial publish·state mutation을 identity 생성 전에
  fail closed하는가
- `TARGET_IDENTITY`: product
  `c44279d4c4a3cd8b6289de76b125c29e46257a50` / tree
  `220087d516f6f1bd25db0dc1a299579ed5346c1c`
- canonical primary Gate: valid checker/report chain이어도 publish evidence가
  `1/0/0` 또는 unchanged state가 아니면 receipt가 존재하지 않아야 함
- `CLOSURE_EVIDENCE`: direct Git identity, permanent negative tests, reviewer source
  mutations, full Rust regressions, existing pack, freshness, actual tracked WASM와
  official deterministic rebuild
- `STOP_CONDITION`: invalid single/compound evidence가 receipt를 발급하거나 exact
  restore 뒤 fixed hash가 달라짐
- `DEEP_RESEARCH_CHECK`: `NOT_USE` — fixed local product evidence로 충분함

## Reviewer와 lineage custody

- reused reviewer worktree:
  `I:\home\urihanl\ddn\codex\build\worktrees\review-ddn-v1-vc09-named-callable-evidence-rebase-i1-20260829`
- 시작 HEAD: previous FAIL review
  `5eff9bda328fb9b3a1c6318970808a25e65258b6`
- 시작 상태: detached / clean / staged 0 / untracked 0 / merge 0
- fixed parent: exact previous FAIL review `5eff9bda...`
- fixed commit/tree: `c44279d4c4a3cd8b6289de76b125c29e46257a50` /
  `220087d516f6f1bd25db0dc1a299579ed5346c1c`
- docs-only handoff/review parent:
  `b77c9754ab0a9dd7762b85004b216ee28029bb7f` / tree
  `3b90f63acc4b1e60f8bd5ae6ecc5dd0d21201599`
- fixed와 handoff는 각각 parent 1 / merge 0 / direct lineage
- new reviewer/task/worktree/branch: 0
- historical reviewer branch force-move/rebase: 0
- producer/shared root write, stage, reset, clean, stash: 0

Fixed product diff는 정확히 두 경로다.

1. `proof/src/lib.rs`
2. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`

`docs/ssot/**`, public SPEC, core/lang/numeric/symbolic/tool/tools, pack/tests,
tracked WASM bytes, Workbench JS/HTML/CSS, visible/unrelated UI diff는 0이다.
Manifest 변경은 proof source 51,688 bytes / SHA-256
`0b3e77a6590dad66987ce86cfc172f1627713118d4f6e3d58f4d911c19530351`와
source-tree identity만 갱신한다.

## Live authority refresh

handoff가 생성될 때 기록된 v25.44.0은 historical custody다. 검토 시점 live
authority를 shared Work root에서 read-only 재검증했다.

| authority | bytes | SHA-256 | 결과 |
|---|---:|---|---|
| `SSOT_INDEX_v25.45.0.md` | 144,214 | `3f998ad22bd1442b07978482877333ae238770ff6d069106d23fde027667cd7d` | MATCH |
| `SSOT_ALL_v25.45.0.md` | 4,733,265 | `e94623f128cf9894d76e0b0d8db8de07d4c86ed0aada6cfafab5a2d6f74fad3e` | MATCH |
| `SSOT_ALL_MANIFEST_v25.45.0.md` | 5,260 | `4a5656c86dd80c33383075a5dd6a7319bb83d396a205c0baff75e858ee88bb5d` | MATCH |
| `CURRENT_SHA256_v25.45.0.md` | 15,965 | `d8437401411f860e3f9bac5122d6ca76ce659e29185e4f2ebae6894402d8f9b7` | MATCH |
| `publish/spec/CURRENT.md` | 2,758 | `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0` | MATCH |

Official live checker도 `files=40`, `seal_rows=94`, mutations 10/10,
isolated regeneration 40/40, RD-001~536 drift 0, public v0.6.0으로 PASS했다.
v25.45.0은 promotion-added semantic RD 0이며 RD-417·421·423의 checker trust,
identity/obligation firewall과 exact public schema/wire OPEN을 그대로 보존한다.

## B-01 direct fail-closed 검증

`proof/src/lib.rs:1277-1290`은 다음 순서로 직접 거부한다.

1. `check_completed_before_publish == true`;
2. `result_publish_count == 1`;
3. `state_publish_count == 0`;
4. `outbox_release_count == 0`;
5. current pure-proof profile에서 `pre_state_hash == post_state_hash`.

receipt identity 계산은 그 뒤인 `proof/src/lib.rs:1303`부터 시작한다. 그 이전에
provider/checker/profile, CheckExecutionIdentity, CheckResultIdentity,
ReportIdentity와 certificate-derived result hash도 재검산한다.

Permanent focused tests 6/6이 다음을 확인했다.

| 축 | 입력 | 관찰 |
|---|---|---|
| incomplete checker | completed=false | `E_PATHIR_PUBLISH_BEFORE_CHECK_INTERNAL` |
| result count | 0, 2 | `E_PATHIR_RESULT_PUBLISH_COUNT_INTERNAL` |
| state count | 1 | `E_PATHIR_STATE_PUBLISH_INTERNAL` |
| outbox count | 1 | `E_PATHIR_OUTBOX_RELEASE_INTERNAL` |
| pure state change | pre != post | `E_PATHIR_PURE_PROOF_STATE_MUTATION_INTERNAL` |
| reviewer compound | result/state/outbox `1/1/1`, pre != post | `E_PATHIR_STATE_PUBLISH_INTERNAL` |

이전 FAIL에서 성공 발급되던 compound counterexample는 이제 receipt identity를
만들지 못한다.

## Reviewer mutation — RED → exact restore → GREEN

| mutation | RED | exact restore | GREEN |
|---|---|---|---|
| result-count guard 제거 | invalid result count 0 receipt가 발급되어 focused test exit 101 | source SHA `0b3e77a...0351` | focused test PASS |
| state/outbox/state-hash guards 동시 제거 | 이전 compound invalid receipt가 발급되어 focused test exit 101 | source SHA `0b3e77a...0351` | proof 18/18 PASS |

두 mutation은 stage/commit하지 않았다. 각 복원 뒤 `git status` tracked diff 0,
최종 fixed source 51,688 bytes / SHA-256
`0b3e77a6590dad66987ce86cfc172f1627713118d4f6e3d58f4d911c19530351`,
Git blob `1377ed051336fcad4fd168fa3a23f16ad9e7ef7d`로 exact match했다.

## XP-05·XP-06 identity와 M11/M12

- wrong provider/checker는 `E_PATHIR_RECEIPT_CHECK_BINDING_INTERNAL`로 거부된다.
- forged CheckExecutionIdentity는
  `E_PATHIR_CHECK_EXECUTION_IDENTITY_INTERNAL`, forged CheckResultIdentity는
  `E_PATHIR_CHECK_RESULT_IDENTITY_INTERNAL`로 거부된다.
- cross-closure certificate와 recomputed wrong-result certificate도 checker에서
  거부된다.
- `ProofProblemIdentity → CertificateIdentity → CheckExecutionIdentity →
  CheckResultIdentity → ReportIdentity → ReceiptIdentity` deterministic chain과
  각 predecessor binding이 GREEN이다.
- M11 unknown internal request version은 fallback 없이
  `E_PATHIR_REQUEST_SCHEMA_VERSION_INTERNAL`이다.
- M12 internal typed closure field-loss는 `nonzero(x)` obligation을 남기고
  checker/report/receipt success에 도달하지 않는다.
- public physical field가 없으므로 public M12/frontdoor mutation은 `NOT RUN`이고
  PASS로 주장하지 않는다.

## Regression, WASM와 residue

| 검증 | 결과 |
|---|---|
| `ddonirang-symbolic --lib` | 17/17 PASS |
| `ddonirang-proof --lib` | 18/18 PASS |
| `ddonirang-tool --lib` | 532/532 PASS |
| existing Symbolic v2 pack checker | PASS |
| fixed tracked-WASM freshness | PASS |
| actual tracked WASM raw cancellation | fail closed / `E_RUNTIME_EXECUTION` containing `E_SYMBOLIC_DEFINEDNESS_OBLIGATION_REQUIRED_INTERNAL nonzero(x - 1)` |
| official manifest-declared release build repeat 1 | 5,571,041 bytes / `ac750ce56f9ee34200136147ba7dd6b3d9187c5e023b0817c4ab030dade35de2` |
| official manifest-declared release build repeat 2 | exact same bytes/SHA |
| generated 2/2 vs tracked WASM | byte-identical |
| tracked WASM refresh/write | 0 |

검토 중 한 번 호출한 별도 `candidate` remap mode는 official tracked build mode가
아니며 candidate-only artifact를 만들었다. 이를 release 동일성 근거에서 제외하고,
manifest가 선언한 default official entrypoint를 두 번 독립 실행해 위 2/2 exact
결과를 얻었다. 어느 빌드도 `CopyToUi`를 사용하지 않았고 tracked write는 0이다.

review-only cargo/build 디렉터리 5개는 검증 뒤 exact path를 확인하고 recoverable
Recycle Bin cleanup했다. original path residue는 0이다. shared external target cache와
protected Node/process/port는 종료·삭제하지 않았다.

## Nonclaims

- public XP-02 ingress/schema/wire/registry PASS: 아님
- public M12 frontdoor parity: 아님 / NOT RUN
- raw DDN assumption surface, CLI option, WASM transport, Workbench mapping: OPEN
- public stable field spelling, diagnostic, hash prefix: OPEN
- whole XP-06 public contract 또는 P1/ERQ closure: 아님
- V1 membership/support/readiness, release, activation, Human PASS: 승인 0

따라서 targeted verdict는 `PASS`, blocking finding 0이며, 이 verdict의 권위는
exact fixed commit/tree와 B-01 internal receipt slice에만 결속된다.
