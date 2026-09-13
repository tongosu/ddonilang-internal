# DDN-LONG-RELINT public self-containment Owner 결정 패킷

product/test fixed HEAD `91e56e59...`에서 결정 없이 가능한 non-browser 기술 교정과
G23/G24 deterministic candidate inventory는 끝났다.
다음 선택은 공개 membership 또는 authority meaning을 바꾸므로 Codex가 대신 정하지 않는다.

## D1. `ai-prompt` 공개 disposition

- A — public projection에서 명시적으로 제외하고 공개 CLI surface에서 비노출한다.
  가장 좁지만 CLI 전체와 동일하지 않다.
- B — independently sealed public authority bundle을 새로 만들어 함께 배포한다. 기능은
  보존되지만 SSOT-derived byte rights와 갱신 절차가 필요하다.
- C — public SPEC을 입력으로 재설계한다. 권위 의미가 바뀌므로 별도 제품/언어 결정이
  필요하며 이번 follow-up에는 비추천이다.

권고: B를 별도 owner-authorized slice로 설계하기 전까지 A 후보로 유지하되, 현재는
어느 것도 자동 착지하지 않는다.

## D2. public SPEC `CURRENT.md` history closure

읽기 전용 재감사에서 링크된 이전판/후보 tree 10개가 shared root에는 있으나 모두
Git 미추적임을 확인했다. 따라서 현재 source commit에서 exact bytes를 도출할 수 없다.

- A — CURRENT가 직접 링크하는 이전판/후보 10개 tree를 exact bytes로 포함한다.
  링크는 닫히지만 공개 projection 규모가 커진다.
- B — live current만 가리키는 별도 public-repository pointer successor를 정식 검토한다.
  작지만 public SPEC 내용 변경 절차가 필요하다.

권고: 기존 공개 history 보존 원칙과 일치하는 A. 단, untracked working-tree bytes를
authority로 쓰지 말고 별도 review-bound tracked commit과 rights 확인이 선행돼야 한다.

## D3. test fixture와 selected example rights

PC01 five-file pack, projectile lesson, `gaji/std_math`를 각각
`CODE_RIGHTS / LESSON_AND_SAMPLE_RIGHTS`에서 public include 가능한지 확인해야 한다.
unknown은 계속 제외한다. fixture를 몰래 synthetic product evidence로 승격하지 않는다.

R3K에서 `ddonirang-tool` runtime pack unit fixture 17건은 crate-owned test constants로
옮겨 공개 pack membership 없이 self-contained가 됐다. 이 기술 교정은 rights 결정을
닫지 않지만 해당 17건을 public include 대상으로 선택할 필요는 없게 한다.

fixed-head Git provenance 원장은 다음을 확인했다.

- code 1,050 tracked files / Git identities 2
- docs 20 tracked files / Git identities 2
- PC01 five-file pack 5 files / Git identity 1
- selected-example input 33 files / Git identity 1
- wordmark assets 2 files / Git identity 1
- live projectile lesson exact blob은 fixed-head object database에 없고 역사 후보와도
  byte-identical하지 않음

이것은 custody/provenance일 뿐 ownership 또는 공개 허가가 아니다. exact membership과
권리 상태를 Owner/권리 관리자가 결정해야 한다.

## D4. third-party license와 notice

offline locked inventory는 Cargo 196 + npm 3 = 199행이며 Cargo license 미선언은 0이다.
Cargo package/version 196개 중 로컬 license material이 없는 항목이 5개다.

```text
r-efi@5.3.0
wasip2@1.0.1+wasi-0.2.4
wasip2@1.0.2+wasi-0.2.9
winapi-i686-pc-windows-gnu@0.4.0
winapi-x86_64-pc-windows-gnu@0.4.0
```

selected license, required notice와 실제 release inclusion은 전부 미결정이다. 특히
AND/OR/Unicode/LGPL 대안 표현을 구현자가 임의로 선택하지 않는다. legal review와
notice closure를 별도 권리 관문에서 결정해야 한다.

## D5. tracked WASM single-family refresh

source-built A/B `ddonirang_tool_bg.wasm`은
`186f4fec75bfa2e0059eeb8fe4e0b830aed5f04a24caf88b46b25a8bb432b171`, tracked는
`77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34`다.
전체 G18 membership이 고정된 뒤 한 번만 refresh/promotion하도록 승인 여부를 결정해야 한다.

## D6. Workbench와 sealed offline browser custody

현재 R3K는 non-browser candidate라 `WORKBENCH_RUNTIME` required role을 요구하면 정확히
fail-closed한다. full G18/G26~G31을 위해서는 다음 exact 입력이 필요하다.

- 공개 포함할 Workbench HTML/JS/runtime path set과 rights status
- source-built WASM과 결속할 browser entrypoint
- network 없이 재현 가능한 browser dependency bundle identity와 재배포/사용 custody
- 실제 Edge workflow의 로컬 entrypoint와 expected receipt

기존 로컬 browser cache의 존재를 공개 dependency 권리나 sealed release artifact로
재해석하지 않는다. 이 입력 전에는 G31을 실행하거나 전체 자체완결성을 주장하지 않는다.

## 제안 재개 입력

```text
DDN_LONG_RELINT_PUBLIC_SELF_CONTAINMENT_OWNER_DIRECTION:
D1_AI_PROMPT_DISPOSITION: <A_EXCLUDE_PUBLIC_SURFACE | B_SEALED_PUBLIC_AUTHORITY_BUNDLE | C_PUBLIC_SPEC_REDESIGN>
D2_PUBLIC_SPEC_HISTORY_CLOSURE: <A_INCLUDE_EXACT_LINKED_HISTORY | B_REVIEWED_POINTER_SUCCESSOR>
D3_PUBLIC_RIGHTS_MEMBERSHIP: <exact paths and rights status>
D4_THIRD_PARTY_LICENSE_NOTICE: <selected licenses, required notices, legal review disposition>
D5_TRACKED_WASM_REFRESH: <AUTHORIZED_AFTER_FULL_SCOPE | NOT_AUTHORIZED>
D6_WORKBENCH_BROWSER_CUSTODY: <exact public paths, rights, sealed offline bundle, Edge entrypoint>
RESUME_EXISTING_GOAL: YES
RESUME_FROM_GATE: G18
```

## 2026-08-28 Owner direction 결속

Owner가 D1~D6 방향을 발행했다. exact 원문과 현재 집행은
`OWNER_DIRECTION_BINDING_D1_D6_R3L.md`에 보존한다.

```text
D1: FIRST_PUBLICATION_AI_PROMPT_EXCLUDED / SEALED_BUNDLE_SUCCESSOR_DEFERRED
D2: INCLUDE_EXACT_HISTORY_AFTER_TRACKED_REVIEW_BOUND_COMMIT
D3: PC01_PROJECTILE_GAJI_STD_MATH_UNKNOWN_RIGHTS_EXCLUDED
D4: DRAFT_INVENTORY_NOTICE_AUTHORIZED / LEGAL_RELEASE_OPEN / MATERIAL_5_OPEN
D5: REFRESH_ONLY_AFTER_FULL_MEMBERSHIP_AND_INDEPENDENT_PASS / FINAL_PROMOTION_NO
D6: READ_ONLY_CUSTODY_AUDIT_AUTHORIZED / PUBLIC_MEMBERSHIP_NO
```

따라서 이 패킷의 선택 질문은 답변됐지만 D2·D4·D5·D6의 외부 선행조건은 아직
충족되지 않았다. publication gate, release, Human PASS는 열리지 않았다.
