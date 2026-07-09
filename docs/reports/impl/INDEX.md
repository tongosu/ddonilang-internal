# 구현 보고서(Report) — impl 인덱스

> 위치: `docs/reports/impl/`
>
> 규약(권장): `REPORT_YYYYMMDD_HHMM_WNN.md` / 내용: generated_at, scope, commands, results, notes

## 목록 (2026-04-12)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-04-12 23:59 | [REPORT_20260412_2359_STUDIO_METRICS_TEMPLATE.md](./REPORT_20260412_2359_STUDIO_METRICS_TEMPLATE.md) | 작업실 DDN 편집-실행 v1 계측 이벤트/주간 리포트 템플릿 | 정리 | studio metric event schema + funnel/KPI formula |

## 목록 (2026-07-09)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-07-09 | [DECLARATIVE_CLOSURE_G1_G3_IMPLEMENTATION_GAP_V1_20260709.md](./DECLARATIVE_CLOSURE_G1_G3_IMPLEMENTATION_GAP_V1_20260709.md) | 선언형 closure G1~G3 SolvePlan/세움 tick/prime S2 런타임 갭 | 부분 | `docs/context/proposals/PROPOSAL_DECLARATIVE_CLOSURE_11AXIS_SSOT_PATCH_V1_20260709.md` |

## 목록 (2026-03-03)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-03-03 | [REPORT_20260303_2120_AGE5_EXEC_POLICY_SELFTEST_HARDENING.md](./REPORT_20260303_2120_AGE5_EXEC_POLICY_SELFTEST_HARDENING.md) | AGE5 실행정책 selftest 의미 계약(직교 축/엄밀 강제/게이트 오류 수렴) 강화 | PASS | `python tests/run_pack_golden_exec_policy_selftest.py` |
| - | 2026-03-03 | [REPORT_20260303_2124_AGE5_EVENT_JJAIM_SELFTEST_HARDENING.md](./REPORT_20260303_2124_AGE5_EVENT_JJAIM_SELFTEST_HARDENING.md) | AGE5 event/jjaim selftest 의미 계약(하드컷/IR 스키마/flatten 참조 일관성) 강화 | PASS | event/jjaim selftest + age5 close/aggregate PASS |
| - | 2026-03-03 | [REPORT_20260303_2128_AGE5_WASM_CLI_PARITY_GATE_HARDENING.md](./REPORT_20260303_2128_AGE5_WASM_CLI_PARITY_GATE_HARDENING.md) | AGE5 wasm/cli parity를 overlay/session diag parity + wired consistency까지 승격 | PASS | wasm-cli parity + age5 close + age5 aggregate diagnostics PASS |

## 목록 (2026-04-04)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-04-04 23:50 | [REPORT_20260404_2350_SSOT_V23_IMPLEMENTATION_MATRIX.md](./REPORT_20260404_2350_SSOT_V23_IMPLEMENTATION_MATRIX.md) | SSOT v23.0.4 구현 항목을 완료/진행/미착수로 매핑하고 다음 실행 순서를 고정 | 정리 | SSOT v23.0.4 + DEV_SUMMARY/PROJECT_STATUS 교차 매핑 |

## 목록 (2026-04-05)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-04-05 | [../migration/REPORT_DDN_CANON_MIGRATION_FINAL_V1.md](../migration/REPORT_DDN_CANON_MIGRATION_FINAL_V1.md) | DDN Canonical Migration Program V1 통합 결과(Inventory/Rules/Pack/Solutions/Walks/Checker) | PASS | active 1314 scan, rewrite 2, legacy marker 0(after) |


## 목록 (2026-02-07)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-02-07 | [REPORT_20260207_1255_SEAMGRIM_BOGAE_REFERENCE.md](./REPORT_20260207_1255_SEAMGRIM_BOGAE_REFERENCE.md) | 셈그림 보개 상세/DDN 작성 가이드 | 정리 | (본문) |

## 목록 (2026-02-21)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-02-21 | [REPORT_20260221_0430_AGE3_OI_CLOSE_EVIDENCE.md](./REPORT_20260221_0430_AGE3_OI_CLOSE_EVIDENCE.md) | AGE3 close + OI-405/OI-406 close 증거 묶음 | PASS | commit `fc7ad85` + build/reports/aggnext55full.* |
| - | 2026-02-21 | [REPORT_20260221_1803_SEAMGRIM_LESSON_SCHEMA_REALIGN.md](./REPORT_20260221_1803_SEAMGRIM_LESSON_SCHEMA_REALIGN.md) | 셈그림 교과 DDN 스키마 정렬(보임/= 제거, 전수 canon 검증) | PASS | `build/reports/seamgrim_lesson_realign_*` + canon 전수 `checked=525 failed=0` |
| - | 2026-02-21 | [REPORT_20260221_2340_ECO_DIAG_CONVERGENCE_V0.md](./REPORT_20260221_2340_ECO_DIAG_CONVERGENCE_V0.md) | `#진단` 런타임/리포트 + eco 진단 스모크 pack | PASS | `python tests/run_pack_golden.py eco_diag_convergence_smoke` |
| - | 2026-02-21 | [REPORT_20260221_2358_ECO_CLI_EXPANSION.md](./REPORT_20260221_2358_ECO_CLI_EXPANSION.md) | `eco network-flow`/`eco abm-spatial` CLI 추가 + eco pack 확장 | PASS | `cargo test eco_` + `python tests/run_pack_golden.py eco_*` |

## 목록 (2026-02-23)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-02-23 | [REPORT_20260223_2355_SEAMGRIM_UI_REBUILD_DELETE_CONFLICTS.md](./REPORT_20260223_2355_SEAMGRIM_UI_REBUILD_DELETE_CONFLICTS.md) | UI 재건 TASK §1 삭제 목록 vs 현재 게이트 의존 충돌 점검 | 부분충돌 정리 | `rg` 경로 점검 + `Test-Path` |
| - | 2026-02-23 | [REPORT_20260223_2359_SEAMGRIM_OVERLAY_CONTRACT_RETIRE_PHASE1.md](./REPORT_20260223_2359_SEAMGRIM_OVERLAY_CONTRACT_RETIRE_PHASE1.md) | overlay/session 계약 UI 직접 의존 제거 1단계 + 테스트 경로 이관 | PASS | overlay selftest + ci gate + aggregate gate |

## 목록 (2026-02-18)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-02-18 | [REPORT_20260218_1605_AGE2_STUDIO_GATE_CHECKLIST.md](./REPORT_20260218_1605_AGE2_STUDIO_GATE_CHECKLIST.md) | AGE2 Studio 완료 게이트 5개 실행 점검 | PASS (G1~G5) | (본문 커맨드 로그) |

## 목록 (2026-02-01)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-02-01 | [REPORT_20260201_2240_SEAMGRIM_UI_LAYER_TIMELINE_SCENE.md](./REPORT_20260201_2240_SEAMGRIM_UI_LAYER_TIMELINE_SCENE.md) | 셈그림 UI: 레이어/타임라인/씬 + 계약 주체 논의 | 정리 | (본문) |

## 목록 (2026-02-04)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-02-04 | [REPORT_20260204_1200_SSOT_PACK_AUDIT.md](./REPORT_20260204_1200_SSOT_PACK_AUDIT.md) | SSOT pack 현황 점검(placeholder/표 자산 누락) | 정리 | (본문) |
| - | 2026-02-04 | [REPORT_20260204_1610_SEAMGRIM_UI_SUMMARY.md](./REPORT_20260204_1610_SEAMGRIM_UI_SUMMARY.md) | 셈그림 UI/교과/런타임 전체 요약 | 정리 | (본문) |

## 목록 (2026-02-06)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-02-06 | [REPORT_20260206_1035_SSOT_PACK_EDU_MIRROR.md](./REPORT_20260206_1035_SSOT_PACK_EDU_MIRROR.md) | SSOT edu pack 미러링 + JSON 기대값 검증 | 정리 | (본문) |
| - | 2026-02-06 | [REPORT_20260206_1125_SEAMGRIM_SCENE_SESSION_VALIDATE.md](./REPORT_20260206_1125_SEAMGRIM_SCENE_SESSION_VALIDATE.md) | seamgrim scene/session JSON 최소 검증 러너 | 정리 | (본문) |
| - | 2026-02-06 | [REPORT_20260206_1205_SEAMGRIM_SCENE_SESSION_CHECKER.md](./REPORT_20260206_1205_SEAMGRIM_SCENE_SESSION_CHECKER.md) | seamgrim scene/session JSON 구조 검증 러너 | 정리 | (본문) |
| - | 2026-02-06 | [REPORT_20260206_1210_SSOT_EDU_AUTO_MIRROR.md](./REPORT_20260206_1210_SSOT_EDU_AUTO_MIRROR.md) | SSOT edu lesson 자동 미러 스크립트 | 정리 | (본문) |
| - | 2026-02-06 | [REPORT_20260206_1235_SSOT_EDU_DIFF.md](./REPORT_20260206_1235_SSOT_EDU_DIFF.md) | SSOT edu ↔ pack 미러 차분 리포트 | 정리 | (본문) |
| - | 2026-02-06 | [REPORT_20260206_1245_SEAMGRIM_FULL_CHECK.md](./REPORT_20260206_1245_SEAMGRIM_FULL_CHECK.md) | seamgrim graph+scene/session 통합 체크 | 정리 | (본문) |

## 목록 (2026-01-31)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-01-31 | [REPORT_20260131_1149_SEAMGRIM_UI_MVP.md](./REPORT_20260131_1149_SEAMGRIM_UI_MVP.md) | 셈그림(Seamgrim) UI MVP / stdlib 범위 / 브리지 점검 | 정리 | (본문) |

## 목록 (2026-01-24)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| - | 2026-01-24 | [STDLIB_ALIGN_PR3_REPORT.md](./STDLIB_ALIGN_PR3_REPORT.md) | stdlib 기본 pack 4종 | DONE | (없음) |

## 목록 (2026-01-15 ~ 2026-01-16)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| 16 | 2026-01-15 | [REPORT_20260115_1932_W16.md](./REPORT_20260115_1932_W16.md) | Text/Sprite drawlist + web skin(symbol swap/asset copy) | PASS | (보고서 본문) |
| 17 | 2026-01-15 | [REPORT_20260115_2024_W17.md](./REPORT_20260115_2024_W17.md) | 샘/키보드 입력 기록·재생(--record-sam/--sam) | PASS | state_hash(본문) |
| 14-17 | 2026-01-16 | [REPORT_20260116_0008_W14_W17.md](./REPORT_20260116_0008_W14_W17.md) | W14~W17 정합화/골든 묶음 실행 메모(※ 인코딩 깨짐 포함) | 참고 | (없음) |
| 18-21 | 2026-01-16 | [REPORT_20260116_0143_W18_W21.md](./REPORT_20260116_0143_W18_W21.md) | W18..W21 golden tests PASS 요약 | PASS | (없음) |

## 목록 (2026-01-17)

| W | generated_at | 파일 | scope | 결과 | 증거(해시) |
|---:|---|---|---|---|---|
| 47 | 2026-01-17 | [REPORT_20260117_0322_W47.md](./REPORT_20260117_0322_W47.md) | W47 live sam input(console/web) + viewer input forwarding | PASS | (없음) |
| 48 | 2026-01-17 | [REPORT_20260117_1048_W48.md](./REPORT_20260117_1048_W48.md) | Tetris Slice0 input skeleton(state model + key mapping) | PASS | (없음) |
| 49 | 2026-01-17 | [REPORT_20260117_1210_W49.md](./REPORT_20260117_1210_W49.md) | teul-cli 일때/아니면 조건 분기 지원 | PASS | (보고서 본문 참조) |
| 50 | 2026-01-17 | [REPORT_20260117_1255_W50.md](./REPORT_20260117_1255_W50.md) | teul-cli 고르기 분기 + Slice0 입력 갱신 | PASS | (없음) |
| 51 | 2026-01-17 | [REPORT_20260117_1410_W51.md](./REPORT_20260117_1410_W51.md) | 고르기 `{...}인것` 정합화 + canon 분기 + Slice0 낙하 추가 | PASS | (없음) |
| 52 | 2026-01-17 | [REPORT_20260117_1505_W52.md](./REPORT_20260117_1505_W52.md) | Slice0 보드 충돌/라인삭제 스켈레톤 + }아닌것 예제 | PASS | (없음) |
| 53 | 2026-01-17 | [REPORT_20260117_1245_W53.md](./REPORT_20260117_1245_W53.md) | Slice0 보드 렌더링 + 라인 삭제 점수/연출 | PASS | state/trace/bogae (본문) |
| 54 | 2026-01-17 | [REPORT_20260117_1408_W54.md](./REPORT_20260117_1408_W54.md) | Slice0 4블록 렌더링 + 이동/회전 개선 + 게임오버 | PASS | state/trace/bogae (본문) |
| 55 | 2026-01-17 | [REPORT_20260117_1611_W55.md](./REPORT_20260117_1611_W55.md) | sam-live 콘솔 종료 키 처리 + 콘솔 스프라이트 문자 매핑 | PASS | (없음) |
| 56 | 2026-01-17 | [REPORT_20260117_1622_W56.md](./REPORT_20260117_1622_W56.md) | web/playback viewer 스프라이트 알파 0 렌더링 스킵 | PASS | (없음) |
| 57 | 2026-01-17 | [REPORT_20260117_1632_W57.md](./REPORT_20260117_1632_W57.md) | Slice0 보개 캔버스 높이 조정(하단 줄 표시) | PASS(부분 FAIL) | bogae_hash (본문) |

## 운영 메모(정합성/재현성)


- **W14~W17 보고서**: 일부 줄이 `??`로 표시되는 인코딩 깨짐이 있음(원본 복구 전까지 참고용).
- **W50**: 샘 테이프 길이(600)와 `--madi` ticks 불일치로 1회 실패 후 재실행 기록이 있음.
  - 권장(TOOLING): `--madi` < sam_ticks 인 경우 경고 또는 즉시 실패(+친절한 안내).
- **W54**: 이번 보고서는 **100회 반복 검증 미수행**.
  - 권장(D-PACK/CI): 변경 폭이 큰 구간에서는 `repeat=100` 같은 리그레션 가드를 주기적으로 수행.
- **W57**: `샘.키보드.*`를 쓰는 실행은 **`--sam` 또는 `--sam-live`가 반드시 필요**함.
  - `--sam`을 쓸 때는 `--madi` ticks와 sam `record_count`가 일치해야 함(불일치 시 E_SAM_RECORD_COUNT_MISMATCH).
