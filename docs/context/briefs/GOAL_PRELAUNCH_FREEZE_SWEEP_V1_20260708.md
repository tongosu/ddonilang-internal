# GOAL: 발표 전 동결 스윕 — 예약어/문법공간/오류코드 실측 감사

작성: 2026-07-08 KST
선행 배치: `docs/context/briefs/GOAL_LONGHORIZON_FOLLOWUP_V1_20260707.md` (트랙 D/E/F 완료, `main` 병합: `a4f762b`)
관련 자료: `docs/context/reports/MUST_GAP_DECISION_QUEUE_V1.md`(결정 대기 81건), `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER1~4_V1.md`(MUST 179건 감사)

## 배경

"발표 후 문법 변경은 사용자에 대한 배신"이라는 원칙 아래, 발표 전 반드시 동결해야 할 항목 6가지 중 **실측(grep/코드 대조)만으로 감사 가능한 4가지**를 이번 배치로 돌린다. 나머지 2가지(스키마 버전 협상 규칙 확정, 모듈/import 표면을 이번 발표 범위에서 뺄지 결정)는 설계 판단이 필요해 이번 배치에서 다루지 않는다 — 사용자/Claude 몫이다.

**중요**: 이번 배치는 순수 실측/대조 문서 작성이다. 예약어를 실제로 추가하거나, 파서에 새 에러를 추가하거나, 오류 코드를 새로 만들지 않는다. "무엇이 비어 있는지" 표로만 만든다.

## 트랙 G1 — 예약어 선점 감사

### Outcome

- 신규 문서 `docs/context/reports/PRELAUNCH_RESERVED_WORD_AUDIT_V1.md`를 작성한다.
- `docs/ssot/ssot/SSOT_LANG_v24.12.9.md`와 `docs/ssot/ssot/SSOT_TERMS_v24.12.9.md`에서 예약어/키워드로 명시된 순우리말 정본 토큰 전체를 추출한다(정의 위치 인용 포함).
- `tools/teul-cli/src/lang/lexer.rs`에서 실제로 reserved keyword로 매치되는 토큰 목록을 추출한다(코드 인용 포함).
- 두 목록을 대조해 3개 열로 표를 만든다: SSOT에 있으나 lexer에 없음 / lexer에 있으나 SSOT에 없음 / 양쪽 일치.
- 추가로: SSOT-only 열에 있는 각 후보 이름이 `pack/`, `tests/`, `gaji/`, `solutions/` 안의 실제 `.ddn` 코드에서 이미 일반 식별자(변수/함수명)로 쓰이고 있는지 grep으로 확인하고, 쓰이고 있으면 "충돌 위험"으로 표시한다(이미 사용 중이면 나중에 예약어로 못 만든다는 뜻).
- 판단/결정 문장을 넣지 않는다 — "빠짐"과 "충돌 위험"만 표시.

### Verification

- 두 원본 목록(SSOT 추출, lexer 추출) 각각의 항목 수를 로그에 남긴다.
- 표의 행 수가 두 목록의 합집합 크기와 일치하는지 확인.

## 트랙 G2 — 문법 공간 예약 감사

### Outcome

- 신규 문서 `docs/context/reports/PRELAUNCH_GRAMMAR_SPACE_AUDIT_V1.md`를 작성한다.
- `tools/teul-cli/src/lang/lexer.rs`에서 `#`/`@`/`~` 계열 기호의 모든 매치 분기(현재 실제로 인식되는 조합)를 나열한다.
- 각 기호 계열에서 **현재 매치되지 않는 조합**(예: 문서상 미정의 상태)을 입력했을 때 실제로 어떻게 처리되는지 실측한다: (a) 명시적 파서 에러로 막히는지, (b) 조용히 다른 토큰(식별자 등)으로 파싱되는지. 이걸 확인하려면 `pack/` 아래 임시 검증용이 아니라, 각 케이스를 `cargo run --manifest-path tools/teul-cli/Cargo.toml -- run --summary-json`으로 실제 실행해 결과를 캡처한다(테스트 케이스 파일은 브리프 작업 디렉터리 내 임시 위치에만 두고 pack에 커밋하지 않는다).
- 결과를 표로: 기호 조합 / 현재 처리 방식(에러 코드 또는 파싱 결과) / "향후 문법화 가능 여부"(에러로 막혀 있으면 가능, 조용히 파싱되면 이미 새서 불가).
- 판단/결정 문장 없이 실측 결과만.

### Verification

- 표에 있는 모든 행이 실제 실행 결과(에러 코드 또는 파싱 출력)로 뒷받침되는지, 즉 추측이 아닌 실측인지 각 행에 실행 로그 인용을 남긴다.

## 트랙 G3 — 오류 코드 네임스페이스 감사

### Outcome

- 신규 문서 `docs/context/reports/PRELAUNCH_ERROR_CODE_AUDIT_V1.md`를 작성한다.
- `tools/teul-cli/src/`, `lang/src/` 전체에서 `E_[A-Z_]+` 패턴의 모든 오류 코드를 grep으로 추출한다(정의 파일:라인 인용 포함, 중복 제거).
- 각 코드를 다음 4개 후보 카테고리 중 하나로 **기계적으로** 분류한다(파일 경로 기준, 판단 아님): `parser.rs`/`lexer.rs`에서 정의 → 파서, `runtime/`에서 정의 → 런타임, `계약`/`contract`/`물림` 관련 이름 포함 → 계약, `AGE_NOT_AVAILABLE` 등 AGE 게이트 관련 → AGE게이트. 애매하면 "미분류"로 남긴다.
- 카테고리 체계 자체가 SSOT 어디에도 명시적으로 고정되어 있지 않다는 점을 문서 서두에 명시한다(이건 이번 배치에서 확인한 사실이지 새 판단이 아니다).

### Verification

- 전체 오류 코드 수와 카테고리별 합계가 일치하는지 확인.
- "미분류" 항목이 있으면 그 개수를 로그에 남긴다(0이어도 됨, 없앨 필요 없음).

## 공통 경계 (절대 준수)

1. `docs/ssot/**` 수정 금지.
2. 예약어 추가, 파서 에러 추가, 오류 코드 신설 등 실제 언어/코드 변경 금지 — 이번 배치는 감사 문서 3건 생성까지만.
3. 새로운 설계 결정 금지 — "이렇게 하면 좋겠다" 문장 대신 사실/표만.
4. G2에서 실행 검증용으로 만든 임시 `.ddn` 파일은 `pack/`에 커밋하지 않는다(재현 커맨드만 문서에 기록).
5. `golden.jsonl`/`contract.detjson` 등 기존 pack 정정 금지.
6. `main` 직접 커밋 금지 — `codex/queue-20260706`에만 커밋한다.
7. push 금지, 네트워크 금지.
8. 판단이 막히면(카테고리 분류 애매 등) "미분류"/"확인 필요"로 남기고 다음으로 넘어간다.

## 진행률 요약 (자기 갱신)

- 트랙 G1: 완료
- 트랙 G2: 완료
- 트랙 G3: 완료

## 실행 로그

(각 트랙 완료 시 `[PLFS-G1]`/`[PLFS-G2]`/`[PLFS-G3]` 태그로 기록)

- `[PLFS-G1]` `docs/context/reports/PRELAUNCH_RESERVED_WORD_AUDIT_V1.md` 작성. SSOT 추출 112건, lexer 추출 33건, 합집합 표 113행. 분류 합계: SSOT-only 80 + lexer-only 1 + 양쪽 일치 32 = 113, 행 수 검증 PASS.
- `[PLFS-G2]` `docs/context/reports/PRELAUNCH_GRAMMAR_SPACE_AUDIT_V1.md` 작성. `#`/`@`/`~` lexer 분기 6종을 근거 라인으로 정리했고, 임시 케이스 16건을 `cargo run --manifest-path tools/teul-cli/Cargo.toml -- run ... --summary-json ...`로 실측. 각 표 행에 `work/prelaunch_freeze_sweep/g2/` 입력/로그 경로를 인용. pack 추가 없음.
- `[PLFS-G3]` `docs/context/reports/PRELAUNCH_ERROR_CODE_AUDIT_V1.md` 작성. `tools/teul-cli/src/`, `lang/src/`에서 오류 코드 869건을 경계 포함 패턴으로 중복 제거했고, 카테고리 합계 869건(파서 42, 런타임 68, 계약 5, AGE게이트 1, 미분류 753) 일치 확인. `docs/ssot/**` 수정 없음.
