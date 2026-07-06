# NuriGym (또니랑 AI Gym) 스펙 — 외부 공유용 V1

> 작성: Claude / 2026-07-06 / 근거: `docs/ssot/ssot/SSOT_MASTER_v24.12.9.md`, `SSOT_PLATFORM_v24.12.9.md`, `SSOT_TOOLCHAIN_v24.12.9.md` 실측 인용 + 코드 실측(`core/src/nurigym/`, `core/src/realms.rs`)
> 용도: "그날"(이치 전투) 프로젝트가 자체 AI Gym 프로토타입(TOOL-01)을 설계할 때 참고할 외부 공유 스펙.
> 원칙: 여기 적힌 건 전부 실제 SSOT 문구 또는 실제 코드에서 확인한 것만이다. 추측/희망사항은 "설계뿐, 미구현"이라고 명시했다.

## 0. 먼저 확인할 것 — "AI Gym"이 가리키는 게 두 가지일 수 있다

이게 제일 중요합니다. "AI Gym"이라는 말이 실제로는 서로 다른 두 가지를 가리킬 수 있어요.

**(A) 진짜 RL 환경 인터페이스** — NuriGym 본연의 목적. `reset → step(action) → (observation, reward, terminated, truncated, info)`의 순환 루프가 있고, 그 안에서 매 스텝 "에이전트"(사람이 짠 정책이든, 학습된 정책이든)가 행동을 선택합니다. OpenAI Gym/Gymnasium API와 개념적으로 동형입니다.

**(B) 결정론적 파라미터 스윕 도구** — 관찰/행동/보상 순환 루프가 필요 없습니다. 룰 파라미터 조합별로 headless 실행 → 최종 결과 비교표. "AI"가 뭔가를 학습하거나 결정을 내리는 게 아니라, 사람이 미리 정한 파라미터 집합을 전부 돌려보고 비교하는 것뿐입니다.

**이치 전투 TOOL-01이 실제로 필요한 건 어느 쪽인지 먼저 정해야 합니다.** (B)라면 아래 스펙의 절반(action 4상태, multi-agent merge pipeline, reward/termination)은 필요 없고, "결정론 재현(seed→같은 결과) + headless 배치 실행 + 결과 비교표"만 있으면 충분합니다 — 이미 별도로 설계하신 AI_GYM_DESIGN_V1 그대로 가면 됩니다. (A)를 검증하고 싶다면(즉 "장차 진짜 RL 에이전트가 이치 전투를 플레이하게 만들 것"까지 미리 검증), 아래 전체 스펙을 작게 재현해봐야 합니다.

---

## 1. 핵심 계약 (SSOT 잠김, `SSOT_MASTER:569,592`, `SSOT_PLATFORM:586`)

```
reset(seed, options) = 모두다시   // 새 episode 시작, world+판+마당+보개/UI 조종값까지 전부 초기값
step(action) -> (observation, reward, terminated, truncated, info)
같은 seed → 같은 state_hash          // 결정론 보장
```

- `reset`는 "새 episode 시작 계약"으로 읽고, 또니랑 reset kind 대응은 **`모두다시`**로 고정합니다(5종 reset kind 중 가장 넓은 범위 — world/판/마당/보개/UI 조종값 전부 초기화). 이전 episode의 live control, live input, view selection, UI override는 암묵 보존하지 않습니다.
- resident(장기 실행 프로세스) 모드에서도 `:reset`은 새 프로세스 1회 실행과 동치여야 합니다.

## 2. Action 4상태 모델 (SSOT 잠김, `SSOT_MASTER:618`)

```
맞음    (valid)    — merge 후보
가만히  (noop)     — merge 후보, 정상 행동 취급(미제출과 다름!)
잘림    (clipped)  — merge 후보, 원래 범위 밖이었지만 정책상 잘라서 유효 처리
거부    (invalid)  — merge 제외
```

**중요한 구분**: `미제출`(슬롯이 비어 있음)과 `가만히`(정상적으로 "아무것도 안 하기"를 선택함)는 **다릅니다**. 이 둘을 같은 것으로 취급하면 안 됩니다.

## 3. 다중 에이전트 action pipeline (SSOT 잠김)

```
1. collect        — 이번 마디의 raw action 후보를 모은다
2. missing-slot-resolve — 마디완성조건에 따라 빈 슬롯 처리(아래 §4)
3. normalize       — 각 agent의 raw action을 canonical envelope로 정규화
4. validate/coerce — 맞음/가만히/잘림/거부로 분류
5. merge           — env meta/schema가 정한 규칙(sum/mean/vote/priority/last_win 등)으로 병합
                     merge 후보 = {맞음, 가만히, 잘림} / merge 제외 = {거부}
6. apply           — shared_env라면 이 시점에서 env.step()은 정확히 1회
7. record          — step record에 raw_action/normalized_action/action_status/merged_action/applied_action 등을 남김
```

## 4. 마디 완성 조건 (SSOT_TERMS 잠김)

```
모두필요 (all_required)  — 활성 agent 전원이 행동을 내야 마디가 닫힘
빈칸채움 (fill_noop)      — 마감 시점까지 안 낸 agent는 자동 "가만히"로 채움
```

(SSOT는 이 둘만 잠갔습니다. "개별마디/독립 시계" 같은 더 복잡한 모드는 아직 SSOT에 없습니다 — 필요하면 별도 설계 논의가 필요합니다.)

## 5. Export/Dataset 스키마 (하류 산출물 — 의미 정본 아님)

**중요한 원칙**: DDN/SSOT 자체가 실행 의미의 정본입니다. 아래 스키마들은 전부 **lowering(하류) 산출물**일 뿐, 이것들이 action/observation/reset의 의미를 새로 정의하지 않습니다.

- `nurigym.dataset_header.v0.1`
- `nurigym.step_record.v0.1` — add-only provenance 필드: `raw_action / resolved_action / normalized_action / action_status / merge_candidates / merged_action / applied_action`(전부 optional, breaking 없이 추가 가능)
- `aigym.metrics_report.v0.1`
- `ddn.observation_manifest.v0`

## 6. 실행 재현성 등급 (D35, `SSOT_MASTER`/`SSOT_TOOLCHAIN` 잠김)

```
닫힘(Closed)        — 완전 결정론, state_hash 검증 가능. 공식/평가용
봉인된 열림(Sealed-Open) — 외부를 쓰되 record/replay로 재현. 공식/평가용
생열림(Live-Open)    — 실시간 직결, 재현 주장 불가. 실험/도구/라이브 UI 전용
```

**제품·평가·경진용 Gym 실행은 `닫힘`/`봉인된 열림`만 인정합니다.** RL 학습 루프처럼 실시간성이 필요한 것도 `봉인된 열림`(record 후 replay 검증)으로 감싸야 "공식 결과"로 인정됩니다.

## 7. 보상(Reward)은 언어 커널 밖

`보상` 선언은 DDN 언어 코어(교육용 lesson이 쓰는 문법)에 넣지 않습니다. NuriGym/AI Gym 확장 표준(위 §5 export 스키마) 레벨에서만 정의합니다 — lesson 저작자가 보상 함수 문법을 배울 필요가 없게 하기 위함입니다.

## 8. 실제 구현 상태 (정직한 현황, 코드 실측)

| 항목 | 상태 | 근거 |
|---|---|---|
| `BanditEnv`(seed 기반 reset/step/observation) | **실동** | `core/src/nurigym/bandit.rs` — `new(seed, config)`, `.step(action)`, `.observation()`, `.is_done()` 실제 구현 확인 |
| `Realm`/`MultiRealmManager`(멀티 인스턴스 병렬 step) | **실동** | `core/src/realms.rs` — `step_batch`, seed 파생 `mix64(master_seed, realm_id)` 실제 구현 확인 |
| `ObservationSpec`/`ActionSpec` | **부분** | `core/src/nurigym/spec.rs` — slot_count/action 목록을 담는 아주 얇은 직렬화 구조체만 있음. 범용 observation manifest 생성 로직은 없음 |
| §3(multi-agent action pipeline), §4(마디완성조건), §5(dataset/step_record/metrics 스키마) | **미구현** | `rg -rln "nurigym.dataset_header\|nurigym.step_record\|aigym.metrics_report" tools/ core/ pack/` → 0건. SSOT 문서에만 있음 |

**결론: "밴딧 하나 돌리는 최소 RL 루프"는 실제로 존재하고 동작합니다. 그 이상(멀티 에이전트, 표준 dataset export, gridworld급 환경)은 전부 설계 문서 단계이고 코드가 없습니다.** 그날 팀이 지금 이 스펙에 의존해서 뭔가를 만들면, `BanditEnv` 패턴 정도까지만 실제로 재사용 가능하고 나머지는 직접 만들어야 합니다.

## 9. 이치 전투 TOOL-01에 대한 구체적 권고

1. **먼저 (A)/(B) 중 뭘 검증하려는 건지 확정하세요.** (B, 파라미터 스윕)뿐이면 이 문서의 §2~§5는 안 가져와도 됩니다 — 지금 설계하신 AI_GYM_DESIGN_V1을 그대로 진행하시면 됩니다.
2. (A, 진짜 RL 검증)를 원하신다면, `core/src/nurigym/bandit.rs`의 패턴(seed→reset→step→observation, 결정론 보장)을 이치 전투 스케일로 최소 재현해보는 게 가장 값진 검증입니다 — 그게 실제로 존재하는 유일한 실동 참고 코드입니다.
3. 어느 쪽이든, **"닫힘/봉인된 열림"만 공식 결과로 인정한다**(§6)는 원칙은 그대로 가져가는 게 좋습니다 — 나중에 또니랑 본체 NuriGym과 합칠 때 재현성 기준이 어긋나지 않습니다.
