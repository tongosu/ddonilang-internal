# Code, docs, assets and third-party rights custody audit

## verdict

```text
D8_RIGHTS_SEPARATION_POLICY: CLOSED
APACHE_2_0_CODE_DIRECTION: SOUND_WITH_REQUIRED_RIGHTS_GUARDS
APACHE_2_0_FINALIZATION: OPEN
PUBLIC_LICENSE_FILE_LANDING: NOT_AUTHORIZED_YET
```

이 문서는 법률 자문이나 최종 권리 확인서가 아니다. 공개 투영 전에 무엇을 누구의 근거로 확인해야 하는지 분리한 custody audit다.

## code

- Git shortlog identity: `urihanl` 857, `또니` 71 commits
- 두 identity의 실제 동일인 여부, 고용/위탁 관계, 외부 제공 코드 여부는 Git metadata만으로 증명되지 않음
- repository LICENSE/NOTICE: 없음
- preferred candidate: [Apache License 2.0 공식 원문](https://www.apache.org/licenses/LICENSE-2.0)

최종 확정에는 Owner의 원저작/양도 가능성 확인, 외부 기여 목록, 복사·변형한 코드의 origin, 특허·상표 경계 확인이 필요하다.

## third-party dependencies

local cached metadata에서 확인한 범위:

- Rust external packages: 196, license metadata undeclared 0
- 대부분 MIT/Apache-2.0/Unicode/BSD/ISC/Zlib/CC0 계열 선택식
- LGPL-2.1-or-later가 대안 중 하나로 포함된 package 1건은 실제 선택 license와 배포 조건 확인 필요
- Node packages: 3 — Apache-2.0 2, MIT 1
- automated license/SBOM tools `cargo-deny`, `cargo-about`, `gitleaks`, `trufflehog`: 현재 설치 안 됨

package metadata가 license compatibility와 binary notice 의무를 자동으로 증명하지 않는다. PUBLIC_RELEASE에는 locked dependency inventory, chosen license, source URL/version, required notice/source-offer 여부를 담은 ledger/SBOM을 요구한다.

## documentation

`publish/**`, public SPEC, QUICKSTART, examples 설명, lesson/curriculum 문서는 code와 별도 저작물로 취급한다.

```text
DOCS_LICENSE_DIRECTION: OPEN
DOCS_LICENSE_EXACT_CHOICE: OPEN
CODE_LICENSE_AUTO_APPLIES_TO_DOCS: NO
```

후속 후보는 CC BY 4.0 또는 Apache-2.0 통일안이지만, Owner 결정 전 문서 license를 추정하지 않는다.

## assets and trademark

R1 public 후보에서 확인된 이미지 asset은 2개다.

- `publish/assets/ddonirang_wordmark.png` — 158,799 bytes, SHA-256 `126cd087156278841860532796e7de9ef950ae65a0ae752f0fc02e9a631b13cc`
- `publish/assets/ddonirang_wordmark.svg` — 1,797 bytes, SHA-256 `6c5091ca4cf32b97f5652dd2a9f1e4a04652466a993d46c9eb697f9c4ff7a5e9`
- 최초 확인 commit: `6d42f88c...`, Git author `urihanl`
- embedded license/origin declaration: 없음

Git author만으로 창작·상표 권리를 확정하지 않는다. Owner가 직접 제작/권리 보유를 확인하면 per-asset ledger에 기록한다. wordmark·name의 trademark policy는 code/doc license와 별도다.

## examples, lessons and data

DDN samples, curriculum/lesson text, CSV/JSON fixture에도 별도 source/origin/redistribution role을 붙인다. 알 수 없는 asset이나 lesson은 기본적으로 public projection에서 제외한다.

## DCO

외부 기여는 [Developer Certificate of Origin 1.1 공식 원문](https://developercertificate.org/) 기준의 `Signed-off-by`를 요구한다. DCO는 inbound contribution provenance를 돕지만 기존 코드·asset의 outbound license 권리를 대신 증명하지 않는다.
