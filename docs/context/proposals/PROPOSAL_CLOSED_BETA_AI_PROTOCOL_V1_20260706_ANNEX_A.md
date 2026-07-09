# PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706 — ANNEX A (T4 베타 오류 fixture 명세, 구현 등급 정교화)

- 작성: 2026-07-09 KST, Claude Code (지시문 16 이행)
- 원 제안서: `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706.md` (T4 과제 대상)
- 기존 산출물 확인: `work/beta/round0/BETA_USER_BUNDLE/fixtures/T4/`에 3개 fixture(`syntax_bad_identifier.ddn`, `type_bad_iterable.ddn`, `contract_bad_mode.ddn`)와 `expected_diagnostics.md`가 **이미 존재**한다. Codex가 지시문 15 Tier A 항목 7에서 "지시문 16-5 명세를 따름"이라고 밝혔으나, 이 ANNEX가 그보다 늦게 작성되어 순서가 뒤바뀌었다 — 이 문서는 기존 fixture를 **사후 검증 + 정식 명세로 승격**하는 역할을 한다.

**본 문서는 구현 등급 설계이며 SSOT 병합 전 canon 아님.**

## 사전 검증 결과 (신규)

3개 fixture를 `cargo run -- check`/`run`으로 직접 실행해 `expected_diagnostics.md`와 대조했다.

| 파일 | 실행 결과 | expected_diagnostics.md와 일치 |
|---|---|---|
| `syntax_bad_identifier.ddn` | `E_LEX_UNEXPECTED_CHAR ...:1:3 예상치 못한 문자: ?` | 일치 |
| `type_bad_iterable.ddn` | `E_RUNTIME_TYPE_MISMATCH ...:2:6 타입 불일치: iterable list/set/map` | 일치 |
| `contract_bad_mode.ddn` | `E_PARSE_UNEXPECTED_TOKEN ...:3:21 예상: '알림' or '물림' or '중단'` | 일치 |

세 fixture 모두 실제 동작과 문서가 정확히 일치함을 확인했다 — 이 ANNEX는 새 fixture를 만들지 않고, 기존 것을 정식 스키마로 승격한다.

## (a) 정확한 스키마 표

### `expected_diagnostics.md`의 암묵 스키마를 명시화 (`ddn.beta_error_fixture.v1` 후보)

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| `fixture_file` | string | 필수 | - | 대상 `.ddn` 경로 |
| `error_category` | enum(`문법`,`타입`,`계약`) | 필수 | - | T4 과제가 요구한 3종 분류(원 제안서 T4: "문법/타입/계약 오류 각 1") |
| `command` | enum(`check`,`run`) | 필수 | - | 재현 커맨드 |
| `expected_exit_nonzero` | bool | 필수 | `true` | 세 케이스 모두 실패를 기대 |
| `expected_error_code` | string | 필수 | - | `E_*` 코드, 정확히 1개 |
| `expected_message_fragment` | string | 필수 | - | 진단 메시지 부분 문자열(전체 일치 아님 — 문구가 다듬어져도 fixture가 안 깨지게) |
| `expected_line_col` | string | 선택 | - | `줄:칸` — 있으면 위치 정확도까지 검증 |
| `friction_axis` | enum(`fix_it_present`,`fix_it_absent`) | 필수 | - | 진단이 "무엇을 고쳐야 하는지"까지 알려주는지 여부(베타 friction log의 4등급과 연동) |

## (b) 엣지케이스 표

| # | 케이스 | 기대 동작 | 근거 |
|---|---|---|---|
| E1 | 베타 사용자가 `run` 대신 `check`로 `type_bad_iterable.ddn`을 실행 | `check`는 정적 분석만 하므로 타입 오류가 실행 시점에만 드러나면 `check`는 통과할 수 있다 — 이 경우 사용자가 "왜 check는 통과했는데 run은 실패하지?"를 겪는 것 자체가 friction log 대상(문서 gap 후보) | 실측: `check`/`run` 분리가 초심자에게 안 알려져 있으면 그 자체가 T4의 발견 대상 |
| E2 | 사용자가 fixture 파일을 고쳐서 재실행 → 진단이 사라지고 정상 실행됨 | fixture는 "정확히 1개 오류만" 심어야 한다 — 고치면 나머지 코드가 정상 실행되는지까지가 fixture 품질 기준(현재 3개 파일 모두 이 조건 충족, 표본 실행으로 확인) | T4 과제 목적("무엇을 고쳐야 할지 설명할 수 있는가") |
| E3 | `expected_message_fragment`가 향후 진단 문구 개선(P4-G1 진단 3층 감사 후속)으로 바뀜 | fixture golden은 `error_code`는 고정, `message_fragment`는 완화 매칭(부분 문자열)이므로 문구가 더 좋아지는 방향의 변경에는 안 깨짐 — 단, `error_code` 자체가 바뀌면 fixture가 실패해야 함(의도된 breaking) | (a) 스키마의 "부분 문자열" 설계 이유 |
| E4 | 세 번째 오류 종류(`계약`)의 `contract_bad_mode.ddn`이 실제로는 파서 단계에서 잡힘(`E_PARSE_UNEXPECTED_TOKEN`) — "계약 오류"라는 이름과 달리 실제 오류 카테고리는 "문법"에 가까움 | 이름(`error_category=계약`)과 실제 코드 카테고리(파서)가 다른 것은 **의도된 것** — "계약 블록 안에 잘못된 모드를 쓰면 파서가 먼저 잡는다"는 것 자체가 유용한 발견(계약 모드 오타는 런타임까지 안 가고 조기에 걸린다는 뜻) | 실측 결과 그대로 반영, 왜곡하지 않음 |

## (c) 오류 코드 배정 확인 (신규 배정 없음)

기존 3개 코드(`E_LEX_UNEXPECTED_CHAR`, `E_RUNTIME_TYPE_MISMATCH`, `E_PARSE_UNEXPECTED_TOKEN`)가 실제 코드베이스에 존재함을 `tools/teul-cli/src/{runtime/error.rs, lang/parser.rs, lang/lexer.rs}`에서 확인했다. 신규 코드 배정 불필요 — 이 항목은 기존 진단을 fixture로 고정하는 것이 전부다.

## (d) pack DoD + golden fixture 스케치

기존 fixture 3개를 그대로 pack 후보로 승격한다.

- pack 후보: `beta_t4_error_fixture_v1` (신규 — `work/beta/round0/BETA_USER_BUNDLE/fixtures/T4/`의 3개 파일을 golden pack 형태로 재포장).
- golden fixture: 이미 존재하는 3개 케이스(`syntax_bad_identifier`, `type_bad_iterable`, `contract_bad_mode`) 그대로 사용. 추가 케이스 불필요 — T4 과제 요구사항("문법/타입/계약 각 1")을 정확히 충족.
- DoD: 3케이스 각각 `expected_error_code` + `expected_message_fragment` PASS(이미 이 ANNEX에서 실측 확인 완료). pack화는 이 fixture 세트를 `tests/run_*_check.py` 표준 러너 형식으로 감싸기만 하면 되는 저비용 작업.

## (e) 남은 결정 질문 (≤3)

1. **베타 friction log와의 연동 형식**: `friction_axis` 필드(E1에서 제안)를 실제 friction log 스키마(`FRICTION_LOG_TEMPLATE.detjson`)와 어떻게 연결할지 — 지시문 14 Round 0 실제 실행 시 결정.
2. **E4에서 발견한 "계약 오류가 실제로는 파서 단계"라는 사실을 T4 과제 설명 문구에 반영할지**: 현재 `expected_diagnostics.md`는 이 사실을 설명하지 않는다. 베타 사용자가 오해하지 않도록 "계약 모드 오타는 파서가 먼저 잡습니다"라는 각주를 추가할지.
3. **pack화 필요성**: 지금 상태(3개 `.ddn` + 1개 `.md`)로도 베타 실행에는 충분하다 — 정식 `pack/beta_t4_error_fixture_v1/`로 승격하는 것이 CI 회귀 감시 목적으로 필요한지, 아니면 베타 전용이라 pack화가 과잉인지.
