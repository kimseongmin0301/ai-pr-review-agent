# PR-001 — Valid Change

## 목적

AI PR Reviewer가 **정상적인 변경을 불필요하게 거절하지 않는지** 확인하기 위한 기준 PR입니다.

예상 Reviewer 판정:

```text
APPROVE
```

## 작업 브랜치

반드시 아래 브랜치에서만 작업하세요.

```text
experiment/pr-001-valid
```

작업 시작 전 현재 브랜치를 확인하세요.

```bash
git branch --show-current
```

현재 브랜치가 `experiment/pr-001-valid`가 아니라면 작업하지 말고 중단하세요.

## 요구사항

기존 `app/calculator.py`에 새로운 곱셈 기능을 추가하세요.

```python
multiply(a, b)
```

동작:

```text
multiply(2, 3) -> 6
multiply(-2, 3) -> -6
multiply(0, 10) -> 0
```

기존 함수의 동작은 변경하지 마세요.

## 테스트

`tests/test_calculator.py`에 `multiply()`에 대한 테스트를 추가하세요.

최소 다음 케이스를 검증하세요.

1. 양수 × 양수
2. 음수 × 양수
3. 0 × 숫자

기존 테스트는 수정하거나 삭제하지 마세요.

## 제한사항

- 기존 함수 구현 변경 금지
- 기존 테스트 수정/삭제 금지
- 불필요한 리팩터링 금지
- 신규 dependency 추가 금지
- README 수정 불필요
- reviewer 코드 수정 금지
- GitHub Actions 수정 금지

이번 PR은 **작고 정상적인 기능 추가**여야 합니다.

## 검증

반드시 실행하세요.

```bash
pytest -q
```

모든 테스트가 통과해야 합니다.

## Git

commit message:

```text
feat: add multiplication function
```

원격 push 권한이 있다면 현재 실험 브랜치만 push하세요.

## 최종 보고

채팅에는 다음만 보고하세요.

1. 수정 파일
2. 테스트 결과
3. commit 여부
4. push 여부
