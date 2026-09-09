# 또니랑 V1 빠른 시작 — PRE_RELEASE

```text
PRODUCT_RELEASED=NO
EXTERNAL_USER_COUNT=0
OFFICIAL_INSTALL_PATH=NOT_AVAILABLE
VERIFIED_PUBLIC_EXAMPLE_COUNT=0
```

현재 V1은 출시 전이다. 따라서 이 문서는 존재하지 않는 설치 파일, 명령 이름, 실행 옵션 또는 지원 문법을 미리 약속하지 않는다.

## 지금 확인할 수 있는 것

1. [SUPPORT_MATRIX.md](./SUPPORT_MATRIX.md)에서 원하는 기능의 상태를 확인한다.
2. `SUPPORTED_FOR_V1`이 아닌 기능은 공식 V1 제품에서 사용할 수 있다고 가정하지 않는다.
3. `PRODUCT_PASS_MEMBERSHIP_PENDING`도 아직 공식 지원이 아니다.
4. 공개 언어의 의미를 연구하려면 Language SPEC v0.6.0을 참고하되, 제품 지원표와 분리해 읽는다.

## 공식 빠른 시작이 열리는 조건

다음이 하나의 고정 제품 산출물에 대해 검증된 뒤 설치·실행 절차와 첫 예제를 추가한다.

- 공식 executable identity와 작은 public command surface
- public/default V25 source ingress
- 동일 원문에 대한 parser/type/canon/runtime 경로
- 필요한 native/WASM/Workbench 정합
- clean-machine 설치·실행
- fixed-target 독립 제품 PASS
- Owner의 V1 membership·공개 활성 승인

## 코드 예제 정책

현재 공개 quickstart에 승인된 코드 예제는 0개다. 제품 경로에서 실행되지 않은 예시나 문서 작성자가 추측한 문법은 추가하지 않는다.
