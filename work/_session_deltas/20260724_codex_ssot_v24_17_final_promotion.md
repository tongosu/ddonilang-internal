# 2026-07-24 Codex SSOT v24.17.0 최종 승격

## 결정

- 사용자 최종 승인을 근거로 `v24.17.0-research-integration-candidate C1`을 내부 SSOT `v24.17.0 live current`로 승격했다.
- 공개 Language SPEC은 `v0.2.1`을 유지했다. 내부 SSOT와 공개 SPEC은 별도 계보이며, 새 장면 표면의 제품 파서·정본화·낭독·golden·CLI/WASM 근거가 아직 닫히지 않았다.
- 현행 `보임 {}`은 새 정본 출력과 신규 예제에서는 금지하고 레거시 입력 호환으로만 남겼다. 제품 파서 제거 및 successor 전환은 OPEN이며, 이번 문서 승격을 `runtime landed`로 주장하지 않는다.
- 별도 외부 독립 검토 기록은 없으나 사용자가 소유자 최종 승격을 직접 지시했다. 결정론적 독립 재계산 검증은 통과했다.

## 적용

- 문서 저장소 승격 커밋: `5835978a66c32712944e7417c987bb9ed65b79d2`
- 백업 스크립트 보정 포함 문서 저장소 HEAD: `cf3c3a1ea7a28d07a0ddbe5880d4a522f324e69a`
- active 포인터·상태 문서 동기화 커밋: `f2410a4`
- 승격 결정 기록: `docs/decisions/SSOT_V24_17_0_FINAL_PROMOTION_DECISION_20260724.md`
- 협업 진입점 `AGENTS.md`, `AGENT_WORKFLOW.md`, `SSOT_POLICY.md`, `GEMINI.md`의 current 포인터를 v24.17.0으로 최소 동기화했다. Git에서 제외된 `CLAUDE.md`도 작업공간에서 같은 기준으로 맞췄다.
- 루트 작업 트리의 다른 세션 변경은 부분 staging으로 제외하고, 이 승격의 포인터·최신 상태 절·세션 기록만 분리했다.
- `publish/spec/**`는 변경하지 않았다.

## 검증

- 승격 생성기 `--check`: PASS
- 보존 v24.16.0 트리 SHA-256: `b803fed013976b0ddd0c4c3cd2007f125efaa29373f7efb04ff34cc070fa2ebb`
- current v24.17.0 트리 SHA-256: `ee8a1a35ed1cd69663acbac294ddec637b8fe9f3fed38aa6a9ef57c5ab8bdcc5`
- companion manifest SHA-256: `932193b9b4f6cd7ee3cd6661493ba9008e74c3bd41b99a936a519af86cdfa9bf`
- 독립 검사: seal 32행, active envelope 30개, aggregate 30개, UTF-8/LF, v24.16 보존 해시 모두 PASS
- `publish/spec` diff: 0

## 백업

- 기존 로컬 전용 백업 원격 `local-backup`의 `main`을 포인터 동기화 커밋 `f2410a4c819e0c9cf36104871a9367af61a91954`까지 갱신했다.
- 로컬 백업에서 `C:\tmp`로 실제 clone 복원 후 승격 생성기 `--check`와 `ssot/CURRENT.md`의 internal/public 포인터를 다시 확인해 PASS를 판정하고 임시 복원본을 제거했다.
- Google·OneDrive 대상 암호화 복제는 민감한 문서의 외부 위치 복사에 대한 별도 명시 승인이 없어 실행하지 않았다.

## 남은 경계

- 공개 Language SPEC 승격은 새 표면의 제품 근거와 공개 호환 정책이 닫힌 뒤 별도 승인·버전으로 진행한다.
- `보임 {}` 제품 제거, successor parser/canon/reading/golden, CLI/WASM parity는 OPEN이다.
