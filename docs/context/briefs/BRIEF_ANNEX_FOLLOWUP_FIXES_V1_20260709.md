# BRIEF: 지시문 13/16 감사에서 발견한 불일치 3건 정리

작성: 2026-07-09 KST
근거: `docs/reports/audit/SSOT_MERGE_AUDIT_20260706.md`(지시문 13), 지시문 16 ANNEX 5건(특히 `PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706_ANNEX_A.md`, `PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707_ANNEX_A.md`)
성격: 실측/정리 위주. 새 설계 결정 없음(각 트랙 안에 "결정 필요"로 남긴 것은 그대로 둔다).

## 트랙 I — OI 번들 2건 통합

### 배경

`docs/context/proposals/OI_CANDIDATE_BUNDLE_20260706.md`(2026-07-07)와 `docs/context/proposals/OI_CANDIDATES_20260706_BUNDLE.md`(2026-07-08)가 같은 주제를 다른 ID/문구로 중복 등록하고 있다(예: `OI-SETTINGS-NURI-KEYSET-01`이 두 문서에서 질문 범위 자체가 다름). `SSOT_MERGE_AUDIT_20260706.md` §4-1에서 발견.

### Outcome

- `OI_CANDIDATES_20260706_BUNDLE.md`(07-08판, 더 최신이고 카테고리 분류·우선순위까지 있음)를 기준본으로 삼는다.
- `OI_CANDIDATE_BUNDLE_20260706.md`(07-07판)에만 있고 07-08판에 없는 항목을 찾아 07-08판에 추가한다(예: `OI-SETTINGS-STORY-ENTRY-KEY-01`, `OI-BOGAE-STANDARD-PACK-NAMING-01` 등 — 직접 대조해서 확인).
- 같은 주제, 다른 ID로 중복된 항목(예: OQ2 계열)은 하나의 ID로 통일하고 두 문서의 질문 문구 차이를 하나로 합친다.
- 통합 완료 후 `OI_CANDIDATE_BUNDLE_20260706.md` 맨 위에 "이 문서는 `OI_CANDIDATES_20260706_BUNDLE.md`로 통합됨(2026-07-09)"이라는 리다이렉트 각주만 남기고 원 내용은 보존한다(삭제 금지).

### Verification

- 두 문서의 OI 항목 합집합이 통합본에 전부 반영됐는지 ID별로 대조표를 만들어 실행 로그에 남긴다.
- 중복 ID 0건 확인.

## 트랙 J — SSOT 인용 line 번호 재확인

### 배경

`SSOT_PATCH_DRAFT_20260706_BUNDLE.md`가 인용한 `docs/ssot/ssot/SSOT_PLATFORM_v24.12.9.md:1825`를 직접 열어보니 주제가 전혀 다른 내용(InjectComponent 화이트리스트)이었다. SSOT 파일은 git 미추적 상태로 계속 갱신되므로 line 번호가 밀린 것으로 보인다. `SSOT_MERGE_AUDIT_20260706.md` §4-2에서 발견.

### Outcome

- `SSOT_PATCH_DRAFT_20260706_BUNDLE.md`의 "결정 후보"/"후보"/"질문" 3개 표에 있는 모든 SSOT 인용(파일:line 형태) 전부를 현재 SSOT 파일 상태 기준으로 재확인한다.
- 인용이 틀렸으면(내용이 안 맞으면) 올바른 현재 line 번호로 수정한다. 못 찾으면(그 내용이 SSOT에서 아예 사라졌거나 다른 곳으로 옮겨졌으면) "재확인 불가 — 근거 문장이 현재 SSOT에서 확인 안 됨"이라고 표기한다.
- 문장 내용 자체(제안 내용)는 바꾸지 않는다 — line 번호 정합성만 고친다.

### Verification

- 전체 인용 개수와 재확인 완료 개수가 일치하는지 로그에 남긴다.
- "재확인 불가" 판정이 나온 항목이 있으면 몇 건인지, 어떤 항목인지 명시한다.

## 트랙 K — `nurigym_step_record_v02_roundtrip_v1` pack 실제 생성

### 배경

원 제안서(`PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707.md` §4)가 요구한 pack이 실제로는 안 만들어졌다 — 대신 범위가 다른 `pack/nurigym_step_record_v02_consumer_g6_v1/`(consumer 층 프로토타입)만 존재한다. 이 pack은 SSOT 병합이 필요 없는 wire-schema 증빙 pack이므로(신규 문법 0건, 기존 `nurigym_shared_sync_action_pipeline_v1`의 필드를 그대로 씀) Tier A로 분류한다.

### Outcome

- `pack/nurigym_step_record_v02_roundtrip_v1/`를 생성한다. `docs/context/proposals/PROPOSAL_NURIGYM_STEP_RECORD_V02_COMPAT_AND_ROUNDTRIP_V1_20260707_ANNEX_A.md` §(d)의 6개 케이스를 그대로 golden fixture로 만든다:
  - `c01_valid`, `c02_noop_missing`, `c03_clip`, `c04_reject`, `c05_shared_merge`, `c06_v01_backward_read`.
- `c06_v01_backward_read`는 v0.1 포맷(신규 필드 없음) 파일을 v0.2 consumer 로직으로 읽어 ANNEX §(b) E1(3필드 없어도 `applied_action`만으로 최소 재생) 동작을 검증한다.
- evidence tier는 `runner_golden`으로 표기, closure 주장 없음.
- `tests/run_nurigym_step_record_v02_roundtrip_pack_check.py` 형태의 checker 작성.

### Verification

- 6케이스 전부 PASS.
- 기존 `pack/nurigym_step_record_v02_consumer_g6_v1`와 필드 정의(이름/타입)가 서로 어긋나지 않는지 교차 확인.
- `cargo test --manifest-path tools/teul-cli/Cargo.toml` PASS 유지.

## 공통 경계 (절대 준수)

1. `docs/ssot/**` 수정 금지.
2. 트랙 I/J: 문서 내용의 실질(제안/질문 내용)을 새로 판단하지 않는다 — 통합/재확인까지만.
3. 트랙 K: 신규 문법 0건, `docs/ssot/**` 수정 0건, closure 주장 없음(`runner_golden`까지만).
4. `golden.jsonl`/`contract.detjson` 등 기존 pack 정정 금지(트랙 K는 신규 pack 생성이라 해당 없음).
5. `main` 직접 커밋 금지 — `codex/queue-20260706`에만 커밋. 트랙별 별도 커밋.
6. push 금지, 네트워크 금지.

## 실행 로그

(트랙 완료 시 `[AFF-I]`/`[AFF-J]`/`[AFF-K]` 태그로 기록)

- [AFF-I] 2026-07-09 KST: `OI_CANDIDATES_20260706_BUNDLE.md`를 기준본으로 유지하고, 07-07판 16개 항목을 통합 ID 16개에 전부 반영했다. 같은 주제의 다른 ID는 최신 ID로 통합했으며, `OI-SETTINGS-SEULGI-KEY-DRIFT-01`와 `OI-BOGAE-STANDARD-PACK-NAMING-01`는 07-08판에 새 행으로 추가했다. `OI_CANDIDATE_BUNDLE_20260706.md` 상단에는 2026-07-09 통합 각주만 추가하고 원문은 보존했다. 검증: 통합 대조표 추가, 중복 ID 0건 확인 예정.
- [AFF-J] 2026-07-09 KST: `SSOT_PATCH_DRAFT_20260706_BUNDLE.md`의 `결정 후보` / `후보` / `질문` 표에서 SSOT `file:line` 인용 3건을 재확인했다. 3건 모두 현재 line으로 갱신했고, 재확인 불가 0건이다. 제안 문장 내용은 변경하지 않았다.
- [AFF-K] 2026-07-09 KST: `pack/nurigym_step_record_v02_roundtrip_v1/`를 새로 생성하고 ANNEX A §(d)의 6개 케이스(`c01_valid`, `c02_noop_missing`, `c03_clip`, `c04_reject`, `c05_shared_merge`, `c06_v01_backward_read`)를 golden fixture로 고정했다. evidence tier는 `runner_golden`, closure claim은 `no`로 유지했다. 검증: `python tests/run_nurigym_step_record_v02_roundtrip_pack_check.py` PASS(6 cases, field_crosscheck PASS), `cargo test --manifest-path tools/teul-cli/Cargo.toml` PASS(1109 passed).
