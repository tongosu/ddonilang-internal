# 또니랑 (Ddonilang)

> 한국어로 프로그램·시뮬레이션·교과 실험을 만들고, 같은 입력을 다시 재현할 수
> 있도록 설계하는 프로그래밍 언어와 도구입니다.

[![Public CI](https://github.com/tongosu/ddonilang/actions/workflows/seamgrim-ci.yml/badge.svg)](https://github.com/tongosu/ddonilang/actions/workflows/seamgrim-ci.yml)
[![Language SPEC](https://img.shields.io/badge/Language%20SPEC-v0.5.0-blue)](publish/spec/CURRENT.md)
[![Product status](https://img.shields.io/badge/product-status%20matrix-orange)](publish/PRODUCT_SUPPORT_CURRENT.md)

![또니랑 로고](publish/assets/ddonirang_wordmark.png)

## 무엇을 만드는 프로젝트인가요?

또니랑은 한국어를 화면 장식이 아니라 프로그램의 의미를 표현하는 언어로 사용합니다.

- **한국어 중심 문법**: 이름·조사·받는자리의 뜻이 코드 구조에 드러납니다.
- **결정적 실행**: 같은 입력·판본·설정은 같은 결과와 기록으로 이어져야 합니다.
- **검증 가능한 AI 협업**: AI가 만든 코드도 정본화·테스트·기록으로 다시 확인합니다.
- **게임과 교과 실험**: 일반 프로그램뿐 아니라 수학·물리·경제·화학·역사 자료를
  실행하고 비교하는 도구로 확장합니다.
- **보기와 실행의 분리**: 세계의 값과 기록이 실행 진실을 가지며, 화면은 이를
  임의로 추측하지 않고 명시적으로 보여줍니다.

## 1분 첫 실행

필요한 것은 Rust와 Cargo입니다.

```sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
```

예제 내용은 다음과 같습니다.

```ddn
x <- 15.
y <- 8.
합 <- (x + y).

"첫 결과" 보여주기.
합 보여주기.
x 보여주기.
y 보여주기.
```

결과에서 `23`, `15`, `8`을 확인한 뒤 숫자를 바꾸어 다시 실행해 보세요.
더 자세한 과정은 [10분 빠른 시작](publish/QUICKSTART.md)을 따릅니다.

## 현재 상태를 먼저 확인해 주세요

또니랑은 언어 계약과 제품 구현 상태를 구분합니다.

| 구분 | 현재 상태 |
| --- | --- |
| GitHub 개발 줄기 | 보호된 `main`, Pull Request와 `seamgrim-gate` 통과 필수 |
| 공개 언어 계약 | [Language SPEC v0.5.0](publish/spec/CURRENT.md), docs-first current |
| 내부 SSOT | v24.25.0 live current, 공개 SPEC과 별도 계보 |
| 기본 첫 실행 | 값·계산·`<-`·`보여주기` CLI 경로 검증 |
| 고급 문법·표준 보기·모형 | 항목별로 docs-first, 검증 후보, 제품 OPEN이 섞여 있음 |
| 실제 브라우저·Human 검토 | 전체 기능 완료를 주장하지 않음 |

공개 SPEC에 문법이 있다고 해서 parser·runtime·CLI·WASM·브라우저 제품이 모두
완료된 것은 아닙니다. 정확한 항목별 상태는
[현재 제품 지원 상태](publish/PRODUCT_SUPPORT_CURRENT.md)를 확인하세요.

## 다섯 층의 실행 구조

고급 구현에서는 실행을 다음 다섯 층으로 구분합니다. 초보자가 첫 프로그램을
작성하기 위해 이 이름을 외울 필요는 없습니다.

| 층 | 역할 |
| --- | --- |
| 샘(Sam) | 외부 입력을 봉인합니다. |
| 이야기(Iyagi) | 시작 시점의 세계를 읽고 규칙을 평가합니다. |
| 누리(Nuri) | 승인된 변화를 원자적으로 적용합니다. |
| 거울(Geoul) | 변화·진단·영수증을 기록합니다. |
| 보개(Bogae) | 기록이 끝난 결과를 관찰하고 보여줍니다. |

AI 협업은 이 결정적 실행층을 몰래 바꾸는 여섯 번째 권위가 아닙니다. AI는 코드와
아이디어를 제안할 수 있지만, 결과는 같은 언어·테스트·기록 관문을 통과해야 합니다.

## 어디에 사용할 수 있나요?

- **프로그래밍 학습**: 한국어로 값·계산·조건·반복·자료구조를 배웁니다.
- **셈그림**: 시간에 따라 바뀌는 수학·물리 결과를 표·그래프·장면으로 탐구합니다.
- **결정적 게임과 시뮬레이션**: 입력과 상태 변화를 기록해 문제를 재현합니다.
- **교과 자료 탐구**: 출처·단위·결측을 보존하며 경제·화학·역사 자료를 비교합니다.
- **AI 실험**: 입력·시드·기록을 봉인해 정책과 결과를 비교하는 기반을 연구합니다.

일부 항목은 장기 방향이거나 docs-first 계약입니다. 현재 기본 제품에서 바로 사용할
수 있는지는 반드시 제품 지원표로 확인하세요.

## 문서 안내

- [빠른 시작](publish/QUICKSTART.md)
- [0~5층 학습 지도](publish/LEARNING_PATH.md)
- [현재 제품 지원 상태](publish/PRODUCT_SUPPORT_CURRENT.md)
- [공개 Language SPEC](publish/spec/CURRENT.md)
- [공개 문서 전체 목록](publish/INDEX.md)
- [다국어 시작 문서 17종](publish/i18n/INDEX.md)
- [다운로드 안내](publish/DOWNLOADS.md)

## 다국어 문서

다국어 문서는 `publish/i18n/<언어 코드>/`에 모읍니다. 번역본은 학습과 탐색을
돕는 안내이며, 언어 의미의 정본은 아닙니다. 사람 검토가 끝나지 않은 번역은
`starter translation / Human review open`으로 표시합니다.

현재 제공 언어: 한국어, 영어, 일본어, 터키어, 몽골어, 아이마라어, 바스크어,
칸나다어, 네팔어, 케추아어, 타밀어, 텔루구어, 중국어, 스페인어, 프랑스어,
독일어, sym3.

## 기여와 라이선스

버그 재현, 초심자 예제, 교과 실험과 문서 개선 제안을 환영합니다. 변경은 임시
분기와 Pull Request에서 공개 CI를 통과한 뒤 `main`에 병합합니다.

현재 저장소의 오픈소스 라이선스는 아직 owner가 확정하지 않았습니다. `LICENSE`
파일이 추가되기 전에는 코드의 사용·수정·재배포 권한이 자동으로 부여된다고
간주하지 마세요. 라이선스 결정 전에도 Issue를 통한 의견과 오류 제보는 가능합니다.

## 프로젝트의 시작

이 프로젝트는 영어 문법의 장벽과 블록 도구의 확장성 한계를 함께 줄이고,
아이들이 공부와 창작을 하나의 기억에 남는 작품으로 연결할 수 있게 하려는
문제의식에서 시작했습니다. 방향은 크지만, 완료 주장은 언제나 실제 증거의 범위로
제한합니다.
