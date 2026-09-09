# Codex session delta — creator gaji circulation Wave 1

- 상태: Pending
- 목표: G0~G16 local-first 창작자 가지·가지곳간 순환
- START_HEAD: `d55e7524591d29943d77a6ab7676bc3a3e2adc2a`

## G0

- 최소 조상, branch, empty stage, clean `docs/ssot/**` 확인.
- 기존 dirty/untracked는 사용자 소유로 보존. 직접 겹치는 `tools/teul-cli/src/canon.rs`는 수정 대상에서 제외.
- 네이티브 다중 파일 authoring full promotion gate PASS.
- 독립 검토 결과는 발견되지 않았고 요청서만 존재하므로 자체 재감사로만 분류.
- 재사용 경계: Rust local project/lock, CLI gaji/registry archive, WASM project adapter, Workbench portable/durable store.
- 열린 제품 연결: AST 추출, 공통 lifecycle plans, Workbench shelf, 두 대표 수직, 4 viewport.

## 읽은 권위

- `AGENTS.md`, `AGENT_WORKFLOW.md`, `SSOT_POLICY.md`
- 목표 지시서 전체
- SSOT index와 LANG/PLATFORM/TOOLCHAIN의 project/gaji/gotgan/lock 관련 절
- 승인 Workbench brief는 G7 UI 착수 전 다시 대조한다.

## 비주장

- 외부 사용자 성공 수: 0
- public registry, account/trust/cloud 완료를 주장하지 않음.
- `docs/ssot/**` 변경 없음.

## G1

- project artifact와 gaji artifact를 분리하고 전체 project export를 가지로 이름만 바꾸는 방식을 금지.
- 기존 `gaji.toml`, registry archive/index, `ddn.lock`, `local_package_payload`를 재사용.
- 표준/나눔/내 profile은 모두 Wave 1 local 의미로 제한.
- publish/install/update/remove/remix의 immutable·stale-base·atomic rollback 불변식을 `g1_product_contract.detjson`에 봉인.

## G2

- `tool/src/local_project.rs`에 `ddn.gaji_extraction_plan.v1` 공통 Rust core 추가.
- 기존 project graph, `쓰임` parser, `드러냄` parser, normalized path를 재사용해 선택 모듈의 dependency closure·공개 API·포함/제외 파일·content hash 계산.
- 주석/문자열의 가짜 `드러냄` 비침범과 private-only 모듈 fatal을 direct Rust test로 검증.
- CLI `gaji plan`과 WASM `wasm_gaji_extraction_plan_json`은 같은 Rust JSON 함수를 호출.
- 검증: Rust extraction 2 tests PASS, teul-cli cargo check PASS, 실제 CLI fixture plan 출력 PASS.

## G3

- 공통 Rust core가 추출 plan에서 결정적 `gaji.toml + ddn/` artifact, file hash, package hash, provenance를 생성.
- artifact verifier가 schema, 필수 manifest/source, normalized duplicate path, file/package hash 변조를 거부.
- CLI `gaji seal`은 검증된 artifact를 임시 디렉터리에 쓴 뒤 rename으로 원자 materialize하고 기존 대상 overwrite를 거부.
- 기존 `gaji registry publish --package-dir`로 실제 deterministic zip과 local index 생성 PASS.
- 검증: artifact 결정성/tamper Rust test PASS, seal 실제 파일 생성 PASS, 동일 output 재봉인 `E_GAJI_SEAL_IMMUTABLE` PASS, registry publish PASS.

## G4

- Rust `ddn.local_gotgan_store.v1` projection이 검증된 artifact만 immutable publish하고 이름/설명/태그/공개 심볼/profile을 검색.
- 같은 profile/id/version 같은 bytes는 idempotent, 다른 bytes는 `E_GOTGAN_VERSION_IMMUTABLE`.
- 105개 역순 발행 후 동일 검색의 정렬/직렬화 결정성 direct test PASS.
- browser persistence adapter는 localStorage만 소유하고 publish/search 의미는 WASM 함수에 위임. Node syntax check PASS.

## G5

- 공통 Rust `ddn.gaji_lifecycle_plan.v1`에 install/update/remove와 expected source/lock 경계 추가.
- install은 검증 artifact를 `vendor/<id>/`, root `가지` alias, canonical `ddn.lock`으로 한 번에 산출.
- update는 기존 immutable vendor bytes를 새 artifact로 교체하고 remove는 참조 위치가 있으면 거부, 미사용이면 vendor/alias/lock 동시 정리.
- stale source/lock과 경로 충돌은 apply 가능한 source를 반환하지 않음.
- direct lifecycle 2 tests PASS, local project graph PASS, CLI/WASM virtual-source parity PASS.
- 기존 aggregate quality gate는 124초 실행 제한으로 결과 전 종료되어 최종 G16에서 충분한 제한으로 재실행 예정.

## G6

- extraction/artifact verification/publish/search/lifecycle Rust core를 실제 WASM exports로 재빌드·UI 복사.
- CLI `gaji plan`과 `gaji lifecycle-plan`은 같은 core adapter이며 실제 WASM binary와 canonical JSON byte equality 확인.
- lifecycle parity에서 resulting vendor tree, root alias, `ddn.lock` hash까지 동일함을 확인.
- stale source 고의 mismatch가 WASM에서 반드시 실패하는 negative control PASS.
- WASM freshness manifest 재생성 및 freshness gate PASS.

## G7

- file drawer의 실제 active module에 `가지로 묶기` 연결. root/entry 선택은 한국어 진단으로 거부.
- id/version/설명/태그/profile 입력과 선택/자동 dependency/public API/files/hash/origin 미리보기 제공.
- 확인 전 publish 없음. 미리보기 뒤 source hash가 바뀌면 발행 거부.
- 확인 시 WASM artifact 생성·검증과 WASM immutable publish를 거쳐 browser local store에 저장.
- 임의 이름의 새 물리 프로젝트에서 `lib/힘.ddn`을 `나만의힘@1.0.0`으로 발행한 실제 Playwright PASS; cancel 무변경 확인.

## G8

- 실제 local gotgan store를 WASM으로 검색하는 가지 선반 추가. 이름/설명/태그/공개 심볼 검색과 표준/나눔/내 profile 필터 제공.
- 선택 시 version/profile/hash/dependency/origin과 vendor/project graph/lock 변화 미리보기.
- 깨끗한 빈 프로젝트에서 import를 먼저 작성하고 `나만의힘` 설치 → vendor/root alias/lock 적용 → 실제 DDN `쓰임` 실행 Playwright PASS.
- Python durable server의 실제 view capability로 다시 열어 설치 버튼 disabled 및 `E_GAJI_VIEW_CAPABILITY_WRITE` 확인.
- 제목 문자열/주석의 `프로젝트`를 root block으로 오인하던 기존 검사기를 lexer token 구조 검사로 수리하고 direct regression PASS.
- WASM freshness PASS.

## G9

- 설치 artifact metadata를 vendor에 보존하고 Rust lifecycle update가 V1→V2 파일/API/의존성/risk diff를 산출하도록 구현.
- 같은 가지 id 갱신은 root bytes를 보존하며, local gotgan에 남은 V1 artifact로 되돌리면 V1 lock/package/runtime state hash가 재현됨.
- 편집으로 기존 lock이 stale해져도 현재 graph에서 새 lock을 계산하되, 명시 expected lock은 embedded lock hash와 검증.
- 제거는 alias뿐 아니라 실제 vendor import path 참조도 찾아 파일 경로가 든 `E_GAJI_REMOVE_REFERENCED`로 거부하고, 참조 제거 뒤 vendor/alias/마지막 lock을 원자 정리.
- Workbench 가지 선반에 install/update/rollback 자동 판별, 파일/API/의존성/risk diff, 제거 버튼과 capability write 경계를 연결.
- Rust lifecycle 3 tests, CLI/WASM parity, WASM freshness, 실제 Playwright V1 설치→V2 갱신→V1 되돌리기→참조 제거 거부→미사용 제거 PASS.

## G10

- extraction request와 artifact provenance에 검증된 `origin_gaji`/`relation=remix` 경계를 연결하고 origin 없는 remix를 거부.
- 설치된 가지에서만 `내 버전 만들기`를 열어 원본 bytes를 별도 편집본으로 복사하고 새 id/version으로 immutable local publish.
- 발행 결과에 원본/리믹스 content hash, 공개 API, `id@version · remix` 계보를 표시하며 원본 package hash 불변 확인.
- 실제 Playwright에서 설치 V1을 달 중력 값으로 수정해 `나만의힘-달@1.0.0` 발행, 제3의 깨끗한 프로젝트에 설치·실행 PASS.
- Rust remix lineage positive/negative test, CLI/WASM parity, WASM freshness PASS.

## G11

- 가지 선반에 선택 artifact `.gaji.detjson` 내보내기와 파일 가져오기를 추가하고, import는 기존 Rust/WASM immutable publish verifier를 반드시 통과.
- 리믹스 소비 프로젝트의 portable export에 vendor bytes, artifact metadata, lock을 포함해 깨끗한 browser context에서 import·실행.
- local gotgan이 비어 있는 clean context에서 artifact import 후 portable project import가 원 실행 state hash를 재현.
- durable save/view 뒤 server를 같은 data dir로 재시작해 embedded remix bytes/lineage 보존 확인.
- view capability write 거부, view→clone independent edit 전환, 기존 native durable vertical 회귀 PASS.

## G12

- parity runner를 설치된 물리 가지의 실제 `project-run`까지 확장해 V1/V2/rollback 각각 CLI/WASM canonical summary equality 확인.
- V2 공개 관찰값이 V1과 달라지고 rollback output/runtime state hash가 V1을 재현.
- Workbench 실제 물리 가지 발행·새 프로젝트 설치·V2 갱신·V1 rollback browser 수직은 G7~G10 통합 runner로 PASS.
- physics change storyboard browser에서 gravity DDN 변경 전/후 canvas pixel hash `0eb2c9b4 → 4f0b75d9` 차이와 durable view link 확인.

## G13

- 물리와 구조가 다른 `lib/grid.ddn` 단일 규칙 모듈을 임의 id `격자규칙`으로 추출·발행·새 소비자 설치.
- 원본 관찰값 `3`, remix `격자규칙-내버전` 관찰값 `5`를 실제 project-run으로 확인하고 원본 package 불변/lineage/content hash 차이 검증.
- remix 참조 중 제거는 `app/main.ddn` 위치와 함께 거부되고, 참조 제거 뒤 vendor와 마지막 lock 원자 정리.
- 같은 generic WASM extraction/artifact/store/lifecycle/run 함수만 사용해 물리 id/name 하드코딩 분기 없이 PASS.
- grid bogae browser DOM smoke, cell-grid primitive, Nurimaker grid render smoke PASS.

## G14

- artifact verifier에 256 files, 1 MiB single file, 8 MiB total, 256 KiB manifest 상한과 case-fold/NFC duplicate path, manifest content hash 검증 추가.
- 기존 project boundary matrix 30 cases로 traversal/absolute/drive/symlink/Unicode·case collision/file bounds/cycle/private export/lock/capability/revision negative controls PASS.
- artifact path/hash/size direct attack tests와 stale source/lock, immutable overwrite, 참조 제거 atomicity, CLI/WASM mismatch negative controls PASS.
- 실패 진단에 주입한 capability secret와 host repository absolute path가 포함되지 않음을 WASM runner에서 확인.
- 이 Windows/Node/WASM 환경 실측: local index 105개 검색 30회 p50 4.1453 ms, p95 4.8599 ms, max 5.0959 ms; 20개 순차 install p50 13.8503 ms, p95 38.1562 ms, max 40.7727 ms.
- 20개 설치에서 기존 한 줄 alias serialization이 하나만 파싱되던 결함을 줄 단위 canonical root block으로 수정하고 graph alias 20개 확인.

## G15

- 통합 browser runner가 `GAJI_VIEWPORT`를 받아 `1440x900`, `1024x768`, `778x912`, `390x844`에서 같은 실제 창작자 순환을 수행하도록 확장.
- 각 실행에서 source editor, native project file list, bogae canvas가 0x0이 아님을 직접 bounding box로 확인.
- 새 프로젝트→수정·실행→가지 묶기/발행→깨끗한 설치→V2 갱신→rollback→remix→다른 프로젝트 설치→save/view/clone→artifact/portable export→server restart→clean context import/replay 전체 PASS.
- 네 viewport 각각 3회, 총 12회 독립 실행 모두 PASS; 회차 경과시간 18.747~19.713초, 각 runner 소유 server/browser/temp lifecycle 정상 종료.

## G16

- machine-readable G0~G16 aggregate, 구현 보고서, 독립 검토 요청, 외부 창작자 Round 0 과제 3개 작성.
- native multifile authoring full promotion, approved Workbench quality, portable roundtrip, view-only invariant PASS.
- CLI/WASM freshness, true parity equality, sync gate 전 단계 PASS; lang 251/251, tool library 304/304 PASS.
- 기존 별도 실패를 숨기지 않음: core Fixed64 lint `from_f64_lossy(f64)`, tool AI prompt golden/현재 SSOT 불일치, legacy one-file fixed-id public wedge.
- 닫힘-동작 G0~G15, 닫힘-문서 G16 보고/파일럿/검토 요청, 외부 창작자 성공 수 0, `docs/ssot/**` 변경 0.
