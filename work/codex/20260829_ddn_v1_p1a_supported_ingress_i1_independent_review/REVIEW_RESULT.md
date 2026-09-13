# DDN-R-V1-P1A-SUPPORTED-INGRESS-I1 독립검토 결과

## 판정

- VERDICT: `PASS_WITH_FOLLOW_UP`
- PRODUCT_TEST_FIXED_HEAD: `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`
- PRODUCT_TEST_FIXED_TREE: `a0d46873734ad50a8e5d4a8dbb5f84f73c03f23a`
- PRODUCT_TEST_PARENT: `0d9dd6091d8df0b697dee7c7cf6e8438b592d782`
- REVIEW_PARENT: `151923c9d6a0708574416895c159ab21ffa87795`
- REVIEW_COMMIT: 이 보고서와 reviewer session delta만을 포함하는 `REVIEW_PARENT`의 직계 후속 commit. 정확한 hash는 commit 후 반환 메시지에 결속한다.
- REVIEWER: `DDN V1 P1-A 독립검토 재결속`
- ROLE: `INDEPENDENT_REVIEWER`

제품 구현과 고정 제품 증거는 검토 범위에서 통과한다. `PASS_WITH_FOLLOW_UP`인 이유는 제품 결함이 아니라 committed fault-injection runner의 한 mutation 이름과 실제 변이 의미가 일치하지 않기 때문이다. 실제 hidden fallback 변이를 독립 주입해 RED를 확인했으므로 제품 재작업은 요구하지 않는다.

## 역할 선언

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex
- AI_CAPABILITY: independent fixed-head product review
- SESSION_NICKNAME: DDN V1 P1-A 독립검토 재결속
- PROJECT_ROLE: INDEPENDENT_REVIEWER
- RETURN_LABEL: `[P1-A독립검토Codex -> Codex관리Work]`
- DEEP_RESEARCH_CHECK: `NOT_USE` — fixed-head 내부 코드·정본·테스트 검증이며 외부 조사가 판정을 개선하지 않는다.

## 재결속 전제

지정된 `C:/Users/ddongosu/.codex/worktrees/375b/codex`에서 쓰기 전 다음을 확인했다.

- detached HEAD: `151923c9d6a0708574416895c159ab21ffa87795`
- clean: yes
- staged: 0
- untracked: 0
- merge: 0

전제가 정확히 일치한 뒤에만 검토를 진행했다. 새 worktree·branch·제품 writer는 만들지 않았고 기본 저장소 checkout은 수정하지 않았다.

## 읽은 권위와 경계

- internal: SSOT v25.19.0 / RD-001~461, `LIVE CURRENT / owner final approved / docs-first / product-open`
- public: Language SPEC v0.6.0, `public current / docs-first / product-open`
- v25.19.0은 Definition `:=`와 Binding/Rebinding `<-`의 의미 분리와 clean-break 경계를 유지한다.
- v25.19.0의 실제 V1 membership row와 numeric maturity는 0이고 readiness floor는 `UNCLAIMABLE`이다.
- public v0.6.0도 문서 승격이 parser/runtime/Workbench parity 또는 제품 완료를 뜻하지 않는다고 명시한다.
- `docs/ssot/**`와 `publish/spec/**`는 읽기 전용으로 대조했으며 변경 0이다.

## 계보

```text
0d9dd6091d8df0b697dee7c7cf6e8438b592d782  P1-A FILE_OWNER lease / product parent
  -> bc883fd1444bfad86c4ebbf92a84ffa6d84d027c  product/test fixed HEAD
    -> 151923c9d6a0708574416895c159ab21ffa87795  handoff / review parent
      -> REVIEW_COMMIT  report + reviewer session delta only
```

- `bc883fd...`의 direct parent는 `0d9dd609...`이다.
- `151923c...`의 direct parent는 `bc883fd...`이다.
- `0d9dd609...`부터 `151923c...`까지 merge commit은 0이다.
- review 결과 commit은 `151923c...`의 direct successor 하나로 만든다.

## exact 16-path product/test diff

`0d9dd609... -> bc883fd...` diff는 정확히 다음 16개 경로다.

1. `pack/v1_core_supported_ingress_w1/fixtures/direct_recursion.ddn`
2. `pack/v1_core_supported_ingress_w1/fixtures/legacy_definition_equals.ddn`
3. `pack/v1_core_supported_ingress_w1/fixtures/mutual_recursion.ddn`
4. `pack/v1_core_supported_ingress_w1/fixtures/positive_definition_rebinding.ddn`
5. `pack/v1_core_supported_ingress_w1/manifest.detjson`
6. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.d.ts`
7. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.js`
8. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool.manifest.detjson`
9. `solutions/seamgrim_ui_mvp/ui/wasm/ddonirang_tool_bg.wasm`
10. `tests/run_v1_core_supported_ingress_fault_injection_w1.py`
11. `tests/run_v1_core_supported_ingress_w1.py`
12. `tests/run_v1_core_supported_ingress_wasm_parity_w1.mjs`
13. `tool/src/ddn_runtime.rs`
14. `tool/src/runtime_surface.rs`
15. `tool/src/source_analysis.rs`
16. `tool/src/wasm_api.rs`

`git diff --check 0d9dd609... bc883fd...`는 PASS했다.

다음 비임대·권위 경로의 diff는 0이다.

- `docs/ssot/**`
- `publish/spec/**`
- `lang/src/parser.rs`
- `lang/src/lib.rs`
- `tool/src/canon.rs`
- `tool/src/main.rs`
- `tools/teul-cli/**`
- visible Workbench UI 전부; UI subtree diff 4개는 tracked WASM family뿐이다.

## 구현 구조 검토

### 단일 supported profile authority

- `tool/src/ddn_runtime.rs`가 `V1_CORE_SUPPORTED_SOURCE_PROFILE_IDENTITY = "v1-core-v25"`, `SupportedSourceProfile`, `resolve_supported_source_profile`을 소유한다.
- 누락·빈 profile은 `E_SOURCE_PROFILE_REQUIRED`, 알 수 없는 profile은 `E_SOURCE_PROFILE_UNSUPPORTED`로 fail closed한다.
- `tool/src/source_analysis.rs`와 `tool/src/runtime_surface.rs`는 이 resolver를 import해 사용한다.
- `tool/src/wasm_api.rs`의 새 export는 별도 resolver를 만들지 않고 native runtime surface를 호출한다.
- 고정 baseline `0d9dd609...`의 네 제품 파일에는 위 profile identity/resolver/constructor/WASM export symbol이 모두 0개였으므로 새 경계는 기존 숨은 authority의 별칭이 아니다.

### 동일 typed V25 constructor

- source analysis와 native run은 resolver 결과를 `DdnProgram::from_supported_source_profile_with_mode`로 전달한다.
- 이 constructor의 V1-Core arm은 `from_v25_source_with_mode`만 호출하고 named-call recursion validator를 통과시킨다.
- WASM run은 native `run_summary_from_supported_source_profile`을 호출하므로 동일 resolver와 constructor를 소비한다.
- supported path 안에 `from_v25...` 실패 뒤 `from_source...`를 재시도하는 branch는 0이다.

### VC/VD 행위

- VC01: 한국어 raw source fixture가 source analysis와 run에서 직접 소비된다. test-only lowering은 없다.
- VC02: Definition `:=`가 ACCEPTED다.
- VC03: Binding/Rebinding `<-`가 ACCEPTED하고 실제 run output은 `2`다.
- VC18: legacy Definition `=`는 `E_V25_DEFINITION_MIGRATION_REQUIRED`로 구조화 거부된다.
- VD01 direct recursion: `E_V1_CORE_RECURSION_UNSUPPORTED`로 결정적 거부된다.
- VD01 mutual recursion: 같은 code로 결정적 거부된다.
- recursion graph와 traversal은 `BTreeMap`/`BTreeSet` 기반이며 반복 payload가 byte-equivalent다.
- structured error 뒤 partial run summary leak은 0이다.

### authority·default 비침범

- hidden PreV25 retry/fallback: 제품 코드 구조상 0.
- global default switch: 0. 기존 strict/default run entrypoint와 `DEFAULT_PARSE_MODE`는 전환되지 않았다.
- 새 parser/canon authority: 0. `lang` parser/lib와 tool canon diff가 없다.
- public executable/command membership: 0. `tool/src/main.rs`와 `tools/teul-cli/**` diff가 없다.
- Workbench default ingress: 0. 새 WASM export는 생성물·테스트 외 visible UI caller가 없다.
- `v1-core-v25`는 이 slice의 explicit review identity이며 public stable spelling이나 installer alias를 승인하지 않는다.

## initial RED contract 실질성

고정 계보에 별도 test-only preimplementation commit은 없으므로 구현 전 시점의 역사적 `4/4 RED` 출력을 동일 commit identity로 재생할 수는 없다. 그러나 다음 근거로 RED contract가 실질적이며 self-fulfilling test가 아니라고 판정했다.

- product parent의 네 제품 파일에 profile resolver·supported constructor·WASM export가 모두 없었다.
- positive, legacy migration, recursion, profile omission assertions가 서로 다른 boundary를 고정한다.
- committed source mutation 3건이 각각 nonzero RED를 만들었다.
- 실제 fallback/retry를 별도로 주입했을 때 exact legacy migration boundary 두 건이 RED가 됐다.
- 원복 뒤 focused/native/WASM/tracked-WASM가 다시 GREEN이었다.

역사적 최초 RED 출력 자체는 handoff custody이며, 이번 verdict가 그 과거 로그를 새 독립 실행으로 재분류하지는 않는다.

## 독립 실행 결과

### focused·parity·regression

- `python tests/run_v1_core_supported_ingress_w1.py`: PASS
  - native focused: 6/6
  - native/WASM exact payload: 1/1
  - tracked-WASM cases: 8/8
  - deterministic repeats: 3
  - partial summary: 0
- `cargo test -p ddonirang-tool --lib`: 523/523 PASS
- `python tests/run_ddn_cli_wasm_freshness_check.py`: PASS

기존 dead-code/filename-collision warning은 있었으나 test failure나 신규 residue는 없었다.

### tracked WASM identity

- WASM Git blob bytes: `5,553,353`
- WASM Git blob SHA-256: `29480a59d264cffa280d6c1fb8a5a74da857955a6f028cd8b2adaf71e2366f51`
- JS Git blob bytes: `89,038`
- JS Git blob SHA-256: `c5a80302a3a872fab1e8d14c2385f8b5b6ddde8cfc1096c64ee0231e4ec8df3d`
- manifest Git blob object: `74ee08dfe743d41406ce0f0126fbe4a22dde6e43`
- manifest Git blob bytes: `18,938`
- manifest Git blob SHA-256: `7ad02442eb9b6542e586b86880b7814560611cf927a51cd657e2c72ddc7b843e`
- manifest source tree SHA-256: `7a152b44b689e91d9d48f0c1ec00aba5bd5d942bc486b60b76c538ff1dff2e37`
- new export occurrence in `export_names`: 1
- manifest closure claim은 `freshness_only_no_full_cli_wasm_equivalence`로 유지된다.

## mutation / fault injection

### committed runner 재실행

`python tests/run_v1_core_supported_ingress_fault_injection_w1.py` 결과:

1. `PROFILE_IDENTITY_DISABLED`: RED → exact restore
2. `HIDDEN_PREV25_RETRY`: RED → exact restore
3. `RECURSION_GUARD_BYPASS`: RED → exact restore

- final focused GREEN: 6/6
- restore SHA-256: `ed16acd803caa65ff5f88471ba675d1198087af71916b585faed02a8fa79ffbb`
- residue: 0

### reviewer correction injection

committed runner의 `HIDDEN_PREV25_RETRY`는 실제로는

```text
from_v25_source_with_mode -> from_source_with_mode
```

의 전면 치환이며 literal retry/fallback은 아니다. 이 점을 검토자가 발견해 다음 실제 변이를 별도로 주입했다.

```text
from_v25_source_with_mode(...)
  .or_else(|_| from_source_with_mode(...))
```

결과는 RED(exit 101)였다. 6개 focused test 중 2개가 실패했고, legacy `=`가 source analysis와 native run에서 잘못 ACCEPTED되는 것을 확인했다. 즉 현재 focused suite는 실제 hidden fallback도 포착한다.

변이 원복 과정에서 편집 도구가 일시적으로 CRLF를 LF로 정규화한 사실까지 검사해 원래 CRLF bytes로 다시 복원했다. 최종 source SHA-256은 `ed16acd...`, Git 상태는 clean이다. 제품·test 파일에는 reviewer correction을 남기지 않았다.

## protected resource custody와 재현성

- 검토 전 존재하던 protected Node PID 10개를 기록했고 종료 시 10/10 모두 생존했다.
- server, port, browser, protected process를 시작·중단·재시작·종료하지 않았다.
- 검토 test가 만든 cargo/rustc/python process는 종료 시 남지 않았다.
- Cargo target은 저장소 밖 `I:/home/urihanl/ddn/codex/target`을 사용했다.
- product fixed HEAD 검증 종료 시 detached/clean/staged 0/untracked 0/merge 0이었다.
- review parent로 복귀한 뒤 clean 상태에서 보고서를 작성했다.

## FOLLOW_UPS

1. non-blocking evidence correction: `tests/run_v1_core_supported_ingress_fault_injection_w1.py`의 `HIDDEN_PREV25_RETRY`를 실제 `.or_else(...)` fallback 변이로 바꾸거나, 현재 변이 이름을 `PREV25_PATH_SUBSTITUTION`처럼 실제 의미에 맞게 고친다.
2. 위 correction은 제품 source의 재작업 요구가 아니다. 이번 독립 주입으로 literal fallback 포착 능력은 확인됐다.
3. 향후 RED-first slice는 가능하면 test-only RED commit 또는 immutable RED log identity를 고정해 역사적 최초 RED를 fixed lineage에서 그대로 재생 가능하게 한다.

## NONCLAIMS / OPEN

이 verdict는 다음을 닫거나 승인하지 않는다.

- Foundation-12 correction/review
- actual 18/18 V1-Core membership
- 4/4 execution contract 전체
- 9/9 exclusion 전체
- public executable/command membership 또는 public stable profile spelling
- Workbench default ingress 또는 visible UI behavior
- whole P0/P1/V1 closure/readiness
- P2/P3/P4/P5/P6 또는 RC
- release, activation, legal status
- public SPEC product-status promotion
- Owner Human Smoke PASS, Human PASS, external-user success

SSOT current, public SPEC current, 제품 slice 구현, 독립검토 verdict, V1 membership, release, activation, Human PASS를 서로 분리한다.

## 최종 결론

`bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`는 explicit `v1-core-v25` supported ingress의 제한된 P1-A 제품/test slice로서 lineage, 16-path lease, shared resolver, V25 typed path, VC01/02/03/18, VD01 deterministic unsupported, native/WASM parity, tracked WASM freshness, mutation sensitivity와 residue 계약을 충족한다.

따라서 verdict는 `PASS_WITH_FOLLOW_UP`이다. 유일한 required follow-up은 fault-injection mutation의 이름/실제 의미 정합화이며 제품 rework나 broad closure 승격은 아니다.
