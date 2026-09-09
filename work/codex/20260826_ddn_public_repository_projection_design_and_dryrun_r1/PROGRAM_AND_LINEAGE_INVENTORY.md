# Program and lineage inventory

## 핵심 판정

현재 저장소에는 하나의 clean release-integration HEAD가 모든 최신 프로그램을 포함하고 있지 않다. 따라서 가장 최근 날짜의 commit 하나를 곧바로 public source authority로 고르면 안 된다.

## 확인된 기준

- shared root `a000e262...`: tracked dirty 201, staged 0
- public projection audit candidate `905efb4a...`: canonical view convergence closure
- W1C2 I2 limited closure `40cd0473...`: `905efb4a...`와 서로 ancestry 관계 없음
- active math physical worktrees: branch ref는 `a000e262...`와 같아도 실제 진행 상태는 각 worktree의 uncommitted/implementation evidence를 함께 봐야 함
- R10/runtime bridge/release lineages: 별도 branches로 존재
- configured origin: `https://github.com/tongosu/ddonilang.git`
- live remote visibility/default branch/protection/current server SHA: network query를 하지 않아 UNKNOWN

## branch/worktree 분류 원칙

```text
ACTIVE
IMPLEMENTED_PENDING_REVIEW
REVIEW
CLOSED
ARCHIVE_CANDIDATE
UNKNOWN
```

HEAD가 오래됐거나 동일하다는 이유만으로 archive candidate로 만들지 않는다. implementation report, successor ancestry, independent review state, integration/promotion state를 함께 확인해야 한다.

## release integration에 필요한 최소 입력

1. 현재 제품 프로그램별 fixed HEAD와 closure/review commit inventory
2. 서로 다른 계보의 merge-base 및 제품 path overlap audit
3. dirty worktree별 Single Writer와 checkpoint commit/disposition
4. owner가 선택한 release feature set
5. clean linear 또는 명시적 integration commit
6. 그 commit에 대한 public projection dry-run과 independent review

R1의 `905efb4a...`는 projection mechanism을 시험한 sealed input일 뿐, 통합 release baseline 승인안이 아니다.
