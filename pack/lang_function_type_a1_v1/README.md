# lang_function_type_a1_v1

함수 타입 정본 화살표 `-->`의 A1 제품 세로줄 pack이다.

- 양성: 영항·단항·다항 함수 타입, 함수를 받거나 반환하는 괄호 고차 타입
- 음성: 비결합 연쇄, 함수 타입의 `->` 별칭, 값 위치의 `-->`
- parity: 공통 Rust 언어 frontdoor, CLI run-summary, 제품 WASM canon/runtime

이 pack은 함수 타입의 lexer·AST·parser·canon과 원문 frontdoor parity만 닫는다.
함수값 저장·반환·capture·효과·직렬화는 범위 밖이다.
