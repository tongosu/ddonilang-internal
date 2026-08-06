# 또니랑 Language SPEC manifest v0.5.0 candidate

> status: public candidate / independent review required / not current / docs-first / product-open
> authority: candidate public projection; internal live SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `v0.5.0` |
| public family | `v0.5.0-candidate` |
| public current remains | `v0.4.0` |
| source SSOT current | `v24.24.1` |
| source SSOT manifest sha256 | `8ce07dd5c7ac60a84183771f78f965f3c886b12972a86626dae96bad58bcf37c` |
| source SSOT seal sha256 | `17e34ee59856528f6fb08e5743d45a09e10b35329ce1e64b27e7bfebbc889b35` |
| owner direction sha256 | `fdbec6dd68e8e75487ca32494d4ffaf0f5158e4b2ec1089b407c657b114b6b3d` |
| predecessor public version | `v0.4.0` |
| predecessor manifest sha256 | `738b2eea90add844d2b076179662399f4ba75c59b78a4ea2e6703648674f3107` |
| predecessor seal sha256 | `1e6472ed996fb4d7ddb8166db93c22ff97d6ceafd0d62b7c31c59dac2516ddac` |
| candidate content tree sha256 | `696a344b18b852262a8c8c26c83137117355cf45b6bc5d8f65d4205cc3deff46` |

## candidate files

| file | sha256 |
|---|---|
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.5.0.md` | `d2234bd6d0c90eef10cc06d07c6c23867a169e748fe4df5af15daaefcb4e3712` |
| `SPEC_DETERMINISM_CONTRACT_v0.5.0.md` | `19643153c3de041f8184e5243f815cb114d09252657d3cd429396737d6fbf275` |
| `SPEC_EXAMPLES_v0.5.0.md` | `ee33fbd0e0e4913355ca7843a8cd88b52b23daa758bcd94c0c2c2aa01adefb9d` |
| `SPEC_LANGUAGE_INTRODUCTION_v0.5.0.md` | `42ee7b9e18b0193dcdddda612380fd597b90c6bb92d3955a3d02528a99812ffd` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.5.0.md` | `4b5042d4d9e00ed370449a406f5c45eb9d870d39fa974853a09023cbb628ad2b` |
| `SPEC_MIGRATION_v0.5.0.md` | `3d3cf5737e324e1e023a842f471128e5d66fdea29ceeebb1393cfb639a51733f` |
| `SPEC_SEMANTIC_CORE_v0.5.0.md` | `0aa37103cb30cf81133b432b4a2666e7c6f25cebaf0350082e7013b12a2bd486` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.5.0.md` | `b468488f3c5e95e9885f2a2c5482ad26c0fde34f04703570dde950e2e177bf7f` |
| `SPEC_TRACE_v0.5.0.detjson` | `78e59550f8da0d2b5f614b73c9a34c7e02decd85363a48eea8a594e89438f3a1` |
| `examples/01_result_and_optional.ddn` | `fb5f8bff0ee97aa465131c0b5aa561cb23a2a8456c50366cb534124feb77dafd` |
| `examples/02_generic_static_header.ddn` | `b44a0b6c0a74893bd38e8bac9628f832608b8134a289c55d930da3b0f90ca1ae` |
| `examples/03_bytes_and_exact_number.ddn` | `e15804f32a732d496f4d74bb640d2be555a6ebc1659e372bef98458e0c4758e1` |
| `examples/04_function_and_optional_map.ddn` | `eb0e4b82920202cdbc4f5d71f91a491e99f9de2a9ddfe02d2ef7c7939a965db9` |
| `examples/05_pack_kinds.ddn` | `e93bdb89710a2dd0012b8fd07d46f8744f3b8028baa62573e71db5598a2a0083` |
| `examples/06_observation_and_mol.ddn` | `b548a07eeea8b707a21008b0e3bd8984f91a5608fc18d8e97743462d5c2bd819` |
| `examples/07_common_model.ddn` | `102d11cacdb1718c21ab9ea3d9b480e69c1fcd55f9b8236727394b01540b819b` |

## projection boundary

- RD-001~122를 연속·유일하게 투영한다.
- public current는 v0.4.0이고 v0.4.0과 이전판을 제자리에서 byte 보존한다.
- OPEN/DEFER 목록은 trace와 지원 범위 문서에 유지한다.
- 독립 PASS와 owner 최종 승격 전에는 public current가 아니다.
- 문서 후보는 parser/runtime landed, behavior-closed, corpus 완료 또는
  외부 사용자 성공을 뜻하지 않는다.
