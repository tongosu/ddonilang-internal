# Security policy candidate

## 범위

공개 projection에 실제 포함되고 receipt로 봉인된 source와 artifact만 이 정책 후보의
기술 범위다. internal repository, private fixture, official store, 사용자 DB와
미공개 Workbench/browser bundle은 공개 범위가 아니다.

## 제보

공개 security contact와 supported release가 아직 Owner 결정되지 않았다. 실제 공개 전
다음 값을 채우고 검증해야 한다.

    SECURITY_CONTACT: OWNER_DECISION_REQUIRED
    SUPPORTED_RELEASES: NONE_PUBLISHED
    RESPONSE_SLA: OWNER_DECISION_REQUIRED

민감한 token, key, 개인정보 또는 실제 exploit 내용은 public issue에 게시하지 않는다.
contact가 확정되기 전에는 공개 취약점 접수 준비 완료를 주장하지 않는다.

history-wide secret audit와 GitHub visibility 변경은 별도 승인 관문이다.
