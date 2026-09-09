# 또니랑 AI 베타 Round 0 시작 가이드

이 번들은 처음 쓰는 사용자가 CLI만으로 또니랑 샘플을 열고, 고치고, 오류를 읽을 수 있는지 확인하기 위한 자료입니다.

## 사용 규칙

- 제공된 번들 안의 파일만 보고 진행합니다.
- 제공된 파일 밖의 저장소 지식, 이전 세션 기억, 검색으로 문제를 우회하지 않습니다.
- 문서에 없어서 막히면 그것이 발견입니다. 추측으로 해결한 경우도 friction log에 남깁니다.
- 실행 자체보다 "어디서 막혔는지"가 더 중요합니다.

## 첫 실행

저장소 루트에서 다음 명령을 실행합니다.

```bash
cargo run --manifest-path tools/teul-cli/Cargo.toml -- check work/beta/round0/BETA_USER_BUNDLE/samples/pendulum_edit.ddn
cargo run --manifest-path tools/teul-cli/Cargo.toml -- run work/beta/round0/BETA_USER_BUNDLE/samples/pendulum_edit.ddn --madi 10
```

성공하면 `CLI_ONE_PAGER.md`를 보고 다른 샘플도 실행합니다.

## 기록

막힘, 우회, 불편, 제안은 `FRICTION_LOG_TEMPLATE.detjson` 형식으로 기록합니다. 문서에 답이 없으면 `인용문서` 값에 `문서 부재`라고 적습니다.
