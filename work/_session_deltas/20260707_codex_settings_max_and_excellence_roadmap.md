# 20260707 Codex Session Delta — 설정 최대 지도 V2와 일곱 목적 훌륭화 로드맵

Status: Pending

## 입력

- 사용자 제공: `PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V1_20260706`
- 사용자 요청: 설정최대지도에 Codex 의견을 반영한 새 문서 작성, 일곱 목적을 모두 "훌륭"으로 끌어올리기 위한 추가 설계/작업 정리

## 산출물

- `docs/context/proposals/PROPOSAL_SETTINGS_MAX_CUSTOM_SURFACE_V2_20260707.md`
- `docs/context/proposals/PROPOSAL_SEVEN_PURPOSES_EXCELLENCE_ROADMAP_V1_20260707.md`

## 반영한 결정

- `설정해시`를 단일 해시가 아니라 `run_config_hash / view_config_hash / doc_config_hash / settings_hash` 4분할 모델로 보정했다.
- `시앗묶음`을 `InputSnapshot` 봉인 경로와 연결했다.
- `설정.누리`에서 `space2d/space3d`를 제외하고, world/state family와 view/presentation family를 분리했다.
- `환경ID`를 기록용 메타로 두고, 실제 결과영향 선택자는 `규칙묶음/첫상태참조`로 분리했다.
- `계산단위계`와 `표시단위계`를 분리했다.
- `승인갈래/재연갈래`는 사실상 단일값 불변 계약으로 두도록 권고했다.
- 일곱 목적별로 "훌륭" 판정에 필요한 추가 설계, 앞으로 할 일, DoD를 정리했다.

## 검증

- 문서 끝 공백 검사 PASS
- `Select-String`으로 `run_config_hash/view_config_hash/doc_config_hash`, `시앗묶음`, `space2d` 분리, 일곱 목적별 훌륭화 DoD 확인
- `docs/ssot/**` 수정 0건 유지 확인
- parser/runtime 변경 0건

## 미해결

- 두 문서는 PROPOSAL 단계다. pack skeleton, 구현, 성능 증빙, 외부 실증은 후속 작업이다.
