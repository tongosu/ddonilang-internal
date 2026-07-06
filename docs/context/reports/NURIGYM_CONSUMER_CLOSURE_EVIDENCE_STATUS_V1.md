# NURIGYM_CONSUMER_CLOSURE_EVIDENCE_STATUS_V1

작성일: 2026-07-06
브랜치: `codex/queue-20260706`
범위: Q36 지시문 6. 신규 문법/런타임/pack/golden 변경 없이 현황만 정리.

## 요약

누리짐 의미 계약의 일부는 제품 코드와 pack runner로 이미 기계 검증된다. 다만 브리프가 요구한 consumer closure 전체를 `golden_closed`로 주장하기에는 세 가지 간극이 남아 있다.

1. 브리프가 명명한 `gym_reset_seed_implies_complete_episode_reset_v1`, `resident_reset_episode_equiv_v1` pack/runner는 현재 `pack/` 아래에 없다.
2. 제품 wire는 `nurigym.step.v1`에 `observation/action/reward/next_observation/done`을 낸다. `terminated/truncated/info` 5튜플 이름 자체는 아직 제품 wire/golden으로 닫히지 않았다.
3. Python/Web parity의 현재 제품 증빙은 `wasmtime-py`/`PyO3`가 아니라 Node 기반 web-side evaluator와 CLI dataset projection 비교다.

따라서 현 상태의 결론은 `golden_closed`가 아니라 "부분 runner/golden 증빙 있음, consumer closure는 미완"이다.

## 현황표

| 항목 | 현재 근거 | 등급 | 판정 |
|---|---|---|---|
| `gym_reset_seed_implies_complete_episode_reset_v1` | `pack/` 검색 결과 해당 디렉터리 없음. 관련 reset/step 행렬 근거는 `roadmap_v2_a1_nurigym_reset_step_matrix_reconciliation_v1`로 존재하나, contract가 `runtime_claim:false`, `representative_environment_golden_claim:false`, `python_web_parity_claim:false`를 명시한다(`pack/roadmap_v2_a1_nurigym_reset_step_matrix_reconciliation_v1/contract.detjson:5`, `:9`, `:10`). | docs_first / 대체 marker | 요청 이름 기준 pack 미착륙 |
| `resident_reset_episode_equiv_v1` | `pack/` 검색 결과 해당 디렉터리 없음. `resident_reset_episode_equiv_v1` 문자열은 구제안/토론 문서에만 남아 있다. | docs_first | 요청 이름 기준 runner 미착륙 |
| reset/step 행렬 반영 | A1 reconciliation pack은 `matrix_closure_claim:true`와 `status: behavior_closed`를 갖는다(`pack/roadmap_v2_a1_nurigym_reset_step_matrix_reconciliation_v1/reconciliation.detjson:5`, `:7`, `:12`). 하지만 false claim 항목은 대표 환경 golden/Python-Web parity를 부정한다(`:34`, `:35`). | runner_fill / marker | 행렬 정합 증빙은 있으나 consumer closure 직접 증빙은 아님 |
| step wire 기본 필드 | 제품 record는 `observation/action/reward/next_observation/done` 구조다(`tools/teul-cli/src/cli/nurigym.rs:119`, `:1296`, `:1307`, `:1321`). core env별 Step도 `observation/reward/next_observation/done` 구조다(`core/src/nurigym/gridmaze.rs:28`, `core/src/nurigym/cartpole.rs:32`, `core/src/nurigym/bandit.rs:22`, `core/src/nurigym/pendulum.rs:27`). | golden_closed(현재 schema) | 현재 `done` 기반 schema는 검증됨 |
| `terminated/truncated/info` 5튜플 | 제품 `nurigym.step.v1` builder와 core Step 구조에 `terminated/truncated/info` 필드가 없다. `tests/run_nuri_gym_contract_check.py`도 `terminal`/`done`만 검사한다(`tests/run_nuri_gym_contract_check.py:143`, `:146`, `:165`). | docs_first | Gym 5튜플 이름으로는 미착륙 |
| action 4상태 | `nurigym_shared_sync_action_pipeline_v1` contract가 `맞음/가만히/잘림/거부`를 요구한다(`pack/nurigym_shared_sync_action_pipeline_v1/contract.detjson:15`). checker도 같은 집합을 검사한다(`tests/run_nurigym_shared_sync_action_pipeline_pack_check.py:231`). 제품 unit test가 4상태 mapping을 직접 고정한다(`tools/teul-cli/src/cli/nurigym.rs:2025`, `:2034`, `:2043`). | runner_fill | 기계 검증 PASS. 단 pack README는 `closure_claim: no`(`pack/nurigym_shared_sync_action_pipeline_v1/README.md:4`)라 closure 주장은 보류 |
| Web consumer | `nurigym_python_web_parity_v1`은 JS evaluator `simulateGridmaze`/`simulateBandit`와 CLI dataset projection을 비교한다(`pack/nurigym_python_web_parity_v1/parity.detjson:5`, `:11`, `:18`; `solutions/seamgrim_ui_mvp/ui/nurigym_python_web_parity.js:170`, `:177`). | runner_fill | bounded web parity는 PASS. `ddonirang_tool.wasm` 직접 consumer 증빙은 아님 |
| Python short consumer | repo 제품 코드/runner 검색에서 `wasmtime-py` 실행 경로는 발견되지 않았다. 관련 표현은 제안/계획 문서 중심이다. | docs_first | 미착륙 |
| Python long consumer | repo 제품 코드/runner 검색에서 PyO3 binding/runner는 발견되지 않았다. `nurigym_python_web_parity_v1` contract도 `runtime_claim:false`, `full_browser_runtime_claim:false`를 명시한다(`pack/nurigym_python_web_parity_v1/contract.detjson:5`, `:38`, `:42`). | docs_first | 미착륙 |

## 실행 증빙

이번 조사에서 실제 실행한 명령과 결과:

```text
python tests/run_nurigym_shared_sync_action_pipeline_pack_check.py
PASS
dataset_hash_clip=sha256:d1c26e7c01937b5a70b7674b0afc86038994588e88cc3ee11719f24990d384cb
dataset_hash_reject=sha256:58744bbf2d5283382fcd75995158b2dce0dcf2be52ec2e5ee5a428ab91115eec
dataset_hash_valid_noop=sha256:6d91d00d8dbfa7e0f84b5aa04a00e6ebc3b2acd0186af53e2f7043530429c348
```

```text
python tests/run_nuri_gym_contract_check.py
PASS
nuri_gym_contract: PASS
```

```text
python tests/run_roadmap_v2_a3_nurigym_python_web_parity_check.py
FAIL
reason: matrix counts mismatch: rows=90 behavior=90 docs=0
```

위 A3 종합 checker 실패는 parity runner 자체 실패가 아니라, checker 내부의 오래된 matrix count 기대값과 현재 matrix 상태의 불일치다. 내부 parity gate는 별도 실행으로 통과했다.

```text
python tests/run_pack_golden.py nurigym_python_web_parity_v1 nuri_gym_gridmaze_v1 nuri_gym_bandit_v1
PASS
```

```text
node tests/nurigym_python_web_parity_runner.mjs
PASS
case_count=2
gridmaze_layout_episode: dataset_count=6 web_count=6 failures=[]
bandit_preferred_action_episode: dataset_count=4 web_count=4 failures=[]
```

## 남은 닫힘 조건

consumer closure를 `golden_closed`로 올리려면 최소한 아래가 별도 작업으로 필요하다.

1. `gym_reset_seed_implies_complete_episode_reset_v1`, `resident_reset_episode_equiv_v1`를 실제 pack/runner 이름으로 만들지, 기존 A1/lifecycle evidence에 매핑할지 결정한다.
2. Gym 표준 5튜플을 채택한다면 `done`과 `terminated/truncated` 관계를 제품 wire schema와 golden에 명시한다.
3. `info` 필드의 최소 schema와 state_hash 포함/제외 경계를 정한다.
4. `web = ddonirang_tool.wasm` 직접 smoke를 현재 JS evaluator parity와 분리한다.
5. `python short = wasmtime-py`, `python long = PyO3`의 실제 runner 또는 명시적 defer 상태를 만든다.

## 불변 경계 확인

- 코드 수정: 0건
- parser/runtime hard-cut 승격: 0건
- golden 갱신: 0건
- state_hash 변경: 0건
- runtime canonical 이름 변경: 0건
- fixed base pack 재설계: 0건
- `docs/ssot/**` 직접 수정: 0건
