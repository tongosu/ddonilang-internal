#!/usr/bin/env python3
"""Generate the Wave-0 DDN V1 product-closure census artifacts.

This is a management/evidence generator.  It does not edit SSOT, public SPEC,
or product sources.  The generated registry deliberately distinguishes the
Owner product-roadmap input from the still-empty authoritative SSOT V1
membership table.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/codex/20260827_ddn_v1_product_closure_long_range_r1"

SSOT_VERSION = "v25.15.0"
SSOT_ALL_SHA256 = "b51fc82e5b922b14e10e48e733f0398d85f4d0b9cb22477ac10e08cef19e3777"
SSOT_MANIFEST_SHA256 = "f08a149b25520e708c8250a71e487d0fb420576a2e088202171dfdbf1e316ad4"
WORKSPACE_BUNDLE = "v24.35.1_20260813_gaji-resolution-lock-v1-candidate-r3"
WORKSPACE_MANIFEST_SHA256 = "97f6554c24d0b2a89aeb3190a5febdde4230498ebdc4156c643d8fd8a969ba9f"
PUBLIC_SPEC = "v0.5.0"
BASELINE = "daabc1188d164888d7c3280588c0dbb5328bb5b6"
PRODUCT_FIXED = "b8530bd6eadcf79658a821f4e9b4538991b89b80"

STATUS = {
    "implemented": "IMPLEMENTED_VERIFIED",
    "unverified": "IMPLEMENTED_UNVERIFIED",
    "partial": "PARTIAL",
    "planned": "PLANNED",
    "missing": "NOT_IMPLEMENTED",
    "na": "NOT_APPLICABLE",
    "unknown": "UNKNOWN",
}

AXES = [
    "lexer_status", "parser_status", "ast_status", "typed_ir_status",
    "typecheck_status", "canon_status", "formatter_status", "runtime_status",
    "tool_status", "teul_cli_status", "official_cli_status", "native_status",
    "wasm_status", "runtime_bridge_status", "workbench_status",
    "diagnostic_status", "migration_status", "pack_status", "conformance_status",
]

PROFILES = {
    "language_partial": {
        "lexer_status": STATUS["partial"], "parser_status": STATUS["partial"],
        "ast_status": STATUS["partial"], "typed_ir_status": STATUS["partial"],
        "typecheck_status": STATUS["partial"], "canon_status": STATUS["partial"],
        "formatter_status": STATUS["partial"], "runtime_status": STATUS["partial"],
        "tool_status": STATUS["partial"], "teul_cli_status": STATUS["partial"],
        "official_cli_status": STATUS["partial"], "native_status": STATUS["partial"],
        "wasm_status": STATUS["partial"], "runtime_bridge_status": STATUS["partial"],
        "workbench_status": STATUS["partial"], "diagnostic_status": STATUS["partial"],
        "migration_status": STATUS["partial"], "pack_status": STATUS["partial"],
        "conformance_status": STATUS["partial"],
    },
    "runtime_partial": {
        **{axis: STATUS["na"] for axis in AXES},
        "typed_ir_status": STATUS["partial"], "runtime_status": STATUS["partial"],
        "tool_status": STATUS["partial"], "teul_cli_status": STATUS["partial"],
        "official_cli_status": STATUS["partial"], "native_status": STATUS["partial"],
        "wasm_status": STATUS["partial"], "runtime_bridge_status": STATUS["partial"],
        "workbench_status": STATUS["partial"], "diagnostic_status": STATUS["partial"],
        "pack_status": STATUS["partial"], "conformance_status": STATUS["partial"],
    },
    "toolchain_partial": {
        **{axis: STATUS["na"] for axis in AXES},
        "runtime_status": STATUS["partial"], "tool_status": STATUS["partial"],
        "teul_cli_status": STATUS["partial"], "official_cli_status": STATUS["partial"],
        "native_status": STATUS["partial"], "wasm_status": STATUS["partial"],
        "runtime_bridge_status": STATUS["partial"], "workbench_status": STATUS["partial"],
        "diagnostic_status": STATUS["partial"], "pack_status": STATUS["partial"],
        "conformance_status": STATUS["partial"],
    },
    "product_partial": {
        **{axis: STATUS["na"] for axis in AXES},
        "runtime_status": STATUS["partial"], "tool_status": STATUS["partial"],
        "official_cli_status": STATUS["partial"], "native_status": STATUS["partial"],
        "wasm_status": STATUS["partial"], "runtime_bridge_status": STATUS["partial"],
        "workbench_status": STATUS["partial"], "diagnostic_status": STATUS["partial"],
        "migration_status": STATUS["partial"], "pack_status": STATUS["partial"],
        "conformance_status": STATUS["partial"],
    },
    "release_open": {
        **{axis: STATUS["na"] for axis in AXES},
        "tool_status": STATUS["planned"], "official_cli_status": STATUS["planned"],
        "native_status": STATUS["planned"], "wasm_status": STATUS["planned"],
        "workbench_status": STATUS["planned"], "diagnostic_status": STATUS["planned"],
        "pack_status": STATUS["planned"], "conformance_status": STATUS["planned"],
    },
    "future_partial": {
        **{axis: STATUS["na"] for axis in AXES},
        "parser_status": STATUS["partial"], "ast_status": STATUS["partial"],
        "typed_ir_status": STATUS["partial"], "runtime_status": STATUS["partial"],
        "tool_status": STATUS["partial"], "teul_cli_status": STATUS["partial"],
        "wasm_status": STATUS["partial"], "workbench_status": STATUS["partial"],
        "pack_status": STATUS["partial"], "conformance_status": STATUS["partial"],
    },
}


# id, Korean name, purpose, profile, roadmap membership, first, experimental,
# required, completion, dependencies, product status, evidence, risk, owner gate, notes
RAW = [
    ("V1-C001", "한국어 기본 원문 표면", "한국어 원문을 정규화·분석해 공통 의미 경로로 보낸다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", [], "PARTIAL", ["lang/src/lexer.rs", "lang/src/frontdoor.rs", "publish/spec/v0.5.0"], "HIGH", False, "Workbench strict JS 분석과 Rust V25 frontdoor가 아직 수렴하지 않았다."),
    ("V1-C002", "Definition `:=`", "새 definition identity를 만드는 이름 있는 정의 결속이다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C001", "V1-C004"], "IMPLEMENTED_UNVERIFIED", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-325", "lang/src/parser.rs", "b8530bd6eadcf79658a821f4e9b4538991b89b80"], "HIGH", False, "PC01 FU01 local evidence는 있으나 fresh plain PASS가 대기 중이다."),
    ("V1-C003", "Binding/Rebinding `<-`", "기존 결속과 persistent update의 최종 root를 다시 결속한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C001", "V1-C004"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-205", "lang/src/parser.rs", "work/codex/20260827_ddn_long_relint_product_01_completion/G14_PARITY_LIMITED_SCOPE_RESULT.md"], "HIGH", False, "native/WASM current rejection parity와 전체 Workbench 성공은 별개다."),
    ("V1-C004", "기본 값·자료형·정체성", "값·자료형·semantic identity를 문맥 간 같은 의미로 보존한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C001"], "PARTIAL", ["lang/src/ast.rs", "lang/src/model.rs", "tools/teul-cli/src/core/value.rs"], "HIGH", False, "lang/tool/teul의 중복 모델을 shared authority로 더 수렴해야 한다."),
    ("V1-C005", "정확수·결정적 수치", "플랫폼에 무관한 기본 수치 결과와 hash를 제공한다.", "runtime_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004"], "PARTIAL", ["core/src/fixed64.rs", "tool/src/fixed64_boundary.rs", "tools/teul-cli/src/core/fixed64.rs"], "MEDIUM", False, "복수 구현과 전체 public conformance가 남아 있다."),
    ("V1-C006", "글·바이트·NFC", "Unicode NFC와 글/바이트 identity를 명시적으로 분리한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C001", "V1-C004"], "PARTIAL", ["lang/src/normalizer.rs", "lang/src/lexer.rs"], "HIGH", False, "전체 frontdoor와 import/export byte custody 검증이 필요하다."),
    ("V1-C007", "Product", "이름 있는 product 구조와 field identity를 표현한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004"], "PARTIAL", ["lang/src/ast.rs", "ab16db245f7ff7234cc604923e527355f5b7d53a"], "MEDIUM", False, "field access scoped PASS를 Product 전체 closure로 확대하지 않는다."),
    ("V1-C008", "Sum·선택값·typed result", "합·선택·성공/실패를 typed value로 표현한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-251-RD-266", "lang/src/ast.rs"], "HIGH", False, "docs-first 의미와 physical product coverage를 분리한다."),
    ("V1-C009", "이름 있는 callable", "이름·pin·결과 자리를 가진 callable definition을 제공한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C002", "V1-C004"], "PARTIAL", ["lang/src/ast.rs", "lang/src/parser.rs", "docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-379-RD-384"], "HIGH", False, "ResultPlace와 generic callable 전체 제품 수직은 OPEN이다."),
    ("V1-C010", "익명 callable", "이름 없는 함수값과 결과식 슬롯을 typed 의미로 제공한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004", "V1-C009"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-379-RD-384", "lang/src/ast.rs"], "HIGH", False, "exact parser/runtime/Workbench product evidence가 부족하다."),
    ("V1-C011", "ResultPlace", "callable 결과가 놓이는 명시적 typed 위치를 결속한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C009", "V1-C008"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#Callable-ResultPlace-R1", "lang/src/ast.rs"], "HIGH", False, "docs-first live 의미이고 일반 block tail·generic return은 범위 밖이다."),
    ("V1-C012", "조건·반복", "조건 분기와 bounded 반복을 동일 runtime authority로 실행한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004"], "PARTIAL", ["lang/src/ast.rs", "tool/src/ddn_runtime.rs", "a633c43f93299c3ec60151857e6aeb54c1d852ae"], "MEDIUM", False, "ForEach/current-item scoped PASS는 보존하되 control-flow 전체 PASS로 확대하지 않는다."),
    ("V1-C013", "bounded recursion", "재귀 실행을 명시적인 누적 한도와 실패로 제한한다.", "runtime_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C009", "V1-C026"], "PARTIAL", ["tool/src/work_cost.rs", "docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-186"], "HIGH", False, "public standard profile과 전체 callable recursion 검증이 필요하다."),
    ("V1-C014", "기본 generic", "제한된 type parameter와 적용 타입을 typed IR에 보존한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C004", "V1-C009"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-232-RD-238", "lang/src/ast.rs"], "HIGH", False, "K1 일부만 PARTIAL이며 K0 이후 behavior closure가 필요하다."),
    ("V1-C015", "구실·골라부름", "typed role 요구와 overload/provider 선택을 fail-closed한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C014", "V1-C009"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-204", "tool/src/ddn_runtime.rs", "04893194c"], "HIGH", True, "stable public identity/wire는 OPEN이며 limited product evidence만 보존한다."),
    ("V1-C016", "기본 collection", "결정적 순서와 identity를 가진 기본 모음을 제공한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004"], "PARTIAL", ["lang/src/ast.rs", "tools/teul-cli/src/core/value.rs"], "MEDIUM", False, "collection family별 public conformance inventory가 필요하다."),
    ("V1-C017", "typed Selection", "index·field·slice 선택과 persistent replacement를 typed하게 구분한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C007", "V1-C016"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-251-RD-266", "lang/src/ast.rs"], "HIGH", False, "docs-first selection 의미와 executable oracle 사이 gap이 남아 있다."),
    ("V1-C018", "Basic Tensor R1", "ordered static shape tensor의 선택·slice·same-shape replacement를 제공한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C005", "V1-C016", "V1-C017"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-385-RD-399", "tools/teul-cli/src/cli/tensor.rs"], "HIGH", False, "executable oracle와 native/WASM/Workbench parity가 OPEN이다."),
    ("V1-C019", "한국어 활용형", "형태 변화가 같은 callable/field identity로 결정적으로 수렴한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C001", "V1-C009"], "PARTIAL", ["lang/src/dialect.rs", "lang/src/term_map.rs", "lang/src/surface.rs"], "HIGH", False, "형태 분석과 callable resolution의 단일 authority 수렴이 필요하다."),
    ("V1-C020", "닫힌 여러표면·canon", "허용된 복수 표면을 하나의 machine canon으로 수렴한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C001", "V1-C019"], "PARTIAL", ["lang/src/canonicalizer.rs", "lang/src/dialect.rs", "pack/dialect_builtin_equiv_v1"], "HIGH", False, "formatter와 teul canon 중복 authority가 남아 있다."),
    ("V1-C021", "모듈·여러 파일", "여러 DDN source를 project identity 아래 결정적으로 조립한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C001", "V1-C022"], "PARTIAL", ["tool/src/local_project.rs", "pack/ddn_local_project_graph_v1", "pack/ddn_local_project_workbench_multifile_v1"], "MEDIUM", False, "fresh public-source build와 Workbench current frontdoor를 함께 검증해야 한다."),
    ("V1-C022", "프로젝트 정체성", "project source·revision·policy identity를 저장·실행·재열기에 보존한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004"], "PARTIAL", ["tool/src/project_meta.rs", "tool/src/project_authoring.rs", "ddn.project.json"], "HIGH", False, "official server revision과 local fallback identity를 분리해야 한다."),
    ("V1-C023", "dependency identity", "dependency content와 resolution identity를 source 의미와 분리해 봉인한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C022"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-161", "pack/ddn_local_project_graph_v1"], "HIGH", False, "외부 resolver/public registry 없이 local 범위만 우선 닫는다."),
    ("V1-C024", "local dependency·lock", "로컬 의존 해소 결과를 lock 또는 동등 봉인으로 고정한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C023", "V1-C028"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-213", "docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-231", "pack/ddn_local_project_graph_v1"], "HIGH", True, "exact public lock schema와 외부 해소는 OPEN이다."),
    ("V1-C025", "기본 stdlib", "V1 필수 기본 연산을 shared typed authority로 제공한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C004", "V1-C009", "V1-C016"], "PARTIAL", ["lang/src/stdlib.rs", "tool/src/runtime_surface.rs"], "HIGH", False, "V1 membership이 비어 있어 stdlib 필수 목록도 아직 provisional이다."),
    ("V1-C026", "결정적 실행", "동일 봉인 입력을 동일 commit·관찰 순서로 실행한다.", "runtime_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C004", "V1-C005"], "PARTIAL", ["core/src/engine.rs", "lang/src/execution_mode.rs", "tool/src/ddn_runtime.rs"], "HIGH", False, "여러 scoped PASS가 있으나 V1 required closure gate는 미정이다."),
    ("V1-C027", "state/result hash", "committed state와 canonical result identity를 receipt에 결속한다.", "runtime_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C026"], "PARTIAL", ["tools/teul-cli/src/core/state.rs", "tool/src/ddn_runtime.rs", "tool/src/schema.rs"], "HIGH", False, "CLI/WASM/Workbench 전체 schema/wire가 stable하지 않다."),
    ("V1-C028", "receipt·replay", "실행 증표와 replay zero-call 경계를 봉인한다.", "runtime_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C027", "V1-C029"], "PARTIAL", ["tool/src/schema.rs", "tools/teul-cli/src/cli/replay.rs", "0e3de501fd5b95a47dba7ba67f2bb7f57583bbb3"], "HIGH", True, "RD-207 exact stable wire는 OPEN이다."),
    ("V1-C029", "외부 입력 sealing", "외부 입력을 기록·봉인하고 replay에서 provider 호출을 0으로 한다.", "runtime_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C026"], "PARTIAL", ["core/src/input.rs", "core/src/sam/input_snapshot.rs", "pack/age2_open_input_record_replay_v1"], "HIGH", False, "입력 source별 physical adapter conformance가 필요하다."),
    ("V1-C030", "silent semantic fallback 금지", "미지원·모호·손상 의미를 성공이나 다른 의미로 바꾸지 않는다.", "runtime_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "CONTINUOUS", ["V1-C001", "V1-C026"], "PARTIAL", ["lang/src/frontdoor.rs", "tool/src/source_analysis.rs", "work/codex/20260827_ddn_long_relint_product_01_completion/SECURITY_AND_PATH_PREFLIGHT.md"], "HIGH", False, "각 frontdoor별 mutation evidence를 계속 유지해야 한다."),
    ("V1-C031", "shared 언어·runtime authority", "parser·AST·runtime 의미 엔진을 한 shared Rust authority로 수렴한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C001", "V1-C026", "V1-C030"], "PARTIAL", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-189", "lang/src/frontdoor.rs", "tool/src/ddn_runtime.rs", "tools/teul-cli/src/lang/parser.rs"], "CRITICAL", False, "teul-cli와 Workbench JS의 독립 semantic authority가 남아 critical path다."),
    ("V1-C032", "official CLI", "공개 사용자가 의존할 하나의 native command frontdoor를 제공한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C031", "V1-C041"], "PARTIAL", ["tool/src/main.rs", "tools/teul-cli/src/main.rs", "work/codex/20260827_ddn_long_relint_product_01_completion/PUBLIC_SELF_CONTAINMENT_RESULT.md"], "CRITICAL", True, "tool과 teul-cli의 public identity/KEEP-MOVE-DROP가 미결정이다."),
    ("V1-C033", "Native adapter", "host filesystem/process와 language runtime 사이를 명시 capability로 연결한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C026", "V1-C029"], "PARTIAL", ["core/src/platform.rs", "tool/src/paths.rs", "tool/src/local_project.rs"], "HIGH", False, "host capability와 semantic state의 분리 conformance가 필요하다."),
    ("V1-C034", "WASM path", "native와 같은 Rust runtime을 browser-compatible artifact로 제공한다.", "toolchain_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C031", "V1-C027"], "PARTIAL", ["tool/src/wasm_api.rs", "scripts/build_wasm_tool.ps1", "b8530bd6eadcf79658a821f4e9b4538991b89b80"], "HIGH", False, "A/B/tracked identity는 slice 증거이며 전체 V1 WASM surface closure가 아니다."),
    ("V1-C035", "RuntimeBridge", "Workbench가 raw runtime을 재해석하지 않고 typed 실행 계약을 호출한다.", "product_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C034", "V1-C031"], "PARTIAL", ["367e231e", "solutions/seamgrim_ui_mvp/ui/workbench/execution_lifecycle.js", "solutions/seamgrim_ui_mvp/ui/workbench/workbench.js"], "CRITICAL", False, "T1 구조는 있으나 current V25 positive source가 shared strict analysis에서 실패한다."),
    ("V1-C036", "HostBridge", "저장·파일·capability session을 runtime 의미와 분리한다.", "product_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C033", "V1-C035"], "PARTIAL", ["9fecddbf", "solutions/seamgrim_ui_mvp/ui/workbench/persistence/capability_session.js", "solutions/seamgrim_ui_mvp/ui/workbench/persistence/project_adapter.js"], "HIGH", False, "official server API와 local fallback을 구분한 end-to-end gate가 필요하다."),
    ("V1-C037", "Common Workbench", "편집·실행·진단·보기·저장을 하나의 사용자 흐름으로 제공한다.", "product_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C035", "V1-C036", "V1-C038", "V1-C039"], "PARTIAL", ["solutions/seamgrim_ui_mvp/ui/workbench/workbench.js", "work/codex/20260827_ddn_long_relint_product_01_completion/WORKBENCH_EDGE_PRODUCT_RESULT.md"], "CRITICAL", True, "current runtime success와 exact server revision reopen이 OPEN이다."),
    ("V1-C038", "renderer-independent canonical view", "runtime 관찰을 renderer 독립 typed payload로 투영한다.", "product_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C027", "V1-C035"], "PARTIAL", ["solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_payload.js", "solutions/seamgrim_ui_mvp/ui/workbench/semantic_view_renderer.js", "905efb4a"], "HIGH", False, "T5 family scoped PASS를 current T5F grid successor로 확대하지 않는다."),
    ("V1-C039", "project save·reopen", "source·project·revision identity를 저장 후 재열기에 보존한다.", "product_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C022", "V1-C036"], "PARTIAL", ["solutions/seamgrim_ui_mvp/ui/workbench/persistence/local_gotgan_store.js", "solutions/seamgrim_ui_mvp/ui/workbench/persistence/project_adapter.js", "de9cb9ed"], "HIGH", False, "local fallback PASS와 official server revision closure를 분리한다."),
    ("V1-C040", "import·export 최소선", "versioned project/portable artifact를 원자적으로 가져오고 내보낸다.", "product_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.2", ["V1-C022", "V1-C024", "V1-C039"], "PARTIAL", ["solutions/seamgrim_ui_mvp/ui/workbench/persistence/portable_project_artifact.js", "solutions/seamgrim_ui_mvp/ui/workbench/persistence/project_adapter.js"], "HIGH", True, "stable public wire는 OPEN이고 current format은 experimental/versioned다."),
    ("V1-C041", "기본 diagnostics", "code·phase·span·expected/actual을 frontdoor와 UI까지 보존한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C001", "V1-C031"], "PARTIAL", ["lang/src/parser.rs", "tool/src/runtime_surface.rs", "work/codex/20260827_ddn_long_relint_product_01_completion/PC01_FU01_CLOSURE_OR_REVIEW_STATUS.md"], "HIGH", True, "stable diagnostic wire와 Workbench structured propagation 일부가 OPEN이다."),
    ("V1-C042", "pre-v25 migration", "옛 표면을 silent fallback 없이 정확한 migration 진단으로 거부·변환한다.", "language_partial", "REQUIRED", "V1.0", "V1.0", "V1.0", "V1.0", ["V1-C002", "V1-C003", "V1-C041"], "IMPLEMENTED_UNVERIFIED", ["lang/src/migration.rs", "lang/src/parser.rs", "b8530bd6eadcf79658a821f4e9b4538991b89b80"], "HIGH", False, "PC01와 G14 fresh independent verdict를 기다린다."),
    ("V1-C043", "public source projection", "clean sealed internal commit을 deterministic allowlist public tree로 투영한다.", "release_open", "REQUIRED", "V1.0", "V0.9", "V1.0", "V1.0", ["V1-C031"], "PARTIAL", ["c3c65ae2", "fab6315c", "work/codex/20260827_ddn_long_relint_product_01_completion/PUBLIC_PROJECTION_R2_RECEIPT.md"], "CRITICAL", False, "A/B tree 결정성은 확인됐지만 self-containment와 private path preflight가 FAIL이다."),
    ("V1-C044", "public-source-only release build", "public source만으로 release artifact를 재현한다.", "release_open", "REQUIRED", "V1.0", "V0.9", "V1.0", "V1.0", ["V1-C043", "V1-C032", "V1-C034"], "NOT_IMPLEMENTED", ["work/codex/20260827_ddn_long_relint_product_01_completion/PUBLIC_SELF_CONTAINMENT_RESULT.md"], "CRITICAL", False, "private include와 browser offline dependency 때문에 현재 FAIL이다."),
    ("V1-C045", "clean-machine install·run", "내부 경로 없이 새 환경에서 설치·예제 실행을 완료한다.", "release_open", "REQUIRED", "V1.0", "V0.9", "V1.0", "V1.0", ["V1-C044", "V1-C037"], "NOT_IMPLEMENTED", ["work/codex/20260827_ddn_long_relint_product_01_completion/PUBLIC_BROWSER_DEPENDENCY_STATUS.md"], "CRITICAL", False, "sealed offline browser/package custody가 없다."),
    ("V1-C046", "license·notice·SBOM", "code/docs/assets/third-party 권리와 release notices를 봉인한다.", "release_open", "REQUIRED", "V1.0", "V0.9", "V1.0", "V1.0", ["V1-C043"], "NOT_IMPLEMENTED", ["work/codex/20260827_ddn_long_relint_product_01_completion/RIGHTS_AND_LICENSE_EXCLUSION_LEDGER.md"], "CRITICAL", True, "Apache-2.0은 후보일 뿐이며 PC01/projectile public copy는 0이다."),
    ("V1-C047", "public conformance", "공개 source tree에서 독립 실행 가능한 V1 필수 계약 검사를 제공한다.", "release_open", "REQUIRED", "V1.0", "V0.9", "V1.0", "CONTINUOUS", ["V1-C043", "V1-C041"], "PARTIAL", ["pack", "tests", "work/codex/20260827_ddn_long_relint_product_01_completion/PUBLIC_CONFORMANCE_ROLE_LEDGER.md"], "CRITICAL", True, "private/rights-blocked fixture 격리 정책이 필요하다."),
    ("V1-C048", "글무늬·Regex", "결정적 text pattern 값을 제공한다.", "future_partial", "OPTIONAL", "V1.0", "V1.0", "V1.5", "V1.5", ["V1-C006", "V1-C009"], "PARTIAL", ["docs/context/proposals/PROPOSAL_REGEX_LITERAL_AND_CALL_OVERLOAD_V1_20260217.md", "tools/teul-cli/src/runtime"], "MEDIUM", True, "V1 floor에는 포함하지 않고 V1.5 필수화 후보로 유지한다."),
    ("V1-C049", "기본 Proof·보임", "assumption·candidate·checker verdict를 분리한다.", "future_partial", "OPTIONAL", "V1.0", "V1.5", "V2.0", "V2.0", ["V1-C005", "V1-C028"], "PARTIAL", ["tool/src/proof", "pack/age1_immediate_proof_smoke_v1", "docs/ssot/ssot/SSOT_ALL_v25.15.0.md#RD-171"], "HIGH", True, "pack 존재를 V1 제품 closure로 계산하지 않는다."),
    ("V1-C050", "State Machine", "typed 상태와 사건 전이를 원자적으로 실행한다.", "future_partial", "DEFERRED", "V2.0", "V2.0", "V2.5", "V2.5", ["V1-C026", "V1-C028"], "PARTIAL", ["pack/state_machine_transition_failure_report_v1", "tools/teul-cli/src/runtime"], "HIGH", True, "V2.5 REQUIRED 후보이며 V1 floor에서 제외한다."),
    ("V1-C051", "AI 협업 surface", "AI 제안과 실행 권위를 분리한 도구 연동을 제공한다.", "future_partial", "DEFERRED", "V3.0", "V3.0", "V3.5", "V3.5", ["V1-C028", "V1-C030"], "PARTIAL", ["tool/src/ai_prompt.rs", "tools/teul-cli/src/cli/ai.rs"], "HIGH", True, "말힘누리·AI 제안 provenance는 별도 트랙이며 V1 floor가 아니다."),
    ("V1-C052", "부분·완전 self-hosting", "언어 도구 일부 또는 전체를 DDN으로 구현한다.", "future_partial", "DEFERRED", "V1.8", "V1.8", "V4_PLUS", "V4_PLUS", ["V1-C031", "V1-C032", "V1-C047"], "NOT_IMPLEMENTED", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md"], "HIGH", True, "부분 self-hosting은 앞당길 수 있으나 완전 self-hosting은 V4+ 후보다."),
    ("V1-C053", "세계·결정적 simulation", "상태·시간·사건을 대규모 결정적 세계로 확장한다.", "future_partial", "DEFERRED", "V2.5", "V2.5", "V2.8", "V3.0", ["V1-C026", "V1-C028", "V1-C050"], "PARTIAL", ["core/src/realms.rs", "tools/teul-cli/src/cli/universe.rs", "tools/teul-cli/src/cli/evolving_universe.rs"], "HIGH", True, "legacy/experimental 구현을 V1 contract로 계산하지 않는다."),
    ("V1-C054", "V0.9 외부 사용자 검증·V1 승격", "처음 접함부터 저장·재열기까지 외부 사용자 성공을 증명한다.", "release_open", "REQUIRED", "V1.0", "V0.9", "V1.0", "V1.0", ["V1-C045", "V1-C046", "V1-C047", "V1-C037"], "NOT_IMPLEMENTED", ["docs/ssot/ssot/SSOT_ALL_v25.15.0.md#PM-O1", "work/codex/20260827_ddn_long_relint_product_01_completion/IMPLEMENTATION_HANDOFF.md"], "CRITICAL", True, "external_user_success_count는 0이며 Human PASS도 없다."),
]


VERSION_ORDER = {
    "V0.9": 9, "V1.0": 10, "V1.2": 12, "V1.5": 15, "V1.8": 18,
    "V2.0": 20, "V2.2": 22, "V2.5": 25, "V2.8": 28,
    "V3.0": 30, "V3.5": 35, "V4_PLUS": 40, "CONTINUOUS": 99, "OPEN": 100,
}


def capability(row: tuple) -> dict:
    (cid, name, purpose, profile, member, first, experimental, required,
     completion, deps, maturity, evidence, risk, owner, notes) = row
    axes = dict(PROFILES[profile])
    semantics = "DOCS_FIRST_OR_SCOPED_CLOSED" if maturity != "NOT_IMPLEMENTED" else "OPEN"
    surface = "PARTIAL" if maturity not in {"NOT_IMPLEMENTED", "UNKNOWN"} else "OPEN"
    closure = "OPEN" if member == "REQUIRED" else "NOT_IN_V1_FLOOR"
    return {
        "capability_id": cid,
        "korean_name": name,
        "short_purpose": purpose,
        "authority_source": [SSOT_VERSION, "PRODUCT_CHAT_OWNER_ROADMAP_DIRECTION_20260827"],
        "authority_version": SSOT_VERSION,
        "semantic_status": semantics,
        "surface_status": surface,
        **axes,
        "current_product_maturity": maturity,
        "v1_membership": member,
        "authoritative_ssot_membership": "OPEN_NOT_YET_POPULATED",
        "membership_authority": "OWNER_PRODUCT_ROADMAP_INPUT_NOT_SSOT_MEMBERSHIP",
        "required_closure_gate_status": closure,
        "first_target_version": first,
        "experimental_from": experimental,
        "required_from": required,
        "completion_target": completion,
        "dependency_ids": deps,
        "compatibility_risk": risk,
        "self_hosting_relevance": "DIRECT" if cid in {"V1-C001", "V1-C020", "V1-C031", "V1-C032", "V1-C047", "V1-C052"} else "INDIRECT",
        "evidence_refs": evidence,
        "last_verified_target": PRODUCT_FIXED if PRODUCT_FIXED in evidence else (evidence[-1] if evidence else "NONE"),
        "successor_impact": "REBASE_REQUIRED" if maturity == "IMPLEMENTED_UNVERIFIED" else "ADDITIVE_OR_UNASSESSED",
        "owner_decision_required": owner,
        "notes": notes,
    }


CAPABILITIES = [capability(row) for row in RAW]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def table(rows: list[list[str]], headers: list[str]) -> str:
    def clean(v: str) -> str:
        return str(v).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(clean(v) for v in row) + " |" for row in rows]
    return "\n".join(out)


def common_header(title: str) -> str:
    return f"""# {title}

```text
PROGRAM_ID: DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1
SSOT_ALL: {SSOT_VERSION} / {SSOT_ALL_SHA256}
SSOT_ALL_MANIFEST_SHA256: {SSOT_MANIFEST_SHA256}
WORKSPACE_BUNDLE: {WORKSPACE_BUNDLE} / {WORKSPACE_MANIFEST_SHA256}
PUBLIC_LANGUAGE_SPEC: {PUBLIC_SPEC}
PROGRAM_BASELINE: {BASELINE}
VERIFIED_PRODUCT_FLOOR: UNCLAIMABLE
AUTHORITATIVE_V1_MEMBERSHIP_ROWS: 0
```
"""


def generate_registry() -> None:
    payload = {
        "schema": "ddn.v1_capability_registry.r1",
        "program_id": "DDN_V1_PRODUCT_CLOSURE_LONG_RANGE_R1",
        "authority": {
            "internal_ssot": SSOT_VERSION,
            "ssot_all_sha256": SSOT_ALL_SHA256,
            "ssot_all_manifest_sha256": SSOT_MANIFEST_SHA256,
            "public_spec": PUBLIC_SPEC,
            "authoritative_v1_membership_rows": 0,
            "verified_product_floor": "UNCLAIMABLE",
        },
        "membership_semantics": "ROADMAP_OWNER_INPUT_ONLY_NOT_AUTHORITATIVE_SSOT_MEMBERSHIP",
        "capabilities": CAPABILITIES,
    }
    write_json(OUT / "v1_capability_registry.detjson", payload)
    write_json(OUT / "v1_implementation_matrix.detjson", {
        "schema": "ddn.v1_implementation_matrix.r1",
        "program_id": payload["program_id"],
        "rows": [{"capability_id": c["capability_id"], **{a: c[a] for a in AXES}, "current_product_maturity": c["current_product_maturity"], "evidence_refs": c["evidence_refs"]} for c in CAPABILITIES],
    })
    write_json(OUT / "product_version_horizon.detjson", {
        "schema": "ddn.product_version_horizon.r1",
        "program_id": payload["program_id"],
        "rows": [{k: c[k] for k in ("capability_id", "korean_name", "v1_membership", "first_target_version", "experimental_from", "required_from", "completion_target")} for c in CAPABILITIES],
    })
    write_json(OUT / "v1_dependency_dag.detjson", {
        "schema": "ddn.v1_dependency_dag.r1",
        "program_id": payload["program_id"],
        "nodes": [{"capability_id": c["capability_id"], "dependencies": c["dependency_ids"], "required": c["v1_membership"] == "REQUIRED", "gate_status": c["required_closure_gate_status"]} for c in CAPABILITIES],
        "critical_path_candidate": ["V1-C001", "V1-C002", "V1-C003", "V1-C031", "V1-C032", "V1-C034", "V1-C035", "V1-C037", "V1-C043", "V1-C044", "V1-C045", "V1-C046", "V1-C047", "V1-C054"],
    })


def generate_docs() -> None:
    counts = {m: sum(c["v1_membership"] == m for c in CAPABILITIES) for m in ("REQUIRED", "OPTIONAL", "DEFERRED")}
    maturity = {m: sum(c["current_product_maturity"] == m for c in CAPABILITIES) for m in ("IMPLEMENTED_VERIFIED", "IMPLEMENTED_UNVERIFIED", "PARTIAL", "PLANNED", "NOT_IMPLEMENTED", "UNKNOWN")}

    write_text(OUT / "00_CURRENT_PRODUCT_MATURITY_AND_VERSION.md", common_header("현재 제품 maturity와 네 버전축") + f"""
## 판정

| 축 | 현재값 | 의미 |
|---|---|---|
| INTERNAL_SSOT_VERSION | `{SSOT_VERSION}` | docs-first live current |
| DEVELOPMENT_MATURITY | `UNCLAIMABLE` | actual membership/gate가 아직 비어 있음 |
| PUBLIC_LANGUAGE_SPEC_VERSION | `{PUBLIC_SPEC}` | 내부 SSOT와 별도 고정 계보 |
| PUBLIC_PRODUCT_VERSION | `UNRELEASED` | public release/activation/Human PASS 없음 |

제품Chat이 제시한 V1.0~V4+ 사다리는 승인된 product roadmap input이다. 그러나 live SSOT의 실제 V1 membership은 0행이므로 numeric floor를 계산하지 않는다. `V0.6`도 현재 제품판으로 선언하지 않는다.

## 현재 수치

- capability family: `{len(CAPABILITIES)}`
- provisional REQUIRED/OPTIONAL/DEFERRED: `{counts['REQUIRED']}/{counts['OPTIONAL']}/{counts['DEFERRED']}`
- full-capability IMPLEMENTED_VERIFIED: `{maturity['IMPLEMENTED_VERIFIED']}`
- IMPLEMENTED_UNVERIFIED/PARTIAL/NOT_IMPLEMENTED: `{maturity['IMPLEMENTED_UNVERIFIED']}/{maturity['PARTIAL']}/{maturity['NOT_IMPLEMENTED']}`
- UNKNOWN: `{maturity['UNKNOWN']}`

독립 PASS된 세부 slice는 evidence history로 보존하지만 더 넓은 capability 전체를 `IMPLEMENTED_VERIFIED`로 계산하지 않았다.
""")

    rows = [[c["capability_id"], c["korean_name"], c["v1_membership"], c["current_product_maturity"], c["first_target_version"], c["required_from"], c["notes"]] for c in CAPABILITIES]
    write_text(OUT / "01_V1_CAPABILITY_CENSUS.md", common_header("V1 capability census R1") + "\n" + table(rows, ["ID", "이름", "V1", "제품 상태", "첫 목표", "필수화", "경계"]) + "\n\n전체 필드는 `v1_capability_registry.detjson`이 소유한다. 이 표의 membership은 SSOT 표가 아니라 Owner product-roadmap input이다.\n")

    matrix_rows = [[c["capability_id"], c["parser_status"], c["typed_ir_status"], c["runtime_status"], c["official_cli_status"], c["wasm_status"], c["workbench_status"], c["conformance_status"]] for c in CAPABILITIES]
    write_text(OUT / "02_V1_IMPLEMENTATION_MATRIX.md", common_header("V1 implementation matrix R1") + "\n" + table(matrix_rows, ["ID", "parser", "typed IR", "runtime", "official CLI", "WASM", "Workbench", "conformance"]) + "\n\n`PARTIAL`은 하나 이상의 실제 경로·slice evidence가 있으나 capability 전체 required gate가 닫히지 않았다는 뜻이다.\n")

    member_rows = [[m, str(counts[m]), "provisional product-roadmap membership"] for m in ("REQUIRED", "OPTIONAL", "DEFERRED")]
    write_text(OUT / "03_V1_RELEASE_MEMBERSHIP.md", common_header("V1 release membership R1") + "\n" + table(member_rows, ["membership", "count", "authority"]) + """

## 중요한 경계

- authoritative SSOT V1 membership row: `0`
- 이 문서의 48/2/4 분류는 제품Chat Owner roadmap direction의 실행용 projection이다.
- readiness floor 계산에는 사용하지 않는다.
- OPTIONAL/DEFERRED는 V1 floor를 낮추지 않는다.
- REQUIRED blocker는 membership과 required closure gate OPEN의 교집합으로 파생한다.

## 즉시 blocker family

1. shared language/runtime authority와 official CLI identity
2. current V25 Workbench frontdoor 및 observation manifest
3. public projection self-containment와 private fixture 격리
4. public-source-only build와 clean install
5. license/notices/SBOM 및 권리 custody
6. 외부 사용자 검증과 V1 promotion
""")

    dag_rows = [[c["capability_id"], ", ".join(c["dependency_ids"]) or "-", c["required_closure_gate_status"]] for c in CAPABILITIES if c["v1_membership"] == "REQUIRED"]
    write_text(OUT / "04_V1_IMPLEMENTATION_DAG.md", common_header("V1 implementation DAG R1") + """
## critical path candidate

```text
Korean source/value identity
→ Definition/Binding current source epoch
→ shared semantic frontdoor
→ official CLI + WASM
→ RuntimeBridge + Workbench
→ deterministic public projection
→ public-source-only build
→ clean install + rights/SBOM
→ public conformance
→ external-user V0.9 validation
→ V1.0 promotion
```

이 경로는 첫 계산 후보이며 actual SSOT membership이 승격되기 전 readiness floor가 아니다.

""" + table(dag_rows, ["required ID", "dependency IDs", "closure gate"]) + "\n")

    write_text(OUT / "05_V1_OWNER_DECISIONS.md", common_header("V1 Owner 결정 대장 R1") + """
## 이미 승인된 product-program 방향

- 네 버전축 분리
- V1.0~V4+ maturity ladder
- V1 provisional REQUIRED/OPTIONAL/DEFERRED 방향
- V0.9 external-user validation before V1.0
- minor reversible choice는 manager가 계속 진행

## OWNER_FINAL_DECISION_REQUIRED

| 결정 | 추천 | 장점 | 비용/위험 |
|---|---|---|---|
| actual SSOT V1 membership·required gate 승격 | census 독립검토 후 정본관리Work successor | readiness floor를 계산 가능 | 현 Wave에서는 아직 승격 불가 |
| official CLI identity | `tool` shared CLI를 공식으로, teul-cli는 KEEP/MOVE/DROP 감사 후 이관 | native/WASM authority 수렴 | compatibility inventory 필요 |
| Workbench current frontdoor | Rust V25 frontdoor + canonical observation manifest | JS 의미 재해석 제거 | 실제 UI/runtime integration vertical 필요 |
| public fixture isolation | 권리 확인 public conformance subset + internal feature-gated tests | 공개 tree self-contained | test layout 조정 필요 |
| stable wire/diagnostics | V1 RC 직전 별도 freeze | 조기 호환 부채 방지 | RC 전까지 experimental label 유지 |
| final license | Apache-2.0 우선 후보, rights audit 뒤 확정 | 공개 기여에 명확 | assets/third-party audit 필요 |

결정에 의존하지 않는 inventory·test isolation 설계·KEEP/MOVE/DROP 감사는 계속한다.
""")

    horizon_rows = [[c["capability_id"], c["korean_name"], c["first_target_version"], c["experimental_from"], c["required_from"], c["completion_target"]] for c in CAPABILITIES]
    write_text(OUT / "06_PRODUCT_VERSION_HORIZON.md", common_header("제품 version horizon R1") + "\n" + table(horizon_rows, ["ID", "capability", "first", "experimental", "required", "completion"]) + "\n")

    write_text(OUT / "07_V1_WAVE_PLAN.md", common_header("V1 Wave plan R1") + """
| Wave | 목적 | 현재 disposition |
|---|---|---|
| 0 | current/custody/evidence census | IN_PROGRESS |
| 1 | source epoch + Definition/Binding + declaration head | PC01 review pending; frontdoor successor 준비 |
| 2 | morphology + closed multisurface + canon | inventory first |
| 3 | callable + ResultPlace + failure/control | docs-first/product gap inventory |
| 4 | generic/구실/collection/Selection | K0~ behavior gap inventory |
| 5 | Basic Tensor R1 | executable oracle gap |
| 6 | module/local dependency/lock | partial product paths |
| 7 | determinism/receipt/replay/input seal | scoped evidence, stable wire open |
| 8 | shared runtime/CLI/WASM | critical-path convergence |
| 9 | Workbench/save/reopen lifecycle | current V25 success open |
| 10 | public source projection | deterministic but self-containment FAIL |
| 11 | packaging/license/SBOM | not started |
| 12 | V0.9 external validation/V1 promotion | external success 0 |

## first verticals

1. `DDN-V1-FD01`: current V25 shared frontdoor and Workbench observation convergence
2. `DDN-V1-PUB01`: public conformance/private fixture isolation
3. `DDN-V1-CLI01`: official CLI identity and teul-cli KEEP/MOVE/DROP audit

FD01은 제품 의미를 새로 만들지 않고 v25.15.0의 current `:=`/`<-`와 RD-189 shared authority를 실제 product path로 연결한다. stable wire·새 syntax·UI redesign은 포함하지 않는다.
""")

    path_rows = [[c["capability_id"], c["parser_status"], c["runtime_status"], c["official_cli_status"], c["wasm_status"], c["workbench_status"], c["current_product_maturity"]] for c in CAPABILITIES if c["v1_membership"] == "REQUIRED"]
    write_text(OUT / "08_V1_PRODUCT_PATH_AND_TEST_MATRIX.md", common_header("V1 product path와 test matrix R1") + "\n" + table(path_rows, ["ID", "source/parser", "runtime", "CLI", "WASM", "Workbench", "maturity"]) + "\n")

    write_text(OUT / "09_LEGACY_AUTHORITY_RETIREMENT_PLAN.md", common_header("legacy semantic authority retirement plan R1") + """
| authority 후보 | 현 상태 | 목표 | 제거/이관 전 gate |
|---|---|---|---|
| `tools/teul-cli/src/lang/**` | 독립 lexer/parser 존재 | shared `lang` frontdoor로 MOVE/DROP | golden command inventory + parity |
| `tools/teul-cli/src/runtime/**` | 독립 runtime 존재 | shared runtime 또는 명시 adapter | command KEEP/MOVE/DROP + receipt parity |
| `tools/teul-cli/src/canon.rs` | 독립 lowering/canon | shared canon consumer | source/canon roundtrip corpus |
| `lang/src/currentline.rs` | 별도 regex/dispatch 역사 경로 | shared typed authority 또는 history-only | call-site·pack migration |
| `tool/src/preprocess.rs` | 일부 semantic lowering | shared frontdoor로 ownership 명시 | no harness-only lowering |
| `source_readiness.js` | strict JS source analysis | Rust V25 analysis 결과 consumer | FD01 actual Edge gate |
| Workbench renderer helpers | raw result 추론 가능성 | canonical view payload consumer only | semantic fallback mutations |

삭제는 이 프로그램에서 승인하지 않는다. inventory→migration→independent parity→successor removal 순서를 지킨다.
""")

    write_text(OUT / "10_V1_RELEASE_CLOSURE_PLAN.md", common_header("V1 release closure plan R1") + """
## release chain

```text
CLEAN SEALED INTERNAL COMMIT
→ deterministic PUBLIC_SOURCE projection
→ public-source-only build/test/WASM/examples/SPEC check
→ signed/versioned RELEASE_ARTIFACT + notices/SBOM
→ clean-machine install or install-free Web entry
→ V0.9 external-user workflow
→ issue repair band
→ owner V1.0 promotion
```

## current gates

| gate | current |
|---|---|
| deterministic projection A/B | PASS candidate evidence |
| public non-browser self-containment | FAIL |
| sealed offline browser dependency | BLOCKED/OPEN |
| private path/include preflight | FAIL |
| rights and final license | OPEN |
| public push/release | NOT AUTHORIZED |
| Human PASS | NOT CLAIMED |
| external user success | 0 |

Internal/experimental artifact와 public release artifact를 혼동하지 않는다.
""")


def generate_packets() -> None:
    packet_dir = OUT / "verticals"
    packets = {
        "DDN_V1_FD01_IMPLEMENTATION_PACKET.md": ("DDN-V1-FD01", "current V25 shared frontdoor와 Workbench observation convergence", "lang/src/frontdoor.rs; tool/src/source_analysis.rs; tool/src/wasm_api.rs; solutions/seamgrim_ui_mvp/ui/workbench/source_readiness.js; workbench.js", "Rust V25 frontdoor가 source analysis와 execution을 소유하고 Workbench는 canonical observation manifest만 소비한다.", "PC01/G14 targeted verdict 또는 정확한 unaffected 판정; UI redesign 0; new syntax 0; stable wire 0"),
        "DDN_V1_PUB01_IMPLEMENTATION_PACKET.md": ("DDN-V1-PUB01", "public conformance와 private fixture dependency 격리", "public projection policy/manifest; public conformance tests; compile-time fixture references", "권리 미확인 pack을 복사하지 않고 public subset이 fresh projection에서 독립 build/test한다.", "rights inference 0; product semantics 0; GitHub/public push 0"),
        "DDN_V1_CLI01_AUDIT_PACKET.md": ("DDN-V1-CLI01", "official CLI identity와 teul-cli KEEP/MOVE/DROP 감사", "tool/src/main.rs; tools/teul-cli/src/**; scripts; public docs", "각 command와 semantic owner를 inventory하고 shared CLI로의 migration DAG를 만든다.", "이번 I1은 read-only audit; command 삭제 0; compatibility promise 0"),
    }
    for filename, (vid, purpose, paths, contract, bounds) in packets.items():
        write_text(packet_dir / filename, common_header(f"{vid} 실행 패킷") + f"""
VERTICAL_ID: `{vid}`

## 목적

{purpose}

## 허용 경로

{paths}

## authoritative contract

{contract}

## 선행·금지 경계

{bounds}

## DoD

1. 실제 제품 source가 공통 frontdoor 또는 명시된 공개 subset을 통과한다.
2. positive·negative·migration·determinism regression을 갖는다.
3. silent fallback mutation이 RED가 된다.
4. native/WASM/Workbench 해당 범위 parity를 실제 입력으로 검증한다.
5. fixed product/test HEAD와 문서 전용 handoff commit을 분리한다.
6. 독립검토 전 PASS/CLOSED를 주장하지 않는다.

## failure disposition

두 번의 좁은 local correction 뒤에도 같은 blocker면 exact owner/authority packet으로 전환한다. 다른 safe slice는 계속한다.
""")

        review_name = filename.replace("IMPLEMENTATION_PACKET", "INDEPENDENT_REVIEW_PACKET").replace("AUDIT_PACKET", "INDEPENDENT_REVIEW_PACKET")
        write_text(packet_dir / review_name, common_header(f"{vid} fixed-target 독립검토 패킷") + f"""
VERTICAL_ID: `{vid}`
REVIEW_MODE: `FRESH_ISOLATED_FIXED_TARGET`
FIXED_TARGET_COMMIT: `TO_BE_BOUND_BY_IMPLEMENTER_HANDOFF`

## 독립 확인

1. fixed target의 direct lineage·merge count·changed paths를 직접 계산한다.
2. `{contract}`가 실제 product/audit 경로에서 성립하는지 원문과 실행으로 검증한다.
3. positive·negative·migration·determinism test가 실제 대상 코드를 실행하는지 확인한다.
4. hidden fallback·독립 semantic authority·scope creep를 공격한다.
5. 최소 한 축의 real mutation을 RED→정확한 복원→GREEN으로 재현한다.
6. 구현자가 제외한 `{bounds}`가 실제 diff와 public surface에서 0인지 확인한다.
7. 제품·SSOT·public SPEC·UI·release claim을 검토 scope보다 넓히지 않는다.

## verdict

`PASS | PASS_WITH_FOLLOW_UP | FAIL | BLOCKED_BY_AUTHORITY | BLOCKED_BY_MISSING_EVIDENCE`

보고서 commit은 fixed handoff의 직접 후손이며 review 문서만 포함한다. product correction은 review branch에서 하지 않는다.
""")

    write_text(OUT / "INDEPENDENT_REVIEW_REQUEST_WAVE0.md", common_header("Wave 0 census 독립검토 요청") + """
```text
FIXED_CENSUS_HEAD: 3afdd4b79b70a417889a78910501b41486fe0bef
REVIEW_PARENT: 이 요청서를 포함하는 최종 handoff commit의 exact identity
```

## 검토 범위

1. live v25.15.0/public v0.5.0/workspace bundle custody
2. 54 capability ID·membership·horizon·dependency의 결정성
3. Owner roadmap membership과 authoritative SSOT membership 0의 분리
4. evidence 없는 IMPLEMENTED_VERIFIED 0
5. scoped historical PASS의 과대 일반화 0 및 유실 0
6. DAG acyclic, critical path 후보와 first vertical의 실제 dependency
7. RELINT review-pending 상태 비승격
8. 제품·SSOT·public SPEC diff 0

판정은 `PASS | PASS_WITH_FOLLOW_UP | FAIL | BLOCKED_BY_AUTHORITY | BLOCKED_BY_MISSING_EVIDENCE`다. 검토자는 registry row 표본이 아니라 전수를 machine checker와 source evidence로 공격한다.

검토 branch는 `REVIEW_PARENT`의 직접 후손이어야 하며 report/session delta만 commit한다. 제품·SSOT·public SPEC·census fixed artifact를 review 중 교정하지 않는다.
""")

    write_text(OUT / "PROGRAM_CHECKPOINT.md", common_header("DDN V1 Product Closure Wave 0 checkpoint") + """
```text
PROGRAM_STATUS: WAVE_0_CENSUS_DRAFT_LOCAL_VALIDATION_PASS
EXISTING_PROGRAM_DISPOSITION: RELINT_PREDECESSOR_EVIDENCE_REVIEW_PENDING
CURRENT_DEVELOPMENT_TARGET: V0.6_CENSUS_GATE_ONLY
VERIFIED_PRODUCT_FLOOR: UNCLAIMABLE
PRODUCT_IMPLEMENTATION_STARTED: NO
SSOT_EDIT: 0
PUBLIC_SPEC_EDIT: 0
PUBLIC_RELEASE: NOT_AUTHORIZED
HUMAN_PASS: NOT_CLAIMED
external_user_success_count: 0
```
""")


def main() -> None:
    generate_registry()
    generate_docs()
    generate_packets()
    print(f"generated {len(CAPABILITIES)} capabilities in {OUT}")


if __name__ == "__main__":
    main()
