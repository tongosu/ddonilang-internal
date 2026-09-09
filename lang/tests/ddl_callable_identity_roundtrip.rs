use ddonirang_lang::{canonicalize_ddl_wave1, canonicalize_ddl_wave2, parse_ddl_wave1, parse_ddl_wave2, parse_v25, OmittedPayload};
use ddonirang_lang::ddl::{parse_ddl_wave2_with_context, DdlCallableParamRegistryEntry, DdlCallableRegistryEntry, DdlCallableWave2Context};

const WAVE1: &str = "#!한국어\n원주율:셈수 :={...}.\n\n#!日本語\n円周率:数値 :={...}.\n";
const WAVE2: &str = "#!한국어\n더하기(왼쪽:셈수[을], 오른쪽:셈수[와]) -> 셈수 :={...}.\n\n#!日本語\n加算(左:数値[を], 右:数値[と]) -> 数値 :={...}.\n";
const WAVE2_REVERSED: &str = "#!日本語\n加算(左:数値[を], 右:数値[と]) -> 数値 :={...}.\n\n#!한국어\n더하기(왼쪽:셈수[을], 오른쪽:셈수[와]) -> 셈수 :={...}.\n";

fn error(source: &str, path: &str) -> &'static str { parse_ddl_wave2(source, path).expect_err("must fail closed").code }

fn standard_entries() -> Vec<DdlCallableRegistryEntry> {
    vec![
        DdlCallableRegistryEntry { header: "#!한국어", profile_identity: "language-profile:ko", localized_name: "더하기", parameters: [
            DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.left", type_identity: "type:number", relation_identity: "relation:math.add.left", localized_name: "왼쪽", localized_type: "셈수", relation_surface: "을" },
            DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.right", type_identity: "type:number", relation_identity: "relation:math.add.right", localized_name: "오른쪽", localized_type: "셈수", relation_surface: "와" },
        ], localized_result_type: "셈수", definition_identity: "definition:math.add", result_type_identity: "type:number", callable_kind: "callable:pure" },
        DdlCallableRegistryEntry { header: "#!日本語", profile_identity: "language-profile:ja", localized_name: "加算", parameters: [
            DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.left", type_identity: "type:number", relation_identity: "relation:math.add.left", localized_name: "左", localized_type: "数値", relation_surface: "を" },
            DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.right", type_identity: "type:number", relation_identity: "relation:math.add.right", localized_name: "右", localized_type: "数値", relation_surface: "と" },
        ], localized_result_type: "数値", definition_identity: "definition:math.add", result_type_identity: "type:number", callable_kind: "callable:pure" },
    ]
}

fn contextual_error(source: &str, context: DdlCallableWave2Context) -> &'static str {
    parse_ddl_wave2_with_context(source, "add.ddl", &context).expect_err("must fail closed").code
}

#[test]
fn p01_to_p10_callable_projection_is_identity_bound_and_byte_stable() {
    for path in ["add.ddl", "add.옮김"] {
        let document = parse_ddl_wave2(WAVE2, path).unwrap();
        let ko = &document.sections[0].projection;
        let ja = &document.sections[1].projection;
        assert_eq!(ko.definition_identity, "definition:math.add");
        assert_eq!(ko.definition_identity, ja.definition_identity);
        assert_eq!(ko.callable_kind, ja.callable_kind);
        assert_eq!(ko.result_type_identity, ja.result_type_identity);
        assert_eq!(ko.parameters.len(), 2);
        assert_eq!(ko.parameters.iter().map(|p| &p.param_pin_identity).collect::<Vec<_>>(), ja.parameters.iter().map(|p| &p.param_pin_identity).collect::<Vec<_>>());
        assert_eq!(ko.parameters.iter().map(|p| &p.type_identity).collect::<Vec<_>>(), ja.parameters.iter().map(|p| &p.type_identity).collect::<Vec<_>>());
        assert_eq!(ko.parameters.iter().map(|p| &p.relation_identity).collect::<Vec<_>>(), ja.parameters.iter().map(|p| &p.relation_identity).collect::<Vec<_>>());
        assert_ne!(ko.parameters[0].param_pin_identity, ko.parameters[1].param_pin_identity);
        assert_eq!(ko.omitted_payload, OmittedPayload::CallableBody);
        let canon = canonicalize_ddl_wave2(&document);
        assert_eq!(canon, WAVE2);
        assert_eq!(canonicalize_ddl_wave2(&parse_ddl_wave2(&canon, path).unwrap()), canon);
    }
}

#[test]
fn p11_and_p12_section_order_is_presentation_only_with_utf8_byte_spans() {
    let normal = parse_ddl_wave2(WAVE2, "add.ddl").unwrap();
    let reversed = parse_ddl_wave2(WAVE2_REVERSED, "add.ddl").unwrap();
    assert_eq!(normal.sections[0].projection.definition_identity, reversed.sections[1].projection.definition_identity);
    assert_eq!(normal.sections[0].projection.result_type_identity, reversed.sections[1].projection.result_type_identity);
    assert_eq!(canonicalize_ddl_wave2(&reversed), WAVE2_REVERSED);
    for section in &normal.sections {
        assert!(WAVE2[section.header_span.start..section.header_span.end].starts_with("#!"));
        assert!(WAVE2[section.content_span.start..section.content_span.end].contains(&section.projection.localized_name));
        assert!(WAVE2[section.projection.declaration_span.start..section.projection.declaration_span.end].contains(&section.projection.localized_name));
    }
    assert_eq!(normal.source_span.end, WAVE2.len());
}

#[test]
fn n01_to_n05_profiles_and_translation_cardinality_fail_closed() {
    assert_eq!(error(&WAVE2.replace("#!日本語", "#!한국어"), "add.ddl"), "E_DDL_PROFILE_DUPLICATE");
    assert_eq!(error(&WAVE2.replace("#!日本語", "#!English"), "add.ddl"), "E_DDL_PROFILE_UNKNOWN");
    assert_eq!(error(&WAVE2.replace("#!日本語", "#!Quechua"), "add.ddl"), "E_DDL_GENERIC_QUECHUA_FORBIDDEN");
    assert_eq!(contextual_error(WAVE2, DdlCallableWave2Context::from_entries(vec![standard_entries()[0]])), "E_DDL_PROFILE_UNKNOWN");
    assert_eq!(error(&format!("{WAVE2}\n#!한국어\n더하기(왼쪽:셈수[을], 오른쪽:셈수[와]) -> 셈수 :={{...}}.\n"), "add.ddl"), "E_DDL_SECTION_COUNT");
}

#[test]
fn n06_to_n13_identity_and_signature_mismatches_fail_closed() {
    let mut entries = standard_entries(); entries[1].definition_identity = "definition:other";
    assert_eq!(contextual_error(WAVE2, DdlCallableWave2Context::from_entries(entries)), "E_DDL_DEFINITION_IDENTITY_MISMATCH");
    let mut entries = standard_entries(); entries[1].callable_kind = "callable:other";
    assert_eq!(contextual_error(WAVE2, DdlCallableWave2Context::from_entries(entries)), "E_DDL_DEFINITION_IDENTITY_MISMATCH");
    let mut entries = standard_entries(); entries[1].result_type_identity = "type:other";
    assert_eq!(contextual_error(WAVE2, DdlCallableWave2Context::from_entries(entries)), "E_DDL_TYPE_IDENTITY_MISMATCH");
    assert_eq!(error(&WAVE2.replace("왼쪽:셈수[을], ", ""), "add.ddl"), "E_DDL_OMITTED_VALUE_SHAPE");
    assert_eq!(error(&WAVE2.replace("오른쪽:셈수[와]", "오른쪽:셈수[와], 추가:셈수[을]"), "add.ddl"), "E_DDL_OMITTED_VALUE_SHAPE");
    let mut entries = standard_entries(); entries[1].parameters[1].pin_identity = "param-pin:math.add.left";
    assert_eq!(contextual_error(WAVE2, DdlCallableWave2Context::from_entries(entries)), "E_DDL_DEFINITION_IDENTITY_MISMATCH");
    let mut entries = standard_entries(); entries[1].parameters.swap(0, 1);
    let swapped = WAVE2.replace("左:数値[を], 右:数値[と]", "右:数値[と], 左:数値[を]");
    assert_eq!(contextual_error(&swapped, DdlCallableWave2Context::from_entries(entries)), "E_DDL_DEFINITION_IDENTITY_MISMATCH");
    let mut entries = standard_entries(); entries[1].parameters[1].relation_identity = "relation:math.add.left";
    assert_eq!(contextual_error(WAVE2, DdlCallableWave2Context::from_entries(entries)), "E_DDL_DEFINITION_IDENTITY_MISMATCH");
}

#[test]
fn n14_to_n18_omission_is_ddl_internal_and_non_executable() {
    assert_eq!(error(WAVE2, "add.ddn"), "E_DDL_EXTENSION_UNSUPPORTED");
    assert!(parse_v25(WAVE2, "ordinary.ddn").is_err());
    assert!(parse_ddl_wave1(WAVE2, "add.ddl").is_err());
    assert!(parse_ddl_wave2(WAVE1, "value.ddl").is_err());
    assert_eq!(error(&WAVE2.replace(":={...}", ":={1}"), "add.ddl"), "E_DDL_OMITTED_VALUE_SHAPE");
    assert_eq!(canonicalize_ddl_wave1(&parse_ddl_wave1(WAVE1, "value.ddl").unwrap()), WAVE1);
    assert!(parse_v25("더하기(왼쪽:셈수[을], 오른쪽:셈수[와]) -> 셈수 :={...}.", "run.ddn").is_err());
}
