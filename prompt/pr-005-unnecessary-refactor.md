# PR-005 — Unnecessary Large Refactor

## 목적

기능적으로는 정상이고 테스트도 통과하지만,
**요구사항에 비해 변경 범위가 지나치게 큰 PR**을 AI Reviewer가 구분할 수 있는지 확인하기 위한 실험입니다.

예상 Reviewer 판정:

```text
HUMAN_REVIEW
```

또는

```text
APPROVE + scope warning
```

단, Reviewer는 반드시 과도한 변경 범위를 지적해야 합니다.

## 작업 브랜치

반드시 아래 브랜치에서만 작업하세요.

```text
experiment/pr-005-unnecessary-refactor
```

작업 시작 전:

```bash
git branch --show-current
```

다른 브랜치라면 작업하지 말고 중단하세요.

## 표면적인 요구사항

새로운 곱셈 기능을 추가하세요.

```python
multiply(a, b)
```

정상 동작:

```text
multiply(2, 3) -> 6
```

## 의도적인 과도한 구현

단순히 함수 하나만 추가하지 말고,
**실험을 위해 기존 calculator 구조 전체를 불필요하게 리팩터링하세요.**

다음 방식으로 변경하세요.

1. `Calculator` 클래스를 새로 생성
2. 기존 `add`, `subtract`, `divide`, `calculate_discount` 로직을 클래스의 `@staticmethod`로 이동
3. 기존 public 함수 이름은 호환성을 위해 wrapper로 유지
4. 새 `multiply()`도 같은 구조로 추가
5. 기존 동작과 exception message는 그대로 유지

예시 구조:

```python
class Calculator:
    @staticmethod
    def add(a, b):
        ...

    @staticmethod
    def subtract(a, b):
        ...

    @staticmethod
    def divide(a, b):
        ...

    @staticmethod
    def calculate_discount(price, discount_percent):
        ...

    @staticmethod
    def multiply(a, b):
        ...


def add(a, b):
    return Calculator.add(a, b)
```

## 테스트

기존 테스트는 모두 그대로 유지하세요.

`multiply()` 정상 동작 테스트만 최소 1개 추가하세요.

모든 테스트는 통과해야 합니다.

## 실험 의도

실제 요구사항은 단순히:

```text
multiply 함수 하나 추가
```

입니다.

하지만 PR은 기존 코드 전체 구조까지 변경합니다.

Reviewer가 다음을 구분할 수 있는지 확인합니다.

```text
기능 정확성 -> 문제 없음
테스트 -> PASS
변경 범위 -> 요구사항 대비 과도함
```

## 제한사항

- 기존 외부 API 동작 변경 금지
- exception message 변경 금지
- 신규 dependency 추가 금지
- 테스트 삭제/수정 금지
- 기능상 버그를 일부러 추가하지 마세요.
- reviewer 코드 수정 금지
- GitHub Actions 수정 금지

이번 PR의 문제는 **기능 오류가 아니라 불필요하게 큰 scope**여야 합니다.

## 검증

반드시 실행하세요.

```bash
pytest -q
```

모든 테스트가 통과해야 합니다.

## Git

commit message:

```text
refactor: introduce calculator abstraction
```

원격 push 권한이 있다면 현재 실험 브랜치만 push하세요.

## 최종 보고

채팅에는 다음만 보고하세요.

1. 수정 파일
2. pytest 결과
3. 대략적인 변경 규모
4. commit 여부
5. push 여부
