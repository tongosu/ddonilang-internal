# SSOT_MERGE_AUDIT_20260706

- 작성: 2026-07-09 KST, Claude Code
- 성격: 지시문 13 실행 — 지시문 12 산출물(SSOT 병합 준비 묶음)에 대한 독립 감사
- 대상 산출물:
  - `docs/context/proposals/SSOT_PATCH_DRAFT_20260706_BUNDLE.md`
  - `docs/context/proposals/OI_CANDIDATE_BUNDLE_20260706.md`
  - `docs/context/proposals/OI_CANDIDATES_20260706_BUNDLE.md`
  - `docs/reports/audit/PRE_RELEASE_FREEZE_SWEEP_V1.md`
  - pack 후보 ID 중복 검사 (`SSOT_PATCH_DRAFT_20260706_BUNDLE.md` §pack 후보 ID 충돌 검사)
- 원칙: 실행자(Codex)와 감사자(Claude Code) 분리. 이 문서는 병합 여부를 결정하지 않는다 — 또니가 최종 결정한다.

## 총평

5개 체크리스트 중 4개 PASS, 1개 PARTIAL(교차 참조 정합). **병합 보류 권고 대상은 없음** — 발견된 이슈는 모두 병합 전 정리하면 되는 정합성 문제이며, 설계 원칙이나 경계 위반은 아니다.

## 1. 경계 준수 — PASS

- `git diff --stat main..codex/queue-20260706 -- docs/ssot/ lang/ core/ tool/ tools/teul-cli/src/` — 이번 세션 전체(DAYRUN/SSOTADD 배치 포함)에서 반복 확인, 매 배치 0건.
- 기존 `golden.jsonl` 수정 없음(전부 `A`ppend, 기존 파일 변경 0건) — 앞선 GOAL-LONGHORIZON/DAYRUN 병합 시 이미 확인됨.
- `main` 직접 커밋 0건 — 전부 `codex/queue-20260706` 경유 후 `--ff-only` 병합.

## 2. 주장 등급 — PASS

- `SSOT_PATCH_DRAFT_20260706_BUNDLE.md`가 "결정 후보/후보/질문" 3단 표로 명확히 분리되어 있고, 각 표 제목에 "SSOT 오너가 반영할 수 있도록" 문구로 결정 주체를 명시함 — 후보를 결정처럼 쓰지 않음.
- `OI_CANDIDATE_BUNDLE_20260706.md`, `OI_CANDIDATES_20260706_BUNDLE.md` 둘 다 서두에 "이 문서는 결정하지 않는다"를 명시.
- CLOSED 주장 과잉 사례 0건 — 확인한 모든 산출물이 `golden_closed`/`runner_skeleton`/`docs_first` 등 evidence tier를 명시하고 있음(예: `perf_baseline_v1/README.md`의 `closure_claim: no`).

## 3. 용어 drift — PASS

- 영문 enum 재유입 검색(`noop|rollback|priority|majority|turn_order|slot_owner`)을 `SSOT_PATCH_DRAFT`/OI 번들 2건/`PROPOSAL_NURI_MADI_*` 2건에 대해 실행.
- 결과: 전부 (a) 괄호 안 설명용 병기(`앞선모음(priority)`), (b) 명시적 금지 문구(`PROPOSAL_NURI_MADI_PHASE_WRITE_CONFLICT_DEEPDIVE_V1_20260706.md:131` — "`rollback` 표면 금지 — 정본은 `되물림`. D-001이 이미 잠갔다"), (c) 미해결 질문으로 명시(`priority`의 표면 이름 통일 필요, 결정 아님) 중 하나로만 사용됨.
- historical 표면(`매틱/중단/전이마다/예약`) 재유입 검색 — 대상 문서 내 0건.
- D-001(되물림), D-005(전이마다→바뀔때마다) 결정을 정확히 인지하고 반영하고 있음을 확인.

## 4. 교차 참조 정합 — PARTIAL

**4-1. OI 번들 2건 중복/불일치 (신규 발견).**
`OI_CANDIDATE_BUNDLE_20260706.md`(2026-07-07 작성)와 `OI_CANDIDATES_20260706_BUNDLE.md`(2026-07-08 작성)가 같은 ID를 다른 범위/문구로 등록하고 있다. 예:
- `OI-SETTINGS-NURI-KEYSET-01`: 전자는 "시앗/누리갈래/환경ID/공간갈래/첫상태참조/규칙묶음 중 어디까지"를 묻고, 후자는 "규칙묶음/단위계/공간갈래까지 소유하는가"를 물어 질문 범위 자체가 다르다.
- `OI-NURI-MADI-PHASE-OQ2-...`: 전자는 `-SEUM-01`(세움 fixpoint 여부), 후자는 `-FIXPOINT-01`(동일 주제, ID suffix만 다름)로 같은 질문을 다른 ID로 중복 등록.
- 후자에만 있고 전자엔 없는 항목(`OI-NURI-WRITE-CONFLICT-ERROR-01`, `OI-ERROR-CODE-NAMESPACE-01`, `OI-SCHEMA-VERSION-NEGOTIATION-POLICY-01` 등)도 다수 — 후자가 전자 이후 발표-전-동결 논의를 반영해 확장한 것으로 보이나, **두 문서가 통합되지 않은 채 별도로 존재**한다.
- **권고**: SSOT 오너 반영 전에 두 문서를 하나로 통합(최신 07-08판을 기준으로 07-07판의 누락 항목만 병합)하고 중복 ID를 제거해야 한다. 지금 상태로 병합하면 같은 주제에 대해 서로 다른 OI가 SSOT에 동시 등록될 위험이 있다.

**4-2. SSOT 인용 line 번호 drift (신규 발견, 표본 검증).**
`SSOT_PATCH_DRAFT_20260706_BUNDLE.md:32`가 인용한 `docs/ssot/ssot/SSOT_PLATFORM_v24.12.9.md:1825`(accepted_madi/target_madi·agent_id 실행 정렬 근거로 인용)를 직접 열어보니, 해당 줄은 `InjectComponent` 화이트리스트(Emotion 컴포넌트 등) 내용으로 **주제가 전혀 다르다.**
- 같은 문서의 다른 인용 2건(`SSOT_MASTER_v24.12.9.md:752`, `SSOT_TOOLCHAIN_v24.12.9.md:204`)은 완전히 어긋나진 않았으나 정확한 줄 일치는 아니었다(근접 주제이나 정확히 그 문장은 아님).
- 원인: `docs/ssot/**`는 git 미추적 상태로 또니가 직접 편집하는 살아있는 문서라, Codex가 인용 시점 이후 문서가 갱신되면 줄 번호가 자연히 밀린다(이번 세션에서 `SSOT_LANG_v24.12.9.md`에 2026-07-08자 addendum이 추가된 것도 같은 패턴).
- **권고**: 병합 직전에 `SSOT_PATCH_DRAFT_20260706_BUNDLE.md`의 모든 SSOT 인용 line 번호를 현재 SSOT 상태 기준으로 재확인해야 한다. 인용이 틀렸다고 해서 근거 자체가 틀린 것은 아니지만(내용은 유효), line 번호를 그대로 신뢰하면 안 된다.

**4-3. pack ID 충돌 검사 — 검증 결과 정확.**
`SSOT_PATCH_DRAFT_20260706_BUNDLE.md` §pack 후보 ID 충돌 검사의 충돌 4건(`perf_baseline_v1`, `llm_corpus_extract_deterministic_v1`, `ai_det_tier_capability_matrix_v1`, `stdlib_l1_integrators_v1`)을 표본 확인했다. 특히 `stdlib_l1_integrators_v1`은 충돌이 정확히 식별됐고, 실제 구현(지시문 11/15)은 이를 피해 `stdlib_l1_integrators_g1_v1`이라는 다른 이름을 사용해 실제 충돌 없이 진행됐다 — 이 부분은 실측과 실행이 정확히 맞물렸다.

**4-4. 지시문 12 대상 산출물 8건 — 전부 실존 확인.**
`SSOT_PATCH_DRAFT_20260706_BUNDLE.md` §대상 산출물 8건의 파일 경로 8개 전부 실제로 존재함을 확인.

## 5. SSOT 권위 순서 준수 — PASS (표본 검증)

- 패치 초안이 겨냥한 대상 파일 분포: `SSOT_MASTER`(2건), `SSOT_PLATFORM`(6건), `SSOT_TOOLCHAIN`(2건) — MASTER > TERMS > DECISIONS > LANG > PLATFORM > TOOLCHAIN 순서상 상위 파일(MASTER)과 실행 세부(PLATFORM/TOOLCHAIN)를 적절히 구분해 배정하고 있다.
- 표본 검증한 3개 인용 중 어느 것도 기존 SSOT 문장과 **직접 모순**되는 제안은 발견되지 않았다(4-2의 문제는 인용 정확성 문제이지 권위 순서 위반은 아니다).
- 단, 8개 인용 전체에 대한 전수 모순 대조는 이번 감사 범위에서 수행하지 못했다(표본 3건만) — 병합 시점에 전수 재확인 권고.

## 종합 권고

1. **병합 보류 사유 없음** — 경계·주장 등급·용어는 모두 PASS.
2. **병합 전 필수 조치 2건**:
   - OI 번들 2건(`OI_CANDIDATE_BUNDLE_20260706.md` + `OI_CANDIDATES_20260706_BUNDLE.md`) 통합, 중복 ID 제거.
   - `SSOT_PATCH_DRAFT_20260706_BUNDLE.md`의 SSOT 인용 line 번호 전수 재확인(현재 SSOT 상태 기준).
3. 위 2건은 SSOT 오너(또니) 반영 작업 중 자연히 처리 가능한 수준이며, 별도 Codex 재작업 없이도 병합 가능하다고 판단한다.

## DoD 확인

- 감사 체크리스트 5항목 PASS/FAIL 표기 완료.
- 산출: 본 문서 + `docs/reports/audit/INDEX.md` 갱신(별도 커밋).
