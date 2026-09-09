# 셈그림 Round 0 운영 패킷 V1

## 현재 상태

- 목표: 포물선 첫 프로젝트를 열고, 바꾸고, 실행하고, 저장하고, 다시 열고, 보기 링크로 공유하고, 복제하는 흐름을 관찰한다.
- 현재 최고 등급: `READY_FOR_CONTAINER_RUNTIME`.
- `RELIABILITY_CLOSED`: 달성.
- `ACTUAL_CONTAINER_VERIFIED`: 미달성.
- `PRIVATE_IDC_DEPLOYED`: 미달성.
- 실제 참여자 수: `0`.
- 실제 성공 수: `0`.

## 참여자 흐름

1. 90초 안에 포물선 첫 프로젝트를 열고 실행한다.
2. 값 하나를 바꾸고 그래프와 궤적 변화를 확인한다.
3. 자기 이름 대신 비식별 project title로 저장한다.
4. 새 브라우저 또는 새 세션에서 다시 연다.
5. 보기 링크를 공유 가능한 읽기 전용 링크로 확인한다.
6. 보기 링크에서 복제하여 자기 콘텐츠를 만든다.
7. 문제 발생 시 진행자에게 되돌리기 또는 지원 요청을 한다.
8. capability 링크 원문은 개인 메신저, 문서, 로그에 붙여넣지 않는다.
9. 데이터 보존 기간과 삭제 요청 절차를 안내받는다.
10. 운영자는 backup, rollback, incident 체크리스트를 따른다.

## 성공 판정

1차 성공은 참여자가 도움 없이 또는 한 번의 안내 안에서 다음 핵심 흐름을 끝낸 경우다.

```text
open -> change -> run -> save -> reopen -> share/clone
```

성공 수치는 실제 참여자 증거가 있을 때만 기록한다. 자동화 runner PASS는 외부 사용자 성공으로 세지 않는다.

## 데이터와 철회

- 개인 이름, 이메일, IP 원문은 기록하지 않는다.
- 프로젝트 제목은 비식별 문자열로 둔다.
- 삭제 요청은 비식별 project id와 요청 시각만 남긴다.
- 참여 철회는 관찰 기록에서 개인 식별 가능 메모를 제거하는 절차로 처리한다.
- capability 링크는 필요한 시간 동안만 보관하고, 원문을 장기 기록에 남기지 않는다.

## 운영자 체크리스트

- first-run reliability matrix PASS 여부 확인.
- 현재 배포 등급과 미도달 범위 안내.
- backup 생성 가능 여부 확인.
- rollback은 code pointer만 바꾸고 data를 자동 삭제하거나 되감지 않는다.
- incident 발생 시 capability 원문, Authorization, DDN 본문, project snapshot 전체를 티켓에 붙이지 않는다.
- `ROUND0_INVITATION_APPROVED=1` 없이는 실제 초대나 메시지 발송을 하지 않는다.

## 현재 미실행 경계

- 실제 OCI container run 없음.
- 운영 TLS 완료 주장 없음.
- private IDC canary 없음.
- 실제 참여자 없음.
