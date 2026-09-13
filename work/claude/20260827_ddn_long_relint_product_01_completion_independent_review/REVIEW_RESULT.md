# DDN-R-RELINT-COMPLETION-01 — fixed-HEAD 통합 독립검토 결과

- EXECUTOR: 독립검증ClaudeCode / RETURN_TO: Codex관리Work
- 검토일: 2026-08-27
- FIXED_PRODUCT_TEST_HEAD: `b8530bd6eadcf79658a821f4e9b4538991b89b80`
- REVIEW_PARENT: `daabc1188d164888d7c3280588c0dbb5328bb5b6`
- 검토 worktree: `build/worktrees/review-ddn-relint-completion-01-20260827` (`review/ddn-relint-completion-01-20260827` 브랜치, main tree 비접촉)

이 검토는 하나의 종합 verdict로 뭉뚱그리지 않는다. 4개 verdict를 분리해서 반환한다.
문서의 주장을 상속하지 않고 코드·팩·스크립트·산출물로 직접 재확인했으며, 재현 불가능한
항목(실제 Edge 실행, public projection 재실행)은 정직하게 `OPEN`/미검증으로 남긴다.

## 계보 확인

```
git merge-base --is-ancestor b8530bd6... daabc118...  → YES (ancestor)
git diff --stat b8530bd6...daabc118...  → 23 files, 777 insertions(+), 0 삭제/수정 — 전부 work/codex/** 문서 신규 추가
git log --merges b8530bd6...daabc118... → 공백 (merge 0)
```
→ `EXPECTED_PRODUCT_DIFF_FIXED_TO_REVIEW_PARENT: 0`, `EXPECTED_TEST_DIFF...: 0`, `EXPECTED_MERGE_COMMIT_COUNT: 0` 모두 직접 확인 일치.

---

## A. 권위와 계보

- `docs/ssot/ssot/CURRENT.md`, `docs/ssot/CURRENT.md`, `SSOT_INDEX_v25.15.0.md`, `SSOT_ALL_MANIFEST_v25.15.0.md`, `CURRENT_SHA256_v25.15.0.md`, `publish/spec/CURRENT.md`의 SHA-256을 직접 재계산 — **FINAL_AUTHORITY_AND_LINEAGE.md/FU01A_LATEST_LIVE_AUTHORITY_BINDING.md에 기재된 값과 일치**.
- `python tools/check_ssot_v25_15_0_live_promotion.py --check` 등은 실행하지 않고(공식 도구 재신뢰 회피) pointer 파일 raw byte만 독립 재해시했다.
- `docs/ssot/**`와 public SPEC은 이 검토 세션에서 읽기만 했다(쓰기 0).

**결과**: 권위/계보 주장은 재해시로 확인됨. PASS.

---

## B. PC01 FU01 — **PASS**

### 직접 재현

```
cargo test -p ddonirang-lang                          → unit 363/363, v25_definition_binding_pack 4/4 PASS
  (신규 v25_typed_local_legacy_equals_targeted_matrix 포함)
node tests/ddn_v25_pc01_definition_binding_mutation_runner.mjs
  → baseline GREEN, M1/M2/M3 RED, restored GREEN, residue=0
node tests/ddn_v25_pc01_typed_local_equals_followup_mutation_runner.mjs
  → baseline GREEN, M1~M5 RED, restored GREEN, residue=0
cargo test --manifest-path tool/Cargo.toml v25_
  → v25_definition_then_rebinding_executes_as_distinct_local_operations: ok
  → v25_typed_legacy_equals_fails_before_runtime_state_exists: ok
```

### 이전 검토(review commit `8e395f56...`)에서 지적한 결함의 해소를 직접 확인

이전 독립검토가 지적한 "typed-local `값:수 = 1.`이 fail-closed는 하지만 범용 `:=` 오류만 낸다"는
결함을, `f80c69b8..b8530bd6` diff(`lang/src/parser.rs` 12줄, `lang/tests/v25_definition_binding_pack.rs`
58줄, `tool/src/ddn_runtime.rs` 10줄)에서 확인했다. `parse_definition_stmt`가 `parse_type_ref()`로
타입 주석을 완전히 해석한 뒤 `Equals` 토큰이면 `E_V25_DEFINITION_MIGRATION_REQUIRED`를 반환하도록
고쳤다(고정 token-lookahead가 아니므로 named/applied/function type에 동일 규칙 적용).

**이 세션이 만든 독자 probe로 재확인**(임시 `lang/tests/zz_completion_review_probe.rs`, 실행 후 삭제):

```
소스: 값:수 = 1.
결과: E_V25_DEFINITION_MIGRATION_REQUIRED: V25 정의에는 `:=`가 필요하며 ...
error.code() == "E_V25_DEFINITION_MIGRATION_REQUIRED"
```

수정 전(이전 검토 시점)에는 이 소스가 범용 `":="` expected 오류만 냈던 것과 대비된다 — **정확히
지적한 gap이 정확히 고쳐졌다**.

### targeted matrix 10건 직접 소스 대조 (`lang/tests/v25_definition_binding_pack.rs:114-153`)

typed-local / untyped-local / top-level 옛 `=` 전부 exact 진단, `:=`/`<-` 구분 유지, 같은 이름
`:=` 재정의 시 `(2, 0)`(Mutate로 collapse 안 됨), `채비` `DeclKind::Butbak`은 별개로 보존, 적용
type(`(글,수)짝맞춤`)·함수 type(`-->`) 뒤 `=`도 exact 진단, malformed type(`(수,글)`)은
migration 오류로 오분류되지 않음(`assert_ne!`) — 전부 테스트 실행으로 통과 확인.

**FINDING (경미, boundary 정확성 문제 — §D 참고)**: `FU01A_LATEST_LIVE_AUTHORITY_BINDING.md`와
`PC01_TYPED_LOCAL_LEGACY_EQUALS_FOLLOW_UP_RESULT.md`가 인용한 `PC01_INITIAL_REPORT_BYTES: 12,582` /
`PC01_INITIAL_REPORT_SHA256: fe24cf6b...` 는 실제 커밋(`8e395f56...`)의 파일 내용과 **다르다**.
`git show 8e395f56...:work/claude/20260826_ddn_pc01_fresh_fixed_head_independent_review/REVIEW_RESULT.md`를
직접 재계산하면 `12427` bytes / `e48cb2edb84ff355e932931eb721afb87f27f3c9479ff9203cb3e929107286af`다
(이 검토 세션 스스로 그 review commit을 작성했으므로 원본 값을 알고 있다). PC01 기술 판정 자체에는
영향이 없지만 completion evidence chain의 인용 정확성 문제로 기록한다.

**PC01_FU01_TECHNICAL_VERDICT: PASS**. (release membership·rights는 별도 OPEN — 이 판정이 열지 않는다.)

---

## C. G14 제한 parity — **PASS**

### 직접 재현 (전용 pack, 일반 13-case parity suite와는 별개 스크립트임을 확인)

`tests/run_seamgrim_wasm_cli_runtime_parity_check.py`(13-case 일반 suite)로 먼저 시도했으나
c09/c11/c13에 대해 top-level `ok=False`가 나왔다 — 이는 **일반 suite가 reject-case를 무조건
failure로 취급**하기 때문이며, G14가 실제로 요구하는 진단 parity 자체와는 무관함을 확인했다
(cli/wasm 메시지 안의 `code`/`phase`는 이미 정확히 일치, 단지 general suite가 이 구분을 하지 않음).
G14 전용 pack을 찾아 이것으로 재검증:

```
node tests/ddn_current_public_rejection_parity_runner.mjs
→ status=PASS, case_count=3, 세 케이스 모두 native_exit_code=1, wasm_exit_code=1,
  outer_diagnostic_code=E_EXECUTION_PREPROCESS, diagnostic_code=E_BOIM_LEGACY_REMOVED,
  phase=preprocess, state_mutation_count=0, partial_output_count=0, partial_effect_count=0,
  compatibility_fallback_count=0, native_wasm_exact_parity=true (3/3)
  wasm_artifact_bytes=5541461  ← §D의 tracked WASM byte count와 일치

node tests/ddn_current_public_rejection_parity_mutation_runner.mjs
→ baseline GREEN, M1_WRONG_DIAGNOSTIC/M2_NATIVE_OR_WASM_FAKE_SUCCESS/M3_ONE_CASE_OMITTED/
  M4_HIDDEN_COMPATIBILITY_ALLOWED/M5_STATE_OR_EFFECT_RESIDUE 전부 RED, restored GREEN, residue=0

python tests/run_ddn_cli_wasm_true_parity_successor_check.py
→ "[ddn-cli-wasm-true-parity-successor] PASS current public expected-rejection parity 3/3"
  (public-facing wrapper leaf에서도 재확인)
```

세 스크립트 각도(전용 runner 직접 실행, mutation runner, public leaf wrapper)에서 일관되게
동일 결론. historical behavior 복구나 pre-V25 fallback 추가 흔적 없음(mutation M4가 정확히
이를 겨냥하고 GREEN이 아니라 RED로 나옴을 확인).

**G14_REJECTION_PARITY_LIMITED_VERDICT: PASS**. (T5F current grid는 범위 밖 — 별도 closure 아님.)

---

## D. WASM — **일부 미해결, 정직하게 기록** (환경 문제로 단정하지 않음)

```
tracked: solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm
  bytes=5,541,461  sha256=77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34
  → 과제에 제시된 기대값과 정확히 일치.

freshness checker: python tests/run_ddn_cli_wasm_freshness_check.py → PASS
  (텍스트 정규화 해시로 source_files/cargo_lock 등 입력이 현재 트리와 일치함을 확인 — 나의
   raw `sha256sum Cargo.lock`이 이 스크립트의 `canonical_text_bytes()`와 다른 값을 냈던 것은
   CRLF/LF 정규화 차이였을 뿐 실제 drift가 아님을 스크립트 소스(sha256_text_file) 확인 후 정정)

독자 A/B 재빌드 (동일 fixed-HEAD 소스, 동일 tool crate, `wasm-pack build . --target web --release
  --out-dir <X> --out-name ddonirang_tool -- --features wasm`):
  toolchain 확인: cargo 1.92.0 (344c4567c 2025-10-21) / rustc 1.92.0 (ded5c06cf 2025-12-08) /
  wasm-pack 0.14.0 — manifest에 기록된 값과 완전 일치
  A: 5,541,525 bytes  sha256=740652ee345481f38e3aaba94cc78f9ef0671338c8fad8d6adc8424a77ffb5dc
  B: 5,541,525 bytes  sha256=740652ee345481f38e3aaba94cc78f9ef0671338c8fad8d6adc8424a77ffb5dc
  → A==B (내 빌드 자체는 재현 가능) 이지만 A/B != tracked (64 bytes 차이, 완전히 다른 해시)
```

**원인 조사**: toolchain 버전 불일치 아님(확인). Cargo.lock/source 입력 drift 아님(freshness
checker가 텍스트-정규화 해시로 독립 확인, 또한 그 스크립트의 정규화 로직을 직접 읽어 확인).
경로 의존성(체크아웃 경로 길이가 다르면 panic!()/file!() 등에 내장되는 경로 문자열 길이가 달라져
바이트 수가 달라지는 Rust/WASM에서 잘 알려진 재현성 이슈)이 가장 유력한 원인으로 판단하지만,
이 세션에서 tracked artifact를 만든 실제 원 빌드 경로를 알 수 없어 **확정 검증은 못했다**.
`freshness_only_no_full_cli_wasm_equivalence`라는 manifest 자체의 closure_claim이 이미 이
한계를 스스로 인정하고 있으므로 이것이 project의 과장 주장은 아니지만, "A/B/tracked raw-byte
identity" 요구사항 자체는 **이 세션에서 완전히 충족되지 않았다** — tracked 파일은 기대 해시와
일치하지만, tracked가 선언된 입력에서 독립적으로 byte-reproducible한지는 이 세션에서 확정하지
못했다.

**결론**: BYTES/SHA256 기대값 = tracked 파일 자체는 일치. 독립 재빌드 byte-identity는 불일치,
원인은 toolchain/입력 drift가 아님을 배제법으로 좁혔으나 확정하지 못함 — 환경 문제로 추정하지
않고 그대로 기록한다.

---

## E. 공개 projection·self-containment — **제한적으로 확인, 완전 재실행은 못함**

- exclusion ledger(`PUBLIC_PROJECTION_R2_EXCLUSIONS.detjson`) 직접 확인: PC01 5-file pack,
  projectile pack/example, `docs/ssot`, `work`, `official-store`, `node_modules` 전부 명시
  제외 — `PC01_FIVE_FILE_PUBLIC_COPY: 0` / `PROJECTILE_PUBLIC_COPY: 0` 주장과 일치.
- `python tests/run_ddn_public_specific_conformance_check.py --check-files-only` 직접 실행 →
  `leaf_roots` 정확히 11개, `PUBLIC_CONFORMANCE_ROLE_LEDGER.md`에 기재된 11개와 1:1 일치.
  `status: CANDIDATE_NOT_PUBLICATION_ACTIVATED`, `pc01_public_membership:
  PENDING_FRESH_TARGETED_PLAIN_PASS_AND_RIGHTS` — **이 세션의 plain PASS(§B) 이후에도 rights가
  남아있어 membership이 자동으로 열리지 않음**을 스크립트 출력 자체로 확인.
- **projection 도구 자체(SHA-256 `43d925e8...`로 봉인된 스크립트)를 이 트리에서 찾지 못했다** —
  ephemeral dry-run 도구로 보이며 커밋되어 남아있지 않다. 따라서 A/B projection tree identity를
  이 세션이 처음부터 재실행해 재현하지는 못했다. receipt(`PUBLIC_PROJECTION_R2_RECEIPT.md`)의
  A/B 동일 해시 주장은 **문서 인용만 확인했고 독립 재현은 하지 못했다** — 정직하게 미검증으로
  남긴다.
- `cargo check --locked --offline`(workspace) 직접 실행 → PASS. `PUBLIC_SOURCE_NON_BROWSER_SELF_CONTAINED`
  요약의 개별 PASS 항목 중 이 하나는 직접 재확인.
- private path grep(`include_str!` 중 `work/codex`/pack 관련) 좁은 패턴으로 2건만 직접 확인 —
  claim된 "13건"과 직접 대조할 만큼 넓게 재현하지 못했다(정확한 카운트는 실제 public-projected
  test compile로만 나오는데, 그 tree를 재생성하지 못했으므로). 모순은 발견하지 못했으나 확증도
  못했다.

**PUBLIC_NON_BROWSER_SELF_CONTAINMENT: FAIL** (claim 그대로 유지 — 이 세션이 직접 확인한
`cargo check`/exclusion ledger/11-leaf 셋은 모두 claim과 일치했고, 반증도 없었다. 다만 전체
FAIL 판정 근거의 일부(13개 include_str!, G14 public runner 누락 입력)는 이 세션이 처음부터
재생성하지 못해 "반증 없음" 수준의 확인이다.)

**PUBLIC_BROWSER_SELF_CONTAINMENT: BLOCKED** (아래 §F에서 이 세션이 동일한 종류의 차단을
직접 경험함으로써 사실상 재확인됨.)

---

## F. 실제 Microsoft Edge — **독립 재현 못함, 정직하게 OPEN**

- `msedge.exe` 존재 확인: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.
- 이 세션 환경에는 Playwright npm 패키지가 어디에도 없다(`node_modules` 부재, `npm ls -g`에
  없음, pip `playwright` 모듈도 없음). "다운로드·설치는 하지 않는다"는 지시에 따라 설치하지
  않았다. 따라서 **실제 Edge headed 세션을 직접 구동해 boot/현재 소스 rejection/local fallback을
  재현하지 못했다.**
- 대신 **정적/구조적 교차검증**을 수행했다: `tool/src/source_analysis.rs:310`의 "shared frontend
  strict" 진입점은 `DdnProgram::from_source_with_mode`(pre-V25 기본 경로)를 호출하며
  `DdnProgram::from_v25_source_with_mode`를 호출하지 않는다(§B/이전 검토에서 확인한 PC02
  미배선 사실과 일치). 즉 V25 `:=` positive source를 Workbench에 넣으면 pre-V25 문법으로
  파싱을 시도하다 실패해 generic `E_PARSE`로 귀결되는 것이 아키텍처상 합리적이다 —
  `WORKBENCH_EDGE_CURRENT_RUNTIME_SUCCESS: FAIL` 주장과 **모순되지 않는다**(그러나 라이브
  실행으로 확정하지는 못했다). `E_WASM_OBSERVATION_MANIFEST_MISSING`도
  `solutions/seamgrim_ui_mvp/ui/runtime/observation_manifest_contract.js:6`에 실존하는
  코드임을 확인했다.
- Codex의 `WORKBENCH_EDGE_PRODUCT_RESULT.md` 주장(BOOT PASS / CURRENT_RUNTIME_SUCCESS FAIL /
  FULL_C9 OPEN)을 **그대로 상속하지 않는다.** 실패를 성공으로 해석하지도, JS fallback/호환
  복구로 보완하지도 않았다(그런 시도 자체를 하지 않았다).

**WORKBENCH_CURRENT_RUNTIME_SUCCESS: OPEN** (이 세션 기준 — 라이브 재현 불가, 정적 근거는
claim과 모순되지 않음 수준).

---

## G. 보호 경계 — **PASS**

```
공식 DB: I:/home/urihanl/ddn/codex/official-store/seamgrim-local-official-v1/seamgrim_projects.sqlite3
  bytes=573440  sha256=3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0
  → 과제/문서 기재값과 정확히 일치. 쓰기 0.
127.0.0.1:8787 → LISTEN 없음(netstat 직접 확인)
PID 53196 → tasklist에 없음(직접 확인)
activation call: 0 (이 세션이 어떤 activation 엔드포인트도 호출하지 않음)
public push/release: 0
shared dirty root(I:/dev/ddonilang/codex): reset/clean/stash/writer 사용 안 함. 이 세션이 만든
  모든 산출물(_review_wasm_A/B, 임시 lang/tests/zz_*.rs, target_review_relint_completion)은
  worktree 또는 worktree 밖 별도 target dir에만 있었고, 전부 삭제/정리 완료.
review worktree git status: 세션 종료 시점 공백(clean).
Human PASS·external user success: 주장하지 않음.
```

---

## 반환 스키마

```yaml
TASK: DDN-R-RELINT-COMPLETION-01
FIXED_PRODUCT_TEST_HEAD: b8530bd6eadcf79658a821f4e9b4538991b89b80
REVIEW_PARENT: daabc1188d164888d7c3280588c0dbb5328bb5b6
REVIEW_COMMIT: (이 커밋 직후 값, 아래 참조)
REVIEW_BRANCH: review/ddn-relint-completion-01-20260827
REPORT_PATH: work/claude/20260827_ddn_long_relint_product_01_completion_independent_review/REVIEW_RESULT.md
REPORT_BYTES: (커밋 후 재계산, 아래 참조)
REPORT_SHA256: (커밋 후 재계산, 아래 참조)
MERGE_COMMIT_COUNT: 0
PRODUCT_DIFF: 0 (b8530bd6..daabc118, lang/tool/core/teul-cli 무변경, 문서만 추가)
TEST_DIFF: 0 (같은 구간, tests/**·lang/tests/**·pack/** 무변경 — 신규 추가 없음, 문서만 추가)
SSOT_DIFF: 0 (이 세션이 docs/ssot/** 미접촉; pointer 재해시로 확인)
PUBLIC_SPEC_DIFF: 0 (publish/spec/CURRENT.md 해시 일치, 이 세션 미접촉)

PC01_FU01_TECHNICAL_VERDICT: PASS
G14_REJECTION_PARITY_LIMITED_VERDICT: PASS
COMPLETION_EVIDENCE_AND_BOUNDARY_VERDICT: PASS_WITH_FOLLOW_UP
WORKBENCH_CURRENT_RUNTIME_SUCCESS: OPEN
PUBLIC_NON_BROWSER_SELF_CONTAINMENT: FAIL
PUBLIC_BROWSER_SELF_CONTAINMENT: BLOCKED
PUBLIC_RELEASE_READINESS: NOT_READY
FOLLOW_UPS:
  - "FU01A_LATEST_LIVE_AUTHORITY_BINDING.md / PC01_TYPED_LOCAL_LEGACY_EQUALS_FOLLOW_UP_RESULT.md의 PC01_INITIAL_REPORT_BYTES/SHA256 인용을 실제 커밋 값(12427 / e48cb2edb84ff355e932931eb721afb87f27f3c9479ff9203cb3e929107286af)으로 정정"
  - "WASM 독립 A/B 재빌드가 tracked artifact와 byte-identical하지 않은 원인을 확정 규명(원 빌드 체크아웃 경로 기록/재현, 또는 --remap-path-prefix 등으로 경로 독립적 재현성 확보)"
  - "public projection 도구(SHA-256 43d925e8...)를 재사용 가능한 형태로 tools/에 커밋해 향후 리뷰가 A/B를 처음부터 재실행할 수 있게 할 것"
  - "이번 completion 범위에서 실제 headed Edge 재현이 가능하도록 Playwright 또는 대체 CDP 구동 경로를 검토 세션이 설치 없이 쓸 수 있는 형태로 사전 준비(예: 프로젝트 sealed offline bundle)"
PROTECTED_RESOURCE_CUSTODY: official DB bytes/sha256 일치(쓰기 0), 8787 미수신, PID 53196 부재, activation/public push 0, shared dirty root 미접촉 — 전부 이 세션이 직접 재확인
TEMP_RESIDUE_COUNT: 0 (worktree git status 공백, 임시 파일/빌드 산출물 전부 정리)
FINAL_STATUS: LIMITED_EVIDENCE_REVIEWED
```

**PC01·G14가 plain PASS여도 다음은 승인하지 않는다**: PUBLIC_RELEASE, PUBLIC_ACTIVATION,
FINAL_LICENSE, RIGHTS_CLEARANCE, WORKBENCH_CURRENT_RUNTIME_SUCCESS, T5F_CURRENT_GRID_SUCCESSOR,
HUMAN_PASS, EXTERNAL_USER_SUCCESS — 이 문서는 이 중 어느 것도 승인하지 않는다.
