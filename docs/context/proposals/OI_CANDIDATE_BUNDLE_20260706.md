# OI_CANDIDATE_BUNDLE_20260706

- 작성: 2026-07-07 KST, Codex
- 성격: 2026-07-06 논의에서 나온 OI 후보 일괄 초안.
- 경계: 이 문서는 결정하지 않는다. SSOT 오너가 `SSOT_OPEN_ISSUES_v24.12.9.md` 반영 여부와 문구를 결정한다.

## 후보 목록

| OI 후보 ID | 상태 | 질문 / 추적 내용 | 근거 |
|---|---|---|---|
| `OI-SETTINGS-NURI-KEYSET-01` | OPEN 후보 | `설정.누리` v1 key set을 `시앗/누리갈래/환경ID/공간갈래/첫상태참조/규칙묶음` 중 어디까지로 둘지 결정한다. `누리갈래`와 `설정.실행.차림새` 중복 여부를 함께 판정한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:52`, `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706.md:82` |
| `OI-SETTINGS-STORY-ENTRY-KEY-01` | OPEN 후보 | `설정.이야기.들머리`를 진입점 key 후보로 둘지, 결과영향 key인지 순수 메타인지 판정한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:56` |
| `OI-SETTINGS-SEULGI-KEY-DRIFT-01` | OPEN 후보 | `두뇌종류/두뇌/끼우개/정책` 예시 drift를 `두뇌` 단일화 또는 `두뇌 { 갈래/끼우개/정책 }` 계층화 중 하나로 정리한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:69` |
| `OI-SEULGI-LATENCY-OWNERSHIP-01` | OPEN 후보 | `지연마디` 소유권을 `설정.슬기`, `설정.샘`, `설정.실행` 중 어디에 둘지 결정한다. | `docs/context/proposals/PROPOSAL_NURI_MADI_TASK_SCHEDULING_AND_CONFLICT_CONTRACT_V1_20260706.md:224` |
| `OI-NURI-MADI-PHASE-OQ1-ORDER-01` | OPEN 후보 | 같은 큰마디 안 임자 실행 순서를 파일 선언 순서로 볼지, `agent_id` 사전순으로 볼지 결정한다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:59` |
| `OI-NURI-MADI-PHASE-OQ2-SEUM-01` | OPEN 후보 | 세움과 매마디 상호 갱신을 fixpoint 반복 없이 1회 평가로 제한할지, 순환 의존을 정적/실행 오류로 볼지 결정한다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:60` |
| `OI-NURI-MADI-PHASE-OQ3-PREPROCESS-01` | OPEN 후보 | 큰마디 P2 전처리를 샘 소속으로 볼지 이야기 소속으로 볼지 결정한다. 어느 쪽이든 raw 봉인과 결정적 재계산 불변식은 유지한다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:61` |
| `OI-NURI-MADI-PHASE-OQ4-EVERY-N-01` | OPEN 후보 | `(N마디)마다` 판정 시점을 P3 내부 어느 위치로 둘지 결정한다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:62` |
| `OI-NURI-RESET-REAPPLY-OQR1-01` | OPEN 후보 | `누리다시`가 `설정.누리`만 재읽는지, `설정.실행`까지 재읽는지 결정한다. 권고 후보는 누리 절만 재읽고 실행 정책 변경은 `모두다시`를 요구하는 방식이다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:123` |
| `OI-NURI-MERGE-ACTIONCOLLECT-NAMING-01` | OPEN 후보 | `합치기갈래` 신설 대신 기존 `행동모음갈래` 값 확장으로 처리할지 결정한다. 후보 값은 `차례모음/보탬모음/앞선모음/다수결모음/자리모음`이다. | `docs/context/proposals/PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:130` |
| `OI-SETTINGS-RESULT-AFFECTING-KEYS-01` | OPEN 후보 | `설정 {}` key를 결과영향 key와 순수 메타/view-only key로 나누는 기계 판독 분류표 후보를 만든다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:172` |
| `OI-BOGAE-DUAL-SELECTION-PATH-01` | OPEN 후보 | 런타임 대입식 `보개종류 <- ...` 경로와 `설정.보개` 선언 경로의 관계를 compat+lint 또는 선언 경로 이관 중 하나로 결정한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:173` |
| `OI-SETTINGS-LOWER-SECTION-MULTILANG-01` | OPEN 후보 | 8개 하위 절 이름(`문서/실행/이야기/누리/샘/거울/보개/슬기`)의 T1 dialect coverage를 확인하고 누락분을 symbol export 백로그에 연결한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:174` |
| `OI-PROJECT-SETTINGS-INHERITANCE-01` | OPEN 후보 | 프로젝트 수준 기본값이 `실행기본 {}` 외에 `설정.문서.말씨`/`설정.보개` 같은 비실행 절까지 허용하는지 `프로젝트 {}` closure 시점에 결정한다. | `또니랑/CODEX_HANDOFF_20260706_설정헤더_정합_및_구제안_델타.md:175` |
| `OI-BOGAE-STANDARD-PACK-NAMING-01` | OPEN 후보 | `std_bogae_graph2d` 같은 표준팩 노출명을 순우리말(`그래프보개` 등)로 할지 profile 이름으로 유지할지 결정한다. | `docs/context/proposals/PROPOSAL_BOGAE_STANDARD_PACK_AND_LOWERING_CONTRACT_V1_20260706.md:530` |
| `OI-PRE_RELEASE-RESERVED-SURFACE-01` | OPEN 후보 | `가설`, `검산`, `단위 정의`, `말거리`, `~이름(...)` 분포 표기 공간을 발표 전 reserved/proposal로 선점할지 결정한다. | `docs/context/notes/IDEAS_DDONIRANG_ENRICHMENT_V1_20260706.md:67` |

## 운영 메모

- `state_hash` 산식, runtime canonical names, parser/runtime 구현은 이 OI 묶음에서 변경하지 않는다.
- SSOT 병합 전에는 Tier B 구현을 해금하지 않는다.
- 후보 ID는 SSOT 오너가 최종 명명할 수 있다. 이 문서의 ID는 병합 준비용 추적 이름이다.
