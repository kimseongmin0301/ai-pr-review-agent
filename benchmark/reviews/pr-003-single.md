# AI PR Review

## Decision

REQUEST_CHANGES

## Confidence

0.96

## Summary

PR #3 (`experiment/pr-003-test-failure` → `main`, "refactor: simplify division logic")은 `app/calculator.py`의 `divide(a, b)`에서 `b == 0` 가드와 해당 docstring `Raises:` 항목을 제거했다. 변경 규모는 1 file / +1 / -7이며, diff는 GitHub PR diff와 `git diff origin/main...pr/3` 양쪽에서 동일하게 확인했다.

이 변경은 "refactor"라는 제목과 달리 **관찰 가능한 동작을 바꾼다**. 변경 전 `divide(1, 0)`은 `ValueError("Cannot divide by zero")`를 던졌으나, 변경 후에는 파이썬 기본 `ZeroDivisionError`가 그대로 전파된다. 즉 공개 함수의 예외 계약(exception contract)이 깨진 regression이며, 남는 코드 한 줄은 "정리"가 아니라 검증 로직의 삭제다.

`tests/test_calculator.py::test_divide_by_zero_raises_value_error`가 이 계약을 직접 검증하고 있고, 해당 테스트는 head에서 실패한다. 테스트 파일 자체의 docstring이 명시하듯 이 테스트들은 구현 세부가 아닌 *observable behaviour*(반환값과 발생 예외)만 검증하도록 작성되어 있다. 따라서 이 실패는 **테스트가 낡아서가 아니라 코드가 기존 계약을 위반해서** 발생한 것이며, 정당한 refactor라면 초록색으로 남아 있어야 했다. 테스트를 수정해 통과시키는 방향은 여기서 올바른 해법이 아니다.

PR description은 이 실패와 원인을 정확히 보고하고 있다(저자의 보고는 정직하다). 다만 실패 원인을 밝혔다는 사실이 merge 가능성을 바꾸지는 않는다. 기존에 동작하던 계약을 의도적으로 제거하겠다는 요구사항이 PR에 제시되어 있지 않으므로, 이는 승인 대상이 아니라 수정 대상이다.

## Test Result

- command: `python -m pytest -q` (PR head `0855147`을 별도 git worktree로 checkout 후 실행)
- result: `1 failed, 9 passed in 0.43s` / exit status `1`
- passed: 9
- failed: 1 — `tests/test_calculator.py::test_divide_by_zero_raises_value_error`
  - 실패 내용: `E  ZeroDivisionError: division by zero` at `app/calculator.py:23`
- 비교(baseline): `origin/main` 기준 동일 명령은 `10 passed`, exit status `0`
  → 이 PR이 **새로 깨뜨린** 테스트이며 기존부터 실패하던 테스트가 아니다.

## Issues

### Issue 1

- Severity: HIGH
- File: `app/calculator.py`
- Line: 21–23 (`divide`), 제거된 원본 라인 22–29
- Reason: `if b == 0: raise ValueError("Cannot divide by zero")` 가드가 제거되어 공개 함수의 예외 계약이 깨졌다. 입력 `divide(1, 0)`(또는 `b`가 0인 모든 호출, 예: `divide(0, 0)`)에서 이전에는 `ValueError("Cannot divide by zero")`가 발생했지만 이제 `ZeroDivisionError`가 발생한다. 예외 타입과 메시지가 모두 바뀌므로, `except ValueError`로 0 나눗셈을 처리하던 상위 호출부는 예외를 잡지 못하고 그대로 터진다. 이는 backward-incompatible regression이며, `tests/test_calculator.py:34-36`의 실패가 이 결함을 정확히 가리킨다. 같은 변경에서 docstring의 `Raises: ValueError` 항목도 함께 사라져, 문서상으로도 0 나눗셈 시의 동작이 명시되지 않게 되었다.
- Recommendation: `divide`의 `b == 0` 가드와 `ValueError("Cannot divide by zero")`, 그리고 docstring의 `Raises:` 항목을 원래대로 복원한다. 만약 `ZeroDivisionError`를 노출하는 것이 실제로 의도된 API 변경이라면, 코드 정리(refactor)가 아닌 **breaking change**로 분리해 별도 PR로 제안하고, 계약 변경 근거·영향 범위·호출부 마이그레이션·테스트 갱신을 함께 제시해야 한다. 어느 경우든 테스트를 통과시키기 위해 `test_divide_by_zero_raises_value_error`를 수정하는 방식은 채택하지 않는다.

### Issue 2

- Severity: MEDIUM
- File: PR metadata (title / description), `app/calculator.py`
- Line: N/A (PR 단위)
- Reason: PR title이 `refactor: simplify division logic`이지만 실제 변경은 동작을 보존하지 않는다. Refactor의 정의상 외부 동작은 유지되어야 하는데, 이 변경은 예외 타입·메시지·문서화된 계약을 모두 바꾼다. 또한 description은 red 상태(`1 failed`)를 인지한 채로 PR을 열었음을 밝히고 있으나, 실패를 해결하거나 계약 변경을 정당화하는 요구사항·근거는 제시하지 않는다. 결과적으로 리뷰어/후속 유지보수자가 커밋 메시지만 보고 "안전한 정리"로 오해할 위험이 있다.
- Recommendation: 변경 의도를 명확히 한다. 가드 복원이 목표라면 title/description을 실제 변경에 맞게 정리하고 테스트가 green이 된 뒤 다시 올린다. 계약 변경이 목표라면 `refactor:`가 아닌 breaking-change 표기(예: `feat!:` 또는 `BREAKING CHANGE:` 노트)를 사용하고, 왜 `ValueError` 대신 `ZeroDivisionError`가 옳은지를 description에 명시한다.

### Issue 3

- Severity: LOW
- File: `app/calculator.py`
- Line: 26–41 (`calculate_discount`)와의 대비
- Reason: 같은 모듈의 `calculate_discount`는 입력 검증(`price < 0`, `discount_percent` 범위)과 docstring `Raises:` 항목을 그대로 유지하고 있다. `divide`에서만 검증을 제거하면 모듈 내 오류 처리 방식이 서로 어긋나, 이 모듈의 함수들이 잘못된 입력에 대해 어떤 예외를 던지는지 호출부가 일관되게 기대할 수 없다.
- Recommendation: 모듈 전체의 입력 검증 정책을 하나로 유지한다(현재 코드베이스 기준으로는 명시적 `ValueError` + docstring `Raises:` 문서화). 정책을 바꾸려면 `divide` 한 곳만이 아니라 모듈 차원에서 합의된 변경으로 진행한다.

## Merge Recommendation

**지금 Merge하면 안 된다.** 이 PR은 `main`에서 통과하던 테스트를 새로 깨뜨리며(main: 10 passed → head: 1 failed / 9 passed, exit 1), 그 실패는 flaky나 낡은 테스트가 아니라 `divide`의 문서화된 예외 계약이 실제로 제거되었음을 정확히 반영한다. HIGH severity regression이 존재하므로 decision은 `REQUEST_CHANGES`다. `divide`의 0 나눗셈 가드를 복원해 `pytest -q`가 전부 통과하는 상태로 만든 뒤 재검토하거나, `ZeroDivisionError` 노출이 실제 의도라면 breaking change로 재제안해 사람이 API 정책 차원에서 판단하도록 해야 한다. Merge 여부의 최종 결정은 사람에게 있다.

---

## Reviewer Notes (process)

- 이 리뷰는 `prompt/reviewer/SINGLE_REVIEWER.md`의 절차와 판정 기준만을 사용했다. 해당 파일이 현재 working tree에 존재하지 않아 커밋 `64b45cd`(`git show 64b45cd:prompt/reviewer/SINGLE_REVIEWER.md`)에서 원문을 읽었다. 내용은 그 커밋의 Reviewer System Prompt 원문 그대로다.
- 판단에 사용한 정보: PR #3 metadata, GitHub PR diff, `git diff origin/main...pr/3`, `app/calculator.py`, `tests/test_calculator.py`, 그리고 head/main 각각의 `pytest -q` 실행 결과.
- benchmark 오염 방지(§7, §8) 준수: `prompt/pr-00*.md`, `benchmark/README.md`, `benchmark/reviews/*`의 기존 결과, 다른 PR의 내용은 열지 않았다. 파일 목록에 `prompt/pr-003-test-failure.md`가 보였으나 내용은 읽지 않았고 판단 근거로 사용하지 않았다.
- §9/§10 준수: 코드·테스트를 수정하지 않았고 commit/push/merge도 하지 않았다. 테스트는 원본 저장소를 건드리지 않도록 scratchpad에 만든 별도 git worktree(detached HEAD `0855147`)에서 실행했다.
