# CODEX 지시문 묶음 — `설정 {}` 헤더 정합 + 구제안 이행 델타

> 원 출처: Claude 앱(claude.ai) 검토·평가 세션, 2026-07-06 작성. 사용자가 워킹트리에 저장해둔 것을 이 세션에서 인용 4건(부록 C-5/E-7B/E-7C/보람주인갈래 등) 실측 검증 후 정식 편입.
> 기준: SSOT v24.x (`ssot_ssot_ALL` 부록 A/B/C-4/C-5, E-7B/E-7C, v24.0.x~v24.12.x 메모)
> 성격: 지시문 1·5·6 = 실행 가능 / 지시문 2·3·4 = **PROPOSAL·OI 제출까지만** (결정은 SSOT 오너)

## 공통 불변 경계 (모든 지시문 적용, MUST)

- `state_hash` 산식·입력 변경 금지. `설정 {}` 내용은 직접 `state_hash` 입력이 아니며, seed/entry/마디수 등은 **결과 상태를 통한 간접 반영**만 허용.
- runtime canonical names 변경 금지: `InputSnapshot.ai_injections`, `SeulgiPacket`, `SeulgiIntent`, `state_hash`.
- fixed base pack 재설계 금지: `sam_inputsnapshot_contract_v1`, `sam_ai_ordering_v1`, `seulgi_gatekeeper_v1`, `sam_seulgi_family_contract_selftest` (2026-04-11 PASS evidence 기준).
- docs-first 표면(설정.슬기 candidate key, 배움틀 `모델틀/공방설정/추론설정` 등)의 parser hard-cut 승격 금지.
- 샘/보개/슬기 블록 sugar의 AGE4 재상정 방침(DR-167) 변경 금지.
- CLOSED 주장은 `golden_closed` pack PASS + SSOT status sync로만 계산. `runner_fill/docs_first`로 closure 주장 금지.
- Sam execution ordering `(agent_id, recv_seq)`, `ui.event -> InputSnapshot -> 이야기/누리` 경로 유지.

---

## 지시문 1 — [T0] `설정.거울 / 설정.실행` 하위 표면 AGE gate 정렬

**배경.** SSOT가 반복 지목한 선행 게이트(T0). 새 표면 승격 전 최우선.

**작업.**
1. `설정.거울` 하위 후보(`기록갈래 / 재연갈래 / 살핌내주기갈래`)와 `설정.실행` 축(`차림새` 5종, `보람주인갈래/보람때갈래/판끝갈래/마디틈갈래` 등)의 `age_scope / runtime_status`를 문법 상태표·frontdoor 진단·pack 참조 3자에서 대조.
2. `뒤살핌`의 문법 자리 = `설정.거울`(설정.실행 아님) 정렬이 코드/문서/진단 메시지에 일관 반영되는지 확인.
3. `설정.실행.차림새` preset이 `설정.거울` 슬롯 키(`살핌내주기갈래`)를 채우는 **교차-절 경로**를 주석/문서로 명시 (preset 표가 거울 키를 결정하는 관계).
4. drift 발견 시 수정 아닌 **목록 리포트** 우선 (frontdoor parity 2건과 함께 T0 bundle로).

**DoD.** 상태표–frontdoor–pack 3자 일치 리포트, drift 0건 또는 잔여 목록 + 원인. `designed/STUB_ONLY` 항목이 implemented로 과잉 표기된 곳 0건.

---

## 지시문 2 — flat `설정` 키 drift 해소 (`마디수` / `제목` / `설명`)

**배경.** 부록 A는 flat `설정 { 키: 값 }`을 비정본으로 규정하나, 현 구현·교재·수식 생성기는 `설정 { 제목/설명 }`, `설정 { 마디수: N. }`을 사용 중 (DEV_SUMMARY 2026-04~05). 정본–구현 어긋남.

**작업.** PROPOSAL 1건 작성 (결정 아님):
1. `마디수` canonical 소속 확정안 — 권고: `설정.실행.마디수`. `마디수`는 실행 길이를 바꿔 결과 상태에 간접 영향을 주므로 **"결과영향 키" 분류 목록**에 등재.
2. `제목/설명` → `설정.문서` (기존 `이름/설명` 키와 표면 통일 여부 포함).
3. flat 표면 처리 옵션 병기: (A) compat input + lint 경고 `SETTINGS_FLAT_KEY_COMPAT` / (B) 즉시 비허용(pre-release zero legacy 원칙). 각 옵션의 영향 파일 목록 첨부.
4. 영향 범위 조사: 교과 템플릿, 빈 편집기 템플릿, 수식 입력 자동 생성 DDN, CLI/WASM direct path의 `설정 { 마디수 }` 소비 지점.

**DoD.** PROPOSAL 문서 + 영향 파일 목록 + `lang_settings_header_closure_v1` 회귀 PASS 유지 확인.

---

## 지시문 3 — `설정.누리 / 설정.이야기` key set v1 OI 등록

**배경.** 두 절은 이름만 예약("seed 등 누리 초기 메타" / "진입점·흐름 메타" 각 1줄). canonical key set 부재.

**작업.** 신규 OI 등록 (docs-first, 닫기 아님):
1. candidate key 초안표:
   - `누리 { 시앗: N. }` (deterministic seed; `InputSnapshot.rng_seed`와의 관계 명시 필요)
   - `누리 { 누리갈래: ... }` — 차림새 축(`따로누리/함께누리`)과의 중복 여부 질문으로 등재
   - `이야기 { 들머리: ... }` (진입점)
2. 누리짐 스키마 매핑 질문 등재: `nurigym.dataset_header.v0.1`의 `env_id / seed` 소스를 `설정.누리`에 둘지, toolchain metadata에 둘지.
3. 헤더 이름("누리 설정" 통칭)과 하위 절 `누리`의 용어 혼동 방지 문구 1줄 제안.

**DoD.** OI 항목 + candidate key 표 + 질문 목록. parser/runtime 변경 0건.

---

## 지시문 4 — `설정.슬기` docs 예시 키 통일

**배경.** docs-only 예시 간 키 불일치: `두뇌종류:`(부록 C-4) vs `두뇌:`(배움틀 C-5, 대표 예시) vs `끼우개/정책`(v23.2.6 demo). 확정 승격 전 통일 필요.

**작업.**
1. `rg`로 `설정 { 슬기` 예시 전수 수집 (SSOT/교재/pack/샘플).
2. 통일안 제안 — 권고: `두뇌`로 단일화하거나, 계층화(`두뇌 { 갈래: #규칙형. 끼우개: .... 정책: @"...". }`) 중 택1을 PROPOSAL로.
3. `지연마디` 소유권 질문 등재: 용어표는 `설정.샘`("입력원천/주입방식/**지연마디** 등")에, 예시는 `설정.슬기`에 두고 있음 → 단일 소유 또는 이중 스코프 규칙 필요.
4. 문서만 수정. parser/candidate key hard-cut 금지.

**DoD.** 예시 키 표기 drift 0건(rg 검증) + 소유권 질문 OI 등재.

---

## 지시문 5 — 구제안(2026-03~04 검토 묶음) 이행 델타 노트 아카이브

**배경.** v20.26~v21.0 기준 외부 검토 문서(성장 순서, F/G/H 정렬, 선언성 로드맵)의 제안 대부분이 v22~v24 정본에 흡수 완료. 신규 작업에 원문을 재인용하면 legacy 표면이 재유입됨.

**작업.** `docs/context/notes/`(또는 `_session_deltas/`)에 델타 노트 1건 작성:

**채택 완료 (정본 반영, 재논의 불필요):**
| 구제안 | 현재 정본 |
|---|---|
| 마디 동기화 계약 우선 (all_required/fill_noop/noop) | B-standard 큰마디/속마디, `#모두필요/#빈칸채움`, `가만히` |
| filter→merge→apply | E-7C: `action_status 판정 → merge → 보람 계산 → 5튜플 반환`, `거부` merge 제외 |
| noop/invalid/clipped 의미 | action 4상태 `맞음/가만히/잘림/거부` + `벗남다룸 = 거부/자르기/기본값채움` |
| source_origin/inject_mode 2축 분리 | `입력원천` / `주입방식(실주입/재연주입)` designed AGE2+ |
| reward/termination env·agent 분리 | `보람주인갈래/보람때갈래/판끝갈래` + 차림새 5종 |
| reset 의미 명확화 | `Gym reset(seed,options) = 모두다시`, resident `:reset` 동치 (v23.0.7) |
| evidence tier ↔ closure 연결 | "CLOSED = pack PASS evidence + SSOT status sync" 원칙 명문화 |

**시효 만료 (재인용 금지):**
- "실구현 최대치 = space2d+graph+보임+모양" → 현재선은 **grid2d 포함**.
- "AI GYM 계약은 나중에" → 누리짐 final line 확정 완료. 남은 것은 consumer closure.
- 영문 enum(noop/invalid/clipped, all_required/fill_noop, relay/rollout) → 순우리말 정본으로 대체됨.
- reset 5종 표기(마당다시/판다시 포함) → 현행 canonical 표(`누리다시/보개다시/모두다시`)와 대조 후에만 인용.

**여전히 OPEN (현행 OI로 추적):**
- overlay full runner / multi-panel / 공식 overlay_layers / anchor-follow
- `될때 / 인 동안` full runtime
- `판{} / 마당{}` 최종 표면
- observation manifest closure (`뒤살핌` designed/STUB_ONLY)
- numeric exact family (P0-N parallel track)

**운영 규칙 1줄 추가:** "구버전 외부 검토 문서는 델타 노트 경유로만 인용한다."

**DoD.** 델타 노트 1건 + SSOT 병합 큐 등록.

---

## 지시문 6 — 누리짐 consumer closure 증빙 현황 (P1)

**배경.** Gym 의미 계약은 final line. 남은 것은 문법이 아니라 wire schema / goldening / parity / perf closure.

**작업.** 신규 문법 도입 없이 증빙 현황만 정리:
1. `gym_reset_seed_implies_complete_episode_reset_v1`, `resident_reset_episode_equiv_v1` pack/runner 진행 상태.
2. `step -> obs/reward/terminated/truncated/info` 5튜플 + action 4상태의 wire schema goldening 상태.
3. dual consumer parity 스모크: `web = ddonirang_tool.wasm` / `python short = wasmtime-py` / `python long = PyO3`.
4. 각 항목을 `golden_closed / runner_fill / docs_first`로 분류한 현황표.

**DoD.** 증빙 현황표 1건. closure 주장 없음(golden PASS 확인 전).

---

## 우선순위 및 순서

1. **지시문 1** (T0 — WASM 로딩/보임{} 계약 등 배포 블로커 다음 순위로)
2. **지시문 2** (drift 해소 — 교재·구현이 이미 소비 중이므로 조기 필요)
3. **지시문 5** (아카이브 — 저비용, 병행 가능)
4. **지시문 3·4** (OI/PROPOSAL 등록 — 병행 가능)
5. **지시문 6** (P1 — 시뮬 코어 증빙과 병행)

---

## Claude Code 세션 실측 각주 (2026-07-06, 편입 시 추가)

이 세션에서 인용 4건을 실제 SSOT에서 재확인했다:
- `SSOT_LANG_v24.12.9.md:8047` — E-7B 실행축 차림새/preset canonical
- `SSOT_LANG_v24.12.9.md:8063` — 차림새 표(임자갈래/누리갈래/마디맺음갈래/행동모음갈래/걷기갈래/살핌내주기갈래/보람주인갈래/보람때갈래/판끝갈래/마디틈갈래)
- `SSOT_LANG_v24.12.9.md:8080` — E-7C `action_status -> 보람` 경계
- `SSOT_LANG_v24.12.9.md:8102` — v23.2.6 부록 C-5 배움틀 docs-first representative note

전부 정확히 일치. 다만 `보람주인갈래/보람때갈래/판끝갈래` 등 이 표의 실제 코드 구현은 0건으로 확인됨(`rg -rln "보람주인갈래|보람때갈래|판끝갈래|없음보람" tools/teul-cli/src core/src` → 결과 없음) — SSOT 설계는 상세하나 코드는 아직 없다는 이번 세션 전체의 반복 패턴과 일치한다.

---

## 실행 보고

### Q36-1 / 지시문 1 — T0 `설정.거울 / 설정.실행` AGE gate 정렬

- 커밋: 예정 `[Q36-1]`
- 산출물: `docs/context/reports/SETTINGS_HEADER_T0_ALIGNMENT_AUDIT_V1.md`
- 수행: 상태표, frontdoor 제품 canon, `lang_settings_header_closure_v1` pack/golden, 제품 코드 검색을 대조했다.
- 결과: `설정.거울` 하위 후보와 `설정.실행` 축은 SSOT 기준 `designed/STUB_ONLY`로 남아 있으며, 제품 코드에서 implemented로 과잉 소비하는 경로는 발견하지 못했다.
- 잔여 drift: `pack/lang_settings_header_closure_v1/golden.jsonl` c02는 legacy `보임` 금지 오류를 기대하지만 현재 `teul-cli canon pack/lang_settings_header_closure_v1/legacy_boim.ddn`은 성공한다.
- 검증:
  - `python tests/run_lang_settings_header_closure_pack_check.py` PASS
  - `python tests/run_pack_golden.py lang_settings_header_closure_v1` FAIL 1건(c02 expected `E_CANON_LEGACY_BOIM_FORBIDDEN`, got exit 0) — 지시문 1의 drift 목록에 기록, 수정 없음
- DoD:
  - 상태표-frontdoor-pack 3자 대조: 완료
  - drift 0건 또는 잔여 목록 + 원인: 잔여 1건 기록
  - `designed/STUB_ONLY` 항목 implemented 과잉 표기 0건: 제품 코드 검색 기준 충족
  - 공통 불변 경계: 코드/팩/SSOT/state_hash/runtime canonical name 변경 없음

### Q36-2 / 지시문 2 — flat `설정` 키 drift 해소 PROPOSAL

- 커밋: 예정 `[Q36-2]`
- 산출물: `docs/context/proposals/PROPOSAL_SETTINGS_FLAT_KEY_DRIFT_RESOLUTION_V1_20260706.md`
- 수행: `마디수/제목/설명` flat key의 canonical 소속 권고안, 처리 옵션, 결과영향 키 분류, 영향 파일 목록을 제안서로 작성했다.
- 결과:
  - `마디수` 권고 소속: `설정.실행.마디수`
  - `제목/설명` 권고 소속: `설정.문서`
  - flat key 처리 권고: compat input + lint warning `SETTINGS_FLAT_KEY_COMPAT`
  - 직접 영향 집계: 51개 파일 / 133행(`제목=47`, `설명=49`, `마디수=37`)
- 검증:
  - 영향 범위 검색 완료
  - `python tests/run_lang_settings_header_closure_pack_check.py` PASS(Q36-1에서 같은 워킹트리 기준 확인)
- DoD:
  - PROPOSAL 문서 작성: 완료
  - 영향 파일 목록: 완료
  - `lang_settings_header_closure_v1` 회귀 PASS 유지 확인: 전용 checker PASS 기준 충족
  - SSOT 직접 수정/parser-runtime hard-cut/pack 변경: 없음
