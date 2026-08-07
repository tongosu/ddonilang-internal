# 공개 문서 다국어 운영 기준

## 정본 위치

다국어 공개 문서는 `publish/i18n/<언어 코드>/`를 단일 정본 위치로 사용합니다.
기존 `publish/README_<언어>.md`는 과거 외부 링크를 깨지 않기 위한 짧은 안내만
유지하며 번역 본문을 중복 보관하지 않습니다.

## 현재 언어

| 코드 | 언어·표기 | 상태 |
| --- | --- | --- |
| ko | 한국어 | 기준 안내 |
| en | English | starter / Human review open |
| ja | 日本語 | starter / Human review open |
| tr | Türkçe | starter / Human review open |
| mn | Монгол | starter / Human review open |
| ay | Aymara | starter / Human review open |
| eu | Euskara | starter / Human review open |
| kn | ಕನ್ನಡ | starter / Human review open |
| ne | नेपाली | starter / Human review open |
| qu | Runasimi | starter / Human review open |
| sym3 | sym3 | compact starter |
| ta | தமிழ் | starter / Human review open |
| te | తెలుగు | starter / Human review open |
| zh | 中文 | starter / Human review open |
| es | Español | starter / Human review open |
| fr | Français | starter / Human review open |
| de | Deutsch | starter / Human review open |

## 각 묶음의 파일

- `README.md`: 프로젝트 소개와 상태 경계
- `QUICKSTART.md`: 첫 CLI 실행과 선택적 작업실 실행
- `DEV_STRUCTURE.md`: 공개 개발 구조 starter
- `DOWNLOADS.md`: 배포 경계
- `RELEASE_NOTES_20260211.md`: 역사적 릴리스 기록

## 생성과 검증

`tools/scripts/generate_public_intro_i18n.mjs`가 17개 언어의 README와 QUICKSTART,
기존 `README_<언어>.md` 호환 안내를 결정적으로 생성합니다.

```sh
node tools/scripts/generate_public_intro_i18n.mjs
python tools/check_public_docs.py
```

생성기를 다시 실행했을 때 같은 바이트가 나와야 합니다.

## 번역 경계

- DDN 코드, 명령, 파일 경로, schema와 오류 코드는 번역하지 않습니다.
- 내부 SSOT와 공개 Language SPEC이 언어 의미를 소유합니다.
- 자동·AI 번역은 starter이며 사람 검토를 통과하기 전 완성 번역으로 표시하지 않습니다.
- 제품 지원 상태는 번역 문서가 독자적으로 올리지 않습니다.
- 한국어 기준 문서가 바뀌면 모든 starter를 함께 재생성합니다.
- 사람 검토 교정은 생성기 데이터에도 반영해 다음 재생성에서 사라지지 않게 합니다.
