# Session Delta — 셈그림 포물선 첫 세계 W1

- Date: 2026-07-10
- Agent: Codex
- Status: Reflected
- Closure: `닫힘-동작`

## 목적

활성 대표 포물선 차시를 셈그림의 첫 공개 제품 진입점으로 만들고, 브라우저에서 관찰·조절·실행 제어·결정적 재실행을 제품 동작으로 검증한다.

## 결정

- 제품 기준 ID는 `rep_phys_projectile_xy_v1`이다.
- `physics_projectile`, `projectile`은 호환 진입 별칭이다.
- 첫 세계는 다섯 매김 중 가로 속도, 세로 속도, 중력만 노출한다.
- 궤적은 런타임 상태 `x/y` 관찰값을 우선 사용한다.
- `trajectory_trail`과 `afterimage`는 분리된 보기 역할이며 상태 해시에 들어가지 않는다.
- W1은 안정 직접 주소의 동작 닫힘이다. 기본 루트 승격은 별도 결정이다.

## 변경

- `solutions/seamgrim_ui_mvp/ui/app.js`
- `solutions/seamgrim_ui_mvp/ui/screens/run.js`
- `solutions/seamgrim_ui_mvp/ui/components/slider_panel.js`
- `solutions/seamgrim_ui_mvp/ui/index.html`
- `solutions/seamgrim_ui_mvp/ui/styles.css`
- `solutions/seamgrim_ui_mvp/lessons/index.json`
- `solutions/seamgrim_ui_mvp/lessons/rep_phys_projectile_xy_v1/meta.toml`
- `pack/seamgrim_first_delight_projectile_v1/`
- `tests/seamgrim_first_delight_projectile_runner.mjs`
- `tests/run_seamgrim_first_delight_projectile_check.py`
- `docs/reports/impl/SEAMGRIM_FIRST_DELIGHT_PROJECTILE_V1_20260710.md`

## 검증

- `node tests/seamgrim_first_delight_projectile_runner.mjs` PASS.
- `python tests/run_pack_golden.py seamgrim_first_delight_projectile_v1` PASS.
- `python tests/run_seamgrim_first_delight_projectile_check.py` PASS, `behavior-closed`.
- 직접 캡처로 데스크톱·모바일 궤적과 세 조절값을 확인했다.

## 경계

- `docs/ssot/**` 변경 없음.
- parser/runtime/state hash 의미 변경 없음.
- 선언형 `세움{}` 비교판과 `world_diff`는 미착지.

## 다음 작업

1. current-line 가등급 대표 세계 3개를 같은 첫 세계 계약으로 정렬한다.
2. 온뭉치 가등급 10세계 pilot manifest와 카드 검증기를 만든다.
3. 포물선 명령형/`세움{}` 선언형 표현판을 `teaching_pair`로 묶되 동등성은 자동 주장하지 않는다.
