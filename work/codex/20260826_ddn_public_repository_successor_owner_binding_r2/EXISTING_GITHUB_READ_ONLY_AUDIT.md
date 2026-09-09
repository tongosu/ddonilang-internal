# Existing GitHub remote read-only audit

## live result — 2026-08-26

```text
REMOTE: https://github.com/tongosu/ddonilang.git
FULL_NAME: tongosu/ddonilang
VISIBILITY: PUBLIC
PRIVATE: false
ARCHIVED: false
DEFAULT_BRANCH: main
LIVE_HEAD: dafde506c20c924330d0728d7606a7b6480a1e05
PUBLIC_BRANCH_COUNT_PAGE_1: 1
MAIN_PROTECTED_FLAG: true
LICENSE_SPDX: NONE
PAGES: false
DISCUSSIONS: false
```

API metadata의 last push는 2026-08-09이며 live commit 자체의 author date는 2026-07-11이다. 현재 내부 개발 계보와 일치하지 않는 오래된 공개 snapshot이다.

## live public tree inventory

- tracked files: 11,696
- `pack/**`: 6,488
- `solutions/**`: 2,201
- `tests/**`: 1,385
- `work/**`: 122
- `docs/**`: 185
- `publish/**`: 111
- `docs/ssot/**`: 0
- LICENSE/SECURITY/CONTRIBUTING/CODE_OF_CONDUCT: 0

`work/_session_deltas`, beta packet, internal context/proposal/report가 live public tree에 들어 있다. 곧바로 민감정보 사고라고 판정하지는 않지만 새 public projection 정책과 맞지 않는다.

## snapshot secret signature check

- private-key header: 0
- AWS access-key pattern: 0
- OpenAI token pattern: 0
- GitHub token pattern: initial 1, source identifier가 정규식과 우연히 겹친 false positive로 확인

이것은 live snapshot의 좁은 signature scan이다. 전체 Git history secret scan, GitHub secret-scanning alert, issue/release/wiki/attachment, clone/fork exposure까지 닫지 않는다.

```text
CONFIRMED_SENSITIVE_DATA_INCIDENT: NO
HISTORY_WIDE_SECRET_AUDIT: OPEN
EXISTING_REPOSITORY_PRIVATE_CHANGE_RECOMMENDED: YES
EXISTING_REPOSITORY_PRIVATE_CHANGE_AUTHORIZED: NO
HISTORY_REWRITE_AUTHORIZED: NO
```

visibility 변경 전에는 [GitHub 공식 visibility 변경 지침](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)에 따라 fork, ruleset/protection, Actions, Pages, stars/watchers, 접근권한 영향을 다시 확인해야 한다. private 전환은 이미 외부에 복제된 과거 bytes를 회수한다는 뜻이 아니다.
