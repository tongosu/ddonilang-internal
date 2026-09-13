# DDN-LONG-RELINT-PRODUCT-01 최종 권위·계보 감사

## 권위

- live SSOT: `v25.15.0`
- live 검증: `tools/check_ssot_v25_15_0_live_promotion.py --check` PASS, 39 files, RD 437, current pointer 3개 일치
- public Language SPEC: `v0.5.0`, 18-file docs-first current
- public 검증: `tools/check_language_spec_v0_5_0_public_current.py` PASS, `tools/check_public_language_spec.py` PASS
- authority impact: `AUTHORITY_DRIFT_NO_PRODUCT_CHANGE_REQUIRED`

`v25.12.0`~`v25.15.0`의 추가 결정은 PathIR/선택 문법·public provenance·governance·maturity floor에 한정되고, 이번 PC01 Definition/Binding migration diagnostic과 G14 legacy rejection 의미는 `v25.11.1`에서 계승된다.

## 선형 계보

```text
372fd3894f48a3e08dbbf81f45be03bd1f6eac67
... 8e395f560d6f8913816cbcf9c6e7ce3b9065f8cb (prior PASS_WITH_FOLLOW_UP custody)
... 5332841a14dc490e320e886da999e6b5ce99cf98 (PC01 correction)
... b8530bd6eadcf79658a821f4e9b4538991b89b80 (product/test fixed HEAD)
... 3f169b472d30927740af1d6586090da616ea35ca (latest-live authority binding)
```

- merge commits from `372fd389...` through authority binding: `0`
- G14 original→rebound identities are preserved in `PC01_TYPED_LOCAL_LEGACY_EQUALS_FOLLOW_UP_RESULT.md`.
- product/test fixed HEAD after this evidence session remains `b8530bd6...`; no product or test source was changed.
- shared dirty root remained `a000e262...`, tracked dirty `201`, staged `0`; it was not reset, cleaned, stashed, or used as writer.

## pointer identities

| artifact | bytes | SHA-256 |
|---|---:|---|
| `docs/ssot/CURRENT.md` | 670 | `9ba5186db604a20c83117839a47fba1dd065191a20a621b3df08846da24079a5` |
| `docs/ssot/ssot/CURRENT.md` | 652 | `23938453e58dbb3024d618cb1940b9553272b35931ccff2b74e28feb481b7095` |
| `SSOT_INDEX_v25.15.0.md` | 109125 | `4944fec57309efbe27c2f3150590edf84935da7b639b73e0196a02529d50f3bb` |
| `SSOT_ALL_MANIFEST_v25.15.0.json` | 5258 | `f08a149b25520e708c8250a71e487d0fb420576a2e088202171dfdbf1e316ad4` |
| live seal | 46009 | `7df920afe46aa6495d1a85bc7a4745370ee3adde063301ac033a5a050b8b17d2` |
| `publish/spec/CURRENT.md` | - | `26158188bd30a3c42c9a93ab43ee676988163fbc55cf145ab4f59bfbaea25855` |
