# 호환성·비주장 정책 — Language SPEC v0.1.1

> trace: Language SPEC `v0.1.1` ← owner-approved SSOT `v24.14.2` administrator candidate
> status: current pre-release public draft; installed SSOT remains v24.14.1 until protected apply
> authority: internal current SSOT wins on conflict


## v0.x 정책

- `v0.1.1`은 출시 전 공개 초안이며 호환성 약속 전 단계다.
- v0.x에서는 충분한 근거와 migration 기록이 있으면 문법·API·stdlib 이름이 바뀔 수 있다.
- Language SPEC `v1.0.0`은 첫 장기 호환성 약속 시점이다.

## v0.1.0에서 v0.1.1

- runtime 의미를 새로 구현한 판이 아니라 사용자-facing 용어·settings 계약을 보완한 patch다.
- `v0.1.0` 문서와 seal은 byte-identical 보존한다.
- 새 정본 출력은 `씨앗값/씨앗묶음`을 사용한다.
- `시앗/시앗묶음`은 입력 호환만 허용하고 deprecation 진단·종료 release는 별도다.
- 평면 `제목/설명/마디수`는 입력 이행을 위해 유지하지만 정본 출력은 중첩 경로다.
- 임의의 새 평면 키와 영어 settings alias를 공개 안정 계약에 자동 추가하지 않는다.

## 이 문서 묶음이 주장하지 않는 것

- 정식 출시, production readiness, 모든 운영체제·브라우저 지원.
- 모든 SSOT 설계 항목의 parser/runtime/CLI/WASM 구현 완료.
- settings 8절과 씨앗묶음의 모든 제품 frontdoor parity 완료.
- 가지곳간 publish/install/search/moderation/security workflow 완료.
- registry의 모든 stdlib/CLI/schema/diagnostic 이름 호환 보장.
- live 외부 입력이나 픽셀·GPU·OS UI의 bit-identical 출력.

결정 입력 1,083건은 applied 75, excluded/history 1,008, deferred 0으로 처분됐다.
남은 evidence gate는 제품 완료 조건이며 미결정 proposal backlog가 아니다.
