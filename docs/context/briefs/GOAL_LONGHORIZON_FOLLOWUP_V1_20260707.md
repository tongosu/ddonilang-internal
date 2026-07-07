# GOAL: LONGHORIZON 후속 정리 — 결정 대기 통합 / gaji 적용 / 통합후보 심사표

작성: 2026-07-07 KST
선행 배치: `docs/context/roadmap/GOAL_LONG_HORIZON_AUTONOMOUS_BACKLOG_V1_20260706.md` (트랙 A 47/47, B 360/360, C 3/3 완료, `main` 병합 완료: `4cdd187`)

## 배경

직전 GOAL-LONGHORIZON 배치는 3개 트랙을 완료했지만, 결과물 자체가 다음 판단을 위한 원재료(raw material)다:

- 트랙 A: 47개 리포트 전부에 `## 결정 필요` 절이 있고, 흩어져 있어 사용자/Claude가 한눈에 우선순위를 매기기 어렵다.
- 트랙 B: 360행 중 34행(삭제 후보 32 + 보류 해소 후보 2)이 실제 조치가 필요한데, 조치는 아직 없다.
- 트랙 C: 3건의 `gaji.toml` 초안은 Claude가 근거를 확인했고 실제 파일 생성만 남았다.

이번 배치는 새로운 설계 결정을 만들지 않는다. **정리, 적용, 심사표 작성까지만** 한다. 실제 설계 판단(예: MathIR 고정 위치, `끝내` builtin 여부)은 이번에도 다루지 않는다 — 그건 사용자/Claude 몫이다.

## 트랙 D — Track A 결정 대기 항목 통합

### Outcome

- 신규 문서 `docs/context/reports/MUST_GAP_DECISION_QUEUE_V1.md`를 작성한다.
- `docs/context/reports/MUST_GAP_DEEPDIVE_A01_*.md` ~ `A47_*.md` 47개 파일 전부에서 `## 결정 필요` 절의 불릿을 그대로(의역/요약 금지, 원문 인용) 추출한다.
- 다음 주제 그룹으로만 재편성한다(새 그룹 만들지 말고 안 맞으면 "기타"에 넣는다):
  1. 이름 충돌/오류코드 명명 (A01, A02, A24, A31 등 관련 항목)
  2. 파이프/해서 표면 (A04~A08)
  3. match 분기 (A09~A15)
  4. MathIR/증명 표현 (A16)
  5. 누리 query 표면 (A17, A18)
  6. 늘지켜보고/불변 훅 (A19)
  7. nuance 결합 ($ 토큰류) (A20~A22)
  8. AI Gym 표면 (A23)
  9. josa/jamo 예약어 (A24, A25, A31)
  10. 용어/버전 표기 정책 (A27~A29)
  11. ambiguity/LSP quickfix (A32, A43)
  12. stem/multi-dispatch (A33~A47 중 나머지)
- 각 항목에 원본 리포트 경로(`docs/context/reports/MUST_GAP_DEEPDIVE_AXX_*.md`)를 링크로 남긴다.
- `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER*_V1.md`에 이미 있는 top-10 severity 순위와 겹치는 항목이 있으면 "기존 top-10 여부" 열에 표시만 한다(순위를 새로 매기지 않는다).
- 문서 맨 위에 "이 문서는 결정하지 않는다. 사용자/Claude가 다음에 결정할 원재료 목록이다" 라고 명시한다.

### Verification

- `grep -c "^- 원본:" docs/context/reports/MUST_GAP_DECISION_QUEUE_V1.md` (또는 유사 anchor)로 47개 항목 전부가 정확히 1회씩 나오는지 확인하고 결과를 로그에 남긴다.
- 47개 원본 파일 각각의 `## 결정 필요` 불릿 개수 합계와 신규 문서의 총 불릿 수가 일치하는지 확인.

## 트랙 E — gaji 메타데이터 실제 적용

### Outcome

- `docs/context/proposals/PROPOSAL_GAJI_MISSING_METADATA_V1_20260706.md`의 3개 초안은 Claude가 근거(README/exports.ddn 인용)를 확인했고 그대로 승인한다.
- 초안 내용 그대로 다음 3개 파일을 실제로 생성한다:
  - `gaji/std_grid/gaji.toml`
  - `gaji/std_input_map/gaji.toml`
  - `gaji/std_physics_1d/gaji.toml`
- 제안서 본문의 TOML 블록을 한 글자도 바꾸지 않고 그대로 옮긴다. 값(`ssot_requires` 등)을 임의로 바꾸지 않는다.

### Verification

- 3개 파일 모두 기존 `gaji/std_math/gaji.toml` 등과 동일한 TOML 문법으로 파싱 가능한지 확인(예: `python -c "import tomllib,sys; tomllib.load(open(sys.argv[1],'rb'))"` 류 또는 저장소에 이미 있는 gaji 감사 커맨드 사용).
- 기존 가지 레지스트리 스캐너(`tools/teul-cli/src/cli/gaji.rs`의 관련 커맨드, 예: `gaji list`/`gaji audit` 등 이미 존재하는 커맨드)로 3개 패키지가 metadata 보유 상태로 인식되는지 확인.
- `cargo test --manifest-path tools/teul-cli/Cargo.toml` PASS 유지(회귀 없음).

## 트랙 F — 통합후보 34건 조치 심사표

### Outcome

- 신규 문서 `docs/context/reports/CONSOLIDATION_ACTION_REVIEW_V1.md`를 작성한다.
- `docs/context/reports/CONSOLIDATION_CANDIDATE_REVERIFY_V1.md`에서 판정이 `재분류 필요(삭제 후보)`인 32행과 `재분류 필요(보류 해소 후보)`인 2행만 뽑는다.
- 각 행에 대해: 파일 경로, 최초 커밋(git_add), active_refs 근거(원본 그대로), 제안 액션(삭제 후보는 "삭제 심사 대상" + 왜 안전한지 근거, 보류 해소 후보는 "보류 해제/승격 검토" + PASS 근거)을 표로 정리한다.
- 문서 맨 위에 "이 문서는 삭제/보류해제를 실행하지 않는다. 사용자 승인 후 별도 배치에서 실행한다"라고 명시한다.

### Verification

- 신규 문서의 행 수가 정확히 34행(32+2)인지 확인.
- 원본 리포트의 32/2 집계와 신규 문서의 행 수가 일치하는지 로그에 남긴다.

## 공통 경계 (절대 준수)

1. `docs/ssot/**` 수정 금지.
2. 트랙 F: 실제 파일 삭제 금지, 보류 상태 변경 반영 금지 — 심사표 작성까지만. `tests/`나 `pack/`의 실제 파일을 지우거나 옮기지 않는다.
3. 트랙 D: 새로운 설계 결정 금지 — 원문 인용 + 재편성 + 기존 순위 표시까지만. "이렇게 결정하면 좋겠다" 같은 새 판단 문장을 넣지 않는다.
4. 트랙 E 외에는 실제 파일 생성 금지(트랙 D/F는 리포트 문서만 생성).
5. `golden.jsonl`/`contract.detjson` 등 기존 pack 정정 금지.
6. 언어 커널(파서/런타임) 구현 금지.
7. `main` 직접 커밋 금지 — `codex/queue-20260706`에만 커밋한다.
8. push 금지, 네트워크 금지.
9. 판단이 진짜로 막히면(트랙 D 그룹 분류가 애매한 항목 등) 억지로 넣지 말고 "기타" 또는 별도 표시 후 다음으로 넘어간다.

## 진행률 요약 (자기 갱신)

- 트랙 D: 47/47 항목 통합
- 트랙 E: 3/3 파일 생성
- 트랙 F: 34/34 행 심사표

## 실행 로그

(각 트랙 완료 시 `[LHF-D]`/`[LHF-E]`/`[LHF-F]` 태그로 기록)
- [LHF-D] Track A 결정 대기 항목 47개를 `docs/context/reports/MUST_GAP_DECISION_QUEUE_V1.md`로 통합. 검증: `rg -c "^- 원본:" docs/context/reports/MUST_GAP_DECISION_QUEUE_V1.md` = 47, 원본 결정 불릿 합계 81 / 신규 문서 원문 불릿 81 일치.
- [LHF-E] proposal의 TOML 블록 그대로 `gaji/std_grid/gaji.toml`, `gaji/std_input_map/gaji.toml`, `gaji/std_physics_1d/gaji.toml` 3개 생성. 검증: proposal block exact_match=true 3건, `python -c "import tomllib,sys; ..."` PASS, `cargo run --manifest-path tools/teul-cli/Cargo.toml -- gaji lock --root . --out build/gaji_metadata_followup/ddn.lock` 결과 package_count=16 및 새 3개 id present, `cargo test --manifest-path tools/teul-cli/Cargo.toml` PASS (1109 passed).
- [LHF-F] `docs/context/reports/CONSOLIDATION_CANDIDATE_REVERIFY_V1.md`에서 삭제 후보 32행과 보류 해소 후보 2행만 추출해 `docs/context/reports/CONSOLIDATION_ACTION_REVIEW_V1.md` 34행 심사표로 정리. 검증: 신규 심사표 행 34, 원본 집계 삭제 후보 32 / 보류 해소 후보 2 / 합계 34, 삭제 후보 중 `NO_MATCH(tests/tools/solutions)` 누락 0.
