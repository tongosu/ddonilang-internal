# 또니랑 Language SPEC manifest v0.1.1

> status: current pre-release public draft
> authority: public projection; installed current SSOT wins on conflict
> source state: SSOT v24.14.2 owner-approved administrator candidate, protected apply pending

## traceability pins

| pin | value |
|---|---|
| public version | `v0.1.1` |
| source SSOT target | `v24.14.2` |
| source SSOT state | `owner-approved administrator candidate / not installed current` |
| source SSOT candidate tree sha256 | `75d1914433ab7f6ba7fbf8ed376b1973d3fea5130d96eafa1536f32dac3e84ad` |
| source SSOT candidate manifest sha256 | `06fac63c84536cb2102b4275cc30466f211a08d21b383052d98678b7de5fa7f6` |
| source SSOT candidate seal sha256 | `da832ad959d21ddd507daade4427571a0116e6ebebf67b0cae77ed60ca97cde4` |
| installed SSOT at publication | `v24.14.1` |
| preserved public predecessor | `v0.1.0` |
| preserved public predecessor tree sha256 | `08ea02e013c6312d0abd1a963c9b824fb1ec0a689e90f3fd5eb8c97bc8bb81c2` |
| preserved public predecessor seal sha256 | `069684097ac3a815ed90c7365a2de3580cec0e32bdb9df57c223c2dc800d6652` |
| lifecycle ledger sha256 | `d0d061afead5d1381988d303f8da509878b151f7cbdebb26871ea45aff699a6e` |
| owner decision sha256 | `98fe5fe76dee10c61ff00c2f20e095677686a8785c82a99c648d57f7c9ac6291` |
| flat settings census sha256 | `ac464ae4e50fe71621ec63d9b844153fae68a20fa70aa23219f6c3f0ca3da757` |
| projection generator sha256 | `21759073887ebcc28717f5e65b7b98bedbc0b669fe9b694e9a3d00fcdfe5ce6a` |

콘텐츠·candidate tree 해시가 권위 핀이다. protected apply가 끝나기 전 충돌은 설치된
SSOT v24.14.1이 이기며, 적용 뒤에는 v24.14.2가 source authority가 된다.

## public documents

| file | sha256 |
|---|---|
| `SPEC_LANGUAGE_INTRODUCTION_v0.1.1.md` | `50bb9fca96cd573af63dde0e54c85cd83aa1b7d98028ce3dae1f3595d9cc0d01` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.1.1.md` | `bfddc3e19c2c1659d455d7f592ec4f288e6fd562e3259d18b001116b78393d83` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.1.1.md` | `a06cf68f430751d7ee62f4f9a1a3d68b33417c8c900420dcbd9daa6365d19c68` |
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.1.1.md` | `0e62615571e5f9ac4a93c6b33d237754c732eb9dc4dbc8930dd6556d9ce45674` |
| `SPEC_DETERMINISM_CONTRACT_v0.1.1.md` | `9120cacaa1d59ef40fec6a97cef2ec4b5f6cf286518914aa98dd293e010d7d0e` |

## patch scope

- `씨앗/씨앗값/씨앗묶음`과 `시앗*` deprecation.
- settings 8절, 평면 `제목/설명/마디수` 이행 정책.
- 한국어 config digest 표시명과 영어 wire/schema id 분리.
- `가지곳간` 사용자-facing 생태계 용어.
- runtime 구현 완료 범위 확대 없음.

## assembly rule

위 문서 순서와 UTF-8 without BOM, LF를 사용한다. manifest self-hash와 모든 public
문서는 `SPEC_SHA256_v0.1.1.md`이 봉인한다.
