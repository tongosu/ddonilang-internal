use ddonirang_lang::{canonicalize_ddl_wave3, parse_ddl_wave3, parse_v25};
use ddonirang_lang::ddl::{parse_ddl_wave3_with_context, DdlSumRegistryEntry, DdlSumWave3Context};

const NORMAL: &str = "#!한국어\n방향:고름씨 := {\n    $왼쪽.\n    $오른쪽.\n}.\n\n#!日本語\n方向:選択型 := {\n    $左.\n    $右.\n}.\n";
const REVERSED: &str = "#!日本語\n方向:選択型 := {\n    $右.\n    $左.\n}.\n\n#!한국어\n방향:고름씨 := {\n    $오른쪽.\n    $왼쪽.\n}.\n";

#[test]
fn wave3_sum_identity_is_order_independent_and_canon_is_stable() {
    for (source, expected) in [(NORMAL, NORMAL), (REVERSED, REVERSED)] {
        for path in ["direction.ddl", "direction.옮김"] {
            let document = parse_ddl_wave3(source, path).expect("sum projection");
            assert_eq!(document.sections[0].projection.definition_identity, "DDL.TYPE.DIRECTION.R1");
            assert_eq!(document.sections[0].projection.type_identity, "DDL.TYPE.DIRECTION.R1");
            let mut first = document.sections[0].projection.branches.iter().map(|branch| branch.owned_branch_identity.clone()).collect::<Vec<_>>();
            let mut second = document.sections[1].projection.branches.iter().map(|branch| branch.owned_branch_identity.clone()).collect::<Vec<_>>();
            first.sort(); second.sort(); assert_eq!(first, second);
            let canon = canonicalize_ddl_wave3(&document); assert_eq!(canon, expected);
            assert_eq!(canonicalize_ddl_wave3(&parse_ddl_wave3(&canon, path).unwrap()), canon);
        }
    }
}

#[test]
fn wave3_sum_rejects_incomplete_or_non_ddl_surfaces() {
    for source in [NORMAL.replace("    $오른쪽.\n", ""), NORMAL.replace("    $왼쪽.\n", ""), NORMAL.replace("    $오른쪽.", "    $왼쪽."), NORMAL.replace("$오른쪽", "$위"), NORMAL.replace(":= {", ":={...}"), NORMAL.replace("$왼쪽.", "$왼쪽(값)."), NORMAL.replace("고름씨", "셈씨"), NORMAL.replace("選択型", "数値")] {
        let err = parse_ddl_wave3(&source, "direction.ddl").expect_err("must fail closed");
        assert!(matches!(err.code, "E_DDL_SUM_SHAPE" | "E_DDL_OWNED_BRANCH_IDENTITY_MISMATCH" | "E_DDL_SOURCE_UNBALANCED"), "{} for {source}", err.code);
    }
    assert_eq!(parse_ddl_wave3(NORMAL, "direction.ddn").unwrap_err().code, "E_DDL_EXTENSION_UNSUPPORTED");
    assert!(parse_v25(NORMAL, "direction.ddn").is_err());
}

#[test]
fn wave3_context_identity_mismatches_have_exact_diagnostics() {
    let base = parse_ddl_wave3(NORMAL, "direction.ddl").unwrap();
    let mut entries = [base.sections[0].projection.clone(), base.sections[1].projection.clone()];
    assert_eq!(entries[0].definition_identity, entries[1].definition_identity); // P06 semantic binding
    let registry = vec![
        DdlSumRegistryEntry { header:"#!한국어", profile_identity:"language-profile:ko", localized_name:"방향", localized_type:"고름씨", definition_identity:"DDL.TYPE.DIRECTION.R1", type_identity:"DDL.TYPE.DIRECTION.R1", branches:[("DDL.BRANCH.DIRECTION.LEFT.R1","왼쪽"),("DDL.BRANCH.DIRECTION.RIGHT.R1","오른쪽")]},
        DdlSumRegistryEntry { header:"#!日本語", profile_identity:"language-profile:ja", localized_name:"方向", localized_type:"選択型", definition_identity:"OTHER", type_identity:"DDL.TYPE.DIRECTION.R1", branches:[("DDL.BRANCH.DIRECTION.LEFT.R1","左"),("DDL.BRANCH.DIRECTION.RIGHT.R1","右")]},
    ];
    assert_eq!(parse_ddl_wave3_with_context(NORMAL, "direction.ddl", &DdlSumWave3Context::from_entries(registry)).unwrap_err().code, "E_DDL_DEFINITION_IDENTITY_MISMATCH");
    let registry = vec![
        DdlSumRegistryEntry { header:"#!한국어", profile_identity:"language-profile:ko", localized_name:"방향", localized_type:"고름씨", definition_identity:"DDL.TYPE.DIRECTION.R1", type_identity:"DDL.TYPE.DIRECTION.R1", branches:[("DDL.BRANCH.DIRECTION.LEFT.R1","왼쪽"),("DDL.BRANCH.DIRECTION.RIGHT.R1","오른쪽")]},
        DdlSumRegistryEntry { header:"#!日本語", profile_identity:"language-profile:ja", localized_name:"方向", localized_type:"選択型", definition_identity:"DDL.TYPE.DIRECTION.R1", type_identity:"OTHER", branches:[("DDL.BRANCH.DIRECTION.LEFT.R1","左"),("DDL.BRANCH.DIRECTION.RIGHT.R1","右")]},
    ];
    assert_eq!(parse_ddl_wave3_with_context(NORMAL, "direction.ddl", &DdlSumWave3Context::from_entries(registry)).unwrap_err().code, "E_DDL_TYPE_IDENTITY_MISMATCH");
    let registry = vec![
        DdlSumRegistryEntry { header:"#!한국어", profile_identity:"language-profile:ko", localized_name:"방향", localized_type:"고름씨", definition_identity:"DDL.TYPE.DIRECTION.R1", type_identity:"DDL.TYPE.DIRECTION.R1", branches:[("DDL.BRANCH.DIRECTION.LEFT.R1","왼쪽"),("DDL.BRANCH.DIRECTION.RIGHT.R1","오른쪽")]},
        DdlSumRegistryEntry { header:"#!日本語", profile_identity:"language-profile:ja", localized_name:"方向", localized_type:"選択型", definition_identity:"DDL.TYPE.DIRECTION.R1", type_identity:"DDL.TYPE.DIRECTION.R1", branches:[("DDL.BRANCH.DIRECTION.RIGHT.R1","左"),("DDL.BRANCH.DIRECTION.LEFT.R1","右")]},
    ];
    assert_eq!(parse_ddl_wave3_with_context(NORMAL, "direction.ddl", &DdlSumWave3Context::from_entries(registry)).unwrap_err().code, "E_DDL_OWNED_BRANCH_IDENTITY_MISMATCH");
    entries.swap(0,1); assert_ne!(entries[0].localized_name, entries[1].localized_name);
}

#[test]
fn wave3_positive_ledger_p01_to_p10_and_negative_matrix_n01_to_n15() {
    // P01..P10: exact source, extension parity, both order axes, identity, LF and repetition.
    for source in [NORMAL, REVERSED] { let one = canonicalize_ddl_wave3(&parse_ddl_wave3(source, "direction.ddl").unwrap()); let two = canonicalize_ddl_wave3(&parse_ddl_wave3(&one, "direction.옮김").unwrap()); assert_eq!(one, two); assert!(!one.contains('\r')); }
    // N01..N15 are represented by exact failure families, never a success fallback.
    let cases = [
        NORMAL.replace("    $왼쪽.\n", ""), NORMAL.replace("    $오른쪽.\n", ""), NORMAL.replace("$오른쪽.", "$왼쪽."), NORMAL.replace("$왼쪽.", "$오른쪽."), NORMAL.replace("$오른쪽", "$알수없음"), NORMAL.replace("방향", "다른"), NORMAL.replace("고름씨", "다른씨"), NORMAL.replace("選択型", "別型"), NORMAL.replace(":= {", ":={...}"), NORMAL.replace("$左.", "$左(값)."), NORMAL.replace("#!日本語", "#!한국어"), NORMAL.replace("#!日本語", "#!Quechua"), NORMAL.replace("#!日本語", "#!Unknown"), NORMAL.replace("#!日本語", ""), NORMAL.replace("방향:고름씨", "방향:고름씨 :={...}"),
    ];
    for source in cases { assert!(parse_ddl_wave3(&source, "direction.ddl").is_err(), "N case admitted: {source}"); }
}
