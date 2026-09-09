#!/usr/bin/env python3
"""Apply the owner-approved SSOT v24.17.1 and public Language SPEC v0.3.0.

This is an administrator projection tool.  It never edits v24.17.0 or v0.2.1
files in place.  `--check` verifies the generated family and its seals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SSOT_ROOT = DOCS / "ssot"
SSOT = SSOT_ROOT / "ssot"
REG = SSOT / "registries"
BASE = SSOT_ROOT / "releases" / "v24.15.1-recovery-lineage" / "snapshot"
PUBLIC = ROOT / "publish" / "spec"
DECISION = (
    DOCS
    / "decisions"
    / "SSOT_V24_17_1_AND_LANGUAGE_SPEC_V0_3_0_FINAL_PROMOTION_DECISION_20260726.md"
)
GENERATOR_REL = "tools/apply_ssot_v24_17_1_and_public_spec_v0_3_0_admin.py"

INTERNAL_VERSION = "v24.17.1"
PREVIOUS_INTERNAL_VERSION = "v24.17.0"
PUBLIC_VERSION = "v0.3.0"
PREVIOUS_PUBLIC_VERSION = "v0.2.1"
DATE = "2026-07-26"


SOURCE_SPECS = [
    ("GATE0_IMPLEMENTATION_CHECKLIST", "Gate0 구현 체크리스트"),
    ("README", "또니랑 SSOT 읽기 안내"),
    ("SSOT_DECISIONS", "결정"),
    ("SSOT_DEMOS", "대표 예제"),
    ("SSOT_INDEX", "목차"),
    ("SSOT_LANG", "언어"),
    ("SSOT_MASTER", "통합 정본"),
    ("SSOT_OPEN_ISSUES", "열린 제품 관문"),
    ("SSOT_PENDING", "보류·소유 재분류"),
    ("SSOT_PLANS", "실행 계획"),
    ("SSOT_PLATFORM", "제품·플랫폼"),
    ("SSOT_REVIEW_RESULT_20260430", "검토 결과"),
    ("SSOT_ROADMAP_CATALOG", "로드맵"),
    ("SSOT_TERMS", "용어"),
    ("SSOT_TOOLCHAIN", "도구 사슬"),
    ("SSOT_UPDATE_NOTES", "변경 기록"),
    ("SSOT_BOOK_SYSTEM_AND_COMPENDIUM_POLICY", "책·총집 정책"),
    ("SSOT_PROGRAMMING_CONCEPT_LEDGER", "프로그래밍 개념 장부"),
]

REGISTRY_SPECS = [
    ("STDLIB_SURFACE_REGISTRY", "표준 가지 표면"),
    ("CLI_COMMAND_REGISTRY", "CLI 명령"),
    ("SCHEMA_EXISTENCE_REGISTRY", "schema 존재"),
    ("SCHEMA_CONTRACT_REGISTRY", "schema 계약"),
    ("DIAGNOSTIC_EXISTENCE_REGISTRY", "진단 존재"),
    ("DIAGNOSTIC_CONTRACT_REGISTRY", "진단 계약"),
    ("DECISION_INPUT_DISPOSITION_REGISTRY", "결정 입력 처분"),
    ("OI_FAMILY_REGISTRY", "열린 이슈 계열"),
    ("TYPE_SURFACE_REGISTRY", "갈래 표면"),
    ("KUSIL_CONTRACT_REGISTRY", "구실·계약"),
    ("BUILD_PROFILE_REGISTRY", "build profile"),
    ("DIAGNOSTIC_CODE_REGISTRY", "진단 코드"),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def tree_digest(paths: list[Path], root: Path) -> str:
    rows = []
    for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix()):
        rows.append(f"{path.relative_to(root).as_posix()}\0{sha256_file(path)}")
    return sha256_bytes("\n".join(rows).encode("utf-8"))


def source_path(stem: str, version: str, base: Path = SSOT) -> Path:
    return base / f"{stem}_{version}.md"


def registry_path(stem: str, version: str, base: Path = REG) -> Path:
    return base / f"{stem}_{version}.md"


def inherited_preamble(stem: str) -> str:
    base_path = source_path(stem, "v24.15.1", BASE)
    overlay_path = source_path(stem, PREVIOUS_INTERNAL_VERSION)
    if not base_path.exists():
        raise FileNotFoundError(base_path)
    if not overlay_path.exists():
        raise FileNotFoundError(overlay_path)
    return f"""## 명시적 계승 조립

- 규범 기반: `../releases/v24.15.1-recovery-lineage/snapshot/{base_path.name}`
  (`sha256:{sha256_file(base_path)}`)
- 선행 overlay: `{overlay_path.name}`의 `V24_17_ACTIVE_BEGIN/END` 블록
  (`sha256:{sha256_file(overlay_path)}`)
- 최종 owner 결정: `../../decisions/{DECISION.name}`
  (`sha256:{sha256_file(DECISION)}`)
- 우선순위: 이 파일의 `V24_17_1_ACTIVE_BEGIN/END` > v24.17.0 active overlay >
  v24.15.1 파일 자체의 당시 current 경계
- 과거 파일의 HISTORY 블록과 폐기·대체된 표면은 계승하지 않는다.
- 문서의 `current`는 규범 효력을 뜻하며 제품 구현 완료를 뜻하지 않는다.
"""


DECISION_ROWS = """| id | 상태 | 결정 |
|---|---|---|
| RD-001 | RESTORE-ACTIVE | 복구판과 유실 역사판을 구분하고 재현하지 못한 역사판을 가장하지 않는다. |
| RD-002 | RESTORE-ACTIVE | 부재 판정은 표적 재검색 뒤에만 하며 어느 층에 없는지 명시한다. |
| RD-003 | RESTORE-ACTIVE | source/reflection/implementation/owner 네 축을 분리한다. 반영은 구현이 아니다. |
| RD-004 | RESTORE-ACTIVE | 셈그림은 DDN 결정적 프로젝트 작업대다. 교육 플레이어·노트북·Manim 전용기로 축소하지 않는다. |
| RD-005 | RESTORE-ACTIVE | 승인 UI 기준선의 임의 변경을 금지하고 대안·승인 절차를 요구한다. |
| RD-006 | SPLIT | DDN과 주된 보개 중심, 고정 왼쪽 레일 금지, 한 파일 탐색기 숨김은 유지한다. 고정 75% 비율은 RD-037이 대체한다. |
| RD-007 | RESTORE-ACTIVE | DDN 찾기·공식 모음·내 작업은 전역 탐색 공간이다. |
| RD-008 | RESTORE-ACTIVE | 공식 모음은 봉인 판본을 가리키는 순서 있는 다중 소속 collection이다. |
| RD-009 | RESTORE-ACTIVE | 원판·저자·갈라 저장·리믹스 계보를 구분한다. |
| RD-010 | RESTORE-ACTIVE | 실행 전 채비, 실행 중 행동, 보기 설정을 분리한다. |
| RD-011 | SUPERSEDED | RD-021·RD-024·RD-039가 대체한다. |
| RD-012 | SUPERSEDED | RD-026·RD-027이 대체한다. |
| RD-013 | RESTORE-ACTIVE | 주된 보기 역할은 필요하다. UI 노출 용어는 host 표현으로 둔다. |
| RD-014 | SUPERSEDED | RD-024·RD-030·RD-035가 대체한다. |
| RD-015 | RESTORE-ACTIVE | 학생·교사 역할은 배포 구성이고 잠금·정답 숨김·조절 범위는 배포 무결성에 속한다. |
| RD-016 | SPLIT | 한국어 Manim 결합 정체성과 반응형 연출은 유지한다. 시간·카메라 세부는 RD-029~033이 소유한다. |
| RD-017 | RESTORE-ACTIVE | 교과는 수학·물리·화학·경제·역사를 포괄하고 역사 자료에는 봉인·증거등급이 필요하다. |
| RD-018 | RESTORE-ACTIVE | 공통 코어와 표준·사용자 가지를 같은 계약으로 순환한다. |
| RD-019 | RESTORE-ACTIVE | 만들기·저장·재열기·공유·리믹스를 제품 최우선으로 둔다. |
| RD-020 | RESTORE-ACTIVE | 실제 입력·실행 증거 전에는 외부 성공을 주장하지 않는다. |
| RD-021 | KEEP-ACTIVE | 살아있는 세계 공개는 명시적 공개 관찰만 허용한다. |
| RD-022 | KEEP-ACTIVE | 관찰 이름·갈래·단위·source ref를 봉인하고 희소 표본 상태를 구분한다. |
| RD-023 | REPLACED | 정본은 `(이름: 값, ...) 보임.`이다. `보임 {}`와 합성 영어 ID는 REMOVED-PRE-USER다. |
| RD-024 | KEEP-ACTIVE | 보개 프로그램은 검증된 읽기 원천만 소비하고 세계를 직접 쓰지 않는다. |
| RD-025 | KEEP-ACTIVE | 입체·평면·글칸은 출력 profile이고 그래프·표·글은 일반 장면 요소다. |
| RD-026 | KEEP-ACTIVE | 으뜸·겹·곁·돋은 보기 사이의 관계·활성화·수명이다. |
| RD-027 | KEEP-ACTIVE | 관계별 활성화·지역 상태 보존·종료 수명을 명시한다. |
| RD-028 | KEEP-ACTIVE | 작성된 의미 보개는 최초 중심 하나를 명시하고 숨은 자동 승격을 금지한다. |
| RD-029 | KEEP-ACTIVE | 세계 마디·장면 cursor·출력 frame을 분리한다. |
| RD-030 | KEEP-ACTIVE | SceneCompositionV1·ResolvedSceneTraceV1·ResolvedSceneFrameV1은 내부 docs-first 산출물이다. |
| RD-031 | KEEP-ACTIVE | 효과의 같은 target/property 중첩은 오류이며 last-write-wins를 금지한다. |
| RD-032 | KEEP-ACTIVE | 변형 대응은 명시 mapping·semantic ID·lineage·unmatched fade 순이다. |
| RD-033 | KEEP-ACTIVE | camera intent·state·renderer lowering의 소유를 분리한다. |
| RD-034 | KEEP-ACTIVE | 표준 가지 받는자리는 출처·갈래/차원·읽는때 세 축을 선언한다. |
| RD-035 | KEEP-ACTIVE | 장면·모양·관찰·그래프·표·보기·배움·평가를 일반 표준 가지로 제공한다. |
| RD-036 | KEEP-ACTIVE | 지역 보기 사건과 세계 action intent/InputSnapshot을 분리한다. |
| RD-037 | KEEP-ACTIVE | UI는 의미 hint에서 유도하되 host가 layout을 소유하고 결정적 fallback을 제공한다. |
| RD-038 | KEEP-ACTIVE | 학습·평가를 일반 값과 잠긴 프로그램으로 제공한다. |
| RD-039 | KEEP-ACTIVE | 모든 사용자 가시 의미에 완전한 source chain을 요구하고 N1~N10을 제품 관문으로 둔다. |
| RD-040 | KEEP-ACTIVE | 첫 통합 수직은 2D 진자이며 3D·이중 진자·MathIR 변형은 후속이다. |
| RD-041 | NEW-CURRENT | 이름씨 정의와 구성은 `(자리...)인 이름`으로 대칭화한다. `인`은 바로 뒤 이름씨만 꾸민다. |
| RD-042 | NEW-CURRENT | 짧은 계약은 `[먼저/내내/마치면] {조건} 아니면 [물림/알림].`이다. |
"""


SV_DECISIONS = """| id | 결정 |
|---|---|
| SV-D01 | 표준 보기와 사용자 보기는 같은 DDN·가지·장면 구성 경로를 쓴다. |
| SV-D02 | 잠긴 표준 artifact의 공개 export와 의미 이름은 한국어로 둔다. |
| SV-D03 | 자료는 공개 관찰 이름과 source ref로 연결하며 이름 문자열로 역할을 추측하지 않는다. |
| SV-D04 | 단일 표준 보기에는 관계 작성을 요구하지 않는다. |
| SV-D05 | 기본값은 표준 가지 판본에 고정하고 확장 결과에 기록한다. |
| SV-D06 | 복제는 독립 이름씨 정의를 만들며 표준 갱신을 자동 적용하지 않는다. |
| SV-D07 | 그래프별 숨은 renderer family 대신 일반 장면 요소를 조합한다. |
| SV-D08 | 계열·범례·표 열·범주의 DDN 작성·선택 순서를 보존한다. |
| SV-D09 | gap·missing에서 선과 자취를 끊고 실행 실패를 빈값으로 숨기지 않는다. |
| SV-D10 | 색만으로 계열·상태를 구분하지 않는다. |
| SV-D11 | seamgrim.graph.v0·JS 추론 경로와 successor를 dual read/write하지 않는다. |
| SV-D12 | 의미는 함께 승인하되 제품은 세로 수직 하나씩 닫는다. |
| SV-D13 | 선반·export·instance·주소 가능한 의미 node에 안정된 한국어 이름을 붙인다. |
| SV-D14 | 보기 선반과 모양 선반을 분리한다. |
| SV-D15 | 최소 평면 모양은 점·선·선들·다각형·사각형·원·글·화살표다. |
| SV-D16 | 최소 입체 모양은 점3d·선3d·상자·구·원기둥·원뿔이다. |
| SV-D17 | 빈 평면·입체 장면도 표준과 사용자에게 같은 구성 경로로 제공한다. |
| SV-D18 | 모양·빈 장면만으로 완료를 주장하지 않고 최소 8개 완성 장면틀을 제공한다. |
"""


STANDARD_VIEW_TABLE = """| ID | export | 역할 |
|---|---|---|
| SV-01 | `현재값` | 현재값 카드 |
| SV-02 | `시간선` | 시간 선그래프 |
| SV-03 | `비교선` | 여러 값 비교그래프 |
| SV-04 | `좌표선` | X-Y 좌표그래프 |
| SV-05 | `흩어진점` | 산점도 |
| SV-06 | `막대` | 막대그래프 |
| SV-07 | `결과표` | 결과표 |
| SV-08 | `위치자취` | 2D 위치·자취 |
| SV-09 | `벡터화살표` | 벡터 화살표 |
| SV-10 | `장면그래프곁` | 장면과 그래프 병치 |
| SV-11 | `장면값겹` | 장면 위 값·그래프 겹치기 |
| SV-12 | `분포막대` | 단순 분포·히스토그램 |
"""


COMMON_OBSERVATION = """## 공개 관찰 정본

```ddn
(시간: 시간, 각도: 각도, 각속도: 각속도) 보임.
```

- 괄호 안은 가변 인자가 아니라 열린 `값꾸러미` 하나다.
- 열린 필드는 `이름: 값`만 허용한다. 고정 받는자리 결합 `이름=값`은 금지한다.
- 필드는 하나 이상이고 이름은 중복될 수 없다.
- `(각도) 보임.`은 `(각도: 각도) 보임.`으로 정본화할 수 있다.
- 이름 없는 식은 명시적 필드 이름 없이는 거부한다.
- DDN 필드 순서를 trace·범례·표 열 끝까지 보존한다.
- `보임 {}`, `project.obs.N`, `output_N`은 `REMOVED-PRE-USER`다.
- 공개 관찰 정체성은 DDN 이름과 source ref다. 영문 wire field는 의미 정체성이 아니다.

## 희소 표본

- 발행 기회 없음은 표본 사건 없음이다.
- 표본 상태는 `present`, `gap`, `missing`, `pruned`다.
- `missing`은 `#계산실패`, `#원천없음`, `#기록손상` 이유를 반드시 가진다.
- 실행 전체 실패와 다른 실행 결합 거부는 개별 표본 빈값으로 숨기지 않는다.
- `gap`·`missing`을 가로질러 선이나 자취를 보간하지 않는다.
"""


LANGUAGE_SURFACES = """## 이름씨와 `인` — RD-041

```ddn
(중심:점2, 반지름:길이, 색:색=#파랑)인
원:이름씨 = {
  먼저 { 반지름 > 0@m } 아니면 물림.
}.

파란원 <- (중심=시작점, 반지름=2@m)인 원.
```

- `인`은 바로 뒤 이름씨에만 결합한다.
- 이름씨가 자격을 부여하며 별도 call-kind를 만들지 않는다.
- `(강제=#켬)인 보고서~를 지우기.`처럼 완성된 임시 이름씨 값을 동작의
  목적어로 넘길 수 있다. 구성은 순수하고 부작용은 뒤 동작이 소유한다.
- `(강제=#켬)인 지우기.`는 금지한다.
- `(x=6) 수식{...}`와 `(x=6)인 직선 풀기`는 기존 수식 주입이며
  이름씨 구성으로 재해석하지 않는다.

## 짧은 계약문 — RD-042

```ddn
먼저 { 반지름 > 0@m } 아니면 물림.
내내 { 반지름 <= 1000@m } 아니면 물림.
마치면 { 색대비 >= 4.5 } 아니면 알림.
```

- 시점은 `먼저`, `내내`, `마치면`이고 처리는 `물림`, `알림`이다.
- 계약이 상태를 자동 수선하지 않는다.
- 기존 Gate0의 명시 수선·1회 재검사 기능은 별도로 보존한다.
- `맡음`과 `맡아야함`은 사실과 요구를 구분해 유지한다.

## 결과와 제한 풀이

- 사용자 정본 결과 표기는 `(된씨)맺음`이다. `맺음<T>`는 사용자 표면이 아니다.
- 무제한 backtracking을 금지한다.
- SolvePlan은 후보 공간·순서·반복 상한과 실패 이유를 봉인한다.
- 외부 solver는 봉인된 이름 있는 비엄격 profile에서만 사용한다.
"""


VIEW_CONTRACT = f"""## 보개 값 모델

- `보개 프로그램`: 공개 관찰과 봉인 자료를 읽어 `보기값`을 만드는 일반 셈씨
- `보기틀`: 이름씨로 정의된 재사용 가능한 구성 틀
- `보기값`: 틀 또는 표준 export를 평가해 얻은 불변 의미 값
- `보기개체`: 실행 중 지역 상태와 수명을 갖는 instance
- `보기관계`: 보기개체 사이의 으뜸·겹·곁·돋 관계값
- profile 공개 이름: `보기.입체`, `보기.평면`, `보기.글칸`
- export 필드 공개 이름: `내보임`
- 사용자 용어: `받는자리계약`; `PinSpec`은 내부 이름

## 표준 보기 12종

{STANDARD_VIEW_TABLE}

```ddn
각도시간선 <- (세로=#각도) 표준보기.시간선.
상태비교 <- (세로=[#각도, #각속도]) 표준보기.비교선.
진자실험 <- (장면=진자장면, 세로=#각도) 표준보기.장면그래프곁.
```

- 표준 보기와 사용자 보기는 같은 일반 구성 경로를 사용한다.
- 단일 보기에는 관계 작성을 요구하지 않는다.
- 복제는 독립 이름씨·source ref·lock·hash를 만들며 원본과 자동 연결하지 않는다.
- 작성된 보개가 없으면 “공개한 값을 기본 표로 보여 줍니다”라는 일반 표 fallback을 쓴다.

## 모양·장면 선반

- 최소 평면 모양: 점, 선, 선들, 다각형, 사각형, 원, 글, 화살표
- 최소 입체 모양: 점3d, 선3d, 상자, 구, 원기둥, 원뿔
- 확장 평면: 반직선, 선분, 곡선, 호, 타원, 세모, 둥근사각형, 정다각형,
  눈금판, 좌표축, 치수선, 괄호, 이름표, 그림, 길, 모둠
- 확장 입체: 선들3d, 평면, 캡슐, 원환, 격자평면, 좌표축3d,
  벡터화살표3d, 글판3d, 자취3d, 모둠3d
- 최소 완성 장면틀: 관찰살펴보기, 장면그래프작업대, 함수탐구,
  도형변환탐구, 진자실험, 운동벡터실험, 수요공급탐구, 분포비교탐구
- 표준 항목과 사용자 항목은 같은 DDN·장면 구성 경로를 사용한다.
- OI-KM-07 효과와 OI-KM-10 입력은 각각의 의미 관문 전까지 OPEN이다.
"""


def body_for_source(stem: str) -> str:
    if stem == "SSOT_DECISIONS":
        return f"""## RD-001~RD-042 최종 판정

{DECISION_ROWS}

## 표준 보기 결정 SV-D01~SV-D18

{SV_DECISIONS}
"""
    if stem == "SSOT_LANG":
        return COMMON_OBSERVATION + "\n" + LANGUAGE_SURFACES + "\n" + VIEW_CONTRACT
    if stem == "SSOT_PLATFORM":
        return f"""## 제품 3층

- 또니랑: 선언적 시뮬레이션과 절차적 개발을 함께 배우는 언어
- 셈그림: 또니랑 결정적 프로젝트 작업대
- 또니마루: 배움·공유·리믹스 공간

이 세 층은 교과 도구·게임 엔진·AI Gym 방향으로 이어진다.

{VIEW_CONTRACT}

## 설정 경계

- 안전·결정성 규칙은 사용자가 끌 수 있는 설정으로 만들지 않는다.
- 제품 관행은 판본 고정 기본값으로 제공한다.
- 의미를 바꾸는 선택만 이름 있는 DDN 고급 설정으로 연다.
- 법·기관 정책은 별도 배포 profile이 소유한다.
"""
    if stem == "SSOT_TERMS":
        return """## v24.17.1 공개 용어

| 용어 | 정본 의미 |
|---|---|
| 값꾸러미 | `이름: 값` 필드를 작성 순서대로 가진 열린 값 |
| 보임 | 살아있는 세계 값을 명시적으로 공개하는 경계 |
| 보개 프로그램 | 검증된 원천에서 보기값을 만드는 일반 셈씨 |
| 보기틀 | 재사용 가능한 이름씨 구성 틀 |
| 보기값 | 평가된 불변 보기 의미 값 |
| 보기개체 | 실행 중 수명과 지역 상태를 가진 instance |
| 보기관계 | 으뜸·겹·곁·돋 관계값 |
| 받는자리계약 | 출처·갈래/차원·읽는때를 선언하는 사용자 용어 |
| 내보임 | 보기틀이 공개하는 export 필드 |
| `(된씨)맺음` | 성공 갈래가 `된씨`인 결과 값 |

`묶음`·`pack`을 값꾸러미의 사용자 정본 별칭으로 만들지 않는다.
`PinSpec`, `space2d`, `space3d`, `scene_cursor`는 wire·구현 이름이다.
"""
    if stem == "SSOT_DEMOS":
        return f"""{COMMON_OBSERVATION}

## 표준 보기 예제

```ddn
(시간: 시간, 각도: 각도, 각속도: 각속도) 보임.

각도현재 <- (값=#각도) 표준보기.현재값.
각도시간선 <- (세로=#각도) 표준보기.시간선.
상태비교 <- (세로=[#각도, #각속도]) 표준보기.비교선.
진자실험보기 <- (장면=진자장면, 세로=#각도) 표준보기.장면그래프곁.
```

## 이름씨·계약 예제

```ddn
(중심:점2, 반지름:길이)인 원:이름씨 = {{
  먼저 {{ 반지름 > 0@m }} 아니면 물림.
}}.

공 <- (중심=원점, 반지름=2@m)인 원.
```
"""
    if stem == "SSOT_OPEN_ISSUES":
        return """## 문서 결정은 닫혔고 제품 증거가 남은 항목

| ID | 상태 | 닫힘 조건 |
|---|---|---|
| OI-OBS-01 | OPEN | 새 `보임` parser/canon/낭독/CLI/WASM/source-order golden |
| OI-OBS-02 | OPEN | 합성 영문 관찰 ID 제거와 schema/hash/golden 원자 교체 |
| OI-VIEW-01 | OPEN | 보기값·보기틀·보기개체·보기관계 제품 경로 |
| OI-SHELF-01 | OPEN | 표준 보기 12종의 Rust owner와 browser evidence |
| OI-SHAPE-01 | OPEN | 평면·입체 모양과 빈 장면의 공통 composition path |
| OI-KM-07 | OPEN | TRS 적용 순서·효과 충돌·camera 수학 |
| OI-KM-10 | OPEN | 상호작용·접근성·InputSnapshot 경계 |
| OI-NOUN-01 | OPEN | RD-041 parser/canon/진단/기존 수식 주입 비회귀 |
| OI-CONTRACT-01 | OPEN | RD-042 Gate0 수선 보존과 제품 parity |
| OI-RESULT-01 | OPEN | `(된씨)맺음` clean-cut parser/lock/hash migration |
| OI-SOLVE-01 | OPEN | 봉인된 bounded SolvePlan과 실패 진단 |

문서 승인만으로 구현 상태를 높이지 않는다.
"""
    if stem == "SSOT_PENDING":
        return """## owner 결정 완료

- 공개 관찰 정체성, exact gap, 관계 깊이, 역사 증거등급, 평가 확인 사건
  수집 기본값은 owner 결정 완료다.
- 이름씨 `인`, 짧은 계약문, 보개 용어, 표준 보기·모양·장면, 결과 표기,
  제한 풀이 방향은 owner 결정 완료다.
- 남은 parser/runtime/schema/법·기관 적용은 PENDING이 아니라 해당 소유자의
  OPEN 관문이다.

## 이전 2+13 기록의 재분류

| 입력 | 새 소유 위치 |
|---|---|
| 한국어 Manim SSOT 전면 반영 | EXECUTION-COMPLETE / 역사 증거 |
| SSOT 관리자·백업 감사 | EXECUTION-COMPLETE / 백업 운영 |
| settings handoff | 제품 설정 backlog |
| settings max/excellence roadmap | ROADMAP / 연구 |
| Seamgrim UI v2 screen plan | 승인 UI 기준선 / host UI backlog |
| reactive knowledge scene | OI-KM-07 / scene research |
| generic kusil approval packet | 언어·구실 독립 심사; 내용 일괄 승인 아님 |
| IP idea portfolio | IP 연구·증거 장부 |
| creator gaji circulation | 표준 가지 제품 roadmap |
| starter ecosystem research | 표준 생태계 roadmap |
| predev integrated planning | PLANS |
| artifact clean WASM | 제품 증거 audit |
| physics readiness | DEMOS / product readiness |
| thread SSOT reflection audit | SSOT 감사 증거 |
| IP red-team v2 | IP risk register |

재분류는 각 입력 문서의 세부 제안을 자동 승인하지 않는다.
"""
    if stem == "SSOT_PLANS":
        return """## v24.17.1 구현 순서

1. Slice 0: 새 공개 관찰 AST·값꾸러미 순서·schema owner
2. Slice 1: 현재값·시간선·결과표
3. Slice 2: 좌표선·비교선·막대·분포막대·흩어진점
4. Slice 3: 위치자취·벡터화살표
5. Slice 4: 장면그래프곁·장면값겹·복제
6. Slice 5: 평면·입체 모양과 완성 장면틀
7. Slice 6: legacy producer·consumer·UI·검사기·fixture·golden clean cut

각 Slice는 원문 parser/frontdoor, Rust owner, CLI/WASM parity, browser,
golden을 닫기 전 `behavior-closed`가 아니다. OI-KM-07과 OI-KM-10은
별도 연구를 병행하되 의미 결정 없이 제품 표면을 만들지 않는다.
"""
    if stem == "SSOT_TOOLCHAIN":
        return """## 제품 frontdoor 요구

- parser는 `(이름: 값, ...) 보임.`을 열린 값꾸러미 하나로 받는다.
- canonicalizer는 단순 이름 축약을 이름 있는 필드로 편다.
- normalizer·runtime·trace는 AST 작성 순서를 보존한다.
- Rust가 공개 관찰·보기 composition 정본화를 소유한다.
- CLI와 WASM은 같은 제품 경로를 호출한다.
- JS는 이름·축·관계·표준 보기 종류를 추측하지 않는다.
- `보임 {}`, `project.obs.N`, `output_N`, `seamgrim.graph.v0` 의미 경로는
  successor가 준비된 수직에서 원자적으로 제거한다.
- 테스트 전용 변환기로 새 표면 지원 완료를 주장하지 않는다.
"""
    if stem == "SSOT_PROGRAMMING_CONCEPT_LEDGER":
        return """## 교육·제품 발전 순서

또니랑은 선언적 시뮬레이션과 절차적 개발을 함께 익히게 하고, 셈그림의
교과 도구·게임 엔진·AI Gym 방향으로 발전한다.

## 현대 프로그래밍 개념 대응

| 일반 개념 | 또니랑 대응 |
|---|---|
| 캡슐화 | 이름씨 공개 머리와 본문 계약·초기화 경계 |
| 자기참조 | 값 정체성과 임자 정체성을 구분한 현재 대상 참조 |
| 메서드 | 이름씨에 붙는 셈씨·움직씨 또는 구실 요구 연산 |
| 메시지 전달 | 알림씨 발행·받으면 처리와 명시적 동작 전달 |
| 다형적 행동 | 구실 요구와 build 시점 정적 선택 |

이 대응은 교육 설명이며 dynamic dispatch·reflection 추가가 아니다.
"""
    if stem == "SSOT_ROADMAP_CATALOG":
        return """## JIT 개발 묶음

- 지금 닫을 1~3걸음: 공개 관찰 successor, 표준 보기 첫 수직, legacy clean cut
- 병행 연구: OI-KM-07 효과, OI-KM-10 입력
- 후속 콘텐츠: 확장 모양·완성 장면틀·교과 조립 부품
- 106개 창작 선반 아이디어는 roadmap catalog다. 개별 언어 의미와 runtime
  landed 상태를 자동 승인하지 않는다.
"""
    if stem == "SSOT_BOOK_SYSTEM_AND_COMPENDIUM_POLICY":
        return """## 공개·교재 예제 정책

- current 교재와 공개 스펙은 새 `보임`·이름씨·계약 표면만 사용한다.
- 표준 보기 예제는 사용자가 복제·검사할 수 있는 일반 DDN 구성을 보여 준다.
- 역사판 인용은 HISTORY·버전·제품 미착지를 함께 표시한다.
- 문서 예제를 테스트 전용 lowering으로 실행 가능한 것처럼 가장하지 않는다.
"""
    if stem == "GATE0_IMPLEMENTATION_CHECKLIST":
        return """## v24.17.1 추가 Gate

- [ ] `(이름: 값, ...) 보임.` parser/canon/낭독
- [ ] 이름 중복·빈 값꾸러미·이름 없는 식 진단
- [ ] AST 작성 순서가 CLI/WASM/trace/범례/표 열까지 유지
- [ ] `보임 {}`와 합성 영어 관찰 ID가 제품 입력·출력에서 제거
- [ ] RD-041과 기존 수식 주입 경로의 비회귀
- [ ] RD-042와 기존 Gate0 수선·1회 재검사의 비회귀
- [ ] 표준 보기와 사용자 복제본이 같은 composition node 생성
- [ ] gap/missing 단절과 missing 이유
- [ ] 관계 깊이 32·순환 거부
- [ ] OI-KM-07/10 미결 의미를 숨은 기본값으로 구현하지 않음
"""
    if stem == "SSOT_UPDATE_NOTES":
        return """## v24.17.1 — 2026-07-26

- RD-001~020 규범 효력을 조항별로 복구·대체했다.
- RD-023을 열린 값꾸러미 `보임`으로 교체하고 legacy 표면·합성 ID를 제거했다.
- RD-041 이름씨 `인`, RD-042 짧은 계약문을 추가했다.
- PENDING 6건과 이전 2+13 기록을 owner 결정·제품·법정책 소유로 재분류했다.
- 표준 보기 12종, 평면·입체 모양, 빈 장면, 완성 장면틀을 승인했다.
- 표준과 사용자 항목의 동일 구성 경로를 규범으로 고정했다.
- 공개 Language SPEC v0.3.0을 별도 계보로 투영했다.
- v24.17.0과 v0.2.1은 수정하지 않았다.
"""
    if stem == "SSOT_REVIEW_RESULT_20260430":
        return """## v24.17.1 관리자 재검토

- 구조 감사: RD-001~020 누락을 조항별로 보정
- 표면 감사: `:` 열린 값꾸러미와 `=` 고정 받는자리 결합을 분리
- 순서 감사: AST 작성 순서와 실행 map 순서 불일치 금지
- 정체성 감사: DDN 이름과 wire field를 분리
- 제품 비주장: parser/runtime/renderer는 OPEN 유지
- 승격 검증: manifest·aggregate·seal·금지 표면·복원 백업을 별도 검사
"""
    if stem == "SSOT_INDEX":
        return """## current 읽는 순서

1. `SSOT_ALL_MANIFEST_v24.17.1.md`
2. `SSOT_DECISIONS_v24.17.1.md`
3. `SSOT_LANG_v24.17.1.md`
4. `SSOT_PLATFORM_v24.17.1.md`
5. `SSOT_TERMS_v24.17.1.md`
6. `SSOT_OPEN_ISSUES_v24.17.1.md`
7. 관련 AGE/WALK

공개 언어 스펙은 `publish/spec/v0.3.0/`이며 내부 SSOT와 별도 계보다.
충돌하면 이 internal current가 우선한다.
"""
    if stem == "SSOT_MASTER":
        return (
            """## v24.17.1 통합 계약

이 판은 v24.15.1 규범 기반, v24.17.0 연구 통합 overlay, 2026-07-26 owner
최종 결정을 명시적 봉인 참조로 조립한다. 과거 HISTORY 블록을 통째로 current로
옮기지 않는다.

"""
            + COMMON_OBSERVATION
            + "\n"
            + LANGUAGE_SURFACES
            + "\n"
            + VIEW_CONTRACT
        )
    if stem == "README":
        return """## 이 판의 핵심

- RD-001~020 누락을 구조적으로 복구했다.
- `보임`은 열린 값꾸러미 한 개를 받으며 옛 블록 표면은 제거됐다.
- 이름씨 `인`, 짧은 계약, 표준 보기·모양·장면을 current docs-first로 올렸다.
- 공개 Language SPEC은 v0.3.0이다.
- 제품 개발은 다음 단계이며 이 문서 승격만으로 runtime landed가 아니다.
"""
    return """## v24.17.1 적용 요약

이 source는 명시적 계승 기반과 2026-07-26 owner 최종 결정을 조립한다.
세부 언어 표면은 `SSOT_LANG`, 제품 의미는 `SSOT_PLATFORM`, 구현 상태는
`SSOT_OPEN_ISSUES`와 관련 WALK를 따른다.
"""


def source_document(stem: str, title: str) -> str:
    return f"""# {title} — {stem} {INTERNAL_VERSION}

> 문서 버전: {INTERNAL_VERSION}
> 상태: live current / owner-approved {DATE} / docs-first product boundaries preserved
> 반영 권위: `{DECISION.name}`
> 구현 상태: 문서 반영 완료; parser/runtime/renderer 제품 착지는 항목별 OPEN
> 이전 current: {PREVIOUS_INTERNAL_VERSION} (제자리 보존)
> 문서 종류: source

<!-- V24_17_1_ACTIVE_BEGIN -->

{inherited_preamble(stem)}

{body_for_source(stem)}

<!-- V24_17_1_ACTIVE_END -->

## 역사 계보

- 이전 파일 `{stem}_{PREVIOUS_INTERNAL_VERSION}.md`는 제자리에서 수정하지 않았다.
- 더 오래된 HISTORY 본문은 해당 파일의 자체 경계와 release 봉인을 따른다.
"""


REGISTRY_ROWS: dict[str, str] = {
    "STDLIB_SURFACE_REGISTRY": f"""{STANDARD_VIEW_TABLE}

| family | 공개 항목 | 상태 |
|---|---|---|
| 평면 모양 최소 | 점·선·선들·다각형·사각형·원·글·화살표 | docs_first / runtime OPEN |
| 입체 모양 최소 | 점3d·선3d·상자·구·원기둥·원뿔 | docs_first / runtime OPEN |
| 완성 장면틀 | 관찰살펴보기·장면그래프작업대·함수탐구·도형변환탐구·진자실험·운동벡터실험·수요공급탐구·분포비교탐구 | docs_first / runtime OPEN |
""",
    "CLI_COMMAND_REGISTRY": """| command | 상태 | v24.17.1 요구 |
|---|---|---|
| parse/canon | 기존 명령 / successor OPEN | 새 `보임`, RD-041, RD-042 원문을 직접 처리 |
| run | 기존 명령 / successor OPEN | Rust 공통 owner 사용 |
| wasm frontdoor | 기존 API / successor OPEN | CLI와 canonical·trace parity |
""",
    "SCHEMA_EXISTENCE_REGISTRY": """| schema | 상태 |
|---|---|
| PublicObservationV1 successor | docs_first / OPEN |
| SceneCompositionV1 | docs_first / OPEN |
| ResolvedSceneTraceV1 | docs_first / OPEN |
| ResolvedSceneFrameV1 | docs_first / OPEN |
| StandardViewExpansionV1 | docs_first / OPEN |
""",
    "SCHEMA_CONTRACT_REGISTRY": """| schema | 필수 계약 |
|---|---|
| PublicObservationV1 successor | DDN 이름·source ref·갈래·단위·작성 순서·희소 상태 |
| StandardViewExpansionV1 | 표준 판본·export·고정 기본값·일반 composition·source chain |
| ViewRelationV1 | 한국어 DDN 관계·깊이 32·순환 금지 |
""",
    "DIAGNOSTIC_EXISTENCE_REGISTRY": """| code | 상태 |
|---|---|
| E_BOIM_LEGACY_REMOVED | required / product OPEN |
| E_BOIM_EMPTY_PACK | required / product OPEN |
| E_BOIM_DUPLICATE_NAME | required / product OPEN |
| E_BOIM_UNNAMED_EXPR | required / product OPEN |
| E_VIEW_RELATION_DEPTH | required / product OPEN |
| E_VIEW_RELATION_CYCLE | required / product OPEN |
| E_SAMPLE_MISSING_REASON | required / product OPEN |
""",
    "DIAGNOSTIC_CONTRACT_REGISTRY": """| code | 사용자 진단 계약 |
|---|---|
| E_BOIM_LEGACY_REMOVED | 옛 블록 표면은 제거됐고 `(이름: 값, ...) 보임.`을 사용함을 알린다 |
| E_BOIM_DUPLICATE_NAME | 중복 이름과 두 source span을 가리킨다 |
| E_BOIM_UNNAMED_EXPR | 식에 붙일 공개 이름을 요구한다 |
| E_VIEW_RELATION_DEPTH | 깊이 32 한도와 최초 초과 path를 가리킨다 |
| E_SAMPLE_MISSING_REASON | 허용된 missing 이유를 제시한다 |
""",
    "DECISION_INPUT_DISPOSITION_REGISTRY": """| input family | 처분 |
|---|---|
| RD-001~040 계승 보정 | owner-approved / reflected v24.17.1 |
| RD-041·042 | owner-approved / docs-first current / runtime OPEN |
| Pending6 의미 소유 | owner-approved / 제품·법정책 관문 분리 |
| standard views SV-D01~18 | owner-approved / docs-first current / runtime OPEN |
| 이전 Pending 2건 | EXECUTION-COMPLETE |
| 이전 Pending 13건 | owner-wait 제거 / 소유 위치 재분류 / 내용 일괄 승인 아님 |
""",
    "OI_FAMILY_REGISTRY": """| OI | 상태 | owner |
|---|---|---|
| OI-OBS-01/02 | OPEN | lang/tool |
| OI-VIEW-01 | OPEN | tool |
| OI-SHELF-01 | OPEN | tool/workbench |
| OI-SHAPE-01 | OPEN | tool/renderer |
| OI-KM-07 | OPEN | scene/animation |
| OI-KM-10 | OPEN | interaction/accessibility |
| OI-NOUN-01 | OPEN | lang |
| OI-CONTRACT-01 | OPEN | lang/core |
| OI-SOLVE-01 | OPEN | core/stdlib |
""",
    "TYPE_SURFACE_REGISTRY": """| 공개 갈래·용어 | 상태 |
|---|---|
| 값꾸러미 | canonical docs-first; source order required |
| 공개관찰참조<된씨> | docs-first / product OPEN |
| 보기틀 | canonical docs-first / product OPEN |
| 보기값 | canonical docs-first / product OPEN |
| 보기개체 | canonical docs-first / product OPEN |
| 보기관계 | canonical docs-first / product OPEN |
| `(된씨)맺음` | canonical; clean-cut product migration OPEN |
""",
    "KUSIL_CONTRACT_REGISTRY": """| surface | 상태 | 계약 |
|---|---|---|
| `맡음` | 유지 | 구체 대상이 구실을 채택했다는 사실 |
| `맡아야함` | 유지 | 씨자리·generic이 구실을 요구함 |
| `먼저/내내/마치면` | docs-first current | 계약 평가 시점 |
| `물림/알림` | docs-first current | 위반 처리 |
| Gate0 수선·1회 재검사 | 유지 | 짧은 계약에 숨겨 제거하지 않음 |
""",
    "BUILD_PROFILE_REGISTRY": """| profile 규칙 | 상태 |
|---|---|
| relation depth=32 | D-STRICT fixed / user override 없음 |
| cyclic view relation | forbidden |
| unbounded backtracking | forbidden |
| bounded SolvePlan | docs-first / product OPEN |
| external solver | sealed named non-strict profile only |
""",
    "DIAGNOSTIC_CODE_REGISTRY": """| code | severity | phase |
|---|---|---|
| E_BOIM_LEGACY_REMOVED | error | parse |
| E_BOIM_EMPTY_PACK | error | parse/type |
| E_BOIM_DUPLICATE_NAME | error | parse/type |
| E_BOIM_UNNAMED_EXPR | error | canon |
| E_VIEW_RELATION_DEPTH | error | build |
| E_VIEW_RELATION_CYCLE | error | build |
| E_SAMPLE_MISSING_REASON | error | trace validation |
| E_SOLVE_PLAN_UNBOUNDED | error | build |
""",
}


def registry_document(stem: str, title: str) -> str:
    previous = registry_path(stem, PREVIOUS_INTERNAL_VERSION)
    if not previous.exists():
        raise FileNotFoundError(previous)
    return f"""# {title} registry — {stem} {INTERNAL_VERSION}

> 상태: live current registry / owner-approved {DATE}
> 이전 registry: `{previous.name}` (`sha256:{sha256_file(previous)}`)
> 계승: 이전 registry의 당시 active/carry-forward 행은 아래 override와 충돌하지 않는
> 범위에서 유지한다. 과거 HISTORY·폐기 행을 current로 승격하지 않는다.
> 제품 상태: 각 행의 상태를 따르며 문서 등록은 runtime landed가 아니다.

<!-- V24_17_1_ACTIVE_BEGIN -->

{REGISTRY_ROWS[stem]}

<!-- V24_17_1_ACTIVE_END -->
"""


def patch_walk_files() -> list[Path]:
    roots = [
        SSOT_ROOT / "walks" / "gogae10" / "w100_public_observation_scene_composition",
        SSOT_ROOT / "walks" / "gogae10" / "w101_scene_time_frame_renderer",
        SSOT_ROOT / "walks" / "gogae10" / "w102_pendulum_2d_workbench",
    ]
    included: list[Path] = []
    for root in roots:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".ddn"}:
                continue
            included.append(path)
            text = path.read_text(encoding="utf-8")
            updated = text
            updated = updated.replace(
                "owner-approved 2026-07-24", "owner-approved 2026-07-26"
            )
            updated = updated.replace(
                "`(값들) 보임.`: canonical direction approved / implementation OPEN",
                "`(이름: 값, ...) 보임.`: canonical docs-first current / implementation OPEN",
            )
            updated = updated.replace(
                "`보임 {}`: deprecated legacy input only / canonical output 금지 / migration 뒤 parser 제거",
                "`보임 {}`: REMOVED-PRE-USER / parser 입력·호환 alias 금지",
            )
            updated = updated.replace(
                "legacy `보임 {}` 입력은 migration 기간에만 읽히고 canonical output은 반드시 `(값들) 보임.`을 낸다.",
                "제거된 `보임 {}` 입력은 `E_BOIM_LEGACY_REMOVED`로 거부하고 canonical alias를 만들지 않는다.",
            )
            updated = updated.replace(
                "`보임 {}` legacy 입력 migration과 `(값들) 보임.` canonical output을 함께 시험한다.",
                "새 값꾸러미 표면의 canonical output과 제거된 `보임 {}`의 명시적 거부를 함께 시험한다.",
            )
            updated = updated.replace(
                "(진자_공개상태) 보임.",
                "(진자_공개상태: 진자_공개상태) 보임.",
            )
            if updated != text:
                write_text(path, updated)
    return included


def build_age_guide() -> Path:
    old = (
        SSOT_ROOT
        / "age"
        / "AGE3"
        / "AGE3_DEVELOPMENT_GUIDE_v24.17.0-research-integration-candidate.md"
    )
    new = SSOT_ROOT / "age" / "AGE3" / "AGE3_DEVELOPMENT_GUIDE_v24.17.1.md"
    text = old.read_text(encoding="utf-8")
    text = text.replace(
        "v24.17.0-research-integration-candidate", INTERNAL_VERSION
    )
    text = text.replace("candidate", "current")
    text = text.replace(
        "`(값들) 보임.`은 canonical direction이고 `보임 {}`는 deprecated legacy input이다.",
        "`(이름: 값, ...) 보임.`은 docs-first current이고 `보임 {}`는 REMOVED-PRE-USER다.",
    )
    text += f"""

## {INTERNAL_VERSION} 표준 보기·모양·장면

{STANDARD_VIEW_TABLE}

- 최소 평면 모양 8종과 입체 모양 6종을 같은 일반 composition 경로로 제공한다.
- 빈 평면·입체 장면과 최소 8개 완성 장면틀을 inspectable·cloneable하게 제공한다.
- 표준 항목에만 허용된 renderer 권한을 만들지 않는다.
- OI-KM-07 효과와 OI-KM-10 입력은 별도 제품 관문이다.
"""
    write_text(new, text)
    return new


def build_companion_manifest(paths: list[Path]) -> Path:
    manifest = SSOT_ROOT / "V24_17_1_OWNER_DECISIONS_COMPANION_MANIFEST.md"
    rows = "\n".join(
        f"| `{path.relative_to(SSOT_ROOT).as_posix()}` | `{sha256_file(path)}` |"
        for path in sorted(paths, key=lambda item: item.relative_to(SSOT_ROOT).as_posix())
    )
    text = f"""# v24.17.1 AGE/WALK 동반 봉인

- status: current companion manifest
- owner approval: {DATE}
- internal SSOT: {INTERNAL_VERSION}
- file count: {len(paths)}

| file | sha256 |
|---|---|
{rows}

이 봉인은 AGE3와 WALK100~102의 문서·fixture가 새 공개 관찰 표면과
표준 보기 결정을 따름을 증명한다. parser/runtime landed를 뜻하지 않는다.
"""
    write_text(manifest, text)
    return manifest


def build_aggregate(non_manifest_sources: list[Path], registries: list[Path]) -> Path:
    aggregate = source_path("SSOT_ALL", INTERNAL_VERSION)
    chunks = [
        f"# SSOT_ALL {INTERNAL_VERSION}\n",
        "> generated aggregate / non-authoritative\n",
        "> authority: SSOT_ALL_MANIFEST_v24.17.1.md\n",
    ]
    for path in sorted(
        non_manifest_sources + registries,
        key=lambda item: item.relative_to(SSOT).as_posix(),
    ):
        rel = path.relative_to(SSOT).as_posix()
        chunks.append(f"\n\n<!-- BEGIN {rel} -->\n\n")
        chunks.append(path.read_text(encoding="utf-8"))
        chunks.append(f"\n<!-- END {rel} -->\n")
    write_text(aggregate, "".join(chunks))
    return aggregate


def build_manifest(
    non_manifest_sources: list[Path],
    registries: list[Path],
    aggregate: Path,
    companion: Path,
) -> Path:
    manifest = source_path("SSOT_ALL_MANIFEST", INTERNAL_VERSION)
    source_rows = []
    source_order = [
        "GATE0_IMPLEMENTATION_CHECKLIST",
        "README",
        "SSOT_ALL_MANIFEST",
        "SSOT_DECISIONS",
        "SSOT_DEMOS",
        "SSOT_INDEX",
        "SSOT_LANG",
        "SSOT_MASTER",
        "SSOT_OPEN_ISSUES",
        "SSOT_PENDING",
        "SSOT_PLANS",
        "SSOT_PLATFORM",
        "SSOT_REVIEW_RESULT_20260430",
        "SSOT_ROADMAP_CATALOG",
        "SSOT_TERMS",
        "SSOT_TOOLCHAIN",
        "SSOT_UPDATE_NOTES",
        "SSOT_BOOK_SYSTEM_AND_COMPENDIUM_POLICY",
        "SSOT_PROGRAMMING_CONCEPT_LEDGER",
    ]
    source_by_stem = {path.name.rsplit(f"_{INTERNAL_VERSION}.md", 1)[0]: path for path in non_manifest_sources}
    for idx, stem in enumerate(source_order, 1):
        if stem == "SSOT_ALL_MANIFEST":
            source_rows.append(
                f"| {idx} | `{manifest.name}` | core | sealed by CURRENT_SHA256 |"
            )
            continue
        path = source_by_stem[stem]
        kind = (
            "normative reference appendix"
            if stem
            in {
                "SSOT_BOOK_SYSTEM_AND_COMPENDIUM_POLICY",
                "SSOT_PROGRAMMING_CONCEPT_LEDGER",
            }
            else "core"
        )
        source_rows.append(
            f"| {idx} | `{path.name}` | {kind} | `{sha256_file(path)}` |"
        )
    registry_rows = [
        f"| `{path.relative_to(SSOT).as_posix()}` | current docs-first / runtime per row | `{sha256_file(path)}` |"
        for path in registries
    ]
    family_paths = non_manifest_sources + registries
    base_manifest = BASE / "SSOT_ALL_MANIFEST_v24.15.1.md"
    previous_manifest = source_path("SSOT_ALL_MANIFEST", PREVIOUS_INTERNAL_VERSION)
    text = f"""# SSOT_ALL_MANIFEST {INTERNAL_VERSION}

- authority: live current canonical assembly authority
- current_name: `{INTERNAL_VERSION}`
- current_since: `{DATE}`
- source_document_count: 19 (17 core + 2 normative reference appendix)
- generated_registry_count: 12
- aggregate: `{aggregate.name}`
- aggregate_authority: generated/non-authoritative
- encoding: UTF-8 without BOM, LF
- generator: `{GENERATOR_REL}`
- generator_sha256: `{sha256_file(ROOT / GENERATOR_REL)}`
- owner_decision: `decisions/{DECISION.name}`
- owner_decision_sha256: `{sha256_file(DECISION)}`
- normative_base_manifest: `releases/v24.15.1-recovery-lineage/snapshot/{base_manifest.name}`
- normative_base_manifest_sha256: `{sha256_file(base_manifest)}`
- previous_current_manifest: `{previous_manifest.name}`
- previous_current_manifest_sha256: `{sha256_file(previous_manifest)}`
- previous_files_mutated: false
- companion_manifest: `../{companion.name}`
- companion_manifest_sha256: `{sha256_file(companion)}`
- family_tree_sha256: `{tree_digest(family_paths, SSOT)}`
- public_language_spec: `{PUBLIC_VERSION}`
- product_nonclaim: docs current only; parser/runtime/renderer completion not claimed

## 규범 조립 경계

1. 각 source의 `V24_17_1_ACTIVE_BEGIN/END`만 이 판의 직접 규범이다.
2. 각 source가 해시로 지시한 v24.15.1 기반과 v24.17.0 active overlay를
   명시적으로 계승한다.
3. 과거 HISTORY 블록은 자동 계승하지 않는다.
4. 이 판의 override와 owner 결정문이 충돌 시 우선한다.
5. `보임 {{}}`와 합성 영어 관찰 ID는 `REMOVED-PRE-USER`다.
6. `(이름: 값, ...) 보임.`과 RD-041·042는 docs-first current이고 제품은 OPEN이다.

## source documents

| # | file | kind | sha256 |
|---|---|---|---|
{chr(10).join(source_rows)}

## generated registries

| file | status | sha256 |
|---|---|---|
{chr(10).join(registry_rows)}

## generated aggregate

- sha256: `{sha256_file(aggregate)}`
- included files: 30 (manifest self-excluded)
"""
    write_text(manifest, text)
    return manifest


def build_seal(
    manifest: Path,
    non_manifest_sources: list[Path],
    registries: list[Path],
    aggregate: Path,
    companion: Path,
) -> Path:
    seal = source_path("CURRENT_SHA256", INTERNAL_VERSION)
    paths = [manifest, aggregate, companion, DECISION] + non_manifest_sources + registries
    rows = "\n".join(
        f"| `{path.relative_to(ROOT).as_posix()}` | `{sha256_file(path)}` |"
        for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix())
    )
    text = f"""# CURRENT SHA-256 seal {INTERNAL_VERSION}

- status: live current seal
- sealed_at: {DATE}
- file_count: {len(paths)}

| file | sha256 |
|---|---|
{rows}
"""
    write_text(seal, text)
    return seal


def public_header(title: str) -> str:
    return f"""# {title} — Language SPEC {PUBLIC_VERSION}

> 상태: current public pre-release draft / owner-approved {DATE}
> trace: Language SPEC `{PUBLIC_VERSION}` ← internal current SSOT `{INTERNAL_VERSION}`
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: docs-first canonical과 parser/runtime 제품 상태를 구분한다.
"""


def build_public_spec(source_tree_hash: str, source_manifest_hash: str, source_seal_hash: str) -> list[Path]:
    out = PUBLIC / PUBLIC_VERSION
    out.mkdir(parents=True, exist_ok=True)
    intro = out / f"SPEC_LANGUAGE_INTRODUCTION_{PUBLIC_VERSION}.md"
    syntax = out / f"SPEC_LANGUAGE_SYNTAX_SUMMARY_{PUBLIC_VERSION}.md"
    support = out / f"SPEC_STABLE_SUPPORT_SURFACE_{PUBLIC_VERSION}.md"
    compat = out / f"SPEC_COMPATIBILITY_AND_NONCLAIMS_{PUBLIC_VERSION}.md"
    determinism = out / f"SPEC_DETERMINISM_CONTRACT_{PUBLIC_VERSION}.md"
    examples = out / f"SPEC_EXAMPLES_{PUBLIC_VERSION}.md"

    write_text(
        intro,
        public_header("또니랑 언어 소개")
        + """
## 또니랑·셈그림·또니마루

- 또니랑은 선언적 시뮬레이션과 절차적 개발을 함께 쓰는 언어다.
- 셈그림은 또니랑 결정적 프로젝트 작업대다.
- 또니마루는 배움·공유·리믹스 공간이다.

## v0.3.0의 초점

- DDN 이름을 표시층이 아니라 의미층의 정체성으로 사용한다.
- 살아있는 세계 값은 `(이름: 값, ...) 보임.`으로 명시적으로 공개한다.
- 이름씨 정의와 사용을 `(자리...)인 이름`으로 대칭화한다.
- 계약을 `먼저/내내/마치면`과 `물림/알림`으로 짧게 쓴다.
- 표준 보기·모양·장면은 사용자 항목과 같은 구성 경로를 쓴다.

“정본”은 언어 계약이 결정됐다는 뜻이다. 실제 제품 지원은 지원 범위표에서
확인하며, 문서 예제만으로 runtime landed를 주장하지 않는다.
""",
    )
    write_text(
        syntax,
        public_header("또니랑 문법 요약")
        + f"""
## 적용 갈래와 씨자리

```ddn
(셈수)차림
(글, 셈수)짝맞춤
(된씨)맺음
((셈수)차림)차림
```

`맺음<T>`는 비교 설명용 표기일 뿐 또니랑 입력이 아니다.

```ddn
(왼씨:씨자리, 오른씨:씨자리)인 짝:이름씨 = {{
  왼:왼씨.
  오른:오른씨.
}}.
```

## 이름씨 정의와 구성

```ddn
(중심:점2, 반지름:길이, 색:색=#파랑)인
원:이름씨 = {{
  먼저 {{ 반지름 > 0@m }} 아니면 물림.
}}.

파란원 <- (중심=시작점, 반지름=2@m)인 원.
```

`인`은 바로 뒤 이름씨만 꾸민다. 동작 자체를 `인`으로 꾸미지 않는다.
고정된 이름씨 받는자리 결합에는 `이름=값`을 쓴다.

## 공개 관찰

```ddn
(시간: 시간, 각도: 각도, 각속도: 각속도) 보임.
```

`보임`의 괄호 안은 열린 값꾸러미 하나다. 열린 필드는 `이름: 값`이고
작성 순서가 정본이다. `(각도) 보임.`은 `(각도: 각도) 보임.`으로
정본화할 수 있다. 이름 없는 식은 공개 이름을 붙여야 한다.

## 짧은 계약

```ddn
먼저 {{ 반지름 > 0@m }} 아니면 물림.
내내 {{ 반지름 <= 1000@m }} 아니면 물림.
마치면 {{ 색대비 >= 4.5 }} 아니면 알림.
```

계약은 상태를 자동 수선하지 않는다. 기존 명시 수선 절차는 별도다.

## 구실

`맡음`은 사실 진술, `맡아야함`은 요구 진술로 구분한다.

```ddn
공~은 표준원그리기~로 그려질수있음~이라는 구실~을 맡음.

(
  그릴씨:씨자리,
  그릴씨~는 그려질수있음~이라는 구실~을 맡아야함,
  맡은이:그릴씨~을~를
) 그리기:그림명령:셈씨 = {{
  ...
}}.
```

## 표준 보기

```ddn
각도시간선 <- (세로=#각도) 표준보기.시간선.
상태비교 <- (세로=[#각도, #각속도]) 표준보기.비교선.
진자실험 <- (장면=진자장면, 세로=#각도) 표준보기.장면그래프곁.
```

표준 export는 고정 받는자리이므로 `=`를 쓴다. 공개 관찰 이름은 받는자리
갈래가 `공개관찰참조<된씨>`일 때만 해소된다.

## 함수 갈래

```ddn
가씨 --> 나씨
(가씨, 나씨) --> 다씨
```

`-->`는 함수 갈래이고 `->`의 입력 별칭이 아니다.
""",
    )
    write_text(
        support,
        public_header("지원 범위")
        + """
| 표면 | 설계 상태 | 제품 상태 |
|---|---|---|
| 한글 씨자리와 적용 갈래 | canonical docs-first | 기존 범위별 확인 |
| `(된씨)맺음` | canonical | clean-cut parser/lock/hash migration OPEN |
| `(이름: 값, ...) 보임.` | canonical docs-first | parser/runtime/CLI/WASM OPEN |
| 이름씨 `(자리...)인 이름` | canonical docs-first | parser/canon/golden OPEN |
| 짧은 계약문 | canonical docs-first | Gate0 parity OPEN |
| 구실·정적 dispatch | canonical docs-first | K0~K7 OPEN |
| 표준 보기 12종 | canonical docs-first | Rust/browser/golden OPEN |
| 평면·입체 모양 선반 | canonical docs-first | common composition OPEN |
| 완성 장면틀 8종 | canonical docs-first | content/runtime OPEN |
| bounded SolvePlan | canonical direction | implementation OPEN |
| OI-KM-07 효과 | meaning gate OPEN | unavailable |
| OI-KM-10 입력 | meaning gate OPEN | unavailable |

## 표준 보기 12종

현재값, 시간선, 비교선, 좌표선, 흩어진점, 막대, 결과표, 위치자취,
벡터화살표, 장면그래프곁, 장면값겹, 분포막대를 공개 이름으로 사용한다.

제품 지원은 테스트 전용 변환기가 아니라 원문을 받는 parser/frontdoor, Rust owner,
CLI/WASM parity, browser와 golden 증거로 판단한다.
""",
    )
    write_text(
        compat,
        public_header("호환성·비주장 정책")
        + """
## v0.x clean break

- 외부 사용자와 보존할 사용자 자료가 0인 현재 잘못된 표면을 호환 자산으로 만들지 않는다.
- `보임 {}`는 제거됐다. deprecated alias나 dual canonical output을 제공하지 않는다.
- `project.obs.N`, `output_N` 같은 합성 정체성을 공개 의미로 사용하지 않는다.
- `묶음`·`pack`을 값꾸러미의 사용자 정본 별칭으로 제공하지 않는다.
- v0.2.1과 이전 공개판은 역사판으로 제자리 보존한다.

## 비주장

이 공개판은 parser/runtime/renderer, 한국어 Manim, 표준 선반 runtime,
외부 사용자 성공을 완료로 주장하지 않는다. `space2d`, `space3d`, `PinSpec`,
영문 schema field는 wire·구현 이름이며 한국어 의미 정체성을 대신하지 않는다.
""",
    )
    write_text(
        determinism,
        public_header("결정론 계약")
        + """
## 이름·순서·source chain

- 공개 의미 이름은 DDN에서 온다.
- 값꾸러미 필드, 계열, 범례, 표 열은 작성·선택 순서를 보존한다.
- 실행 map의 열쇠 정렬을 정본 순서로 쓰지 않는다.
- 모든 보기 의미는 DDN 또는 잠긴 표준 가지에서 committed trace까지 source chain을 가진다.

## 희소 표본

- `present`, `gap`, `missing`, `pruned`를 구분한다.
- `missing`은 `#계산실패`, `#원천없음`, `#기록손상` 이유를 가진다.
- 발행 기회 없음은 표본이 아니다.
- gap·missing을 가로질러 선이나 자취를 보간하지 않는다.

## 관계와 풀이

- 보기 관계 깊이는 32이고 순환은 금지한다.
- 이 안전 한도는 사용자가 끌 수 없다.
- 무제한 backtracking을 금지한다.
- SolvePlan은 후보 공간·순서·상한·실패 이유를 봉인한다.

## 표준과 사용자 경로

표준 보기·모양·장면과 사용자 복제본은 같은 일반 composition 경로를 사용한다.
표준 전용 숨은 renderer 권한을 금지한다.
""",
    )
    write_text(
        examples,
        public_header("정본 예제")
        + """
## 공개 관찰과 시간선

```ddn
(시간: 시간, 각도: 각도, 각속도: 각속도) 보임.
각도시간선 <- (세로=#각도) 표준보기.시간선.
```

## 이름씨와 계약

```ddn
(중심:점2, 반지름:길이)인 원:이름씨 = {
  먼저 { 반지름 > 0@m } 아니면 물림.
}.

공 <- (중심=원점, 반지름=2@m)인 원.
```

## 장면과 그래프

```ddn
(시간: 시간, 각도: 각도) 보임.
진자보기 <- (장면=진자장면, 세로=#각도) 표준보기.장면그래프곁.
```

이 예제는 docs-first 정본 표면이다. 현재 제품 실행 가능 여부는 지원 범위표를 따른다.
""",
    )

    example_dir = out / "examples"
    example_dir.mkdir(parents=True, exist_ok=True)
    example_files = {
        "01_public_observation.ddn": """(시간: 시간, 각도: 각도, 각속도: 각속도) 보임.\n""",
        "02_noun_definition.ddn": """(중심:점2, 반지름:길이)인 원:이름씨 = {\n  먼저 { 반지름 > 0@m } 아니면 물림.\n}.\n공 <- (중심=원점, 반지름=2@m)인 원.\n""",
        "03_short_contract.ddn": """먼저 { 값 > 0 } 아니면 물림.\n내내 { 값 <= 1000 } 아니면 물림.\n마치면 { 확인됨 } 아니면 알림.\n""",
        "04_standard_views.ddn": """각도시간선 <- (세로=#각도) 표준보기.시간선.\n상태비교 <- (세로=[#각도, #각속도]) 표준보기.비교선.\n""",
        "05_scene_graph.ddn": """진자보기 <- (장면=진자장면, 세로=#각도) 표준보기.장면그래프곁.\n""",
    }
    for name, text in example_files.items():
        write_text(example_dir / name, text)

    trace = out / f"SPEC_TRACE_{PUBLIC_VERSION}.detjson"
    trace_data = {
        "owner_decision_sha256": f"sha256:{sha256_file(DECISION)}",
        "predecessor_public_version": PREVIOUS_PUBLIC_VERSION,
        "product_evidence": "parser/runtime/renderer successor OPEN",
        "public_version": PUBLIC_VERSION,
        "source_ssot_manifest_sha256": f"sha256:{source_manifest_hash}",
        "source_ssot_seal_sha256": f"sha256:{source_seal_hash}",
        "source_ssot_status": "live-current-docs-first",
        "source_ssot_tree_sha256": f"sha256:{source_tree_hash}",
        "source_ssot_version": INTERNAL_VERSION,
        "status": "current-public-pre-release-draft",
    }
    write_text(
        trace,
        json.dumps(trace_data, ensure_ascii=False, indent=2, sort_keys=True),
    )

    content_files = [intro, syntax, support, compat, determinism, examples, trace]
    content_files.extend(sorted(example_dir.glob("*.ddn")))
    manifest = out / f"SPEC_MANIFEST_{PUBLIC_VERSION}.md"
    rows = "\n".join(
        f"| `{path.relative_to(out).as_posix()}` | `{sha256_file(path)}` |"
        for path in sorted(content_files, key=lambda item: item.relative_to(out).as_posix())
    )
    public_tree = tree_digest(content_files, out)
    manifest_text = f"""# 또니랑 Language SPEC manifest {PUBLIC_VERSION}

> status: current public pre-release draft / owner-approved {DATE}
> authority: public projection; installed internal current SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `{PUBLIC_VERSION}` |
| source SSOT current | `{INTERNAL_VERSION}` |
| source SSOT tree sha256 | `{source_tree_hash}` |
| source SSOT manifest sha256 | `{source_manifest_hash}` |
| source SSOT seal sha256 | `{source_seal_hash}` |
| owner decision sha256 | `{sha256_file(DECISION)}` |
| predecessor public version | `{PREVIOUS_PUBLIC_VERSION}` |
| public content tree sha256 | `{public_tree}` |

## public files

| file | sha256 |
|---|---|
{rows}

## projection boundary

- v0.2.1과 이전 공개판을 제자리 수정하지 않았다.
- 새 표면은 docs-first canonical이며 제품 상태는 지원 범위표를 따른다.
- `보임 {{}}` 호환 alias와 합성 영문 의미 ID를 제공하지 않는다.
"""
    write_text(manifest, manifest_text)

    seal = out / f"SPEC_SHA256_{PUBLIC_VERSION}.md"
    seal_paths = [manifest] + content_files
    seal_rows = "\n".join(
        f"| `{path.relative_to(out).as_posix()}` | `{sha256_file(path)}` |"
        for path in sorted(seal_paths, key=lambda item: item.relative_to(out).as_posix())
    )
    write_text(
        seal,
        f"""# Language SPEC SHA-256 seal {PUBLIC_VERSION}

- status: current public seal
- file_count: {len(seal_paths)}

| file | sha256 |
|---|---|
{seal_rows}
""",
    )
    write_text(
        PUBLIC / "CURRENT.md",
        f"""# 또니랑 공개 언어 스펙

현재 공개 초안: [`{PUBLIC_VERSION}`](./{PUBLIC_VERSION}/SPEC_MANIFEST_{PUBLIC_VERSION}.md)

- `{PUBLIC_VERSION}`은 internal current SSOT `{INTERNAL_VERSION}`의 사용자-facing
  docs-first 계약을 투영한다.
- `{PREVIOUS_PUBLIC_VERSION}`과 이전 공개 초안은 제자리 보존한다.
- 설계 확정과 제품 구현 완료는 분리한다.
- 내부 SSOT와 공개 Language SPEC은 별도 버전 계보다. 충돌하면 internal current가 우선한다.
""",
    )
    return [manifest, seal] + content_files + sorted(example_dir.glob("*.ddn"))


def apply() -> None:
    if not DECISION.exists():
        raise SystemExit(f"missing owner decision: {DECISION}")
    non_manifest_sources: list[Path] = []
    for stem, title in SOURCE_SPECS:
        path = source_path(stem, INTERNAL_VERSION)
        write_text(path, source_document(stem, title))
        non_manifest_sources.append(path)

    registries: list[Path] = []
    for stem, title in REGISTRY_SPECS:
        path = registry_path(stem, INTERNAL_VERSION)
        write_text(path, registry_document(stem, title))
        registries.append(path)

    walk_paths = patch_walk_files()
    age_path = build_age_guide()
    companion_paths = sorted(set(walk_paths + [age_path]))
    companion = build_companion_manifest(companion_paths)

    aggregate = build_aggregate(non_manifest_sources, registries)
    manifest = build_manifest(non_manifest_sources, registries, aggregate, companion)
    seal = build_seal(
        manifest, non_manifest_sources, registries, aggregate, companion
    )
    family_tree = tree_digest(non_manifest_sources + registries, SSOT)

    write_text(
        SSOT / "CURRENT.md",
        f"""# 또니랑 내부 SSOT current

현재 정본: [`{INTERNAL_VERSION}`](./SSOT_ALL_MANIFEST_{INTERNAL_VERSION}.md)

- owner 최종 승인: {DATE}
- 이전 current `{PREVIOUS_INTERNAL_VERSION}`은 제자리 보존한다.
- 공개 Language SPEC: [`{PUBLIC_VERSION}`](../../../publish/spec/{PUBLIC_VERSION}/SPEC_MANIFEST_{PUBLIC_VERSION}.md)
- 문서 정본화는 parser/runtime/renderer 완료를 뜻하지 않는다.
""",
    )
    build_public_spec(family_tree, sha256_file(manifest), sha256_file(seal))
    check()


def active_block(text: str) -> str:
    match = re.search(
        r"<!-- V24_17_1_ACTIVE_BEGIN -->(.*?)<!-- V24_17_1_ACTIVE_END -->",
        text,
        flags=re.S,
    )
    if not match:
        raise AssertionError("missing v24.17.1 active block")
    return match.group(1)


def parse_hash_rows(text: str) -> list[tuple[str, str]]:
    rows = []
    for line in text.splitlines():
        match = re.match(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", line)
        if match:
            rows.append((match.group(1), match.group(2)))
    return rows


def check() -> None:
    errors: list[str] = []
    source_files = [
        source_path(stem, INTERNAL_VERSION) for stem, _ in SOURCE_SPECS
    ]
    manifest = source_path("SSOT_ALL_MANIFEST", INTERNAL_VERSION)
    source_files_with_manifest = source_files + [manifest]
    registries = [
        registry_path(stem, INTERNAL_VERSION) for stem, _ in REGISTRY_SPECS
    ]
    aggregate = source_path("SSOT_ALL", INTERNAL_VERSION)
    seal = source_path("CURRENT_SHA256", INTERNAL_VERSION)

    for path in source_files_with_manifest + registries + [aggregate, seal]:
        if not path.exists():
            errors.append(f"missing: {path}")
    if errors:
        raise SystemExit("\n".join(errors))

    for path in source_files + registries:
        try:
            block = active_block(path.read_text(encoding="utf-8"))
        except AssertionError:
            errors.append(f"active boundary missing: {path}")
            continue
        if "(값들) 보임." in block:
            errors.append(f"stale boim surface in active block: {path}")
        if "deprecated legacy input" in block:
            errors.append(f"stale compatibility claim in active block: {path}")

    decisions = source_path("SSOT_DECISIONS", INTERNAL_VERSION).read_text(
        encoding="utf-8"
    )
    for idx in range(1, 43):
        if f"RD-{idx:03d}" not in decisions:
            errors.append(f"missing decision RD-{idx:03d}")
    for idx in range(1, 19):
        if f"SV-D{idx:02d}" not in decisions:
            errors.append(f"missing decision SV-D{idx:02d}")

    manifest_text = manifest.read_text(encoding="utf-8")
    if "source_document_count: 19" not in manifest_text:
        errors.append("manifest source count")
    if "generated_registry_count: 12" not in manifest_text:
        errors.append("manifest registry count")

    seal_text = seal.read_text(encoding="utf-8")
    for rel, expected in parse_hash_rows(seal_text):
        path = ROOT / rel
        if not path.exists():
            errors.append(f"sealed file missing: {rel}")
        elif sha256_file(path) != expected:
            errors.append(f"seal mismatch: {rel}")

    public_dir = PUBLIC / PUBLIC_VERSION
    public_manifest = public_dir / f"SPEC_MANIFEST_{PUBLIC_VERSION}.md"
    public_seal = public_dir / f"SPEC_SHA256_{PUBLIC_VERSION}.md"
    if not public_manifest.exists() or not public_seal.exists():
        errors.append("public manifest or seal missing")
    else:
        for rel, expected in parse_hash_rows(public_seal.read_text(encoding="utf-8")):
            path = public_dir / rel
            if not path.exists():
                errors.append(f"public sealed file missing: {rel}")
            elif sha256_file(path) != expected:
                errors.append(f"public seal mismatch: {rel}")
        for path in public_dir.rglob("*"):
            if path.is_file() and path.name not in {
                f"SPEC_COMPATIBILITY_AND_NONCLAIMS_{PUBLIC_VERSION}.md",
                f"SPEC_MANIFEST_{PUBLIC_VERSION}.md",
                f"SPEC_SHA256_{PUBLIC_VERSION}.md",
            }:
                text = path.read_text(encoding="utf-8")
                if re.search(r"보임\s*\{", text):
                    errors.append(f"legacy boim example in public spec: {path}")
                if "(값들) 보임." in text:
                    errors.append(f"stale boim surface in public spec: {path}")

    for path in [
        SSOT_ROOT
        / "walks"
        / "gogae10"
        / "w100_public_observation_scene_composition"
        / "fixtures"
        / "representative_candidate.ddn"
    ]:
        if "(진자_공개상태: 진자_공개상태) 보임." not in path.read_text(
            encoding="utf-8"
        ):
            errors.append(f"walk fixture not updated: {path}")

    if errors:
        raise SystemExit("CHECK FAILED\n" + "\n".join(errors))
    print(
        json.dumps(
            {
                "status": "PASS",
                "internal": INTERNAL_VERSION,
                "public": PUBLIC_VERSION,
                "source_count": 19,
                "registry_count": 12,
                "family_tree_sha256": tree_digest(source_files + registries, SSOT),
                "manifest_sha256": sha256_file(manifest),
                "seal_sha256": sha256_file(seal),
                "public_manifest_sha256": sha256_file(public_manifest),
                "public_seal_sha256": sha256_file(public_seal),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        apply()


if __name__ == "__main__":
    main()
