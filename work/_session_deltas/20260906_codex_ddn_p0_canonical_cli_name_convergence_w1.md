# P0 canonical CLI convergence W1 session delta

- Fixed product commit `d96d638ed55f29e1b51813318b93e0d635ca9bdc` follows `e802c92a3f3d290f0f857f263aeb2a19ef868d7b` directly.
- The Korean artifact literal was materialized incorrectly by Windows PowerShell during the first candidate run. The script now derives the artifact basename from Unicode code points; the first output root is preserved and the clean second run passed.
- Four pre-existing untracked session-delta custody files were not staged or modified.
