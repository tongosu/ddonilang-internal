# [Codex관리Work -> 독립검증ClaudeCode] DDN-R-V1-FD01-I1-01

DDN V1 제품 마감 프로그램의 FD01 frontdoor/RuntimeBridge 준비도 감사를 독립 검토하라.

```text
REVIEW_ID: DDN-R-V1-FD01-I1-01
SCOPE: FD01_FRONTDOOR_RUNTIMEBRIDGE_READINESS_AUDIT_I1
AUDIT_FIXED_HEAD: 7002c31b83370ed432d3a6d91f3afde3b1e2b8a3
REQUIRED_REVIEW_PARENT: 71657a4e4a9f1f983b4ead889964196a9b699e78
BASELINE: 25a63aba7dc6ab362dd3f640385ad9a7ebfa0455
LIVE_INTERNAL_SSOT_AT_HANDOFF: v25.15.0
PUBLIC_LANGUAGE_SPEC_AT_HANDOFF: v0.5.0
```

검토 전 repository current를 다시 읽고 successor가 생겼으면 영향만
`UNAFFECTED / ADDITIVE / REBASE_REQUIRED / INVALIDATED`로 분류하라. SSOT나 SPEC을
직접 수정하지 말라.

## 반드시 독립 확인할 주장

1. fixed HEAD가 baseline의 선형 후손이고 merge가 0인지 확인한다.
2. audit diff가 테스트·팩·감사 문서뿐이며 제품 source, UI source, tracked WASM,
   `docs/ssot/**`, public SPEC을 바꾸지 않았는지 확인한다.
3. `parse_v25_with_mode`와 `DdnProgram::from_v25_source`의 존재와 실제 호출부를
   처음부터 추적한다.
4. 공식 CLI `run`/`run-summary`, 기본 WASM VM, source analysis가 현 시점에 어떤
   constructor를 쓰는지 추적한다.
5. 공개 V25 제품 ingress `0` 판정이 맞는지 source/CLI/env/WASM/UI 표면을 검색한다.
6. RuntimeBridge source analysis가 실제 Rust WASM export를 요구하고 누락·stale 결과를
   fail-closed하는지 확인한다.
7. native observation 경로가 JS semantic synthesis 없이 Rust/WASM manifest를 소비하는지
   확인한다. `observation_manifest.js`가 active인지 dead re-export인지 구분한다.
8. T5F current grid가 왜 RED인지 실제 tracked WASM runner로 재현하고, historical T5
   PASS와 current grid gap을 혼동하지 않는다.
9. 557개 lesson dual-parser inventory를 격리 build로 직접 재실행해 다음을 검증한다.

```text
total=557
both=0
pre_v25_only=127
v25_only=0
neither=430
v25_pass=0
```

10. diagnostic family `414 / 8 / 135`가 실제 제품 parser 결과인지 확인한다.
11. historical PC02 `04566a24...`의 diff·review 상태와 exact inverse `0dd73ab9` 계보를
    독립 확인한다. PC02를 current reviewed product로 승격하지 않는다.
12. 추천안 internal typed routing이 현 증거에서 합리적인지 검토하되, 새 공개 문법·wire를
    제안하거나 제품 구현을 시작하지 않는다.

## 실행

최소 다음을 fresh isolated target에서 수행한다.

```powershell
python tools/generate_v1_fd01_readiness_audit_i1.py
python tests/run_v1_fd01_readiness_audit_i1.py
cargo test -p ddonirang-tool --test v1_fd01_lesson_epoch_inventory --offline --locked -- --nocapture
node tests/seamgrim_workbench_runtime_bridge_t1_runner.mjs
node tests/seamgrim_workbench_source_analysis_t4_runner.mjs
node tests/seamgrim_workbench_observation_manifest_t4d_runner.mjs
node tests/seamgrim_workbench_observation_channel_t4f_runner.mjs
```

tracked WASM을 사용하는 T4와 T5F도 repository runner의 exact 환경 계약을 찾아
실행한다. T5F grid RED는 예상값을 베껴 쓰지 말고 실제 failure를 기록한다.

## 최소 fault injection

감사 checker가 실제 drift를 잡는지 다음을 각각 RED→exact restore→GREEN으로 확인한다.

1. default Rust constructor를 V25로 바꾼 것처럼 checker anchor 변이
2. source analysis가 다른 epoch를 쓰도록 변이
3. missing-WASM fail-closed code 제거
4. Workbench stale generation 검사를 무력화
5. native manifest 대신 JS builder를 active import
6. lesson inventory의 한 분류 또는 diagnostic expected count 변경
7. historical PC02 blind reapply flag를 true로 변경

정적 텍스트 변이가 실제 의미축을 잡지 못하면 원인을 쓰고 유효한 변이로 교정한다.

## 판정

```text
PASS
PASS_WITH_FOLLOW_UP
FAIL
BLOCKED_BY_AUTHORITY
BLOCKED_BY_MISSING_EVIDENCE
```

plain `PASS`는 감사의 사실·분류·기계 재현이 모두 정확할 때만 가능하다. plain PASS가
발행돼도 FD01 제품 구현, global V25 default, V1 membership, stable wire, activation,
release, Human PASS를 승인하지 않는다.

## 결과 custody

- review branch는 required parent의 직접 후손으로 만든다.
- report와 session delta만 commit한다.
- 제품 파일을 고치지 않는다.
- 검토용 worktree/target/process/profile/socket을 정리한다.
- 반환에는 verdict, review commit, report path/bytes/SHA-256, merge 수, 제품 diff,
  각 핵심 claim과 fault 결과를 포함한다.

결과 제목:

```text
[독립검증ClaudeCode -> Codex관리Work] DDN-R-V1-FD01-I1-01 — 결과
```

