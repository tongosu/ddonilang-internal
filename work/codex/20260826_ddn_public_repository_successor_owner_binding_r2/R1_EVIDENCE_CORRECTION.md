# R1 evidence correction — public SPEC identity

## finding

R1의 A/B projection tree identity와 file manifest는 재현 가능하다. 그러나 R1 projection receipt의 `public_spec_identity`는 projected source에서 계산하지 않고 `Language_SPEC_v0.5.0_docs_first`로 고정돼 있었다.

R1 source commit `905efb4a...`의 실제 `publish/spec/CURRENT.md`는 `v0.3.0`을 가리키며 `publish/spec/v0.5.0/`은 존재하지 않는다.

## corrected classification

```text
R1_TREE_IDENTITY_A_B: VALID
R1_FILE_MANIFEST_A_B: VALID
R1_PUBLIC_SPEC_IDENTITY_CLAIM: INVALID_HARDCODED_VALUE
R1_ACTUAL_PROJECTED_PUBLIC_SPEC: v0.3.0
R1_PUBLICATION_READY: NO
R1_COMMIT_REWRITE: NO
```

shared root의 현재 파일은 `v0.5.0`을 가리키지만 root HEAD 대비 tracked modified 상태다. public SPEC v0.5.0의 문서 authority와 release integration Git custody는 구분한다. clean sealed integration commit에 결속되기 전에는 public projection source로 사용할 수 없다.

## successor guard

R2 checker는 다음 두 가지를 모두 확인한다.

1. `publish/spec/CURRENT.md`가 expected marker `v0.5.0`을 포함할 것
2. `publish/spec/v0.5.0/SPEC_MANIFEST_v0.5.0.md`가 실제로 존재할 것

R1 preview에서는 두 조건 모두 실패해 `PUBLIC_SPEC_IDENTITY_MISMATCH`로 fail-closed했다. 향후 receipt는 projected bytes에서 SPEC identity를 계산해야 하며 manifest의 선언만 복사해서는 안 된다.
