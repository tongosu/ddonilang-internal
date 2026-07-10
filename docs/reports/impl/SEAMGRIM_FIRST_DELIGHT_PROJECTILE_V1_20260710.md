# 셈그림 포물선 첫 세계 W1 구현 보고서

상태: `닫힘-동작` / 2026-07-10

## 범위

- 안정 진입 주소: `solutions/seamgrim_ui_mvp/ui/index.html?first_delight=projectile`
- 활성 제품 차시: `rep_phys_projectile_xy_v1`
- 호환 별칭: `physics_projectile`, `projectile`
- 첫 화면 조절값: 가로 속도(`초기속도x`), 세로 속도(`초기속도y`), 중력(`중력가속도`)
- 실행 제어: 실행, 일시정지, 한 마디, 초기화
- 보기 역할: `trajectory_trail` 필수, `afterimage` 보조

기본 루트 화면을 첫 세계로 교체하지는 않았다. W1은 직접 진입 가능한 안정 주소와 활성 대표 차시의 제품 흐름을 닫은 단위다.

## 구현

1. `first_delight=projectile`을 활성 대표 차시로 정본화하고 자동 실행한다.
2. 첫 세계에서는 다섯 매김 가운데 세 핵심 조절값만 사람용 이름으로 노출한다.
3. 현재 관찰 상태의 `x/y`를 포물선 궤적으로 합성해 주 보개에 그린다.
4. 지나온 경로선과 감쇠 잔상을 각각 `trajectory_trail`, `afterimage`로 구분한다.
5. 보기 역할과 합성 도형은 상태 해시 입력에 넣지 않는다.
6. 첫 세계 실행 뒤에는 `조절` 탭을 유지해 세 조절값이 즉시 보이게 한다.
7. 제품 시험용으로 엔진 상태, 주 보기 역할, 궤적 선분 수를 DOM 상태에 노출한다.

직접 화면 검수에서 임시 그래프의 `t/vy`가 실제 위치 `x/y`보다 먼저 선택되는 문제를 발견했다. 첫 세계의 `space2d` 합성 순서를 `x/y` 관찰 우선으로 바꾸고, browser runner가 궤적 선분 3개 이상을 요구하도록 강화했다.

## 검증

```text
node tests/seamgrim_first_delight_projectile_runner.mjs
PASS seamgrim_first_delight_projectile: ok

python tests/run_pack_golden.py seamgrim_first_delight_projectile_v1
PASS pack golden ok

python tests/run_seamgrim_first_delight_projectile_check.py
PASS [seamgrim-first-delight-projectile-v1] OK behavior-closed
```

통합 검사기는 다음을 함께 확인한다.

- 데스크톱 1360x860과 모바일 390x844에서 가로 넘침·캔버스/조절 겹침 없음.
- 실제 캔버스 비공백과 `trajectory_trail` 선분 3개 이상.
- 세 조절값의 이름·순서·접근성 label.
- 실행, 일시정지, 한 마디, 초기화.
- 중력값 변경이 제품 DDN 원문으로 반영되고 재실행됨.
- 같은 입력으로 두 번 완주했을 때 같은 `state_hash`.
- 대표 포물선 원문이 CLI `check`, `canon`, `run`을 직접 통과함.

화면 증거는 로컬 빌드 산출물에 있다.

- `I:/home/urihanl/ddn/codex/build/seamgrim_first_delight_desktop.png`
- `I:/home/urihanl/ddn/codex/build/seamgrim_first_delight_mobile.png`

## 경계

- `docs/ssot/**` 변경 없음.
- parser, canonical surface, runtime 의미론, `state_hash` 산식 변경 없음.
- `원리{}` 또는 새 언어 표면 추가 없음.
- 선언형 `세움{}` 비교판, world diff, 리믹스 계보, 기본 루트 승격은 후속 단위다.
