# creator_gaji_round5_regression_v1

R5에서 R0~R4 수리 뒤 creator-gaji 제품 순환이 유지되는지 확인한 증거 묶음이다. Windows clean checkout에서 드러난 CRLF 휴대성 결함을 제품 경계에서 고쳤으며, `docs/ssot/**`는 읽기만 하고 수정하지 않았다.

주요 수리:

- WASM manifest가 텍스트와 바이너리 해시 모드를 명시하고 브라우저가 그 모드를 엄격히 검증한다.
- 새 네이티브 프로젝트는 `뿌리.ddn`이 아니라 선언된 진입 파일을 편집 대상으로 연다.
- 디스크 local-project frontdoor는 CRLF 텍스트를 LF로 정본화한 뒤 graph/lock/hash 경계에 전달한다.
- 보기 capability는 로컬 WASM 실행을 허용하지만 서버 run archive를 쓰지 않는 R2 계약을 승격 게이트에서도 검증한다.
- Git 비추적 SSOT ZIP은 `DDN_VOL4_BUNDLE_PATH`로 읽기 전용 주입할 수 있다.

빠른 증거 검사:

```text
python tests/run_creator_gaji_round5_regression_check.py
```

전체 실행 명령과 결과는 `r5_evidence.detjson`에 기록했다. 외부 창작자 파일럿 성공 수는 여전히 0이며 전체 R0~R7 닫힘을 주장하지 않는다.
