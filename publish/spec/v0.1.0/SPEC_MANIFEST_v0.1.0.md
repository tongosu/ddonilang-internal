# 또니랑 Language SPEC manifest v0.1.0

> status: pre-release public draft
> authority: public projection; SSOT `v24.14.1` wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `v0.1.0` |
| source SSOT | `v24.14.1` |
| source SSOT tree sha256 | `da399c42feb9fc6a664b9a596a7c04b220c66e3c335bbe6079a852ca1487ad91` |
| source SSOT manifest sha256 | `97a042091ddf9d6c34454b1c74c1abc912ead09f232f8364a417dce5c4dbad83` |
| source SSOT seal sha256 | `6d0cea225aff41bb3b95ccf72cf1489a2ad6005d0626b5ab28568136ee1c6476` |
| preserved prior SSOT | `v24.14.0` |
| preserved prior tree sha256 | `da0ab5f164fe076c8c315cc909bcfee20dd0c3b7da3eede4639e1f54cd9effd3` |
| lifecycle ledger sha256 | `6f21e4e99289e59b95cf87f80c9c4024819a85edb09ff26a10941bbe289c3659` |
| source census sha256 | `be56357afa56f708392aef22b48b6d4a6dfd6691692453a0a77c0dbf8e38521c` |
| repository HEAD (context only) | `3ee7b50fbece053d85603d35421661d3f569c670` |
| projection generator sha256 | `f712cec4fb3d0733c4d38738b2b0758d94e2d5987ce77f4b7b7f0111eb4066bf` |

콘텐츠 해시가 권위 핀이다. HEAD는 dirty worktree에서도 추적을 돕는 문맥 정보일
뿐이며 현재 문서 bytes의 권위 증거가 아니다.

## public documents

| file | sha256 |
|---|---|
| `SPEC_LANGUAGE_INTRODUCTION_v0.1.0.md` | `5d2d3ad90ac5a258edbab58e6eafb142ebc83473b58786bf3293c75d8be6465e` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.1.0.md` | `d0038d70f1f2b18a6982d7871208455a5258eb2c68608a387ad20b5b153db958` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.1.0.md` | `5c26e4d2ae05ca4f2b62c1e94d448a12f29c296501402f7db7c522d108fb37a6` |
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.1.0.md` | `44ceccb7ceffdeea06dcc2bf8afecb4940faed943327026cc9e0b33f3875f472` |
| `SPEC_DETERMINISM_CONTRACT_v0.1.0.md` | `c0078ce7ff5710095646c34051f2683c97d3646e76ff0b4e99bc0100a4a17be7` |

## assembly rule

위 순서와 UTF-8(no BOM), LF를 사용한다. 공개 문서는 새 언어 의미를 만들지 않으며,
내부 SSOT와 충돌하면 `SSOT_ALL_MANIFEST_v24.14.1.md`와 그 source 문서가 우선한다.
