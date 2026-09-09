# DDN V1 Product Closure 프로그램 시작 기준점

```text
PROGRAM_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
PROGRAM_STATUS: WAVE_0_CENSUS_IN_PROGRESS
AI_PROVIDER: OpenAI
AI_SURFACE: Codex Work
AI_CAPABILITY: repository audit / program management / evidence custody
SESSION_NICKNAME: V1마감관리Work
PROJECT_ROLE: PROGRAM_MANAGER
RETURN_LABEL: [개발관리Work -> 제품Chat]
DEEP_RESEARCH_CHECK: NOT_USE — 현 단계는 내부 저장소 원문·실행 증거 감사
```

## 실행 권위

- live internal SSOT: `v25.15.0`
- `SSOT_ALL_v25.15.0.md` SHA-256: `b51fc82e5b922b14e10e48e733f0398d85f4d0b9cb22477ac10e08cef19e3777`
- `SSOT_ALL_MANIFEST_v25.15.0.md` SHA-256: `f08a149b25520e708c8250a71e487d0fb420576a2e088202171dfdbf1e316ad4`
- live checker: `v25.15.0 LIVE BUILD CHECK PASS files=39 rd=437 current=3 public=v0.5.0`
- workspace bundle: `v24.35.1_20260813_gaji-resolution-lock-v1-candidate-r3`
- workspace manifest SHA-256: `97f6554c24d0b2a89aeb3190a5febdde4230498ebdc4156c643d8fd8a969ba9f`
- public Language SPEC: `v0.5.0`

제품Chat 지시문의 `v25.11.1`은 역사 참고값으로만 보존하고 실행에는 사용하지 않는다.

## Git custody

- shared root HEAD: `a000e262cb96b51007286e2fb70bb2fa31e2af32`
- shared root tracked dirty: `201`
- shared root staged: `0`
- isolated baseline: `daabc1188d164888d7c3280588c0dbb5328bb5b6`
- isolated branch: `codex/ddn-v1-product-closure-long-range-r1-20260827`
- isolated worktree start state: clean / staged `0`

shared root는 읽기 전용으로 보존한다. 프로그램 문서와 registry는 격리 worktree에서만 작성한다.

## 기존 프로그램 disposition

`DDN-LONG-RELINT-PRODUCT-01-COMPLETION`은 폐기·재개·대체하지 않는다.

```text
EXISTING_PROGRAM_DISPOSITION:
PREDECESSOR_EVIDENCE_PROGRAM_WAITING_FOR_EXTERNAL_INDEPENDENT_REVIEW
```

RELINT의 PC01·G14·public projection·Workbench·rights 증거는 V1 census의 입력이다. 독립검토 전 local PASS를 current closure로 승격하지 않는다.

## 현행 V1 권위 경계

live SSOT v25.15.0은 다음을 명시한다.

- 실제 V1 membership row: `0`
- numeric maturity: `0`
- readiness floor: `UNCLAIMABLE`
- product-status transition: `0`

제품Chat의 REQUIRED/OPTIONAL/DEFERRED 목록은 `OWNER-APPROVED PRODUCT ROADMAP INPUT`으로 census에 기록한다. SSOT의 실제 membership이라고 표시하지 않는다. 향후 정본 반영이 필요하면 정본관리Work로 제안한다.

## 최초 safe work

1. capability family census와 실제 제품 경로 inventory
2. 완료·검토대기·candidate evidence의 target-bound 분류
3. provisional V1 membership과 SSOT membership 0의 분리
4. dependency DAG와 critical path 후보
5. first implementation vertical 1~3개의 권위·DoD·review 계약 작성

제품 코드, `docs/ssot/**`, public SPEC, GitHub, activation, release는 이 Wave에서 변경하지 않는다.
