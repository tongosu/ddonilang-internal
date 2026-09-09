# DDN-R-V1-P1A-FU01-EVIDENCE-CORRECTION-I1 독립 재검토 결과

## 판정

- VERDICT: `PASS`
- SCOPE: `DDN-R-V1-P1A-FU01-EVIDENCE-CORRECTION-I1`
- CORRECTION_PRODUCT_TEST_FIXED: `25a271bfab45ef5c0b5f9abb67d6323547e1f5b4`
- CORRECTION_FIXED_TREE: `3644bfb81f41c0226d395c26188cb87eb93b91c3`
- REREVIEW_PARENT: `9a5fca2fe6a8f1cad611a7998a23ecd3bcbb2300`
- REREVIEW_PARENT_TREE: `c2155b2f1889daf672e83e9ee5d65cda81a4c980`
- PREDECESSOR_REVIEW: `b65463cc8f6f981e290000ffb4e14e1db6699fad`
- REREVIEW_COMMIT: 이 보고서와 reviewer session delta만 포함하는 `REREVIEW_PARENT`의 direct successor. 정확한 hash는 commit 후 반환 메시지에 결속한다.

이 판정은 fault-injection evidence correction에만 대한 plain `PASS`다. 제품 source 재작업, broader P1-A closure, membership/readiness, release, activation 또는 Human PASS를 판정하지 않는다.

## 역할 선언

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex
- AI_CAPABILITY: targeted fixed-lineage evidence rereview
- SESSION_NICKNAME: DDN V1 P1-A FU01 독립재검토
- PROJECT_ROLE: INDEPENDENT_REVIEWER
- RETURN_LABEL: `[P1-A독립검토Codex -> DDN V1제품마감Codex]`
- DEEP_RESEARCH_CHECK: `NOT_USE` — 고정 commit과 로컬 test evidence의 제한 재검토다.

기존 reviewer task와 `C:/Users/ddongosu/.codex/worktrees/375b/codex`만 재사용했다. 새 task, worktree, branch, product writer를 만들지 않았고 기본 저장소 checkout을 수정하지 않았다.

## fixed lineage와 handoff identity

```text
b65463cc8f6f981e290000ffb4e14e1db6699fad  predecessor independent review
  -> 25a271bfab45ef5c0b5f9abb67d6323547e1f5b4  correction product/test fixed
    -> 9a5fca2fe6a8f1cad611a7998a23ecd3bcbb2300  docs-only rereview handoff
      -> REREVIEW_COMMIT  report + reviewer session delta only
```

- `25a271bf...`의 direct parent는 `b65463cc...`이고 tree는 `3644bfb8...`다.
- `9a5fca2f...`의 direct parent는 `25a271bf...`이고 tree는 `c2155b2f...`다.
- predecessor review부터 handoff까지 merge commit은 0이다.
- correction fixed diff는 `tests/run_v1_core_supported_ingress_fault_injection_w1.py` 한 파일뿐이다.
- handoff diff는 지정 handoff와 handoff session delta 두 파일뿐이다.

handoff Git blob:

- path: `work/codex/20260827_ddn_v1_product_closure_long_range_r1/P1A_FU01_EVIDENCE_CORRECTION_HANDOFF_20260829.md`
- bytes: `6,098`
- SHA-256: `6df8f4ffd11b3f7412887e84ad1917cb7c5b77badb773afe680b89f602e7bd64`
- Git object: `46092bdb9baa30868ebef390605157ed0c90a922`

corrected runner Git blob:

- bytes: `4,339`
- SHA-256: `68efdc3a831819f076cf1f5d3e18f64d26c21f5146e068078d62ee6ad054e33c`
- Git object: `8a60169d4f3b44e0b78ee1a0058b8847286447bf`

## correction diff 검토

### 네 mutation 축의 이름과 실제 의미

1. `PROFILE_IDENTITY_DISABLED`
   - supported profile identity match를 disabled spelling으로 바꾼다.
   - predecessor 축을 유지했다.
2. `PREV25_PATH_SUBSTITUTION`
   - `from_v25_source_with_mode(...)`를 `from_source_with_mode(...)`로 전면 치환한다.
   - predecessor에서 오해를 낳았던 `HIDDEN_PREV25_RETRY` 이름을 실제 의미에 맞게 정확히 바꿨다.
3. `HIDDEN_PREV25_RETRY`
   - V25 path 실패 뒤 `.or_else(|_| Self::from_source_with_mode(...))`를 호출한다.
   - 전면 치환이 아니라 실제 hidden PreV25 fallback/retry다.
4. `RECURSION_GUARD_BYPASS`
   - named-call recursion validator 호출을 우회한다.
   - predecessor 축을 유지했다.

각 축은 mutation target occurrence가 정확히 1인지 검사하고, nonzero RED뿐 아니라 예상 실패 test marker가 출력에 실제 존재하는지도 검사한다. 매 축 뒤 원래 runtime bytes를 복원하고 hash를 비교한 다음 focused GREEN을 다시 실행한다. 마지막에도 focused GREEN과 원본 hash를 재확인한다.

### 비대상 byte diff

`b65463cc... -> 25a271bf...`에서 다음은 diff 0이다.

- 제품 source 전체 `tool/**`
- pack
- tracked WASM과 visible UI 전체 `solutions/**`
- internal SSOT `docs/ssot/**`
- public SPEC `publish/spec/**`
- language/parser/canon/CLI authority 경로 `lang/**`, `tools/**`

즉 correction은 runner 한 파일의 evidence behavior만 바꾸며 제품 source, tracked WASM, SSOT, SPEC, visible UI bytes를 바꾸지 않는다.

## 독립 mutation 재실행

고정 HEAD `25a271bf...`에서 `python tests/run_v1_core_supported_ingress_fault_injection_w1.py`를 독립 재실행했다.

| mutation ID | 관찰 RED exit | 예상 signature | exact restore 뒤 focused |
|---|---:|---|---|
| `PROFILE_IDENTITY_DISABLED` | `101` | positive source analysis + native run | GREEN `6/6` |
| `PREV25_PATH_SUBSTITUTION` | `101` | positive source analysis + native run | GREEN `6/6` |
| `HIDDEN_PREV25_RETRY` | `101` | exact legacy migration + native fail-closed | GREEN `6/6` |
| `RECURSION_GUARD_BYPASS` | `3221225725` | deterministic direct/mutual recursion rejection | GREEN `6/6` |

최종 출력은 다음 identity에 결속됐다.

```text
P1A_MUTATION_PASS mutations=4 restore_sha256=ed16acd803caa65ff5f88471ba675d1198087af71916b585faed02a8fa79ffbb
```

네 축 모두 요구된 exit와 예상 signature를 정확히 냈다. 각 RED 뒤 exact restore와 focused GREEN을 통과했고 최종 Git status는 clean이었다.

### line-ending 층 분리와 exact restore

고정 runtime Git blob:

- Git object: `b928a9af77a490d103d24f0e0bdb39d34eb5f856`
- bytes: `1,110,630`
- SHA-256: `e81002d0f579a20960d5b90c3a82955c8f20bf46dcd6b339a756d0e87e0994a5`

reviewer checkout runtime 시작/종료 identity:

- bytes: `1,139,853` / `1,139,853`
- CRLF count: `29,223` / `29,223`
- SHA-256: `ed16acd803caa65ff5f88471ba675d1198087af71916b585faed02a8fa79ffbb` / 동일
- start/end byte sequence: exact equal
- runtime Git diff after all mutations: 0

handoff의 product worktree runtime identity `1,139,543 bytes`, CRLF `28,913`, SHA-256 `f8752ac4...`와 reviewer checkout identity가 다른 것은 checkout line-ending 층 차이다. 판정은 각 실행 worktree의 start/end bytes와 공통 Git blob `e81002d0...`을 함께 결속했다.

### 첫 시도의 환경 사건

첫 mutation 시도에서 `PROFILE_IDENTITY_DISABLED` RED 뒤 원복 GREEN을 링크할 때 공유 Cargo target의 test executable 잠금으로 `LNK1104`가 한 번 발생했다. runner의 `finally`가 원본 bytes를 복원했고 다음을 즉시 확인했다.

- runtime start/end SHA-256 동일: `ed16acd...`
- start/end bytes exact equal
- Git status clean
- cargo/rustc/test process가 모두 종료된 뒤 잠금 해제

보호 프로세스를 종료하지 않고 `CARGO_BUILD_JOBS=1`로 재실행했으며, 두 번째 실행은 위 네 축 전체를 끝까지 PASS했다. 이 환경 사건은 mutation signature 실패나 correction 결함이 아니며 residue를 남기지 않았다.

## focused·parity·regression·freshness

고정 HEAD `25a271bf...`에서 독립 실행한 결과:

- runner Python compile: PASS
- focused native: `6/6` PASS
- native/WASM exact payload: `1/1` PASS
- tracked-WASM: `8/8` PASS
- deterministic repeats: `3`
- partial summary leak: `0`
- `cargo test -p ddonirang-tool --lib`: `523/523` PASS
- official tracked WASM freshness: PASS
- `git diff --check`: PASS

기존 dead-code와 Cargo output filename collision warning은 있었으나 최종 실패나 파일 residue는 없었다.

## custody와 residue

- 검토 시작 시 기존 Node PID 10개를 기록했다.
- 검토 종료 시 그중 9개가 생존했다.
- 사라진 baseline PID: `60264`.
- reviewer는 어떤 Node/server/port/browser/protected process에도 stop, restart, kill 명령을 내리지 않았다.
- PID `60264`의 종료는 장시간 검증 중 외부 수명주기 변화로 관찰됐으며 reviewer 행위와 결속되는 종료 명령은 0이다.
- 새 persistent Node PID: 0.
- TCP 8787 listener: absent before any reviewer intervention and 종료 시 0.
- cargo/rustc/python/test process residue: 0.
- Python compile이 만든 exact ignored cache 파일은 reviewer task-owned residue로 제거했다.
- 제품/test fixed HEAD 검증 종료 시 clean/staged 0/untracked 0/merge 0이었다.
- handoff parent 복귀 뒤 detached/clean/staged 0/untracked 0/merge 0에서 이 보고서를 작성했다.

## NONCLAIMS / OPEN

이 targeted `PASS`는 다음을 닫거나 승인하지 않는다.

- 제품 source rework 또는 broader P1-A 제품 판정
- P1-A closure
- Foundation-12
- 실제 18/18 V1-Core membership
- 전체 4/4 execution contract 또는 9/9 exclusion
- public executable/command membership 또는 stable profile spelling
- Workbench default ingress 또는 visible UI behavior
- whole P0/P1/V1 closure/readiness
- P2~P6, RC, release, activation, legal status
- SSOT 또는 public SPEC product-status 승격
- Owner Human Smoke PASS, Human PASS, external-user success

SSOT current, public SPEC current, 제품 구현, evidence correction, independent targeted verdict, membership, release, activation, Human PASS를 서로 분리한다.

## 최종 결론

`25a271bfab45ef5c0b5f9abb67d6323547e1f5b4`의 FU01 correction은 predecessor substitution 축을 `PREV25_PATH_SUBSTITUTION`으로 정확히 개명하고 실제 `.or_else(...)` PreV25 fallback을 `HIDDEN_PREV25_RETRY`로 별도 추가했다. 기존 identity-disabled와 recursion-guard-bypass 축도 유지된다. 네 mutation 모두 요구된 RED exit와 signature, CRLF 포함 exact restore, focused GREEN을 독립 재현했으며 전체 focused/parity/lib/freshness 회귀도 PASS했다.

따라서 이 targeted evidence correction의 verdict는 plain `PASS`다.
