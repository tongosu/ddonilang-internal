# 설정.거울 / 설정.실행 T0 정렬 감사 V1

- 작업: Q36-1 / 지시문 1
- 일시: 2026-07-06
- 범위: 상태표, frontdoor 진단/테스트, pack 참조의 3자 대조
- 불변 경계: 코드, pack, SSOT 본문, state_hash 산식 변경 없음

## 결론

`설정.거울 / 설정.실행` 하위 표면은 SSOT 상태표 기준으로 `designed` / `STUB_ONLY`가 맞다. 제품 코드에서 `기록갈래`, `재연갈래`, `살핌내주기갈래`, `뒤살핌`, `보람주인갈래`, `보람때갈래`, `판끝갈래`, `마디틈갈래`, `없음보람`을 런타임 구현으로 소비하는 경로는 발견하지 못했다.

다만 `lang_settings_header_closure_v1` pack의 c02 golden은 현재 frontdoor 동작과 다르다. `golden.jsonl`은 `legacy_boim.ddn`의 canon이 `E_CANON_LEGACY_BOIM_FORBIDDEN`으로 실패해야 한다고 기대하지만, 현재 제품 `teul-cli canon`은 `보임 { x: 1. }.`을 성공적으로 정본 출력한다. 전용 checker는 현재 제품 테스트를 따르기 때문에 PASS한다. 따라서 T0 bundle의 잔여 drift는 "pack golden 기대값과 현재 frontdoor acceptance의 불일치" 1건이다.

## 상태표 대조

| 항목 | 상태표 근거 | 문법 자리 | age_scope | runtime_status | 감사 판정 |
|---|---|---|---|---|---|
| `기록갈래` | `SSOT_LANG_v24.12.9.md:700`, `PROPOSAL_HARDCUT_HASH_HEADERS...:201` | `설정.거울` 후보 | next support bundle candidate | parser/runtime closure 아님 | 과잉 구현 표기 없음 |
| `재연갈래` | `SSOT_LANG_v24.12.9.md:700`, `PROPOSAL_HARDCUT_HASH_HEADERS...:202` | `설정.거울` 후보 | next support bundle candidate | parser/runtime closure 아님 | 과잉 구현 표기 없음 |
| `살핌내주기갈래` | `SSOT_LANG_v24.12.9.md:8063`, `:8074`, `:8091` | `설정.거울` | AGE3~AGE4 | designed / STUB_ONLY | 자리 정렬 맞음 |
| `뒤살핌` | `SSOT_LANG_v24.12.9.md:8091` | `설정.거울` | AGE3~AGE4 | designed / STUB_ONLY | `설정.실행`이 아님 |
| `보람주인갈래` | `SSOT_LANG_v24.12.9.md:8063`, `:8072`, `:8085` | `설정.실행` | AGE3~AGE4 | designed / STUB_ONLY | 과잉 구현 표기 없음 |
| `보람때갈래` | `SSOT_LANG_v24.12.9.md:8063`, `:8073` | `설정.실행` | AGE3~AGE4 | designed / STUB_ONLY | 과잉 구현 표기 없음 |
| `판끝갈래` | `SSOT_LANG_v24.12.9.md:8063` | `설정.실행` | AGE3~AGE4 | designed / STUB_ONLY | 과잉 구현 표기 없음 |
| `마디틈갈래` | `SSOT_LANG_v24.12.9.md:8063`, `:8094` | `설정.실행` | AGE3~AGE4 | designed / STUB_ONLY | 과잉 구현 표기 없음 |

## 교차 절 경로

`설정.실행.차림새`는 `SSOT_LANG_v24.12.9.md:8049-8051`에서 실행 차림새의 유일한 v1 위치로 고정되어 있고, `SSOT_LANG_v24.12.9.md:8063-8069`의 preset 표는 각 차림새가 `살핌내주기갈래 = 뒤살핌`을 채운다고 적는다. 그러나 `SSOT_LANG_v24.12.9.md:8074`는 `살핌내주기갈래`의 문법 자리를 `설정.거울`로 다시 못박는다.

따라서 문서상 경로는 다음처럼 해석해야 한다.

| 단계 | 의미 | 판정 |
|---|---|---|
| `설정.실행.차림새` 선택 | 실행 preset 선택은 `설정.실행`에서 한다 | 정렬됨 |
| preset 표 확장 | preset이 `살핌내주기갈래` 값을 산출한다 | 정렬됨 |
| 산출 키의 소속 | `살핌내주기갈래` 값은 `설정.거울` 슬롯 의미다 | 정렬됨 |
| 런타임 소비 | 현재 제품 런타임은 이 슬롯을 소비하지 않는다 | designed / STUB_ONLY 유지 |

## Frontdoor / Pack 대조

| 증거 | 명령/파일 | 결과 | 판정 |
|---|---|---|---|
| 설정 헤더 제거 | `cargo run --quiet --manifest-path tools/teul-cli/Cargo.toml -- canon pack/lang_settings_header_closure_v1/input.ddn` | `x <- 1.` | 현재 frontdoor 성공 |
| legacy `보임` canon | `cargo run --quiet --manifest-path tools/teul-cli/Cargo.toml -- canon pack/lang_settings_header_closure_v1/legacy_boim.ddn` | `보임 { x: 1. }.` | 현재 frontdoor 성공 |
| 전용 checker | `python tests/run_lang_settings_header_closure_pack_check.py` | PASS | 현재 제품 테스트 기준 통과 |
| pack golden | `python tests/run_pack_golden.py lang_settings_header_closure_v1` | FAIL: c02 expected `E_CANON_LEGACY_BOIM_FORBIDDEN`, got exit 0 | 잔여 drift |

## 코드 구현 검색

실행 코드 검색:

```text
rg -n "기록갈래|재연갈래|살핌내주기갈래|보람주인갈래|보람때갈래|판끝갈래|마디틈갈래|없음보람|뒤살핌" tools/teul-cli/src core/src lang/src tests pack --glob '!**/target/**'
```

제품 코드(`tools/teul-cli/src`, `core/src`, `lang/src`)에는 해당 하위 키를 구현으로 소비하는 행이 없었다. 발견된 행은 `tests/toolchain_golden/ai_prompt_lean.txt`의 문서형 golden과 SSOT/제안 문서성 참조뿐이다.

## 잔여 목록

| drift | 위치 | 내용 | 원인 | 처리 |
|---|---|---|---|---|
| pack golden c02 불일치 | `pack/lang_settings_header_closure_v1/golden.jsonl` | legacy `보임` 금지를 기대 | 현재 제품 frontdoor/canon 테스트는 `보임` surface acceptance를 통과시킴 | Q36에서는 수정 금지. 별도 pack contract 정리 필요 |

## DoD 확인

| DoD | 결과 |
|---|---|
| 상태표-frontdoor-pack 3자 대조 | 완료 |
| drift 0건 또는 잔여 목록 + 원인 | 잔여 drift 1건 기록 |
| `designed/STUB_ONLY` 항목이 implemented로 과잉 표기된 곳 0건 | 제품 코드 구현 검색 기준 0건 |
| state_hash / runtime canonical name / fixed base pack 변경 없음 | 변경 없음 |
| docs-first 표면 parser hard-cut 승격 없음 | 변경 없음 |
