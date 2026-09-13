use ddonirang_lang::{
    canonicalize, normalize, parse_v25, ExprKind, NormalizationLevel, Stmt, TopLevelItem,
};

const SOURCE: &str = r#"선택:고름씨 := {
    선택.$예.
    선택.$수(값:셈수).
}.

값 <- 선택.$수(값=3).

값에 따라 {
    선택.$예이면 { 보여주기("예"). }.
    선택.$수(값)이면 { 보여주기(값). }.
    아니면 { 보여주기("기타"). }.
}.
"#;

#[test]
fn typed_sum_and_statement_match_keep_distinct_shared_ast_categories() {
    let program = parse_v25(SOURCE, "typed_sum_match.ddn").expect("current source parses");
    assert!(matches!(program.root_stmts[0], Stmt::SumDefinition { .. }));
    let Stmt::Mutate { value, .. } = &program.root_stmts[1] else {
        panic!("second statement must construct a typed branch value");
    };
    assert!(matches!(value.kind, ExprKind::SumBranchValue { .. }));
    let Stmt::SumMatch { arms, default_body, .. } = &program.root_stmts[2] else {
        panic!("third statement must be a statement-only typed match");
    };
    assert_eq!(arms.len(), 2);
    assert!(default_body.is_some());
}

#[test]
fn typed_sum_match_canon_round_trips_with_lf_and_exact_qualification() {
    let mut program = parse_v25(SOURCE, "typed_sum_match.ddn").expect("parse");
    canonicalize(&mut program).expect("canonicalize");
    let once = normalize(&program, NormalizationLevel::N1);
    assert!(!once.contains('\r'));
    assert!(once.contains("$수(값:셈수)"));
    assert!(once.contains("선택.$수(값=3)"));

    let mut reparsed = parse_v25(&once, "typed_sum_match.ddn").expect("reparse");
    canonicalize(&mut reparsed).expect("recanonicalize");
    let twice = normalize(&reparsed, NormalizationLevel::N1);
    assert_eq!(once, twice);
}

#[test]
fn typed_sum_match_rejects_fuzzy_or_incomplete_forms_and_keeps_dollar_in_literals() {
    for source in [
        "선택:고름씨 := { $예. $예. }.\n",
        "값 <- $예.\n",
        "선택:고름씨 := { $예. $수(값:셈수). }. 값 <- 선택.$예. 값에 따라 { 선택.$예이면 { 보여주기(\"예\"). }. }.\n",
        "선택:고름씨 := { $예. }. 값 <- 선택.$예. 값에 따라 { 선택.$예이면 { 보여주기(\"예\"). }. 아니면 { 보여주기(\"기타\"). }. 아니면 { 보여주기(\"중복\"). }. }.\n",
        "선택:고름씨 := { $예. }. 값 <- 선택.$예. 값에 따라 { 다른.$예이면 { 보여주기(\"예\"). }. }.\n",
    ] {
        assert!(parse_v25(source, "typed_sum_match_negative.ddn").is_err());
    }

    let literal_source = "검산:움직씨 := { 보여주기(\"$는 문자열입니다\"). }\n";
    let program = parse_v25(literal_source, "typed_sum_literal.ddn")
        .expect("a dollar inside a string remains ordinary text");
    let TopLevelItem::SeedDef(seed) = &program.items[0];
    assert!(matches!(seed.body.as_ref().unwrap().stmts[0], Stmt::Show { .. }));
}
