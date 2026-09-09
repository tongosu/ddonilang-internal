use super::document_store::DocumentSnapshot;
use super::position::ByteRange;
use ddonirang_lang::{parse_v25, Lexer, TokenKind};
use std::fmt;

pub const MAX_DOCUMENT_LINKS: usize = 1_000;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DocumentLinkResolution {
    pub range: ByteRange,
    pub target: String,
    pub resource_path: String,
    pub document_version: i64,
    pub snapshot_identity: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DocumentLinkError {
    InvalidUtf8,
    InvalidSource,
}

impl fmt::Display for DocumentLinkError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidUtf8 => f.write_str("document link source가 UTF-8이 아닙니다"),
            Self::InvalidSource => f.write_str("document link source를 해석할 수 없습니다"),
        }
    }
}

impl std::error::Error for DocumentLinkError {}

pub fn document_links_snapshot(
    snapshot: &DocumentSnapshot,
) -> Result<Vec<DocumentLinkResolution>, DocumentLinkError> {
    let source = snapshot
        .text()
        .map_err(|_| DocumentLinkError::InvalidUtf8)?;
    if snapshot.language_id != "ddn" {
        return Ok(Vec::new());
    }
    if parse_v25(source, &snapshot.uri).is_err() {
        return Ok(Vec::new());
    }
    let tokens = Lexer::new(source)
        .tokenize()
        .map_err(|_| DocumentLinkError::InvalidSource)?;
    let mut links = Vec::new();
    for pair in tokens.windows(2) {
        let [at, resource] = pair else {
            continue;
        };
        let TokenKind::StringLit(resource_path) = &resource.kind else {
            continue;
        };
        if !matches!(at.kind, TokenKind::At) || !safe_relative_resource(resource_path) {
            continue;
        }
        let Some(target) = relative_target_uri(&snapshot.uri, resource_path) else {
            continue;
        };
        links.push(DocumentLinkResolution {
            range: ByteRange::new(at.span.start, resource.span.end)
                .map_err(|_| DocumentLinkError::InvalidSource)?,
            target,
            resource_path: resource_path.clone(),
            document_version: snapshot.version,
            snapshot_identity: snapshot.identity.as_str().to_string(),
        });
        if links.len() == MAX_DOCUMENT_LINKS {
            break;
        }
    }
    Ok(links)
}

fn safe_relative_resource(path: &str) -> bool {
    !path.is_empty()
        && !path.contains('\\')
        && !path.contains('\0')
        && !path.starts_with('/')
        && !path.contains(':')
        && path.split('/').all(|part| !part.is_empty() && part != "." && part != "..")
}

fn relative_target_uri(uri: &str, resource_path: &str) -> Option<String> {
    let (directory, _) = uri.rsplit_once('/')?;
    if !directory.contains("://") {
        return None;
    }
    Some(format!("{directory}/{}", encode_uri_path(resource_path)))
}

fn encode_uri_path(path: &str) -> String {
    let mut encoded = String::new();
    for byte in path.as_bytes() {
        if byte.is_ascii_alphanumeric() || matches!(*byte, b'-' | b'.' | b'_' | b'~' | b'/') {
            encoded.push(*byte as char);
        } else {
            encoded.push('%');
            encoded.push(hex_digit(byte >> 4));
            encoded.push(hex_digit(byte & 0x0f));
        }
    }
    encoded
}

fn hex_digit(value: u8) -> char {
    match value {
        0..=9 => (b'0' + value) as char,
        10..=15 => (b'A' + value - 10) as char,
        _ => unreachable!("hex digit is bounded to four bits"),
    }
}
