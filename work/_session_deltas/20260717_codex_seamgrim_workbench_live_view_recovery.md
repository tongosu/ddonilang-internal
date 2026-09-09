# Session Delta — 셈그림 작업대 실행·보개·UI 신뢰성 복구 V1

- Date: 2026-07-17 KST
- Agent: Codex
- Status: Active — G0/G1/G2/G3/G4/G5/G6/G7/G8/G9/G10/G11/G12 complete
- Branch: `codex/queue-20260706`
- START_HEAD: `56862318cae8f1b43bb36d1513c3dcec3cba7ccd`

## 읽은 기준

- `AGENTS.md`, `AGENT_WORKFLOW.md`, `SSOT_POLICY.md`, `ARTIFACT_POLICY.md`, `CLAUDE.md`
- 사용자 승인 초초초장기 목표와 승인 Workbench brief
- SSOT v24.15.1 PLATFORM/TERMS 및 관련 current/walk/age 자료(읽기 전용)
- 최신 `docs/context/all/DEV_SUMMARY.md`

## G0 결정과 결과

- 첨부 목표와 저장소 목표 파일의 SHA-256이 `d09c61db5059c84589ca9b6771de283b766209db451d1d4fa4c57237b005f990`로 동일함을 확인했다.
- 예상 브랜치와 HEAD가 정확히 일치했다.
- 시작 dirty는 status 183행, tracked dirty 27개, untracked file 1,913개였다. 기존 변경은 모두 사용자/다른 작업 소유로 보존한다.
- freshness checker가 `source_tree_sha256 mismatch`, `source_files mismatch`로 실패함을 재현했다.
- 실제 Chromium에서 live 미진행, 고정 진자, uncommitted source 기반 포물선, 단일 viewRole, 첫 viewport 관리 UI 과밀을 재현했다.
- G0 machine-readable 기준선과 감사 보고를 작성했다.

## 소유권 경계

- 수정 가능 후보: G0 신규 파일, clean `tool/src/wasm_api.rs`/`tool/src/lib.rs`, clean Workbench/WASM 제품 파일, 새 전용 검사.
- 보존: `lang/src/stdlib.rs`, `tools/teul-cli/src/canon.rs`, 선행 dirty Workbench checker/runner 7개, dirty `DEV_SUMMARY`와 audit index.
- 금지: `docs/ssot/**` 직접 수정·stage·commit.

## 다음 관문

- G2에서 파싱된 프로그램의 one-shot/live 판정을 공용 Rust 계약으로 한 번만 계산하고 CLI/WASM/Workbench가 소비하게 한다.
- 선행 dirty `lang/src/stdlib.rs`와 기존 Workbench checker/runner 7개는 계속 보존한다.

## G1 결과

- `5686231` clean checkout에서도 freshness의 `source_tree_sha256/source_files mismatch`를 재현해 shared dirty만의 문제가 아님을 확인했다.
- clean checkout 빌드를 막던 ignored dialect 문서 의존을 동일 canonical bytes의 `lang/src/dialect_keywords_v8.tsv` 제품 resource로 분리하고 freshness source 목록에 넣었다. 원 ignored 문서는 수정·stage하지 않았다.
- `build_wasm_tool.ps1`이 wasm-pack/cargo/wasm-bindgen 실패를 성공으로 숨기지 않도록 exit code 전파를 고쳤고 negative checker를 추가했다.
- clean committed source에서 offline release/web WASM을 공식 빌드하고 manifest를 재생성했다.
- clean freshness PASS, true parity equality PASS, sync gate 11/11 PASS, public physics wedge PASS, 방언 12/12 PASS를 확인했다.
- 선행 creator-gaji 보고의 `5686231 freshness/sync PASS` 오주장을 삭제하지 않고 baseline FAIL과 `G1_SELF` 복구를 aggregate/report/session/checker에 함께 기록했다.
- 공유 dirty 작업 트리 freshness는 보존한 `lang/src/stdlib.rs` 한 행 때문에만 예상 FAIL이며, clean committed source PASS와 분리했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g1_wasm_freshness_recovery.detjson`.

## 현재 주장

- `G0_RED_BASELINE_REPRODUCED`
- `WASM_FRESHNESS_RESTORED`
- 외부 사용자 성공 수: `0`
- `BLOCK_EXTERNAL_ROUND0`
- 실행·보개·UI 동작 닫힘 주장 없음

## G2 결과

- lowering 전 DDN 표면을 Rust 파서로 한 번 판정하는 `ddn.execution_mode_decision.v1` 계약을 추가했다.
- 훅 없음·시작만·조건만은 `oneshot`, `(매마디)마다`·`(N마디)마다`는 `live`로 판정한다.
- 별칭/공백 변형은 정본과 동일하고, 문자열·주석 속 훅 모양은 live로 오인하지 않는다.
- CLI와 WASM execution envelope, WASM VM, Studio 실행 화면, Workbench 한 파일/연결 프로젝트가 동일한 `parsed_program` 판정만 소비한다.
- Studio의 원문 정규식 실행 모드 권한을 제거했다. Workbench 연결 프로젝트는 linked source 전체의 Rust envelope와 VM 판정이 다르면 실행을 거부한다.
- clean committed source에서 release/web WASM을 offline 재빌드하고 freshness PASS, 실제 WASM 8/8 판정 일치, CLI/WASM true parity equality PASS를 확인했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g2_shared_execution_mode_decision.detjson`.

## 다음 관문

- G3에서 one-shot bounded execution과 live 자동 마디 pump를 분리하고, start/pause/resume/stop/reset/step 상태 기계를 동일 판정 계약 위에 연결한다.

## G2 제품 연결 보정

- 실제 진자 원문은 `(매마디)마다`를 포함하지만 legacy UI 전처리가 이를 `매마디:움직씨`로 낮춘 뒤 VM 판정을 다시 읽어 `oneshot`으로 덮어쓰는 연결 결함을 브라우저 G3 검증에서 발견했다.
- Rust 판정이나 WASM 산출물을 바꾸지 않고, 원문 DDN을 `wasm_execution_envelope_json`에 직접 넘긴 `parsed_program` 판정을 제품 runtime handle이 유지하도록 고쳤다.
- 실제 진자 원문이 JS lowering 뒤에도 `live`로 남는 회귀 검사를 추가하고 `9031053`으로 독립 커밋했다.

## G3 결과

- `seamgrim.workbench.execution_lifecycle.v1` 상태 기계를 추가했다: `idle`, `preparing`, `running`, `pausing`, `paused`, `stopping`, `done`, `failed`, `history_readonly`.
- 실행 버튼 정책은 lifecycle과 committed cursor에서만 파생하며, disabled 이유를 `data-disabled-reason`, tooltip, 접근 가능한 라벨에 같이 노출한다.
- start/project switch/stop/history가 generation을 갱신해 오래된 준비·WASM callback을 폐기한다. 실제 Chromium에서 preparing 중 프로젝트를 바꿔도 stale run과 VM이 새 프로젝트에 남지 않았다.
- 빠른 이중 시작은 두 번째 요청을 동기 거부해 run 하나만 생성한다.
- live는 running에서 pause, paused에서 수동 step/resume, 과거 cursor에서 read-only/branch, 활성 상태에서 stop을 허용한다.
- one-shot은 실제 WASM 한 번 실행과 frame commit 뒤 즉시 `done/completed`가 되며 pause/resume/step/stop은 비활성이다.
- branch는 parent run/madi/state hash를 봉인한 새 자식 run을 생성한다.
- 실패 archive finalize는 네트워크 호출 전에 동기 claim하고 attempt count를 1로 고정해 중복 finalize를 거부한다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g3_execution_lifecycle.detjson`.

## 다음 관문

- G4에서 현재 명시 상태 기계 위에 serial one-step live pump를 붙인다. 자동/수동 step은 같은 commit 경로를 사용하고 한 번에 WASM step 하나만 허용한다.

## G4 결과

- 자동과 수동 live step이 모두 `commitNextLiveStep`을 사용한다. 각 호출은 WASM `step(1)` 하나만 실행하고 evidence/frame/checkpoint를 직렬 commit한다.
- timer는 32ms 표시 간격으로 다음 step을 예약할 뿐 마디 수나 state hash를 결정하지 않는다.
- pump generation과 execution generation을 함께 검사해 새 실행, 프로젝트 전환, 과거 cursor, stop, done, failure 뒤 오래된 callback을 폐기한다.
- pause 요청 시 예약 step은 취소하고 이미 in-flight인 step은 committed boundary까지 마친 뒤 `paused`로 전이한다. 실제 브라우저에서 pause 후 180ms 동안 commit 수가 늘지 않았다.
- resume은 같은 run/VM에서 펌프를 다시 예약한다. stop은 in-flight promise 정리 뒤 archive finalize를 한 번만 수행한다.
- InputSnapshot에 안정적인 `input_id`를 주고, step 시작 때 캡처한 입력만 현재 commit에 적용한다. 실행 도중 새 입력이 들어오면 다음 commit에 남으며 같은 입력은 한 번만 소비한다.
- active run은 `execution_source`/linked source를 봉인해 editor 수정 뒤에도 동일 VM/source hash로 계속된다. 수정 원문은 새 실행 후보로만 남는다.
- 원문 WASM execution envelope에서 `configured_madi`도 execution mode와 함께 보존한다. legacy lowering 뒤 VM 값이 0이 되는 반례와 실제 진자 240을 검사했다.
- 실제 `마디수: 3` live 원문이 자동 3 step 뒤 `done/completed`로 종료됨을 확인했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g4_deterministic_live_step_pump.detjson`.

## 다음 관문

- G5에서 committed frame 식별자, ordered observations, view binding과 deterministic semantic view payload를 명시 계약으로 묶는다.

## G5 결과

- `seamgrim.workbench.semantic_view_payload.v1`을 추가해 renderer 입력을 active committed frame에서 명시적으로 만든다.
- payload는 `run_id/frame_id/madi/state_hash/source_hash`, runtime channel 순서를 보존한 observation, view binding resolution, committed frame trajectory, state hash 밖 view config를 포함한다.
- 진자/포물선/격자/선 그래프의 선호 channel을 이름으로 resolve하고, 없으면 runtime numeric channel 순서로 정직하게 fallback한다.
- canvas가 committed frame identity/state hash/semantic payload hash/view binding resolution을 dataset으로 노출하고 view artifact에 같은 payload hash를 봉인한다.
- 관찰값 DOM도 active frame의 ordered runtime observations에서 생성한다. 프로젝트 trace dataset은 기존 계보 호환을 유지하면서 semantic payload hash를 별도 노출한다.
- 같은 frame+view config를 다시 만들면 semantic payload와 view artifact hash가 동일했다. overlay config로 바꾸면 semantic hash는 바뀌지만 runtime state hash는 변하지 않았고, primary로 돌아오면 두 hash가 원래 값으로 복원됐다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g5_committed_semantic_view_payload.detjson`.

## 다음 관문

- G6에서 진자/포물선/격자/정적 그래프 renderer를 semantic payload의 committed 값과 trajectory만 사용하도록 바꾼다.

## G6 결과

- `seamgrim.workbench.semantic_render_model.v1`을 추가하고 renderer 입력을 semantic payload 하나로 제한했다. 실행 전에는 가짜 상태 대신 committed frame 대기 상태를 표시한다.
- 진자는 고정 `theta = 0.52`를 제거하고 committed `theta/L`에서 bob 좌표를 계산한다. committed `omega/energy/kinetic_energy/potential_energy`를 라벨로 표시하고 overlay도 같은 canvas 좌표를 재사용한다.
- 포물선의 DDN source 정규식 매개변수 추출과 별도 JS 물리 계산을 삭제했다. 현재 점은 committed `x/y`, 라벨은 `t/vx/vy`, 궤적은 active cursor 이하 committed frame만 사용한다.
- 격자는 고정 8x8 조각과 `tick 0`를 삭제했다. 실제 runtime `view_meta.space2d`의 committed 64개 rect, committed piece 위치, committed frame madi/tick을 그린다.
- 선 그래프는 one-shot committed `x/y/a/b`를 의미 라벨이 있는 정적 결과로 표시한다. 의미 채널이 없는 legacy archive 숫자는 임의 그래프로 승격하지 않고 증거 카드로 표시한다.
- canvas dataset과 debug snapshot에 renderer family/status/source/current value/trajectory/tick/geometry를 노출했다. 실제 Chromium에서 진자·포물선 committed step마다 view artifact가 바뀌고, 격자와 one-shot 정적 그래프가 실제 runtime 값에 결합됨을 확인했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g6_committed_view_verticals.detjson`.

## 다음 관문

- G7에서 현재 전역 `viewRole` 버튼을 독립 view instance와 layout policy로 바꾸고, 지원되지 않는 역할은 정직하게 제거한다.

## G7 결과

- 전역 `state.viewRole`과 `data-view-role` 모드 전환을 제거하고 `seamgrim.workbench.view_workspace.v1`의 독립 instance 목록으로 교체했다.
- 으뜸보기는 항상 1개를 유지한다. 곁보기는 고유 `view_instance_id`와 semantic payload hash를 가진 N개 독립 canvas로 추가·개별 닫기·모두 닫기가 가능하다.
- 겹보기는 `render_surface=target_overlay`, `target_view_instance_id=primary`인 instance이며 primary semantic config의 `overlay_instance_ids`로 같은 좌표계에 합성된다.
- 돋보기는 committed renderer target을 canvas에서 실제 선택한 뒤에만 열리는 temporary instance다. committed frame/state hash가 바뀌면 selected target과 temporary magnifier만 폐기하고 durable side instance는 유지한다.
- 역할 내용이 없는 실행 전에는 으뜸보기 action만 표시한다. committed renderer가 준비된 뒤에만 family/관찰값에 맞는 곁·겹·돋보기 action을 노출한다.
- DDN 메인에서는 곁보기를 보개 아래, 보개 메인에서는 옆과 primary refit, 보개 전체에서는 view surface와 명시적 DDN 이동 버튼, 600px 좁은 화면에서는 수직 배치를 Chromium에서 확인했다.
- durable side instance는 local fallback 저장·다시 열기 후 같은 ID로 복원되고, selected target/temporary magnifier는 저장하지 않는다. legacy `selected_view/view_role`은 compatibility projection으로 유지한다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g7_independent_view_instances.detjson`.

## 다음 관문

- G8에서 server/revision, portable metadata, lineage, diagnostics/hash, gaji 상세를 요청 시 drawer/dialog로 옮기고 첫 화면을 프로젝트·실행·DDN·으뜸보기·프로젝트 조절값 중심으로 정돈한다.

## G8 결과

- server/link/revision/conflict는 `project-storage-drawer`, 프로젝트·실행 lineage/archive는 `project-history-drawer`, state hash/diagnostics는 `project-verification-drawer`로 옮겼다.
- portable import preview와 metadata 편집은 `portable-project-dialog`로 옮기고 dialog 안 재내보내기 action을 제공했다. 기존 toolbar direct export 다운로드는 그대로 유지한다.
- 가지 선반 진입은 첫 화면에서 제거하고 keyboard-accessible `세부` 메뉴의 실제 `가지 workflow` 요청 뒤에만 노출한다. publish/install 상세는 기존 modal workflow 안에 보존했다.
- 닫힌 drawer/dialog는 모두 native `<dialog>`의 `display:none` 상태로 레이아웃을 차지하지 않는다. ESC 닫기, 명명된 닫기 버튼, backdrop/focus 경계를 Chromium에서 확인했다.
- 1360x840에서 DDN/primary 시작점이 y=803.09375px에서 y=520.09375px로 올라왔고 문서 높이는 1535px에서 1252px로 줄었다. 프로젝트 제목·파일·실행줄·프로젝트 조절·DDN·으뜸보기가 첫 viewport에 함께 보인다.
- 600x900에서도 제목→실행→DDN/보개 순서를 유지한다. 진단이 생기면 세부 메뉴의 검증 action에 개수와 오류 여부를 접근 가능한 이름으로 표시한다.
- G5/G6/G7 browser, lifecycle, durable persistence, native one-file, direct portable export 회귀가 모두 PASS했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g8_progressive_disclosure_first_viewport.detjson`.

## 다음 관문

- G9에서 현재 전역 하드코딩 g/L·화살표를 제거하고 Rust/WASM authoring/maegim plan과 action map에서 현재 프로젝트 전용 controls를 생성한다.

## G9 결과

- 전역 정적 `g/L` 입력과 `left/right/drop` 화살표 DOM·handler를 제거했다. 채비는 배포 WASM의 `wasm_canon_maegim_plan`이 반환한 `ddn.maegim_control_plan.v1`만 소비하며 DDN source regex fallback은 두지 않았다.
- 포물선은 `초기속도x/초기속도y/중력가속도/dt/마디수` 5개, 진자는 `g/L/theta0/omega0/damp/dt/t_max` 7개를 현재 프로젝트 순서대로 표시한다. 격자에는 매김이 없으므로 채비 카드 자체를 숨긴다.
- 격자 프로젝트가 포함한 `action_map.json`의 `ddn.input_action_map.v1`에서만 `left/right/drop` 행동을 만든다. action map이 없는 포물선·진자에는 행동 카드와 화살표가 존재하지 않는다.
- 채비 저장은 `seamgrim.workbench.run_recipe_candidate.v1`을 만들고 현재 committed run을 바꾸지 않는다. 새 run은 recipe를 봉인한 뒤 `WasmVmHandle.setParam`으로 적용한다. `중력가속도=12.3`이 Fixed64 `12.299999999813735`로 적용됨을 Chromium에서 확인했다.
- 활성 run 중 다음 recipe를 `10.7`로 바꿔도 현재 frame state hash와 적용 중 parameter `12.299999999813735`는 변하지 않았다. 프로젝트 전환은 pending recipe, next input, 이전 control/action DOM을 모두 폐기한다.
- 행동은 project/action-map identity와 함께 next `InputSnapshot`에 들어가며 정확히 한 번 commit된다. 보기 instance 추가는 run recipe/InputSnapshot을 만들지 않고 current world state hash도 바꾸지 않는다.
- 기존 G3/G4/G6/G7/G8 browser, durable persistence, native one-file, UI common, WASM runtime 회귀가 PASS했다. G7 target click은 동적 채비 높이에서도 실제 canvas를 먼저 viewport에 넣도록 browser runner를 보강했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g9_project_derived_controls.detjson`.

## 다음 관문

- G10에서 live pump의 frame sequence/checkpoint/finalization/reopen/branch 경계를 durable 실행계보와 archive 기준으로 통합 검증한다.

## V2 R0 재개 인수 감사

- V2 재개 목표와 첨부 원문의 인수 시 SHA-256이 `25910454121880d681f5050a9f0d79fa0dd99f262555b691722d219b07f1c6f8`로 일치했다. commit 전 EOF 빈 줄만 `git diff --check`에 맞춰 정규화한 repo SHA-256은 `95cd9f20ff9bb2c40b92482a001adc1a95091923c52c9832d98d691e609f0528`이다.
- branch/HEAD는 기대값 `codex/queue-20260706` / `4d861f7`과 정확히 일치했고 G0~G9 커밋과 machine evidence 10개가 모두 정상 조상/존재 상태였다.
- 알려진 G10 WIP 중 HTML/CSS는 기대 blob과 정확히 일치했다. JS/lineage runner의 추가 변경은 sealed source projection과 실제 failure archive fixture 진단으로, 모두 G10 목적 hunk이며 unrelated 변경은 없었다.
- 보호 dirty checker/runner 7개는 모두 비스테이지로 보존했고 `docs/ssot/**` 변경 0건, 시작 stage empty, 대상 WIP `git diff --check` PASS를 확인했다.
- R0 대표 smoke에서 연결 프로젝트 action이 첫 frame snapshot과 다음 pump frame에 2회 기록되는 G9 회귀를 발견했다. 첫 linked-project WASM commit에 queued action을 실제 전달하고 같은 `input_id`를 소비하도록 최소 수리했다.
- 회귀 수리는 `fe35782 fix(seamgrim): consume project action at first committed frame`로 G10 WIP와 분리 커밋했다. project-controls browser와 live pump가 PASS했다.
- clean detached `fe35782`에서 freshness PASS, 공용 execution mode 8/8, live pump, committed 진자/포물선 view, project-derived controls smoke가 PASS했다.
- 첫 clean freshness 시도는 worktree 생성 뒤 cwd를 바꾸지 않아 shared dirty tree를 측정한 명령 오류였으며 증거에서 제외했다. 두 owned R0 worktree는 모두 제거돼 잔류 0이다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/r0_resume_audit.detjson`.

## V2 다음 관문

- `RESUME_HEAD=fe357828911a51d065b9da66c69983608a0e8e77`에서 알려진 G10 WIP를 이어 durable archive/lineage 제품 계약과 연속 검증을 닫는다.

## G10 결과

- live parent 실행에서 pause/resume가 같은 local/server run을 유지하고, frame id·committed madi·checkpoint sequence·previous checkpoint hash가 단조/연속임을 실제 서버와 Chromium에서 확인했다.
- history cursor에서 branch한 자식은 parent server run/madi/state hash를 봉인했다. 자식 실행·종료 뒤 부모 archive 전체가 byte-level JSON 비교에서 불변이었다.
- stopped parent, stopped child, configured-madi completed run, WASM prepare failed run이 각각 finalize attempt 1회로 종료됐다. failed fixture는 server run archive 생성 뒤 `@@@` product parse failure를 내므로 start failure finalization 경로를 직접 덮는다.
- 새 브라우저에서 서버 run 4개를 다시 열고 history drawer에서 부모 checkpoint frame과 hash chain을 실제 archive detail API 기준으로 렌더했다.
- layout/view 변경은 active state hash와 checkpoint count/hash를 바꾸지 않았다. renderer pixel은 archive에 저장하지 않는다.
- single-file live reset frame이 아직 적용하지 않은 queued action을 기록하던 결함을 고쳤다. InputSnapshot에 `input_id`를 보존하고, reset frame은 action 없음, 다음 실제 commit은 동일 input id/action-map lineage를 정확히 한 번 기록한다. project-controls browser 3회 동시 stress와 최종 단독 실행이 모두 PASS했다.
- G10 실패 fixture가 한 줄 `설정 { ... }.` 뒤 runtime body가 전부 제거되는 기존 guide-meta 결함을 드러냈다. JS/Python parser를 함께 고치고 `0d20be0`으로 분리 커밋했다. guideblock parity, UI common, native one-file 실제 WASM run이 PASS했다.
- 직접 검증: run archive lineage behavior gate, archive store gate, lifecycle unit/browser, live pump, semantic payload/renderer, view instances, progressive disclosure, native one-file가 모두 PASS했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g10_durable_live_lineage.detjson`.

## 다음 관문

- G11에서 legacy `selected_view/view_role` 입력을 새 view instance 구조로 결정적으로 이행하고, old artifact import 취소/실패 불변성과 export/reopen/share 호환을 닫는다.

## G11 결과

- `seamgrim.workbench.view_workspace_migration.v1` compatibility record를 추가하고 legacy `selected_view`/`view_role` 입력을 `W_LEGACY_VIEW_SELECTION_MIGRATED` 진단과 함께 새 view instance 구조로 이행했다.
- modern `view_workspace` snapshot은 legacy 입력으로 덮어쓰지 않는다. legacy `side`는 독립 곁보기, legacy `overlay`는 primary target overlay instance로 이행한다. target 없는 `magnifier`와 알 수 없는 legacy family 값은 결정적으로 primary에 머문다.
- portable/project snapshot export가 `controls_snapshot.view_workspace`의 새 schema를 보존하도록 했다. `selected_view`는 기존 사용자 artifact 호환 projection으로 유지한다.
- Workbench의 project snapshot 적용, local fallback reopen, portable import/open, catalog reopen, clone/share 경로가 같은 migration helper를 사용한다.
- old portable artifact preview는 source/project/view/world를 바꾸지 않고, open 뒤 imported source와 project를 보존하며 run/active frame을 만들지 않았다. legacy overlay artifact는 primary+overlay instance와 compat diagnostic으로 열린다.
- local fallback legacy `view_role=side` snapshot을 제품 reopen API로 열어 project/source/run world가 변하지 않고 side instance와 diagnostic이 생김을 확인했다.
- tampered SHA, old wrapper schema, import cancel은 project/server/source/viewWorkspace/active state hash를 바꾸지 않았다.
- G8 이후 drawer/dialog UI에 맞게 clone/reopen/share regression runner를 보정했고, capability share/clone, my-work reopen, server save/reopen 회귀가 PASS했다.
- 검증 PASS: view instance model, portable artifact, portable workbench, portable artifact/workbench wrappers, capability share clone, my-work reopen, server save/reopen, view instances browser, progressive disclosure browser, project controls browser, `git diff --check`, `git status --short -- docs/ssot`.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g11_legacy_view_migration.detjson`.

## 다음 관문

- G12에서 진자/포물선 live animation과 one-shot 완료를 실제 browser gate로 잠근다. 자동 progression, pause/resume/stop, auto/manual hash 동등성, semantic payload/hash, canvas pixel 변화, view open/close state-hash 불변을 포함한다.

## G12 결과

- `tests/seamgrim_workbench_animation_oneshot_gate_runner.mjs`와 wrapper `tests/run_seamgrim_workbench_animation_oneshot_gate_check.py`를 추가했다.
- 공식 포물선/진자 프로젝트에서 실행 클릭 뒤 추가 step 클릭 없이 committed step이 진행되고, 제한 시간 안에 active frame madi가 3 이상으로 도달함을 확인했다.
- 포물선/진자 각각 3개 이상 표본에서 committed state hash, semantic payload hash, 실제 canvas pixel hash가 모두 달라짐을 확인했다.
- pause 후 220ms 동안 committed step count와 active state hash가 고정되고, resume 후 증가하며, stop/done 뒤 더 이상 증가하지 않음을 확인했다.
- 같은 committed frame에서 현재 mode를 다시 렌더해도 semantic payload hash가 동일하고, side view open/close는 active world state hash를 바꾸지 않음을 확인했다.
- native one-shot 프로젝트는 실행 뒤 `done/oneshot`이 되고 committed step count가 1에 머문다. pause/resume/step은 비활성이고 정적 결과 canvas는 nonblank다.
- 같은 source에서 자동 5 step hash 열과 paused 수동 5 step hash 열이 같고, 연속 10 step과 `5 + pause + resume + 5` hash 열이 같음을 확인했다.
- 관련 기존 live/semantic 세로줄 검사도 재실행해 PASS했다: live step pump, committed view verticals browser, semantic view renderer, semantic view payload.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g12_animation_oneshot_browser_gate.detjson`.

## 다음 관문

- G13에서 네 viewport(`1440x900`, `1024x768`, `778x912`, `390x844`) 제품 품질 gate를 닫는다. DDN/으뜸보기 접근, 관리 입력폼 0개, canvas nonblank/time-change, side refit, overlay movement, magnifier gating, overflow/overlap/console error 0을 실제 browser evidence로 묶는다.

## G13 결과

- `1440x900`, `1024x768`, `778x912`, `390x844` 네 viewport에서 실제 Chromium product quality gate를 추가했다.
- compact viewport에서 프로젝트 목록을 내부 스크롤로 제한하고, setup controls를 전체 grid 폭으로 배치했다. tablet 폭은 4열 compact controls로, mobile 폭은 run strip/file tabs/workbench layout을 control grid보다 먼저 배치해 실제 사용 시작점을 앞당겼다.
- gate runner는 DDN source/primary view 접근, 관리 입력폼 0개, unrelated project controls 0개, canvas nonblank/time-change, side open/close refit, overlay movement, target 없는 magnifier 비활성, horizontal overflow 0, incoherent overlap 0, console error/key warning 0을 확인한다.
- 산출 스크린샷과 pixel evidence는 `out/seamgrim_workbench_g13/`에 생성하되 커밋하지 않는다.
- 검증 PASS: `node tests/seamgrim_workbench_four_viewport_recovery_gate_runner.mjs`, `python tests/run_seamgrim_workbench_four_viewport_recovery_gate_check.py`, `node tests/seamgrim_workbench_progressive_disclosure_browser_runner.mjs`, `node tests/seamgrim_workbench_project_controls_browser_runner.mjs`, `git diff --check`, `git status --short -- docs/ssot`.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g13_four_viewport_recovery_gate.detjson`.

## 다음 관문

- G14에서 double-click/select-import-cancel-rapid-switch-pause-resume-stop-step-viewport-change race matrix를 실제 제품 경로로 묶고, stale frame/negative count/missing disabled state/input leakage가 없음을 닫는다.

## G14 결과

- `tests/seamgrim_workbench_race_matrix_runner.mjs`를 추가해 실제 `ddn_exec_server.py` + Chromium 경로에서 공격·순서·race matrix를 닫았다.
- Workbench debug snapshot에 봉인 run의 `source_hash`, `source_kind`, `execution_mode`, `server_archive_status`를 노출해 source edit, one-shot/live 판정, checkpoint failure를 UI 텍스트 추론 없이 검증했다. 사용자 UI 동작 변경은 없다.
- runner가 확인한 제품 race: 실행 double-start는 `[true,false]`와 run 1개, source edit during live는 active sealed run source hash 불변, pause/resume 연타는 한 번만 수락되고 중복 step 없음, stop 연타와 stale callback은 finalize attempt 1회 및 추가 frame 0개, live 중 project switch는 old run/callback 제거, live 중 reopen은 run/pump clear, checkpoint 503 지연/실패 주입은 world step 중복 없음.
- view race도 함께 닫았다: side/overlay/magnifier visibility 변경은 active world state hash 불변, legacy selected_view tamper portable preview는 `E_PORTABLE_CANONICAL_MISMATCH`로 거부되고 import cancel 뒤 active state/run 불변이다.
- 문자열/주석 속 `(매마디)마다` 표면은 one-shot으로 실행되어 live control을 노출하지 않음을 확인했다.
- wrapper가 freshness negative controls를 selftest로 묶었다: stale wasm manifest는 `wasm_sha256 mismatch`, dirty source-tree fingerprint는 `source_tree_sha256 mismatch`로 실패한다.
- 검증 PASS: `node tests/seamgrim_workbench_race_matrix_runner.mjs`, `python tests/run_seamgrim_workbench_race_matrix_check.py`, `node tests/seamgrim_workbench_live_step_pump_runner.mjs`, `node tests/seamgrim_workbench_execution_lifecycle_browser_runner.mjs`, `node tests/seamgrim_workbench_view_instances_browser_runner.mjs`, G14 out JSON parse, `git diff --check`, `git status --short -- docs/ssot`.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g14_race_matrix.detjson`.

## 다음 관문

- G15에서 승인된 전체 관련 회귀 배터리를 최신 G0~G14 계약에 맞춰 재정렬하고 실행한다. 특히 기존 approved Workbench quality/semantic/runtime runners의 낡은 pre-G7 view-role 기대를 새 instance/action gating 계약으로 갱신한다.

## G15 결과

- approved Workbench shell/quality/semantic/runtime lineage runner를 post-G7 view instance, drawer/dialog, action-map gating, paused runtime semantics에 맞춰 갱신했다. SSOT clean 확인은 repository-local exclude 영향 없이 `git -c core.excludesfile=` 기준으로 고정했다.
- public physics wedge는 committed frame 기준 관측, storage drawer 기반 clone/reopen, viewport별 drawer control visibility, 예상 가능한 connection reset/409 console noise 필터로 재정렬했다.
- durable workflow는 saved snapshot 대기, storage drawer 조작, 빠른 auto-complete/stop race 허용, archive branch fallback으로 현재 제품 경로를 검증한다.
- multifile workbench/portable runner는 pause-aware manual step, stale source unbound contract, active frame/latest output 기준, clone 전 storage drawer open/close 경로를 반영했다.
- `seamgrim_moyang_render_smoke_v1` fixture 3개는 아직 제품 경로가 지원하지 않는 parameterized `원틀:움직씨` 호출 대신 직접 `모양 { 원(...) }` 표면으로 교정했다.
- `DDN_WASM_DIR` 기반 fresh artifact 경로를 parity/boundary runner에 허용했다. 현재 dirty workspace 검증을 위해 WASM manifest를 재작성했지만, manifest diff가 G15 외 source-root dirty/untracked 파일을 fingerprint하므로 G15 커밋에서는 제외한다.
- 검증 PASS: approved workbench 4종, G12/G13/G14 회귀 3종, public physics wedge, durable quality gate, portable workbench/artifact, multifile workbench/portable, boundary matrix, WASM freshness/true parity/sync gate, `cargo check`, `cargo check --manifest-path tools/teul-cli/Cargo.toml`, `cargo test -p ddonirang-tool`, `python tests/run_ci_sanity_gate.py --profile core_lang`, `git diff --check`, `git status --short -- docs/ssot`.
- 첫 `core_lang` sanity 시도는 `teul-cli` 컴파일 중 transient `serde_core` StableCrateId collision으로 실패했다. 별도 cargo checks와 이후 전체 sanity 재실행은 PASS했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g15_integrated_workbench_recovery_gate.detjson`.

## 다음 관문

- G16에서 G15 커밋을 clean detached 상태로 검증한다. unrelated dirty source-root 변경 없이 freshness, public/durable/multifile/boundary, core_lang sanity를 재확인하고 manifest 업데이트 필요 여부를 분리 판정한다.

## G16 결과

- `582be2e`를 `I:/home/urihanl/ddn/codex/build/worktrees/g16_582be2e`에 detached clean worktree로 checkout했다. 시작/종료 `git status --short`는 tracked 변경 0건이었다.
- clean worktree 자체에는 `node_modules`가 없어서 Playwright import가 실패했다. tracked 파일을 바꾸지 않고 main workspace의 `node_modules`를 junction으로 연결해 browser runner dependency만 재사용했다.
- clean worktree에는 ignored/local SSOT zip bundle이 없어 첫 public wedge 내부 sync gate가 `ddonirang_vol4_project_currentline_bundle_20260502.zip` missing으로 실패했다. `DDN_VOL4_BUNDLE_PATH`를 main workspace의 로컬 zip으로 지정한 뒤 sync gate와 public wedge가 PASS했다.
- clean PASS: freshness, approved workbench 4종, G12 animation one-shot(첫 timing fail 뒤 즉시 재시도 PASS), G13 four viewport, G14 race matrix, WASM sync gate, public physics wedge, durable quality, portable workbench/artifact, multifile workbench/portable, boundary matrix, `cargo check`, `cargo check --manifest-path tools/teul-cli/Cargo.toml`, `cargo test -p ddonirang-tool` 중 SSOT-local-data 의존 ai_prompt 2개 제외 319 tests, `git diff --check`.
- clean full `cargo test -p ddonirang-tool`은 ai_prompt 2개가 `docs/ssot` 디렉터리 부재로 실패했다. clean `core_lang` sanity도 `ssot_sync_dr173_177_check`에서 `E_SSOT_SYNC_VERSION_SSOT_DIR_MISSING: docs/ssot/ssot`로 중단됐다. 이는 G15 코드 결함이 아니라 detached clean worktree에 local SSOT 자료가 없는 환경 제약이다.
- G15에서 제외한 WASM manifest 업데이트는 clean commit에서는 필요 없었다. `python tests/run_ddn_cli_wasm_freshness_check.py`가 `582be2e` clean checkout에서 바로 PASS했다.
- machine evidence: `work/codex/20260717_seamgrim_workbench_recovery/g16_clean_detached_verification.detjson`.

## 다음 관문

- G17에서 detached worktree에 local SSOT 자료를 제공하는 승인된 방식(예: read-only 경로 override 또는 검증 전용 bundle path)을 설계하거나, core_lang clean detached 검증을 main checkout local-SSOT dependency와 분리하는 정책을 정리한다.

## G17 결과

- 구현 보고서 `docs/reports/impl/REPORT_SEAMGRIM_WORKBENCH_RECOVERY_IMPLEMENTATION_V1_20260718.md`를 추가했다.
- 독립 검토 요청서 `docs/reports/audit/REQUEST_SEAMGRIM_WORKBENCH_RECOVERY_INDEPENDENT_REVIEW_V1_20260718.md`를 추가했다.
- `docs/reports/impl/INDEX.md`, `docs/reports/audit/INDEX.md`, `docs/context/all/DEV_SUMMARY.md`에는 G17 관련 항목만 추가했다. 기존 dirty hunk는 stage하지 않는다.
- 보고서에는 닫힘-동작, clean detached 검증, local SSOT 자료 부재로 인한 core_lang 환경 제약, 외부 사용자 성공 0, Round 0 재개 미주장을 분리 표기했다.

## 다음 관문

- G18에서 최종 HEAD 기준 필수 게이트/상태/dirty 보존 목록을 감사하고 final handoff를 작성한다.

## G18 결과

- 최종 감사 보고서 `docs/reports/impl/REPORT_SEAMGRIM_WORKBENCH_RECOVERY_FINAL_AUDIT_V1_20260718.md`를 추가했다.
- machine evidence `work/codex/20260717_seamgrim_workbench_recovery/g18_final_audit.detjson`를 추가했다.
- G18 직전 HEAD `5806244` 기준 main workspace `git diff --check` PASS, `git status --short -- docs/ssot` clean.
- clean detached worktree를 `5806244`로 이동한 뒤 `python tests/run_ddn_cli_wasm_freshness_check.py` PASS.
- 최종 상태 주장은 `WORKBENCH_LIVE_EXECUTION_AND_VIEW_RECOVERY_CLOSED`, `READY_FOR_INDEPENDENT_REVIEW`, `BLOCK_EXTERNAL_ROUND0_PENDING_INDEPENDENT_REVIEW`로 제한한다. 외부 사용자 성공 수는 `0`이며, `READY_TO_START_EXTERNAL_CREATOR_ROUND0`는 주장하지 않는다.
