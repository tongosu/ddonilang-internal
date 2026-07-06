# PROPOSAL_SETTINGS_SEULGI_EXAMPLE_KEY_UNIFICATION_V1_20260706

## 상태

- 분류: PROPOSAL / OPEN ISSUE / LANG / AI-SURFACE
- 작성: 2026-07-06
- 출처: Q36-4 / `BRIEF_SETTINGS_HEADER_ALIGNMENT_AND_LEGACY_PROPOSAL_DELTA_V1`
- 상태: docs-first. Parser/runtime hard-cut 없음.
- 결정 상태: 미확정. SSOT 오너 결정 필요.

## 문제

`설정.슬기`는 docs-first 예시로만 유지되어야 하지만, 예시 key 표기가 서로 다르다.

| 표기 | 발견 근거 | 의미 |
|---|---|---|
| `두뇌종류` | `SSOT_LANG_v24.12.9.md:7812`, `:7827`; `PROPOSAL_V23_2_SEULGI_INTENT_PACK_AND_DDN_SURFACE_V1_20260409.md:336`, `:353` | 슬기 backend/model family 종류 |
| `두뇌` | `SSOT_LANG_v24.12.9.md:8109`; `tests/toolchain_golden/ai_prompt_lean.txt:10143`, `:10328` | 배움틀/규칙형 등 AI 표면의 짧은 이름 |
| `끼우개` / `정책` | `SSOT_LANG_v24.12.9.md:470-471`; `docs/ssot/pack/edu_ddn_vol3_seulgi_boundary_v1/input.ddn:3-4` | bridge adapter와 policy artifact |
| `지연마디` | `SSOT_LANG_v24.12.9.md:7813`, `:7828`; `docs/ssot/pack/edu_ddn_vol3_seulgi_boundary_v1/input.ddn:4` | 슬기 응답/주입 지연 후보 |

현재 repo-wide `rg` 기준 drift는 0건이 아니다. 사용자가 명시한 범위상 이 커밋은 실제 SSOT/예시 수정이 아니라, drift를 없애기 위한 결정안과 OI 등록까지만 한다.

## 권고안

권고는 계층화다.

```ddn
설정 {
  슬기 {
    두뇌 {
      갈래: #규칙형.
      끼우개: "gaji/seulgi_bridge_v1".
      정책: @"seulgi_policy.json".
    }.
    지연마디: 3.
  }.
}.
```

이유:

- `두뇌종류`와 `두뇌`를 동시에 유지하지 않아도 된다.
- `끼우개`와 `정책`이 무엇의 속성인지 분명해진다.
- `두뇌 { 갈래: ... }`는 `#규칙형`, `#LLM통로`, `#배움틀` 같은 family 값을 한 자리에 모은다.
- parser/runtime으로 승격하지 않아도 docs-first 예시 표면을 정리할 수 있다.

## 대안

| 대안 | 예시 | 장점 | 단점 |
|---|---|---|---|
| A. 단일 key `두뇌` | `두뇌: #규칙형.` | 짧고 교재 친화적 | adapter/policy 속성을 나란히 두면 관계가 흐려짐 |
| B. 기존 `두뇌종류` 유지 | `두뇌종류: #규칙형.` | 기존 C-4 예시와 호환 | `두뇌`와 계속 충돌함 |
| C. 계층화 `두뇌 { 갈래... }` | `두뇌 { 갈래: #규칙형. ... }.` | 속성 묶음이 명확함 | 예시가 조금 길어짐 |

권고: C. 단, 초급 교재에서는 축약 별칭으로 `두뇌: #규칙형.`을 허용할지 별도 결정할 수 있다.

## `지연마디` 소유권 질문

현재 용어표는 `설정.샘`을 "입력원천/주입방식/지연마디 등 입력 메타"로 설명하고, `설정.슬기` 예시는 `지연마디`를 직접 둔다. 두 위치가 같은 의미라면 중복이다.

결정 질문:

| 질문 | 선택지 |
|---|---|
| `지연마디`의 1차 소유 절 | A. `설정.샘`이 모든 외부 주입 지연을 소유 / B. `설정.슬기`가 슬기 응답 지연만 소유 / C. 둘 다 허용하되 의미를 분리 |
| 이름 분리 여부 | A. 둘 다 `지연마디` / B. `샘.지연마디`와 `슬기.응답지연마디`로 분리 |
| `InputSnapshot` ordering과의 관계 | `Sam execution ordering (agent_id, recv_seq)`를 바꾸지 않고 metadata로만 읽을지, scheduling input으로 올릴지 결정 |

권고: `설정.샘.지연마디`는 주입 지연, `설정.슬기.응답지연마디`는 AI 응답 지연으로 분리한다. 이름이 길어지는 단점이 있지만, `InputSnapshot`과 `SeulgiIntent` 경계가 섞이지 않는다.

## OI 초안

```md
### OI-SETTINGS-SEULGI-KEY-UNIFICATION-01

`설정.슬기` docs-first 예시 key를 하나의 표면으로 통일한다.

- 권고 표면: `슬기 { 두뇌 { 갈래: #규칙형. 끼우개: "...". 정책: @"...". }. 지연마디: 3. }.`
- 대안: `두뇌: #규칙형.` 단일 key 또는 `두뇌종류` 유지
- 질문: `지연마디`의 소유권을 `설정.샘`과 `설정.슬기` 중 어디에 둘지, 또는 `응답지연마디`로 분리할지
- 상태: docs-first / parser-runtime hard-cut 금지
```

## rg 검증

사용한 검색:

```text
rg -n "설정\s*\{[\s\S]*슬기|슬기\s*\{|두뇌종류\s*:|두뇌\s*:|끼우개\s*:|정책\s*:|지연마디\s*:|설정\.슬기|설정\.샘" docs/context docs/ssot pack tests tools core solutions --glob '!docs/context/all/DEV_SUMMARY_ARCHIVE_20260706.md' --glob '!**/target/**'
rg -n "두뇌종류|두뇌:|끼우개|정책|지연마디" docs/ssot/ssot/SSOT_LANG_v24.12.9.md docs/context/proposals docs/context/reports pack tests tools core solutions --glob '!docs/context/all/DEV_SUMMARY_ARCHIVE_20260706.md' --glob '!**/target/**'
```

현재 drift:

| key family | 현재 상태 |
|---|---|
| `두뇌종류` | C-4 대표 예시에 존재 |
| `두뇌` | C-5/배움틀 대표 예시에 존재 |
| `끼우개/정책` | v23.2.6 demo와 pack docs-first 예시에 존재 |
| `지연마디` | `설정.샘` 설명과 `설정.슬기` 예시에 걸쳐 있음 |

zero-drift 조건:

1. SSOT 오너가 권고안 또는 대안을 하나 선택한다.
2. SSOT와 docs-first pack 예시를 선택 표면 하나로 맞춘다.
3. `rg -n "두뇌종류|두뇌:|끼우개|정책|지연마디"` 결과에서 선택 표면 밖의 예시 key가 0건이어야 한다.

## DoD 확인

| DoD | 결과 |
|---|---|
| 예시 key drift 수집 | 완료 |
| 통일안 제안 | 계층화 `두뇌 { 갈래/끼우개/정책 }` 권고 |
| `지연마디` 소유권 질문 OI 등재 | 완료 |
| parser/candidate key hard-cut 없음 | 충족 |
| 실제 SSOT/pack 예시 수정 없음 | 사용자 지시대로 수정 없음 |
