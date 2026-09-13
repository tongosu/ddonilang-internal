# P1-A FU01 Evidence Correction Handoff — 2026-08-29

## 판정

```text
P1A_FU01_EVIDENCE_CORRECTION_IMPLEMENTED_UNDER_REREVIEW
P1A_CLOSURE_NOT_ISSUED
```

이 handoff는 P1-A 제품 결함 교정이 아니다. 독립검토 `PASS_WITH_FOLLOW_UP`에서
발견된 fault-injection mutation 명칭과 실제 동작의 불일치만 고친 evidence-only
후속이다. 제품 source, tracked WASM, SSOT, public SPEC, visible UI는 byte-unchanged다.

## 권위와 계보

- internal CURRENT: SSOT v25.19.0 / RD-001~461
- public Language SPEC CURRENT: v0.6.0
- P1-A product/test fixed: `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`
- P1-A handoff: `151923c9d6a0708574416895c159ab21ffa87795`
- independent review: `b65463cc8f6f981e290000ffb4e14e1db6699fad`
- review report: 12,967 bytes / SHA-256 `5e900b72cdada47f03b025677c8ba3185eb1a3fec408488330f45214b1d0ab04`
- FU01 correction product/test fixed: `25a271bfab45ef5c0b5f9abb67d6323547e1f5b4`
- FU01 fixed tree: `3644bfb81f41c0226d395c26188cb87eb93b91c3`
- direct parent: `b65463cc8f6f981e290000ffb4e14e1db6699fad`
- merge count: 0
- fixed diff: `tests/run_v1_core_supported_ingress_fault_injection_w1.py` 한 파일

## 교정 내용

`tests/run_v1_core_supported_ingress_fault_injection_w1.py`의 mutation 축을 다음처럼
정확히 결속했다.

1. `PROFILE_IDENTITY_DISABLED`: 기존 축 유지
2. `PREV25_PATH_SUBSTITUTION`: 기존의 V25 path 전체 PreV25 치환을 실제 의미에 맞게 개명
3. `HIDDEN_PREV25_RETRY`: V25 실패 뒤
   `.or_else(|_| Self::from_source_with_mode(...))`를 실행하는 실제 fallback 변이 추가
4. `RECURSION_GUARD_BYPASS`: 기존 축 유지

runner는 각 mutation이 nonzero RED인지뿐 아니라 해당 boundary의 예상 실패 test 이름이
출력에 존재하는지도 검사한다. 각 RED 뒤 원본 runtime bytes를 복원하고 SHA-256을
확인한 다음 focused suite GREEN을 다시 실행한다. 마지막에도 focused GREEN과 원본
SHA-256을 재확인한다.

## fixed identity

- runner Git blob: 4,339 bytes
- runner SHA-256: `68efdc3a831819f076cf1f5d3e18f64d26c21f5146e068078d62ee6ad054e33c`
- runtime Git blob: 1,110,630 bytes
- runtime Git blob SHA-256: `e81002d0f579a20960d5b90c3a82955c8f20bf46dcd6b339a756d0e87e0994a5`
- execution worktree runtime: 1,139,543 bytes / CRLF 28,913
- execution worktree exact-restore SHA-256:
  `f8752ac4a2841eebfc4cd15c0d7ec461d7c7273851e7139a6e8aa1c894b00cbc`
- runtime start/end hash and CRLF count: exact match
- runtime Git diff after all mutations: 0

Git blob identity와 checkout CRLF identity는 서로 다른 층이다. runner는 실행한 동일
worktree의 시작 bytes를 보존하며, 각 mutation 뒤 CRLF를 포함한 전체 bytes를 exact
restore한다.

## mutation RED → exact restore → GREEN

| mutation ID | RED exit | 관찰 signature | restore / GREEN |
|---|---:|---|---|
| `PROFILE_IDENTITY_DISABLED` | 101 | `p1a_v1_core_profile_accepts_definition_and_rebinding`, `p1a_supported_profile_run_executes_v25_definition_and_rebinding` | exact hash / focused 6/6 |
| `PREV25_PATH_SUBSTITUTION` | 101 | `p1a_v1_core_profile_accepts_definition_and_rebinding`, `p1a_supported_profile_run_executes_v25_definition_and_rebinding` | exact hash / focused 6/6 |
| `HIDDEN_PREV25_RETRY` | 101 | `p1a_v1_core_profile_reports_exact_legacy_definition_migration`, `p1a_supported_profile_run_fails_closed_for_profile_and_v25_boundaries` | exact hash / focused 6/6 |
| `RECURSION_GUARD_BYPASS` | 3221225725 | `p1a_v1_core_profile_rejects_direct_and_mutual_recursion_deterministically` | exact hash / focused 6/6 |

최종 출력:

```text
P1A_MUTATION_PASS mutations=4 restore_sha256=f8752ac4a2841eebfc4cd15c0d7ec461d7c7273851e7139a6e8aa1c894b00cbc
```

## 회귀·parity·freshness

- focused native: 6/6 PASS
- native/WASM exact payload: 1/1 PASS
- tracked-WASM cases: 8/8 PASS
- deterministic repeats: 3
- partial summary leak: 0
- `cargo test -p ddonirang-tool --lib`: 523/523 PASS
- official tracked WASM freshness: PASS
- `git diff --check`: PASS
- runner Python compile check: PASS

고정 tracked artifacts:

- WASM: 5,553,353 bytes / SHA-256
  `29480a59d264cffa280d6c1fb8a5a74da857955a6f028cd8b2adaf71e2366f51`
- JS: 89,038 bytes / SHA-256
  `c5a80302a3a872fab1e8d14c2385f8b5b6ddde8cfc1096c64ee0231e4ec8df3d`
- manifest: 18,938 bytes / SHA-256
  `7ad02442eb9b6542e586b86880b7814560611cf927a51cd657e2c72ddc7b843e`

## custody

- 기존 P1-A branch와 product worktree 재사용
- 새 branch/worktree/product writer 생성: 0
- 제품 source diff: 0
- tracked WASM diff: 0
- SSOT/SPEC/visible UI diff: 0
- server/port/browser/protected process start/stop/restart/kill: 0
- 종료 관찰 Node PID: 10개
- TCP 8787 listener: absent
- cargo/rustc/python residue: 0
- task-owned 기존 untracked preflight 문서는 보존하며 stage하지 않음

## targeted independent rereview 요청

재검토자는 이 handoff commit을 review parent로 사용하고, 제품/test 검증은 반드시
`25a271bfab45ef5c0b5f9abb67d6323547e1f5b4`에서 수행한다.

검토 범위는 다음으로 제한한다.

1. fixed commit diff가 runner 한 파일뿐인지
2. 네 mutation ID와 실제 replacement가 정확히 대응하는지
3. 실제 `HIDDEN_PREV25_RETRY`가 `.or_else(...)` fallback인지
4. 네 축이 각각 예상 RED signature를 내는지
5. 각 축 뒤 CRLF 포함 exact restore와 focused GREEN인지
6. 제품 source·WASM·SSOT·SPEC·visible UI diff 0인지
7. review commit이 report+reviewer session delta 두 파일뿐인지

## OPEN / NONCLAIMS

- targeted independent plain PASS: OPEN
- P1-A closure: 미발급
- Foundation-12: OPEN
- 18/18 V1-Core membership과 전체 4/4 execution contract·9/9 exclusion: 미승격
- public executable/command membership과 stable profile spelling: OPEN
- Workbench default ingress와 visible UI behavior: OPEN
- whole P0/P1/V1 closure/readiness, P2~P6, RC, release, activation, legal status,
  Owner Human Smoke PASS, Human PASS, external-user success: OPEN

이 evidence correction과 self-test는 독립검토 PASS나 제품·membership·release 승격을
대신하지 않는다.
