# MUST_GAP_DECISION_QUEUE_V1

이 문서는 결정하지 않는다. 사용자/Claude가 다음에 결정할 원재료 목록이다.

## 범위

- 원본 범위: `docs/context/reports/MUST_GAP_DEEPDIVE_A01_*.md` ~ `MUST_GAP_DEEPDIVE_A47_*.md` 47개.
- 추출 대상: 각 원본의 `## 결정 필요` 절에 있는 불릿 원문.
- 금지: 의역/요약/신규 설계 결정 없음.

## 검증 요약

- 원본 리포트 수: 47
- 원본 결정 필요 불릿 수 합계: 81
- `- 원본:` anchor는 항목당 1개만 둔다.

## 그룹별 결정 대기

### 이름 충돌/오류코드 명명

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A01 | `[V18-00D] X vs X하 이름 충돌 금지` | 예 (#1 `X`/`X하`/call-tail 충돌) | 2 |
| A02 | CALL-TAIL-RESOLVE-01 해석 규칙 | 예 (#1 `X`/`X하`/call-tail 충돌) | 1 |

#### A01 — `[V18-00D] X vs X하 이름 충돌 금지`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A01_x_xha_collision_V1.md](MUST_GAP_DEEPDIVE_A01_x_xha_collision_V1.md)
- 기존 top-10 여부: 예 (#1 `X`/`X하`/call-tail 충돌)
- 결정 필요 원문:

```text
- 정의 시점에서 바로 `E_SEED_NAME_CONFLICT_X_HA`류 진단을 낼지, AGE2 별칭 문법이 도입될 때까지 runtime ambiguity fail만 유지할지 결정 필요.
- 오류 코드 이름은 SSOT에 고정되어 있지 않으므로 사용자/SSOT 관리자 결정이 필요하다.
```

#### A02 — CALL-TAIL-RESOLVE-01 해석 규칙

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A02_call_tail_resolve_unresolved_V1.md](MUST_GAP_DEEPDIVE_A02_call_tail_resolve_unresolved_V1.md)
- 기존 top-10 여부: 예 (#1 `X`/`X하`/call-tail 충돌)
- 결정 필요 원문:

```text
    - 0개 후보를 E_CALL_TAIL_UNRESOLVED로 고정할지, 현재 E_RUNTIME_TYPE_MISMATCH fallback을 유지할지 결정 필요.
```

### 파이프/해서 표면

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A04 | §P1 파이프(해서) | 예 (#3 `해서` 파이프 §P1) | 1 |
| A05 | §P1.2 호출식만 허용 | 예 (#3 `해서` 파이프 §P1) | 1 |
| A06 | §P1.3 암묵 주입 금지 | 예 (#3 `해서` 파이프 §P1) | 1 |
| A07 | §P1.6 `{ ... }해서` 파이프 꼬리 | 예 (#3 `해서` 파이프 §P1) | 1 |
| A08 | §P1.7 흐름값 주입 알고리즘 | 예 (#3 `해서` 파이프 §P1) | 1 |

#### A04 — §P1 파이프(해서)

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A04_p1_pipe_surface_V1.md](MUST_GAP_DEEPDIVE_A04_p1_pipe_surface_V1.md)
- 기존 top-10 여부: 예 (#3 `해서` 파이프 §P1)
- 결정 필요 원문:

```text
    - 파이프 표면을 call-tail/흐름값 규칙과 어느 계층에서 통합할지 결정 필요.
```

#### A05 — §P1.2 호출식만 허용

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A05_p1_pipe_call_only_V1.md](MUST_GAP_DEEPDIVE_A05_p1_pipe_call_only_V1.md)
- 기존 top-10 여부: 예 (#3 `해서` 파이프 §P1)
- 결정 필요 원문:

```text
    - stage 문법을 호출식으로만 제한할 진단 코드 이름 결정 필요.
```

#### A06 — §P1.3 암묵 주입 금지

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A06_p1_pipe_no_implicit_inject_V1.md](MUST_GAP_DEEPDIVE_A06_p1_pipe_no_implicit_inject_V1.md)
- 기존 top-10 여부: 예 (#3 `해서` 파이프 §P1)
- 결정 필요 원문:

```text
    - flow value injection을 명시 pin 전용으로 닫을지, 위치 fallback을 허용할지 SSOT §P1.7과 함께 결정 필요.
```

#### A07 — §P1.6 `{ ... }해서` 파이프 꼬리

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A07_p1_block_tail_pipe_V1.md](MUST_GAP_DEEPDIVE_A07_p1_block_tail_pipe_V1.md)
- 기존 top-10 여부: 예 (#3 `해서` 파이프 §P1)
- 결정 필요 원문:

```text
    - 토막 꼬리 `}해서`를 `}하고`/계약 표면과 같은 계층에서 처리할지 결정 필요.
```

#### A08 — §P1.7 흐름값 주입 알고리즘

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A08_p1_pipe_inject_algorithm_V1.md](MUST_GAP_DEEPDIVE_A08_p1_pipe_inject_algorithm_V1.md)
- 기존 top-10 여부: 예 (#3 `해서` 파이프 §P1)
- 결정 필요 원문:

```text
    - 모호성 오류와 기본 주입 순서를 제품 PinSpec과 통합할지 결정 필요.
```

### match 분기

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A09 | 27.1.1 갈래 분기 `~에 따라` | 예 (#4 `~에 따라`/`없으면`) | 1 |
| A10 | 27.1.1.1 `E에 따라 { ... }` 문법 | 예 (#4 `~에 따라`/`없으면`) | 1 |
| A11 | 27.1.1.2 바인딩/스코프 규칙 | 예 (#4 `~에 따라`/`없으면`) | 1 |
| A12 | 27.1.1.3 타입 규칙 | 예 (#4 `~에 따라`/`없으면`) | 1 |
| A13 | 27.1.1.4 완전성/중복 규칙 | 예 (#4 `~에 따라`/`없으면`) | 1 |
| A14 | 27.1.1.5 반환 타입 규칙 | 예 (#4 `~에 따라`/`없으면`) | 1 |
| A15 | 27.1.1.6 `없으면` sugar | 예 (#4 `~에 따라`/`없으면`) | 1 |

#### A09 — 27.1.1 갈래 분기 `~에 따라`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A09_match_branch_e_ttara_V1.md](MUST_GAP_DEEPDIVE_A09_match_branch_e_ttara_V1.md)
- 기존 top-10 여부: 예 (#4 `~에 따라`/`없으면`)
- 결정 필요 원문:

```text
    - `고르기`와 별도 expression match로 둘지, sugar로 낮출지 결정 필요.
```

#### A10 — 27.1.1.1 `E에 따라 { ... }` 문법

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A10_match_branch_syntax_V1.md](MUST_GAP_DEEPDIVE_A10_match_branch_syntax_V1.md)
- 기존 top-10 여부: 예 (#4 `~에 따라`/`없으면`)
- 결정 필요 원문:

```text
    - 패턴 문법과 branch body expression/statement 형태를 확정해야 한다.
```

#### A11 — 27.1.1.2 바인딩/스코프 규칙

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A11_match_branch_binding_scope_V1.md](MUST_GAP_DEEPDIVE_A11_match_branch_binding_scope_V1.md)
- 기존 top-10 여부: 예 (#4 `~에 따라`/`없으면`)
- 결정 필요 원문:

```text
    - 패턴 payload binding을 branch-local scope로 제한하는 symbol table 규칙 결정 필요.
```

#### A12 — 27.1.1.3 타입 규칙

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A12_match_branch_type_rules_V1.md](MUST_GAP_DEEPDIVE_A12_match_branch_type_rules_V1.md)
- 기존 top-10 여부: 예 (#4 `~에 따라`/`없으면`)
- 결정 필요 원문:

```text
    - 옵션/참거짓/고름씨 match 대상 타입 집합과 불가능 패턴 진단을 확정해야 한다.
```

#### A13 — 27.1.1.4 완전성/중복 규칙

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A13_match_branch_completeness_overlap_V1.md](MUST_GAP_DEEPDIVE_A13_match_branch_completeness_overlap_V1.md)
- 기존 top-10 여부: 예 (#4 `~에 따라`/`없으면`)
- 결정 필요 원문:

```text
    - 고름씨/옵션 variant exhaustiveness와 중복/순서 진단 정책 결정 필요.
```

#### A14 — 27.1.1.5 반환 타입 규칙

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A14_match_branch_return_type_V1.md](MUST_GAP_DEEPDIVE_A14_match_branch_return_type_V1.md)
- 기존 top-10 여부: 예 (#4 `~에 따라`/`없으면`)
- 결정 필요 원문:

```text
    - match를 expression으로 둘 때 branch 결과 타입 통합 규칙 결정 필요.
```

#### A15 — 27.1.1.6 `없으면` sugar

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A15_match_branch_none_sugar_V1.md](MUST_GAP_DEEPDIVE_A15_match_branch_none_sugar_V1.md)
- 기존 top-10 여부: 예 (#4 `~에 따라`/`없으면`)
- 결정 필요 원문:

```text
    - `없으면`을 match sugar로 낮출지 독립 coalesce operator로 둘지 결정 필요.
```

### MathIR/증명 표현

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A16 | §M1.5 MathIR v1 / De Bruijn / DetBin | 예 (#5 MathIR v1/De Bruijn/DetBin) | 1 |

#### A16 — §M1.5 MathIR v1 / De Bruijn / DetBin

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A16_mathir_v1_debruijn_detbin_V1.md](MUST_GAP_DEEPDIVE_A16_mathir_v1_debruijn_detbin_V1.md)
- 기존 top-10 여부: 예 (#5 MathIR v1/De Bruijn/DetBin)
- 결정 필요 원문:

```text
    - MathIR node set, binder normalization, DetBin byte layout을 TOOLCHAIN/제품 경로 중 어디서 먼저 고정할지 결정 필요.
```

### 누리 query 표면

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A17 | 16.2 쿼리 표현식과 필터 `임자들` | 예 (#6 누리 query 표면) | 1 |
| A18 | 16.3 군집 실행 블록 `모두` | 예 (#6 누리 query 표면) | 1 |

#### A17 — 16.2 쿼리 표현식과 필터 `임자들`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A17_nuri_query_imjadeul_surface_V1.md](MUST_GAP_DEEPDIVE_A17_nuri_query_imjadeul_surface_V1.md)
- 기존 top-10 여부: 예 (#6 누리 query 표면)
- 결정 필요 원문:

```text
    - 언어 표면 query를 core archetype API에 연결할지, 먼저 pack/spec로 더 나눌지 결정 필요.
```

#### A18 — 16.3 군집 실행 블록 `모두`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A18_nuri_query_modu_block_V1.md](MUST_GAP_DEEPDIVE_A18_nuri_query_modu_block_V1.md)
- 기존 top-10 여부: 예 (#6 누리 query 표면)
- 결정 필요 원문:

```text
    - `모두 {}`를 기존 `~에 대해` sugar로 낮출지, query executor를 별도로 둘지 결정 필요.
```

### 늘지켜보고/불변 훅

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A19 | 16.2 `늘지켜보고` 문법 | 예 (#7 `늘지켜보고`/`덧댐거부`) | 1 |

#### A19 — 16.2 `늘지켜보고` 문법

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A19_neul_jikyeobogo_invariant_hook_V1.md](MUST_GAP_DEEPDIVE_A19_neul_jikyeobogo_invariant_hook_V1.md)
- 기존 top-10 여부: 예 (#7 `늘지켜보고`/`덧댐거부`)
- 결정 필요 원문:

```text
    - `늘지켜보고`를 계약 시스템에 낮출지 별도 commit-stage hook으로 둘지 결정 필요. `덧댐거부` 감사 이벤트도 별도 결정 필요.
```

### nuance 결합 ($ 토큰류)

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A20 | 17.5 말결 결합 규칙 | 예 (#8 말결 `$...`) | 1 |
| A21 | `5.4 규칙` 말결 없음/중복/부정 결합 | 예 (#8 말결 `$...`) | 2 |
| A22 | `뉘.3 부정과의 조합` | 예 (#8 말결 `$...`) | 2 |

#### A20 — 17.5 말결 결합 규칙

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A20_nuance_token_combination_V1.md](MUST_GAP_DEEPDIVE_A20_nuance_token_combination_V1.md)
- 기존 top-10 여부: 예 (#8 말결 `$...`)
- 결정 필요 원문:

```text
    - 말결을 lexer token으로 둘지, builtin 함수 계층에 머물게 할지 결정 필요. 부정어 결합의 부호/스케일 정책도 필요하다.
```

#### A21 — `5.4 규칙` 말결 없음/중복/부정 결합

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A21_nuance_54_rules_V1.md](MUST_GAP_DEEPDIVE_A21_nuance_54_rules_V1.md)
- 기존 top-10 여부: 예 (#8 말결 `$...`)
- 결정 필요 원문:

```text
- `$...`를 lexer token으로 승격할지, 기존 `말결값(문자열)` builtin과 별도 계층으로 병존시킬지 결정 필요.
- 부정 결합의 “부호 반전”이 weight 부호인지, valence 축 반전인지, 논리 결과의 confidence 반전인지 런타임 의미를 확정해야 한다.
```

#### A22 — `뉘.3 부정과의 조합`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A22_nuance_negation_combination_V1.md](MUST_GAP_DEEPDIVE_A22_nuance_negation_combination_V1.md)
- 기존 top-10 여부: 예 (#8 말결 `$...`)
- 결정 필요 원문:

```text
- `아님`이 논리값 자체를 뒤집을 때 말결 weight를 어떻게 보존/반전할지 결정 필요.
- `$전혀` 같은 0.0 계열과 부정어가 결합할 때 결과 weight의 하한/상한 및 정본 표현을 확정해야 한다.
```

### AI Gym 표면

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A23 | `AI.1 끝내` | 예 (#9 AI Gym 표면) | 2 |

#### A23 — `AI.1 끝내`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A23_ai_end_episode_surface_V1.md](MUST_GAP_DEEPDIVE_A23_ai_end_episode_surface_V1.md)
- 기존 top-10 여부: 예 (#9 AI Gym 표면)
- 결정 필요 원문:

```text
- `끝내`를 DDN runtime builtin으로 둘지, NuriGym 전용 effect statement로 둘지 결정 필요.
- `끝내.` 호출 시 현재 episode의 `done` 처리, reward zeroing 여부, multi-agent/shared-env 전파 범위를 확정해야 한다.
```

### josa/jamo 예약어

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A24 | `NAMING-LINT 1) 금지(예약)` | 예 (#10 조사/canon/SEMSI) | 2 |
| A25 | `NAMING-LINT 3) 정본화` | 예 (#10 조사/canon/SEMSI) | 2 |
| A31 | `시스템 예약 자음 식별자` | 아니오 | 2 |

#### A24 — `NAMING-LINT 1) 금지(예약)`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A24_josa_reserved_identifier_V1.md](MUST_GAP_DEEPDIVE_A24_josa_reserved_identifier_V1.md)
- 기존 top-10 여부: 예 (#10 조사/canon/SEMSI)
- 결정 필요 원문:

```text
- bare 조사 단독 금지를 lexer 단계 fatal로 둘지, parser/lint 단계 diagnostic으로 둘지 결정 필요.
- 금지 목록 확장 시 Minor만 허용한다는 SSOT 정책을 제품 config/registry에 어떻게 반영할지 결정 필요.
```

#### A25 — `NAMING-LINT 3) 정본화`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A25_josa_canon_tilde_insertion_V1.md](MUST_GAP_DEEPDIVE_A25_josa_canon_tilde_insertion_V1.md)
- 기존 top-10 여부: 예 (#10 조사/canon/SEMSI)
- 결정 필요 원문:

```text
- 자동 split을 lexer tokenization에서 수행할지, parser/name resolution 이후 canon 단계에서 수행할지 결정 필요.
- `T`와 `S`가 모두 유효한 경우 경고와 fatal의 경계를 lint 정책으로 확정해야 한다.
```

#### A31 — `시스템 예약 자음 식별자`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A31_jamo_reserved_identifier_V1.md](MUST_GAP_DEEPDIVE_A31_jamo_reserved_identifier_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 자음식별자 금지를 lexer fatal로 둘지, parser/lint 단계에서 이름 선언 위치별로 집행할지 결정 필요.
- SystemRootAlias 표의 소유 위치와 확장 정책을 TERM-MAP/NAME-LINT와 어떻게 연결할지 결정해야 한다.
```

### 용어/버전 표기 정책

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A27 | `[V18-00A-1] TERM-MAP 단일 소스` | 아니오 | 2 |
| A28 | `기계 판독용 TERM-MAP 블록` | 아니오 | 2 |
| A29 | `[V18-00B] 버전 표기 정책` | 아니오 | 2 |

#### A27 — `[V18-00A-1] TERM-MAP 단일 소스`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A27_term_map_single_source_V1.md](MUST_GAP_DEEPDIVE_A27_term_map_single_source_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- TERM-MAP 추출기를 빌드 단계 codegen으로 둘지, 런타임에 SSOT JSON 블록 해시를 읽는 방식으로 둘지 결정 필요.
- FATAL/LEGACY/WARN 정책을 `teul-cli` canon, lint, LSP quick-fix 중 어느 계층에서 authoritative하게 적용할지 결정 필요.
```

#### A28 — `기계 판독용 TERM-MAP 블록`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A28_term_map_machine_block_V1.md](MUST_GAP_DEEPDIVE_A28_term_map_machine_block_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- SSOT markdown 내부 JSON 블록을 제품 빌드가 직접 읽을지, 별도 generated artifact를 승인 후 생성할지 결정 필요.
- TermMap hash를 report metadata, lint diagnostic, pack contract 중 어디에 필수로 실을지 결정해야 한다.
```

#### A29 — `[V18-00B] 버전 표기 정책`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A29_version_notation_policy_V1.md](MUST_GAP_DEEPDIVE_A29_version_notation_policy_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 이 정책을 docs lint로 둘지, SSOT release helper로 둘지, AI prompt 생성 단계의 hard gate로 둘지 결정 필요.
- `r1/r2` 탐지를 단순 regex로 할지, 문맥상 revision 표기만 골라낼지 기준이 필요하다.
```

### ambiguity/LSP quickfix

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A32 | `[ASSIGN-ARROW-RIGHT-01] -> 우향 대입` | 아니오 | 2 |
| A43 | `10.5.2 바인딩 모호성 진단 + LSP QuickFix` | 아니오 | 3 |

#### A32 — `[ASSIGN-ARROW-RIGHT-01] -> 우향 대입`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A32_assign_arrow_right_V1.md](MUST_GAP_DEEPDIVE_A32_assign_arrow_right_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- `->`를 lexer token으로 둘지, parser에서 `Minus` + `Gt`를 sugar로 조립할지 결정 필요.
- 대입용 `->`와 타입 시그니처 `T -> U`의 문맥 충돌을 어느 단계에서 분리할지 결정해야 한다.
```

#### A43 — `10.5.2 바인딩 모호성 진단 + LSP QuickFix`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A43_binding_ambiguity_lsp_quickfix_V1.md](MUST_GAP_DEEPDIVE_A43_binding_ambiguity_lsp_quickfix_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 제품 `tools/teul-cli` AST에 ambiguous candidate list를 보존할지, LSP 전용 분석기가 별도 symbol table에서 후보를 계산할지 결정 필요.
- `PIN_AMBIGUOUS` 오류 코드의 계층이 parser/runtime/LSP 중 어디에 속하는지 확정해야 한다.
- `@` 오용 QuickFix의 자동 치환 범위가 `@대상` 전체인지, 뒤따르는 `~조사`까지 포함한 접미 chain 전체인지 결정 필요.
```

### stem/multi-dispatch

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A33 | `이름씨 본문 초기화 규칙` | 아니오 | 2 |
| A34 | `자기 참조 나` | 아니오 | 2 |
| A35 | `고름씨 정의` | 아니오 | 2 |
| A36 | `고름씨 정의 문법` | 아니오 | 2 |
| A37 | `6.2.2 말 이음씨` | 아니오 | 2 |
| A38 | `6.2.3 기호 이음씨` | 아니오 | 2 |
| A39 | `6.2.4 확장 이음기호 집합` | 아니오 | 2 |
| A40 | `6.2.5 사용자 정의 이음씨 우선순위` | 아니오 | 2 |
| A41 | `7.3 흐름씨-훅 위상 분리` | 아니오 | 3 |
| A42 | `10.4.1 숫자 리터럴 접미 분리` | 아니오 | 3 |
| A44 | `11.3.1 원칙` | 아니오 | 2 |
| A45 | `11.3.3 교대 트리거` | 아니오 | 3 |
| A46 | `11.3.4 정본 처리 파이프라인` | 아니오 | 3 |
| A47 | `14. 다중 디스덧댐` | 아니오 | 3 |

#### A33 — `이름씨 본문 초기화 규칙`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A33_imeumssi_body_init_V1.md](MUST_GAP_DEEPDIVE_A33_imeumssi_body_init_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- `이름씨`를 현재 ECS/임자 모델의 component type으로 직접 낮출지, 별도 type constructor 계층으로 둘지 결정 필요.
- 본문 내 실행문과 nested seed definition의 static binding 순서를 확정해야 한다.
```

#### A34 — `자기 참조 나`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A34_self_na_identifier_V1.md](MUST_GAP_DEEPDIVE_A34_self_na_identifier_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- `나`를 `이름씨` constructor/init frame의 lexical binding으로 둘지, runtime object receiver slot으로 둘지 결정 필요.
- `나` 캡처 허용 범위와 `제`와의 충돌/동시 사용 진단을 확정해야 한다.
```

#### A35 — `고름씨 정의`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A35_goreumssi_tag_union_V1.md](MUST_GAP_DEEPDIVE_A35_goreumssi_tag_union_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- `고름씨` runtime 표현을 문자열 atom으로 유지할지, SSOT의 `(고름씨ID, 변형Index)` 정수쌍 표현으로 전환할지 결정 필요.
- 기존 context tag 중복 검사와 closed union registry의 책임 경계를 확정해야 한다.
```

#### A36 — `고름씨 정의 문법`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A36_goreumssi_definition_syntax_V1.md](MUST_GAP_DEEPDIVE_A36_goreumssi_definition_syntax_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- `고름씨` 정의를 기존 seed parser에 통합할지, type declaration parser로 분리할지 결정 필요.
- variant field default와 ABI ordering을 canon/state_hash 경계에서 어떻게 직렬화할지 결정해야 한다.
```

#### A37 — `6.2.2 말 이음씨`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A37_word_ieumssi_operator_V1.md](MUST_GAP_DEEPDIVE_A37_word_ieumssi_operator_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 사용자 정의 이음씨 registry를 parser symbol table에 둘지, type checker 이후 lowering 단계에 둘지 결정 필요.
- word operator와 기존 call-tail/bare call 해석의 충돌 우선순위를 확정해야 한다.
```

#### A38 — `6.2.3 기호 이음씨`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A38_symbol_ieumssi_operator_V1.md](MUST_GAP_DEEPDIVE_A38_symbol_ieumssi_operator_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- builtin 기호와 사용자 정의 기호의 shadowing/override 허용 범위를 결정해야 한다.
- `+~더하기` alias metadata를 canon artifact에 보존할지, type registry에만 보존할지 결정 필요.
```

#### A39 — `6.2.4 확장 이음기호 집합`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A39_extended_operator_symbols_V1.md](MUST_GAP_DEEPDIVE_A39_extended_operator_symbols_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- EXT_OPCHAR scanner가 기존 sym3/token dispatch보다 먼저 실행될지, reserved token을 먼저 차단할지 결정 필요.
- Unicode variation selector 정규화/오류 정책을 제품 진단으로 확정해야 한다.
```

#### A40 — `6.2.5 사용자 정의 이음씨 우선순위`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A40_user_operator_precedence_V1.md](MUST_GAP_DEEPDIVE_A40_user_operator_precedence_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 사용자 operator precedence를 parse-time에 반영할지, parse 후 Pratt/precedence 재구성 단계로 둘지 결정 필요.
- 같은 우선순위/결합성 기본값과 충돌 diagnostic을 확정해야 한다.
```

#### A41 — `7.3 흐름씨-훅 위상 분리`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A41_flow_hook_phase_reverify_V1.md](MUST_GAP_DEEPDIVE_A41_flow_hook_phase_reverify_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- `SSOT_MUST_RULE_AUDIT_TIER2_V1.md`의 A41 행을 다음 감사 라운드에서 `미구현`에서 `구현/검증됨 후보` 또는 `추가 검증 필요`로 재분류할지 결정 필요.
- 이전 `FLOW_HOOK_PHASE_SEPARATION_VERIFICATION_V1.md`는 현재 코드와 충돌하므로, 별도 문서 정정/폐기/후속 검증 보고서 승격 여부 결정 필요.
- `closure_claim: yes`를 공식 behavior-closed로 인정하려면 core_lang sanity 외에 해당 pack checker를 정규 CI 게이트에 포함할지 결정 필요.
```

#### A42 — `10.4.1 숫자 리터럴 접미 분리`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A42_numeric_literal_suffix_split_V1.md](MUST_GAP_DEEPDIVE_A42_numeric_literal_suffix_split_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 숫자 뒤 ASCII 단위(`cm`, `m`, `s`)와 한글 조사(`를`, `을` 등)를 lexer token 내부에서 분해할지, parser suffix-chain 단계에서 원문 span을 재분석할지 결정 필요.
- `100cm를`의 정본을 `100@cm~를`처럼 explicit 접착자로 canonicalize할지, AST에 원접미 chain을 보존할지 결정 필요.
- 단위 후보가 스코프 식별자와 충돌할 때의 오류 코드와 QuickFix 문구가 필요하다.
```

#### A44 — `11.3.1 원칙`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A44_stem_ambiguity_no_guess_principle_V1.md](MUST_GAP_DEEPDIVE_A44_stem_ambiguity_no_guess_principle_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 11.3.1 원칙의 닫힘 기준을 runtime call-tail ambiguity만으로 볼지, 정의 시점 이름 충돌 금지와 0개 후보 전용 진단까지 포함해 볼지 결정 필요.
- 표면 추천/출력 계층(LSP/formatter/canon export)의 닫힘 기준 pack을 별도 분리할지 결정 필요.
```

#### A45 — `11.3.3 교대 트리거`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A45_stem_alternation_trigger_V1.md](MUST_GAP_DEEPDIVE_A45_stem_alternation_trigger_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- trigger table을 parser/canon 단계에서 표면 이름으로 낮출지, runtime seed dispatch 전에 후보 생성기로 둘지 결정 필요.
- `니/으니`, `면/으면`, `니까/으니까`, `며/으며`, `면서/으면서`의 최소 Gate0 scope와 오류 코드를 확정해야 한다.
- A46의 3-step pipeline과 같은 pack으로 닫을지, trigger 전용 pack과 pipeline 전용 pack을 분리할지 결정 필요.
```

#### A46 — `11.3.4 정본 처리 파이프라인`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A46_stem_canon_pipeline_V1.md](MUST_GAP_DEEPDIVE_A46_stem_canon_pipeline_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 3-step pipeline을 parser/canon에서 실행해 AST를 확정할지, runtime dispatch 직전의 별도 resolver에서 실행할지 결정 필요.
- 축약/표기 정리는 save/format 출력 전용으로 둘지, 입력 정본화에도 포함할지 결정 필요.
- `E_CALL_TAIL_AMBIGUOUS`와 별도 형태소 pipeline 오류 코드의 관계를 정해야 한다.
```

#### A47 — `14. 다중 디스덧댐`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A47_multi_dispatch_specificity_V1.md](MUST_GAP_DEEPDIVE_A47_multi_dispatch_specificity_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- 같은 이름 seed를 parser 단계에서 다중 후보로 허용할지, 현재처럼 단일 이름 충돌을 금지하고 별도 overload 문법을 둘지 결정 필요.
- 타입 구체성 lattice를 `셈수/바른수/정수32` 같은 numeric family부터 최소 구현할지, 전체 타입/고름씨/엔티티까지 확장할지 결정 필요.
- 오류 코드는 `E_MULTI_DISPATCH_AMBIGUOUS`류로 새로 둘지, 기존 type mismatch 계열에 포함할지 결정 필요.
```

### 기타

| 항목 | 규칙/제목 | 기존 top-10 여부 | 결정 필요 불릿 수 |
|---|---|---|---:|
| A03 | 7.2 이전값보기 | 예 (#2 `이전값보기`) | 1 |
| A26 | `SEMSI-RESULT-01 셈씨 결과칸` | 예 (#10 조사/canon/SEMSI) | 2 |
| A30 | `[V18-02] ~해보고: + 그것` | 아니오 | 2 |

#### A03 — 7.2 이전값보기

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A03_previous_value_view_V1.md](MUST_GAP_DEEPDIVE_A03_previous_value_view_V1.md)
- 기존 top-10 여부: 예 (#2 `이전값보기`)
- 결정 필요 원문:

```text
    - D55처럼 참조된 대상만 저장하는 스냅샷 범위를 제품 경로에 넣을지 결정 필요. 이번 작업에서는 구현하지 않는다.
```

#### A26 — `SEMSI-RESULT-01 셈씨 결과칸`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A26_semsi_result_slot_V1.md](MUST_GAP_DEEPDIVE_A26_semsi_result_slot_V1.md)
- 기존 top-10 여부: 예 (#10 조사/canon/SEMSI)
- 결정 필요 원문:

```text
- 기존 `돌려주기` 반환과 SEMSI 결과칸 대입을 병행 허용할지, 셈씨 내부에서는 결과칸 대입만 허용할지 결정 필요.
- 결과칸 미대입과 섀도잉 오류의 diagnostic 이름을 확정해야 한다.
```

#### A30 — `[V18-02] ~해보고: + 그것`

- 원본: [docs/context/reports/MUST_GAP_DEEPDIVE_A30_haebogo_geugeot_frontdoor_parity_V1.md](MUST_GAP_DEEPDIVE_A30_haebogo_geugeot_frontdoor_parity_V1.md)
- 기존 top-10 여부: 아니오
- 결정 필요 원문:

```text
- `tools/teul-cli`가 루트 `ddonirang-lang`의 `Stmt::Try`를 제품 frontdoor로 재사용할지, 내부 `tools/teul-cli/src/lang`에 별도 표면을 맞출지 결정 필요.
- root `lang`/legacy `tool` 구현을 현재 Gate0 제품 경로로 승격할 수 있는지 별도 parity 검증이 필요하다.
```
