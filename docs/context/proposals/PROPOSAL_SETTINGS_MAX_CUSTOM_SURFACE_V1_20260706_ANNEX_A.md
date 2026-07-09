# PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706 — ANNEX A (설정해시 + 시앗묶음, 구현 등급 정교화)

- 작성: 2026-07-09 KST, Claude Code (지시문 16 이행, §2.1/§2.2 두 항목을 한 원 제안서 기준으로 통합)
- 원 제안서: `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md` §2.1, §2.2
- 기존 도구층 확인: `tests/tools/config_digest_proto.py`(Tier A 프로토타입, `--selftest` 보유)와 정합 확인 — 이 ANNEX는 그 프로토타입의 실제 분류 로직을 근거로 삼는다.

**본 문서는 구현 등급 설계이며 SSOT 병합 전 canon 아님.**

---

## Part 1 — 설정해시 (§2.1)

### (a) 정확한 스키마 표

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| `schema` | string | 필수 | - | `"ddn.config_digest.v1"` |
| `digest_algo` | enum(`blake3`) | 필수 | `blake3` | v1은 BLAKE3 고정 |
| `digest` | string | 필수 | - | `blake3:` 접두 hex |
| `included_sections` | array\<string\> | 필수 | `["실행","누리","샘","거울","보개","슬기"]` | 해시 입력에 포함된 절 이름(정본 절 이름 기준) |
| `excluded_sections` | array\<string\> | 필수 | `["문서"]` | 해시에서 제외된 절(순수 메타) — **아래 (b) E1 참조, `이야기`는 재검토 필요** |
| `key_classification_version` | string | 필수 | `config_digest_proto/v2` | 분류 로직 버전(기존 도구의 `CLASSIFIER_VERSION`과 동일 값 사용) |
| `canonical_serialization` | object | 필수 | - | 아래 직렬화 규칙 |
| `canonical_serialization.section_order` | array\<string\> | 필수 | 정본 절 8종 고정 순서(`문서/실행/이야기/누리/샘/거울/보개/슬기` 중 포함분만) | 절 순서는 alias 입력 순서와 무관하게 **고정 canonical 순서**로 정렬 |
| `canonical_serialization.key_order` | enum(`declaration`,`sorted`) | 필수 | `sorted` | 절 내부 key 정렬 — 입력 순서 의존 제거 위해 사전순 권고 |
| `canonical_serialization.float_normalization` | enum(`fixed_decimal`,`raw`) | 필수 | `fixed_decimal` | 부동소수 표기 정규화(예: `1.0`과 `1.00`을 같은 바이트로) |
| `mismatch_policy` | enum(`error`,`override_flag`) | 필수 | `error` | replay 시작 시 불일치 처리 |
| `override_flag_name` | string | 선택 | `--allow-config-digest-mismatch` | `mismatch_policy=override_flag`일 때만 |

### (b) 엣지케이스 표

| # | 케이스 | 기대 동작 | 근거 |
|---|---|---|---|
| E1 | `설정.이야기.들머리`가 결과영향 키로 최종 확정되는 경우 | 현재 `config_digest_proto.py`의 `DOC_SECTIONS = {"문서", "이야기"}`는 `이야기` 전체를 메타로 분류해 해시에서 제외한다. 이는 원 제안서 §2.1의 "권고: 제외 — 순수 메타"가 **`문서`에만 적용된다고 읽었을 때와 어긋난다.** `들머리`가 결과영향으로 확정되면 `이야기`를 `DOC_SECTIONS`에서 빼야 한다. | 지시문 3의 미해결 질문(`설정.이야기.들머리` 결과영향 여부)과 직접 충돌 — **이 ANNEX가 발견한 실제 코드-설계 불일치** |
| E2 | 같은 값을 다른 alias 키로 입력(`seed: 1` vs `시앗: 1`) | 동일 다이제스트 — `KEY_ALIASES` 정규화가 먼저 적용된 후 해시 계산 | `config_digest_proto.py` 기존 `selftest` 케이스와 동일 원칙 |
| E3 | 절 순서만 다르게 입력(`실행 {} 누리 {}` vs `누리 {} 실행 {}`) | 동일 다이제스트 — `canonical_serialization.section_order` 고정 | (a) 표 근거 |
| E4 | `unclassified` 키(신규 키, 아직 분류표에 없음)가 존재 | v1 정책: **포함(보수적으로 result-affecting 취급)** — 미분류를 제외하면 새 키가 조용히 해시 밖으로 새어나가 재현성 구멍이 생김 | "빠짐이 안전보다 낫다"는 이 프로젝트 전체의 결정성 원칙과 일치 |
| E5 | `override_flag_name` 사용 후 실제로 재현 실패 | override는 다이제스트 불일치를 무시할 뿐 재현 실패 자체를 없애지 않음 — override 사용 시 기록층에 `config_digest_override_used: true`를 별도 기록해 감사 가능하게 함 | replay 신뢰성 원칙 |

### (c) 오류 코드 배정안

| 코드 | 배정 근거 |
|---|---|
| `E_CONFIG_DIGEST_MISMATCH` | `mismatch_policy=error`일 때 replay 시작 시 발화. 카테고리: 계약(재현 계약) |
| `E_CONFIG_DIGEST_UNCLASSIFIED_KEY` (신규 후보, 선택) | strict 모드에서 `unclassified` 키 발견 시 경고 대신 오류로 승격하고 싶을 경우. v1 기본은 경고(E4 정책과 별개) |

### (d) pack DoD + golden fixture 스케치

- pack 후보: `settings_config_digest_v1` (신규, `PRE_RELEASE_FREEZE_SWEEP_V1.md`의 pack ID 충돌 검사에 없던 이름 — 충돌 확인 필요).
- golden fixture 스케치:
  - `c01_alias_equivalence`: `seed:1` 입력과 `시앗:1` 입력 → 동일 `digest`.
  - `c02_section_order_invariance`: 절 순서 뒤바꾼 두 입력 → 동일 `digest`.
  - `c03_doc_section_excluded`: `문서.제목`만 바꾼 두 입력 → 동일 `digest`(문서 제외 확인).
  - `c04_result_key_changes_digest`: `실행.마디수`만 바꾼 두 입력 → **다른** `digest`(결과영향 키는 포함 확인).
  - DoD: 4개 케이스 PASS + `config_digest_proto.py --selftest`와 golden 결과 일치.

---

## Part 2 — 시앗묶음 (§2.2)

### (a) 정확한 스키마 표

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|---|---|---|---|---|
| `설정.누리.시앗` | u64 | 필수 | - | 뿌리 시앗(기존 키, 변경 없음) |
| `설정.누리.시앗묶음` | object\<string, 갈래시앗 호출\> | 선택 | 없음(미지정 시 전부 뿌리 시앗 공유) | 스트림 이름 → 유도 함수 |
| `갈래시앗(N)` | 함수 호출, N: u32 | - | - | 도메인 분리 인덱스 |

### 유도 함수 명세

```
스트림_시드(스트림이름, N) = BLAKE3(뿌리시앗의 8바이트 리틀엔디안 직렬화 ∥ 스트림이름의 UTF-8 바이트 ∥ N의 4바이트 리틀엔디안 직렬화)의 앞 8바이트를 u64로 해석
```

- `뿌리시앗 ∥ 스트림이름 ∥ N` 순서 고정(∥ = 바이트 연결).
- `N`은 사용자가 `갈래시앗(N)`에 명시한 정수 — **스트림 이름만으로 유도하지 않는 이유**: 같은 이름의 스트림을 실수로 두 번 선언했을 때 조용히 같은 시드가 되는 것을 막기 위해 명시적 인덱스를 요구한다(아래 (b) E2).

### (b) 엣지케이스 표

| # | 케이스 | 기대 동작 | 근거 |
|---|---|---|---|
| E1 | `시앗묶음` 미지정 | 모든 서브시스템이 `설정.누리.시앗`을 직접 공유(v0 하위 호환 동작 그대로 유지) | §2.2 "미지정 시 뿌리 공유" |
| E2 | 같은 스트림 이름을 두 번 선언(`물리: 갈래시앗(1).` 두 번) | `E_SEED_BAG_DUPLICATE_STREAM` — 조용히 마지막 선언이 이기게 두지 않는다(결정성 침묵 마스킹 금지 원칙과 동일선) | 프로젝트 전역 "조용한 덮어쓰기 금지" 원칙 |
| E3 | 같은 `N`을 두 스트림 이름에 사용(`물리: 갈래시앗(1).` / `슬기: 갈래시앗(1).`) | 허용(경고 없음) — 스트림 이름 자체가 도메인 분리 입력에 포함되므로 다른 시드가 보장됨(이름이 다르면 `N`이 같아도 해시 입력이 다름) | 유도 함수 정의상 안전 |
| E4 | `시앗묶음`에 정의 안 된 서브시스템이 난수를 요청 | 뿌리 시앗 직접 사용으로 폴백(E1과 동일 경로) — 부분 지정을 허용해야 점진 도입 가능 | §2.2 목적("서브시스템 추가/제거가 다른 서브시스템을 흔들지 않음")과 정합 |
| E5 | `주사위씨`가 스트림 이름을 받는 후속 설계(§2.2 "후속") 시점의 하위 호환 | `주사위씨(이름 없음)` = 기존 동작(뿌리 또는 지정 안 된 폴백), `주사위씨(이름: "물리")` = 해당 스트림 시드 사용 — **이번 annex 범위 밖, 후속 설계로 남김** | §2.2 원문 "후속 설계"로 명시된 범위 |

### (c) 오류 코드 배정안

| 코드 | 배정 근거 |
|---|---|
| `E_SEED_BAG_DUPLICATE_STREAM` | E2. 카테고리: 런타임(초기화 단계) |
| `E_SEED_BAG_INVALID_INDEX` (신규 후보) | `갈래시앗(N)`에 음수/비정수 등 잘못된 `N` 입력 시 |

### (d) pack DoD + golden fixture 스케치

- pack 후보: `nuri_seed_bag_derivation_v1` (신규 — `PRE_RELEASE_FREEZE_SWEEP_V1.md` pack ID 충돌 검사에 없던 이름, 충돌 확인 필요).
- golden fixture 스케치:
  - `c01_no_seed_bag_shares_root`: `시앗묶음` 미지정 → 물리/슬기 스트림 요청 시 둘 다 뿌리 시앗과 동일한 값 계열.
  - `c02_named_streams_diverge`: `물리: 갈래시앗(1)`, `슬기: 갈래시앗(2)` → 두 스트림의 난수열이 서로 다름(회귀: 슬기 스트림 추가/제거해도 물리 스트림 값 불변).
  - `c03_duplicate_stream_fatal`: 같은 이름 두 번 선언 → `E_SEED_BAG_DUPLICATE_STREAM`.
  - DoD: 3개 케이스 PASS. `c02`가 이 기능의 핵심 가치(독립성)를 직접 증명하는 케이스이므로 최우선.

## 남은 결정 질문 (≤3, Part 1+2 통합)

1. **`설정.이야기` 전체를 해시 제외로 둘지, `들머리`만 분리해 포함할지** — 지시문 3의 `들머리` 결과영향 여부 결정에 종속. (b) E1에서 발견한 실제 코드-설계 불일치이므로 우선순위 높음.
2. **`unclassified` 키의 v1 기본 정책** — 포함(보수적, 이 ANNEX 권고) vs 제외(느슨) vs 오류(엄격). 권고: 포함.
3. **시앗묶음 pack ID(`nuri_seed_bag_derivation_v1`)와 설정해시 pack ID(`settings_config_digest_v1`)가 `PRE_RELEASE_FREEZE_SWEEP_V1.md`의 53개 충돌 검사 목록에 없었음** — 병합 전 재검사 필요(신규 제안이므로 그 시점 목록에 없는 게 정상이지만, 실제 pack 생성 직전 재확인 필수).
