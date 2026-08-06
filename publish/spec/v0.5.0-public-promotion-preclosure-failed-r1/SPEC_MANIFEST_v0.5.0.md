# 또니랑 Language SPEC manifest v0.5.0

> status: public current / owner-approved / independently reviewed / docs-first / product-open
> authority: current public projection; internal live SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `v0.5.0` |
| public family | `v0.5.0` |
| source SSOT current | `v24.24.1` |
| source SSOT manifest sha256 | `8ce07dd5c7ac60a84183771f78f965f3c886b12972a86626dae96bad58bcf37c` |
| source SSOT seal sha256 | `17e34ee59856528f6fb08e5743d45a09e10b35329ce1e64b27e7bfebbc889b35` |
| reviewed candidate manifest sha256 | `0455f162869a837d81d8683d543b92c27f063ee6423a7638a341209941de2ccb` |
| reviewed candidate seal sha256 | `7fc6b41950659b067267bb2c573f145cba241dcd01f7a74c9711d3589267145f` |
| independent review sha256 | `e5ce11613f0a4aeb2f728b1d08d18948640c1b8624e023dcaae57f1cf0c25c9a` |
| owner final promotion sha256 | `1d042ec2cc4531fa9150eadbc138141f1ed43556bd5856804f5a8f193c00e98d` |
| predecessor public version | `v0.4.0` |
| predecessor manifest sha256 | `738b2eea90add844d2b076179662399f4ba75c59b78a4ea2e6703648674f3107` |
| predecessor seal sha256 | `1e6472ed996fb4d7ddb8166db93c22ff97d6ceafd0d62b7c31c59dac2516ddac` |
| public content tree sha256 | `8e53acb35ea47a287499a24873588e22200c16e2fb3d03a1968ea651f34b0532` |

## public files

| file | sha256 |
|---|---|
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.5.0.md` | `41b9115a781022cbf6118a2f2b1be13fd206db459539830b0f51787165ef8cfa` |
| `SPEC_DETERMINISM_CONTRACT_v0.5.0.md` | `8e6d646e35f2b9213cfdb25a11e9b7fb4452e86325b0dc5db2f0cf89a556a919` |
| `SPEC_EXAMPLES_v0.5.0.md` | `802402650cf76ec9a6dc65ac94bd96ba09673be2e053975153f2f2e02c89ac16` |
| `SPEC_LANGUAGE_INTRODUCTION_v0.5.0.md` | `406aa8bfc5fa3e48757f31498ebc40706094e633a0352be4ab41feb15ee3692a` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.5.0.md` | `5bb7db2d6b885ae7df62c31a7e168786b96815aed9ee8e4dba263aa381044d8e` |
| `SPEC_MIGRATION_v0.5.0.md` | `bcbfc835f227b34843a320b84f9edfc1f3d1a4ac1737ff59ee0281ae1d279c20` |
| `SPEC_SEMANTIC_CORE_v0.5.0.md` | `f2cd59c8b0d9d86dd16d2dafbba8db6ed7cd02cac05ddde3e6233ac5c1d7de74` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.5.0.md` | `695747d2f938118945e00352c40c8cf6b24c2f02bc43e819e08e8f04b50b5aa2` |
| `SPEC_TRACE_v0.5.0.detjson` | `31eb90b19d870543b5c80d3c9998935d70c80412b0cffffc44de15a33bba4538` |
| `examples/01_result_and_optional.ddn` | `03e2ebad78e72e984055698046002271866581c679d9e2365ea3ba5586dbf0c5` |
| `examples/02_generic_static_header.ddn` | `e54938b27ee24735c8c3536aa3b9d826521412ceba2db11d746d470e59a677d4` |
| `examples/03_bytes_and_exact_number.ddn` | `28116c1d97ee0dd71fa51e2020eb7f59678db53cc43958936661a9568142b4e9` |
| `examples/04_function_and_optional_map.ddn` | `b5021ede495c3350ecdef32b40f7a49ba366486265100b68818051794f50050d` |
| `examples/05_pack_kinds.ddn` | `ea5a6472e180e048717a2deaa2abc4dec2d5dff215723155ae1f252bf1356ce0` |
| `examples/06_observation_and_mol.ddn` | `b025e5f27832ffc68427995f612bbf302fd67cc73efe43ebb1402a63bf3ae1fd` |
| `examples/07_common_model.ddn` | `c46a71301b66404279d9ac4b4998517bdbcff03d3c68a4b504052c50eadf5ccc` |

## projection boundary

- RD-001~122를 연속·유일하게 투영한다.
- `publish/spec/CURRENT.md`의 public current는 v0.5.0이다.
- v0.5.0-candidate-r3, 첫 candidate, R2, v0.4.0과 이전판은 제자리에서 byte 보존한다.
- 모든 OPEN/DEFER 목록은 trace와 지원 범위 문서에 유지한다.
- 문서 current는 parser/runtime landed, behavior-closed, 기본 제품 승격,
  corpus 완료, 외부 solver 또는 외부 사용자 성공을 뜻하지 않는다.
