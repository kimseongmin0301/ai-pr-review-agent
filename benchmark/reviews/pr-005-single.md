# AI PR Review

- PR: #5 — `refactor: introduce calculator abstraction`
- base: `main` / head: `experiment/pr-005-unnecessary-refactor`
- Reviewer: Claude Code (Single Reviewer, `prompt/reviewer/SINGLE_REVIEWER.md`)

## Decision

HUMAN_REVIEW

## Confidence

0.82

## Summary

동작 측면에서 이 PR은 안전하다. `add` / `subtract` / `divide` / `calculate_discount` 는 `Calculator` staticmethod 로 옮겨졌지만 로직, 검증 순서, 예외 타입, 예외 메시지 문자열이 모두 그대로다. module-level 공개 함수는 이름·시그니처가 유지된 채 위임 wrapper 로 남아 있어 호출부 호환성이 깨지지 않는다. 신규 `multiply(a, b)` 도 `a * b` 로 올바르다. base/head 두 트리를 직접 로드해 4개 기존 함수 × 484개 입력 조합으로 반환값과 예외(타입+메시지)를 비교한 결과 **차이 0건**이었다. 즉 correctness / regression / backward compatibility 관점의 merge-blocking 결함은 없다.

문제는 **변경의 성격과 범위**다. 실제로 요구되는 기능 변경은 `multiply` 한 개(약 4줄)인데, PR 은 이를 위해 모듈 전체를 클래스 기반 구조로 재편했다. 그 결과 `app/calculator.py` 는 46줄 → 97줄로 늘었고, 모든 연산이 `Calculator.<op>` 와 module-level `<op>` **두 곳에 중복 정의**되며 docstring 도 그대로 복제됐다. `Calculator` 는 상태도, 인스턴스화도, 다형성도 없는 순수 namespace 이고 Python 의 module 은 이미 namespace 이므로, 이 계층이 현재 코드베이스에 제공하는 기능적 이득은 확인되지 않는다.

이것은 "코드가 틀렸다" 가 아니라 **공개 API 표면과 모듈 구조에 대한 설계 결정**이다. `Calculator` 라는 두 번째 공개 진입점을 앞으로 유지할 것인지, 아니면 `multiply` 만 추가하고 기존 flat 구조를 유지할 것인지는 팀 컨벤션의 문제이고, AI Reviewer 가 자동 승인/거절로 결정할 사안이 아니다. 따라서 REQUEST_CHANGES(명백한 결함 없음)도 APPROVE(범위가 의도에 비례하지 않고 아키텍처 판단이 필요함)도 아닌 **HUMAN_REVIEW** 로 판정한다.

## Test Result

- command: `python -m pytest -q` (head 트리를 `git archive` 로 별도 디렉터리에 추출해 실행, 작업 트리는 건드리지 않음)
- result: exit status `0` — 전부 통과
- passed: 11
- failed: 0

참고 — 대조군으로 base(`origin/main`)에서도 동일하게 실행: **10 passed, exit 0**. 즉 이 PR 은 테스트 1개를 추가했을 뿐이며 기존 10개 중 깨진 것은 없다.

추가 검증(테스트 스위트와 별개로 리뷰어가 직접 수행):

```text
base vs head 동작 비교 — add / subtract / divide / calculate_discount
입력 조합 484건 (음수, 0, 소수, 경계값 0·100·101, 1e9 포함)
반환값 및 예외 타입·메시지 불일치: 0건
head 에서 새로 노출된 public 이름: Calculator, multiply
```

`pytest` 가 PASS 라는 사실만으로 APPROVE 하지 않았다. 테스트가 통과한 이유는 이 PR 이 실제로 동작 보존적(behaviour-preserving)이기 때문이며, 위 differential 검증으로 그 점을 독립적으로 확인했다.

또한 GitHub PR diff(`gh pr diff 5`)와 local `git diff origin/main...origin/experiment/pr-005-unnecessary-refactor` 를 교차 확인했다. hunk header 의 context 표기를 제외하면 내용은 동일했다(불일치 없음). PR description 이 주장한 `2 files changed, 66 insertions(+), 11 deletions(-)` 와 `11 passed` 도 실제 결과와 일치했다.

## Issues

### Issue 1

- Severity: MEDIUM
- File: `app/calculator.py`
- Line: 11 (`class Calculator`) — 63~97 (위임 wrapper 들)
- Reason: `Calculator` 는 상태가 없고 인스턴스화되지 않으며 하위 클래스나 다형성 사용처도 없는 순수 namespace 다. Python module 자체가 이미 동일한 역할을 하므로 이 계층은 새로운 능력을 제공하지 않는다. 결과적으로 모든 연산이 `Calculator.add` 와 module-level `add` 두 곳에 정의되고 docstring 까지 그대로 복제되어(예: `divide` 의 `Raises:` 블록이 34~43행과 78~85행에 중복), 유지보수 지점이 2배가 되고 두 사본이 시간이 지나며 어긋날 위험이 생긴다. 모듈은 46줄에서 97줄로 늘었지만 관측 가능한 동작은 `multiply` 추가분을 빼면 완전히 동일하다. 저장소 전체를 검색한 결과 `app/calculator.py` 외부의 호출부는 `tests/test_calculator.py` 뿐이며, 이 추상화를 요구하는 기존 소비자는 존재하지 않는다.
- Recommendation: (a) 이 구조가 팀이 합의한 방향인지 먼저 확정할 것. (b) 유지한다면 공개 진입점을 하나로 정할 것 — 예를 들어 `__all__` 로 module-level 함수만 노출하고 `Calculator` 를 내부용(`_Calculator`)으로 두거나, 반대로 `Calculator` 를 정식 API 로 삼고 module-level 함수는 deprecated shim 임을 docstring 에 명시. (c) 중복 docstring 은 한쪽에만 두어 drift 를 막을 것. (d) 지금 당장 필요한 것이 `multiply` 뿐이라면, 클래스 도입은 별도 PR 로 분리하고 이 PR 은 `multiply` 추가만 담는 편이 리뷰 비용과 회귀 위험 모두를 줄인다.

### Issue 2

- Severity: MEDIUM
- File: `app/calculator.py`, `tests/test_calculator.py`
- Line: `app/calculator.py:73` (`def multiply`) / `tests/test_calculator.py:28` (`test_multiply_returns_product`)
- Reason: 새로 추가된 공개 함수 `multiply` 의 테스트가 `multiply(2, 3) == 6` 단 한 줄이다. 같은 파일의 동급 함수들과 비교하면 커버리지가 눈에 띄게 얕다 — `test_add_returns_sum` 과 `test_subtract_returns_difference` 는 각각 양수·부호 반전·0 케이스 3건을 검증한다. 현재 테스트는 부호 처리(`multiply(-2, 3)`), 0 흡수(`multiply(5, 0)`), 소수 연산(`multiply(2.5, 4)`) 을 전혀 덮지 않는다. 지금 구현이 `a * b` 로 올바르기 때문에 이 갭이 결함을 감추고 있지는 않지만, 이후 이 함수가 수정될 때 회귀를 잡아줄 안전망이 얇다.
- Recommendation: `test_multiply_returns_product` 에 최소한 음수 한 케이스, 0 한 케이스, 소수 한 케이스를 추가해 기존 `add` / `subtract` 테스트와 동일한 수준으로 맞출 것. 예: `assert multiply(-2, 3) == -6`, `assert multiply(5, 0) == 0`, `assert multiply(2.5, 4) == 10`.

### Issue 3

- Severity: LOW
- File: PR title / description, `app/calculator.py:73`
- Line: —
- Reason: PR title 이 `refactor:` 로 되어 있지만 실제로는 동작 보존적 리팩터링과 신규 공개 API(`multiply`) 추가가 한 커밋에 섞여 있다. 리팩터링과 기능 추가가 섞이면 나중에 회귀가 발생했을 때 `git bisect` 나 revert 로 원인을 좁히기 어렵다. 순수 리팩터링 부분만 되돌리려 해도 `multiply` 까지 같이 사라진다.
- Recommendation: 커밋/PR 을 `feat: add multiply` 와 `refactor: introduce Calculator namespace` 두 개로 분리하거나, 최소한 title 을 실제 내용에 맞게(예: `feat(calculator): add multiply and consolidate ops into Calculator`) 조정할 것. 이것만으로 merge 를 막을 사안은 아니다.

### Issue 4

- Severity: LOW
- File: `app/calculator.py`
- Line: 11
- Reason: 모듈에 `__all__` 이 정의되어 있지 않아, 이 PR 이후 `from app.calculator import *` 는 의도치 않게 `Calculator` 까지 export 한다. 공개 표면이 명시적으로 통제되지 않는다.
- Recommendation: `__all__` 을 추가해 의도한 공개 이름만 노출할 것. Issue 1 의 (b) 와 함께 처리하면 된다.

## Merge Recommendation

**지금 자동으로 merge 하지 말고 사람의 설계 판단을 거칠 것을 권한다.** 이 PR 은 기능적으로 안전하다 — 기존 4개 함수의 동작·예외가 완전히 보존됨을 484개 입력 조합으로 확인했고, 테스트도 11개 전부 통과하며 호출부 호환성도 유지된다. 따라서 merge 해도 런타임 회귀가 발생할 가능성은 낮다. 다만 `multiply` 한 줄을 위해 모듈을 클래스 구조로 재편하고 공개 진입점을 이중화하는 것은 코드 결함이 아니라 **팀이 결정해야 할 아키텍처 방향**이다. 담당자가 (1) `Calculator` 이중 API 를 앞으로 유지할 것인지, (2) 리팩터링을 `multiply` 추가와 분리할 것인지 두 가지만 확인해 주면, 그 결정에 따라 그대로 merge 하거나 범위를 축소해 재제출하면 된다.

---

## Reviewer Notes — Benchmark 오염 방지 고지 (§7)

리뷰 과정에서 파일 탐색(`find`)과 PR metadata 조회 결과로 다음 **이름**을 보게 되었다.

```text
prompt/pr-005-unnecessary-refactor.md      (파일명만 노출, 내용 미열람)
experiment/pr-005-unnecessary-refactor     (PR head branch 이름)
```

두 이름에 포함된 `unnecessary-refactor` 라벨은 expected outcome 을 암시할 수 있다. 해당 task 정의 파일, `benchmark/README.md`, `benchmark/reviews/*`, 다른 PR 및 그 리뷰 결과는 **일절 열람하지 않았다.** 위 라벨 역시 판단 근거에서 제외했으며, 본 리뷰의 결론은 PR title/description, 실제 diff, `app/` · `tests/` 소스, 그리고 직접 실행한 pytest 및 differential 검증 결과만을 근거로 도출했다. (head branch 이름은 PR metadata 의 일부라 회피가 불가능하다.)

§9 / §10 준수: 코드·테스트를 수정하지 않았고, commit·push·merge 를 수행하지 않았다. pytest 는 작업 트리를 건드리지 않도록 `git archive` 로 추출한 별도 임시 디렉터리에서 실행했다.
