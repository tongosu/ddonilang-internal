# 또니랑 Language SPEC manifest v0.6.0

> status: public current / owner-approved / independently reviewed / docs-first / product-open
> authority: current public projection; internal live SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `v0.6.0` |
| public family | `v0.6.0` |
| source SSOT current | `v25.15.0 / RD-001~437` |
| source SSOT manifest sha256 | `f08a149b25520e708c8250a71e487d0fb420576a2e088202171dfdbf1e316ad4` |
| source SSOT seal sha256 | `7df920afe46aa6495d1a85bc7a4745370ee3adde063301ac033a5a050b8b17d2` |
| reviewed candidate family | `v0.6.0-v25.15.0-trace-custody-correction-candidate-r6` |
| reviewed candidate manifest sha256 | `3212aafbe75e816b9a3fc193e20436ae7e4cc5cebde3ffaaaa30b2c172c9f718` |
| reviewed candidate seal sha256 | `f1e52b5af73973952ec748fc3bb4ffb2f68e231769c684a217573c7a39564e01` |
| independent review sha256 | `81f15dfd969c76eff0e6a2c355ceb3c1a7133b47635efc086fbe9f93435391da` |
| owner final promotion sha256 | `3ad32140a1ffcb7066bbf072505225195746002ea84c0996f5e7231b20934a68` |
| pre-promotion backup report sha256 | `3b6c96afe05db6e3e9eef4a06f9420abad7b1461b8862378c9b045dc0caa4a04` |
| pre-promotion archive sha256 | `6f1807138ba8a667e1c591062d13d4d9e739f697e0f1232fae788a681ac7e185` |
| predecessor public version | `v0.5.0` |
| predecessor manifest sha256 | `78cd7af3a15ba26bebc0392504b15a5c925e54e45e75948cf10db75b31bb7d87` |
| predecessor seal sha256 | `40a2f7548b25aca15060e886b1b946ae06baf36d1651b78b37173f752dfe7370` |
| public content tree sha256 | `713f8651c81b2d2f6c3155623647598dd5176aaff78d387df1dd2aee3beeeb28` |

## public files

| file | sha256 |
|---|---|
| `SPEC_CALLABLE_RESULT_FAILURE_R1_v0.6.0.md` | `d120600428d9911135a6f38ebc761de654a6662831d6d4bba1d41646bfdd9261` |
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.6.0.md` | `c954bce295905ac920151cd342981d275307d5d0253fbb3aaac553eb3eb8e22a` |
| `SPEC_DETERMINISM_CONTRACT_v0.6.0.md` | `c2fd625bb0d85c044da7953170ea88df0eda3792fee3c1ee17a6193e1a0a9faf` |
| `SPEC_EXAMPLES_v0.6.0.md` | `2967a3783d6e89015b39fb63730c083013d3db7af692851c8f1a62a9f4700a90` |
| `SPEC_HOTT_RESEARCH_SURFACE_v0.6.0.md` | `438678fdcd6fa73e011d24c43f10787273c54b2a7385f39eab0f7ae0185d1571` |
| `SPEC_LANGUAGE_INTRODUCTION_v0.6.0.md` | `fb19cb4131e6072b0a277fa703e93b08883f524bcd616a8f5e121106f915605b` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.6.0.md` | `9ec297e6cc1bfa71af2a341a4a47df5fc58583747d210074b71594505518e98d` |
| `SPEC_MIGRATION_v0.6.0.md` | `53aa0326c33a171cb495efd2e39d4ea0c78d57399db03882f099685cb7c96bed` |
| `SPEC_PROOF_KERNEL_PROFILES_v0.6.0.md` | `12d6e1b48270f741bf151e904005183e4d9f2a0457a69a8ae41cfb82b0cd135f` |
| `SPEC_SEMANTIC_CORE_v0.6.0.md` | `907b794d520842aebb2ea3ac68ee06a2f79dacf234c822b75b957a016b22d0d4` |
| `SPEC_SPECIALIST_OPEN_SURFACES_v0.6.0.md` | `336c8d5c892573fc068766f95c9f439839d6c6f6f34ce51ca9eb5b910a5144fd` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.6.0.md` | `0c4fdf722a679bf1bcfa6cb108f1dc3cf93b353d4fbc0d0a73f8dfddd1d2d51c` |
| `SPEC_TENSOR_R1_v0.6.0.md` | `6faf1369a279806532eb48a0c13e70aa38cdd847bac480da089ffecfd80cf401` |
| `SPEC_TRACE_v0.6.0.detjson` | `92dd8209369e5bf90e9a2e9bad2f64be08514219aef877ce861049b3e54f94c6` |
| `SPEC_V25_15_PROJECTION_DISPOSITION_v0.6.0.md` | `266b8db9d7deba1165ca51d4455d6faf484328181476cdbc0d002bdc1d63fb3d` |
| `examples/01_definition_and_rebinding.ddn` | `0e0b391fac3f8282c2387618e4e9f6afdaa20d2fceb92dfa26998f52af1eb98f` |
| `examples/02_complete_callable.ddn` | `2764ddbbd042cd191cc43bae5c03c3f5e8b98f50f1cd11c7744712071cae8f59` |
| `examples/03_typed_morphology.ddn` | `28c0577a75e80e7de6afdb79aab5ec10cc8b3b25e3b3f3194754960310e15c8f` |
| `examples/04_closed_multisurface.ddn` | `f753cf06cfa626ff0a2108bad5477b464e17f7ac5e8f1ace3c2b0c93975d6784` |
| `examples/05_presentation_identity.ddn` | `fd41147d1c8f7a8f8b099f897503dd7bdc52b705857bbfe15ef869b02c808091` |
| `examples/06_persistent_update_root.ddn` | `9de515b0c5eb4a53d17bddb7cccc60e47dcc41428760b6b3ab1ad751ec0e0921` |
| `examples/07_static_header.ddn` | `7baf68eb089b6d5de50440b26a6cb5a43ea1fa002558dfaa7f58435701f19ecd` |
| `examples/08_product_definition.ddn` | `cd19fa0a161800c14a07c0a7e6722c0c959ac3dd195e1e4920c2d15b340d6306` |
| `examples/09_sum_definition.ddn` | `a2a0c772b95b13ac4cd4e3483b706d632b07118ef589badd194c9dc0d80fb364` |
| `examples/10_typed_selection.ddn` | `d8b213983b47f86f45c25f85d01999080cc5f4edd0c4d7c55c84d5d063520ba0` |
| `examples/11_anonymous_function.ddn` | `1c08ab0d174bd9d7476672e076477587f546aac700426156ae4571833652f432` |
| `examples/12_resultplace_and_finish.ddn` | `137d85c33cd40cc907f7d8327f143ecb31776dbe72362037688f3e81b0f0a64d` |
| `examples/13_tensor_selection.ddn` | `eac21d8dde640707596f142f84cab279dddefa311f0e67ee96e5c4e02c586e20` |

## sealed promotion inputs

| file | bytes | sha256 |
|---|---:|---|
| `docs/decisions/LANGUAGE_SPEC_V0_6_0_PUBLIC_CURRENT_FINAL_PROMOTION_OWNER_APPROVAL_20260827.md` | 1378 | `3ad32140a1ffcb7066bbf072505225195746002ea84c0996f5e7231b20934a68` |
| `docs/reports/audit/BACKUP_RESULT_PUBLIC_SPEC_PRE_V0_6_0_FINAL_PROMOTION_R6_20260827.md` | 1144 | `3b6c96afe05db6e3e9eef4a06f9420abad7b1461b8862378c9b045dc0caa4a04` |
| `docs/reports/audit/INDEPENDENT_REVIEW_RESULT_LANGUAGE_SPEC_V0_6_V25_15_TRACE_CUSTODY_R6_CANDIDATE_20260827.md` | 8308 | `81f15dfd969c76eff0e6a2c355ceb3c1a7133b47635efc086fbe9f93435391da` |
| `docs/ssot/ssot/CURRENT_SHA256_v25.15.0.md` | 46009 | `7df920afe46aa6495d1a85bc7a4745370ee3adde063301ac033a5a050b8b17d2` |
| `docs/ssot/ssot/SSOT_ALL_MANIFEST_v25.15.0.md` | 5258 | `f08a149b25520e708c8250a71e487d0fb420576a2e088202171dfdbf1e316ad4` |
| `external:D:\urihanl\git-backups\ddonirang-ssot-live-promotions\public-spec-pre-v0.6.0-final-promotion-r6_20260827_140144.7z` | 62033 | `6f1807138ba8a667e1c591062d13d4d9e739f697e0f1232fae788a681ac7e185` |
| `external:D:\urihanl\git-backups\ddonirang-ssot-live-promotions\public-spec-pre-v0.6.0-final-promotion-r6_20260827_140144.files.utf8.tsv` | 45229 | `529a2e5cd7c282b32f7a3ba2f6df1df8d072050ace1b84ae0745d84800712e38` |
| `external:D:\urihanl\git-backups\ddonirang-ssot-live-promotions\public-spec-pre-v0.6.0-final-promotion-r6_20260827_140144.key.dpapi` | 294 | `e5d28d2bfa84e3f5e377485497c359a26d38840f7d81c218ff164319b300edb1` |
| `external:D:\urihanl\git-backups\ddonirang-ssot-live-promotions\public-spec-pre-v0.6.0-final-promotion-r6_20260827_140144.result.detjson` | 1299 | `5b6366cd856e620b0cd3e8d1eaf0d3b8a719665e853b70a09fb1b2224362176e` |
| `publish/spec/CURRENT.md` | 2758 | `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0` |
| `publish/spec/v0.5.0/SPEC_MANIFEST_v0.5.0.md` | 3584 | `78cd7af3a15ba26bebc0392504b15a5c925e54e45e75948cf10db75b31bb7d87` |
| `publish/spec/v0.5.0/SPEC_SHA256_v0.5.0.md` | 2720 | `40a2f7548b25aca15060e886b1b946ae06baf36d1651b78b37173f752dfe7370` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_CALLABLE_RESULT_FAILURE_R1_v0.6.0.md` | 5817 | `029477d3101c7c0009770c9ead0330ecd9f29e8d611aed4a1300df5fc5aa7f02` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.6.0.md` | 1918 | `13767d18d937102b7ea86854862f597f95ba6514cd8d7db8e514cd31cc5d8dbc` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_DETERMINISM_CONTRACT_v0.6.0.md` | 2004 | `698bc93a5648424608873af2c9274129fdbf57e3d70e869f4e7a3baa093fd6df` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_EXAMPLES_v0.6.0.md` | 1890 | `9eb3d1b8fb3056416472d00d0f9f33354652ce337a072e22c83ceb080e7e90dc` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_HOTT_RESEARCH_SURFACE_v0.6.0.md` | 654 | `438678fdcd6fa73e011d24c43f10787273c54b2a7385f39eab0f7ae0185d1571` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_LANGUAGE_INTRODUCTION_v0.6.0.md` | 1746 | `f5a0bc58d98c2a32dbfaa22b315a5467bcec77ce3f4cb1ea875a8747a823b409` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.6.0.md` | 6988 | `9b28043cf3cafdf34e8ad8a8cfc3dee917b52d252b7d10d53c051b2aa4858cc5` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_MANIFEST_v0.6.0.md` | 11999 | `3212aafbe75e816b9a3fc193e20436ae7e4cc5cebde3ffaaaa30b2c172c9f718` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_MIGRATION_v0.6.0.md` | 1581 | `bdb798873b3b89f4d51eb78d9322c6fa07e0cc26af808cd2cffa74f2099c407b` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_PROOF_KERNEL_PROFILES_v0.6.0.md` | 5667 | `30fde02b5100ee81457b63ce96b1c38b1561dfac7c1893c923bc6ffa4d9cb55a` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_SEMANTIC_CORE_v0.6.0.md` | 4044 | `0fafa5e9080fc40916f69d6a426aaffbf80b1808193027b50ea595115e3bffaf` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_SHA256_v0.6.0.md` | 11421 | `f1e52b5af73973952ec748fc3bb4ffb2f68e231769c684a217573c7a39564e01` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_SPECIALIST_OPEN_SURFACES_v0.6.0.md` | 865 | `9e6e10c5f1d64932693e077dafaf2a65ca3ec360d05ba827e4ac6ffcc5d5a36a` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_STABLE_SUPPORT_SURFACE_v0.6.0.md` | 2706 | `3ef49be6856700ec82287e8724f9d15e56f3c216da9ce08d4db9ac77aad31a2b` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_TENSOR_R1_v0.6.0.md` | 5356 | `7c2ef0f9b8236ee8989cbc7361ebf0efb0421725a8c6cf3fae552704c4e01706` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_TRACE_v0.6.0.detjson` | 1672 | `2ff5d30a18fbee559a97d40bf988c48c10ff2e5a1898d4ac3b2f975b12d5301a` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/SPEC_V25_15_PROJECTION_DISPOSITION_v0.6.0.md` | 1118 | `f49dbf575d6024738c10bf3e6597a4231e93b8013b823b737d871af9b171eb9a` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/01_definition_and_rebinding.ddn` | 38 | `0e0b391fac3f8282c2387618e4e9f6afdaa20d2fceb92dfa26998f52af1eb98f` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/02_complete_callable.ddn` | 97 | `2764ddbbd042cd191cc43bae5c03c3f5e8b98f50f1cd11c7744712071cae8f59` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/03_typed_morphology.ddn` | 105 | `28c0577a75e80e7de6afdb79aab5ec10cc8b3b25e3b3f3194754960310e15c8f` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/04_closed_multisurface.ddn` | 179 | `f753cf06cfa626ff0a2108bad5477b464e17f7ac5e8f1ace3c2b0c93975d6784` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/05_presentation_identity.ddn` | 232 | `fd41147d1c8f7a8f8b099f897503dd7bdc52b705857bbfe15ef869b02c808091` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/06_persistent_update_root.ddn` | 72 | `9de515b0c5eb4a53d17bddb7cccc60e47dcc41428760b6b3ab1ad751ec0e0921` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/07_static_header.ddn` | 134 | `7baf68eb089b6d5de50440b26a6cb5a43ea1fa002558dfaa7f58435701f19ecd` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/08_product_definition.ddn` | 70 | `cd19fa0a161800c14a07c0a7e6722c0c959ac3dd195e1e4920c2d15b340d6306` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/09_sum_definition.ddn` | 85 | `a2a0c772b95b13ac4cd4e3483b706d632b07118ef589badd194c9dc0d80fb364` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/10_typed_selection.ddn` | 68 | `d8b213983b47f86f45c25f85d01999080cc5f4edd0c4d7c55c84d5d063520ba0` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/11_anonymous_function.ddn` | 27 | `1c08ab0d174bd9d7476672e076477587f546aac700426156ae4571833652f432` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/12_resultplace_and_finish.ddn` | 243 | `137d85c33cd40cc907f7d8327f143ecb31776dbe72362037688f3e81b0f0a64d` |
| `publish/spec/v0.6.0-v25.15.0-trace-custody-correction-candidate-r6/examples/13_tensor_selection.ddn` | 161 | `eac21d8dde640707596f142f84cab279dddefa311f0e67ee96e5c4e02c586e20` |
| `tools/check_language_spec_v0_6_0_public_current.py` | 2323 | `e26a9fbb6494e570c1746d6ea954451f4d6b479617a006af930792436bb40c0a` |
| `tools/promote_language_spec_v0_6_0.py` | 16620 | `f1a12814c8972eb6c61857d45648f02dddfaac21f25f935e0f3c7f2e116abd1b` |

## projection boundary

- 내부 SSOT v25.15.0의 RD-001~437 중 공개 언어·governance 투영 범위를 결속한다.
- v0.6.0 source-surface epoch, Tensor, callable result/failure, PathIR/Proof profile을 문서 current로 투영한다.
- R6와 R5/R4/R3, v0.5.0과 이전 공개판은 제자리 보존한다.
- physical parser·AST·schema·wire·proof kernel·runtime·oracle와 제품은 OPEN이다.
- V1 membership·numeric maturity·Human PASS·외부 사용자 성공을 변경하지 않는다.
