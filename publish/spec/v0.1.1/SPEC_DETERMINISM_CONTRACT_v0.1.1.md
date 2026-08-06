# 결정론 계약 — Language SPEC v0.1.1

> trace: Language SPEC `v0.1.1` ← owner-approved SSOT `v24.14.2` administrator candidate
> status: current pre-release public draft; installed SSOT remains v24.14.1 until protected apply
> authority: internal current SSOT wins on conflict


## 약속

같은 canonical source, 같은 명시 설정, 같은 `InputSnapshot`, 같은 `씨앗값`, 같은
봉인 record, 같은 toolchain 계약을 사용하면 또니랑의 정본 세계 상태와
`state_hash`는 동일해야 한다.

## 실행 등급

| 등급 | 재현성 근거 |
|---|---|
| 닫힘 | 외부 입력을 deny한다. |
| 봉인된 열림 | 외부 입력을 record하고 replay한다. |
| 생열림 | live 입력을 사용한다. 재현 가능하다고 주장하지 않는다. |

## 설정 digest 경계

| 사용자 표시명 | wire/schema id | 책임 |
|---|---|---|
| `실행설정해시` | `run_config_hash` | 결과에 영향을 주는 설정 |
| `보기설정해시` | `view_config_hash` | 보기·재현 설정 |
| `문서설정해시` | `doc_config_hash` | 제목·설명 등 문서 메타 |
| `설정해시` | `settings_hash` | 위 digest의 감사 envelope |

영어 이름은 사용자 언어 표면을 영어로 바꾸는 결정이 아니라 wire/schema의 안정
식별자다. 이 네 digest의 계산·기록·불일치 처리는 별도 제품 evidence gate다.

## 씨앗묶음 결정론 원칙

- 이름 있는 stream은 root `씨앗값`과 stream 이름으로 domain separation한다.
- stream 하나를 추가해도 다른 stream 난수열이 흔들리면 안 된다.
- world-affecting 난수 입력은 `InputSnapshot` 또는 replay 가능한 기록에 봉인한다.
- view-only 난수는 `state_hash`를 바꾸지 않는다.

이 원칙은 canonical design이다. isolation/runtime/replay pack이 닫히기 전에는
`씨앗묶음` 제품 구현 완료를 주장하지 않는다.

쓰기 phase는 고정되고 같은 phase·같은 대상 충돌은 기본 오류다. 순환 흐름은 암묵
fixpoint가 아니라 명시 오류다.
