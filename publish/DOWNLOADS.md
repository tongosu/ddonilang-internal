# 또니랑 다운로드

## 현재 배포 경계

- 이 문서는 안정적인 최종 사용자 바이너리가 출시됐다고 주장하지 않습니다.
- 검증된 GitHub Release가 발행되기 전에는 [빠른 시작](QUICKSTART.md)에 따라 소스에서
  빌드하고 실행하는 방식이 기준입니다.
- Windows·macOS·Linux 같은 예정 플랫폼 이름이나 파일명 예시는 실제 출시 증거가 아닙니다.

## 소스 빌드

```sh
cargo build --manifest-path tools/teul-cli/Cargo.toml
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- --help
```

## 향후 공개 바이너리 요건

공개 바이너리를 출시할 때는 다음을 함께 제공합니다.

- 버전과 운영체제·아키텍처 표지
- SHA-256 체크섬
- 확정된 라이선스와 필요한 고지 파일
- 실제 바이너리 검증 기록

저장소 소스 공개와 바이너리 배포는 서로 다른 관문입니다. 현재 라이선스는 owner 결정
대기 상태이며, 라이선스가 없다는 사실을 임의의 재사용 허가로 해석하면 안 됩니다.

[제품 지원 현황](PRODUCT_SUPPORT_CURRENT.md)
