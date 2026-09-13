# DDN-R-LONG-RELINT-R3K-R3L-R3N-TARGETED-REREVIEW-01 독립 검토 결과

- EXECUTOR: 독립검증ClaudeCode / RETURN_TO: Codex관리Work
- 검토일: 2026-08-28
- REVIEW_PARENT: `a34ee611e4c82d70e35d89c23869016c76813e78`
- PRODUCT_TEST_FIXED_HEAD: `5c4a7684e3a041a4e5775ec14fac93aa40db0f09`
- 검토 worktree: `build/worktrees/review-ddn-r3k-r3l-r3n-20260828` (CRLF checkout, "B" 역할)
- 보조 worktree: `build/worktrees/review-ddn-r3n-lf-checkout-20260828` (`git -c core.autocrlf=false`로
  강제 LF checkout, "A"/"C" 역할)
- 격리 산출물: `I:/home/urihanl/ddn/codex/build/review_r3n/**` (검토 종료 시 전부 삭제)

## VERDICT: **PASS_WITH_FOLLOW_UP**

plain PASS 아님 — §8에서 candidate substitution 후 validation receipt/tree identity가
문서 주장값과 다름(정밀 재현 실패)을 발견했으나 구조적 수치(895/895/18/0)는 정확히
일치함을 확인했다. 이 판정은 `R3K_F1_METADATA_PATH_CLOSED`, `R3K_F2_FULL_FILE_SECURITY_SCAN_CLOSED`,
`R3N_TOOLCHAIN_ROOT_REMAP_CANDIDATE_CLOSED`, `R3L_D1_D6_READ_ONLY_CUSTODY_BOUND`만 닫는다.
`TRACKED_WASM_REFRESH`, `PUBLIC_WASM_MEMBERSHIP`, `SPEC_HISTORY_MEMBERSHIP`,
`RIGHTS_LICENSE_NOTICE`, `OFFLINE_BROWSER_BUNDLE`, `PUBLICATION_READY`, `PUBLIC_RELEASE`,
`PUBLIC_ACTIVATION`, `HUMAN_PASS`는 닫지 않는다.

## 1. 계보

```
git merge-base --is-ancestor c177f5e9 5c4a7684 → YES
git merge-base --is-ancestor 5c4a7684 a34ee611 → YES
git log --oneline c177f5e9..a34ee611 → 652db180(owner binding) 613a59fb 2393c61f f55eb524
  5c4a7684(fixed head) a34ee611(review parent) — 6 commits, 단일 parent 체인
git log --merges c177f5e9..a34ee611 → 공백 (merge 0)
git diff --stat 5c4a7684 a34ee611 → 7 files, 576(+)/0(-), 전부 work/codex/** 문서 신규 — 제품 diff 0
```

## 2. F1 metadata path — 실제 fix를 소스·산출물 양쪽에서 확인

이전 검토(review commit `9cdf474d...`)가 지적한 `ddn.project.json`의
`"teul_cli_bin": "I:/home/urihanl/ddn/codex/target/debug/teul-cli.exe"`가 어떻게 처리됐는지
확인했다.

- 실제 repo-root `ddn.project.json`(로컬 개발용 파일 그 자체)은 **여전히** 이 값을 갖고
  있다 — 소스 파일 자체를 고친 게 아니다.
- `PUBLIC_PROJECTION_R3N_MANIFEST.detjson`의 rules 배열에서 해당 파일 규칙에
  `"json_remove_paths": [["toolchain", "teul_cli_bin"]]`가 추가된 것을 확인했다.
- 독자적으로 `tools/project_public_source.py`를 이 매니페스트로 재실행해 투영본
  `ddn.project.json`을 직접 열어 확인: `"toolchain":{}` — 해당 키가 구조적으로 제거되어
  있음을 직접 확인했다.

```
PROJECTED_TEUL_CLI_BIN_COUNT: 0 (직접 확인)
PRODUCT_METADATA_INTERNAL_PATH_COUNT: 0 (투영본 전체 재스캔, 아래 §3)
PRIVATE_BUILD_PATH_FALLBACK_COUNT: 0 (환경 fallback/checkout-relative 대체 흔적 없음 — 단순 키 제거)
```

**F1_METADATA_STATUS: CLOSED** — 정확히 지적한 필드가 정확히 구조적으로 제거됐다.

## 3. F2 전체 파일 security scan — 895/895, role 18개, 미스캔 0

```
python tools/project_public_source.py --repo . --manifest .../PUBLIC_PROJECTION_R3N_MANIFEST.detjson
  --output <isolated> --receipt-dir <isolated>
→ {"file_count": 895, "public_tree_identity": "sha256:135866f2...20e5d", "source_commit": "5c4a7684..."}

python tools/validate_public_projection.py --projection <isolated> --receipt-dir <isolated> --write-validation-receipt
→ (tracked WASM family 그대로 있는 상태) E_PUBLIC_INTERNAL_ABSOLUTE_PATH:
    solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
```
이 RED는 **예상된 것**이다 — tracked WASM은 default(repository-root-only) remap으로
빌드되어 여전히 cargo-registry/toolchain 115개 경로를 담고 있으며, candidate 대체 전
validator가 정확히 이를 검출해야 한다는 R3N 설계 그대로다(문서의 "candidate 이전
projection validator는 tracked WASM에서 정확히 E_PUBLIC_INTERNAL_ABSOLUTE_PATH로
RED였다"와 일치).

candidate WASM family로 substitute 후 재검증(§8) 결과:
```
PUBLIC_PROJECTION_VALIDATION_PASS files=895
PUBLIC_VALIDATION_RECEIPT.detjson:
  TOTAL_PROJECTED_FILES: 895
  SECURITY_SCANNED_FILES: 895
  SCANNED_ROLE_COUNT: 18
  UNSCANNED_SECURITY_RELEVANT_FILES: 0
```
예상값(895/895/0, role count 18)과 **정확히 일치**. `SCANNED_ROLES`(validator 소스, 이전
검토에서 5개 role만 커버하던 gap)가 이번엔 대폭 확장돼 `PRODUCT_METADATA` 포함 전체
role을 커버함을 소스로도 직접 확인했다(이전 R3K 검토가 지적한 role-scope gap의 직접적인
후속 교정).

## 4. 원본 115-row inventory

```
python -m pytest tests/test_wasm_candidate_remap.py::WasmCandidateRemapTests::test_tracked_inventory_is_exact_115 -v
→ PASSED
```
`R3N_115_PATH_EXACT_INVENTORY.detjson`을 직접 열람 — family 분류 `CARGO_REGISTRY_ROOT: 94,
RUSTUP_TOOLCHAIN_ROOT: 21, REPOSITORY_ROOT/CARGO_HOME_OTHER/TOOLCHAIN_OTHER/UNKNOWN: 0`,
합계 115 확인. WASM raw byte offset까지 전수 대조할 시간은 없었으나(범위 제한으로 기록),
94+21=115이고 UNKNOWN 0임은 직접 확인했다.

## 5. candidate-only build contract — 소스 직접 감사 + 독자 attack

`scripts/build_wasm_tool.ps1`과 `tools/wasm_candidate_remap.py`를 라인 단위로 읽었다.

- default(`-SourceRemapMode default` 또는 미지정) 경로는 기존 `--remap-path-prefix=$repoRoot=/ddn-src`
  단일 매핑만 유지 — **변경 0**을 소스로 확인.
- candidate 모드만 `E_WASM_CANDIDATE_TRACKED_COPY_FORBIDDEN`(CopyToUi 강제 차단),
  `E_WASM_BUILD_INHERITED_RUSTFLAGS_UNSUPPORTED`(상속 RUSTFLAGS 거부),
  `E_WASM_CANDIDATE_SOURCE_DIRTY`(dirty worktree 거부), fixed-HEAD LF `git clone --shared
  --no-checkout` + `core.autocrlf false` 강제 checkout, 3-root remap(`REPOSITORY_ROOT`,
  `CARGO_REGISTRY_ROOT`, `RUSTUP_TOOLCHAIN_ROOT`)을 수행함을 확인.

```
python -m pytest tests/test_wasm_candidate_remap.py tests/test_wasm_source_remap_entrypoint.py -v
→ 13 + 5 = 18 passed (missing/duplicate/overlap root, sibling-prefix, UNC/device/URI,
  policy identity stability, receipt tamper 등 포함)
```

**독자 CLI-level 공격 3건** (pytest 파일 복사가 아니라 직접 CLI 인자로 공격):
```
1) cargo-home == rust-sysroot(둘 다 존재하지 않는 동일 경로) → E_WASM_REMAP_REQUIRED_ROOT_MISSING (fail-closed)
2) repository-root를 소문자 드라이브(i:/...)로 전달 → 대문자(I:\...)로 정규화되고
   policy_identity가 대소문자 무관하게 sha256:d80fdb94...ed6646a로 동일(Windows drive case 축 확인)
3) cargo-home에 repo-root 재사용(registry 서브경로 부재) → E_WASM_REMAP_REQUIRED_ROOT_MISSING (fail-closed)
```
독자 attack 3건 모두 기대대로 동작. 전체 15축 중 pytest 13+5=18건은 기존 스위트를 직접
실행(복사 아님)해 재확인했고, 그중 최소 3축(drive case, required-root-missing 2종)은
CLI 직접 호출로 별도 재현했다 — 시간 제약으로 전체 15축을 전부 CLI로 재구현하지는
못했음을 범위 제한으로 기록한다.

## 6. A/B/C 재빌드 — 공식 `scripts/build_wasm_tool.ps1`로 세 번 독립 실행

ad-hoc `wasm-pack` 직접 호출을 쓰지 않고 **공식 build entrypoint**만 사용했다.

```
A (LF invoking checkout, `git -c core.autocrlf=false worktree add`로 만든 별도 worktree):
  DDN_BUILD_DIR=<isolated>, CARGO_NET_OFFLINE=true
  & scripts\build_wasm_tool.ps1 -Profile release -Target web -CopyToUi $false -SourceRemapMode candidate
  → EXITCODE=0, semantic_identity=sha256:fcb144cb...d65fa

B (CRLF invoking checkout, 이 검토의 기본 worktree):
  → EXITCODE=0, semantic_identity=sha256:fcb144cb...d65fa (A와 동일)

C (LF invoking checkout에서 반복, 별도 DDN_BUILD_DIR):
  → EXITCODE=0, semantic_identity=sha256:fcb144cb...d65fa (A/B와 동일)
```

4개 산출물 raw byte 직접 대조(A/B/C 전부):
```
ddonirang_tool_bg.wasm  : 48be0af0f5cdb3cae78414b42d7cb519961994b9df387cdcc2dbc985487e043f (5,538,645 bytes)
ddonirang_tool.js       : 16b4de4cac8bfebbc7d7f881ab1241b0d22d652ff8ad00b9045f40c81d7c90a9
ddonirang_tool.d.ts     : 3f7f02aaffc0fb50146f47c4350bcaadb607d26ab2dd88e9b03bb82d9a3f1fec
package.json            : 223687f3faa5ab0f3552070ca639ba343186ded73627b712cc2a5e27ef439fa3
```
A=B=C, 그리고 이 4개 값 **모두 문서에 기재된 예상값과 정확히 일치**한다
(`CANDIDATE_A/B/C` 예상 WASM hash `48be0af0...` 포함). R3N_WASM_REMAP_RECEIPT.detjson도
직접 열람해 확인:
```
build_entrypoint_git_blob_sha256: 33b2db4e0707c034ce8ac239dc85e90b05829e73293ac9fa3405ca8cd645636a  (예상값과 일치)
policy.policy_identity:           sha256:d80fdb94b79cbab3ac4fd580c701a0dc5947676706964cf0252111237ed6646a  (예상값과 일치)
path_scan: internal_absolute_path_count=0, official_store_path_count=0, private_include_count=0,
           unknown_path_count=0
status: CANDIDATE_ONLY_NOT_TRACKED_NOT_PUBLIC_MEMBERSHIP, public_membership: false,
        tracked_manifest_write: 0, tracked_wasm_write: 0
```

**A_B_C_RAW_EQUAL: YES. CANDIDATE_INTERNAL_PATH_COUNT/PRIVATE_PATH_COUNT/OFFICIAL_STORE_PATH_COUNT/
UNKNOWN_PATH_COUNT: 전부 0.** 이 결과는 이 review 시리즈가 지난 세 차례(RELINT-COMPLETION,
V1-FD01A, R3K)에서 반복 관찰했던 "독자 ad-hoc wasm-pack 재빌드가 tracked/claimed 값과
어긋난다"는 패턴과 대비된다 — **공식 candidate entrypoint를 정확히 사용하니 완전히
재현됐다.** 이전 mismatch들의 근본 원인이 정확히 이 R3N remap이 해결하려던 문제였음을
사실상 실증한다(정식 결론은 아니며, 단지 이 review가 관찰한 상관관계로만 기록한다).

## 7. mutation과 fail-closed — §5에 통합 기록 (위 참조)

## 8. isolated projection — 구조 일치, 정밀 해시 불일치 발견

```
python tools/wasm_candidate_remap.py substitute-projection --projection <proj_A>
  --receipt-dir <receipt_projA> --candidate-dir <run_A3 결과>
→ {"public_membership": false, "status": "TEST_OWNED_ISOLATED_OUTPUT_ONLY",
   "tracked_source_write_count": 0, "candidate_artifact_identity": "sha256:fcb144cb...d65fa"}

python tools/validate_public_projection.py --projection <proj_A> --receipt-dir <receipt_projA> --write-validation-receipt
→ PUBLIC_PROJECTION_VALIDATION_PASS files=895
  validation_receipt_identity=sha256:9f188f7f94e580945a9dac46d0b2ae192525752f7dbbfa31a49ba1f84725467a
```
구조적 수치(TOTAL_PROJECTED_FILES=895, SECURITY_SCANNED_FILES=895, SCANNED_ROLE_COUNT=18,
UNSCANNED_SECURITY_RELEVANT_FILES=0)는 예상과 **정확히 일치**했다. 그러나
`validation_receipt_identity`가 문서에 기재된 `sha256:c63d09f7c08916e08400edf4f090d69cf732fa9d7a0d8f79ba79510224e72351`와
**다르다**(`9f188f7f...`). `public_tree_identity`도 예상 `sha256:7f2bcb7d...`와 다르다
(`4d6ac626...`). WASM/JS/d.ts/package 4개 candidate 산출물 자체는 §6에서 byte-identical을
확인했으므로, 이 tree/receipt 수준의 차이는 candidate 예술물 자체의 문제가 아니라 이
substitution·validation 단계의 어떤 경로/환경 의존 요소(가능성: `--projection`/`--receipt-dir`
절대경로가 receipt 내용에 흡수됨, 또는 이 review의 proj_A가 처음부터 문서가 사용한 것과
다른 방식으로 생성됨) 때문으로 추정되나, 시간 제약으로 근본 원인을 확정하지 못했다.
"환경 문제로 추정하지 말라"는 지시에 따라 추측을 사실로 단정하지 않고 그대로 기록한다.
**candidate substitution이 public membership 승격이나 tracked artifact 교체로 기록되지
않았음**은 receipt의 `public_membership: false` / `tracked_source_write_count: 0` /
`status: TEST_OWNED_ISOLATED_OUTPUT_ONLY`로 명확히 확인했다.

## 9. 회귀 — source/projection 양쪽 직접 재현

```
python -m pytest tests/test_project_public_source.py tests/test_validate_public_projection.py
  tests/test_wasm_candidate_remap.py tests/test_wasm_source_remap_entrypoint.py -q
→ 10+25+13+5 = 53 passed  (Python tests: 53/53 정확히 일치)
  (10+25=35 = "projection/validator: 35/35"과도 일치)

[source worktree] cargo test --manifest-path tool/Cargo.toml --lib  → 517 passed
[source worktree] cargo test --manifest-path tool/Cargo.toml        → 405 passed, 2 failed
  (ai_prompt::tests::ai_prompt_output_invariants_hold / ai_prompt_output_matches_golden — 동일 2건)

[fresh projection proj_A] cargo test --manifest-path tool/Cargo.toml → 405 passed, 2 failed (동일 2건)
  → projection-caused additional RED: 0

[fresh projection proj_A] node tests/ddn_current_public_rejection_parity_runner.mjs
  → status: PASS, cases: 3  (G14 3/3)

public SPEC v0.6.0 seal: raw git blob(`git show HEAD:<path>`) 기준 29/29 byte·hash 완전 일치
  (파일시스템 직접 읽기는 CRLF checkout 오탐 발생 — 이 review 시리즈에서 반복 확인한 패턴,
   raw blob으로 우회)
```
ai-prompt 2건 RED를 성공으로 위장하거나 고치지 않았음을 원문 그대로 확인했다.

## 10. tracked artifact·R3L custody

```
git diff --stat c177f5e9..a34ee611 -- docs/ssot publish/spec solutions/seamgrim_ui_mvp/ui/wasm
→ 공백 (tracked WASM family, Workbench UI, docs/ssot, publish/spec 전부 diff 0)
```
R3L 4개 custody 파일 raw sha256 직접 재계산:
```
WORKBENCH_BROWSER_PATH_RIGHTS_LEDGER_R3L.detjson : 704d48bd3ef50a28d1a800162312edc03ef75e54cf8f65790597121fe7b18321 (일치)
THIRD_PARTY_NOTICE_DRAFT_R3L.md                  : dbdf6b2671eba3002e86e9255a1ebaf6d0143a566810c3dfdbe342f2fcedd540 (일치)
WORKBENCH_BROWSER_READ_ONLY_CUSTODY_AUDIT_R3L.md : 0e1b666cd55bd10c99588af210dcf9b2c0d756e21a3b32d4716e02d37f8a4a08 (일치)
PUBLIC_FACADE_CANDIDATE_R3J/NOTICE_CANDIDATE.md  : bc08698db3f17bcaed0f07784610234f0998dd50250cca76b5e1efb13f42a479 (일치)
```
107-path ledger·199-row dependency inventory·5건 미확보 라이선스 자료 등은 이 4개 해시
불변 확인으로 간접 확인했다(전체 콘텐츠 재파싱은 시간 제약으로 생략). ai-prompt
first-public 제외/SPEC linked history 대기/PC01·projectile·gaji rights 제외/legal
selection·NOTICE 미승인/offline browser bundle OPEN/tracked WASM refresh 미실행/public
membership 미승인 — 모두 grep과 위 receipt 필드로 그대로 유지됨을 확인, 승인 언어
0건.

## 11. 보호 자원

```
official-store DB: bytes 확인 안 했으나 sha256=3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0 (직접 재해시, 불변)
127.0.0.1:8787 → LISTEN 없음 (직접 확인)
PID 53196 → tasklist에 없음 (직접 확인)
activation/public push/network download: 0 (이 세션이 어느 것도 수행하지 않음)
review-owned residue: I:/home/urihanl/ddn/codex/build/review_r3n/** 전부 삭제,
  두 worktree(review-ddn-r3k-r3l-r3n-20260828, review-ddn-r3n-lf-checkout-20260828)
  git status 공백 재확인
```

---

## 반환 스키마

```
VERDICT: PASS_WITH_FOLLOW_UP
REVIEW_PARENT: a34ee611e4c82d70e35d89c23869016c76813e78
REVIEW_COMMIT: (커밋 직후 값, 아래)
REVIEW_BRANCH: review/ddn-r3k-r3l-r3n-20260828
REPORT_PATH: work/claude/20260828_ddn_r3k_r3l_r3n_targeted_rereview_independent_review/REVIEW_RESULT.md
REPORT_GIT_BLOB: (커밋 후 재계산)
REPORT_BYTES: (커밋 후 재계산)
REPORT_SHA256: (커밋 후 재계산)

LINEAR_ANCESTRY: YES (c177f5e9 -> ... -> 5c4a7684 -> a34ee611, merge 0)
MERGE_COMMIT_COUNT: 0
F1_METADATA_STATUS: CLOSED (json_remove_paths 구조적 제거를 소스+투영 산출물 양쪽에서 직접 확인)
F2_TOTAL_FILES: 895
F2_SCANNED_FILES: 895
F2_ROLE_COUNT: 18
ORIGINAL_PATH_INVENTORY: CARGO_REGISTRY_ROOT 94 / RUSTUP_TOOLCHAIN_ROOT 21 / UNKNOWN 0 / TOTAL 115 (문서와 일치, WASM section별 byte offset 전수 대조는 생략)
REMAP_POLICY_STATUS: CONFIRMED — policy_identity sha256:d80fdb94...ed6646a, build_entrypoint_git_blob sha256:33b2db4e...45636a 둘 다 예상값과 정확히 일치. drive-case normalization을 독자 CLI attack으로 재확인.
CANDIDATE_A: 48be0af0f5cdb3cae78414b42d7cb519961994b9df387cdcc2dbc985487e043f (공식 build script, LF checkout worktree)
CANDIDATE_B: 48be0af0f5cdb3cae78414b42d7cb519961994b9df387cdcc2dbc985487e043f (공식 build script, CRLF checkout worktree)
CANDIDATE_C: 48be0af0f5cdb3cae78414b42d7cb519961994b9df387cdcc2dbc985487e043f (공식 build script, LF checkout 반복)
A_B_C_RAW_EQUAL: YES (WASM/JS/d.ts/package.json 4종 전부 byte-identical, 예상값과도 일치)
CANDIDATE_INTERNAL_PATH_COUNT: 0
FAULT_INJECTION: pytest 53/53 직접 실행(복사 아님) + 독자 CLI attack 3건(전부 fail-closed 또는 정규화 확인). 15축 전체를 CLI로 재구현하지는 못함(범위 제한)
PROJECTION_AB_IDENTITY: 구조 수치(895/895/18/0) 정확히 일치. tree/validation-receipt hash는 문서 기재값과 불일치 — 근본 원인 미확정, 정직하게 기록
VALIDATION_RECEIPT: 895/895/18/0 확인, exact hash 불일치(§8 참조, PASS_WITH_FOLLOW_UP의 핵심 근거)
REGRESSION_RESULTS: Python 53/53, tool lib 517/517(source), tool binary 405/2(source/projection 완전 동일), G14 3/3(source/projection), SPEC 29/29(raw blob) — 전부 직접 재현
TRACKED_ARTIFACT_DIFF: 0 (tracked WASM/manifest/JS/d.ts/package/Workbench UI/docs/ssot/publish/spec 전부 diff 0 확인)
R3L_CUSTODY_STATUS: 4개 custody 파일 raw sha256 전부 일치, 불변 확인
PROTECTED_RESOURCE_CUSTODY: official DB sha256 일치·쓰기 0, 8787 미수신, PID 53196 부재
REVIEW_OWNED_RESIDUE_COUNT: 0
OPEN_GATES: TRACKED_WASM_REFRESH, PUBLIC_WASM_MEMBERSHIP, SPEC_HISTORY_MEMBERSHIP, RIGHTS_LICENSE_NOTICE, OFFLINE_BROWSER_BUNDLE, PUBLICATION_READY, PUBLIC_RELEASE, PUBLIC_ACTIVATION, HUMAN_PASS — 전부 확인된 대로 열림 유지
FINAL_STATUS: R3K_R3L_R3N_TARGETED_REREVIEW_PASS_WITH_FOLLOW_UP
```

## Follow-up (비차단, 이 PASS_WITH_FOLLOW_UP의 근거)

1. `wasm_candidate_remap.py substitute-projection` + `validate_public_projection.py`의
   `validation_receipt_identity`/`public_tree_identity`가 이 review의 독자 재현에서
   문서 기재값과 다른 이유를 규명할 것 — candidate 4대 산출물(WASM/JS/d.ts/package) 자체는
   byte-identical임이 이미 확인됐으므로, 원인은 substitution·validation 단계의 경로/환경
   의존성일 가능성이 높다.
2. 115-row inventory의 WASM section byte offset 전수 대조를 별도 세션에서 완료할 것.
3. fault-injection 15축 전체를 CLI 직접 호출로 재구현해 pytest 재실행을 넘어서는 독립성을
   강화할 것(이번엔 3축만 CLI로 추가 검증).
