use super::document_store::DocumentSnapshot;
use super::position::{byte_range_to_lsp_range, ByteRange, PositionEncoding};
use ddonirang_lang::stdlib::minimal_stdlib_sigs;
use ddonirang_lang::{parse_v25, Lexer, SeedKind, Token, TokenKind, TopLevelItem};
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;

pub const MAX_TOKEN_DATA: usize = 100_000;

pub const LEGEND_TOKEN_TYPES: &[&str] = &[
    "function",
    "type",
    "variable",
    "parameter",
    "keyword",
    "string",
    "number",
    "operator",
    "atom",
    "josa",
];

pub const LEGEND_TOKEN_MODIFIERS: &[&str] = &["declaration", "defaultLibrary"];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SemanticTokensResolution {
    pub document_version: i64,
    pub snapshot_identity: String,
    pub result_id: String,
    pub data: Vec<u32>,
    pub source_profile: &'static str,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SemanticTokensEdit {
    pub start: u32,
    pub delete_count: u32,
    pub data: Vec<u32>,
}

pub fn semantic_tokens_snapshot(
    snapshot: &DocumentSnapshot,
    encoding: PositionEncoding,
) -> Result<SemanticTokensResolution, SemanticTokensError> {
    let source = snapshot
        .text()
        .map_err(|_| SemanticTokensError::InvalidUtf8)?;
    if snapshot.language_id != "ddn" {
        return Ok(empty_resolution(snapshot));
    }
    let tokens = match Lexer::new(source).tokenize() {
        Ok(tokens) => tokens,
        Err(_) => return Ok(empty_resolution(snapshot)),
    };
    let Ok(program) = parse_v25(source, &snapshot.uri) else {
        return lexical_fallback_resolution(snapshot, source, &tokens, encoding);
    };
    let local_names = program
        .items
        .iter()
        .filter_map(|item| match item {
            TopLevelItem::SeedDef(seed) => Some(seed.canonical_name.clone()),
        })
        .collect::<BTreeSet<_>>();
    let declaration_ranges = program
        .items
        .iter()
        .filter_map(|item| {
            let TopLevelItem::SeedDef(seed) = item;
            super::symbol::declaration_range(&tokens, seed)
        })
        .collect::<Vec<_>>();
    let type_definition_ranges = program
        .items
        .iter()
        .filter_map(|item| {
            let TopLevelItem::SeedDef(seed) = item;
            matches!(seed.seed_kind, SeedKind::Imeumssi)
                .then(|| super::symbol::declaration_range(&tokens, seed))
                .flatten()
        })
        .collect::<Vec<_>>();
    let parameter_declaration_ranges = program
        .items
        .iter()
        .flat_map(|item| {
            let TopLevelItem::SeedDef(seed) = item;
            seed.params.iter().filter_map(|param| {
                tokens
                    .iter()
                    .find(|token| {
                        token.span.start >= param.span.start
                            && token.span.end <= param.span.end
                            && token.raw == param.pin_name
                    })
                    .map(|token| ByteRange {
                        start: token.span.start,
                        end: token.span.end,
                    })
            })
        })
        .collect::<Vec<_>>();
    let parameter_names = program
        .items
        .iter()
        .flat_map(|item| match item {
            TopLevelItem::SeedDef(seed) => seed.params.iter().map(|param| param.pin_name.clone()),
        })
        .collect::<BTreeSet<_>>();
    let stdlib_names = minimal_stdlib_sigs()
        .into_iter()
        .map(|signature| signature.name.to_string())
        .collect::<BTreeSet<_>>();
    let data = encode_token_data(source, &tokens, encoding, |token, previous| {
        token_classification(
            token,
            previous,
            &local_names,
            &parameter_names,
            &stdlib_names,
            &declaration_ranges,
            &type_definition_ranges,
            &parameter_declaration_ranges,
        )
    })?;
    Ok(data
        .map(|data| resolution_from_data(snapshot, data))
        .unwrap_or_else(|| empty_resolution(snapshot)))
}

pub fn semantic_tokens_delta(previous: &[u32], current: &[u32]) -> SemanticTokensEdit {
    let prefix = previous
        .iter()
        .zip(current)
        .take_while(|(left, right)| left == right)
        .count();
    let suffix = previous[prefix..]
        .iter()
        .rev()
        .zip(current[prefix..].iter().rev())
        .take_while(|(left, right)| left == right)
        .count();
    let previous_end = previous.len().saturating_sub(suffix);
    let current_end = current.len().saturating_sub(suffix);
    SemanticTokensEdit {
        start: prefix as u32,
        delete_count: previous_end.saturating_sub(prefix) as u32,
        data: current[prefix..current_end].to_vec(),
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SemanticTokensError {
    InvalidUtf8,
    InvalidPosition(super::position::PositionError),
}

impl std::fmt::Display for SemanticTokensError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::InvalidUtf8 => f.write_str("semantic tokens source가 UTF-8이 아닙니다"),
            Self::InvalidPosition(error) => {
                write!(f, "semantic tokens position이 잘못되었습니다: {error}")
            }
        }
    }
}

impl std::error::Error for SemanticTokensError {}

fn empty_resolution(snapshot: &DocumentSnapshot) -> SemanticTokensResolution {
    resolution_from_data(snapshot, Vec::new())
}

fn resolution_from_data(snapshot: &DocumentSnapshot, data: Vec<u32>) -> SemanticTokensResolution {
    SemanticTokensResolution {
        document_version: snapshot.version,
        snapshot_identity: snapshot.identity.as_str().to_string(),
        result_id: result_id(snapshot, &data),
        data,
        source_profile: "v25",
    }
}

fn lexical_fallback_resolution(
    snapshot: &DocumentSnapshot,
    source: &str,
    tokens: &[Token],
    encoding: PositionEncoding,
) -> Result<SemanticTokensResolution, SemanticTokensError> {
    let data = encode_token_data(source, tokens, encoding, |token, _| {
        lexical_token_classification(token)
    })?;
    Ok(data
        .map(|data| resolution_from_data(snapshot, data))
        .unwrap_or_else(|| empty_resolution(snapshot)))
}

fn encode_token_data<F>(
    source: &str,
    tokens: &[Token],
    encoding: PositionEncoding,
    mut classify: F,
) -> Result<Option<Vec<u32>>, SemanticTokensError>
where
    F: FnMut(&Token, Option<&Token>) -> Option<TokenClassification>,
{
    let mut data = Vec::new();
    let mut previous_line = 0;
    let mut previous_start = 0;
    let mut previous: Option<&Token> = None;
    for token in tokens {
        let Some(classification) = classify(token, previous) else {
            previous = Some(token);
            continue;
        };
        let range = byte_range_to_lsp_range(
            source,
            super::position::ByteRange {
                start: token.span.start,
                end: token.span.end,
            },
            encoding,
        )
        .map_err(SemanticTokensError::InvalidPosition)?;
        if range.start.line != range.end.line || range.end.character <= range.start.character {
            previous = Some(token);
            continue;
        }
        let delta_line = range.start.line.saturating_sub(previous_line);
        let delta_start = if delta_line == 0 {
            range.start.character.saturating_sub(previous_start)
        } else {
            range.start.character
        };
        data.extend([
            delta_line,
            delta_start,
            range.end.character - range.start.character,
            classification.token_type,
            classification.modifiers,
        ]);
        if data.len() > MAX_TOKEN_DATA {
            return Ok(None);
        }
        previous_line = range.start.line;
        previous_start = range.start.character;
        previous = Some(token);
    }
    Ok(Some(data))
}

fn result_id(snapshot: &DocumentSnapshot, data: &[u32]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(b"ddonirang.lsp9.semantic-tokens.v2\0");
    hasher.update((snapshot.uri.len() as u64).to_le_bytes());
    hasher.update(snapshot.uri.as_bytes());
    hasher.update(snapshot.version.to_le_bytes());
    hasher.update(snapshot.identity.as_str().as_bytes());
    hasher.update((data.len() as u64).to_le_bytes());
    for value in data {
        hasher.update(value.to_le_bytes());
    }
    format!("sha256:{:x}", hasher.finalize())
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct TokenClassification {
    token_type: u32,
    modifiers: u32,
}

fn lexical_token_classification(token: &Token) -> Option<TokenClassification> {
    let token_type = if matches!(token.kind, TokenKind::StringLit(_)) {
        5
    } else if matches!(token.kind, TokenKind::Integer(_) | TokenKind::Float(_)) {
        6
    } else if matches!(
        token.kind,
        TokenKind::KwImeumssi
            | TokenKind::KwUmjikssi
            | TokenKind::KwGallaessi
            | TokenKind::KwRelationssi
            | TokenKind::KwValueFunc
            | TokenKind::KwSam
            | TokenKind::KwHeureumssi
            | TokenKind::KwIeumssi
            | TokenKind::KwSemssi
            | TokenKind::KwManyak
            | TokenKind::KwIramyeon
            | TokenKind::KwIlttae
            | TokenKind::KwAniramyeon
            | TokenKind::KwBanbok
            | TokenKind::KwButeo
            | TokenKind::KwKkaji
            | TokenKind::KwDongan
            | TokenKind::KwDaehae
            | TokenKind::KwMeomchugi
            | TokenKind::KwGeonneottwigi
            | TokenKind::KwDollyeojwo
            | TokenKind::KwTolabogi
            | TokenKind::KwAllyeo
            | TokenKind::KwHaebogo
            | TokenKind::KwGoreugi
            | TokenKind::KwMajeumyeon
            | TokenKind::KwJeonjehae
            | TokenKind::KwBojanghago
            | TokenKind::KwHaeseo
            | TokenKind::KwNeuljikeobogo
            | TokenKind::KwBoyeojugi
            | TokenKind::KwBeat
            | TokenKind::KwReserve
            | TokenKind::And
            | TokenKind::Or
            | TokenKind::Not
    ) {
        4
    } else if matches!(
        token.kind,
        TokenKind::At
            | TokenKind::Question
            | TokenKind::Bang
            | TokenKind::Tilde
            | TokenKind::Colon
            | TokenKind::Define
            | TokenKind::Equals
            | TokenKind::Arrow
            | TokenKind::RightArrow
            | TokenKind::TypeArrow
            | TokenKind::AsyncLeftArrow
            | TokenKind::AsyncRightArrow
            | TokenKind::RendezvousLeftArrow
            | TokenKind::PersistentDependencyArrow
            | TokenKind::DoubleArrow
            | TokenKind::Dot
            | TokenKind::DotDot
            | TokenKind::DotDotEq
            | TokenKind::Comma
            | TokenKind::Semicolon
            | TokenKind::Pipe
            | TokenKind::LParen
            | TokenKind::RParen
            | TokenKind::LBrace
            | TokenKind::RBrace
            | TokenKind::LBracket
            | TokenKind::RBracket
            | TokenKind::Plus
            | TokenKind::PlusArrow
            | TokenKind::PlusEqual
            | TokenKind::Minus
            | TokenKind::MinusArrow
            | TokenKind::MinusEqual
            | TokenKind::Star
            | TokenKind::Slash
            | TokenKind::Percent
            | TokenKind::Caret
            | TokenKind::RelationEq
            | TokenKind::EqEq
            | TokenKind::NotEq
            | TokenKind::Lt
            | TokenKind::Gt
            | TokenKind::LtEq
            | TokenKind::GtEq
    ) {
        7
    } else {
        return None;
    };
    Some(TokenClassification {
        token_type,
        modifiers: 0,
    })
}

fn token_classification(
    token: &Token,
    previous: Option<&Token>,
    local_names: &BTreeSet<String>,
    parameter_names: &BTreeSet<String>,
    stdlib_names: &BTreeSet<String>,
    declaration_ranges: &[ByteRange],
    type_definition_ranges: &[ByteRange],
    parameter_declaration_ranges: &[ByteRange],
) -> Option<TokenClassification> {
    let range = ByteRange {
        start: token.span.start,
        end: token.span.end,
    };
    let declaration = if declaration_ranges.contains(&range) {
        1
    } else {
        0
    };
    let default_library = if stdlib_names.contains(&token.raw) {
        1 << 1
    } else {
        0
    };
    let type_position = previous
        .map(|token| matches!(token.kind, TokenKind::Colon | TokenKind::TypeArrow))
        .unwrap_or(false);
    match &token.kind {
        TokenKind::Ident(name) => {
            if type_definition_ranges.contains(&range) || type_position {
                Some(TokenClassification {
                    token_type: 1,
                    modifiers: declaration,
                })
            } else if local_names.contains(name) || stdlib_names.contains(name) {
                Some(TokenClassification {
                    token_type: 0,
                    modifiers: if declaration != 0 {
                        declaration
                    } else {
                        default_library
                    },
                })
            } else if parameter_names.contains(name) {
                Some(TokenClassification {
                    token_type: 3,
                    modifiers: if parameter_declaration_ranges.contains(&range) {
                        1
                    } else {
                        0
                    },
                })
            } else {
                Some(TokenClassification {
                    token_type: 2,
                    modifiers: 0,
                })
            }
        }
        TokenKind::Josa(_) => {
            if type_position {
                Some(TokenClassification {
                    token_type: 1,
                    modifiers: 0,
                })
            } else {
                Some(TokenClassification {
                    token_type: 9,
                    modifiers: 0,
                })
            }
        }
        TokenKind::Variable(_) | TokenKind::Nuance(_) => Some(TokenClassification {
            token_type: 2,
            modifiers: 0,
        }),
        TokenKind::StringLit(_) => Some(TokenClassification {
            token_type: 5,
            modifiers: 0,
        }),
        TokenKind::Integer(_) | TokenKind::Float(_) => Some(TokenClassification {
            token_type: 6,
            modifiers: 0,
        }),
        TokenKind::Atom(_) => Some(TokenClassification {
            token_type: 8,
            modifiers: 0,
        }),
        TokenKind::Pragma(_) => Some(TokenClassification {
            token_type: 4,
            modifiers: 0,
        }),
        TokenKind::KwImeumssi
        | TokenKind::KwUmjikssi
        | TokenKind::KwGallaessi
        | TokenKind::KwRelationssi
        | TokenKind::KwValueFunc
        | TokenKind::KwSam
        | TokenKind::KwHeureumssi
        | TokenKind::KwIeumssi
        | TokenKind::KwSemssi
        | TokenKind::KwManyak
        | TokenKind::KwIramyeon
        | TokenKind::KwIlttae
        | TokenKind::KwAniramyeon
        | TokenKind::KwBanbok
        | TokenKind::KwButeo
        | TokenKind::KwKkaji
        | TokenKind::KwDongan
        | TokenKind::KwDaehae
        | TokenKind::KwMeomchugi
        | TokenKind::KwGeonneottwigi
        | TokenKind::KwDollyeojwo
        | TokenKind::KwTolabogi
        | TokenKind::KwAllyeo
        | TokenKind::KwHaebogo
        | TokenKind::KwGoreugi
        | TokenKind::KwMajeumyeon
        | TokenKind::KwJeonjehae
        | TokenKind::KwBojanghago
        | TokenKind::KwHaeseo
        | TokenKind::KwNeuljikeobogo
        | TokenKind::KwBoyeojugi
        | TokenKind::KwBeat
        | TokenKind::KwReserve
        | TokenKind::And
        | TokenKind::Or
        | TokenKind::Not => {
            if type_position {
                Some(TokenClassification {
                    token_type: 1,
                    modifiers: 0,
                })
            } else {
                Some(TokenClassification {
                    token_type: 4,
                    modifiers: 0,
                })
            }
        }
        TokenKind::At
        | TokenKind::Question
        | TokenKind::Bang
        | TokenKind::Tilde
        | TokenKind::Colon
        | TokenKind::Define
        | TokenKind::Equals
        | TokenKind::Arrow
        | TokenKind::RightArrow
        | TokenKind::TypeArrow
        | TokenKind::AsyncLeftArrow
        | TokenKind::AsyncRightArrow
        | TokenKind::RendezvousLeftArrow
        | TokenKind::PersistentDependencyArrow
        | TokenKind::DoubleArrow
        | TokenKind::Dot
        | TokenKind::DotDot
        | TokenKind::DotDotEq
        | TokenKind::Comma
        | TokenKind::Semicolon
        | TokenKind::Pipe
        | TokenKind::LParen
        | TokenKind::RParen
        | TokenKind::LBrace
        | TokenKind::RBrace
        | TokenKind::LBracket
        | TokenKind::RBracket
        | TokenKind::Plus
        | TokenKind::PlusArrow
        | TokenKind::PlusEqual
        | TokenKind::Minus
        | TokenKind::MinusArrow
        | TokenKind::MinusEqual
        | TokenKind::Star
        | TokenKind::Slash
        | TokenKind::Percent
        | TokenKind::Caret
        | TokenKind::RelationEq
        | TokenKind::EqEq
        | TokenKind::NotEq
        | TokenKind::Lt
        | TokenKind::Gt
        | TokenKind::LtEq
        | TokenKind::GtEq => Some(TokenClassification {
            token_type: 7,
            modifiers: 0,
        }),
        TokenKind::AssertionBlock(_)
        | TokenKind::TemplateBlock(_)
        | TokenKind::FormulaBlock(_)
        | TokenKind::StateMachineBlock(_)
        | TokenKind::BogeaMadangBlock(_)
        | TokenKind::BogeaJangmyeonBlock(_)
        | TokenKind::JjaimBlock(_)
        | TokenKind::Eof => None,
    }
}
