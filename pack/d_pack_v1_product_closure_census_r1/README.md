# D-PACK-V1-PRODUCT-CLOSURE-CENSUS-R1

V1 capability census가 제품Chat roadmap input, live SSOT authority, 실제 제품 증거와 release nonclaim을 혼동하지 않는지 검사한다.

```powershell
python tests/run_v1_product_closure_census_r1.py
```

검사는 17개 필수 축과 UTF-8 BOM, DAG cycle, deterministic regeneration을 확인한다. PASS는 census 문서의 내부 정합만 뜻하며 제품 구현·SSOT membership·V1 readiness·release를 승인하지 않는다.
