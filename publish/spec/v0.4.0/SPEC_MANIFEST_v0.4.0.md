# 또니랑 Language SPEC manifest v0.4.0

> status: public current / owner-approved / docs-first / product-open
> authority: current public projection; internal live SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `v0.4.0` |
| public family | `v0.4.0` |
| source SSOT current | `v24.22.1` |
| source SSOT manifest sha256 | `10f71a250deb4ce76988cb3b93d1f34716d9f10be5e6a5caf86c12bf2a8204dc` |
| source SSOT seal sha256 | `1423660ea3aefc6336d0626082c1cc4137245e3dd1ebe8cae10c00e399e6e9ec` |
| reviewed candidate manifest sha256 | `be7804ba6b6babd077cec2dca9fe6bd621a8ebae82f406874323a0721efa4d9f` |
| reviewed candidate seal sha256 | `e9284920b6d440c48f6822fb13f8a00d5a1848d2c2cfbb9113ce1267b2bf9dab` |
| independent review sha256 | `1b45ab2c83f295389138cde9fc16d6903739eddea5e20ab7b41d571f8ed083b0` |
| owner final promotion sha256 | `35251e69e5fdaeea682531317359ba4c3dc3cb8e797a108d64ef746dc8f53538` |
| predecessor public version | `v0.3.0` |
| predecessor manifest sha256 | `3e0a2ecfc0b4d3ebbcbe014124395b5172778d0a3ba49237163d9b0bd6cbb53a` |
| predecessor seal sha256 | `f25af1dc447520e35a34f40a6125163d42235f42a6fa9d6981ec07f23b87b8bf` |
| public content tree sha256 | `6f42b56eff9d0aaea16da1d5098626e25ae4d2f1b67c461f08f8d5877927f296` |

## public files

| file | sha256 |
|---|---|
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.4.0.md` | `55966edec8043645d9170316af3c791a1f386932268015c424ca7ef4fb880bfa` |
| `SPEC_DETERMINISM_CONTRACT_v0.4.0.md` | `a3c7fec2925bc442bfa3414258cce30f5dbdf021dbb756ddc165ce31102ccc79` |
| `SPEC_EXAMPLES_v0.4.0.md` | `4748ec2615f842312a4344ab63565405e655e02e5c255de4b9e6d967594ef4e1` |
| `SPEC_LANGUAGE_INTRODUCTION_v0.4.0.md` | `d8b322f9775dad7fa9d55f8131d948e9fb678748d97934046b2928e7edd5ba2d` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.4.0.md` | `a62c109350e095aa9eabc64f714cc8ff0de22d2e3aa8c321bfe1dbac0884eb35` |
| `SPEC_MIGRATION_v0.4.0.md` | `2db0f7fe87ec840c19ba010c34d91da22e3c81732731c2dca39a8ad863b469c0` |
| `SPEC_SEMANTIC_CORE_v0.4.0.md` | `642308a7e7b39de87e9a276f5530cba602fb8b3aa47e714badc5602103edde1d` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.4.0.md` | `674d64fc2b0ad490a65dfa710d937b4e2256d4839b74e72a9458600c37a9018f` |
| `SPEC_TRACE_v0.4.0.detjson` | `c5ed5fee60072469d18a7b824a3fdcc61af5f2835f7a14202b7982c01690d6a3` |
| `examples/01_result_and_optional.ddn` | `ad2afee4b3a05608f428c9362606a32a942433ba316d730fa61b5d0e10dc8bab` |
| `examples/02_generic_static_header.ddn` | `5d8769965da0847e7b91e57c5b339efcce6967dd974d9aab4c510de00293d229` |
| `examples/03_bytes_and_exact_number.ddn` | `e472c5368531ac61e8494fb1a52009ffa9f69a7ffe5a4212e7cd556d68bbec50` |
| `examples/04_function_and_optional_map.ddn` | `53459ee191f1d28f0c3261851b43f6109e69b61a0c56e7336034657d715c0843` |
| `examples/05_pack_kinds.ddn` | `26fcc743eccb2e033b9a26f0f3c1dc65bf9bd6d6373e157af3abd8c724848fe0` |
| `examples/06_observation_and_mol.ddn` | `46ed35740b67e0530d393d444dd96ae241cfefcd16d636f66bfa0f2fb1834b37` |

## projection boundary

- `publish/spec/CURRENT.md`의 public current는 v0.4.0이다.
- v0.4.0-candidate, v0.3.0과 이전 공개판은 제자리에서 byte 보존한다.
- P1·C-02·C-04·C-05·C-06·KS 최종 syntax·exact wire·제품 관문은 OPEN이다.
- 문서 current는 parser/runtime landed, behavior-closed, 기본 제품 승격,
  corpus 완료, 외부 solver 또는 외부 사용자 성공을 뜻하지 않는다.
