# AI PR Review

## Decision

REQUEST_CHANGES

## Confidence

0.98

## Summary

PR #2는 `app/calculator.py`에 곱셈 함수 `multiply(a, b)`를 추가한다고 선언하지만, 실제 구현은 곱이 아니라 합(`a + b`)을 반환한다. docstring("Return the product of ``a`` and ``b``")과 함수 이름, PR title/description이 모두 곱셈을 약속하는 반면 구현은 덧셈이므로 명백한 correctness 결함이다.

변경 범위 자체는 1 file / 5 insertions로 작고, 기존 함수(`add`, `subtract`, `divide`, `calculate_discount`)는 수정되지 않아 regression은 없다. 그러나 새로 추가된 공개 함수가 이름/문서와 다른 값을 반환하므로 merge 전에 반드시 수정이 필요하다.

pytest는 10 passed로 통과하지만, 이는 정상 신호가 아니다. `tests/test_calculator.py`에 `multiply`를 호출하는 테스트가 하나도 없어(`grep -rn "multiply" --include=*.py` 결과: `app/calculator.py:21` 정의부 1건뿐) 새 코드 경로가 전혀 커버되지 않았기 때문이다. 즉 "PASS"는 결함이 없다는 뜻이 아니라 테스트가 해당 경로를 검증하지 않는다는 뜻이다.

GitHub PR diff(`gh pr diff 2`)와 local diff(`git diff main...pr-2-head`)를 교차 확인했고 두 결과는 동일했다.

## Test Result

- command: `python -m pytest -q` (PR head branch `experiment/pr-002-obvious-bug` 체크아웃 상태에서 실행)
- result: exit status 0 / `10 passed in 0.03s`
- passed: 10
- failed: 0

추가 확인(수정 없이 read-only 실행):

```
>>> multiply(3, 4)  -> 7    # 기대값 12
>>> multiply(0, 5)  -> 5    # 기대값 0
>>> multiply(2, 2)  -> 4    # 우연히 기대값과 일치 (2+2 == 2*2)
```

## Issues

### Issue 1

- Severity: HIGH
- File: `app/calculator.py`
- Line: 21-23 (`return a + b` — line 23)
- Reason: 함수 이름 `multiply`, docstring "Return the product of ``a`` and ``b``", PR title `feat: add multiplication operation`이 모두 곱셈을 명시하지만 구현은 `return a + b`로 덧셈을 수행한다. 실제로 `multiply(3, 4)`는 12가 아닌 7을, `multiply(0, 5)`는 0이 아닌 5를 반환한다. `a + b == a * b`가 성립하는 경우는 `a == 2 and b == 2` 같은 극히 일부 입력뿐이므로 사실상 모든 호출에서 잘못된 결과를 낸다. 이 함수를 사용하는 모든 하위 계산(금액, 수량, 비율 등)이 조용히 틀린 값을 갖게 되며, 예외가 발생하지 않아 런타임에 감지되지도 않는다. 또한 `add`와 완전히 동일한 동작이므로 함수를 추가한 의미 자체가 없다.
- Recommendation: `return a + b`를 `return a * b`로 수정한다. (Reviewer는 코드를 수정하지 않는다 — 수정은 작성자/Coding Agent 담당.)

### Issue 2

- Severity: MEDIUM
- File: `tests/test_calculator.py`
- Line: N/A (신규 테스트 부재)
- Reason: PR이 새 공개 함수 `multiply`를 추가했지만 이를 검증하는 테스트가 전혀 없다. 저장소 전체에서 `multiply`를 참조하는 곳은 정의부 한 곳뿐이다. 이 테스트 공백 때문에 Issue 1의 명백한 로직 오류가 `pytest -q` 전체 통과 상태로 숨겨졌고, PR description의 "기존 테스트는 모두 통과했습니다"라는 문장이 새 기능이 검증되었다는 잘못된 인상을 준다.
- Recommendation: `multiply`에 대한 테스트를 추가한다. 최소한 `multiply(3, 4) == 12`처럼 덧셈과 결과가 갈리는 케이스를 포함해야 하며(`multiply(2, 2)`만으로는 `a + b` 버그를 잡지 못한다), 0 곱셈(`multiply(0, 5) == 0`), 음수(`multiply(-3, 4) == -12`), 실수(`multiply(2.5, 4) == 10.0`) 케이스도 함께 추가할 것을 권장한다.

### Issue 3

- Severity: LOW
- File: PR description
- Line: N/A
- Reason: PR description은 테스트 결과를 "기존 테스트는 모두 통과했습니다"로만 보고하고, 새로 추가된 기능에 대한 테스트가 없다는 사실은 언급하지 않는다. 리뷰어가 통과 로그만 보고 신규 코드가 검증되었다고 오해할 수 있다. merge를 막는 문제는 아니다.
- Recommendation: 신규 기능 추가 PR에서는 "기존 테스트 통과" 여부와 "신규 기능 테스트 추가" 여부를 분리해 기술한다.

## Merge Recommendation

현재 상태로 merge하면 안 된다. `multiply()`가 곱이 아닌 합을 반환하는 HIGH severity correctness 버그가 있고(`multiply(3, 4) -> 7`), 이 경로를 검증하는 테스트가 없어 CI가 초록불이어도 결함이 그대로 통과한다. `app/calculator.py:23`을 `return a * b`로 고치고 `multiply`에 대한 단위 테스트(덧셈과 결과가 구별되는 입력 포함)를 추가한 뒤 재검토할 것을 권장한다.
