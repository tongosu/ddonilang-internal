# 2026-07-09 — Claude Code — 지시문 7/13/16 이행

## 배경

또니가 fable(외부 AI)이 준 15/16개 지시문을 전부 나열해 붙여넣었고, 저장소 실측 대조 결과 Codex 담당분(1~12, 15)은 사실상 완료, 나머지 미착수 3건(7, 13, 16) 중 13·16은 원래 Claude Code 담당으로 지정된 항목이었다. "셋 다 해줘" 요청으로 이번 세션에서 처리.

## 지시문 7 — [Codex 담당] 언어 정체성 경계 감사

Claude 본업(설계/브리프)만 수행: `docs/context/briefs/BRIEF_DIRECTIVE7_LANGUAGE_IDENTITY_BOUNDARY_AUDIT_V1_20260709.md` 작성·커밋. 실행은 Codex가 `codex/queue-20260706`에서 수행할 대상.

## 지시문 13 — SSOT 병합 준비물 감사

`docs/reports/audit/SSOT_MERGE_AUDIT_20260706.md` 작성. 5개 체크리스트(경계/주장등급/용어drift/교차참조/SSOT권위순서) 중 4개 PASS, 교차참조 PARTIAL.

**신규 발견 2건**:
1. `OI_CANDIDATE_BUNDLE_20260706.md`(07-07)와 `OI_CANDIDATES_20260706_BUNDLE.md`(07-08) 두 OI 번들이 같은 주제를 다른 ID/범위로 중복 등록 — 병합 전 통합 필요.
2. `SSOT_PATCH_DRAFT_20260706_BUNDLE.md:32`가 인용한 `SSOT_PLATFORM_v24.12.9.md:1825`를 직접 열어보니 주제가 전혀 다름(InjectComponent 화이트리스트 vs accepted_madi 실행 순서) — SSOT가 git 미추적 살아있는 문서라 인용 시점 이후 line 번호가 밀린 것으로 판단. 병합 전 전체 인용 재확인 권고.

병합 보류 사유는 없음(경계/주장/용어 전부 PASS).

## 지시문 16 — 설계안 정교화 (ANNEX 6건)

원래 6개 대상 중 2개(설정해시/시앗묶음)가 같은 원 제안서(`PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706`)의 다른 절이라 "제안서마다 ANNEX_A" 원칙에 따라 1개 파일로 통합 — 실제로는 5개 파일 생성.

1. `PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706_ANNEX_A.md` — 위상 실행 레코드/write-conflict 스키마, W1~W3 DDN 예제 3건, OQ-4 옵션별 결과표.
2. `PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706_ANNEX_A.md` — 설정해시 + 시앗묶음 통합. **기존 `config_digest_proto.py`의 `DOC_SECTIONS={"문서","이야기"}`가 "이야기" 전체를 메타로 분류해 해시 제외하고 있는데, 이는 지시문 3의 미해결 질문(`들머리` 결과영향 여부)과 충돌함을 발견** — 실제 코드-설계 불일치.
3. `PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707_ANNEX_A.md` — v0.1/v0.2 필드 매트릭스, roundtrip 6케이스. **원 제안서가 요구한 pack `nurigym_step_record_v02_roundtrip_v1`이 실제로는 안 만들어지고, 범위가 다른 `nurigym_step_record_v02_consumer_g6_v1`(consumer 층 프로토타입)만 존재함을 발견** — pack 이름/역할 간극.
4. `PROPOSAL_CLOSED_BETA_AI_PROTOCOL_V1_20260706_ANNEX_A.md` — T4 오류 fixture 3건을 `cargo run -- check/run`으로 직접 재실행해 `expected_diagnostics.md`와 완전 일치 확인(신규 fixture 제작 없이 기존 것을 정식 스키마로 승격).
5. `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706_ANNEX_A_MADANG_TRACK.md` — **`seamgrim.scene.v0`를 직접 열어보니 `#자막`/`#해설`/`강조하기`가 이미 실제 lesson fixture(`lesson_econ_01`, `lesson_phys_01`)에 존재함을 확인, "확장 vs 병렬" 질문에 확장으로 판정.**

## 검증

- 모든 ANNEX는 근거를 실제 파일(제안서, 기존 pack, 실행 결과)에서 인용했고, 최소 1건 이상은 직접 재실행/직접 열람으로 검증했다.
- `docs/ssot/**` 수정 없음. parser/runtime 변경 없음.

## 남은 것

- 이번에 발견한 3건의 실제 불일치(OI 번들 중복, SSOT 인용 drift, config_digest 이야기절 제외, step_record pack 이름 간극)는 다음 병합/개발 배치에서 해소 대상으로 남겨둔다 — 이 세션에서 직접 고치지 않았다(설계 정교화 범위이므로).
