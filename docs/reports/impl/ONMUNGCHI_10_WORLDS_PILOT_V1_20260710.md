# 온뭉치 가등급 10세계 pilot W3 보고서

상태: machine-verified pilot / corpus promotion open / `닫힘-문서`

## 결과

- `corpus_card.v1` 후보 스키마 1개.
- current-line 대표 차시 카드 10개.
- 기계 관문 4개 x 10세계 = 40개 PASS.
- 낭독 관문 10개 `pending_human_review`.
- 사용자 결정 10개 `pending`.
- 정식 수록 0개.

기계 관문은 pack 실행, canonical roundtrip, 리믹스 손잡이 형식, child/teacher few-shot 짝 형식이다. 각 원문은 대표 마디로 두 번 실행해 카드의 `state_hash`와 `trace_hash`가 모두 재현되는지 확인한다.

## 선택 원칙

원 기획안의 이름 붙은 첫 10세계는 착수 후보였고 제작 시 current-line과 재대조하도록 되어 있다. 이번 pilot은 새 예제 10개를 급히 만드는 대신 제품 `representative_v1` 근거가 있는 다음 10개를 선택했다.

1. 일차함수 그래프
2. 포물선 운동
3. 수요·공급과 세금
4. 선형 탐색 단계 보기
5. 상변화와 온도 그래프
6. 격자 상태와 낙하 조각
7. 속도 기록 그래프
8. 복리 성장과 생산성
9. 자료 바꾸기
10. 상태 전이와 체력 변화

## 산출물

- `pack/onmungchi_10_worlds_pilot_v1/pilot.detjson`
- `pack/onmungchi_10_worlds_pilot_v1/corpus_card.schema.json`
- `pack/onmungchi_10_worlds_pilot_v1/cards/*.detjson`
- `tests/run_onmungchi_10_worlds_pilot_check.py`

```text
python tests/run_onmungchi_10_worlds_pilot_check.py
PASS [onmungchi-10-worlds-pilot-v1] OK cards=10 machine_gates=40 human_readaloud_pending=10 owner_pending=10 included=0
```

## 경계

- 10개 카드의 lifecycle은 모두 `검증중`이다.
- 낭독 확인자와 사용자 결정은 AI가 채우지 않는다.
- 온뭉치 수록 10/10, 잠김 corpus, 100세계 완료를 주장하지 않는다.
- `docs/ssot/**`, parser, runtime, 제품 UI 변경 없음.
