# 또니랑 Language SPEC manifest v0.2.0

> status: owner-approved public projection candidate / not yet published
> authority: public projection; installed internal current SSOT wins on conflict

## traceability pins

| pin | value |
|---|---|
| public version | `v0.2.0` |
| source SSOT target | `v24.15.0` |
| source SSOT candidate tree sha256 | `78212ebe8561e2dcf51f98b79b32e14d26c00665770184f603c01f02b90a3f7c` |
| source SSOT manifest sha256 | `fd8afc77b259330be265ac929a18d5a61499de20a877d165de68372fdb946459` |
| preserved SSOT snapshot | `v24.14.2` |
| preserved SSOT tree sha256 | `75d1914433ab7f6ba7fbf8ed376b1973d3fea5130d96eafa1536f32dac3e84ad` |
| repository HEAD | `143cf2e37bcf6031060fa4e7631544f1c0f87a3c` |
| workspace dirty at build | `true` |
| owner packet sha256 | `a5fb7dde37af48d5abd4be3a4123496efac26c102518a25dbd733aacd4ae2ffc` |
| projection generator sha256 | `417e25cb189b30647c9e3a2180d613162c9b5b34a7d2b764efa1f5a6ec90fbbb` |
| preserved v0.1.0 tree sha256 | `08ea02e013c6312d0abd1a963c9b824fb1ec0a689e90f3fd5eb8c97bc8bb81c2` |
| preserved v0.1.1 tree sha256 | `7b704192195b0d9f7dc70ffc3599106b7275a14c2c91acf8564f4d4ef6481c86` |

## public files

| file | sha256 |
|---|---|
| `SPEC_LANGUAGE_INTRODUCTION_v0.2.0.md` | `05fedc91cd5827989aeba9626be8dfeb1d5cbff7a40a9bb7c365a1f9c6132c3d` |
| `SPEC_LANGUAGE_SYNTAX_SUMMARY_v0.2.0.md` | `9f78a814d72305fb0d6497c09e0f35cae08bc4072283f9cc1dbc00f23a882193` |
| `SPEC_STABLE_SUPPORT_SURFACE_v0.2.0.md` | `da416ea00d8d203ad7b9079766ddb84372adb7e69b8cc9c005cc3e938dcb1cab` |
| `SPEC_COMPATIBILITY_AND_NONCLAIMS_v0.2.0.md` | `4073cc4b1e308d7867d0170856a93991960df4533671dfac0c7957b299c871b8` |
| `SPEC_DETERMINISM_CONTRACT_v0.2.0.md` | `12abf3f7388814b3cdd17bf2284540a8209a94353a6b619062aeb7c082794725` |
| `SPEC_TRACE_v0.2.0.detjson` | `44970f15db08d382c3d3a4726c17d2343946d6ec700d87602cc4ed4d0a321bc2` |

## projection boundary

- G7-01~G7-07, 한글 씨자리·hash 계층, 함수 타입 `-->`를 사람용 문서로 투영한다.
- 설계 상태와 K0~K7 제품 상태를 분리한다.
- M3-실험 0은 `씨앗지음` 연구 표시와 함께 experimental/unavailable로만 표시한다.
- 지음 하위 artifact의 stable wire/API 이름은 포함하지 않는다.
- v0.1.0과 v0.1.1은 수정하지 않는다.
