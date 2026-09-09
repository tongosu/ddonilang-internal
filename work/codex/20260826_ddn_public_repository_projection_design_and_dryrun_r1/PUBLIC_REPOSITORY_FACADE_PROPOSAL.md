# Public repository facade proposal

## R1 권고

초기 공개판에서는 내부 source path를 대규모로 예쁘게 개명하지 않는다. path remap은 build/import/link를 깨뜨릴 위험이 크다. 대신 top-level facade와 공개 문서, examples index, CI를 정돈하고 내부 구조는 안정된 뒤 단계적으로 정리한다.

```text
README.md                 무엇인지, 바로 보기, 현재 지원 범위
QUICKSTART.md             CLI와 Workbench 첫 실행
LICENSE                   Owner 결정 뒤 추가
SECURITY.md               취약점 제보 경계
CONTRIBUTING.md           public contribution 정책
SUPPORT.md                current/experimental/open 표
publish/spec/             Language SPEC public current
core/ lang/ ... tool/     제품 source
tools/teul-cli/           후속에서 public 명칭을 cli로 수렴할지 별도 결정
solutions/seamgrim_ui_mvp/ Workbench 제품과 예제
pack_public/              검증된 public packs만
tests/                    최소 public conformance closure만
```

## 첫 화면에서 보여줄 예제

- 30초: 선 그래프 또는 포물선 실행
- 2분: projectile 값 편집 후 다시 실행
- 5분: 진자/space2d 보기
- 놀이: mini tetris, maze, bounce
- 언어: symbolic simplify, 등가성 증명
- 데이터: table/structure/text payload

각 예제는 `SUPPORTED`, `EXPERIMENTAL`, `INTERNAL_ONLY`, `OPEN` 중 하나로 표시해야 한다. 존재하는 샘플이 곧 public stable support를 뜻하지 않는다.

## 저장소 이름 제안

- 내부 기존 저장소: `ddonilang-internal` 또는 현재 이름 유지 후 private
- 새 공개 저장소: `ddonilang` 또는 `ddonilang-public`

추천은 기존 원격을 먼저 private internal custody로 확정하고, 새 공개 저장소는 최종 이름 `ddonilang`을 쓰는 것이다. 단, 기존 URL 사용자/링크가 이미 있으면 redirect 영향 감사를 먼저 한다.
