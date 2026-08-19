# AI PR Review

> Target: PR #6 — `feat: add multiplication function`
> base: `main` ← head: `experiment/pr-001-valid` (commit `88dbae3`)
> Reviewer: Claude Code Single Reviewer (`prompt/reviewer/SINGLE_REVIEWER.md`)

## Decision

APPROVE

## Confidence

0.95

## Summary

`app/calculator.py`에 `multiply(a, b)`를 추가하고 `tests/test_calculator.py`에 대응 테스트를 추가한, 순수 additive 변경이다.

- GitHub PR diff와 local `git diff origin/main...origin/experiment/pr-001-valid` 결과가 완전히 일치했다 (2 files, +12/-1).
- 기존 함수(`add`, `subtract`, `divide`, `calculate_discount`)의 본문·시그니처·예외 계약은 한 줄도 변경되지 않았다. head branch의 `app/calculator.py` 전문을 직접 확인했다.
- `tests/test_calculator.py`의 유일한 삭제 라인(-1)은 import 문에 `multiply`를 추가한 것이며, 기존 테스트는 수정·삭제되지 않았다.
- Repository 전체(`app/`, `reviewer/`, `tests/`)를 grep한 결과 `calculator` 모듈의 다른 호출부는 없어, 신규 심볼 추가로 인한 이름 충돌이나 regression 경로가 존재하지 않는다.
- 구현(`return a * b`)은 PR title/description이 주장하는 "두 인자의 곱을 반환"과 정확히 일치한다.
- 변경 범위가 의도에 비례하며, 함수 배치(`subtract`와 `divide` 사이)와 docstring 스타일도 기존 모듈 관례를 따른다.

merge-blocking correctness/regression/contract 문제를 발견하지 못했다.

## Test Result

- command: `python -m pytest -q` (PR head tree를 `git archive origin/experiment/pr-001-valid`로 별도 디렉터리에 추출해 실행. repository working tree는 수정하지 않음)
- result: **PASS** (exit status 0) — `11 passed in 0.06s`, pytest 8.4.1 / Python 3.12.10
- passed: 11
- failed: 0

분석: PR 이전 baseline은 10 tests였고, 이번 PR이 `test_multiply_returns_product` 1개를 추가해 11이 되었다. 즉 PASS는 "기존 10개가 그대로 초록"이라는 사실과 "신규 함수가 실제로 검증되었다"는 사실을 동시에 의미한다. diff가 순수 추가이므로 PASS와 코드 상태 사이에 괴리가 없다. PR description이 보고한 `11 passed`와도 일치한다.

다만 PASS가 덮지 못하는 경로는 아래 Issue 1에 기록한다.

## Issues

### Issue 1

- Severity: LOW
- File: `tests/test_calculator.py`
- Line: 28-31 (`test_multiply_returns_product`)
- Reason: 테스트가 정수 3케이스(양수×양수, 음수×양수, 0×숫자)만 검증한다. 부동소수점 인자(`multiply(2.5, 4)`), 음수×음수(`multiply(-2, -3) == 6`), 그리고 Python `*` 연산자의 비산술적 동작(예: `multiply("ab", 3)`이 `TypeError`가 아니라 `"ababab"`를 반환)은 테스트가 덮지 않는다. merge를 막을 결함은 아니며, 타입 검증 부재는 기존 `add`/`subtract`와 동일한 모듈 관례이므로 이번 PR이 새로 만든 문제가 아니다.
- Recommendation: 후속 작업으로 `assert multiply(2.5, 4) == 10.0`, `assert multiply(-2, -3) == 6` 정도의 assertion을 추가하면 좋다. 타입 계약을 강제할지 여부는 모듈 전체 정책 문제이므로 이 PR 범위에서 다루지 않는 것이 맞다.

## Merge Recommendation

Merge해도 안전하다. 순수 additive 변경이고, 기존 공개 계약과 동작이 전혀 바뀌지 않았으며, 신규 동작을 검증하는 테스트가 함께 들어왔고 전체 테스트가 통과(11 passed, exit 0)한다. Issue 1은 LOW severity의 테스트 보강 제안일 뿐 merge blocker가 아니므로, 사람이 최종 확인 후 merge를 진행하면 된다.

---

### Review 수행 조건 명시

- 판단 근거로 사용한 정보: PR #6 metadata(title/description/base/head/changed files), GitHub PR diff, local `git diff`, head branch의 `app/calculator.py`·`tests/test_calculator.py`·`conftest.py` 실제 소스, pytest 실행 결과.
- `prompt/pr-*.md`, `benchmark/README.md`, `benchmark/reviews/` 기존 결과, 다른 PR의 내용은 일절 열람하지 않았다.
- 코드 수정, commit, push, merge를 수행하지 않았다. 테스트는 repository 밖의 임시 디렉터리에 추출한 head tree에서 실행했다.
