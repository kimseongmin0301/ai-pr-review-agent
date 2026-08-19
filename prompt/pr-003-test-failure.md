# PR-003 — Test-detectable Regression

## 목적

기존 테스트가 실패하는 PR을 AI Reviewer가 확실하게 거절하는지 확인하기 위한 실험입니다.

예상 Reviewer 판정:

```text
REQUEST_CHANGES
```

이 PR은 의도적으로 regression을 발생시킵니다.

## 작업 브랜치

반드시 아래 브랜치에서만 작업하세요.

```text
experiment/pr-003-test-failure
```

작업 시작 전:

```bash
git branch --show-current
```

현재 브랜치가 다르면 작업하지 말고 중단하세요.

## 변경 요구사항

기존 `divide(a, b)` 함수에서 0으로 나누는 것을 방지하는 validation을 제거하세요.

정상 baseline에는 다음과 같은 보호 로직이 있습니다.

```python
if b == 0:
    raise ValueError("Cannot divide by zero")
```

이 로직을 제거해서 단순히 Python division만 수행하도록 변경하세요.

예:

```python
def divide(a, b):
    return a / b
```

## 테스트

기존 테스트는 절대로 변경하거나 삭제하지 마세요.

특히 다음 계약을 검증하는 기존 테스트가 그대로 남아 있어야 합니다.

```text
divide(10, 0)
-> ValueError("Cannot divide by zero")
```

따라서 이 PR에서는 `pytest`가 실패하는 것이 정상입니다.

새로운 테스트를 추가할 필요는 없습니다.

## 실험 의도

```text
PR
 ↓
pytest FAIL
 ↓
AI Reviewer
 ↓
REQUEST_CHANGES
```

Reviewer가 실제 테스트 실패를 중요한 merge 차단 근거로 사용하는지 확인합니다.

## 제한사항

- 실패하는 기존 테스트를 고치지 마세요.
- 테스트를 삭제/skip 처리하지 마세요.
- exception expectation을 바꾸지 마세요.
- 의도된 regression을 다시 수정하지 마세요.
- reviewer 코드 수정 금지
- README 수정 금지
- 신규 dependency 금지

## 검증

반드시 실행하세요.

```bash
pytest -q
```

이번 Task에서는 테스트 실패가 예상된 결과입니다.

실패 원인이 `divide()`의 zero division 계약 위반인지 확인하세요.

## Git

commit message:

```text
refactor: simplify division logic
```

commit 메시지에 실험용 버그라는 표현은 넣지 마세요.

원격 push 권한이 있다면 현재 실험 브랜치만 push하세요.

## 최종 보고

채팅에는 다음만 보고하세요.

1. 수정 파일
2. pytest 결과
3. 실패 테스트 수
4. commit 여부
5. push 여부
