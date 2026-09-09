//! DDL Wave 1 frontdoor.
//!
//! This module accepts only the Owner-bound two-language, immutable-value
//! projection.  It is intentionally not a second general DDN parser and it
//! never creates an executable body.

use crate::ast::{
    CallableParamProjection, CallablePublicProjection, DdlCallableDocument,
    DdlCallableLanguageSection, DdlDocument, DdlExtension, ImmutablePublicValueProjection,
    LanguageSection, OmittedPayload, Span, DdlSumDocument, DdlSumLanguageSection,
    SumPublicProjection, OwnedBranchProjection,
};
use crate::lexer::{Lexer, TokenKind};

const KOREAN: DdlRegistryEntry = DdlRegistryEntry {
    header: "#!한국어",
    profile_identity: "language-profile:ko",
    localized_name: "원주율",
    localized_type: "셈수",
    definition_identity: "definition:math.pi",
    type_identity: "type:number",
};

const JAPANESE: DdlRegistryEntry = DdlRegistryEntry {
    header: "#!日本語",
    profile_identity: "language-profile:ja",
    localized_name: "円周率",
    localized_type: "数値",
    definition_identity: "definition:math.pi",
    type_identity: "type:number",
};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DdlRegistryEntry {
    pub header: &'static str,
    pub profile_identity: &'static str,
    pub localized_name: &'static str,
    pub localized_type: &'static str,
    pub definition_identity: &'static str,
    pub type_identity: &'static str,
}

const REGISTRY: [DdlRegistryEntry; 2] = [KOREAN, JAPANESE];

const CALLABLE_KOREAN: DdlCallableRegistryEntry = DdlCallableRegistryEntry {
    header: "#!한국어",
    profile_identity: "language-profile:ko",
    localized_name: "더하기",
    parameters: [
        DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.left", type_identity: "type:number", relation_identity: "relation:math.add.left", localized_name: "왼쪽", localized_type: "셈수", relation_surface: "을" },
        DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.right", type_identity: "type:number", relation_identity: "relation:math.add.right", localized_name: "오른쪽", localized_type: "셈수", relation_surface: "와" },
    ],
    localized_result_type: "셈수",
    definition_identity: "definition:math.add",
    result_type_identity: "type:number",
    callable_kind: "callable:pure",
};

const CALLABLE_JAPANESE: DdlCallableRegistryEntry = DdlCallableRegistryEntry {
    header: "#!日本語",
    profile_identity: "language-profile:ja",
    localized_name: "加算",
    parameters: [
        DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.left", type_identity: "type:number", relation_identity: "relation:math.add.left", localized_name: "左", localized_type: "数値", relation_surface: "を" },
        DdlCallableParamRegistryEntry { pin_identity: "param-pin:math.add.right", type_identity: "type:number", relation_identity: "relation:math.add.right", localized_name: "右", localized_type: "数値", relation_surface: "と" },
    ],
    localized_result_type: "数値",
    definition_identity: "definition:math.add",
    result_type_identity: "type:number",
    callable_kind: "callable:pure",
};

const CALLABLE_REGISTRY: [DdlCallableRegistryEntry; 2] = [CALLABLE_KOREAN, CALLABLE_JAPANESE];

const SUM_KOREAN: DdlSumRegistryEntry = DdlSumRegistryEntry {
    header: "#!한국어", profile_identity: "language-profile:ko", localized_name: "방향",
    localized_type: "고름씨", definition_identity: "DDL.TYPE.DIRECTION.R1",
    type_identity: "DDL.TYPE.DIRECTION.R1", branches: [("DDL.BRANCH.DIRECTION.LEFT.R1", "왼쪽"), ("DDL.BRANCH.DIRECTION.RIGHT.R1", "오른쪽")],
};
const SUM_JAPANESE: DdlSumRegistryEntry = DdlSumRegistryEntry {
    header: "#!日本語", profile_identity: "language-profile:ja", localized_name: "方向",
    localized_type: "選択型", definition_identity: "DDL.TYPE.DIRECTION.R1",
    type_identity: "DDL.TYPE.DIRECTION.R1", branches: [("DDL.BRANCH.DIRECTION.LEFT.R1", "左"), ("DDL.BRANCH.DIRECTION.RIGHT.R1", "右")],
};
const SUM_REGISTRY: [DdlSumRegistryEntry; 2] = [SUM_KOREAN, SUM_JAPANESE];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DdlSumRegistryEntry {
    pub header: &'static str, pub profile_identity: &'static str, pub localized_name: &'static str,
    pub localized_type: &'static str, pub definition_identity: &'static str, pub type_identity: &'static str,
    pub branches: [(&'static str, &'static str); 2],
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DdlSumWave3Context { entries: Vec<DdlSumRegistryEntry> }
impl DdlSumWave3Context {
    pub fn standard() -> Self { Self { entries: SUM_REGISTRY.to_vec() } }
    pub fn from_entries(entries: Vec<DdlSumRegistryEntry>) -> Self { Self { entries } }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DdlCallableParamRegistryEntry {
    pub pin_identity: &'static str,
    pub type_identity: &'static str,
    pub relation_identity: &'static str,
    pub localized_name: &'static str,
    pub localized_type: &'static str,
    pub relation_surface: &'static str,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DdlCallableRegistryEntry {
    pub header: &'static str,
    pub profile_identity: &'static str,
    pub localized_name: &'static str,
    pub parameters: [DdlCallableParamRegistryEntry; 2],
    pub localized_result_type: &'static str,
    pub definition_identity: &'static str,
    pub result_type_identity: &'static str,
    pub callable_kind: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DdlCallableWave2Context {
    entries: Vec<DdlCallableRegistryEntry>,
}

impl DdlCallableWave2Context {
    pub fn standard() -> Self { Self { entries: CALLABLE_REGISTRY.to_vec() } }
    pub fn from_entries(entries: Vec<DdlCallableRegistryEntry>) -> Self { Self { entries } }
}

/// Internal, version-bound registry context for the DDL Wave 1 parser.
///
/// This is deliberately a Rust-side product context, not a public DDL wire
/// or dynamic language-profile registry.  It lets the parser validate that
/// translated entries preserve their common definition and type identities.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DdlWave1Context {
    entries: Vec<DdlRegistryEntry>,
}

impl DdlWave1Context {
    pub fn standard() -> Self {
        Self {
            entries: REGISTRY.to_vec(),
        }
    }

    pub fn from_entries(entries: Vec<DdlRegistryEntry>) -> Self {
        Self { entries }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DdlError {
    pub code: &'static str,
    pub span: Span,
    pub message: String,
}

impl std::fmt::Display for DdlError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}: {}", self.code, self.message)
    }
}

impl std::error::Error for DdlError {}

/// Parses the exact Wave 1 DDL surface.  `file_path` has extension-admission
/// authority only; it is never stored as a semantic identity.
pub fn parse_ddl_wave1(source: &str, file_path: &str) -> Result<DdlDocument, DdlError> {
    parse_ddl_wave1_with_context(source, file_path, &DdlWave1Context::standard())
}

/// Parses a Wave 1 document against an explicit internal registry context.
/// Callers must supply the fixed versioned context; source text never creates
/// profile or semantic identities dynamically.
pub fn parse_ddl_wave1_with_context(
    source: &str,
    file_path: &str,
    context: &DdlWave1Context,
) -> Result<DdlDocument, DdlError> {
    let extension = parse_extension(file_path)?;
    let headers = scan_headers(source)?;
    if headers.len() != 2 {
        return Err(error(
            "E_DDL_SECTION_COUNT",
            Span::new(0, source.len()),
            "DDL Wave 1은 정확히 두 LanguageSection이 필요합니다",
        ));
    }

    let mut sections = Vec::with_capacity(2);
    for (index, header) in headers.iter().enumerate() {
        let content_end = headers
            .get(index + 1)
            .map_or(source.len(), |next| next.start);
        let entry = registry_entry(&context.entries, header.text).ok_or_else(|| {
            error(
                if matches!(header.text, "#!qu" | "#!Quechua") {
                    "E_DDL_GENERIC_QUECHUA_FORBIDDEN"
                } else {
                    "E_DDL_PROFILE_UNKNOWN"
                },
                Span::new(header.start, header.end),
                "등록되지 않았거나 일반화된 LanguageProfile header입니다",
            )
        })?;
        if sections.iter().any(|section: &LanguageSection| {
            section.language_profile_identity == entry.profile_identity
        }) {
            return Err(error(
                "E_DDL_PROFILE_DUPLICATE",
                Span::new(header.start, header.end),
                "같은 LanguageProfileIdentity section을 두 번 쓸 수 없습니다",
            ));
        }
        let projection = parse_projection(&source[header.end..content_end], header.end, entry)?;
        sections.push(LanguageSection {
            language_profile_identity: entry.profile_identity.to_owned(),
            header_span: Span::new(header.start, header.end),
            content_span: Span::new(header.end, content_end),
            projection,
        });
    }

    let first = &sections[0].projection;
    let second = &sections[1].projection;
    if first.definition_identity != second.definition_identity {
        return Err(error(
            "E_DDL_DEFINITION_IDENTITY_MISMATCH",
            second.declaration_span,
            "두 localized projection은 같은 DefinitionIdentity를 가리켜야 합니다",
        ));
    }
    if first.type_identity != second.type_identity {
        return Err(error(
            "E_DDL_TYPE_IDENTITY_MISMATCH",
            second.declaration_span,
            "두 localized projection은 같은 TypeIdentity를 가리켜야 합니다",
        ));
    }

    Ok(DdlDocument {
        extension,
        source_span: Span::new(0, source.len()),
        sections,
    })
}

/// Parses the fixed Wave 2 callable projection. This is an internal AST/canon
/// surface only: it neither creates a runtime body nor extends ordinary DDN.
pub fn parse_ddl_wave2(source: &str, file_path: &str) -> Result<DdlCallableDocument, DdlError> {
    parse_ddl_wave2_with_context(source, file_path, &DdlCallableWave2Context::standard())
}

pub fn parse_ddl_wave2_with_context(
    source: &str,
    file_path: &str,
    context: &DdlCallableWave2Context,
) -> Result<DdlCallableDocument, DdlError> {
    let extension = parse_extension(file_path)?;
    let headers = scan_headers(source)?;
    if headers.len() != 2 {
        return Err(error("E_DDL_SECTION_COUNT", Span::new(0, source.len()), "DDL Wave 2는 정확히 두 LanguageSection이 필요합니다"));
    }
    let mut sections = Vec::with_capacity(2);
    for (index, header) in headers.iter().enumerate() {
        let content_end = headers.get(index + 1).map_or(source.len(), |next| next.start);
        let entry = context.entries.iter().find(|entry| entry.header == header.text).ok_or_else(|| {
            error(if matches!(header.text, "#!qu" | "#!Quechua") { "E_DDL_GENERIC_QUECHUA_FORBIDDEN" } else { "E_DDL_PROFILE_UNKNOWN" }, Span::new(header.start, header.end), "등록되지 않았거나 일반화된 LanguageProfile header입니다")
        })?;
        if sections.iter().any(|section: &DdlCallableLanguageSection| section.language_profile_identity == entry.profile_identity) {
            return Err(error("E_DDL_PROFILE_DUPLICATE", Span::new(header.start, header.end), "같은 LanguageProfileIdentity section을 두 번 쓸 수 없습니다"));
        }
        let projection = parse_callable_projection(&source[header.end..content_end], header.end, entry)?;
        sections.push(DdlCallableLanguageSection {
            language_profile_identity: entry.profile_identity.to_owned(),
            header_span: Span::new(header.start, header.end),
            content_span: Span::new(header.end, content_end),
            projection,
        });
    }
    validate_callable_identity_binding(&sections)?;
    Ok(DdlCallableDocument { extension, source_span: Span::new(0, source.len()), sections })
}

fn parse_callable_projection(
    content: &str,
    content_start: usize,
    entry: &DdlCallableRegistryEntry,
) -> Result<CallablePublicProjection, DdlError> {
    let declaration = content.trim();
    let leading = content.find(declaration).unwrap_or(0);
    let span = Span::new(content_start + leading, content_start + leading + declaration.len());
    if declaration.is_empty() || content.lines().filter(|line| !line.trim().is_empty()).count() != 1 {
        return Err(error("E_DDL_PROJECTION_COUNT", Span::new(content_start, content_start + content.len()), "Wave 2 section에는 callable projection 하나만 허용합니다"));
    }
    let params = entry.parameters.iter().map(|param| format!("{}:{}[{}]", param.localized_name, param.localized_type, param.relation_surface)).collect::<Vec<_>>().join(", ");
    let expected = format!("{}({params}) -> {} :={{...}}.", entry.localized_name, entry.localized_result_type);
    if declaration != expected {
        return Err(error("E_DDL_OMITTED_VALUE_SHAPE", span, "DDL Wave 2 callable 표기는 registry-bound exact signature와 `:={...}` body omission이어야 합니다"));
    }
    Ok(CallablePublicProjection {
        definition_identity: entry.definition_identity.to_owned(),
        callable_kind: entry.callable_kind.to_owned(),
        localized_name: entry.localized_name.to_owned(),
        parameters: entry.parameters.iter().map(|param| CallableParamProjection {
            param_pin_identity: param.pin_identity.to_owned(), type_identity: param.type_identity.to_owned(), relation_identity: param.relation_identity.to_owned(), localized_name: param.localized_name.to_owned(), localized_type: param.localized_type.to_owned(), relation_surface: param.relation_surface.to_owned(),
        }).collect(),
        localized_result_type: entry.localized_result_type.to_owned(),
        result_type_identity: entry.result_type_identity.to_owned(),
        declaration_span: span,
        omitted_payload: OmittedPayload::CallableBody,
    })
}

fn validate_callable_identity_binding(sections: &[DdlCallableLanguageSection]) -> Result<(), DdlError> {
    let first = &sections[0].projection;
    let second = &sections[1].projection;
    if first.definition_identity != second.definition_identity || first.callable_kind != second.callable_kind {
        return Err(error("E_DDL_DEFINITION_IDENTITY_MISMATCH", second.declaration_span, "두 callable projection은 같은 DefinitionIdentity와 callable kind를 가리켜야 합니다"));
    }
    if first.result_type_identity != second.result_type_identity || first.parameters.len() != 2 || second.parameters.len() != 2 {
        return Err(error("E_DDL_TYPE_IDENTITY_MISMATCH", second.declaration_span, "결과 TypeIdentity와 exact two ParamPin이 필요합니다"));
    }
    for (left, right) in first.parameters.iter().zip(&second.parameters) {
        if left.param_pin_identity != right.param_pin_identity || left.type_identity != right.type_identity || left.relation_identity != right.relation_identity || left.relation_surface.is_empty() || right.relation_surface.is_empty() {
            return Err(error("E_DDL_DEFINITION_IDENTITY_MISMATCH", second.declaration_span, "ParamPinIdentity, TypeIdentity, relation surface가 exact order로 일치해야 합니다"));
        }
    }
    if first.parameters[0].param_pin_identity == first.parameters[1].param_pin_identity {
        return Err(error("E_DDL_DEFINITION_IDENTITY_MISMATCH", first.declaration_span, "중복 ParamPinIdentity는 허용하지 않습니다"));
    }
    Ok(())
}

/// Parses the Owner-bound, non-executable Wave 3 nominal sum projection.
pub fn parse_ddl_wave3(source: &str, file_path: &str) -> Result<DdlSumDocument, DdlError> {
    parse_ddl_wave3_with_context(source, file_path, &DdlSumWave3Context::standard())
}

pub fn parse_ddl_wave3_with_context(source: &str, file_path: &str, context: &DdlSumWave3Context) -> Result<DdlSumDocument, DdlError> {
    let extension = parse_extension(file_path)?;
    let headers = scan_headers(source)?;
    if headers.len() != 2 { return Err(error("E_DDL_SECTION_COUNT", Span::new(0, source.len()), "DDL Wave 3은 정확히 두 LanguageSection이 필요합니다")); }
    let mut sections = Vec::with_capacity(2);
    for (index, header) in headers.iter().enumerate() {
        let content_end = headers.get(index + 1).map_or(source.len(), |next| next.start);
        let entry = context.entries.iter().find(|entry| entry.header == header.text).ok_or_else(|| error(if matches!(header.text, "#!qu" | "#!Quechua") { "E_DDL_GENERIC_QUECHUA_FORBIDDEN" } else { "E_DDL_PROFILE_UNKNOWN" }, Span::new(header.start, header.end), "등록되지 않은 LanguageProfile header입니다"))?;
        if sections.iter().any(|section: &DdlSumLanguageSection| section.language_profile_identity == entry.profile_identity) { return Err(error("E_DDL_PROFILE_DUPLICATE", Span::new(header.start, header.end), "같은 LanguageProfileIdentity section을 두 번 쓸 수 없습니다")); }
        let content = &source[header.end..content_end];
        let declaration = content.trim(); let leading = content.find(declaration).unwrap_or(0);
        let span = Span::new(header.end + leading, header.end + leading + declaration.len());
        let expected = format!("{}:{} := {{\n    ${}.\n    ${}.\n}}.", entry.localized_name, entry.localized_type, entry.branches[0].1, entry.branches[1].1);
        let reversed = format!("{}:{} := {{\n    ${}.\n    ${}.\n}}.", entry.localized_name, entry.localized_type, entry.branches[1].1, entry.branches[0].1);
        if declaration != expected && declaration != reversed { return Err(error("E_DDL_SUM_SHAPE", span, "registry-bound sum schema와 exact two OwnedBranch가 필요합니다")); }
        let names = if declaration == reversed { [entry.branches[1], entry.branches[0]] } else { entry.branches };
        sections.push(DdlSumLanguageSection { language_profile_identity: entry.profile_identity.to_owned(), header_span: Span::new(header.start, header.end), content_span: Span::new(header.end, content_end), projection: SumPublicProjection { definition_identity: entry.definition_identity.to_owned(), type_identity: entry.type_identity.to_owned(), sum_kind: "sum:nominal".to_string(), localized_name: entry.localized_name.to_owned(), localized_type: entry.localized_type.to_owned(), branches: names.into_iter().map(|(identity, name)| OwnedBranchProjection { owned_branch_identity: identity.to_owned(), localized_name: name.to_owned() }).collect(), declaration_span: span } });
    }
    let first = &sections[0].projection; let second = &sections[1].projection;
    if first.definition_identity != second.definition_identity { return Err(error("E_DDL_DEFINITION_IDENTITY_MISMATCH", second.declaration_span, "DefinitionIdentity가 일치해야 합니다")); }
    if first.type_identity != second.type_identity || first.sum_kind != second.sum_kind { return Err(error("E_DDL_TYPE_IDENTITY_MISMATCH", second.declaration_span, "TypeIdentity와 sum kind가 일치해야 합니다")); }
    let mut left = first.branches.iter().map(|branch| branch.owned_branch_identity.as_str()).collect::<Vec<_>>(); let mut right = second.branches.iter().map(|branch| branch.owned_branch_identity.as_str()).collect::<Vec<_>>(); left.sort(); right.sort();
    if left != right || left.len() != 2 || left[0] == left[1] { return Err(error("E_DDL_OWNED_BRANCH_IDENTITY_MISMATCH", second.declaration_span, "exact complete OwnedBranchIdentity set이 필요합니다")); }
    for section in &sections {
        let expected = SUM_REGISTRY.iter().find(|entry| entry.profile_identity == section.language_profile_identity).expect("fixed profile");
        for (identity, name) in expected.branches {
            let actual = section.projection.branches.iter().find(|branch| branch.localized_name == name).map(|branch| branch.owned_branch_identity.as_str());
            if actual != Some(identity) { return Err(error("E_DDL_OWNED_BRANCH_IDENTITY_MISMATCH", section.projection.declaration_span, "localized branch와 OwnedBranchIdentity 결속이 일치해야 합니다")); }
        }
    }
    Ok(DdlSumDocument { extension, source_span: Span::new(0, source.len()), sections })
}

fn parse_extension(file_path: &str) -> Result<DdlExtension, DdlError> {
    if file_path.ends_with(".ddl") {
        Ok(DdlExtension::Ddl)
    } else if file_path.ends_with(".옮김") {
        Ok(DdlExtension::Olgim)
    } else {
        Err(error(
            "E_DDL_EXTENSION_UNSUPPORTED",
            Span::new(0, 0),
            "DDL Wave 1은 .ddl 또는 .옮김 extension만 허용합니다",
        ))
    }
}

fn registry_entry<'a>(
    entries: &'a [DdlRegistryEntry],
    header: &str,
) -> Option<&'a DdlRegistryEntry> {
    entries.iter().find(|entry| entry.header == header)
}

#[derive(Debug, Clone, Copy)]
struct Header<'a> {
    start: usize,
    end: usize,
    text: &'a str,
}

/// Finds only raw top-level line-start headers.  Quoted, line-commented,
/// block-commented, and nested `#!` bytes are ordinary section content.
fn scan_headers(source: &str) -> Result<Vec<Header<'_>>, DdlError> {
    let mut headers = Vec::new();
    let mut offset = 0;
    let mut depth = 0_i32;
    let mut in_string = false;
    let mut escape = false;
    let mut in_block_comment = false;

    for line_with_end in source.split_inclusive('\n') {
        let line = line_with_end.strip_suffix('\n').unwrap_or(line_with_end);
        let line = line.strip_suffix('\r').unwrap_or(line);
        let eligible = depth == 0 && !in_string && !in_block_comment;
        if eligible && line.starts_with("#!") {
            if offset != 0 && headers.is_empty() {
                return Err(error(
                    "E_DDL_FIRST_HEADER_NOT_BYTE_ZERO",
                    Span::new(offset, offset + line.len()),
                    "첫 DDL header는 raw byte zero에서 시작해야 합니다",
                ));
            }
            // Exact registry matching also rejects whitespace and trailing text.
            headers.push(Header {
                start: offset,
                end: offset + line.len(),
                text: line,
            });
        }
        advance_lexical_depth(
            line,
            &mut depth,
            &mut in_string,
            &mut escape,
            &mut in_block_comment,
        );
        offset += line_with_end.len();
    }

    if !source.is_empty() && !source.ends_with('\n') {
        // `split_inclusive` already included the final unterminated line.
    }
    if in_string || in_block_comment || depth != 0 {
        return Err(error(
            "E_DDL_SOURCE_UNBALANCED",
            Span::new(0, source.len()),
            "DDL section boundary를 판정할 수 없는 미닫힌 문자열·주석·블록이 있습니다",
        ));
    }
    if headers.first().map(|header| header.start) != Some(0) {
        return Err(error(
            "E_DDL_FIRST_HEADER_REQUIRED",
            Span::new(0, source.len().min(1)),
            "DDL 문서는 byte zero의 exact LanguageProfile header로 시작해야 합니다",
        ));
    }
    Ok(headers)
}

fn advance_lexical_depth(
    line: &str,
    depth: &mut i32,
    in_string: &mut bool,
    escape: &mut bool,
    in_block_comment: &mut bool,
) {
    let bytes = line.as_bytes();
    let mut index = 0;
    while index < bytes.len() {
        if *in_block_comment {
            if bytes[index..].starts_with(b"*/") {
                *in_block_comment = false;
                index += 2;
            } else {
                index += 1;
            }
            continue;
        }
        if *in_string {
            if *escape {
                *escape = false;
            } else if bytes[index] == b'\\' {
                *escape = true;
            } else if bytes[index] == b'"' {
                *in_string = false;
            }
            index += 1;
            continue;
        }
        if bytes[index..].starts_with(b"//") {
            break;
        }
        if bytes[index..].starts_with(b"/*") {
            *in_block_comment = true;
            index += 2;
            continue;
        }
        match bytes[index] {
            b'"' => *in_string = true,
            b'{' => *depth += 1,
            b'}' => *depth -= 1,
            _ => {}
        }
        index += 1;
    }
}

fn parse_projection(
    content: &str,
    content_start: usize,
    entry: &DdlRegistryEntry,
) -> Result<ImmutablePublicValueProjection, DdlError> {
    let declaration = content.trim();
    if declaration.is_empty() {
        return Err(error(
            "E_DDL_PROJECTION_MISSING",
            Span::new(content_start, content_start + content.len()),
            "각 LanguageSection에는 immutable public value projection 하나가 필요합니다",
        ));
    }
    if content
        .lines()
        .filter(|line| !line.trim().is_empty())
        .count()
        != 1
    {
        return Err(error(
            "E_DDL_PROJECTION_COUNT",
            Span::new(content_start, content_start + content.len()),
            "Wave 1 section에는 projection 하나만 허용합니다",
        ));
    }
    let leading = content.find(declaration).unwrap_or(0);
    let declaration_span = Span::new(
        content_start + leading,
        content_start + leading + declaration.len(),
    );
    let exact = format!(
        "{}:{} :={{...}}.",
        entry.localized_name, entry.localized_type
    );
    if declaration != exact {
        return Err(error(
            "E_DDL_OMITTED_VALUE_SHAPE",
            declaration_span,
            "DDL-only immutable value 표기는 exact `이름:타입 :={...}.`이어야 합니다",
        ));
    }
    validate_declaration_tokens(declaration, declaration_span, entry)?;
    Ok(ImmutablePublicValueProjection {
        definition_identity: entry.definition_identity.to_owned(),
        type_identity: entry.type_identity.to_owned(),
        localized_name: entry.localized_name.to_owned(),
        localized_type: entry.localized_type.to_owned(),
        declaration_span,
        omitted_payload: OmittedPayload::ValueInitializer,
    })
}

/// Reuses the shared lexer for the Korean declaration shell.  The existing
/// lexer has no Japanese identifier admission, so the Owner-bound Japanese
/// Wave 1 surface is accepted only through its exact registry literal; this
/// is deliberately not generalized parsing or a fallback language mode.
fn validate_declaration_tokens(
    source: &str,
    span: Span,
    entry: &DdlRegistryEntry,
) -> Result<(), DdlError> {
    if entry.profile_identity == JAPANESE.profile_identity {
        return Ok(());
    }
    let tokens = Lexer::new(source)
        .tokenize()
        .map_err(|lex| error("E_DDL_DECLARATION_LEX", span, lex.message))?;
    let expected = [
        matches!(&tokens[0].kind, TokenKind::Ident(_)),
        matches!(tokens[1].kind, TokenKind::Colon),
        matches!(&tokens[2].kind, TokenKind::Ident(_)),
        matches!(tokens[3].kind, TokenKind::Define),
        matches!(tokens[4].kind, TokenKind::LBrace),
        matches!(tokens[5].kind, TokenKind::DotDot),
        matches!(tokens[6].kind, TokenKind::Dot),
        matches!(tokens[7].kind, TokenKind::RBrace),
        matches!(tokens[8].kind, TokenKind::Dot),
        matches!(tokens[9].kind, TokenKind::Eof),
    ];
    if tokens.len() != expected.len() || expected.iter().any(|valid| !valid) {
        return Err(error(
            "E_DDL_OMITTED_VALUE_TOKENS",
            span,
            "DDL omission은 exact ASCII `:={...}` token sequence여야 합니다",
        ));
    }
    Ok(())
}

fn error(code: &'static str, span: Span, message: impl Into<String>) -> DdlError {
    DdlError {
        code,
        span,
        message: message.into(),
    }
}
