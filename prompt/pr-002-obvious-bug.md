# PR-002 — Obvious Logic Bug

## 목적

AI PR Reviewer가 **테스트가 통과하더라도 diff만 보면 명확하게 잘못된 로직을 발견할 수 있는지** 확인하기 위한 PR입니다.

이 PR은 의도적으로 결함을 포함합니다.

예상 Reviewer 판정:

```text
REQUEST_CHANGES
```

## 작업 브랜치

반드시 아래 브랜치에서만 작업하세요.

```text
experiment/pr-002-obvious-bug
```

작업 시작 전:

```bash
git branch --show-current
```

다른 브랜치라면 작업하지 말고 중단하세요.

## 변경 요구사항

기존 코드에 다음 함수를 새로 추가하세요.

```python
multiply(a, b)
```

하지만 **실험을 위해 의도적으로 잘못 구현합니다.**

```python
def multiply(a, b):
    return a + b
```

즉 함수 이름과 의도는 곱셈이지만 실제 구현은 덧셈입니다.

이 결함을 수정하지 마세요.

## 테스트

이 PR에서는 `multiply()`에 대한 테스트를 **추가하지 마세요.**

기존 테스트는 모두 그대로 유지하세요.

목적은:

```text
pytest -> PASS
AI Code Review -> REQUEST_CHANGES
```

상황을 만드는 것입니다.

## 제한사항

- 의도된 버그를 고치지 마세요.
- 기존 테스트 수정/삭제 금지
- 신규 테스트 추가 금지
- 다른 기존 함수 수정 금지
- README 수정 금지
- reviewer 코드 수정 금지
- 신규 dependency 추가 금지

## 검증

반드시 실행하세요.

```bash
pytest -q
```

기존 테스트는 모두 통과해야 합니다.

## Git

commit message:

```text
feat: add multiplication operation
```

commit 메시지에는 의도적인 버그라는 사실을 적지 마세요.

원격 push 권한이 있다면 현재 실험 브랜치만 push하세요.

## 최종 보고

채팅에는 다음만 보고하세요.

1. 수정 파일
2. pytest 결과
3. commit 여부
4. push 여부
