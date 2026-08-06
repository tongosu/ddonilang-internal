# 또니랑 Language SPEC manifest v0.4.0 candidate

> status: public candidate / not current / docs-first / product-open
> authority: public projection candidate; internal live SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public family | `v0.4.0-candidate` |
| public version | `v0.4.0` |
| public current remains | `v0.3.0` |
| source SSOT current | `v24.22.1` |
| source SSOT manifest sha256 | `10f71a250deb4ce76988cb3b93d1f34716d9f10be5e6a5caf86c12bf2a8204dc` |
| source SSOT seal sha256 | `1423660ea3aefc6336d0626082c1cc4137245e3dd1ebe8cae10c00e399e6e9ec` |
| owner direction sha256 | `ecbfb9b2356a45fbc60eb509acb4169a762a55f6eaaeb1d7a6100f5f6ab97aac` |
| projection generator sha256 | `b57a860fb866d51d9d1df399f41c9f9f1059c3a93fc20737a6ae658b9e8f8c51` |
| predecessor public manifest sha256 | `3e0a2ecfc0b4d3ebbcbe014124395b5172778d0a3ba49237163d9b0bd6cbb53a` |
| predecessor public seal sha256 | `f25af1dc447520e35a34f40a6125163d42235f42a6fa9d6981ec07f23b87b8bf` |
| predecessor public tree sha256 | `db752de511cd1eb3b8cdac62d113cb8e10ebb0f62f5b43e042e3fe35bf03a3fb` |
| public content tree sha256 | `e36933d90041fbe334ebf8abc046a7f96d54f8dd3fcd34cda481c56d9111c459` |
| decision coverage | `RD-001~099 continuous and unique` |

## candidate files

| file | sha256 |
|---|---|
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.4.0.md` | `497fe83d5e3b8865866297fc1b98a9d17d71baf1fe3d4e6f5a19f22010a3b60f` |
| `SPEC_DETERMINISM_CONTRACT_v0.4.0.md` | `2ae0d0fdf009880add1c44f9af32593c73b7d58dce50221d2e6b01781fa7d985` |
| `SPEC_EXAMPLES_v0.4.0.md` | `fec96436d08ff1d639c1ca4aff1edb5eafbcd8006e1b64678c987fc4b94ccf68` |
| `SPEC_LANGUAGE_INTRODUCTION_v0.4.0.md` | `d650f66f1f7b57d2a7fadee8015126ba98c17e39b4558ed116ec7cddc63603c9` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.4.0.md` | `f7280eefeb78eb1025d2bb9a777d862a12dfe2db624ebaefc4ab98a885aca85d` |
| `SPEC_MIGRATION_v0.4.0.md` | `1bb36dff7bb808e686782ddad07ca45abc0866c7f0e25976cf11c51594b02053` |
| `SPEC_SEMANTIC_CORE_v0.4.0.md` | `b7236abb9a41e435fcfcfa34b281d98023d0847aa32c1da401317a1b33af46fe` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.4.0.md` | `b1638cd7b6e26206c0fd5e81c506b327ecdbe3b08633f0a1811492e3605cafea` |
| `SPEC_TRACE_v0.4.0.detjson` | `7c893acfd25fe60b314f5512de501047ca43ce55508b55f16e95330a67a932f2` |
| `examples/01_result_and_optional.ddn` | `a67704905b876017dddf47d551de1b6e1673186728c3b16e9219ebf5b70e5074` |
| `examples/02_generic_static_header.ddn` | `c59a226d2748c14b4d97a3c33cee3321f373fc402586d18020e2350f331f9b9b` |
| `examples/03_bytes_and_exact_number.ddn` | `818c7cca262562de166948591cffa3db8401ff094ce9e4285f806e7b4c7b7efd` |
| `examples/04_function_and_optional_map.ddn` | `b32fe8216e86bf52a404f051bb54f99ab795bb8d91acd960dfaa4f99dab1c745` |
| `examples/05_pack_kinds.ddn` | `638e0c528d42aa0831054b1ad3013b077d7170e1f35545860541f8116c283c90` |
| `examples/06_observation_and_mol.ddn` | `44e0ab0f49a81e23be04680928b1fb213847b7b4378d97dde7c638f698e86e25` |

## projection boundary

- v0.3.0과 이전 공개판은 수정하지 않았다.
- 공개 current는 계속 v0.3.0이며 이 family는 독립 검토 후보이고
  public current가 아니다.
- RD-001~099의 공개 투영 여부와 OPEN은 trace·지원표에서 구분한다.
- 문서 후보는 parser/runtime landed, behavior-closed, corpus 완료,
  기본 제품 승격 또는 외부 사용자 성공이 아니다.
