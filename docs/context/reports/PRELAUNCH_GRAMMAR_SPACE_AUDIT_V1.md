# 발표 전 문법 공간 예약 감사 V1

작성: 2026-07-08 KST
범위: `tools/teul-cli/src/lang/lexer.rs`의 `#`/`@`/`~` 계열 분기와 실제 `cargo run --manifest-path tools/teul-cli/Cargo.toml -- run ... --summary-json ...` 실행 결과.

임시 입력과 실행 로그는 `work/prelaunch_freeze_sweep/g2/` 아래에만 두었다. `pack/`에는 검증용 `.ddn` 파일을 추가하지 않았다.

## 현재 인식 분기

| 계열 | 현재 lexer 분기 | 근거 |
|---|---|---|
| 행 시작 `#...` | `Lexer::tokenize`에서 line directive start이면 `read_line_pragma()`로 `TokenKind::Pragma` 생성 | `tools/teul-cli/src/lang/lexer.rs:51`, `tools/teul-cli/src/lang/lexer.rs:487`, `tools/teul-cli/src/lang/lexer.rs:509` |
| 행 중간 `#...` | `next_token`의 `'#' => read_hash_or_atom()` 경로로 `TokenKind::Atom` 생성 | `tools/teul-cli/src/lang/lexer.rs:261`, `tools/teul-cli/src/lang/lexer.rs:483`, `tools/teul-cli/src/lang/lexer.rs:514`, `tools/teul-cli/src/lang/lexer.rs:533` |
| `@` | 단일 `TokenKind::At` 생성 | `tools/teul-cli/src/lang/lexer.rs:233` |
| 알려진 `~조사` | `read_josa()`가 `dialect.canonicalize_josa()` 성공 시 `TokenKind::Josa` 생성 | `tools/teul-cli/src/lang/lexer.rs:614`, `tools/teul-cli/src/lang/lexer.rs:635`, `lang/src/dialect.rs:41`, `docs/context/notes/dialect/DDONIRANG_dialect_keywords_full_v8_20260215.tsv:87` |
| 미정의 `~...` | `read_josa()`가 rewind 뒤 `is_tilde_tail_char` 범위를 읽어 `TokenKind::Ident(full_text)` 생성 | `tools/teul-cli/src/lang/lexer.rs:637`, `tools/teul-cli/src/lang/lexer.rs:654`, `tools/teul-cli/src/lang/lexer.rs:1090` |
| `~~>` | `try_read_sym3_token()`의 선행 분기에서 `TokenKind::SignalArrow` 생성 | `tools/teul-cli/src/lang/lexer.rs:180`, `tools/teul-cli/src/lang/lexer.rs:695`, `tools/teul-cli/src/lang/lexer.rs:701` |

## 실측 결과

가능 여부 표기는 브리프의 기준만 따른다: 에러로 막힘 = 가능, 조용히 파싱/실행 = 불가, 이미 의미 있음 = 기존 사용 중.

| 기호 조합 | 입력/명령 로그 | 현재 처리 방식 | 향후 문법화 가능 여부 |
|---|---|---|---|
| 행 시작 `#말씨: en` | `work/prelaunch_freeze_sweep/g2/g2_hash_line_pragma_known.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_hash_line_pragma_known.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_FRONTDOOR_LEGACY_HEADER_FORBIDDEN line=1 key=말씨 use=설정{}/매김{}/설정.보개` | 에러로 막힘=가능 |
| 행 시작 `#미정의: 값` | `work/prelaunch_freeze_sweep/g2/g2_hash_line_pragma_unknown.ddn`; summary `work/prelaunch_freeze_sweep/g2/g2_hash_line_pragma_unknown.summary.detjson`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 0, stdout 첫 줄 `1`, summary 생성 | 조용히 파싱=불가 |
| 행 시작 `##미정의` | `work/prelaunch_freeze_sweep/g2/g2_hash_line_double.ddn`; summary `work/prelaunch_freeze_sweep/g2/g2_hash_line_double.summary.detjson`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 0, stdout 첫 줄 `1`, summary 생성 | 조용히 파싱=불가 |
| 행 중간 `(#ascii) 수식{...}` | `work/prelaunch_freeze_sweep/g2/g2_hash_inline_formula_atom.ddn`; summary `work/prelaunch_freeze_sweep/g2/g2_hash_inline_formula_atom.summary.detjson`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 0, stdout 첫 줄 `(#ascii) 수식{ 1 + 1 }`, summary 생성 | 이미 의미 있음 |
| 행 중간 `#미정의` | `work/prelaunch_freeze_sweep/g2/g2_hash_inline_unknown_atom.ddn`; summary `work/prelaunch_freeze_sweep/g2/g2_hash_inline_unknown_atom.summary.detjson`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 0, stdout 첫 줄 `#미정의`, summary 생성 | 조용히 파싱=불가 |
| 행 중간 단독 `#` | `work/prelaunch_freeze_sweep/g2/g2_hash_inline_bare_atom.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_hash_inline_bare_atom.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_RUN_SUMMARY_WRITE canon 실패: E_CANON_BAD_ATOM 원자 이름이 필요합니다.` | 에러로 막힘=가능 |
| `1@K` | `work/prelaunch_freeze_sweep/g2/g2_at_unit_known.ddn`; summary `work/prelaunch_freeze_sweep/g2/g2_at_unit_known.summary.detjson`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 0, stdout 첫 줄 `1@K`, summary 생성 | 이미 의미 있음 |
| 단독 `@K` | `work/prelaunch_freeze_sweep/g2/g2_at_bare.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_at_bare.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_PARSE_EXPECTED_EXPR ... 표현식이 필요합니다` | 에러로 막힘=가능 |
| `1@` | `work/prelaunch_freeze_sweep/g2/g2_at_missing_unit.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_at_missing_unit.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_PARSE_EXPECTED_UNIT ... 단위가 필요합니다` | 에러로 막힘=가능 |
| `1@@K` | `work/prelaunch_freeze_sweep/g2/g2_at_double.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_at_double.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_PARSE_EXPECTED_UNIT ... 단위가 필요합니다` | 에러로 막힘=가능 |
| 알려진 `~을`/`~에` 조사 | `work/prelaunch_freeze_sweep/g2/g2_tilde_known_josa.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_tilde_known_josa.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_RUN_SUMMARY_WRITE canon 실패: E_CANON_BAD_CHAR 알 수 없는 문자: ~` | 에러로 막힘=가능 |
| 미정의 `~분포` | `work/prelaunch_freeze_sweep/g2/g2_tilde_unknown_simple.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_tilde_unknown_simple.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_RUNTIME_UNDEFINED ... 정의되지 않은 경로: 살림.~분포` | 조용히 파싱=불가 |
| 미정의 `~분포(정규)` | `work/prelaunch_freeze_sweep/g2/g2_tilde_unknown_call_like.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_tilde_unknown_call_like.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_RUNTIME_UNDEFINED ... 정의되지 않은 경로: 살림.~분포(정규)` | 조용히 파싱=불가 |
| 미정의 `~분포-정규` | `work/prelaunch_freeze_sweep/g2/g2_tilde_unknown_dash.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_tilde_unknown_dash.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_RUNTIME_UNDEFINED ... 정의되지 않은 경로: 살림.~분포-정규` | 조용히 파싱=불가 |
| 숫자 뒤 미정의 `1~분포` | `work/prelaunch_freeze_sweep/g2/g2_tilde_after_number_unknown.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_tilde_after_number_unknown.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_PARSE_UNEXPECTED_TOKEN ... 예상: '.' or newline` | 에러로 막힘=가능 |
| 식 안의 `~~>` | `work/prelaunch_freeze_sweep/g2/g2_tilde_signal_arrow_expr.ddn`; stderr `work/prelaunch_freeze_sweep/g2/g2_tilde_signal_arrow_expr.stderr.txt`; 결과 모음 `work/prelaunch_freeze_sweep/g2/run_results.jsonl` | exit 1, `E_PARSE_UNEXPECTED_TOKEN ... 예상: '.' or newline` | 에러로 막힘=가능 |

## 검증 로그

- 실행 케이스: 16건
- 모든 표 행에 입력 파일, stdout/stderr 또는 summary 경로를 인용했다.
- 임시 `.ddn` 위치: `work/prelaunch_freeze_sweep/g2/`
- pack 추가: 없음
