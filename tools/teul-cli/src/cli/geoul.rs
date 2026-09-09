use std::cell::RefCell;
use std::path::{Path, PathBuf};

use crate::cli::sam_snapshot::apply_snapshot;
use crate::core::geoul::{
    decode_input_snapshot, geoul_state_hash_bytes, GeoulBundleReader, InputSnapshotV1,
};
use crate::core::state::Key;
use crate::core::value::Value;
use crate::core::State;
use crate::lang::lexer::Lexer;
use crate::lang::parser::Parser;
use crate::runtime::{Evaluator, RuntimeError};
pub fn run_geoul_query(
    dir: &Path,
    madi: u64,
    key: &str,
    entry_override: Option<&Path>,
) -> Result<(), String> {
    let entry_path = resolve_entry_path(dir, entry_override)?;
    let source = std::fs::read_to_string(&entry_path)
        .map_err(|err| format!("E_GEOUL_ENTRY_READ {} {}", entry_path.display(), err))?;
    let snapshots = load_snapshots(dir, madi)?;
    let key = parse_query_key(key)?;

    let tokens = Lexer::tokenize(&source).map_err(|err| format!("E_GEOUL_LEX {:?}", err))?;
    let default_root = Parser::default_root_for_source(&source);
    let program = Parser::parse_with_default_root(tokens, default_root)
        .map_err(|err| format!("E_GEOUL_PARSE {:?}", err))?;
    let evaluator = Evaluator::with_state(State::new());

    let mut value_out: Option<String> = None;
    let mut hash_out: Option<[u8; 32]> = None;
    let mut before_tick = |tick: u64, state: &mut State| -> Result<(), RuntimeError> {
        if let Some(snapshot) = snapshots.get(tick as usize) {
            apply_snapshot(state, snapshot);
        }
        Ok(())
    };
    let mut on_tick = |tick: u64, state: &State, _tick_requested: bool| {
        if tick == madi {
            value_out = Some(value_canon(state, &key));
            hash_out = Some(geoul_state_hash_bytes(state));
        }
    };
    evaluator
        .run_with_ticks_observe_and_inject(&program, madi + 1, &mut before_tick, &mut on_tick)
        .map_err(|err| format!("E_GEOUL_RUNTIME {:?}", err))?;

    let value = value_out.unwrap_or_else(|| "없음".to_string());
    let hash = hash_out
        .map(|bytes| format!("blake3:{}", hex32(&bytes)))
        .unwrap_or_else(|| "blake3:".to_string());

    println!("madi={}", madi);
    println!("key={}", key_label(&key));
    println!("value={}", value);
    println!("state_hash={}", hash);
    Ok(())
}

pub fn run_geoul_backtrace(
    dir: &Path,
    key: &str,
    from: u64,
    to: u64,
    entry_override: Option<&Path>,
) -> Result<(), String> {
    if from > to {
        return Err(format!("E_GEOUL_RANGE from={} to={}", from, to));
    }
    let entry_path = resolve_entry_path(dir, entry_override)?;
    let source = std::fs::read_to_string(&entry_path)
        .map_err(|err| format!("E_GEOUL_ENTRY_READ {} {}", entry_path.display(), err))?;
    let snapshots = load_snapshots(dir, to)?;
    let key = parse_query_key(key)?;

    let tokens = Lexer::tokenize(&source).map_err(|err| format!("E_GEOUL_LEX {:?}", err))?;
    let default_root = Parser::default_root_for_source(&source);
    let program = Parser::parse_with_default_root(tokens, default_root)
        .map_err(|err| format!("E_GEOUL_PARSE {:?}", err))?;
    let evaluator = Evaluator::with_state(State::new());

    let changes: RefCell<Vec<(u64, String)>> = RefCell::new(Vec::new());
    let last_value: RefCell<Option<String>> = RefCell::new(None);
    let mut before_tick = |tick: u64, state: &mut State| -> Result<(), RuntimeError> {
        if let Some(snapshot) = snapshots.get(tick as usize) {
            apply_snapshot(state, snapshot);
        }
        Ok(())
    };
    let mut on_tick = |tick: u64, state: &State, _tick_requested: bool| {
        if tick < from || tick > to {
            return;
        }
        let value = value_canon(state, &key);
        let mut last = last_value.borrow_mut();
        let changed = match last.as_ref() {
            None => true,
            Some(prev) => prev != &value,
        };
        if changed {
            changes.borrow_mut().push((tick, value.clone()));
            *last = Some(value);
        }
    };
    evaluator
        .run_with_ticks_observe_and_inject(&program, to + 1, &mut before_tick, &mut on_tick)
        .map_err(|err| format!("E_GEOUL_RUNTIME {:?}", err))?;

    let changes = changes.into_inner();
    println!("key={}", key_label(&key));
    println!("from={}", from);
    println!("to={}", to);
    println!("change_count={}", changes.len());
    for (madi, value) in changes {
        println!("change_madi={} value={}", madi, value);
    }
    Ok(())
}

fn hex32(bytes: &[u8; 32]) -> String {
    let mut out = String::with_capacity(64);
    for b in bytes {
        use std::fmt::Write;
        let _ = write!(&mut out, "{:02x}", b);
    }
    out
}

fn resolve_entry_path(dir: &Path, entry_override: Option<&Path>) -> Result<PathBuf, String> {
    let entry_path = entry_override
        .map(|path| path.to_path_buf())
        .unwrap_or_else(|| dir.join("entry.ddn"));
    if !entry_path.exists() {
        return Err(format!("E_GEOUL_ENTRY_MISSING {}", entry_path.display()));
    }
    Ok(entry_path)
}

fn load_snapshots(dir: &Path, until: u64) -> Result<Vec<InputSnapshotV1>, String> {
    let mut reader = GeoulBundleReader::open(dir)?;
    let frame_count = reader.frame_count();
    if frame_count == 0 {
        return Err("E_GEOUL_EMPTY_LOG geoul 로그에 프레임이 없습니다".to_string());
    }
    if until >= frame_count {
        return Err(format!(
            "E_GEOUL_RANGE until={} max={}",
            until,
            frame_count.saturating_sub(1)
        ));
    }
    let mut snapshots = Vec::with_capacity((until + 1) as usize);
    for madi in 0..=until {
        let frame = reader.read_frame(madi)?;
        if frame.header.madi != madi {
            return Err(format!(
                "E_GEOUL_FRAME_MADI_MISMATCH expected={} got={}",
                madi, frame.header.madi
            ));
        }
        let snapshot = decode_input_snapshot(&frame.snapshot_detbin)?;
        if snapshot.madi != madi {
            return Err(format!(
                "E_GEOUL_SNAPSHOT_MADI_MISMATCH expected={} got={}",
                madi, snapshot.madi
            ));
        }
        snapshots.push(snapshot);
    }
    Ok(snapshots)
}

fn parse_query_key(input: &str) -> Result<Key, String> {
    let trimmed = input.trim();
    if trimmed.is_empty() {
        return Err("E_GEOUL_KEY_EMPTY key가 비었습니다".to_string());
    }
    if trimmed.starts_with("살림.") || trimmed.starts_with("바탕.") {
        return Err(
            "E_SALIM_REMOVED geoul key는 접두 없이 bare key만 허용합니다. 예: `점수`".to_string(),
        );
    }
    if let Some(rest) = trimmed.strip_prefix("샘.") {
        if rest.is_empty() {
            return Err("E_GEOUL_KEY_EMPTY 샘. 뒤가 비었습니다".to_string());
        }
        return Ok(Key::new(format!("샘.{}", rest)));
    }
    Ok(Key::new(trimmed.to_string()))
}

fn key_label(key: &Key) -> String {
    if key.as_str().starts_with("샘.") || key.as_str().starts_with("입력상태.") {
        key.as_str().to_string()
    } else {
        key.as_str().to_string()
    }
}

fn value_canon(state: &State, key: &Key) -> String {
    match state.get(key) {
        Some(value) => value.canon(),
        None => Value::None.canon(),
    }
}

pub use ddonirang_tool::geoul_workflow::{
    run_geoul_hash, run_geoul_record_check, run_geoul_record_make, run_geoul_seek,
};
#[cfg(test)]
mod tests {
    use super::parse_query_key;

    #[test]
    fn parse_query_key_accepts_bare_key() {
        let key = parse_query_key("점수").expect("bare key should parse");
        assert_eq!(key.as_str(), "점수");
    }

    #[test]
    fn parse_query_key_accepts_sample_key() {
        let key =
            parse_query_key("샘.키보드.누르고있음.ArrowRight").expect("sample key should parse");
        assert_eq!(key.as_str(), "샘.키보드.누르고있음.ArrowRight");
    }

    #[test]
    fn parse_query_key_rejects_empty() {
        let err = parse_query_key("   ").expect_err("empty key must fail");
        assert!(err.contains("E_GEOUL_KEY_EMPTY"));
    }

    #[test]
    fn parse_query_key_rejects_legacy_root_prefix() {
        let err = parse_query_key("살림.점수").expect_err("legacy root must fail");
        assert!(err.contains("E_SALIM_REMOVED"));
    }
}
