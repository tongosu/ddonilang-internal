# 또니랑 Language SPEC manifest v0.5.0 candidate R3

> status: public candidate / independent review required / not current / docs-first / product-open
> authority: semantic-corrected candidate projection; internal live SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `v0.5.0` |
| public family | `v0.5.0-candidate-r3` |
| public current remains | `v0.4.0` |
| source SSOT current | `v24.24.1` |
| source SSOT manifest sha256 | `8ce07dd5c7ac60a84183771f78f965f3c886b12972a86626dae96bad58bcf37c` |
| source SSOT seal sha256 | `17e34ee59856528f6fb08e5743d45a09e10b35329ce1e64b27e7bfebbc889b35` |
| owner direction sha256 | `fdbec6dd68e8e75487ca32494d4ffaf0f5158e4b2ec1089b407c657b114b6b3d` |
| R2 format correction sha256 | `07ae4fdeea4ebaa1cf3716256c1289e9af8c98e4a2a17cda63ce772a34698ab2` |
| R3 semantic correction sha256 | `5969afbf7ee589ff589cc01e95e86cfa61360bd5abbb8689a13714701979141a` |
| predecessor public version | `v0.4.0` |
| predecessor manifest sha256 | `738b2eea90add844d2b076179662399f4ba75c59b78a4ea2e6703648674f3107` |
| predecessor seal sha256 | `1e6472ed996fb4d7ddb8166db93c22ff97d6ceafd0d62b7c31c59dac2516ddac` |
| candidate content tree sha256 | `ea2e2b69d80f9ac1a844549f4aa8c6f5015405bda8d5b2d42282a21dbbb803b5` |

## candidate files

| file | sha256 |
|---|---|
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.5.0.md` | `d2234bd6d0c90eef10cc06d07c6c23867a169e748fe4df5af15daaefcb4e3712` |
| `SPEC_DETERMINISM_CONTRACT_v0.5.0.md` | `19643153c3de041f8184e5243f815cb114d09252657d3cd429396737d6fbf275` |
| `SPEC_EXAMPLES_v0.5.0.md` | `076e879440d1c4d2cb4fd1853552ffd94ca1fc1b7465c2373e938119bb38258b` |
| `SPEC_LANGUAGE_INTRODUCTION_v0.5.0.md` | `a7a271436117a70d822e664a7cad8f1b5cfd4a7a62647672db1b63198cc54e2b` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.5.0.md` | `4b5042d4d9e00ed370449a406f5c45eb9d870d39fa974853a09023cbb628ad2b` |
| `SPEC_MIGRATION_v0.5.0.md` | `3d3cf5737e324e1e023a842f471128e5d66fdea29ceeebb1393cfb639a51733f` |
| `SPEC_SEMANTIC_CORE_v0.5.0.md` | `633989e8a79c5ad1b2276fb9764646c9fc99d01a5e037b4988fab3c7aa9e0963` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.5.0.md` | `9251a34f2bfe2fc3b54c9797a8c7cf4b7b5fa8742bee898a37933af6fbcbd58d` |
| `SPEC_TRACE_v0.5.0.detjson` | `8ccc19ee622d6152bd9785dc340a3792d5f78728e4bc74464b72073ac5177862` |
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
- 첫 candidate와 R2는 각 manager self-check 실패판으로 byte 보존한다.
- OPEN/DEFER 목록은 trace와 지원 범위 문서에 유지한다.
- 독립 PASS와 owner 최종 승격 전에는 public current가 아니다.
- 문서 후보는 parser/runtime landed, behavior-closed, corpus 완료 또는
  외부 사용자 성공을 뜻하지 않는다.
