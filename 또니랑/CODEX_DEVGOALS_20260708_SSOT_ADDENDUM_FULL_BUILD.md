# CODEX DEVGOALS 2026-07-08 — SSOT 부록 전체 개발 목표 지시서

- 기반 SSOT: `docs/ssot/ssot/*_v24.12.9.md`의 2026-07-08 addendum
- 기반 기록: `work/_session_deltas/20260708_codex_ssot_direct_reflection.md`
- 목적: 설정/누리/샘/슬기/거울/보개/7목적/발표전동결 내용을 가능한 한 제품 경로와 반복 검증으로 개발한다.
- 형식: **목표 + 성공 기준**만 준다. 구현 방법은 Codex 자율. 막히면 멈추지 말고 질문 큐에 적고 다음 목표로 간다.

## 상위 성공 기준

기술 목표는 아래 North Star를 앞지르지 않는다.

```text
2026년 안에, 우리가 모르는 사람 10명이 설치 없이 또는 최소 설치로 셈그림 물리 시뮬레이션을 만들고 공유한다.
```

현재 wedge는 **셈그림 물리 차시**다. G1~G8을 수행할 때도 교육/물리 vertical slice, 설치 없이 눌러보기, 공개 안정성 라벨에 가까운 작업을 우선한다.

7목적은 portfolio다. 첫 공개 성공은 portfolio 전체가 아니라 wedge 하나로 만든다.

## 운영 규칙

**최우선 원칙**: SSOT에 반영된 내용을 개발하되, SSOT가 `candidate / runtime landed claim 아님`으로 둔 것은 구현 전까지 완료 주장하지 않는다.

**자율 허용**:
- 파일 배치, runner/test 구조, pack skeleton, report 형식, 내부 helper 이름.
- 기존 제품 경로를 깨지 않는 additive field, additive checker, additive pack.
- 성능/진단/코퍼스/동결 스윕 같은 도구층 개발.

**질문 큐로 보류**:
- 새 문법/예약어 hard-cut.
- 정본화기 출력 변경.
- public schema required field 확정.
- `state_hash` 산식/입력 변경.
- `InputSnapshot`, `SeulgiPacket`, `SeulgiIntent` 같은 runtime canonical type rename.
- `설정.누리` key set, `설정.이야기` current 노출, `지연마디` 소유권처럼 OI에 등록된 결정.

**금지**:
- 테스트 전용 Python/JS lowering으로 정식 언어/런타임 지원 완료 주장.
- SSOT 후보 surface를 parser/runtime에 조용히 hard-cut.
- `state_hash` truth를 보개/슬기/도구층으로 넘기는 서술 또는 구현.
- 자연어 직접 실행 구현.
- 기존 사용자 변경 revert.

**닫힘 표기**:
- 도구/문서/pack skeleton만 있으면 `닫힘-문서`.
- 제품 runtime/frontdoor 동작이 바뀌고 검증되면만 `닫힘-동작`.
- 부분 구현은 반드시 `부분`으로 보고한다.

## 시작 조건

새 세션 시작 직후 아래를 읽는다.

1. `AGENTS.md`
2. `SSOT_POLICY.md`
3. `docs/context/all/DEV_SUMMARY.md`
4. `work/_session_deltas/20260708_codex_ssot_direct_reflection.md`
5. `docs/ssot/ssot/SSOT_UPDATE_NOTES_v24.12.9.md`
6. `docs/ssot/ssot/SSOT_DECISIONS_v24.12.9.md`
7. `docs/ssot/ssot/SSOT_PLATFORM_v24.12.9.md`
8. `docs/ssot/ssot/SSOT_OPEN_ISSUES_v24.12.9.md`
9. `docs/ssot/ssot/SSOT_PENDING_v24.12.9.md`
10. `docs/ssot/ssot/SSOT_PLANS_v24.12.9.md`

시작 시 `work/_session_deltas/YYYYMMDD_codex_ssot_addendum_development.md`를 만들고, 진행 중 질문/부분/검증 결과를 누적한다.

## 검증 배터리

목표 하나가 끝날 때마다 관련 검증을 실행한다. 하루 또는 세션 마감 시 최소 아래를 실행한다.

```bash
cargo check
python tests/run_ci_sanity_gate.py --profile core_lang
git status --short
```

`docs/ssot/**`는 현재 `.gitignore`에 걸려 일반 git status에 보이지 않을 수 있다. SSOT를 수정하지 않는 개발 세션이라면 이 사실만 기록하고 넘어간다.

---

## 목표 큐

### G0. 작업 경계와 질문 큐가 세션 안에서 닫힌다

**목표**: 개발을 시작하기 전에 candidate/landed 경계를 오해하지 않는 상태를 만든다.

**성공 기준**:
- 세션 델타 파일이 존재한다.
- `## 질문 큐`, `## 부분 구현`, `## 검증` 섹션이 있다.
- OI 중 이번 세션에서 결정하지 않을 항목을 최소 10개 적고, 작업을 멈추지 않는다.
- `git status --short` 결과를 세션 델타에 기록한다.

**최소 성공선**: G0 없이 다른 목표 착수 금지.

### G1. 발표 전 동결 검증이 반복 가능한 도구가 된다

**목표**: reserved surface, syntax space, E-code, schema version, pack ID 충돌 검사를 한 번의 명령으로 재현한다.

**성공 기준**:
- 반복 실행 가능한 검사 명령 1개가 있다. 예: `python tests/run_pre_release_freeze_tools_check.py`
- 산출 report가 `build/` 또는 `out/` 아래 생성된다.
- report에 최소 항목이 포함된다:
  - 예약어/예약 후보 발견 현황.
  - `~이름(...)`, `~분포(...)` 등 syntax-space probe.
  - `E_*` namespace 현황.
  - `schema_version` 사용 현황.
  - pack 후보 ID 충돌 현황.
- 기존 `PRE_RELEASE_FREEZE_SWEEP_V1.md`의 주요 수치와 비교 가능한 summary가 나온다.
- 제품 runtime/parser 변경 없음.

**닫힘 표기**: `닫힘-문서`.

### G2. 설정 해시와 시앗묶음이 도구층 prototype으로 동작한다

**목표**: `run_config_hash / view_config_hash / doc_config_hash / settings_hash`와 `시앗묶음`을 runtime 비접촉 prototype으로 만든다.

**성공 기준**:
- 설정 digest prototype 명령이 있다. 예: `python tests/tools/config_digest_proto.py`
- 같은 의미의 설정 표기 차이 3쌍이 같은 digest로 검증된다.
- result-affecting key classifier 초안이 있다.
- `run_config_hash`와 `view_config_hash`가 분리되어 산출된다.
- `시앗묶음` named stream derivation fixture가 있다.
- derived seed가 InputSnapshot에 들어가기 전 단계까지만 검증한다.
- runtime record schema, `state_hash`, parser는 건드리지 않는다.

**닫힘 표기**: `닫힘-문서`.

### G3. 누리 큰마디/속마디/행동기록 계약이 fixture와 pack으로 보인다

**목표**: P0~P7 phase, raw/merged action, `action_status`, write conflict fatal 후보가 pack evidence 형태로 보인다.

**성공 기준**:
- `pack/nuri_madi_phase_trace_g1_v1` 또는 동등 pack이 있다.
- P0~P7 phase trace fixture가 있다.
- raw action, merged action, `action_status`(`맞음/가만히/잘림/거부`)를 담은 detjson fixture가 있다.
- `E_MADI_WRITE_CONFLICT` fatal case fixture가 있다.
- 제품 경로에 이미 관련 기능이 있으면 그 경로로 검증한다.
- 제품 경로가 없으면 skeleton/checker로 두고 `닫힘-동작`을 주장하지 않는다.

**닫힘 표기**: 기본 `닫힘-문서`, 제품 경로 검증 시에만 `닫힘-동작`.

### G4. 보개 표준팩의 최소 제품 경로가 생긴다

**목표**: 사용자가 raw `모양`만으로 그래프/시뮬레이션을 억지로 만들지 않도록 표준 보개팩 개발을 시작한다.

**성공 기준**:
- 최소 pack:
  - `std_bogae_core`
  - `std_bogae_grid2d` 또는 기존 grid2d pack 연결
  - `std_bogae_graph2d`
- graph2d lowering fixture가 있다:
  - series order deterministic.
  - domain/tick deterministic.
  - label collision 처리 후보 기록.
  - 같은 입력 2회 실행 시 payload byte 동일.
- `bogae_hash`는 payload/DrawList hash로만 다루고 pixel hash를 truth로 삼지 않는다.
- 보개가 world state를 바꾸지 않는다는 checker 또는 report가 있다.

**닫힘 표기**: rendering 없이 payload/pack이면 `닫힘-문서`; 실제 UI/backend smoke가 있으면 해당 workflow만 `닫힘-동작`.

### G5. 교육 + 물리 시뮬 vertical slice를 최대한 닫는다

**목표**: 7목적 중 가장 가까운 교육/물리 시뮬을 실제 사용 흐름에 가깝게 만든다.

**성공 기준**:
- WASM/browser delivery smoke를 시도한다.
- WASM이 막히면 blocker report를 남기고 CLI fallback으로 교육 흐름을 검증한다.
- 진단 메시지 3층(`무엇이/어디서/어떻게`) fixture가 최소 5개 있다.
- 물리 적분기 pack이 최소 2종 이상 실행된다:
  - 명시적 오일러.
  - 반암시적 오일러.
  - 여력 시 RK4 또는 속도 베를레 후보.
- 물리 결과를 graph2d payload로 연결하는 fixture가 있다.

**닫힘 표기**: browser까지 통과하면 해당 vertical slice `닫힘-동작`; CLI/pack만이면 `닫힘-문서`.

### G6. AI Gym consumer와 step_record가 연구용 최소선에 접근한다

**목표**: AI Gym의 "조건부"를 줄이기 위해 consumer closure와 vectorized rollout prototype을 만든다.

**성공 기준**:
- `step_record.v0.2` additive schema fixture가 있다.
- 기존 reader가 unknown additive field 때문에 깨지지 않는 roundtrip test가 있다.
- raw/merged/action_status/settings hash field 후보가 들어간다.
- vectorized consumer prototype은 언어 문법이 아니라 consumer layer API로 만든다.
- 처리량 측정이 `perf_baseline_v1`과 연결된다.

**닫힘 표기**: consumer/tool layer는 `닫힘-문서`; 실제 Gymnasium-compatible consumer가 동작하면 범위를 좁혀 `닫힘-동작`.

### G7. 슬기/AI-friendly 개발 자료가 반복 생성된다

**목표**: AI가 또니랑을 개발·사용·검증하기 위한 corpus와 gate fixture를 유지 가능한 도구로 만든다.

**성공 기준**:
- deterministic LLM corpus 추출 명령이 있다.
- 같은 저장소 상태에서 2회 실행 시 byte 동일하다.
- corpus에는 SSOT 용어, 예제, 오류/진단 카드, pack summary가 구분되어 들어간다.
- 슬기 gate fixture가 있다:
  - AI proposal.
  - gate accept/reject.
  - sealed artifact 전까지 no-authority.
- 자연어 직접 실행은 구현하지 않는다.

**닫힘 표기**: `닫힘-문서`.

### G8. 7목적 excellence dashboard가 현재 증빙을 기준으로 갱신된다

**목표**: 목적별로 "조건부/미달"이 왜 남았고 무엇을 하면 "훌륭"이 되는지 개발 증빙과 연결한다.

**성공 기준**:
- report가 있다. 예: `docs/reports/audit/SEVEN_PURPOSE_EXCELLENCE_PROGRESS_V1.md`
- 각 목적별로 아래 열이 있다:
  - 현재 판정.
  - 이번 세션 개발 증빙.
  - 남은 gap.
  - "훌륭" 전환 조건.
  - 다음 pack/test/report.
- 교육/물리, AI Gym, 보개/Manim, 게임, 경제/수학, 교착어권, AI-friendly를 모두 포함한다.
- 과잉 주장을 막기 위해 `docs-first`, `pack-skeleton`, `tooling`, `behavior`를 분리한다.

**닫힘 표기**: `닫힘-문서`.

### G9. 공개 쐐기 패키지가 외부인에게 보이는 형태가 된다

**목표**: 처음 보는 사람이 방대한 문서 대신 바로 이해할 수 있는 첫 표면을 만든다.

**성공 기준**:
- 90초 데모 script 또는 storyboard가 있다.
- 랜딩 페이지 초안이 있다. 핵심 문장은 셈그림 물리 차시와 결정적 재현성에 맞춘다.
- "설치 없이 눌러보기" 링크를 만들기 위한 현재 blocker 표가 있다.
- 첫 페르소나를 1명으로 좁힌다. 기본 후보: 과학/정보 교사.
- 공개 안정성 라벨 초안이 있다:
  - 안정: 셈그림 물리 차시에 필요한 표면.
  - 실험: 그 밖의 후보/고급 표면.

**닫힘 표기**: `닫힘-문서`. 실제 브라우저 링크가 작동하면 해당 항목만 `닫힘-동작`.

### G10. AI 협업 WIP 부채가 줄어든다

**목표**: 제안서와 OI가 계속 늘어나는 구조를 끊고, 병합/기각/아카이브 흐름을 만든다.

**성공 기준**:
- 미병합 proposal 수와 Open OI 수를 세는 report 또는 script가 있다.
- proposal 상태값을 최소 4종으로 분류한다:
  - active
  - reflected
  - deferred
  - expired candidate
- 신규 설계 금지선이 report에 표시된다:
  - 미병합 proposal 10건 초과.
  - 활성 목표 지시서 2건 초과.
- 이번 세션에서 OI 3건 이상을 `닫힘/이월/기각/사용자결정필요` 중 하나로 정리한다.
- North Star와 무관한 새 설계는 만들지 않는다.

**닫힘 표기**: `닫힘-문서`.

---

## 우선순위

최소 성공선:

1. G0
2. G1
3. G2
4. G9의 blocker 표

좋은 하루:

1. G0~G2 완료.
2. G3 또는 G4 중 하나 완료.
3. G8 dashboard 작성.
4. G9 공개 쐐기 초안 작성.

강한 하루:

1. G0~G4 완료.
2. G5 일부 또는 G6 일부.
3. G9 또는 G10 완료.
4. 전체 검증 배터리 PASS.

전체 목표:

- G1~G10을 여러 세션으로 나눠 진행한다.
- 한 세션에서 다 끝내려 하지 않는다.
- 구현 가능한 것은 구현하고, 결정이 필요한 것은 OI/질문 큐로 남긴다.

## 질문 큐 초기값

다음은 개발 중 멈추지 말고 질문 큐에 남길 항목이다.

1. `설정.누리` key set current floor 확정.
2. `설정.이야기` section current 노출 여부.
3. `지연마디` 소유권: `설정.슬기` vs `설정.실행`.
4. `(N마디)마다` 기준: 큰마디 vs 속마디.
5. `행동모음갈래`와 기존 `합치기갈래` compat.
6. `E_MADI_WRITE_CONFLICT` payload와 사용자 진단 문구.
7. graph2d label collision canonical rule.
8. `시앗묶음` stream name canonicalization.
9. reserved surface를 실제 예약어로 막을 시점.
10. schema version negotiation policy.

## 마감 보고 형식

`work/_session_deltas/YYYYMMDD_codex_ssot_addendum_development.md`에 아래 형식으로 마감한다.

```text
## 결과 요약
- G0: 완료/부분/미착수 — 증빙:
- G1: 완료/부분/미착수 — 증빙:

## 닫힘 등급
- 닫힘-문서:
- 닫힘-동작:
- 과잉 주장 금지:

## 질문 큐
- 또니 결정 필요:

## 발견한 문제
- 기존 drift:
- 구현 blocker:

## 검증
- cargo check:
- core_lang sanity:
- 목표별 test:
- git status:

## 다음 세션 추천
```

## 성공의 정의

이번 목표 지시서의 성공은 "SSOT 부록 전체를 하루 만에 완성"이 아니다. 성공은 다음이다.

```text
가장 위험한 동결/설정/기록 경계를 먼저 반복 검증 가능하게 만들고,
제품 경로가 없는 것은 skeleton/checker로 정직하게 남기며,
교육/물리/보개/AI Gym 쪽 vertical slice를 순서대로 닫아 가는 것.
```
