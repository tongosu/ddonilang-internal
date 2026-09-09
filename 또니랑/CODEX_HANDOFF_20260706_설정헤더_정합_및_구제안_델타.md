# CODEX 지시문 묶음 — `설정 {}` 헤더 정합 + 구제안 이행 델타

- 작성: 2026-07-06 (Asia/Seoul), Claude (검토·평가 역할)
- 기준: SSOT v24.x (`ssot_ssot_ALL` 부록 A/B/C-4/C-5, E-7B/E-7C, v24.0.x~v24.12.x 메모)
- 성격: 지시문 1·5·6 = 실행 가능 / 지시문 2·3·4 = **PROPOSAL·OI 제출까지만** / 지시문 7 = **AUDIT·경계 문구 제안** / 지시문 8·10 = **PROPOSAL·PACK_DESIGN** / 지시문 9 = **OI·AUDIT 등록 묶음** (결정은 SSOT 오너)

## 공통 불변 경계 (모든 지시문 적용, MUST)

- `state_hash` 산식·입력 변경 금지. `설정 {}` 내용은 직접 `state_hash` 입력이 아니며, seed/entry/마디수 등은 **결과 상태를 통한 간접 반영**만 허용.
- runtime canonical names 변경 금지: `InputSnapshot.ai_injections`, `SeulgiPacket`, `SeulgiIntent`, `state_hash`.
- fixed base pack 재설계 금지: `sam_inputsnapshot_contract_v1`, `sam_ai_ordering_v1`, `seulgi_gatekeeper_v1`, `sam_seulgi_family_contract_selftest` (2026-04-11 PASS evidence 기준).
- docs-first 표면(설정.슬기 candidate key, 배움틀 `모델틀/공방설정/추론설정` 등)의 parser hard-cut 승격 금지.
- 샘/보개/슬기 블록 sugar의 AGE4 재상정 방침(DR-167) 변경 금지.
- CLOSED 주장은 `golden_closed` pack PASS + SSOT status sync로만 계산. `runner_fill/docs_first`로 closure 주장 금지.
- Sam execution ordering `(agent_id, recv_seq)`, `ui.event -> InputSnapshot -> 이야기/누리` 경로 유지.
- `docs/ssot/**` 직접 수정 금지. SSOT 문구 변경이 필요하면 `docs/context/proposals/`, `docs/context/reports/`, `work/_session_deltas/` 중 하나로 라우팅한다.

---

## 지시문 1 — [T0] `설정.거울 / 설정.실행` 하위 표면 AGE gate 정렬

**배경.** SSOT가 반복 지목한 선행 게이트(T0). 새 표면 승격 전 최우선.

**작업.**
1. `설정.거울` 하위 후보(`기록갈래 / 재연갈래 / 살핌내주기갈래`)와 `설정.실행` 축(`차림새` 5종, `보람주인갈래/보람때갈래/판끝갈래/마디틈갈래` 등)의 `age_scope / runtime_status`를 문법 상태표·frontdoor 진단·pack 참조 3자에서 대조.
2. `뒤살핌`의 문법 자리 = `설정.거울`(설정.실행 아님) 정렬이 코드/문서/진단 메시지에 일관 반영되는지 확인.
3. `설정.실행.차림새` preset이 `설정.거울` 슬롯 키(`살핌내주기갈래`)를 채우는 **교차-절 경로**를 리포트/제안서로 명시한다. SSOT 본문 수정은 사용자/SSOT 오너 반영 대상으로 둔다.
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
1. `rg`로 `설정 { 슬기` 예시 전수 수집 (SSOT/교재/pack/샘플). `docs/ssot/**`는 읽기 전용 근거로만 사용한다.
2. 통일안 제안 — 권고: `두뇌`로 단일화하거나, 계층화(`두뇌 { 갈래: #규칙형. 끼우개: .... 정책: @"...". }`) 중 택1을 PROPOSAL로.
3. `지연마디` 소유권 질문 등재: 용어표는 `설정.샘`("입력원천/주입방식/**지연마디** 등")에, 예시는 `설정.슬기`에 두고 있음 → 단일 소유 또는 이중 스코프 규칙 필요.
4. 문서 산출은 전수조사표 + 통일안 PROPOSAL/OI 후보까지로 제한한다. parser/candidate key hard-cut 금지, `docs/ssot/**` 직접 수정 금지.

**DoD.** 예시 키 drift 전수조사표 + 통일안 PROPOSAL + `지연마디` 소유권 질문 OI 후보. SSOT 오너 반영 뒤 별도 단계에서 drift 0건(rg 검증)을 목표로 한다. parser/runtime 변경 0건.

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
- reset 관련 구버전 문장 → 현행 v24.12.9 reset kind 5종(`마당다시/판다시/누리다시/보개다시/모두다시`) 의미표와 대조 후에만 인용. 특히 Gym episode reset은 `모두다시`, authoring reset은 `누리다시`, view-only reset은 `보개다시`로 구분한다.

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

## 지시문 7 — 언어 정체성·교육·국제화·게임엔진 경계 감사 (P1)

**배경.** 또니랑은 "한국어로 결정적 세계를 정의하고 재현하는 언어"라는 정본 정체성을 갖고 있으며, 교육·누리짐·말힘누리·교착어권 표면으로 확장되는 제품선을 가진다. 다만 이를 "범용 프로그래밍 언어", "완성된 국제어", "풀스택 게임 엔진", "현대 언어 이론 전체 교육과정"으로 과잉 주장하면 SSOT·구현·검증 상태와 어긋난다.

**작업.** AUDIT 보고서 1건 작성 (결정 아님):
1. 네 역할별 주장-근거 매트릭스 작성:
   - 선언적 시뮬레이션: `누리/마디/InputSnapshot/state_hash/replay`로 닫힌 부분과 `세움/잇기/될때/인 동안` 등 아직 열려 있는 부분 분리.
   - 교육/현대 언어 이론: 초심자 문법·세계 모델링·결정성·상태/입력/재연 교육에는 강점이 있으나, 타입 이론/증명론/효과 시스템/컴파일러 이론 전체 커리큘럼으로 닫지 않음.
   - 한국어 기반 교착어권 국제 표면: 한국어 정본 + `sym3` + 방언 후보의 방향성은 강점이지만, `ko-common` 및 T2 언어군은 native review·pack equivalence 전까지 "국제어 완성" 주장 금지.
   - 게임 엔진 역할: world kernel/game-logic engine/DrawList producer로는 주장 가능하나, 렌더링·에셋·오디오·네트워크·편집기까지 포함한 full game engine 주장은 금지.
2. 각 역할을 `closed / conditional / proposal / not-claim`로 분류하고, 문구 예시를 함께 제안한다.
3. 공개 문구 권고안을 작성한다:
   - 권장: "한국어 네이티브 결정적 세계 모델링 언어", "교육용 시뮬레이션 언어", "게임 월드 로직 커널", "교착어권 친화 표면을 목표로 하는 다언어 DSL".
   - 비권장: "범용 언어", "완성된 국제어", "완성형 게임 엔진", "현대 언어학/프로그래밍 언어 이론 전체를 대체하는 교육과정".
4. 다음 증빙 필요 목록을 만든다: 대표 교육 vertical slice, dialect native review 표, dialect pack equivalence, DrawList adapter smoke, 누리짐 consumer parity, 언어이론 학습 범위표.
5. 보고서는 `docs/reports/audit/`에 두고 `docs/reports/audit/INDEX.md`를 갱신한다. SSOT 본문 변경이 필요하면 별도 PROPOSAL/OI로만 올린다.

**DoD.** 감사 보고서 1건 + 주장-근거 매트릭스 + 권장/비권장 문구표 + 증빙 gap 목록. parser/runtime 변경 0건, `docs/ssot/**` 수정 0건, closure 주장 없음.

---

## 지시문 8 — 보개 표준팩/lowering 계약 설계 (P1)

**배경.** `격자겸콘솔 / 2D / 3D` 큰 길은 이미 `console_headless / web2d / engine3d` 백엔드 축과 `grid2d / sim2d / graph2d / grid3d / game3d` 프로필 축으로 정리되어 있다. 남은 문제는 사용자가 `모양` 원자만으로 그래프·표·게임판·슬기 실험실을 직접 조립하지 않도록 표준 보개팩과 lowering 계약을 준비하는 것이다.

**작업.** PROPOSAL 1건 작성 및 후속 pack 후보 등록:
1. `std_bogae_grid2d`, `std_bogae_graph2d`, `std_bogae_table`, `std_bogae_timeline`을 1차 표준 보개팩으로 정의한다.
2. `std_bogae_nurigym`, `std_bogae_seulgi_lab`을 2차 표준 보개팩으로 정의한다.
3. `std_bogae_grid3d`, `std_bogae_game3d`는 engine adapter와 연결되는 3차 표준 보개팩으로 둔다.
4. 각 보개팩마다 의미 payload, lowering 규칙, backend capability gate, `state_hash/view_meta/InputSnapshot` 경계를 표로 작성한다.
5. 특히 `graph2d`는 축·눈금·범례·series·label collision·auto tick deterministic policy를 포함해, 사용자가 그래프를 `모양` 원자만으로 직접 조립하지 않도록 한다.
6. `sim2d/grid2d/timeline/table`은 좌표계·축·카메라·궤적·벡터·충돌 영역·시간 조절·상태표·state diff를 기본 제공 대상으로 분류한다. 사용자는 시뮬레이션별 특수 생김새와 도메인 표시만 커스텀하는 것을 목표로 한다.
7. `std_bogae_network`, `std_bogae_tree`, `std_bogae_matrix`, `std_bogae_form_control`, `std_bogae_surface`, `std_bogae_profiler`, `std_bogae_debugger`를 추가 후보로 유지한다.
8. 산출물 기준 문서: `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md`.

**DoD.** 표준 보개팩 목록 + graph2d lowering 계약 + 시뮬레이션 기본 제공 항목 + 제품선별 기본 묶음 + pack 후보 ID + OI 후보 목록. parser/runtime 변경 0건, `docs/ssot/**` 수정 0건, closure 주장 없음.

---

## 지시문 9 — `설정 {}` 헤더 추가 고려 4건 OI/AUDIT 등록 묶음 (P1)

**배경.** 설정 헤더 검토(2026-07-06)에서 나온 추가 고려사항. `지연마디` 소유권은 지시문 4-3에, 차림새 교차-절 경로는 지시문 1-3에 이미 포함되어 있으므로 여기서는 나머지 4건만 다룬다. 전부 OI/AUDIT 등록까지만, 닫기 아님.

**작업.**
1. **"결과영향 키" 분류 AUDIT + OI.** `설정 {}` 키를 두 부류로 나누는 분류표 초안 작성: (a) 결과 상태에 간접 영향을 주는 키(`시앗`, `마디수`, `들머리` 등) / (b) 순수 메타 키(`제목`, `설명`, `말씨` 등). replay 검증·감사 lint가 기계적으로 참조할 수 있는 형식(detjson 후보)으로 제안. 부록 A의 "간접 반영" 규칙을 키 단위로 구체화하는 것이 목적.
2. **보개 선택 이중 경로 AUDIT.** 샘플·교재에서 `보개종류 <- "콘솔격자"` 류 **런타임 대입**으로 보개를 고르는 지점을 `rg`로 전수 수집. `설정.보개` 선언 경로와의 관계를 (A) 대입식 compat 유지 / (B) 설정.보개로 이관 + lint 경고 두 옵션으로 정리해 OI 등록. view 선택이 세계 상태에 섞이는지(state_hash 오염 여부) 각 지점별로 표기.
3. **하위 절 이름 다국어 별칭 커버리지 점검.** 8개 하위 절 이름(`문서/실행/이야기/누리/샘/거울/보개/슬기`)이 dialect 키워드 매트릭스(T1: ko-common/en/ja/mn/tr)에 등재되어 있는지 대조표 작성. 누락분은 다국어 심볼 익스포트 파이프라인(PROPOSAL_MULTILANG_SYMBOL_EXPORT) 백로그에 연결.
4. **프로젝트 수준 상속 범위 OI 1줄 등록.** `뿌리.ddn`의 `실행기본 {}`은 실행축만 커버함. `설정.문서.말씨`/`설정.보개` 등 비실행 절의 프로젝트 수준 기본값 허용 여부를 `프로젝트 {}` closure 시점에 함께 다룰 항목으로 OI에 등재만 한다 (지금 설계 금지).

**DoD.** 분류표 초안 1건 + 대입식 보개 선택 전수조사표 + 다국어 커버리지 대조표 + OI 2건 등록. parser/runtime 변경 0건, `docs/ssot/**` 수정 0건.

---

## 지시문 10 — 누리 시간/마디/태스크 경합 계약 심화 (P1)

**배경.** 누리 커스텀에서 가장 중요한 축 중 하나는 "시간을 어떻게 걷고, 큰마디/속마디를 어떻게 닫고, 여러 입력·태스크·임자 행동이 경합할 때 무엇을 적용하는가"다. 이 논의는 `설정.누리` 하나에 넣기보다 `설정.누리/설정.실행/설정.샘/설정.슬기/설정.거울` 경계로 나눠야 한다.

**작업.** PROPOSAL 1건 작성 및 후속 pack 후보 등록:
1. 큰마디는 shared world 공식 commit 단위, 속마디는 local progression/proposal/trace 단위로 정리한다.
2. completion 정책 `#모두필요/#빈칸채움`, missing vs `가만히`, action_status 4종(`맞음/가만히/잘림/거부`)의 경계를 표로 작성한다.
3. 경합 처리 파이프라인을 `모으기 -> 빈칸처리 -> 바른꼴화 -> 검증/보정 -> 거르기 -> 합치기 -> 적용 -> 보람 -> 판끝 -> 기록`으로 정리한다.
4. deterministic merge policy 후보(`priority/majority/turn_order/slot_owner`)를 pack evidence 필요 항목으로 분리한다.
5. 슬기 지연마디(`accepted_madi/target_madi`), late drop, `(agent_id, recv_seq)` execution ordering, duplicate/reverse seq fail 규칙을 한 표로 정리한다.
6. 설정 블록 경계를 나눈다: `설정.누리`는 세계 정체성/초기조건/rule pack, `설정.실행`은 마디 운용/completion/merge/reward/termination, `설정.샘`은 입력 봉인, `설정.슬기`는 AI 제안/지연, `설정.거울`은 기록/재연.
7. 산출물 기준 문서: `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md`.

**심화 v2 추가 항목 (2026-07-06 Claude 검토 반영).**
8. **큰마디 위상표(phase table) 초안.** action 파이프라인만이 아니라 한 큰마디 전체의 canonical 위상 순서를 표로 제안: 입력동결(샘) → 속마디/제안 → action 파이프라인(모으기~적용) → 매마디 본문/세움 재평가/흐름씨 전파 → 훅 4가족(`할때/될때/인 동안/마다`)·`바뀔때마다` 실행 위상 → 보람/판끝 → 거울 기록 → 보개 방출. 각 훅이 어느 위상에 끼는지 질문 목록 포함. E-7C(action 순서)와 모순 금지.
9. **상태 쓰기 경합 × `덩이 {}`/`미루기` 통합.** action merge 밖의 일반 상태 쓰기 경합(같은 마디에 두 임자/규칙이 같은 변수를 쓰는 경우)을 다룬다: 큰마디 commit과 `덩이` 경계의 관계, 복수 `미루기`가 같은 대상을 겨눌 때의 deterministic tie-break(정렬 키 후보: 선언 순서 / `(agent_id, recv_seq)` 유래 / FATAL). 옵션 병기, 결정은 SSOT 오너.
10. **속마디 관측 격리 규칙.** 속마디의 읽기 경계를 명시: 기본 후보 = 직전 큰마디 commit 상태만 관측(snapshot isolation), 다른 임자의 tentative proposal 비가시. 속마디 수가 결과에 영향을 주지 않음을 불변식으로 제안.
11. **reset 5종 상호작용표.** reset kind별로 `설정.누리/실행/샘/슬기` 키가 재적용되는지, 지연 중 슬기 패킷(`target_madi` 미래분)·미적용 InputSnapshot이 어떻게 되는지 표로 작성. 지시문 9-1(결과영향 키 분류)과 교차 참조.
12. **키 충돌·명명 정리.** `합치기갈래` ↔ 기존 `행동모음갈래`(차례모음/보탬모음) 중복 여부 선행 검토. `세계영향경계` 키는 불변식 재진술이므로 후보에서 제외 권고. 영문 후보명(`priority/majority/turn_order/slot_owner`, `accepted_madi/target_madi`, `world_family`)의 순우리말 정본 후보 병기.
13. **기본 운용형 평가.** 설정을 거의 건드리지 않았을 때의 의미를 "동기식 큰마디 commit 기반 결정적 turn/tick engine"으로 평가하고, realtime/async/rollback/OS scheduler가 아님을 명시한다.
14. **일반 preset vs 고급 preset 분리.** `교과기본/체험기본/배움기본/협동기본/놀이기본`은 일반 사용자 preset으로, `물리실험고급/슬기실험고급/경합실험고급`은 고급자용 후보로 분리한다.
15. **고급 옵션 위험표.** `#빈칸채움`, `합치기갈래`, `priority/majority/turn_order`, `지연마디`, `늦은제안다룸`, `rollback` 후보는 초심자 UI에 노출하지 않고, pack evidence와 위험 설명이 붙은 고급 설정으로만 다룬다.

**DoD.** 시간/마디 모델 표 + 큰마디 위상표 초안 + 상태 쓰기 경합/덩이 통합 옵션표 + 속마디 관측 격리 불변식 + reset 상호작용표 + completion/action_status/merge 규칙표 + 기본 운용형 평가 + 일반 preset/고급 preset 표 + 고급 옵션 위험표 + 설정 블록 경계표 + 지연마디 소유권 OI 후보 + pack 후보 ID. parser/runtime 변경 0건, `docs/ssot/**` 수정 0건, closure 주장 없음.

---

## 지시문 11 — 7목적 고도화 G1 실행 묶음 (P0~P1)

**배경.** `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md`가 7목적(AI Gym/한국어 Manim/게임엔진/교육/선언시뮬/교착어권/AI친화)의 고도화를 F0 공통 기반 + 목적별 G1/G2/G3로 설계했다. 이 지시문은 그중 **즉시 실행 가능한 G1 항목만** 실행한다. G2/G3는 설계 고정/구현 보류 — 착수 금지.

**공통 경계.** 본 문서 공통 불변 경계 전부 적용. 신규 문법 도입 0건. F0-1(WASM 복구)은 별도 최우선 트랙이며 이 지시문과 병행.

**작업.** (독립 항목 — 병렬 가능, 각각 별도 세션 권장)
1. **[F0-2] 결정적 벤치 계약**: `perf_baseline_v1` 설계서 + 러너 스켈레톤. 고정 시앗 시나리오 3종(tick 처리량/WASM 로드 시간/Gym rollout step·초), 기준선 detjson, 회귀 게이트(±X%) 1개. 측정 실행은 비트 동일 원칙.
2. **[P1-G1] `nurigym.step_record.v0.2` PROPOSAL**: `raw_action/normalized_action/action_status/merged_action/applied_action` 필드 추가안 + `nurigym_step_record_v02_roundtrip_v1` pack 후보. v0.1과의 호환 규칙 명시.
3. **[P4-G1] 진단 3층 AUDIT**: 대표 E-코드 20종의 현재 메시지를 ①무엇이 ②어디서 ③어떻게(fix-it) 3층 기준으로 채점하고, 초심자 문구 사전 초안(detjson)을 작성. `diag_three_layer_message_v1` pack 후보 등록. 메시지 실변경은 SSOT 오너 승인 후.
4. **[P5물리-G1] 적분기 pack**: `적분.오일러/반암시적오일러/선형보간` pack skeleton + runner (AGE4 MUST 후보 연결, 기존 방향 유지). Fixed64 권장 dt/stiff 한계 1쪽 문서.
5. **[P5경제-G1] model-first 스켈레톤 3종**: 수요-공급 균형/통화 공급/세금-후생. agent-first 5종과 이름·구조 대칭. evidence tier = skeleton/docs_first 명시.
6. **[P6-G1] ko-common 승격 실측**: 승격 4조건(core_keyword_matrix/josa_role_matrix/roundtrip golden/native 확인) 체크리스트 실측 리포트. 미충족 항목별 남은 작업량 추정.
7. **[P7-G1] LLM 코퍼스 파이프라인 프로토타입**: 기존 pack/골든에서 정본 예제+설명 쌍 추출 → `out/llm_corpus_v1.jsonl`. 같은 저장소 상태 = 같은 코퍼스(결정적 추출). grammar manifest 기반 문법 카드 포함.

**DoD.** 항목별 산출물 7건 + 각자 pack 후보 ID + DEV_SUMMARY 갱신. parser/runtime 신규 문법 0건, `docs/ssot/**` 수정 0건, G2/G3 착수 0건, closure 주장 없음.

---

## 지시문 12 — [Codex] 2026-07-06 논의 SSOT 병합 준비 묶음

**배경.** 오늘 논의 산출물을 SSOT에 반영하려면, `docs/ssot/**` 직접 수정이 금지이므로 **병합 준비물**(패치 초안 + 큐 등록)을 만들어 또니가 반영하는 경로를 탄다.

**대상 산출물 (전부 2026-07-06):**
- `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md` (지시문 1~14)
- `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md`
- `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md`
- `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md`
- `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md`
- `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md`
- `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md`
- `docs/context/notes/IDEAS_DDONIRANG_ENRICHMENT_V1_20260706.md`

**작업.**
1. **SSOT 패치 초안 작성**: 각 제안서의 "결정 후보"를 SSOT 문장 형식(어느 SSOT 파일 어느 절에 어떤 문장을 추가/수정하는지)으로 정리한 `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md` 1건. 결정/후보/질문을 명확히 분리 — 후보를 결정처럼 쓰지 않는다.
2. **OI 후보 일괄 등록 초안**: 오늘 나온 OI 후보 전건(설정.누리 key set, 지연마디 소유권, 위상표 OQ 1~4, OQ-R1, 합치기갈래↔행동모음갈래, 결과영향 키 분류, 보개 이중 경로 등)을 OI 형식으로 정리.
3. **발표 전 동결 스윕 실측**: (a) 오늘 문서들의 G2/G3 후보 표면명 + IDEAS 문서의 "주의" 표면명(`가설/검산/단위 정의/~분포` 등)이 reserved 등재돼 있는지 rg 대조 (b) 미사용 기호 조합이 조용히 식별자로 허용되는 지점 목록 (c) E_* 코드 체계 현황표. 결과는 `docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md`.
4. **pack 후보 ID 중복 검사**: 오늘 신설 pack 후보 20여 건과 기존 pack 이름 충돌 여부.
5. DEV_SUMMARY / PROJECT_STATUS 갱신.

**DoD.** 패치 초안 1건 + OI 등록 초안 1건 + 동결 스윕 리포트 + 중복 검사 결과. `docs/ssot/**` 수정 0건, parser/runtime 변경 0건.

---

## 지시문 13 — [Claude Code] 병합 준비물 감사

**배경.** 지시문 12 산출물을 또니가 병합하기 전에 Claude Code가 감사한다. 실행자(Codex)와 감사자(Claude Code)를 분리하는 것이 이 체계의 핵심이다.

**감사 체크리스트.**
1. **경계 준수**: `docs/ssot/**` 무변경, parser/runtime 무변경, 공통 불변 경계(본 문서 상단) 위반 0건을 `git status`/diff로 확인.
2. **주장 등급**: 패치 초안에서 후보→결정 승격 과잉, closure 과잉 주장(golden PASS 없는 CLOSED) 탐지.
3. **용어 drift**: 영문 enum 재유입(noop/rollback/priority 등이 정본 자리에 들어갔는지 — 정본은 가만히/되물림/앞선모음 계열), historical 표면(`매틱/중단/전이마다/예약`) 재유입.
4. **교차 참조 정합**: 지시문 번호·파일 경로·pack ID가 실제 존재하는지, 제안서 간 상호 인용이 맞는지.
5. **SSOT 권위 순서 준수**: 패치 초안이 MASTER > TERMS > DECISIONS > ... 순서에 맞는 파일을 겨냥했는지.

**산출.** `docs/reports/audit/SSOT_MERGE_AUDIT_20260706.md` — 항목별 PASS/FAIL + 수정 요구 목록. FAIL 존재 시 병합 보류 권고. `docs/reports/audit/INDEX.md` 갱신.

---

## 지시문 14 — [Codex 실행 + Claude Code 감사] AI 닫힌 베타 Round 0

**배경.** `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md`의 프로토콜을 따른다. 상세(페르소나/과제/로그 형식/격리 규칙)는 그 문서가 정본.

**Codex 작업.**
1. `BETA_USER_BUNDLE` 구성 (시작 가이드 부재 시 과제 0으로 초안 작성).
2. **새 세션 3개**(페르소나별 독립, SSOT 비제공)에서 과제 매트릭스 실행, friction log를 `work/beta/round0/`에 기록.
3. 지식 격리 준수: 제공 문서 밖 지식으로 우회하지 않는다 — 문서에 없으면 그것이 발견이다.

**Claude Code 작업.**
4. 프로토콜 §5대로 재현 검증 → 중복 병합 → P0~P3 분류 → 원인 4분류(문법/문서/진단/구현).
5. `docs/reports/audit/BETA_ROUND0_AUDIT.md` 작성. **문법 결함 후보는 수정하지 말고 또니 승인 큐로만.**

**DoD.** friction log 15건+ (또는 "마찰 없음" 명시) + 감사 보고서 + P0/P1 목록 + OI 전환 제안. `docs/ssot/**` 수정 0건. Round 0 종료 조건: P0 = 0.

---

## 지시문 15 — [Codex] 설계 확정분 구현 착수 (2-Tier)

**배경.** 2026-07-06 설계 묶음 중 구현 가능분을 개발한다. 단 SSOT 미병합 설계를 parser/runtime canon에 넣는 것은 금지이므로 2단계로 나눈다.

### Tier A — 즉시 구현 가능 (도구층·pack·러너: SSOT 병합 불필요)

1. **`perf_baseline_v1` 러너 구현** (7목적 설계 F0-2): 고정 시앗 시나리오 3종 벤치 + 기준선 detjson + 회귀 게이트. `tests/run_perf_baseline_check.py` 형태.
2. **LLM 코퍼스 추출기 구현** (P7-G1): 기존 pack/골든 → `out/llm_corpus_v1.jsonl` 결정적 추출. 같은 저장소 상태 = 같은 출력 검증 포함.
3. **적분기 pack 구현** (P5물리-G1): `적분.오일러/반암시적오일러/선형보간` — 기존 AGE4 MUST 후보 경로이므로 stdlib/pack 층에서 진행, 새 문법 0.
4. **경제 model-first pack 스켈레톤 3종** (P5경제-G1): 수요-공급/통화/세금-후생. evidence tier 명시.
5. **`설정해시` 프로토타입 — 도구층만**: 정본화된 `설정 {}` 블록의 BLAKE3 다이제스트를 계산하는 **독립 checker 스크립트** (`tests/tools/config_digest_proto.py`). 런타임/기록 스키마에는 넣지 않는다 — 정본화 입력 정의 검증용 프로토타입.
6. **예약어 스윕 lint 도구**: 지시문 12-3의 실측을 반복 가능하게 만드는 스크립트 (reserved 목록 vs 문서·샘플의 식별자 사용 대조).
7. **BETA_USER_BUNDLE 구성 + 오류 3종 fixture** (지시문 14 과제 T4용 — Claude Code가 지시문 16-5에서 설계한 명세를 따름).

### Tier B — SSOT 병합 후 해금 (착수 금지, 준비만)

- `nurigym.step_record.v0.2` 구현, `시앗묶음` 런타임, `설정.누리` key set, `행동모음갈래` 값 확장, 위상표 계약 코드화, `설정해시` 기록층 통합.
- **해금 조건**: 지시문 12 패치 초안 → 지시문 13 감사 PASS → 또니 병합 → 해당 항목이 SSOT에 반영 확인. 그 전에는 Tier A 프로토타입과 설계 정교화(지시문 16)까지만.

**공통 경계.** 본 문서 공통 불변 경계 전부. 새 문법 0건, `docs/ssot/**` 수정 0건, state_hash 산식 불변. 각 항목 완료 시 `cargo check`/관련 pack PASS + DEV_SUMMARY 갱신.

**DoD.** Tier A 7건 각각: 코드 + 실행 증빙(PASS 로그) + evidence tier 표기. Tier B: 착수 0건 확인.

---

## 지시문 16 — [Claude Code] 설계안 정교화 (구현 등급으로)

**배경.** 오늘 제안서들은 방향·경계 수준이다. Codex가 Tier B를 구현하려면 스키마·엣지케이스·오류코드까지 정밀해야 한다. Claude Code가 각 설계를 **구현 등급 부속서(annex)**로 정교화한다.

**공통 산출 형식** — 대상 제안서마다 `docs/context/proposals/{원제안서명}_ANNEX_A.md`:
(a) 정확한 스키마 표(필드/타입/필수 여부/기본값) (b) 엣지케이스 표 (c) 오류 코드 배정안(`E_*` 체계 준수) (d) pack DoD + golden fixture 스케치 (e) 남은 결정 질문 3개 이하로 압축.

**대상 및 정교화 요점.**
1. **큰마디 위상표** (`..._PHASE_WRITE_CONFLICT_DEEPDIVE_...`): P0~P7을 상태기계 의사코드로. 훅 4가족 × 위상 배치 결정표. `(N마디)마다` 판정 시점(OQ-4) 옵션별 결과 차이 예시 3개. 쓰기 경합 W1~W3 각각의 최소 재현 DDN 예제.
2. **`설정해시`** (`..._MAX_CUSTOM_SURFACE_...` §2.1): 해시 입력의 정확한 정의 — 정본화 AST 직렬화 규칙, 절 정렬 순서, `문서` 절 포함/제외(권고: 제외 — 순수 메타), 부동 표기 정규화. 다이제스트 불일치 시 오류 코드와 override 플래그 표면.
3. **`시앗묶음`** (§2.2): 유도 함수 명세 — `BLAKE3(뿌리시앗 ∥ 도메인이름)` 형식, 스트림 이름 충돌 규칙, `주사위씨` 연결 표면 초안, 미지정 시 뿌리 공유의 하위 호환 규칙.
4. **`step_record.v0.2`**: v0.1 대비 필드 표 + 마이그레이션 규칙(v0.1 리더가 v0.2를 만났을 때) + roundtrip golden fixture 1개 스케치.
5. **베타 오류 fixture 명세** (지시문 14 T4): 문법/타입/계약 오류 각 1을 심은 진자 변형 파일 설계 — 어떤 오류를, 어떤 줄에, 어떤 진단이 나와야 하는지 기대표 포함.
6. **보개마당 트랙 v1** (7목적 P2-G2): `자막/해설/강조` 3트랙 스키마 + 마디 키 타임라인 + `seamgrim.scene.v0`와의 관계(확장인가 병렬인가) 판정.

**경계.** CLAUDE.md 준수: `docs/ssot/**` 수정 금지, 구현 착수 금지(정교화 문서까지만), 후보를 결정처럼 쓰지 않기, 각 annex 말미에 "본 문서는 구현 등급 설계이며 SSOT 병합 전 canon 아님" 명기.

**DoD.** annex 6건 + 각각 남은 질문 ≤3개 + `work/_session_deltas/`에 세션 기록. 이후 흐름: **지시문 16(정교화) → 또니 결정 → 지시문 12/13(병합·감사) → 지시문 15 Tier B(구현) → Claude Code 구현 감사**.

---

## 우선순위 및 순서

0. **F0-1 WASM 복구** (별도 최우선 트랙 — 모든 목적의 전달층)
0-1. **지시문 12 → 13** (SSOT 병합 준비 + 감사 — 오늘 논의 휘발 방지, 즉시)
0-2. **지시문 14** (AI 닫힌 베타 Round 0 — CLI 기반, WASM과 무관하게 지금 가능)
0-3. **지시문 16** (Claude Code 설계 정교화) ∥ **지시문 15 Tier A** (Codex 도구층 구현 — 병렬 가능)
0-4. **지시문 15 Tier B** (SSOT 병합 후에만 해금)
1. **지시문 1** (T0 — 배포 블로커 다음 순위로) / **지시문 11** (7목적 G1 — 병렬 세션 가능)
2. **지시문 2** (drift 해소 — 교재·구현이 이미 소비 중이므로 조기 필요)
3. **지시문 5** (아카이브 — 저비용, 병행 가능)
4. **지시문 7** (감사 — 제품/교육/국제화/게임엔진 과장 주장 방지, 병행 가능)
5. **지시문 10** (누리 시간/마디/태스크 경합 — 세계 실행 의미 기반)
6. **지시문 8** (보개 표준팩/lowering — 그래프·교육·게임 사용성 기반)
7. **지시문 3·4·9** (OI/PROPOSAL/AUDIT 등록 — 병행 가능)
8. **지시문 6** (P1 — 시뮬 코어 증빙과 병행)
