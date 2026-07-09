# PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706 — ANNEX A (보개마당 트랙 v1, 구현 등급 정교화)

- 작성: 2026-07-09 KST, Claude Code (지시문 16 이행)
- 원 제안서: `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706.md` §3 P2-G2(보개마당 트랙 v1)
- 판정 대상: `seamgrim.scene.v0`와의 관계(확장인가 병렬인가)

**본 문서는 구현 등급 설계이며 SSOT 병합 전 canon 아님.**

## 핵심 발견 — `seamgrim.scene.v0`는 이미 트랙 3종의 절반 이상을 구현하고 있다

`tests/run_seamgrim_scene_session_check.py`와 실제 fixture(`docs/ssot/pack/edu/pilot_phys_econ/lesson_econ_01/expected.scene.v0.json`, `.../lesson_phys_01/expected.scene.v0.json`)를 직접 열어 확인한 결과:

| 원 제안서 트랙 | `seamgrim.scene.v0`의 대응물 | 실측 근거 |
|---|---|---|
| 자막 | `target.type = "#자막"`, `verb: "나타나기"` | `lesson_econ_01/expected.scene.v0.json` — `{"args":{"글":"소득(income)을 바꾸면..."},"target":{"type":"#자막","view":"text"},"verb":"나타나기"}` |
| 해설 | `target.type = "#해설"` | `lesson_phys_01/expected.scene.v0.json:73` |
| 강조 | `verb: "강조하기"`(하이라이트 대상은 `target`으로 표현) | `lesson_phys_01/expected.scene.v0.json:76` |

또한 스키마는 이미 **마디(tick) 기준 구간**을 쓴다(`sections[].tick_from/tick_to`, `id`) — 원 제안서가 "타임라인 키는 마디 번호 기준"이라 요구한 것과 정확히 같은 구조다.

**판정: 확장(병렬 아님).** `seamgrim.scene.v0`는 새 스키마를 만들 필요 없이 이미 자막/해설/강조 3종을 `target.type`/`verb` 조합으로 표현하고 있다. 남은 일은 이 ad-hoc 관례를 **정식 계약으로 고정**(허용 `target.type`/`verb` 값의 닫힌 목록화, 검증 강화)하는 것이다.

## (a) 정확한 스키마 표

### 보개마당 트랙 계약 v1 (기존 `seamgrim.scene.v0`의 부분 집합을 명시화)

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| `sections[].id` | string | 필수 | - | 기존 필드, 변경 없음 |
| `sections[].tick_from` / `tick_to` | int | 필수 | - | 기존 필드, 변경 없음. **마디 번호 기준 = 이미 충족** |
| `sections[].commands[].target.type` | enum(`#제목`,`#자막`,`#해설`,`#강조`) | 필수 | - | **신규: 이 4개로 닫힌 목록 고정**(현재는 자유 문자열 — 검증 스크립트가 값을 제한하지 않음, 아래 엣지케이스 E1 참조) |
| `sections[].commands[].target.ref` | string | `#강조`일 때 필수, 그 외 선택 | - | 하이라이트 대상 참조(원 제안서 "하이라이트 대상 ref"). 현재 fixture는 `args.토큰`으로 유사 표현 중 — **명칭 통일 필요**(아래 (e) 질문 1) |
| `sections[].commands[].verb` | enum(`나타나기`,`사라지기`,`강조하기`) | 필수 | - | 기존 값 그대로, `강조하기`가 이미 존재 확인 |
| `sections[].commands[].args.글` | string | `#자막`/`#해설`일 때 필수 | - | 기존 필드, 변경 없음 |

## (b) 엣지케이스 표

| # | 케이스 | 기대 동작 | 근거 |
|---|---|---|---|
| E1 | `target.type`에 `#제목/#자막/#해설/#강조` 외의 값(예: `#배경음`)이 들어옴 | 현재 `validate_scene()`은 `target.type` 값 자체를 검증하지 않는다(자유 문자열 허용) — 트랙 3종으로 닫으려면 **새 검증 단계 추가 필요**. v1은 미지 `type`을 경고로만 두고 fatal화는 후속(카메라/전환 등 G3 확장 여지를 막지 않기 위함) | 원 제안서 "트랙 3종만... 카메라/전환은 G3"과 정합 — 지금 fatal로 잠그면 G3 확장이 스키마 변경을 요구하게 됨 |
| E2 | 같은 구간(`tick_from`~`tick_to`)에 `#자막`과 `#해설`이 동시에 존재 | 허용 — 트랙은 논리적 채널이지 배타적 슬롯이 아니다(자막과 해설이 같은 구간에 동시에 뜨는 것은 정상적인 교육 연출) | `lesson_econ_01` fixture에서 같은 section에 `#제목`과 `#자막` 커맨드가 이미 공존 |
| E3 | `#강조`인데 `verb`가 `강조하기`가 아닌 `나타나기` | 현재 fixture(`lesson_phys_01`)는 `target.type=#해설` + `verb=강조하기` 조합을 쓴다 — 즉 **강조는 target이 아니라 verb로 표현되는 패턴도 실존**. v1 스키마는 이 두 표현(`target.type=#강조` 단독 vs `해설+강조하기` 조합)을 모두 허용할지 하나로 통일할지 결정 필요(아래 (e) 질문 2) | 실측에서 발견한 표현 방식의 이중성 |
| E4 | `tick_from == tick_to`(순간 이벤트) | 허용 — 순간 강조(예: 특정 tick에서 반짝) 표현에 필요 | 기존 스키마가 `tick_from > tick_to`만 금지(`if tick_from > tick_to: fail`), 동일값은 이미 허용됨 |

## (c) 오류 코드 배정안

| 코드 | 배정 근거 |
|---|---|
| `E_SCENE_TRACK_TYPE_UNKNOWN` (신규 후보, 경고 등급) | E1 — v1은 경고, G3 이후 fatal 전환 검토 |
| `E_SCENE_HIGHLIGHT_REF_MISSING` (신규 후보) | `target.type=#강조`인데 `target.ref` 누락 시 |

기존 `tests/run_seamgrim_scene_session_check.py`의 `fail()` 함수가 이미 스키마 검증 실패를 `SystemExit(1)`로 처리하는 패턴을 그대로 확장하면 된다 — 새 검증 로직 추가만 필요, 새 실행 경로 불필요.

## (d) pack DoD + golden fixture 스케치

- pack 후보: `bogae_madang_track_v1_schema_smoke` (원 제안서 §3-G2에 이미 명시된 이름, `PRE_RELEASE_FREEZE_SWEEP_V1.md` 충돌 검사에 없었음 — 신규 확인 필요).
- golden fixture는 **새로 만들 필요 없이 기존 2개 lesson fixture를 재사용**할 수 있다:
  - `lesson_econ_01/expected.scene.v0.json` — `#제목`+`#자막` 조합 검증.
  - `lesson_phys_01/expected.scene.v0.json` — `#해설`+`강조하기` 조합 검증.
  - 추가 케이스 1개만 신규: `c03_unknown_track_type_warning` — 임의의 `target.type` 값을 넣어 E1의 경고 동작 확인.
- DoD: 기존 2개 fixture로 회귀 없음 확인(이미 PASS 중인 검증을 안 깨는지) + 신규 1케이스로 트랙 목록 고정 검증.

## (e) 남은 결정 질문 (≤3)

1. **하이라이트 대상 참조 필드명 통일**: 원 제안서는 "ref"라 부르고, 기존 fixture는 `args.토큰`으로 표현한다. `target.ref`로 통일할지 `args` 안에 유지할지.
2. **강조 표현 방식 통일**: `target.type=#강조` 단독 패턴을 새로 쓸지, 기존 fixture의 `target.type=#해설 + verb=강조하기` 조합 패턴을 정본으로 굳힐지 — 후자면 "트랙 3종"이 아니라 "type 2종(`#자막`/`#해설`) + verb 확장(`강조하기`)"로 재정의될 수 있음.
3. **E1의 미지 `target.type` 처리를 언제 경고에서 fatal로 승격할지**: G3(카메라/전환) 스키마가 확정된 뒤인지, 아니면 v1부터 닫힌 목록으로 갈지.
