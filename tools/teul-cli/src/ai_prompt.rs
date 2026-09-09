//! Retained CLI adapter for the shared tool-owned AI prompt authority.
//!
//! The implementation lives in `ddonirang_tool::ai_prompt`; this module keeps
//! the historical internal command wiring without retaining a private parser,
//! authority selector, canonicalizer, or bundle hash implementation.

pub use ddonirang_tool::ai_prompt::{run_ai_prompt, AiPromptArgs};
