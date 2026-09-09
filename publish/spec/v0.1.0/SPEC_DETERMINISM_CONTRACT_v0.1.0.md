# 결정론 계약 — Language SPEC v0.1.0

> trace: Language SPEC `v0.1.0` ← SSOT `v24.14.1` ← byte-identical `v24.14.0` snapshot
> status: pre-release public draft; internal SSOT wins on conflict

## 약속

같은 canonical source, 같은 명시 설정, 같은 `InputSnapshot`, 같은 seed, 같은
봉인 record, 같은 toolchain 계약을 사용하면 또니랑의 정본 세계 상태와
`state_hash`는 동일해야 한다.

## 실행 등급

| 등급 | 재현성 근거 |
|---|---|
| 닫힘 | 외부 입력을 deny한다. |
| 봉인된 열림 | 외부 입력을 record하고 replay한다. |
| 생열림 | live 입력을 사용한다. 재현 가능하다고 주장하지 않는다. |

재현 근거로 인정하는 것은 deny/record/replay뿐이다. 외부 bridge나 AI가 runtime
truth를 우회 소유할 수 없다.

## hash 경계

- 포함: 정본 세계 상태와 명시적으로 계약된 상태 값.
- 제외: view, debug 표시, 진단 UI, 발화 메타, 사후 거울 요약.
- 보개·Manim·브라우저 픽셀·GPU 렌더는 결정론 소비자가 될 수 있지만 그 bytes를
  이 언어 초안이 bit-identical로 약속하지 않는다.

쓰기 phase는 고정되고 같은 phase·같은 대상 충돌은 기본 오류다. 순환 흐름은
암묵 fixpoint가 아니라 명시 오류다. 이 규칙은 결과가 우연히 같다는 수준을
넘어 원인을 감사할 수 있게 하기 위한 계약이다.
