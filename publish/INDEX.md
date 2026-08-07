# 또니랑 공개 문서 목록

이 목록은 GitHub 사용자에게 현재 안내할 문서와 감사 목적으로 보존하는 문서를
구분합니다.

## 현재 진입점

| 문서 | 목적 | 갱신 조건 |
| --- | --- | --- |
| [`../README.md`](../README.md) | GitHub 첫 화면과 프로젝트 소개 | 제품 방향·공개 기준선 변경 |
| [`README.md`](README.md) | 공개 문서 허브 | 공개 문서 구조 변경 |
| [`QUICKSTART.md`](QUICKSTART.md) | CLI 첫 실행과 선택적 작업실 실행 | 첫 실행 경로 변경 |
| [`LEARNING_PATH.md`](LEARNING_PATH.md) | 0~5층 학습 순서 | 사용자 표면·선행 관계 변경 |
| [`PRODUCT_SUPPORT_CURRENT.md`](PRODUCT_SUPPORT_CURRENT.md) | docs-first·제품 근거·OPEN 구분 | 제품 기준선·검증 상태 변경 |
| [`spec/CURRENT.md`](spec/CURRENT.md) | 공개 Language SPEC current | 공개 SPEC 승격 |
| [`i18n/INDEX.md`](i18n/INDEX.md) | 17개 다국어 starter 문서 | 기준 소개·번역 상태 변경 |
| [`DOWNLOADS.md`](DOWNLOADS.md) | 바이너리·소스 배포 경계 | 릴리스 방식 변경 |
| [`LOCALIZATION.md`](LOCALIZATION.md) | 다국어 운영 규칙 | 번역 정책 변경 |

## 참고 문서

| 문서 | 역할 |
| --- | --- |
| [`ddonirang_grammar_summary.md`](ddonirang_grammar_summary.md) | 발표용 문법 요약 |
| [`ddonirang_grammar_full.md`](ddonirang_grammar_full.md) | 전체 문법 참고 자료 |
| [`DDONIRANG_DEV_STRUCTURE.md`](DDONIRANG_DEV_STRUCTURE.md) | 개발 구조 참고 자료 |
| [`examples/00_first_result.ddn`](examples/00_first_result.ddn) | 첫 실행 DDN 예제 |

참고 문서가 현재 Language SPEC 또는 제품 지원표와 충돌하면 SPEC과 제품 지원표를
우선합니다.

## 고정 Language SPEC 계보

- current: [`v0.5.0`](spec/v0.5.0/SPEC_MANIFEST_v0.5.0.md)
- 이전 public current: [`v0.4.0`](spec/v0.4.0/SPEC_MANIFEST_v0.4.0.md)
- 검토 후보·자체 검사 실패판: [`spec/CURRENT.md`](spec/CURRENT.md)의 감사 계보
- v0.3.0과 이전판: 역사적 공개 스냅숏

봉인된 SPEC family는 소개 문서 정리 과정에서 이름을 바꾸거나 제자리 수정하지
않습니다.

## 다국어 파일 경계

- 정본 위치: `publish/i18n/<언어 코드>/`
- 기존 `publish/README_<언어>.md`: 과거 링크를 새 위치로 연결하는 호환 안내
- 번역 상태: `starter translation / Human review open` 또는 사람 검토 완료
- 번역 문서는 언어 의미의 정본이 아닙니다.

## 역사 보존

- [`RELEASE_NOTES_20260211.md`](RELEASE_NOTES_20260211.md)는 당시 릴리스 기록으로
  보존합니다.
- 검토가 끝난 `GITHUB_RELEASE_DRAFT_20260211.md`와 내부 CI 수정 메모는 현재 공개
  문서에서 제거했습니다. Git 이력에는 남아 있습니다.

## 공개 제외

다음은 GitHub 사용자 문서가 아닙니다.

- private `docs/ssot/**`, owner 결정 원문, Work 세션 기록
- `build/`, `out/`, `target/`, 캐시와 검사 로그
- 비밀정보·개인정보·고객 제한 자료
- 검증되지 않은 연구 원문과 대규모 임시 산출물
