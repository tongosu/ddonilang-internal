# CT-CLAUDE-DDN-EXECUTION-CONCURRENCY-W1C1-F1-TARGETED-REREVIEW — 결과

## 0. 결론 (VERDICT)

**VERDICT: PASS**

**의미:**
```
W1C1_SENDER_ROUTE_INTERNAL_PROVIDER_CORE_SCOPE_PASS
W1C1_F1_FOLLOW_UP_CLOSED
```

**의미하지 않음:**
```
WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION_CLOSED
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE_APPROVED
W1_FULL_CLOSURE
RD207_PUBLIC_STABLE_WIRE
PUBLIC_ACTIVATION
DEPLOYMENT
EXTERNAL_OUTREACH
HUMAN_PASS
```

F1(parity runner trailing-newline) 교정을 격리된 fresh worktree/build로 직접 재현했다. LF 계약은 지시된 정확한 ternary 형태이며 broad whitespace 정규화가 전혀 없음을 정적 감사와 4건의 실행 시 실패주입으로 모두 확인했다. official 10-case runner는 fresh 빌드에서 10/10 PASS했고, native/source-WASM/tracked-WASM 3자 parity와 byte-identical WASM(5,467,851 bytes, 기대 SHA-256과 일치)을 재현했다. 회귀(lang 357, tool 491, teul-cli 1161)와 freshness/deploy 체커 모두 PASS. F2(Workbench UI 진단 전파)는 이번 목표에서 의도적으로 미구현 상태로 남아 있으며 UI/제품 diff는 정확히 0임을 확인했다. blocking finding은 없다.

---

## 1. 고정 좌표

```text
ORIGINAL_W1C1_PRODUCT_FIXED_HEAD:      da791953f51a38e9489d0b2a158eeb419645fd43
ORIGINAL_INDEPENDENT_REVIEW_COMMIT:    fe9077839130ba6fa33d80b7d09494a5f9f62faa
F1_CORRECTION_COMMIT:                  2e080cdb36d5497454430b4c7cb27f04c29b178e
TARGETED_REREVIEW_FIXED_HEAD:          07f22eb20de650ad064bfcb1f9278a4b4daf6c38
FINAL_REQUEST_COMMIT:                  53ec44bd2035eac6c2854a2f08b9f3c34568b2f6
EXPECTED_WASM_SHA256:                  7106d312993408029404db967d100fdb6838192daef9e38bc45e2aa8acd7a6e7
```

제품·검증 대상은 `07f22eb2...`로 고정했고, 리포트 브랜치는 `53ec44bd...`를 parent로 생성했다.

---

## 2. 계보와 범위 (Section 3)

`git log --format='%H %P'`로 직접 확인한 선형 계보(모두 단일 부모, merge commit 0):

```
6d84137a  <- e6135377
fe907783  <- 6d84137a   (이전 독립 검토 커밋, PASS_WITH_FOLLOW_UP)
2e080cdb  <- fe907783   (F1 교정: runner 개행 계약)
8d256882  <- 2e080cdb   (docs: F1 인계)
792b4bec  <- 8d256882   (docs: targeted 재검토 요청)
07f22eb2  <- 792b4bec   (docs: F1 UI change zero 기록) ← TARGETED_REREVIEW_FIXED_HEAD
53ec44bd  <- 07f22eb2   (docs: retarget fixed head)     ← FINAL_REQUEST_COMMIT
```

`fe907783`는 cherry-pick·squash·rebase 없이 `2e080cdb`의 직계 부모로 보존됨을 확인했다(직접 커밋 체인 조회, 재작성 흔적 없음). `git log --merges fe907783..53ec44bd`는 빈 출력(병합 0).

`fe907783..07f22eb2` 변경 파일(`git diff --stat`, 3 files):

```
tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs | 21 ++++++++++++++-----
.../IMPLEMENTATION_HANDOFF.md (신규)                                   | 140 ++++
.../TARGETED_INDEPENDENT_REREVIEW_REQUEST.md (신규)                    | 117 ++++
```

**F1 제품/test 변경은 official runner 1개 파일뿐**이며 나머지 2개는 인계·재검토 요청 문서다. `53ec44bd`(FINAL_REQUEST_COMMIT) 자체는 재검토 요청 문서의 `TARGETED_REREVIEW_FIXED_HEAD` 값을 `8d256882`→`07f22eb2`로 정정하는 1줄짜리 문서 diff뿐이다.

다음 경로에 대해 `git diff --stat fe907783 07f22eb2 -- <path>`를 개별 실행했고 전부 **빈 출력(diff 0)**을 확인했다:

```
lang/**
tool/src/**
tools/teul-cli/**
solutions/seamgrim_ui_mvp/ui/workbench/**  (Workbench UI 소스)
solutions/seamgrim_ui_mvp/ui/wasm/**       (tracked WASM 및 manifest)
docs/ssot/**
publish/spec/**
pack/ddn_execution_concurrency_w1b*        (W1-B 히스토리컬 팩)
pack/ddn_execution_concurrency_w1c1_sender_route_provider  (오라클 corpus)
work/claude/20260822_..._independent_review/REVIEW_RESULT.md  (내 원본 판정서, 재작성 없음)
```

원본 판정서 custody 확인: `git show fe907783:.../REVIEW_RESULT.md`를 직접 재추출해 바이트 수/해시를 재계산 — **26,885 bytes, SHA-256 `3dc650554eb06858cf82990164bc8ad432f3d3527fe3236af16d7bddcb9e5a06`**, IMPLEMENTATION_HANDOFF.md가 인용한 값과 정확히 일치. prior `PASS_WITH_FOLLOW_UP`과 F2 관찰은 재작성되지 않았다.

예상 밖 변경 없음 — blocking finding 0.

---

## 3. LF 계약 정적 감사 (Section 4)

`fe907783..07f22eb2`의 runner diff를 직접 읽었다. 핵심 추가:

```js
function nativeCanonPresentation(canonicalBody) {
  return canonicalBody.endsWith("\n") ? canonicalBody : `${canonicalBody}\n`;
}

assert.equal(nativeCanonPresentation("본문\n"), "본문\n", "existing canonical LF is not duplicated");
```

그리고 case 09(canon 모드) 비교부:

```js
const sourceCanonBody = sourceBuilt.wasm_canon_ddn(source);
assert.equal(native.stdout, nativeCanonPresentation(sourceCanonBody), ...);
if (tracked) {
  const trackedCanonBody = tracked.wasm_canon_ddn(source);
  assert.equal(trackedCanonBody, sourceCanonBody, ...);              // exact body 비교, LF 관용 없음
  assert.equal(native.stdout, nativeCanonPresentation(trackedCanonBody), ...);
}
```

확인 결과:

- 비교 계약이 지시된 정확한 형태와 **1:1 동일**: `expected = body.endsWith("\n") ? body : body + "\n"`.
- 전체 파일에 대해 `grep -n '\.trim\(|\.trimEnd\(|\.trimStart\('`를 실행 — 매치되는 6건은 모두 `process.env.*.trim()`(CLI/WASM 경로 인자)와 `expected.jsonl` 파싱용 `.trim()`뿐이며, canonical body/native stdout 비교 경로에는 **0건**.
- `trackedCanonBody`와 `sourceCanonBody`는 `assert.equal(trackedCanonBody, sourceCanonBody, ...)`로 **exact string 비교**(LF 관용 로직을 통과하지 않음) — 내부 문자·공백·줄 순서·Unicode 차이를 숨기지 않는다.
- native 표시용 LF는 `nativeCanonPresentation()` 호출 한 번만 통과하며, 이미 LF로 끝나는 body에는 LF를 추가하지 않는다는 self-test(`assert.equal(nativeCanonPresentation("본문\n"), "본문\n", ...)`)가 러너 로드 시 즉시 실행된다.

negative guard(broad normalization 부재)는 정적 감사로 확인되며, §4에서 실행 시 재검증한다.

---

## 4. 독립 재현 환경

`07f22eb20de650ad064bfcb1f9278a4b4daf6c38`에서 `git worktree add --detach`로 fresh worktree를 만들고, 두 개의 격리된 `CARGO_TARGET_DIR`(tool/lang 전용 `target-claude-w1c1-f1-review-20260822`, teul-cli 전용 `target-claude-w1c1-f1-teulcli-20260822`)로 처음부터 분리했다. read-only v24.44.1 SSOT bridge와 `node_modules` junction을 로컬에 구성했다(원본 미변경).

---

## 5. 독립 실행 재현 (Section 5, 7)

| 항목 | 결과 |
|---|---|
| `cargo build -p ddonirang-tool --bin ddonirang-tool` | 성공 (dev profile, 1m 27s) |
| `cargo test -p ddonirang-lang -q` | **357 passed; 0 failed** |
| `cargo test -p ddonirang-tool --lib -q` | **491 passed; 0 failed** |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml -q` (별도 격리 target) | **1161 passed; 0 failed** |
| `wasm-pack build --target web --out-dir pkg -- --features wasm` | 성공 |
| `wasm-pack build --target nodejs --out-dir pkg-nodejs -- --features wasm` | 성공 |
| fresh web-target `tool/pkg/ddonirang_tool_bg.wasm` SHA-256 | `7106d312...a6e7` (5,467,851 bytes) |
| fresh nodejs-target `tool/pkg-nodejs/ddonirang_tool_bg.wasm` SHA-256 | `7106d312...a6e7` (동일) |
| tracked `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm` SHA-256 | `7106d312...a6e7` (동일) — **3자 완전 일치, EXPECTED_WASM_SHA256과 일치** |
| official 10-case runner (`DDN_W1C1_CLI`=fresh native, `DDN_W1C1_WASM_DIR`=fresh pkg-nodejs, `DDN_W1C1_TRACKED_WASM_DIR`=tracked ui/wasm) | `{"cases":10,"success_cases":6,"failure_cases":4,...}`, exit 0 — **10/10 PASS** |
| `python tests/run_ddn_cli_wasm_freshness_check.py` | `[ddn-cli-wasm-freshness] PASS` |
| `python tests/run_seamgrim_deploy_artifacts_check.py` | `seamgrim deploy artifacts check ok` |
| `git diff --check` | 클린 (exit 0) |

case 00~08의 sender/route/diagnostic summary·candidate 진단 parity는 러너 내부에서 `assert.deepEqual(sourceWasm.summary, nativeSummary, ...)` / `assertCandidateDiagnostic(...)`로 함께 검증되며 예외 없이 통과했다(러너가 예외를 던지지 않고 정상 종료·JSON 출력했다는 사실 자체가 전건 통과의 증거). case 09는 canonical body exact identity와 native 표시 LF 구분이 정확히 성립함을 확인했다.

**부모 상태 RED 재현**: 이전 리뷰(`fe907783`)에서 이미 `native.stdout === wasm_output + "\n"`이 유일한 차이임을 실측했고, 그 근거가 된 case 09 실패 원문을 이번에도 재확인했다(§2 참고 자료 및 IMPLEMENTATION_HANDOFF.md의 RED 재현 로그와 대조 완료: `WASM canonical body: ... "}"` vs `native stdout: ... "}\n"` — 정확히 이 차이 하나).

---

## 6. 실제 결함 주입 (Section 6)

리뷰 워크트리에서 러너 파일에 4건의 임시 변이를 각각 적용→실행→원복했다. 매 원복 후 SHA-256이 기준값(`35b48fa86d3a5faf8aaaf4b15050588a3b7a66596acc146e44af4c8b91770cc6` — implementer의 IMPLEMENTATION_HANDOFF.md가 인용한 "최종 원복 runner SHA-256"과 정확히 일치)과 같음을 확인했다.

| # | 변이 | 방법 | 결과 |
|---|---|---|---|
| 1 | canonical body 내부 문자 1개 변경 | `sourceCanonBody`의 마지막 문자를 `］`로 치환한 값과 비교 | **RED** — `AssertionError`, 09 케이스에서 `}` vs `］` 불일치 정확히 보고 |
| 2 | native expected output에 trailing space 1개 추가 | `` `${nativeCanonPresentation(sourceCanonBody)} ` `` 와 비교 | **RED** — 정확히 trailing space 1개 차이로 실패 |
| 3 | native expected output에 LF 1개 추가 | `` `${nativeCanonPresentation(sourceCanonBody)}\n` `` 와 비교 | **RED** — 정확히 LF 중복 1개 차이로 실패 |
| 4 | broad `.trimEnd()`로 assertion 약화 | `native.stdout.trimEnd()` vs `(정상표시 + "\n\n   ").trimEnd()` 비교로 교체 | **GREEN** (아래 판정 참고) |

각 변이 직후 `git checkout -- tests/ddn_execution_concurrency_w1c1_sender_route_provider_runner.mjs`로 원복하고 SHA-256 일치를 재확인했다. 최종 원복 후 official 10-case runner를 다시 실행해 GREEN(10/10, exit 0)과 `git status --short` 클린을 재확인했다.

**변이 4 판정**: 변이 4는 예상대로 GREEN이었다 — `.trimEnd()`를 양쪽에 적용하면 인위적으로 주입한 trailing LF/space 결함(변이 2·3과 동일한 종류의 결함)이 상쇄되어 검출되지 않는다. 이는 **broad normalization이 실제로 위험하다는 것을 입증하는 negative-control**이며, 정확히 이 위험성 때문에 현재 배포된 runner가 `.trimEnd()`를 쓰지 않고 정확한 ternary 계약만 쓰는 것이 올바른 선택임을 뒷받침한다. **blocking 여부 판정: 비차단(non-blocking).** 근거:
1. 실제 배포된 runner 코드에는 `.trim()`/`.trimEnd()`가 canonical body 비교 경로에 전혀 없음을 §3의 정적 감사로 이미 확인했다(이번 변이는 가상의 "만약 trimEnd를 썼다면"을 실행 시 검증한 것이지, 배포된 코드의 실제 결함이 아니다).
2. 이 negative-control이 GREEN인 것은 논리적으로 당연하다 — 어떤 결함이든 그 결함과 똑같은 방향으로 문자열을 정규화하면 결함이 사라지는 것은 `.trimEnd()` 자체의 정의상 자명하다. 이것이 "blocking"이 되려면 배포된 코드 자체가 이런 정규화를 실제로 사용하고 있어야 하는데, 그렇지 않다.
3. 향후 유지보수자가 이 계약을 실수로 `.trimEnd()`로 되돌리는 것을 막는 전용 회귀 테스트(negative guard test)는 현재 runner에 없다 — 이는 F1의 원래 범위(case 09 수정)를 넘어서는 강화 제안이며, 후속 개선 사항으로 기록하되 이번 F1 교정의 정확성 판정에는 영향을 주지 않는다.

---

## 7. F2 경계 확인 (Section 8)

- **runtime product state의 diagnostic code/phase 보존**: 리뷰 워크트리에서 센더 불일치 소스(`(영희)의 7 ~> 관제탑`, 관제탑은 `철수`만 수신)를 fresh 네이티브 CLI로 직접 재실행:

  ```json
  {"code":"E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE","message":"matching route count is 0","phase":"async_route","source_span":{"start":129,"end":156}}
  STATUS=1
  ```

  F1 교정 전후로 이 구조화된 candidate 진단(code+phase+source_span)이 정확히 동일하게 보존됨을 확인했다 — F1은 이를 삭제하거나 일반화하지 않았다.
- **Workbench UI source 변경 0**: `git diff --stat fe907783 07f22eb2 -- solutions/seamgrim_ui_mvp/ui`가 빈 출력임을 재확인(§2에서도 확인).
- **`_CANDIDATE` 코드의 공개/안정 승격 없음**: `docs/status/` 등 공개 문서 어디에도 `E_ASYNC_ENDPOINT_UNHANDLED_CANDIDATE` / `E_ASYNC_SENDER_IDENTITY_UNRESOLVED_CANDIDATE`가 승격 문구로 등장하지 않음을 확인했다.
- **F2 OPEN 상태 정확히 기록됨**: `07f22eb2`가 추가한 `UI_CHANGE_0` 마커와 `WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION_OPEN` / `RUNTIME_CODE_PHASE_PRESERVED_IN_PRODUCT_STATE` / `UI_CHANGE_NOT_AUTHORIZED` 상태 문자열을 IMPLEMENTATION_HANDOFF.md와 TARGETED_INDEPENDENT_REREVIEW_REQUEST.md 양쪽에서 확인했다. F2 UI 구현은 이번 targeted rereview 범위에 없으며, 그 부재 자체를 실패 사유로 삼지 않았다.

F2 경계는 정확히 지켜졌다 — 결함 없음.

---

## 8. 보호 자원 (Section 9)

| 자원 | 검토 전 | 검토 후 | 상태 |
|---|---|---|---|
| PID `53196` | `53196`, StartTime `2026-08-08T12:27:21.8634297+09:00` | 동일 | 불변 |
| `127.0.0.1:8787` owner | PID 53196 (python), 동일 StartTime | 동일 | 불변 |
| 공식 DB (`build/seamgrim_project_data/seamgrim_projects.sqlite3`) | SHA-256 `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228`, mtime `2026-08-02 15:25:18`, 540,672 bytes | 완전 동일(SHA-256·mtime·크기 모두 불변) | 미접촉 |
| 공식 store write | — | 0건 | 이 리뷰는 official store에 어떤 요청도 보내지 않음(로컬 CLI/cargo/wasm-pack/node 실행뿐) |
| activation endpoint call | — | 0건 | 동일 |
| shared dirty root 조작 | — | 0건 | reset/stash/clean 미실행, 기존 워크트리(main repo)는 건드리지 않음 |
| 잔여 process/socket/profile/temp DB | — | 0건 | 리뷰용 worktree 2개, cargo target 2개 모두 제거 완료, `git worktree list`에서 소거 확인 |

보호 자원 전/후 완전 일치. 침해 없음.

---

## 9. 정리 완료

- 리뷰 워크트리 `claude-w1c1-f1-review-20260822` — `git worktree remove --force` 완료.
- 격리 Cargo 타깃 2개(`target-claude-w1c1-f1-review-20260822`, `target-claude-w1c1-f1-teulcli-20260822`) — 삭제 완료.
- `node_modules` junction, `docs/ssot/ssot` v24.44.1 bridge — 워크트리 제거와 함께 소거.
- 4건의 러너 변이 — 매 건 즉시 원복, 최종 SHA-256이 기준값과 일치, `git status --short` 클린.
- 리포트 커밋용 워크트리는 `53ec44bd...`를 부모로 새로 생성(별도 detached worktree).

---

## 10. 승인 범위 명시

이 판정 `PASS`는 다음만을 의미한다:

```
W1C1_SENDER_ROUTE_INTERNAL_PROVIDER_CORE_SCOPE_PASS
W1C1_F1_FOLLOW_UP_CLOSED
```

다음을 의미하지 않는다:

```
WORKBENCH_STRUCTURED_DIAGNOSTIC_PROPAGATION_CLOSED
W1C2_REACTION_PROVIDER_PUBLIC_SURFACE_APPROVED
W1_FULL_CLOSURE
RD207_PUBLIC_STABLE_WIRE
PUBLIC_ACTIVATION
DEPLOYMENT
EXTERNAL_OUTREACH
HUMAN_PASS
```

F2(Workbench 구조화 진단 전파)는 별도 Owner 승인 UI 트랙으로 OPEN 상태를 유지한다.

---

## 부록 — 이 보고서 자체의 메타데이터

이 섹션을 추가하기 직전까지의 본문 바이트 수와 SHA-256(자기 참조 불가능성으로 인해 이 메타데이터 문단 자체는 해시 계산 대상에서 제외):

```
바이트 수: 16042
SHA-256:   94206d1bb0272892a7de0fcbbc8c48b300ae8d36d99aea4d33daa76c2b208429
```
