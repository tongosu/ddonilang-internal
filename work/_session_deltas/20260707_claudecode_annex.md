# 20260707 Claude Code — 지시문 16 ANNEX 세션 기록

(실제 작업일: 2026-07-09. 지시문 16 정본 지정 경로 `work/_session_deltas/20260707_claudecode_annex.md`에 맞춰 사후 기록.)

## 산출 6건 경로

원래 6개 대상 중 2/3번(설정해시, 시앗묶음)이 같은 원 제안서(`PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706`)의 서로 다른 절(§2.1, §2.2)이라, "제안서마다 ANNEX_A 1건" 원칙에 따라 하나의 파일로 통합했다. 따라서 실제 산출은 5개 파일이다.

1. `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706_ANNEX_A.md` — 큰마디 위상표(P0~P7 상태기계, 훅 4가족 배치 결정표, OQ-4 옵션별 결과 예시 3건, W1~W3 DDN 예제).
2. `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706_ANNEX_A.md` — 설정해시(§2.1) + 시앗묶음(§2.2) 통합.
3. `docs/context/proposals/PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707_ANNEX_A.md` — step_record v0.2.
4. `docs/context/proposals/PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706_ANNEX_A.md` — 베타 T4 오류 fixture 명세.
5. `docs/context/proposals/PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706_ANNEX_A_MADANG_TRACK.md` — 보개마당 트랙 v1.

각 문서 말미에 "본 문서는 구현 등급 설계이며 SSOT 병합 전 canon 아님"을 명기했다.

## 남은 질문 총목록 (우선순위순)

1. **(높음, ANNEX 2)** `config_digest_proto.py`의 `DOC_SECTIONS = {"문서", "이야기"}`가 `이야기` 절 전체를 해시 제외 대상으로 처리하는데, 지시문 3의 미해결 질문(`설정.이야기.들머리`가 결과영향 키인지 순수 메타인지)과 직접 충돌한다. `들머리`가 결과영향으로 확정되면 `이야기`를 제외 목록에서 빼야 한다.
2. **(중간, ANNEX 1)** OQ-2(세움/매마디 순환 의존 처리 — 정적 분석 vs 런타임 감지), OQ-4((N마디)마다 판정 시점 — 3옵션 중 채택, 권고는 옵션 A) 최종 채택 필요.
3. **(중간, ANNEX 1)** §2.2 옵션(다)(`보탬` 결정적 병합 opt-in)을 합 연산만 허용할지 최댓값/최솟값 등도 포함할지.
4. **(중간, ANNEX 3)** step_record v0.2 pack 명명 정리 — 원 제안서가 요구한 `nurigym_step_record_v02_roundtrip_v1`은 미생성, 대신 범위가 다른 `nurigym_step_record_v02_consumer_g6_v1`(consumer 층)만 존재. 통합할지 역할 분리 유지할지.
5. **(낮음, ANNEX 5)** 보개마당 트랙의 하이라이트 참조 필드명 통일(`target.ref` vs 기존 `args.토큰`), 강조 표현 방식 통일(`target.type=#강조` 단독 vs 기존 `#해설+강조하기` 조합).
6. **(낮음, ANNEX 4)** 베타 friction log와 `friction_axis` 필드 연동 형식은 Round 0 실제 실행 시 결정.

## 발견한 기존 문서/코드 불일치

- **config_digest_proto.py ↔ 지시문 3 미결 질문 충돌**(위 1번과 동일 — 실제 코드가 이미 특정 방향으로 결정을 내려버렸는데, 그 결정이 SSOT 미결 사안과 모순됨).
- **step_record v0.2 pack 이름/역할 간극**(위 4번과 동일 — 제안서가 지정한 pack ID가 실제로는 다른 이름의 다른 범위 pack으로 대체되어 존재).
- **보개마당 트랙**: 제안서는 "새 스키마가 필요한가"를 물었지만, 실제로는 기존 `seamgrim.scene.v0`(실사용 중, `lesson_econ_01`/`lesson_phys_01` fixture에 `#자막`/`#해설`/`강조하기`가 이미 존재)의 부분집합을 정식 계약으로 명시화하는 문제로 재정의됨 — "확장"으로 판정.

## 검증

- 5개 ANNEX 모두 원 제안서/기존 pack/실행 결과에서 근거를 인용했다.
- 최소 3건은 직접 재실행 또는 직접 코드 열람으로 검증했다(베타 T4 fixture 3종 CLI 재실행, `seamgrim.scene.v0` fixture 직접 열람, `config_digest_proto.py` 소스 직접 추적).
- `docs/ssot/**` 수정 없음, parser/runtime 코드 수정 없음.
- `git status` 의도하지 않은 변경 없음(ANNEX 5개 + 이 세션 델타 외 변경 없음).

## 완료 상태

6건 요청 중 5개 파일로 전부 완료(2건 통합). 미완 항목 없음.
