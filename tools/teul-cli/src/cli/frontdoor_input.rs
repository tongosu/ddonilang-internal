//! Retained CLI adapter for shared frontdoor input authority.

pub use ddonirang_tool::preprocess::{
    prepare_frontdoor_canon_input, prepare_frontdoor_runtime_source,
    validate_no_legacy_frontdoor_surface,
};
#[cfg(test)]
pub use ddonirang_tool::preprocess::find_legacy_header;

#[cfg(test)]
mod tests {
    use super::{
        find_legacy_header, prepare_frontdoor_canon_input, validate_no_legacy_frontdoor_surface,
    };

    #[test]
    fn legacy_header_is_detected_via_lang_single_source() {
        let source = "#이름: 금지\n(매마디)마다 { n <- 1. }.";
        let found = find_legacy_header(source).expect("must detect");
        assert_eq!(found.0, 1);
        assert_eq!(found.1, "이름");
        let prepared = prepare_frontdoor_canon_input(source);
        assert!(!prepared.prepared.contains("#이름:"));
        assert!(prepared.prepared.contains("(매마디)마다"));
    }

    #[test]
    fn boim_is_accepted_via_frontdoor_guard() {
        let source = "보임 { x: 1. }.";
        validate_no_legacy_frontdoor_surface(source).expect("must pass");
    }

    #[test]
    fn legacy_root_prefix_is_rejected_via_frontdoor_guard() {
        let source = "살림.x <- 1.";
        let err = validate_no_legacy_frontdoor_surface(source).expect_err("must reject");
        assert!(err.contains("E_SALIM_REMOVED"));
    }
}
