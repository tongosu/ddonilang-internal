# SESSION_DELTA

- 작성일: 2026-07-06
- 작성 주체: Codex
- 세션명: settings_header_baseline
- 관련 SSOT: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md`

## 결정된 것

| 상태 | 관련 모듈 | 내용 | 근거/파일 |
|---|---|---|---|
| Reflected | 설정 헤더 pack | `lang_settings_header_closure_v1`의 c02는 `보임 {}` 차단이 아니라 structured view surface 수용을 고정한다. | `pack/lang_settings_header_closure_v1/golden.jsonl`, `README.md` |
| Reflected | 보임 surface | `보임 {}`는 SSOT의 정식 structured view sugar 입력 surface로 유지한다. `E_CANON_LEGACY_BOIM_FORBIDDEN` 기대는 stale로 정리한다. | `docs/ssot/ssot/SSOT_LANG_v24.12.9.md`, `docs/status/LANG_STATUS.md` |

## 확인이 필요한 것

| 질문 | 관련 모듈 | 필요 근거 | 확인 담당 | 상태 |
|---|---|---|---|---|
| 과거 status/changelog의 historical 기록까지 재작성할지 여부 | 문서 정리 | 사용자 요청 | 사용자 | Open |

## 다음 세션에 이어받을 것

- `보임 {}` 전체 금지 또는 루트-only 금지는 이번 기준선에서 채택하지 않는다.
- 향후 설정 헤더 수리에서는 `설정 {}` file-leading 처리와 `보임 {}` structured view sugar를 분리해서 본다.

## 생성/수정 파일

| 파일 | 목적 | 후속 처리 |
|---|---|---|
| `pack/lang_settings_header_closure_v1/golden.jsonl` | c02 golden을 현재 제품 canon 성공 출력으로 정정 | 유지 |
| `pack/lang_settings_header_closure_v1/contract.detjson` | c02 case id 정정 | 유지 |
| `pack/lang_settings_header_closure_v1/README.md` | historical filename과 현재 의미 명시 | 유지 |
| `tests/run_lang_settings_header_closure_pack_check.py` | c02 의미 drift 회귀 방지 | 유지 |
| `docs/status/LANG_STATUS.md` | stale current claim 정정 | 유지 |
| `docs/context/all/DEV_SUMMARY.md` | Q37 기록 | 유지 |

## 검증

| 명령/확인 | 결과 | 비고 |
|---|---|---|
| `cargo run --quiet --manifest-path tools/teul-cli/Cargo.toml -- canon pack/lang_settings_header_closure_v1/legacy_boim.ddn` | PASS | `보임 { ... }.` 성공 출력 확인 |
| `python tests/run_lang_settings_header_closure_pack_check.py` | PASS | Q37 checker |
| `python tests/run_pack_golden.py lang_settings_header_closure_v1` | PASS | pack golden |
| `cargo test -p ddonirang-lang validate_no_legacy_boim_surface_accepts_boim_block -- --nocapture` | PASS | lang frontdoor |
| `cargo test --manifest-path tools/teul-cli/Cargo.toml canon_accepts_boim_surface_on_frontdoor -- --nocapture` | PASS | teul-cli canon |
| `python tests/run_ci_sanity_gate.py --profile core_lang` | PASS | core_lang |

## SSOT 병합 메모

- SSOT 본문은 이미 `보임 {}` structured view sugar를 정식 입력 surface로 둔다.
- 이번 작업은 SSOT 변경이 아니라 stale pack/docs 기대값 정합이다.
