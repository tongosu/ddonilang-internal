use ddonirang_lang::{
    canonicalize, normalize, parse, parse_v25, parse_v25_and_normalize, NormalizationLevel,
    SourceEpoch, Stmt, TopLevelItem,
};

const PUBLIC_SAFE_POSITIVE: &str = r#"검산:움직씨 := {
    합계:수 := 4.
    합계 <- 7.
    합계 보여주기.
}
"#;
const PUBLIC_SAFE_OLD_EQUALS: &str = "검산:움직씨 = {\n}\n";
const PUBLIC_SAFE_BINDING_AS_DEFINITION: &str = r#"검산:움직씨 := {
    채비: { 합계:수 <- 4. }.
}
"#;

fn statement_categories(source: &str) -> (usize, usize) {
    let program = parse_v25(source, "pc01.ddn").expect("V25 source must parse");
    assert_eq!(program.source_epoch, SourceEpoch::V25);
    let TopLevelItem::SeedDef(seed) = &program.items[0];
    let body = seed.body.as_ref().expect("seed body");
    let definitions = body
        .stmts
        .iter()
        .filter(|stmt| matches!(stmt, Stmt::Definition { .. }))
        .count();
    let bindings = body
        .stmts
        .iter()
        .filter(|stmt| matches!(stmt, Stmt::Mutate { .. }))
        .count();
    (definitions, bindings)
}

#[test]
fn v25_definition_binding_pack_matches_oracle() {
    assert_eq!(statement_categories(PUBLIC_SAFE_POSITIVE), (1, 1));
    for (case, source, diagnostic) in [
        (
            "old-equals.ddn",
            PUBLIC_SAFE_OLD_EQUALS,
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
        ),
        (
            "binding-as-definition.ddn",
            PUBLIC_SAFE_BINDING_AS_DEFINITION,
            "E_V25_DEFINITION_MIGRATION_REQUIRED",
        ),
    ] {
        let error = parse_v25(source, case).expect_err("case must fail closed");
        assert!(
            error.message.contains(diagnostic),
            "unexpected diagnostic for {case}: {}",
            error.message
        );
    }
}

#[test]
fn v25_parse_canon_parse_preserves_categories_and_symbols() {
    let before = statement_categories(PUBLIC_SAFE_POSITIVE);
    let mut program = parse_v25(PUBLIC_SAFE_POSITIVE, "positive.ddn").expect("parse");
    canonicalize(&mut program).expect("canonicalize");
    let canonical = normalize(&program, NormalizationLevel::N1);

    assert!(canonical.contains("검산:움직씨 :="));
    assert!(canonical.contains("합계:수 := 4."));
    assert!(canonical.contains("합계 <- 7."));
    assert!(!canonical.contains("합계:수 <- 4."));
    assert_eq!(statement_categories(&canonical), before);
}

#[test]
fn v25_normalization_accepts_direct_definition_and_rejects_legacy_chaebi() {
    let canonical =
        parse_v25_and_normalize(PUBLIC_SAFE_POSITIVE, "positive.ddn", NormalizationLevel::N1)
            .expect("current V25 direct definitions normalize");
    assert!(canonical.contains("합계:수 := 4."));
    assert!(!canonical.contains("채비"));
    parse_v25(&canonical, "positive.canon.ddn").expect("canonical output remains V25 source");

    for source in [
        local_source("    채비 {\n        상수:수 = 1.\n    }."),
        local_source("    채비 {\n        상수:수 := 1.\n    }."),
        local_source("    값:수 := 1.\n    채비 {\n        상수:수 = 1.\n    }."),
    ] {
        let error = parse_v25_and_normalize(&source, "legacy_chaebi.ddn", NormalizationLevel::N1)
            .expect_err("legacy chaebi must not normalize as current V25");
        assert_eq!(error.code(), DEFINITION_MIGRATION_DIAGNOSTIC);
    }
}

#[test]
fn pre_v25_reader_is_explicitly_separate_from_v25_reader() {
    let legacy = parse(PUBLIC_SAFE_OLD_EQUALS, "legacy.ddn").expect("historical pre-V25 reader");
    assert_eq!(legacy.source_epoch, SourceEpoch::PreV25);

    let error =
        parse_v25(PUBLIC_SAFE_OLD_EQUALS, "v25.ddn").expect_err("V25 must reject silent alias");
    assert!(error
        .message
        .contains("E_V25_DEFINITION_MIGRATION_REQUIRED"));
}

const DEFINITION_MIGRATION_DIAGNOSTIC: &str = "E_V25_DEFINITION_MIGRATION_REQUIRED";

fn local_source(statements: &str) -> String {
    format!("계산:움직씨 := {{\n{statements}\n}}\n")
}

fn assert_v25_migration_required(source: &str) {
    let error =
        parse_v25(source, "typed_local_equals.ddn").expect_err("legacy equals must fail closed");
    assert_eq!(error.code(), DEFINITION_MIGRATION_DIAGNOSTIC);
    assert!(error.message.starts_with(DEFINITION_MIGRATION_DIAGNOSTIC));
    assert!(
        error.span.start < error.span.end,
        "diagnostic span must be present"
    );
}

#[test]
fn v25_typed_local_legacy_equals_targeted_matrix() {
    // typed-local, untyped-local, and top-level old Definition surfaces.
    assert_v25_migration_required(&local_source("    값:수 = 1."));
    assert_v25_migration_required(&local_source("    값 = 1."));
    assert_v25_migration_required("계산:움직씨 = {\n}\n");

    // Valid Definition and Binding remain distinct, including redefinition.
    let valid = local_source("    값:수 := 1.\n    값 <- 2.");
    assert_eq!(statement_categories(&valid), (1, 1));
    let redefined = local_source("    값:수 := 1.\n    값:수 := 2.");
    assert_eq!(statement_categories(&redefined), (2, 0));

    // Any `채비 {}` block is legacy in current V25, regardless of its item form.
    assert_v25_migration_required(&local_source("    채비 {\n        상수:수 = 1.\n    }."));
    assert_v25_migration_required(&local_source("    채비 {\n        상수:수 := 1.\n    }."));

    // Full type parsing precedes the Equals decision; no fixed-token lookahead.
    assert_v25_migration_required(&local_source("    표:(글, 수)짝맞춤 = 1."));
    assert_v25_migration_required(&local_source("    변환:(수, 글) --> 수 = 1."));

    // A malformed annotation remains a type error and is not relabeled.
    let malformed = parse_v25(&local_source("    값:(수, 글) = 1."), "malformed_type.ddn")
        .expect_err("malformed type must fail closed");
    assert_ne!(malformed.code(), DEFINITION_MIGRATION_DIAGNOSTIC);
    assert!(!malformed.message.contains(DEFINITION_MIGRATION_DIAGNOSTIC));
}

#[test]
fn v25_strict_chaebi_rejection_does_not_match_string_contents() {
    let source = local_source("    메모:글 := \"채비\".");
    assert_eq!(statement_categories(&source), (1, 0));
}
