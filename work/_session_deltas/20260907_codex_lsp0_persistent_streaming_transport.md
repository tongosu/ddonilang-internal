# 2026-09-07 LSP-0 persistent streaming transport

## 완료

- `ddonirang-lsp`를 EOF 일괄 입력에서 persistent incremental stdin stream으로 전환했다.
- 응답 즉시 flush, complete frame 전부 순차 처리, EOF에서만 decoder finish, exit notification 즉시 종료를 구현했다.
- 기존 transport checker에 I1–I8을 추가하고 Rust focused test ST01–ST08을 추가했다.
- M1–M3 source mutation 각각 RED → exact restore hash `3315b496e6c78c44bbdebb58dd315f553514ee6de9636da037e2018e887c495f` → GREEN을 확인했다.
- 제품 commit: `932487a3d92fc2384f51acd64f869bcfb7742675`.

## 검증·경계

- 직접 실행된 focused Rust test는 13/13 PASS이며 follow-on minimum pack도 PASS다.
- 일반 Cargo 재빌드는 보존된 foreign `lang/**` dirty와 공유 `core` 불일치로 LSP 실행 전 `lang` 컴파일 단계에서 막혔다. 해당 파일은 수정하지 않았다.
- 제품 외 의미론, SSOT, 공개 SPEC, push, 추가 reviewer는 이번 slice에서 다루지 않는다.
- 다음 owner: 동일 target/product commit과 이 evidence handoff를 독립 reviewer에게 전달한다.
