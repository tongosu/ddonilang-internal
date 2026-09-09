# [VC09독립검토Work -> 제품마감관리 heartbeat] DDN-R-V1-VC09-NAMED-CALLABLE-EVIDENCE-REBASE-I1 — 독립 검토 결과

## 판정

`PASS_WITH_FOLLOW_UP`

고정 대상 `23f6087e1a932d9c813c485fa117c58da20e081c`의 VC09 named-callable evidence slice는 지정된 구조·실행·실패폐쇄·tamper 복원 계약을 충족했다. 다만 handoff에 적힌 fault-run 집계 identity `bafb74452f32fcac5030dde94d159094420f9929292ffba502979df9c83197b2`는 같은 fixed tree에서 독립 재현한 `9a1660715619ad4c96253477202d4bd1d612ff89d40e800cba5aae729bf4bbb9`와 일치하지 않는다. 개별 파일 identity, Git blob, fixed tree, tamper 전후 task-owned identity는 모두 일치하므로 제품 증거 실패가 아니라 handoff 집계값 기록 drift로 한정한다.

이 판정은 이 VC09 evidence slice에만 적용된다. VC09 binding·promotion, P1-A/P1/V1 readiness·closure, V1 membership, release, activation, Human PASS와 외부 사용자 성공은 모두 `OPEN`이며 이 검토로 바뀌지 않는다.

## 검토 계약과 역할

- `FROM`: 제품마감관리 heartbeat
- `TO` / `EXECUTOR` / `REVIEWER`: VC09독립검토Work
- `RETURN_TO`: 제품마감관리 heartbeat
- `CONTROL_OWNER`: 언어Chat
- `MANAGER`: 개발관리Work
- `FILE_OWNER`: 이 보고서와 대응 session delta 정확히 두 문서
- `ORIGIN_TASK_ID`: `DDN-R-V1-VC09-NAMED-CALLABLE-EVIDENCE-REBASE-I1`
- `DEEP_RESEARCH_CHECK`: `NOT_USE` — 고정 로컬 commit·제품 frontdoor·tamper 재현만으로 판정 가능한 과업

검토 worktree는 새 worktree/branch 생성 없이 지정 경로 `C:\Users\ddongosu\.codex\worktrees\3a1f\codex`만 사용했다. shared root `I:\dev\ddonilang\codex`는 운영·SSOT current 확인을 위한 읽기만 수행했고 reset/clean/stash/stage하지 않았다.

## 입력 및 시작 상태

- review parent HEAD: `6220e4c9929c8e6328270fc54ecc509017fac9d5`
- fixed evidence HEAD: `23f6087e1a932d9c813c485fa117c58da20e081c`
- baseline: `88c8bd664c03320f53baaaa917da11d7770a462a`
- fixed tree: `eb4a4341260938876d41243f5af1d51f7e6cafc1`
- 시작 상태: exact review parent / detached HEAD / clean / staged 0 / merge 0
- 현재 SSOT 확인: v25.19.0 live current, docs-first/product-open; actual V1 membership·numeric maturity는 0, readiness floor는 `UNCLAIMABLE`
- 관련 의미 경계: RD-370 callable-local result는 semantics-closed이나 exact CFG/diagnostic/product migration은 OPEN

## 구조·계보 감사

| 항목 | 독립 확인 | 결과 |
|---|---|---|
| fixed direct parent | `23f6087e^ = 88c8bd66...` | PASS |
| baseline → fixed direct lineage | commit 1, merge 0 | PASS |
| fixed tree | `eb4a4341260938876d41243f5af1d51f7e6cafc1` | PASS |
| changed path 수 | 17 | PASS |
| changed path 집합 | handoff의 leased 17 paths와 exact set match | PASS |
| `git diff --check` | 출력 없음 | PASS |
| 보호 경로 diff | product source, tracked WASM, `docs/ssot/**`, public SPEC, visible UI, `lang/`, `tool/`, `tools/teul-cli/` 모두 0 | PASS |

전체 baseline→fixed diff가 `pack/v1_core_named_callable_evidence_rebase_w1/**` 14경로와 runner 3경로뿐이므로 product source lease는 0이다.

## packet identity와 6-case bijection

Windows checkout의 text raw bytes는 CRLF 변환으로 커질 수 있어 handoff 계약대로 CRLF→LF만 정규화한 identity와 Git blob을 대조했다.

| 파일 | 정규화 bytes / SHA-256 | Git blob | 결과 |
|---|---|---|---|
| manifest | 2,019 / `b3ffe6c96853da2789b836d9311677908002da8286f3d6c3b26d101fb70d66ed` | `8bcccd899fa3b93f0b811c15a3a98ac0199a6cfe` | PASS |
| native runner | 13,520 / `1060c1d8244303acd85c6a7a0656a5b42a23f8890022640b260b7eb9aeae4e71` | `3fae3a8c44e07d8972501676989d50cdc2c55dd5` | PASS |
| WASM runner | 7,157 / `b6ee7162fe7f0641eb777d19894b1e697680d2699c9f25bb31cdb8cecd32e45f` | `591b6fb6f1dd3fdb5df2aa5d12628e7ae5f84cdb` | PASS |
| fault runner | 5,383 / `79e5455a360fedf29097d96d550bcc0cbc3b3f79175ba5c39a3adb7b6f7df13b` | `74700cab9aee752b7d658eb6fcb26e4acc93ed43` | PASS |

manifest는 case count 6, 고정 order, fixture 6개와 expected receipt 6개의 1:1 bijection, `repeat_count=3`, `ticks=1`, profile `v1-core-v25`를 고정한다. fixture/receipt 정규화 SHA-256은 전부 manifest와 일치했다.

## 제품 frontdoor 실행 결과

### native

명령:

```text
python tests/run_v1_core_named_callable_evidence_rebase_w1.py
```

결과:

```text
VC09_NATIVE_EVIDENCE_PASS cases=6 success=2 failure=4 deterministic_repeats=3 partial_publish=0 supplementary_cases=3 supplementary_commands=3
```

### tracked WASM parity

명령:

```text
node tests/run_v1_core_named_callable_wasm_parity_w1.mjs
```

결과:

```text
VC09_WASM_PARITY_PASS cases=6 native_wasm_exact=6 deterministic_repeats=3 partial_publish=0 freshness=PASS tracked_wasm_refresh=0
```

native와 WASM은 선택 필드가 아니라 각 case의 전체 success/error result object를 exact 비교했다.

### case-level contract

| case | 독립 관찰 | 판정 |
|---|---|---|
| NC01 | `(2, 3) 더하기` → output `5`; source/preprocess identity 동일 | PASS |
| NC02 | input `IDENTITY` → output `IDENTITY`; source/preprocess identity 동일 | PASS |
| NC03 | unknown callable → `E_EXECUTION_PARSE`, partial publish 0 | PASS |
| NC04 | arity mismatch → `E_EXECUTION_PARSE`, partial publish 0 | PASS |
| NC05 | declared type mismatch → `E_RUNTIME_EXECUTION`, partial publish 0 | PASS |
| NC06 | recursion attempt → `E_V1_CORE_RECURSION_UNSUPPORTED`, partial publish 0 | PASS |

NC01 source/preprocess SHA는 `ed3e97d0...`, NC02는 `f0746bd9...`로 각각 fixture identity와 같았다. success output은 수 인자 계산 결과와 글 인자 identity를 보존했고, failure object에는 output/state/effect publication 금지 필드가 없었다.

### 회귀

```text
cargo test -p ddonirang-tool --lib
test result: ok. 523 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

## tamper RED → exact restore → GREEN

명령:

```text
python tests/run_v1_core_named_callable_fault_injection_w1.py
```

| 축 | RED signature | 결과 |
|---|---|---|
| case omission | `VC09_CASE_COUNT_MISMATCH` | PASS |
| case order | `VC09_CASE_ID_OR_ORDER_MISMATCH` | PASS |
| fixture hash | `VC09_FIXTURE_HASH_MISMATCH` | PASS |
| receipt | `VC09_RECEIPT_HASH_MISMATCH` | PASS |
| outcome | `VC09_OUTCOME_MISMATCH` | PASS |
| profile identity | `VC09_PROFILE_IDENTITY_MISMATCH` | PASS |

최종 marker:

```text
VC09_FAULT_INJECTION_PASS mutations=6 exact_restore=6 native_green=1 wasm_green=1 residue=0 tracked_identity_sha256=9a1660715619ad4c96253477202d4bd1d612ff89d40e800cba5aae729bf4bbb9
```

tamper는 임시 packet 복사본 안에서만 수행되었다. task-owned 원본의 before/after identity는 exact 같았고 fixed checkout은 clean/staged0/merge0로 돌아왔다.

## 구현 경계 감사

- Python native runner는 임시 Rust harness를 만들고 `ddonirang_tool::runtime_surface::run_summary_from_supported_source_profile`를 호출한다. Python 의미 구현·parser·canon·token rewrite는 없다.
- JS runner는 tracked `wasm_run_summary_with_source_profile_json` export를 호출한다. JS 의미 구현·lowering은 없다.
- 두 runner의 원문 변환은 checkout 독립성을 위한 CRLF→LF 한 가지뿐이다.
- `v1-core-v25` resolver는 profile 누락/unknown을 fail-closed한다.
- supported profile 제품 경로는 `DdnProgram::from_v25_source_with_mode`를 한 번 호출하고 named-callable recursion 검사를 수행한다. 실패 후 PreV25 parser 재시도·downgrade 경로는 없다.
- baseline→fixed에서 `lang/`, `tool/`, `tools/teul-cli/` diff가 0이므로 test-only semantic implementation이 제품 의미로 가장되지 않았다.

## tracked WASM와 보호 자원 custody

- WASM: 5,553,353 bytes / SHA-256 `29480a59d264cffa280d6c1fb8a5a74da857955a6f028cd8b2adaf71e2366f51` / blob `899c2734f4267339edf15a8bdfb5aaf70ba33797`
- JS: 정규화 89,038 bytes / SHA-256 `c5a80302a3a872fab1e8d14c2385f8b5b6ddde8cfc1096c64ee0231e4ec8df3d` / blob `215249c3ab0dd441f4b9a7a200f33b83f4c43cfb`
- tracked manifest: 19,506 bytes / SHA-256 `b3daeb51b7e0d65348b6461785b0aaf34568dd1b624ec43d3d38e77962a21537`
- tracked WASM refresh: 0
- Node PID baseline/제품·tamper 검증 종료: exact 동일 14/14 (`17232,29264,35048,45264,46564,47736,49768,56500,56632,56872,57068,58644,60632,61732`)
- 문서 커밋 뒤 최종 관찰에서는 PID `47280`이 추가되었다. 시작 명령은 Codex app-tools MCP의 `node.exe ./server.mjs`, 부모는 `launch_codex_app_tools_mcp.cmd`였고 이 과업이 실행한 제품/WASM test child가 아니다. 이 reviewer는 해당 프로세스를 시작·중지·재시작·kill하지 않았다.
- TCP 8787 listener: absent → absent
- server/browser/port/protected-process start·stop·restart·kill 명령: 0

## follow-up

제품마감관리/Evidence Custodian은 fixed tree를 기준으로 handoff의 `tracked_identity_sha256=bafb...` 기록이 왜 독립 재현값 `9a1660...`와 다른지 확인하고, 필요하면 handoff correction successor에서 집계값만 바로잡아야 한다. 이 follow-up은 fixed product/evidence commit 수정이나 VC09 binding 권한을 부여하지 않는다.

## 최종 비주장

이 문서는 independent review verdict만 기록한다. VC09 binding은 수행하지 않았고, owner CURRENT/SSOT pointer, 제품 source, test, pack, WASM, UI, public SPEC, `lang/`, `tool/`, `tools/teul-cli/`는 수정하지 않았다.
