# ARTIFACT_POLICY.md

> 이 저장소의 산출물, 임시 파일, 공개 파일, 정본 파일을 구분하는 정책.

## 분류

| 분류 | 위치 | 정본 여부 | 규칙 |
|---|---|---|---|
| SSOT 정본 | `docs/ssot/**` | 예 | 에이전트 직접 수정 금지 |
| 제품 소스 | `core/`, `lang/`, `tool/`, `tools/teul-cli/`, `solutions/` | 예 | 테스트와 함께 변경 |
| 실행 근거 | `pack/`, `tests/`, `golden/` | 예 | 결정적 비교 가능해야 함 |
| 개발 문서 | `docs/context/**`, `docs/reports/**`, `docs/status/**`, `docs/steps/**` | 부분 | SSOT 전까지 비정본 |
| 공개 문서 | `publish/` | 공개용 사본 | 내부 문서와 분리 |
| 로컬 빌드 | `I:/home/urihanl/ddn/codex/build` 또는 `C:/ddn/codex/build` | 아니오 | 배포 대상 아님 |
| 로컬 산출 | `I:/home/urihanl/ddn/codex/out` 또는 `C:/ddn/codex/out` | 아니오 | 검토/임시 산출 |
| 세션 작업 | `work/<agent>/YYYYMMDD_task/` | 아니오 | 검토 후 승격 또는 보관 |
| 원본 투입 | `_inbox/` | 원본 | 직접 편집 금지 |
| 작업 사본 | `inputs/` | 아니오 | 원본에서 복사해 작업 |
| 보관 | `_archive/` | 아니오 | 삭제 대신 보관 |

## 내부 문서와 공개 투영

`docs/`는 미출시 내부 문서를 공개 저장소에 올리지 않기 위해 Git에서 제외한다.
문서가 ignored라는 사실은 임시, 폐기 가능, 비권위를 뜻하지 않는다.

- 내부 상세 상태: `docs/status/**`
- 내부 최신 개발 요약: `docs/context/all/DEV_SUMMARY.md`
- 공개 가능한 간결한 상태 투영: 루트 `PROJECT_STATUS.md`, `CHANGELOG.md`
- 외부 공개 문서: `publish/**`

보고서는 다음 집을 사용한다.

- `docs/context/reports/`: legacy redirect/색인. 새 완료 보고서 추가 금지.
- `docs/reports/audit/`: 완료된 감사.
- `docs/reports/impl/`: 완료된 구현·검증 보고.
- `docs/reports/rationalization/`: 완료된 저장소·문서 구조 합리화 보고.
- 작업 중 초안: `work/<agent>/<task>/`.

## build/out 경로

새 로컬 산출물은 저장소 루트의 `build/` 또는 `out/`보다 아래 경로를 우선한다.

```text
I:/home/urihanl/ddn/codex/build
I:/home/urihanl/ddn/codex/out
```

위 경로가 없으면 아래를 사용한다.

```text
C:/ddn/codex/build
C:/ddn/codex/out
```

기존 스크립트가 루트 `build/` 또는 `out/`을 쓰는 경우에는 그 동작을 임의로 바꾸지 않는다.

pack/test 실행의 Cargo target도 pack 폴더 안에 만들지 않는다. `CARGO_TARGET_DIR` 또는
`DDN_PACK_GOLDEN_CARGO_TARGET_DIR` 지정값을 우선하고, 없으면 위 외부 build 경로 아래의
`cargo-target-pack-golden`을 사용한다.

## 승격 규칙

임시 산출물이 장기 의미를 가지려면 아래 중 하나로 승격한다.

- 구현 근거: `pack/` 또는 `tests/`
- 개발 요약: `docs/context/all/DEV_SUMMARY.md`
- 설계/정책 제안: `docs/context/proposals/`
- 공개 문서: `publish/`
- 릴리스 바이너리: GitHub Releases

`work/`, `build/`, `out/`, `_inbox/`, `inputs/`, `_archive/`의 파일은 그 자체로 SSOT나 완료 근거가 아니다.

## 원본과 사본

- 외부에서 받은 원본은 `_inbox/`에 둔다.
- 원본은 직접 편집하지 않는다.
- 분석/변환/정리는 `inputs/` 또는 `work/<agent>/`의 사본으로 한다.
- 재사용 가능한 산출물은 검토 후 프로젝트의 기존 도메인 폴더로 옮긴다.

## 대량 이동

파일을 많이 옮기기 전에는 이동 계획을 작성한다.

필수 필드:

- source path
- target path
- reason
- sha256
- 실행 전 상태
- 실행 후 상태

불확실한 파일은 삭제하지 않는다. 보존이 필요하면 `_archive/`로 보낸다.
