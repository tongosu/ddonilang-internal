# 20260708_codex_dayrun_g1_freeze_sweep

- 작업자: Codex
- 기준: DAYRUN 2026-07-07 G1 / 지시문 12
- 경계: `docs/ssot/**` 직접 수정 없음

## 결과 요약

G1 완료 (`닫힘-문서`).

- `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md` 확인 및 유지.
- `docs/context/proposals/OI_CANDIDATE_BUNDLE_20260706.md` 확인 및 유지.
- `docs/context/proposals/OI_CANDIDATES_20260706_BUNDLE.md` 추가.
- `docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md` 추가/현행 실측값으로 정리.
- `docs/reports/audit/INDEX.md`, `docs/context/all/DEV_SUMMARY.md`, `docs/status/PROJECT_STATUS.md`, `docs/status/CHANGELOG.md` 갱신.

## 실측 요약

- 예약어 후보 26개를 정적 스윕했다.
- SSOT 본문에서 0회인 주요 후보: `여러속마디`, `고정박자`, `사건박자`, `시앗묶음`, `설정해시`, `검산`, `관찰범위`.
- 문법 공간: `~분포` 0회, `~이름` 1회, `#모두필요` 120회, `#빈칸채움` 94회.
- 제품/pack/test 경로 `E_*` unique token: 3,805개. DAYRUN 재현 스윕은 3,749개, 테스트/러너성 접두를 거칠게 제외하면 2,782개.
- `schema_version` 흔적: 200줄.
- pack 후보 ID는 초기 부분 스윕 39개 중 기존 존재 2개, SSOT patch bundle 최종 표 53개 중 기존 존재 4개.

## 질문 큐

1. `설정.누리`와 `설정.실행`의 경계를 어디까지 나눌지.
2. `설정.이야기` 절을 지금 예약할지, `말거리`만 예약할지.
3. `설정해시` 입력에서 문서/보기 metadata를 제외하는 원칙을 확정할지.
4. `시앗묶음`, `가설`, `검산`, `단위 정의`, `말거리`, `~이름(...)`을 예약어/문법 공간으로 선점할지.
5. `E_*` namespace를 parser/runtime/contract/AGE gate 범주로 고정할지.
6. 공개 schema별 version 협상 규칙을 reject/read_compat/upgrade/ignore 중 하나로 표준화할지.

## 발견한 문제

- 개별 후보어를 매번 전체 검색하는 방식은 저장소 규모에서 느렸다. 이후 G6 reserved-word lint는 단일 패스 검색으로 만들어야 한다.
- `E_*` 검색은 테스트/러너/문서성 토큰이 많이 섞인다. 정식 오류 코드 registry가 없으면 실측이 계속 부정확하다.
- `schema_version`은 여러 경로에서 쓰이지만 공개 schema별 호환 정책을 한곳에서 읽기 어렵다.

## 다음 날 추천 착수점

1. reserved-word lint 도구화.
2. `~분포`, `~이름(...)`, 미사용 `#/@/~` 조합의 parser negative test.
3. `E_*` namespace registry 초안.
4. 공개 schema version policy 표.

## 검증

- 예약어 후보/문법 공간/E-code/schema/pack ID 정적 스윕 수행.
- `docs/ssot/**` 직접 수정 없음.
