# 발표 전 예약어 선점 감사 V1

작성: 2026-07-08 KST
범위: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md`, `docs/ssot/ssot/SSOT_TERMS_v24.12.9.md`, `tools/teul-cli/src/lang/lexer.rs`, `.ddn` 코드 grep(`pack/`, `tests/`, `gaji/`, `solutions/`).

## 추출 규칙

- SSOT 쪽은 순한글 단일 토큰만 집계했다. 공백 포함 표면(`단위 정의`), 기호 포함 표면(`~분포(...)`, `}하며` 등), ASCII/하이픈 토큰은 제외했다.
- SSOT 포함 근거는 예약어 블록, `reserved_words` 배열, `키워드`/`예약 후보`/`정본 또는 current-line 표면`으로 명시된 줄이다. legacy alias 설명어는 제외했다.
- Lexer 쪽은 `tools/teul-cli/src/lang/lexer.rs`의 `classify_ident`에서 `TokenKind::Ident`가 아닌 토큰으로 분기되는 순한글 문자열만 집계했다.
- 충돌 검색은 SSOT-only 토큰에 대해 `.ddn` 파일의 텍스트 grep을 수행했다. `토큰:`, `토큰 <-`, `토큰 =`, `토큰.` 형태가 보이면 `충돌 위험`으로 표시하고, 단순 등장만 있으면 `grep hit(일반 식별자 패턴 미확인)`로 남겼다.

## 검증 로그

- SSOT 추출 항목 수: 112
- Lexer 추출 항목 수: 33
- 합집합 행 수: 113
- 분류 합계: SSOT-only 80 + lexer-only 1 + 양쪽 일치 32 = 113
- 행 수 검증: PASS

## 대조 표

| SSOT에 있으나 lexer에 없음 | lexer에 있으나 SSOT에 없음 | 양쪽 일치 |
|---|---|---|
| `가설`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| - | - | `감사`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어<br>lexer: tools/teul-cli/src/lang/lexer.rs:666 |
| `값구하기`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5388 정본/current-line 표면<br>미발견 | - | - |
| `값꾸러미`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>충돌 위험: pack/edu_pilot_phys_econ/lesson_phys_01/lesson.ddn:57 | - | - |
| `거울`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1354 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5185 reserved_words 배열<br>미발견 | - | - |
| - | - | `거짓`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2256 참거짓 리터럴<br>lexer: tools/teul-cli/src/lang/lexer.rs:662 |
| - | - | `건너뛰기`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:401 정본/current-line 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:451 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:688 |
| `검산`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `경계다룸`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| - | - | `고르기`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1451 정본/current-line 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1457 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:681 |
| `고름씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a35_goreumssi_tag_union_red_v1/cases/c01_goreumssi_definition/input.ddn:1, pack/must_gap_a09_match_branch_e_ttara_red_v1/cases/c01_e_ttara_match_surface/input.ddn:1 | - | - |
| `고장`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1353 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5184 reserved_words 배열<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a17_nuri_query_imjadeul_surface_red_v1/cases/c01_imjadeul_query_surface/input.ddn:1 | - | - |
| `고정박자`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `고침`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1358 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5189 reserved_words 배열<br>미발견 | - | - |
| `공간갈래`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `관계씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>미발견 | - | - |
| `관찰범위`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `규칙묶음`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `그것`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2199 §4.4 예약어<br>충돌 위험: pack/must_gap_a30_haebogo_geugeot_frontdoor_red_v1/cases/c01_haebogo_geugeot_frontdoor/input.ddn:2 | - | - |
| `그릇채비`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2201 §4.4 예약어<br>충돌 위험: pack/diag_fixit_json_schema_v1/input_block_header_forbidden.ddn:1, pack/edu_ddn_mc_l03_assign_update/lesson.ddn:1, pack/game_maker_tetris_full/input.ddn:6 | - | - |
| - | - | `그리고`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2200 §4.4 예약어<br>lexer: tools/teul-cli/src/lang/lexer.rs:689 |
| `글`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>충돌 위험: pack/rpg_dialogue_template_parse_v1/input.ddn:2 | - | - |
| `끝`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1631 내장/수명주기 훅 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3045 내장/수명주기 훅 표면<br>충돌 위험: pack/gate0_contract_abort_statehash_v1/input_alert.ddn:7 | - | - |
| `나`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2199 §4.4 예약어<br>충돌 위험: pack/must_gap_a34_self_na_identifier_red_v1/cases/c01_na_self_in_imeumssi/input.ddn:2 | - | - |
| `나란히`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1633 예약 동시성 표면<br>미발견 | - | - |
| `누리`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1351 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5182 reserved_words 배열<br>미발견 | - | - |
| `늘지켜보고`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:740 불변 훅 정본 키워드; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a19_neul_jikyeobogo_invariant_hook_red_v1/cases/c01_invariant_hook_surface/input.ddn:1 | - | - |
| `늦은입력다룸`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `늦은제안다룸`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `다수결모음`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:41 TERMS 키워드/예약/정본 표면<br>미발견 | - | - |
| - | - | `다짐하고`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:758 AI 정본 키워드<br>lexer: tools/teul-cli/src/lang/lexer.rs:680 |
| - | - | `대해`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1619 정본/current-line 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1644 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:686 |
| - | - | `덩이`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5934 정본/current-line 표면; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:1263 TERMS 키워드/예약/정본 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:684 |
| - | - | `동안`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:401 정본/current-line 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1644 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:683 |
| `동점다룸`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `되돌림`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어<br>충돌 위험: pack/seamgrim_josa_binding_v1/c01_newton_motion/input.ddn:4, pack/seamgrim_josa_binding_v1/c02_josa_reorder/input.ddn:4 | - | - |
| - | - | `되풀이`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어<br>lexer: tools/teul-cli/src/lang/lexer.rs:682 |
| `될때`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:401 정본/current-line 표면; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:667 TERMS 키워드/예약/정본 표면<br>grep hit(일반 식별자 패턴 미확인): pack/lang_flow_hook_interaction_v1/c01_흐름씨_후_훅_스냅샷.ddn:20, pack/lang_flow_hook_interaction_v1/c02_같은마디_재발화_금지.ddn:18, pack/lang_hook_when_edge_v1/c01_false_true_edge_once/input.ddn:10 | - | - |
| `드러냄`<br>docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:555 TERMS 키워드/예약/정본 표면<br>grep hit(일반 식별자 패턴 미확인): pack/module_system_smoke_v1/c01_import_export_run/input.ddn:6, pack/module_system_smoke_v1/c07_export_block_duplicate_EXPECT_FAIL/input.ddn:1 | - | - |
| `따라`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a09_match_branch_e_ttara_red_v1/cases/c01_e_ttara_match_surface/input.ddn:2 | - | - |
| - | - | `또는`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2200 §4.4 예약어<br>lexer: tools/teul-cli/src/lang/lexer.rs:690 |
| - | - | `마다`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:669 TERMS 키워드/예약/정본 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:672 |
| `마디`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1348 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5179 reserved_words 배열<br>충돌 위험: pack/std_grid_game_bogae_finite_live_loop_v1/input.ddn:2 | - | - |
| - | - | `만약`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1488 정본/current-line 표면; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:1364 TERMS 키워드/예약/정본 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:673 |
| `말거리`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `맞물림씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>미발견 | - | - |
| - | - | `맞으면`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1526 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:678 |
| `매김`<br>docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:572 TERMS 키워드/예약/정본 표면<br>grep hit(일반 식별자 패턴 미확인): pack/diag_fixit_coverage_v1/input_maegim_grouped.ddn:2, pack/edu_seamgrim_rep_cs_linear_search_timeline_v1/lesson.ddn:8, pack/edu_seamgrim_rep_cs_linear_search_timeline_v1/lesson.ddn:9 | - | - |
| - | - | `매마디`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1632 내장/수명주기 훅 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3044 내장/수명주기 훅 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:670 |
| - | - | `멈추기`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1657 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:687 |
| `모음`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>충돌 위험: pack/age1_container_resource/input.ddn:3, pack/numeric_type_alias_korean_v1/c01_korean_collection_alias_pass.ddn:3 | - | - |
| - | - | `미루기`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:686 정본/current-line 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5934 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:685 |
| `바뀔때`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>미발견 | - | - |
| - | - | `바탕`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1356 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5187 reserved_words 배열<br>lexer: tools/teul-cli/src/lang/lexer.rs:664 |
| - | - | `바탕으로`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:758 AI 정본 키워드<br>lexer: tools/teul-cli/src/lang/lexer.rs:679 |
| - | - | `반복`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1644 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:682 |
| `반환`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어<br>미발견 | - | - |
| `받으면`<br>docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:570 TERMS 키워드/예약/정본 표면<br>grep hit(일반 식별자 패턴 미확인): pack/lang_owner_inner_seum_parser_boundary_spike_v1/input.ddn:4, pack/lang_owner_inner_seum_structure_check_v1/example_surface.ddn:11, pack/lang_owner_inner_seum_structure_check_v1/input.ddn:4 | - | - |
| - | - | `보여주기`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7885 정본/current-line 표면; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:648 TERMS 키워드/예약/정본 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:665 |
| `붙박이마련`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2202 §4.4 예약어<br>충돌 위험: pack/edu_pilot_phys_econ/lesson_phys_01/lesson.ddn:1, pack/edu/pilot_phys_econ/lesson_econ_01/lesson.ddn:1, pack/edu/pilot_phys_econ/lesson_phys_01/lesson.ddn:1 | - | - |
| `사건박자`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `샘`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1349 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5180 reserved_words 배열<br>충돌 위험: pack/game_maker_tetris_full/input.ddn:262, pack/game_maker_tetris_full/input.ddn:263, pack/game_maker_tetris_full/input.ddn:264 | - | - |
| `설정해시`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `셈씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>충돌 위험: pack/seamgrim_josa_binding_v1/c01_newton_motion/input.ddn:2 | - | - |
| `수`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>충돌 위험: pack/edu_seamgrim_rep_cs_linear_search_timeline_v1/lesson.ddn:8 | - | - |
| - | - | `수식`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5293 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:668 |
| `스냅틈`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `슬롯정의`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `시앗묶음`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| - | - | `시작`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1631 내장/수명주기 훅 표면; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3043 내장/수명주기 훅 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:669 |
| `쓰임`<br>docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:554 TERMS 키워드/예약/정본 표면<br>grep hit(일반 식별자 패턴 미확인): pack/module_system_smoke_v1/c01_import_export_run/input.ddn:1, pack/module_system_smoke_v1/c02_public_alias_run/input.ddn:1, pack/module_system_smoke_v1/c03_import_alias_duplicate_EXPECT_FAIL/input.ddn:1 | - | - |
| `쓸감`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1355 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5186 reserved_words 배열<br>미발견 | - | - |
| - | - | `아니고`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5244 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:677 |
| - | - | `아니면`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1488 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:676 |
| `아님`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2200 §4.4 예약어<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a20_nuance_token_combination_red_v1/cases/c01_dollar_nuance_combination/input.ddn:1 | - | - |
| `알림`<br>docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:1181 TERMS 키워드/예약/정본 표면<br>충돌 위험: pack/malhim_rpg_1_v1/input.ddn:8 | - | - |
| `앞선모음`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:40 TERMS 키워드/예약/정본 표면<br>미발견 | - | - |
| `어찌씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>미발견 | - | - |
| - | - | `없음`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>lexer: tools/teul-cli/src/lang/lexer.rs:663 |
| `여러속마디`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `올때`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>미발견 | - | - |
| `움직씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>충돌 위험: pack/lang_ddn_meta_header_basics/c01_basic/input.ddn:1 | - | - |
| - | - | `이라면`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1488 정본/current-line 표면; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:1364 TERMS 키워드/예약/정본 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:674 |
| `이름씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a34_self_na_identifier_red_v1/cases/c01_na_self_in_imeumssi/input.ddn:1, pack/must_gap_a33_imeumssi_body_init_red_v1/cases/c01_imeumssi_body_init/input.ddn:1 | - | - |
| `이면`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:1364 TERMS 키워드/예약/정본 표면<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a09_match_branch_e_ttara_red_v1/cases/c01_e_ttara_match_surface/input.ddn:3, solutions/seamgrim_ui_mvp/lessons/ssot_edu_econ_e008_04_supply_p_q/lesson.ddn:1, solutions/seamgrim_ui_mvp/lessons/ssot_edu_econ_e008_04_supply_p_q/inputs/preset_1.ddn:1 | - | - |
| `이음씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>grep hit(일반 식별자 패턴 미확인): pack/must_gap_a37_ieumssi_operator_red_v1/cases/c01_word_ieumssi/input.ddn:1 | - | - |
| - | - | `일때`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5244 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:675 |
| `일때씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>미발견 | - | - |
| `일묶음씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>미발견 | - | - |
| `임시`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:70 표면 키워드 open issue<br>충돌 위험: pack/seamgrim_guseong_flatten_diag_v1/c18_tuple_out_of_range_index_EXPECT_FAIL/input.ddn:13, pack/seamgrim_guseong_flatten_diag_v1/c20_tuple_access_on_scalar_input_EXPECT_FAIL/input.ddn:13 | - | - |
| `임자`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1350 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5181 reserved_words 배열<br>충돌 위험: pack/w25_all_block_sugar/input.ddn:3 | - | - |
| `입력틈`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `자리모음`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:42 TERMS 키워드/예약/정본 표면<br>미발견 | - | - |
| `잠깐`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:70 표면 키워드 open issue<br>미발견 | - | - |
| `저마다`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2199 §4.4 예약어<br>미발견 | - | - |
| `제안한도`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `지킴이`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1352 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5183 reserved_words 배열<br>미발견 | - | - |
| `진단말`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1357 reserved_words 배열; docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5188 reserved_words 배열<br>미발견 | - | - |
| `짝맞춤`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>충돌 위험: pack/age1_container_resource/input.ddn:4, pack/numeric_type_alias_korean_v1/c01_korean_collection_alias_pass.ddn:4 | - | - |
| `차림`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>충돌 위험: pack/age1_container_resource/input.ddn:2, pack/connect_endpoint_boundary_range_check_fail_v1/input.ddn:8 | - | - |
| - | - | `참`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2256 참거짓 리터럴<br>lexer: tools/teul-cli/src/lang/lexer.rs:661 |
| `참거짓`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2197 §4.4 예약어<br>충돌 위험: pack/seamgrim_wasm_cli_runtime_parity_v1/cases/c06_chaebi_derived_show/input.ddn:3 | - | - |
| `채비`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2203 §4.4 예약어<br>충돌 위험: pack/diag_fixit_coverage_v1/input_header_colon.ddn:1 | - | - |
| - | - | `채우기`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:5603 정본/current-line 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:667 |
| - | `처음`<br>tools/teul-cli/src/lang/lexer.rs:669 | - |
| `첫상태참조`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| - | - | `톺아보기`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2198 §4.4 예약어<br>lexer: tools/teul-cli/src/lang/lexer.rs:666 |
| `하나하나`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2199 §4.4 예약어<br>미발견 | - | - |
| - | - | `할때`<br>SSOT: docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7935 정본/current-line 표면; docs/ssot/ssot/SSOT_TERMS_v24.12.9.md:666 TERMS 키워드/예약/정본 표면<br>lexer: tools/teul-cli/src/lang/lexer.rs:671 |
| `함께`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:1633 예약 동시성 표면<br>미발견 | - | - |
| `해시검사틈`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:29 발표 전 예약 검토 후보<br>미발견 | - | - |
| `흐름`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>충돌 위험: pack/connect_flow_v1c_closure_v1/input.ddn:5 | - | - |
| `흐름씨`<br>docs/ssot/ssot/SSOT_LANG_v24.12.9.md:2196 §4.4 예약어<br>미발견 | - | - |
