# 소스 소유와 call graph

## 판정

```text
SOURCE_OWNERSHIP_CYCLE_WITHOUT_CARGO_CYCLE
```

Cargo가 보고하는 package dependency는 한 방향이지만, 실제 소스 소유는 양방향이다.

```text
teul-cli crate
  ├─ Cargo dependency ───────────────> ddonirang-tool crate
  ├─ path source import ─────────────> tool/src/preprocess.rs
  ├─ private parser/AST/runtime ─────> tools/teul-cli/src/lang + runtime
  └─ 63-command frontend

ddonirang-tool crate
  ├─ shared language/runtime ────────> lang
  ├─ path source import ─────────────> tools/teul-cli/src/canon.rs
  ├─ WASM API
  └─ 28-command frontend
```

## 직접 근거

| edge | 근거 |
|---|---|
| teul-cli → ddonirang-tool Cargo dependency | `tools/teul-cli/Cargo.toml:23` |
| ddonirang-tool → teul canon source | `tool/src/lib.rs:1` |
| teul-cli → tool preprocess source | `tools/teul-cli/src/main.rs:14` |
| tool runtime → shared lang | `tool/src/ddn_runtime.rs:32-38` |
| teul private parser/runtime | `tools/teul-cli/src/runtime/eval.rs:10-24` |

## 규모

| 영역 | Rust 파일 | 줄 수 |
|---|---:|---:|
| tool/src/main.rs | 1 | 7,281 |
| tool/src/ddn_runtime.rs | 1 | 27,792 |
| teul-cli/src/main.rs | 1 | 15,359 |
| teul-cli/src/canon.rs | 1 | 10,827 |
| teul-cli/src/lang | 7 | 9,531 |
| teul-cli/src/runtime | 7 | 25,141 |
| teul-cli/src/cli | 75 | 46,137 |

## 왜 위험한가

1. 파일의 물리적 위치가 semantic authority와 일치하지 않는다.
2. 한쪽 crate를 정리하면 다른 쪽 빌드가 깨질 수 있다.
3. 같은 DDN 원문이 tool shared runtime과 teul private runtime에서 달라질 수 있다.
4. public CLI 이름만 바꿔도 실제 실행 의미가 통합되지는 않는다.

## 목표 구조

```text
lang + tool shared product libraries
             │
             ├── official CLI frontend
             ├── WASM frontend
             └── Workbench RuntimeBridge

internal/research command packages
             └── shared libraries를 소비하되 제품 의미를 재구현하지 않음
```

`canon.rs`와 `preprocess.rs`는 package 경계를 넘는 path-import를 없애고 명시적인 shared module API로 옮기는 것이 첫 구조 교정이다.
