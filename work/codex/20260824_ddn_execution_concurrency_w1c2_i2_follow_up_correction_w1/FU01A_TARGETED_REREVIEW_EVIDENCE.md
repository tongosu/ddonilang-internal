# DDN-W1C2-I2-FU01A targeted 재검토 전 인계 증거

## 계보와 범위

```text
STARTING_PARENT: cb801ed576d2c7d4872b1b890e70b40edacc369e
PREVIOUS_PRODUCT_TEST_FIXED_HEAD: f6be35616418b748b7201f9fcfa48c2524c8bcd4
EVIDENCE_CORRECTION_COMMIT: 6d39254b6d2d6116b5839a3afffddb6ab40ce1ce
PRODUCT_TEST_FIXED_HEAD: 6d39254b6d2d6116b5839a3afffddb6ab40ce1ce
DEEP_RESEARCH_CHECK: NOT_USE
```

F1~F3 제품 구현은 다시 수행하지 않았다. 새 commit은 test/checker 세 파일만 바꿨고
`tool/src/**`, UI source, tracked WASM, manifest, SSOT와 SPEC의 diff는 0이다.

## 12축 fault injection과 외부 소비자

`tests/ddn_execution_concurrency_w1c2_i2_fault_injection_runner.mjs`는 각 축에서
원본 GREEN, 실제 mutation RED, raw-byte 원복, 복원 GREEN을 순서대로 검사한다.
compile RED나 inert mutation은 PASS로 세지 않는다.

| 그룹 | 축 | 결과 |
|---|---|---|
| F1 | builder `pub`; crate-root re-export와 public builder | 2/2 |
| F2 | prepare effect; provider-failure effect; merge-failure effect; precommit state; abort 뒤 outbox publish; commit 뒤 effect 중복 | 6/6 |
| F3 | wrong profile/toolchain; stale WASM; wrong manifest WASM path; source membership +1 | 4/4 |
| 합계 | required exact axes | 12/12 |

별도 외부 Cargo consumer가 `DdnRunner::with_internal_reaction_provider_registry`를
가져오면 정확히 `E0624` private-method compile failure가 난다. 외부 Rust injection API와
crate-root re-export 수는 각각 0이다. actual DdnRunner runner는 15/15이며 source/CLI/env/
WASM/UI public provider ingress도 모두 0이다.

## DB custody

두 해시는 동일 파일의 before/after가 아니다.

| identity | 절대 경로 | bytes | mtime | SHA-256 | WAL/SHM |
|---|---|---:|---|---|---|
| I2 runtime project DB | `I:/home/urihanl/ddn/codex/build/seamgrim_project_data/seamgrim_projects.sqlite3` | 540,672 | `2026-08-02T15:25:18.9785384+09:00` | `c8fdd4d47e20f7ad7ce4f095389991859432d5af0a87aa1f7b0b06e90fe44228` | WAL 0 bytes, `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; SHM 32,768 bytes, `fd4c9fda9cd3f9ae7c962b0ddf37232294d55580e1aa165aa06129b8549389eb` |
| official store DB | `I:/home/urihanl/ddn/codex/official-store/seamgrim-local-official-v1/seamgrim_projects.sqlite3` | 573,440 | `2026-08-09T17:19:08.2693667+09:00` | `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0` | WAL absent; SHM absent |

Runtime WAL mtime은 `2026-08-18T13:49:27.5828769+09:00`, runtime SHM mtime은
`2026-08-18T13:49:39.0778518+09:00`이다. 둘 다 FU01 시작 전 상태다.

I2 독립 보고서는 첫 경로를 540,672 bytes와 `c8fdd4...`로 전후 동일하게 기록했다.
FU01 인계는 둘째 경로의 기존 공식-store 봉인값 `3fbf028...`을 기록했다. W1-C1 마감
문서도 두 경로를 동시에 별도 identity로 열거한다. 두 mtime은 FU01 commit 시각
`2026-08-24T14:20:01+09:00`보다 오래됐고 FU01A 종료 재측정까지 해시가 같았다.

`c21c6820..cb801ed5` 및 `cb801ed5..6d39254b` diff에는 DB 파일·official write·activation
call path가 없다. 실행한 cargo/node/python/freshness 경로도 DB를 열지 않는다.

```text
DB_CUSTODY_VERDICT: DIFFERENT_DB_PATH_IDENTITY_CONFUSION
TASK_OWNED_OFFICIAL_WRITE_COUNT: 0
```

## 보호 PID/port custody

- I2 독립 검토 종료: PID `53196` python과 `127.0.0.1:8787` owner `53196` 유지.
- FU01 시작/종료 기록: PID absent, port not listening.
- FU01A 시작/종료 실측: PID absent, port not listening.
- FU01 Edge runner는 OS 할당 port를 쓰고 `port != 8787`, `child.pid != 53196`을
  assert한다. cleanup은 보관한 task-owned `server.child`만 `kill()`한다.
- FU01A는 Edge/process를 시작하거나 종료하지 않았다.

따라서 상태 단절은 I2 종료와 FU01 시작 사이의 외부 drift이며 FU01/FU01A 명령의
보호 프로세스 종료가 아니다. 보호 프로세스를 임의 재시작하지 않았다.

```text
PROCESS_CUSTODY_VERDICT: PREEXISTING_EXTERNAL_PROCESS_DRIFT + TASK_DID_NOT_TOUCH_PROTECTED_PROCESS
```

## UI/WASM 표현 분리

`f6be3561..6d39254b` 기준:

```text
WORKBENCH_UI_SOURCE_DIFF: 0
TRACKED_WASM_DIFF: 0
WASM_MANIFEST_DIFF: 0
USER_VISIBLE_UI_BEHAVIOR_DIFF: 0
```

FU01에서 봉인된 A/B/C/D/tracked artifact는 모두 5,509,880 bytes,
`27d18e40571e8987a3d0149840a231310e800b6895dcf469456958675017cbaa`다.
FU01A의 네 F3 mutation 뒤 raw hash 원복과 freshness `PASS`를 다시 확인했다.

## baseline failure custody

| 항목 | baseline `af7ad522` | current `6d39254b` | exact input/path와 인과 | follow-up |
|---|---|---|---|---|
| `ai_prompt_output_invariants_hold` | FAIL | FAIL | 각 clean worktree의 `docs/ssot` directory 자체가 없어 os error 3. I2/FU01 변경 아님 | SSOT bundle/bridge 환경 계약 OPEN |
| `ai_prompt_output_matches_golden` | FAIL | FAIL | 위와 동일. assertion skip/완화 0 | 위와 동일 |
| tool binary aggregate | 두 targeted test 0/2; baseline filter 395 | 현 binary 410/412, 같은 두 test만 FAIL | current exact filter에서 410 filtered + 2 failed | 사전 존재 OPEN |
| W1-C1 case 09 canon LF | exit 0, UTF-8 97 bytes, LF 1, SHA `753272403b0e414870474843891538037cc4b5c7f3f9c749032050be8c5295c3` | baseline과 byte-identical | input `pack/ddn_execution_concurrency_w1c1_sender_route_provider/09_exact_surface_canon_roundtrip/input.ddn`, 83 bytes, SHA `5db2088060c6a405f02c197db0ddce39a78c33a491fbcb7f2851c12c459d7ac7` | raw 제품 LF 회귀 없음; full orchestration 환경 후속 OPEN |
| W1-C1 full orchestration | fail-closed | fail-closed | `I:/home/urihanl/ddn/codex/build/worktrees/ddn-w1c2-i2-fu01-20260824/docs/ssot/SSOT_MASTER_v24.44.1.md` absent; case 00 native 전 차단 | historical v24.44.1 bundle custody OPEN |

공유 root의 live SSOT는 `docs/ssot/ssot/SSOT_INDEX_v24.53.0.md`가 CURRENT라고 명시한다.
이는 현행 읽기 전용 권위이며, historical runner가 요구하는 root-level
`docs/ssot/SSOT_MASTER_v24.44.1.md`를 대체하거나 임시 생성할 권한이 아니다.
SSOT/SPEC는 수정하지 않았다.

## 인계 판정

```text
FAULT_INJECTION: 12/12
EXTERNAL_CONSUMER_COMPILE_FAIL: PASS
DB_CUSTODY: RESOLVED_AND_NOT_TASK_OWNED_MUTATION
PROTECTED_PROCESS_CUSTODY: RESOLVED_AND_NOT_TASK_OWNED_TERMINATION
WORKBENCH_UI_SOURCE_DIFF: 0
PUBLIC_PROVIDER_SOURCE_INGRESS: 0
WASM_A_B_C_D_TRACKED_IDENTITY: PASS
READY_FOR_TARGETED_REREVIEW: YES
```

Codex는 plain PASS, I2 CLOSED, W1 전체 CLOSED, public surface/wire, activation 또는
Human PASS를 선언하지 않는다.
