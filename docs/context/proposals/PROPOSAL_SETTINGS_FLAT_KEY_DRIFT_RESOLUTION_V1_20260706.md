# PROPOSAL_SETTINGS_FLAT_KEY_DRIFT_RESOLUTION_V1_20260706

## 상태

- 분류: PROPOSAL / LANG / TOOLCHAIN / DOCS
- 작성: 2026-07-06
- 출처: Q36-2 / `BRIEF_SETTINGS_HEADER_ALIGNMENT_AND_LEGACY_PROPOSAL_DELTA_V1`
- 결정 상태: 미확정. SSOT 오너 결정 필요.
- 구현 범위: 없음. 이 문서는 parser/runtime hard-cut을 제안하지 않고 영향 범위를 정리한다.

## 문제

SSOT current line은 file-leading meta root를 `설정 {}`로 고정하고 하위 절을 `문서 / 실행 / 이야기 / 누리 / 샘 / 거울 / 보개 / 슬기`로 나눈다. 그러나 제품 경로와 교과 자산은 아직 flat key를 직접 쓴다.

```ddn
설정 {
  제목: "포물선 운동".
  설명: "초기 속도와 중력을 바꾸며 포물선 운동을 관찰합니다.".
  마디수: 240.
}.
```

이 표면은 사람이 읽기 쉽고 이미 UI/CLI가 소비하지만, canonical 소속이 불분명하다. 특히 `마디수`는 실행 길이를 바꿔 최종 상태에 간접 영향을 주므로 단순 문서 메타로 볼 수 없다.

## 권고안

| flat key | 권고 canonical 소속 | 분류 | 이유 |
|---|---|---|---|
| `마디수` | `설정.실행.마디수` | 결과영향 키 | 실행 tick 수를 바꿔 결과 상태와 state_hash를 간접적으로 바꾼다. 단 `설정` 자체를 state_hash 입력에 직접 넣지는 않는다. |
| `제목` | `설정.문서.이름`의 input compat alias 또는 `설정.문서.제목` | 문서 키 | UI와 교재는 `제목`을 자연스럽게 쓰지만 기존 SSOT 예시는 `이름/설명` 축을 갖는다. |
| `설명` | `설정.문서.설명` | 문서 키 | 기존 SSOT와 제품 UI가 모두 같은 한국어 키를 쓴다. |

`제목`은 사용자-facing으로 자연스럽다. 다만 이미 `설정.문서 { 이름: ... }` 예시가 있으므로, 아래 둘 중 하나를 정해야 한다.

| 선택지 | 내용 | 장점 | 단점 |
|---|---|---|---|
| A. `이름` canonical, `제목` compat | 정본 출력은 `설정.문서.이름`, 입력은 `제목`도 허용 | 기존 SSOT 문구와 맞음 | UI/교재 표현과 정본 출력이 달라짐 |
| B. `제목` canonical, `이름` compat | 정본 출력은 `설정.문서.제목`, `이름`은 alias | 교재/제품 UI와 자연스럽게 맞음 | 기존 SSOT 예시 수정 필요 |

권고는 B다. 교재와 제품 UI에서 `제목`이 이미 압도적으로 자연스럽고, `설명`과 짝을 이룬다. 단 SSOT 오너가 기존 `이름` 용어를 파일 identity로 유지하려면 A도 가능하다.

## flat 표면 처리 옵션

| 옵션 | 정책 | 진단 | 영향 |
|---|---|---|---|
| A. compat input + lint | `설정 { 제목/설명/마디수 }` 입력은 계속 허용하고, 정본/신규 예시는 하위 절로 유도 | `SETTINGS_FLAT_KEY_COMPAT` warning | 기존 lesson/UI/tests 보존. migration이 점진적이다. |
| B. 즉시 비허용 | flat key를 pre-release zero legacy 원칙으로 금지 | hard error | 51개 파일/133행 이상의 자산과 제품 소비 경로를 즉시 고쳐야 한다. |

권고는 A다. 이유는 `마디수`가 이미 `teul-cli run`과 셈그림 UI의 실제 실행 길이로 소비되고 있어 즉시 hard-cut하면 제품 경로가 깨진다.

## 결과영향 키 목록

초기 목록:

| key | canonical | state_hash 관계 |
|---|---|---|
| `마디수` | `설정.실행.마디수` | 직접 state_hash 입력은 아니다. 실행 마디 수가 달라지면 결과 상태가 달라질 수 있으므로 간접 반영된다. |

비목록:

| key | canonical | state_hash 관계 |
|---|---|---|
| `제목` | `설정.문서.제목` 또는 `설정.문서.이름` | 문서 메타. 직접 state_hash 입력 금지. |
| `설명` | `설정.문서.설명` | 문서 메타. 직접 state_hash 입력 금지. |

## 영향 범위 조사

검색 방법:

```text
rg -l "설정\s*\{" pack solutions tests tools --glob "*.ddn" --glob "*.js" --glob "*.mjs" --glob "*.rs" --glob "*.md"
Select-String -Pattern "^\s*(제목|설명|마디수)\s*:"
```

집계:

| key | 직접 행 수 |
|---|---:|
| `제목` | 47 |
| `설명` | 49 |
| `마디수` | 37 |
| 합계 | 133 |

영향 파일 수: 51개.

### 소비 지점

| 영역 | 파일/행 | 현재 동작 | 영향 |
|---|---|---|---|
| CLI run | `tools/teul-cli/src/cli/run.rs:3081` | `find_setting_key(body, "마디수")`로 flat `마디수`를 읽는다 | `설정.실행.마디수`로 옮기려면 parser/pre-scan 소비 경로 추가 필요 |
| CLI 진단 | `tools/teul-cli/src/cli/run.rs:3124` | `E_SETTING_MADI_BAD_VALUE` | canonical 변경 시 진단 문구도 소속을 말해야 함 |
| CLI tests | `tools/teul-cli/src/cli/run.rs:7540`, `:7566`, `:7585` | flat `마디수` test fixture | migration 대상 |
| WASM/UI run | `solutions/seamgrim_ui_mvp/ui/screens/run.js:462-473` | `readConfiguredMadiFromDdnText`가 flat `마디수/max_madi/maxMadi/ticks`와 `채비` resource `마디수`를 읽는다 | compat 유지 없이는 UI runtime limit이 깨짐 |
| WASM/UI rewrite | `solutions/seamgrim_ui_mvp/ui/screens/run.js:1846-1853` | `설정 {}` 안에 flat `마디수`를 삽입한다 | 신규 출력 정책 변경 필요 |
| legacy rewrite | `solutions/seamgrim_ui_mvp/ui/screens/run.js:1860-1863` | `title/desc/최대마디`를 `제목/설명/마디수`로 바꾼다 | canonical이 하위 절로 바뀌면 rewrite target 변경 |
| 빈 편집기 템플릿 | `solutions/seamgrim_ui_mvp/ui/app.js:142-143`, `solutions/seamgrim_ui_mvp/ui/screens/editor.js:2-3` | `설정 { 제목/설명 }` 생성 | `설정.문서` 예시로 migration 필요 |
| 수식 입력 자동 생성 | `solutions/seamgrim_ui_mvp/ui/formula_sugar.js:116-117` | `제목/설명` 생성 | `설정.문서` 예시로 migration 필요 |
| 첫 실행 템플릿 | `solutions/seamgrim_ui_mvp/ui/free_lab_first_run.js:24-25` | `제목/설명` 생성 | `설정.문서` 예시로 migration 필요 |
| 셈그림 대표 lesson | `solutions/seamgrim_ui_mvp/lessons/**/lesson.ddn` | flat `제목/설명/마디수` 다수 | migration 대상 |
| 대표 pack lesson | `pack/edu_seamgrim_rep_*_v1/lesson.ddn` | flat `제목/설명/마디수` 다수 | migration 대상 |
| CLI/WASM parity pack | `pack/seamgrim_wasm_cli_runtime_parity_v1/cases/c10_*`, `c12_*`, `c13_*` | flat `마디수` 계약 pack | canonical 변경 시 golden/runner 검토 필요 |

### 파일별 직접 flat key 목록

아래 목록은 `설정 {}`가 있는 파일 안에서 `제목/설명/마디수`가 줄 시작 key로 나온 파일만 세었다. 일반 설명 텍스트는 제외했다.

| 파일 | key count |
|---|---|
| `pack/edu_seamgrim_rep_cs_linear_search_timeline_v1/lesson.ddn` | 제목:1, 설명:1, 마디수:2 |
| `pack/edu_seamgrim_rep_econ_supply_demand_tax_v1/lesson.ddn` | 제목:1, 설명:1, 마디수:2 |
| `pack/edu_seamgrim_rep_math_function_line_v1/lesson.ddn` | 제목:1, 설명:1 |
| `pack/edu_seamgrim_rep_phys_projectile_xy_v1/lesson.ddn` | 제목:1, 설명:1, 마디수:2 |
| `pack/edu_seamgrim_rep_science_phase_change_timeline_v1/lesson.ddn` | 제목:1, 설명:1, 마디수:2 |
| `pack/seamgrim_wasm_cli_runtime_parity_v1/cases/c10_setting_madi_count/input.ddn` | 제목:1, 설명:1, 마디수:1 |
| `pack/seamgrim_wasm_cli_runtime_parity_v1/cases/c12_setting_madi_bad_value/input.ddn` | 마디수:1 |
| `pack/seamgrim_wasm_cli_runtime_parity_v1/cases/c13_bogae_draw_madi_view_sugar/input.ddn` | 제목:1, 설명:1, 마디수:1 |
| `solutions/seamgrim_ui_mvp/lessons/rep_*` | 31개 파일, 제목/설명 중심, 대표 시뮬 lesson은 마디수 포함 |
| `solutions/seamgrim_ui_mvp/samples/15_console_grid_maze_probe.ddn` | 제목:1, 설명:1, 마디수:1 |
| `solutions/seamgrim_ui_mvp/samples/16_space2d_bounce_probe.ddn` | 제목:1, 설명:1, 마디수:1 |
| `solutions/seamgrim_ui_mvp/seed_lessons_v1/roguelike_grid_pathfind_v1/lesson.ddn` | 제목:1, 설명:1, 마디수:1 |
| `solutions/seamgrim_ui_mvp/ui/app.js` | 제목:1, 설명:1 |
| `solutions/seamgrim_ui_mvp/ui/free_lab_first_run.js` | 제목:1, 설명:1 |
| `solutions/seamgrim_ui_mvp/ui/screens/editor.js` | 제목:1, 설명:1 |
| `tests/seamgrim_bogae_madi_graph_ui_runner.mjs` | 제목:1, 설명:1, 마디수:1 |
| `tests/seamgrim_studio_draft_runtime_runner.mjs` | 제목:1, 설명:1 |
| `tools/teul-cli/src/cli/run.rs` | 마디수:3 |

## 제안되는 migration 순서

1. SSOT 오너가 `제목` vs `이름` canonical을 결정한다.
2. `설정.실행.마디수`와 `설정.문서.(제목|이름)/설명`을 docs-first로 먼저 확정한다.
3. compat input + lint warning `SETTINGS_FLAT_KEY_COMPAT`를 도입할지 결정한다.
4. UI 템플릿과 lesson generator 출력만 먼저 canonical 하위 절로 바꾼다.
5. 기존 lesson/pack은 별도 migration 브리프로 처리한다.
6. 마지막에 flat key hard-cut 여부를 결정한다.

## 명시적 비범위

- SSOT 본문 직접 수정 없음.
- parser/runtime hard-cut 없음.
- `state_hash` 산식 변경 없음.
- `InputSnapshot.ai_injections`, `SeulgiPacket`, `SeulgiIntent`, `state_hash` 이름 변경 없음.
- fixed base pack 재설계 없음.

## 사용자 결정 필요

| 결정 | 권고 | 대안 |
|---|---|---|
| `제목` canonical 여부 | `설정.문서.제목` canonical, `이름` compat | `설정.문서.이름` canonical, `제목` compat |
| flat key 처리 | compat input + `SETTINGS_FLAT_KEY_COMPAT` lint | 즉시 비허용 |
| `마디수` 소속 | `설정.실행.마디수` | tool-only CLI/UI metadata로 유지 |
| 기존 lesson migration 시점 | UI 생성기 먼저, 기존 lesson은 별도 배치 | 전수 migration 일괄 수행 |

