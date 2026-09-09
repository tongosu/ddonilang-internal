# public SPEC 문서 예제와 제품 예제의 간극

public Language SPEC v0.5.0의 예제 7개는 각 파일 첫 줄에
`docs-first / product-open`이라고 명시한다. 실제 제품 parser 결과도 이를 확인한다.

```text
V25_PASS: 0/7
PRE_V25_PASS: 1/7
NEITHER: 6/7
```

따라서 다음 세 주장은 서로 다르다.

1. 문서가 설명하는 언어 의미가 있다.
2. 공개 저장소에 예제 파일이 있다.
3. 현재 공식 CLI/WASM/Workbench에서 같은 바이트가 실행된다.

현 v0.5.0은 1과 2의 문서 권위이며 3을 보장하지 않는다. V1 product closure에서는
기존 예제를 억지로 통과시키거나 historical parser fallback을 넣지 않는다. 선택된 제품
예제를 current V25 source로 별도 migration하고, public SPEC successor가 필요하면
정본관리 경로에서 별도 다룬다.

