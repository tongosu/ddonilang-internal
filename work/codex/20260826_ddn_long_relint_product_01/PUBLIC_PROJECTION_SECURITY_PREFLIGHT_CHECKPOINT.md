# DDN-LONG-RELINT-PRODUCT-01 G29 preliminary projection security checkpoint

이 checkpoint는 mutable R1 projection 현재 tree의 bounded 사전 감사다. clean integration
successor에서 수행할 최종 G29나 history-wide secret audit를 대신하지 않는다. matched
secret-like value는 보고서에 복사하지 않고 category·path·line·match hash만 기록했다.

## result

```text
PROJECTION_FILES: 3483
STRONG_SECRET_PATTERN_FINDINGS: 0
SENSITIVE_FILE_CANDIDATES: 0
EXECUTABLE_OR_BYTECODE_CANDIDATES: 15
ARCHIVE_CANDIDATES: 0
REVIEW_BINARY_CANDIDATES: 11
INTERNAL_MARKER_OCCURRENCES: 101
INTERNAL_MARKER_PATHS: 28
STATUS: FAIL_CLOSED
```

strong-pattern 0은 다음 패턴의 현재 tree match가 없다는 뜻뿐이다.

```text
PEM private-key header
AWS access-key id
GitHub token prefix
Google API key
OpenAI API key
Slack token
```

generic secret assignment, entropy audit, Git history, remote state는 이번 bounded scan의
coverage가 아니다.

## mutable projection residue

15개 executable/bytecode candidate는 모두 `tests/__pycache__/*.cpython-313.pyc`이며 합계
231,946 bytes다. source commit `905efb4a...`의 Git tree에는 `tests/__pycache__` member가
없다. 따라서 R1 projection이 검증 중 생성물을 받아 immutable output identity를 잃은
것이다. 기존 projection을 삭제·정리하지 않고 증거로 보존한다.

G25 successor requirements:

```text
PYTHONDONTWRITEBYTECODE: 1 or equivalent isolated cache owner
PROJECTION_OUTPUT_WRITE_AFTER_GENERATION: 0
__pycache__ / *.pyc allowlist: empty
A/B output tree identity: exact
post-validation output tree identity: unchanged
```

## binary role candidates

review-required binaries 11개는 다음 두 역할로 분리한다.

- `tool/assets/detmath/lut_sin_v1.dtm`: runtime deterministic math asset candidate 1
- CLI W17/W20/W22 `.bin/.packet/.detbin`: golden fixture candidates 10

확장자만으로 제거하지 않는다. runtime asset은 product role과 hash를 결속해야 하고,
golden fixture는 D7 public conformance root에 실제 필요할 때만 포함한다.

## internal markers

101 occurrences의 분류:

```text
PRIVATE_ABSOLUTE_PATH_I: 14
PRIVATE_ABSOLUTE_PATH_C: 35
PRIVATE_SSOT_PATH: 52
```

기존 G20의 15-file 수치는 `I:/home/...`와 `docs/ssot/ssot` 두 marker만 사용한 최초
하한선이다. 이번 scanner는 C:/ fallback, `docs/ssot/pack|walks|age`까지 넓혀 28 paths를
찾았다. `PUBLIC_PATH_PORTABILITY_MIGRATION_PLAN.md`의 제품·utility·conformance 분류를
successor scanner coverage에 맞춰 재검증해야 한다.

## custody

```text
AUDIT_TOOL: audit_public_projection_security.py
LEDGER: PUBLIC_PROJECTION_SECURITY_PREFLIGHT.detjson
LEDGER_BYTES: 28606
LEDGER_SHA256: 3ce54d8ce776ced0d83e4b7f45fd61c6994bdbc2c6022a6a71814f286bec029c
MATCHED_SECRET_VALUES_DISCLOSED: false
NETWORK_ACCESS: 0
CURRENT_TREE_ONLY: true
HISTORY_WIDE_AUDIT_CLAIM: false
FRESH_SUCCESSOR_PROJECTION_CLAIM: false
```
