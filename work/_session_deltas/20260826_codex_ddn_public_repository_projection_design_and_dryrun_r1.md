# 2026-08-26 Codex public repository projection R1

## session identity

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex Work/Desktop
- AI_CAPABILITY: local repository audit, deterministic projection prototype, dry-run validation
- SESSION_NICKNAME: 또니랑저장소·Codex관리Work
- PROJECT_ROLE: MANAGER / Repository Custody
- RETURN_LABEL: Codex관리Work
- DEEP_RESEARCH_CHECK: NOT_USE — 현재 저장소 원문과 운영 정본만으로 R1 경계 설계가 가능하다.

## owner direction

기존 개발 소스와 Git 이력을 훼손하지 않고, 공개용 소스와 실행 산출물을 별도로 예쁘게 정리하는 체계를 격리된 위치에서 시작한다. 이번 R1은 GitHub 변경, 삭제, 이동, visibility 변경, push, release를 하지 않는다.

## result

- isolated worktree and branch created from sealed audit-baseline candidate
- deterministic allowlist projection manifest and task-owned prototype added
- public preview A/B: 3,468 files, raw tree identity equal
- root Rust workspace and teul-cli ordinary offline check: PASS
- public self-contained unit-test compile: fail-closed on two internal fixture dependencies
- public conformance selected closure: 18 referenced test/runner paths missing
- internal absolute path and public facade/license/security gaps recorded
- existing GitHub, shared root, product, SSOT, public SPEC unchanged

## decisions/open

- keep current development source in internal Work; do not reorganize it by mass move
- make public source through deterministic projection from a future clean integration commit
- existing GitHub private conversion and new public repository creation remain network/owner gates
- release integration baseline, license, public repository name, public product scope remain owner decisions

## protected boundaries

- shared dirty root untouched
- `docs/ssot/**` untouched
- public SPEC untouched
- product source untouched
- official DB/process/activation untouched

## final status

```text
DDN_PUBLIC_REPOSITORY_PROJECTION_R1_IMPLEMENTED_UNDER_REVIEW
DETERMINISTIC_PUBLIC_PREVIEW_A_B_PASS
PUBLIC_REPO_SELF_CONTAINED_TESTS_FAIL_CLOSED
PUBLICATION_READY_NO
R2_RELEASE_INTEGRATION_CHECKPOINT_OPEN
GITHUB_OPERATION_NOT_AUTHORIZED
```
