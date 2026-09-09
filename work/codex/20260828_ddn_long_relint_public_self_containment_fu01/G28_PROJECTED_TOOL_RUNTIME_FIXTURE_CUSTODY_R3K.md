# G28 projected tool runtime fixture custody — R3K

## 고정점

```text
PREDECESSOR_HANDOFF: 934c7cfb6d01a0a043cdb7c51ed83d4ec9d96617
PRODUCT_TEST_FIXED_HEAD: 91e56e597a920a8346e18bf68fa80afadf92d3aa
PRODUCT_TEST_DIRECT_PARENT: 934c7cfb6d01a0a043cdb7c51ed83d4ec9d96617
PRODUCT_RUNTIME_MEANING_CHANGE: 0
PUBLIC_PACK_MEMBERSHIP_CHANGE: 0
```

## 원인과 교정

R3J projected `ddonirang-tool`의 source fixed-head 대비 추가 17 RED는 제품 런타임
결함이 아니라 `#[cfg(test)]` 단위 테스트가 projection에서 권리상 제외된 private
`pack/**` 파일을 실행 시점에 읽은 결과였다.

정확한 분류는 다음과 같다.

```text
network snapshot parsing/state hash: 3
W24 through W33 parameter/state hash: 10
container resource state hash: 1
runtime typecheck matrix: 1
eco macro/micro c02 and c03: 2
TOTAL: 17
```

`tool/src/self_contained_test_sources.rs`를 기존 crate-owned test fixture owner로 유지해
동일 입력과 기대 hash를 상수로 봉인했다. 경로 읽기 자체를 검증하는 network/eco
cases는 task-owned 임시 디렉터리에 상수를 기록한 뒤 기존 제품 함수를 호출한다.
W24~W33은 test-only parser에 문자열을 직접 전달하고, runtime typecheck는 이름과
source의 고정 배열을 순회한다. private pack을 public projection에 추가하거나 제품
runtime fallback을 만들지 않았다.

## 직접 재현

```text
source fixed HEAD tool binary: 405 PASS / 2 RED
R3K fresh projection tool binary: 405 PASS / 2 RED
projection-caused additional RED: 0
remaining RED exact family: ai_prompt docs/ssot authority 2
R3K projection validator: PASS 894/894 A/B
R3K projection/validator unit tests: PASS 18/18 A/B
fresh Git A/B commit: bb5b646ed72620f9942a460f9ea8bf4c744b7dbd
fresh Git A/B tree: a3bc8b2da6392734e07add737e4b9a1de8578fb9
fresh Git A/B status: clean 0
network access: 0
```

`teul-cli`의 projection-only 추가 RED 1건인
`run_cli_real_gaji_package_publish_download_vendor_matches_source`는 실제
`gaji/std_math` package 권리·membership D3 결정이 필요하다. synthetic fixture로
바꾸면 real-package 증거를 약화하고, package를 포함하면 공개 권리 결정을 선점하므로
교정하지 않았다.

## 판정

```text
G28_DDONIRANG_TOOL_PRIVATE_RUNTIME_FIXTURE_GAP: CLOSED
G28_PROJECTED_TOOL_ADDITIONAL_FAILURES: 0
G28_TEUL_CLI_GAJI_STD_MATH_RIGHTS_GAP: OPEN
G28_OVERALL: PARTIAL
SELF_PASS: NOT_CLAIMED
PUBLICATION_READY: NOT_CLAIMED
```
