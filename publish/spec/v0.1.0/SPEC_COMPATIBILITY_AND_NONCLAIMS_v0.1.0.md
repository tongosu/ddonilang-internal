# 호환성·비주장 정책 — Language SPEC v0.1.0

> trace: Language SPEC `v0.1.0` ← SSOT `v24.14.1` ← byte-identical `v24.14.0` snapshot
> status: pre-release public draft; internal SSOT wins on conflict

## v0.x 정책

- `v0.1.0`은 출시 전 공개 초안이며 호환성 약속 전 단계다.
- v0.x에서는 충분한 근거와 migration 기록이 있으면 문법·API·stdlib 이름이 바뀔 수 있다.
- 바뀔 때는 공개 change record, 입력 별칭 종료 시점, golden/migration 순서를 함께 기록한다.
- Language SPEC `v1.0.0`은 첫 장기 호환성 약속 시점이며 현재 달성 주장이 아니다.

## 이 문서 묶음이 주장하지 않는 것

- 정식 출시, production readiness, 모든 운영체제·브라우저 지원.
- 모든 SSOT 설계 항목의 parser/runtime/CLI/WASM 구현 완료.
- registry에 존재하는 250개 stdlib 이름이나 모든 CLI/schema/diagnostic의 호환 보장.
- 일반 해석기, 무제한 solver, macro/reflection/async/FFI의 core 지원.
- live 외부 입력의 재현성, 픽셀·GPU·OS UI의 bit-identical 출력.
- 책·총집서·보개·Manim 결과가 내부 SSOT보다 높은 권위를 가진다는 주장.

결정 입력 1,074건의 행정 처분은 닫혔지만, 명시 보류 3건과
제품 구현 관문은 남아 있다. “결정 완료”와 “제품 완료”는 다른 상태다.
