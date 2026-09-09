# 공개 브라우저 offline dependency custody

## 감사 범위와 결론

네트워크 다운로드 없이 public projection
`I:/home/urihanl/ddn/codex/build/public-projection-r1/tree-a`를 감사했다.

```text
PUBLIC_BROWSER_DEPENDENCY_CLOSURE_OPEN
NETWORK_DOWNLOAD_COUNT: 0
```

## 현재 metadata

- `package.json` SHA-256:
  `9b3ff4b17d4ab08dc648a92b920566dc78b7b25bd4732a6c21bacd3417b0a199`
- `package-lock.json` SHA-256:
  `755d4cced0b6aa5517350dbf65bd518fb1555d70c5340acbcbc86ecbda3ad518`
- 두 파일은 source와 public projection에서 byte-identical이다.
- manifest/lock은 `playwright@1.44.0`과 `playwright-core@1.44.0`을 선언한다.
- lock은 두 package의 integrity를 포함한다.
- public projection에는 `node_modules`가 없고 포함해서도 안 된다.
- public browser runner 2개는 `playwright`를 직접 import한다.
- fresh projection의 `import('playwright')`는 `ERR_MODULE_NOT_FOUND`로
  fail-closed했다.

로컬 사용자 cache와 별도 설치에서 Chromium revision `1117` 및 ffmpeg `1009`
metadata가 보였지만 이는 우연한 local state이므로 공식 custody 근거로 사용하지
않았다.

## exact missing dependency set

1. lock integrity와 일치하는 `playwright@1.44.0` offline package payload
2. lock integrity와 일치하는 `playwright-core@1.44.0` offline package payload
3. 대상 플랫폼별 Chromium payload의 revision/archive/SHA-256 identity
4. 해당 플랫폼에서 필요한 helper payload(예: ffmpeg)의 identity와 SHA-256
5. 위 payload를 묶는 sealed dependency manifest와 offline restore/check 절차

현재 public projection만으로 브라우저 archive의 exact bytes/hash를 확정할 수
없으므로 exact browser byte set은 미봉인 상태다.

## 권고 custody

`package.json`과 lock은 공개 build/test metadata로 보존한다. `node_modules`를
저장소에 넣지 말고, package tarball hash, browser revision/platform/archive hash,
helper payload, license metadata, offline restore/check script를 포함하는 별도
sealed release/test dependency bundle을 만든다. 이 문서는 bundle 생성, 다운로드,
GitHub 변경 또는 공개 배포를 승인하지 않는다.
