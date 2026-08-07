# 또니랑 공개 개발 구조

> 현재 공개 저장소를 이해하기 위한 짧은 안내입니다. 언어 의미의 기준은
> [Language SPEC current](spec/CURRENT.md)이며, 실제 제품 지원 범위는
> [제품 지원 현황](PRODUCT_SUPPORT_CURRENT.md)을 따릅니다.

## 주요 코드 영역

| 영역 | 경로 | 책임 |
| --- | --- | --- |
| 결정적 엔진 | `core/` | 승인된 세계 상태의 전이와 기록 |
| 언어 | `lang/` | 문법, 파서, 정본화 |
| 수·기호·증명 | `numeric/`, `symbolic/`, `proof/` | 경계가 정해진 계산·증명 커널 |
| 실행 도구 | `tool/` | 공통 실행 진입점과 WASM API |
| 명령줄 도구 | `tools/teul-cli/` | CLI 실행과 공개 검증 |
| 셈그림 | `solutions/seamgrim_ui_mvp/` | 브라우저 작업대와 보기 계층 |
| 공개 문서 | `publish/` | 안내서와 봉인된 공개 SPEC 계보 |

## 다섯 실행 층

내부 실행 구조는 다음 다섯 층을 구분합니다.

1. **샘(Sam)** — 입력
2. **이야기(Iyagi)** — 선언과 프로그램 의미
3. **누리(Nuri)** — 승인된 세계 상태
4. **거울(Geoul)** — 기록·감사·재현
5. **보개(Bogae)** — 보기와 표현

이는 구현 구조를 설명하는 이름이지 초보자가 모두 직접 다뤄야 하는 문법은 아닙니다.
AI는 이 다섯 층 위에서 제안하거나 돕는 도구일 수 있지만, 숨은 여섯째 실행 권한을 갖지
않습니다.

## 공개 검증 경계

- GitHub 공개 CI는 공개 코드 테스트, 선택된 golden, 공개 SPEC seal, 첫 CLI 예제를 검사합니다.
- 이 검사는 전체 브라우저 제품, 모든 docs-first 문법, Human 화면 검토, 비공개 SSOT 관문을
  완료했다는 증거가 아닙니다.
- 언어·런타임 지원은 테스트 전용 Python/JavaScript 변환이 아니라 실제 `lang`·`tool`·CLI·WASM
  제품 진입점에 있어야 합니다.
- renderer는 CSS, 프로젝트 제목, metadata, 파일 순서에서 숨은 의미를 추측하지 않습니다.

## 문서 우선순위

1. 공개 언어 의미: [Language SPEC current](spec/CURRENT.md)
2. 구현 지원 여부: [제품 지원 현황](PRODUCT_SUPPORT_CURRENT.md)
3. 시작 방법: [빠른 시작](QUICKSTART.md)
4. 다국어 안내: [다국어 색인](i18n/INDEX.md)

내부 SSOT와 공개 SPEC은 별도 계보입니다. 문서에 적힌 설계가 곧 parser/runtime/browser에
구현됐다는 뜻은 아닙니다.
