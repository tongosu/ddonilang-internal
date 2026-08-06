# 또니랑 언어 소개 — Language SPEC v0.1.1

> trace: Language SPEC `v0.1.1` ← owner-approved SSOT `v24.14.2` administrator candidate
> status: current pre-release public draft; installed SSOT remains v24.14.1 until protected apply
> authority: internal current SSOT wins on conflict


또니랑은 한국어로 세계의 상태, 시간, 원인과 실험을 표현하는 결정론 모델링
언어다. 범용 언어를 대체하기보다 Scratch 다음, Python 전에 놓이는 첫 텍스트
모델링 언어를 지향한다.

## 무엇을 배우는가

- 값과 상태를 구분하고, 상태 변화의 원인을 문장으로 남긴다.
- 고정된 `마디`를 따라 같은 입력이 같은 결과를 만드는 세계를 구성한다.
- 포물선·단위·미분·관계 같은 수학·과학 모델을 실행하고 비교한다.
- AI 도움은 작성 도구로 사용하되 실행 세계의 권위와 분리한다.

## v0.1.1에서 정리한 사용자 계약

- 난수 문맥의 일반말은 `씨앗`, 숫자 설정·code key는 `씨앗값`, 이름 있는 난수
  흐름 묶음은 `씨앗묶음`이다.
- `시앗`, `시앗묶음`은 deprecated 입력 호환 별칭이며 새 정본 출력에 쓰지 않는다.
- settings는 여덟 중첩 절이 소유하고, 평면 `제목/설명/마디수`는 닫힌 이행 입력이다.
- 설정 digest의 사용자 표시는 한국어, wire/schema 식별자는 영어로 분리한다.
- 가지 registry의 사용자-facing generic 이름은 `가지곳간`이다.

## 핵심 경계

- 사용자·AI가 쓰는 결정론 모델 로직은 이야기 층에 둔다.
- 외부 입력은 `InputSnapshot`을 거쳐야 세계 의미에 참여한다.
- 보개·시각화·디버그 표시는 세계 상태를 바꾸지 않는 소비자다.
- 이 문서는 출시 전 공개 초안이다. 설계 확정, 호환 입력, 구현 완료를 구분한다.

`씨앗`은 기존 언어에서 이름 붙은 계산·함수 family를 가리키기도 한다. 난수 설정의
code key는 항상 `씨앗값`이라고 써서 두 문맥을 구분한다.
