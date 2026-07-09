# BRIEF: Q27 재감사 보고서 정정 — 정적분석 대신 실제 실행으로 111건 전수 재확인

작성: 2026-07-09 KST
근거: `docs/context/reports/Q27_DELETION_REAUDIT_V1_20260709.md`(Codex 작성)에서 Claude가 직접 코드를 추적해 확인한 오류.

## 배경 — 발견된 구체적 오류

`Q27_DELETION_REAUDIT_V1_20260709.md`의 "실수삭제" 목록 중 다음 항목들은 "누락 .md 상수는 선언됐지만 실제 존재/읽기 검사 경로에 쓰이지 않음 -> 검사 없음"으로 분류되어 있다:

- `tests/run_lang_blocked_ssot_track_parking_rebase_check.py`
- `tests/run_lang_flow_history_ssot_acceptance_request_check.py`
- `tests/run_lang_non_ssot_track_resume_rebase_check.py`
- `tests/run_lang_pack_checker_stability_sweep_check.py`
- `tests/run_lang_post_ssot_landing_product_gate_rebase_check.py`
- `tests/run_lang_prime_ssot_acceptance_request_check.py`
- `tests/run_lang_product_path_transition_closure_rebase_check.py`
- `tests/run_lang_ssot_acceptance_request_closure_rebase_check.py`
- `tests/run_lang_ssot_landing_coordination_rebase_check.py`
- `tests/run_lang_ssot_landing_wait_state_rebase_check.py`
- `tests/run_lang_ssot_owner_landing_audit_rebase_check.py`
- `tests/run_lang_ssot_owner_landing_handoff_check.py`
- `tests/run_lang_tuck_ssot_acceptance_handoff_check.py`
- `tests/run_lang_tuck_ssot_acceptance_request_check.py`
- `tests/run_roadmap_v2_ga5_release_gate_blocker_audit.py`

Claude가 `git show 2e6a956^:<경로>`로 직접 소스를 열어 확인한 결과, **이 15건 전부**에서:
1. `DOC = ROOT / "<...>V1.md"` 선언이 있고,
2. `check_required_files()`(또는 `check_files()`) 함수 안에 `DOC`가 `require(path)` 반복문 대상 목록에 실제로 포함되어 있으며,
3. `main()`이 `check_required_files()`(또는 `check_files()`)를 실제로 호출한다.

즉 이 15건은 "검사 없음"이 아니라 **실제로 `require()`가 missing DOC에서 FAIL한다** — `정말죽음`으로 재분류되어야 한다. 예시(가장 명확한 사례): `tests/run_lang_blocked_ssot_track_parking_rebase_check.py:11,99-111,294` (`DOC`가 `check_required_files()` 목록 line 101에 있고, `main()` line 294가 그 함수를 호출).

## 원인 추정

이전 재감사는 **정적 코드 추적**(문자열 검색/함수 인용 추적)으로 111건을 분류했는데, "DOC가 리스트 리터럴 안에 들어가고 범용 `require(path)` 반복문으로 검사되는" 패턴을 추적 스크립트가 놓친 것으로 보인다. `require_file(DOC)`처럼 DOC를 직접 인자로 쓰는 패턴만 잡고, 리스트+반복문 패턴은 못 잡았을 가능성이 크다.

이 오류가 15건에서만 나타나는지, 나머지 70건("실수삭제" 85건 중 15건 제외)에도 같은 종류의 정적분석 맹점이 더 있는지 확인되지 않았다.

## 작업 — 정적분석 대신 실제 실행으로 전수 재확인

**111건 전부**(기존 26건 "정말죽음" + 85건 "실수삭제" 포함)를 아래 절차로 다시 확인한다. 이번엔 코드 추적이 아니라 **실제 실행 결과**만 근거로 삼는다.

1. `git show 2e6a956^:<경로>`로 삭제 직전 소스를 `work/_tmp_q27_reaudit_v2/<파일명>`에 복원한다.
2. 그 파일을 저장소 루트에서 직접 실행한다(`python work/_tmp_q27_reaudit_v2/<파일명>` 또는 필요하면 임시로 `tests/` 안에 복사해 실행 후 즉시 제거 — 원래 상대경로 의존성이 있으면 `tests/` 안 임시 파일로 실행해야 할 수 있다).
3. 실행 결과가 실제로 PASS인지 FAIL인지, FAIL이면 정확히 어떤 이유(missing path 등)로 FAIL하는지 기록한다.
4. 실행 결과 기준으로만 재분류한다:
   - 실행 결과 FAIL(어떤 이유든 실제로 실패) → `정말죽음`.
   - 실행 결과 PASS → `실수삭제`.
   - 실행 자체가 안 되는 경우(import 오류, 상대경로 문제 등 환경 이슈) → `실행불가` + 원인 기록, 판단 보류.
5. 실행 후 임시 파일/디렉터리(`work/_tmp_q27_reaudit_v2`, 또는 `tests/` 안에 둔 임시 사본)를 반드시 제거한다.
6. 기존 `Q27_DELETION_REAUDIT_V1_20260709.md`는 수정하지 말고, 새 문서로 정정판을 만든다.

## 산출물

`docs/context/reports/Q27_DELETION_REAUDIT_V2_EXECUTION_BASED_20260709.md` — 111행, 컬럼: 파일명 / 실행결과(PASS/FAIL/실행불가) / FAIL 이유 excerpt / 최종분류(정말죽음/실수삭제/실행불가) / 기존 v1 보고서 분류와의 일치여부(일치/불일치).

## 공통 경계 (절대 준수)

1. 이미 삭제된 파일을 저장소에 다시 커밋하지 않는다 — 임시 실행/삭제만.
2. `docs/ssot/**` 수정 금지.
3. `main` 직접 커밋 금지 — `codex/queue-20260706`에만.
4. push 금지, 네트워크 금지.
5. 111건 전부 실행 기반으로 재확인해야 한다 — 표본만으로 끝내지 않는다(이전 실수가 정적분석의 맹점이었으므로, 이번엔 표본이 아니라 전수 실행이 유일한 신뢰 가능 방법이다).

## Verification

- 111행 전부 실행결과 기록.
- v1 보고서와 불일치하는 행이 몇 개인지, 어느 방향(v1이 정말죽음→FAIL 확인 / v1이 실수삭제→PASS 확인 / 반대 방향 등)인지 요약.
- 실행불가로 남은 행이 있으면 개수와 이유.
- 임시 파일/디렉터리 잔여 0건 확인(`git status --short` 클린).

## DoD

- 실행 기반 재감사 보고서 1건, 111건 전수.
- v1 대비 불일치 요약(특히 이번에 발견된 15건이 정말죽음으로 정정되는지 확인).
- 임시 실행 흔적 완전 제거.
