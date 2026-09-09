# PC01 typed-local legacy equals targeted independent rereview 요청

## 요청

```text
TASK: DDN-P-RELINT-PC01-FU01
SCOPE: PC01 typed-local legacy equals diagnostic precision
REQUIRED_VERDICT: plain PASS만 follow-up closure 허용
MODE: fixed-HEAD read-only isolated review
```

## 고정점

- review custody commit: `8e395f560d6f8913816cbcf9c6e7ce3b9065f8cb`
- prior verdict: `PASS_WITH_FOLLOW_UP`
- rebound G14 handoff parent: `5a50a58e6dde1c48b18a5148fb05e2f767628d5c`
- correction commit: `5332841a14dc490e320e886da999e6b5ce99cf98`
- product/test fixed HEAD: `b8530bd6eadcf79658a821f4e9b4538991b89b80`
- merge count from original PC01 review parent: `0`

## 반드시 직접 확인할 항목

1. `값:수 = 1.`이 accept되지 않고 exact
   `E_V25_DEFINITION_MIGRATION_REQUIRED`인가
2. recommended surface가 `:=`이며 일반 expected-token 오류로 퇴행하지 않았는가
3. `OPTION_B`가 type parser 완료 뒤 Equals만 분류해 applied/function type을 다루는가
4. malformed type을 migration 오류로 오분류하지 않는가
5. untyped-local/top-level old equals의 기존 diagnostic이 유지되는가
6. valid `:=`, `<-`, 재정의 Definition identity가 유지되는가
7. `채비` Butbak `=`가 별도 의미로 유지되는가
8. parse 실패 전에 program/state/output/effect가 생성되지 않는가
9. original M1/M2/M3와 FU01 M1~M5가 각각 RED이며 residue 0인가
10. five-file pack이 byte-unchanged이고 3/3인가
11. PC02 exact inverse 및 G14 successor parity가 보존됐는가
12. A/B WASM byte identity와 tracked freshness가 재현되는가
13. SSOT/SPEC/UI/public membership/projectile/activation 경계 diff가 0인가

## 허용 verdict

Claude만 `PASS / PASS_WITH_FOLLOW_UP / REWORK`를 발행한다. plain `PASS`일 때만
FU01 closure와 후속 PC01 membership 판단으로 진행한다. 이 요청은 release membership,
public conformance, activation 또는 Human PASS를 승인하지 않는다.
