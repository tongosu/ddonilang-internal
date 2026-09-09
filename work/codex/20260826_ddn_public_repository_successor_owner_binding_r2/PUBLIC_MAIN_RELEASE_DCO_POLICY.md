# Public main, release and DCO policy

## public main

- allowlist projection과 public CI를 통과한 개발 checkpoint만 받는다.
- main commit은 사용자 권장 stable release를 뜻하지 않는다.
- force-push와 history rewrite는 기본 금지한다.
- public source에 없는 internal evidence를 required check로 요구하지 않는다.

## release

- Owner가 사용자 권장 stable checkpoint로 명시한 main commit만 tag 후보가 된다.
- source commit, public tree identity, build toolchain, artifact hashes, SBOM/license ledger, conformance receipt를 봉인한다.
- PUBLIC_SOURCE만으로 clean build를 재현한다.
- pre-release/experimental artifact와 stable release를 별도 channel로 표시한다.

## contribution

- initial publication: DCO 1.1 `Signed-off-by` required
- CLA: initial publication에서 요구하지 않음
- code review가 DCO와 test를 대체하지 않으며, DCO가 technical review와 rights audit를 대체하지 않음
- docs/assets contribution은 파일 role과 origin을 별도 기록

## branch suggestion

```text
main                  validated public development checkpoints
release tags          Owner-recommended stable checkpoints
short-lived branches  public contribution/review only
internal branches     public repository로 투영하지 않음
```

정확한 semantic version/tag 이름은 제품 version authority와 release candidate가 정해질 때 별도 결정한다.
