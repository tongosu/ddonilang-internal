# 또니랑 V1 결정성·프로젝트 안내 — PRE_RELEASE

현재 문서는 V1 제품이 지향하는 사용자 관점 계약을 설명한다. 실제 공식 제품 지원이나 저장 형식을 확정하지 않는다.

## 결정성 목표

같은 지원 원문, 프로젝트 입력, SourceEpoch, target profile과 봉인된 의존성을 사용하면 worker 수나 물리 실행 순서가 달라도 같은 의미 결과로 수렴해야 한다.

V1 제품 폐쇄 전 확인할 항목:

- 입력과 프로젝트 의미 자원의 명시적 봉인
- state/result identity
- internal receipt/replay
- silent semantic fallback 0
- 실패 시 partial semantic publish 0
- required native/WASM/Workbench 경로의 동일 의미

현재 이 항목들은 `V1_PLANNED`이며 제품 전체 PASS가 아니다.

## 프로젝트 목표

formal project는 source root, entry, SourceEpoch, 의미 설정, 명시된 자원, 의존성·lock과 실행 snapshot을 결정적으로 소유해야 한다.

출시 전 경계:

- exact manifest filename과 physical schema는 공개 확정되지 않았다.
- 미선언 물리 파일을 의미 입력으로 추측하지 않는다.
- 실행 중 hidden resolve·update·network를 허용한다고 가정하지 않는다.
- save/reopen/recovery의 제품 구현 완료를 주장하지 않는다.

공식 프로젝트 예제와 파일 배치는 Project Custody 의미계약의 제품 구현·독립 검토·V1 membership 뒤에 추가한다.

