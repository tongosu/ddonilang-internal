# 의미 핵심 — Language SPEC v0.5.0 후보

> 상태: `public candidate / independent review required / not current / docs-first / product-open`
> trace: Language SPEC `v0.5.0` candidate ← internal live SSOT `v24.24.1`
> 현 공개판: Language SPEC `v0.4.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 후보와 parser/runtime/default-product 지원을 분리한다.

## 값·참조·실패

- 일반 값과 불변 collection은 값 의미론이다.
- 정체성 참조값은 `(owner space, target ID, generation)`의 작은 불변 값이다.
- 참조 복사는 손잡이 값만 복사하며 대상·소유권·수명·변경 권한을 복사하지 않는다.
- 삭제된 대상은 `끊김`이고 다른 대상에 재연결하거나 부활하지 않는다.
- 참조 읽기는 불변 snapshot을 `맺음`으로 돌려준다.

## 수와 단위

- overflow를 wrap·saturate로 숨기지 않는다.
- 상수 overflow는 compile error, runtime overflow와 0 나눗셈은 구조화 실패다.
- 같은 차원 단위량은 계산·동등성·hash 전에 canonical unit으로 환산한다.
- 점 온도와 온도 간격을 구분한다.
- `mol`을 입자 수로 거짓 exact 자동 변환하지 않는다.
- 계산 반올림은 의미값·receipt에 참여하고 표시 반올림은 화면 문자열만 바꾼다.

## 함수와 효과

- 함수값은 생성 시 자유 변수의 불변 snapshot만 갈무리한다.
- 누리 전체, live mutable 값, 숨은 실행 문맥을 갈무리하지 않는다.
- 기대 함수씨가 있는 값 자리에서만 이름 있는 셈씨를 함수값으로 만든다.
- 골라부름·정의 ID·호출 graph·효과·순도를 생성 때 한 번 봉인한다.
- 함수값은 일반 equality·ordering·set 원소·map 열쇠가 아니다.
- 효과는 표준 registry의 version·contract hash와 함께 봉인한다.

## 모듈과 잠금

- 기계 파일명은 `ddn.lock`, 사용자 설명말은 `잠금글`이다.
- 실제 의존 가지를 실행할 때만 존재·정본 바이트·출처·알맹이를 재검증한다.
- 이름 연결은 검증된 가지엮음과 공개 이름표를 거치며 내장 fallback을 금지한다.
- exact wire와 `얼개` migration은 OPEN이므로 이 문서는 제품 파일 형식을 만들지 않는다.

## 선언형 모델 의미

ModelDefinition·ModelInstance·SolveRecipe·RunRequest는 identity와 권한이 다른
객체다. authored relation, semantic relation, lowered node의 순서도 분리한다.
같은 대상의 복수 producer는 기본 거부하며 명시 CommitResolutionPolicy만
예외다. accepted commit 전 sample을 공개하지 않는다.

이 내부 의미 계약과 공통 모형 docs-first 문법은 parser·typed IR·solver 제품
지원, 일반 DAE, IDA adapter, remote solver 또는 확률 분포 지원을 뜻하지 않는다.

## 지식 장면·보기 합성

- 표준 보기와 사용자 보기는 같은 DDN·자료·모양·장면·artifact·lock 경로를 쓴다.
- 자료→변환→척도·좌표→표시→도표값→보기값/장면요소값을 분리한다.
- typed 자료열은 source·TypeId·단위·작성 순서·run·branch·madi·emission과
  `present/gap/missing/pruned`를 보존한다.
- 효과는 sealed 입력과 절대 장면 시간의 순수 함수라는 방향만 current이며
  exact 문법·schema·ABI·카메라·보간·수명 알고리즘은 OPEN이다.

## 공통 모형

- 모형 머리는 외부 결속과 권한, 몸통은 축·상태·미지수·관계·사건·합성을 소유한다.
- `::`는 typed AST로 보존하는 닫힌 성질이며 알 수 없는 항목·중복·충돌은 오류다.
- 고정 초기값·solver 어림값·관계로 계산할 값을 구분하고 생략으로 추측하지 않는다.
- 동시 사건과 같은 대상 다시놓기 충돌은 source order로 고르지 않고 fail-closed다.
- N항 `잇기`는 값 동일 관계와 안쪽 방향 부호합 0의 흐름 관계로 낮추며
  원래 instance path와 provenance를 보존한다.
- `풀기` 요청은 schema 검사 뒤 SolveRecipe와 RunRequest로 분리·봉인한다.
