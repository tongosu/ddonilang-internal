# Public browser sealed offline dependency status

## package/lock identity

```text
package.json:
  bytes: 63
  sha256: 9b3ff4b17d4ab08dc648a92b920566dc78b7b25bd4732a6c21bacd3417b0a199
package-lock.json:
  bytes: 1707
  sha256: 755d4cced0b6aa5517350dbf65bd518fb1555d70c5340acbcbc86ecbda3ad518
lockfileVersion: 3

playwright:
  version: 1.44.0
  integrity: sha512-F9b3GUCLQ3Nffrfb6dunPOkE5Mh68tR7zN32L4jCk4FjQamgesGay7/dAAe1WaMEGV04DkdJfcJzjoCKygUaRQ==
  license metadata: Apache-2.0
playwright-core:
  version: 1.44.0
  integrity: sha512-ZTbkNpFfYcGWohvTTl+xewITm7EOuqIqex0c7dNZ+aXsbrLj0qI8XlGKfPpipjm0Wny/4Lt4CJsWJk1stVS5qQ==
  license metadata: Apache-2.0
```

## 현재 로컬 cache와 권위 경계

로컬 cache에는 Chromium revision 1117, 1217, 1232와 ffmpeg 1009, 1011 등이
존재한다. 이 cache는 여러 작업의 우연한 local state이며 package-lock과 결속된 공식
bundle, archive 원본, license bundle 또는 복구 가능한 release artifact가 아니다.

따라서 다음이 아직 없다.

1. package-lock integrity와 일치하는 npm tarball exact bytes와 SHA-256
2. Playwright 1.44.0이 요구하는 Windows browser revision/platform archive의 exact
   source URL, bytes, SHA-256 및 추출 manifest
3. helper payload(ffmpeg 등)의 exact identity와 SHA-256
4. 위 payload들의 license/notice material
5. clean machine에서 network 0으로 복구하고 hash를 재검증하는 offline restore script
6. bundle manifest와 independent custody receipt

fresh rights-excluded projection에는 `node_modules`를 포함하지 않는다. 따라서 browser
runner는 `ERR_MODULE_NOT_FOUND` 또는 Workbench product dependency 부재로 fail-closed해야
한다. 로컬 cache 존재를 성공으로 확대하지 않는다.

```text
NETWORK_DOWNLOAD_COUNT: 0
LOCAL_CACHE_PROMOTED_TO_OFFICIAL_BUNDLE: NO
PUBLIC_BROWSER_SELF_CONTAINED: BLOCKED_BY_SEALED_OFFLINE_DEPENDENCY_BUNDLE
PUBLIC_BROWSER_OPEN_BLOCKS_LIMITED_INTERNAL_CLOSURE: NO
PUBLIC_BROWSER_OPEN_BLOCKS_PUBLIC_RELEASE: YES
```
