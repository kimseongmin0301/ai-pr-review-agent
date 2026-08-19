# AI PR Review

## Decision

REQUEST_CHANGES

## Confidence

0.90

## Summary

PR #4 (`refactor: normalize discount calculation output`)는 `calculate_discount()`의 반환식 한 줄만 바꾼다.

```diff
- return price * (100 - discount_percent) / 100
+ return round(price * (1 - discount_percent / 100), 2)
```

`refactor:`라는 title과 "반환식을 정리했습니다"라는 설명은 동작 보존을 암시하지만, 이 한 줄은 서로 다른 **두 가지 동작 변경**을 동시에 포함한다.

1. 결과를 무조건 소수점 둘째 자리로 `round()` 한다 (반올림 정책이 새로 생김).
2. 곱셈보다 나눗셈을 먼저 수행하도록 연산 순서를 바꿔, 기존 식이 피하고 있던 부동소수점 표현 오차를 새로 들여온다.

(2)는 설명에 언급조차 없고, 수치적으로 기존 식보다 **엄격하게 나쁘다.** (1)은 설명에 언급되어 있으나 docstring에 반영되지 않았고, 반올림 정책이 정의되지 않은 채 `float` 기반 `round()`에 위임되어 있다. 그 결과 **0% 할인이 더 이상 항등이 아니며, 할인 결과가 원래 price보다 커지는 입력이 존재한다.**

기존 테스트 10개는 모두 통과하지만, 이는 안전성의 근거가 되지 못한다. 10개 테스트가 사용하는 입력은 정확한 결과가 모두 정수(`80`, `225`, `100`, `0`)여서 새로 추가된 반올림 경로를 전혀 통과하지 않는다. 즉 **PASS는 "이 변경이 안전하다"가 아니라 "이 변경을 검증하는 테스트가 없다"를 의미한다.**

아래 수치는 모두 PR head branch에서 직접 실행해 확인했다.

| price | discount | 기존 결과 | PR 결과 | 차이 |
| --- | --- | --- | --- | --- |
| `19.99` | 10 | `17.991` | `17.99` | `-0.001` |
| `5.35` | 50 | `2.675` | `2.67` | `-0.005` |
| `1234.567` | 15 | `1049.38195` | `1049.38` | `-0.00195` |
| `0.001` | 50 | `0.0005` | `0.0` | 전액 소실 |
| `0.996` | **0** | `0.996` | `1.0` | **price보다 커짐** |
| `0.001` | **0** | `0.001` | `0.0` | **전액 소실** |
| `12345678.91` | 7 | `11481481.3863` | `11481481.39` | `+0.0037` |

소수점 2자리 price 입력을 전수 비교하면, `discount_percent`가 7/13/33일 때 **약 99%의 입력에서 반환값이 달라진다** (297,000 / 299,997). 한 줄 "정리"가 사실상 모든 fractional price 호출부의 반환값을 바꾼다.

## Test Result

- command: `python -m pytest -q` (PR head `401a09d`를 별도 git worktree에 checkout 후 실행)
- result: PASS / exit status 0
- passed: 10
- failed: 0
- error: 0

추가 검증: `git diff main...<pr-4-head>` 와 `gh pr diff 4` 를 교차 확인했고 두 diff는 완전히 동일하다 (`app/calculator.py`, 1 file changed, 1 insertion, 1 deletion). PR 설명의 변경 규모 주장과도 일치한다.

**테스트 결과 해석:** PASS이지만 diff에 결함이 있다. 아래 Issue 5 참고 — 현재 테스트 스위트는 새로 도입된 반올림 경로를 한 번도 실행하지 않는다.

## Issues

### Issue 1 — 0% 할인이 항등이 아니게 되고, 결과가 원래 price를 초과할 수 있다

- Severity: **HIGH**
- File: `app/calculator.py`
- Line: 46
- Reason:
  `round()`가 `discount_percent`와 무관하게 **무조건** 적용된다. 따라서 할인을 전혀 적용하지 않는 경우에도 price가 변형된다.

  ```text
  calculate_discount(0.996, 0)  ->  1.0     # price(0.996)보다 크다
  calculate_discount(0.999, 0)  ->  1.0
  calculate_discount(9.999, 0)  ->  10.0
  calculate_discount(0.001, 0)  ->  0.0     # price 전액 소실
  calculate_discount(0.005, 0)  ->  0.01
  ```

  "할인 함수"가 원래 금액보다 **큰 값**을 돌려주는 것은 반올림 정책과 무관하게 어떤 기준으로도 정당화되지 않는다. 또한 `test_calculate_discount_with_zero_percent_returns_original_price`가 문서화하고 있는 계약("0%면 원래 price")은 `price=100`에서만 우연히 성립하고, 센트 미만 단위를 가진 price에서는 깨진다. 이 테스트는 정수 입력만 쓰기 때문에 초록색으로 남는다.

  `calculate_discount(0.001, 50) -> 0.0` 처럼 sub-cent 금액이 0으로 사라지는 것도 금액 계산에서는 조용한 데이터 손실이다.
- Recommendation:
  반올림을 함수 내부에 무조건 박아 넣지 말고 다음 중 하나를 택한다.
  1. 반올림 책임을 호출부/표시 계층으로 옮기고 `calculate_discount()`는 정확한 값을 반환한다 (기존 동작 유지).
  2. 반올림을 유지해야 한다면 `round`의 자릿수를 파라미터화하고(`ndigits=None`을 기본값으로 두어 opt-in), 최소한 `discount_percent == 0`일 때 `price`를 그대로 반환하며, 반환값이 절대 `price`를 초과하지 않음을 보장한다.

  어느 쪽을 택하든 `calculate_discount(p, 0) == p`, `0 <= result <= price` 를 property test로 고정한다.

### Issue 2 — 반올림 정책이 정의되지 않았고 float 기반 `round()`에 위임되어 예측 불가능하다

- Severity: **HIGH**
- File: `app/calculator.py`
- Line: 46
- Reason:
  Python 내장 `round()`는 (a) banker's rounding(half-to-even)이며 (b) 실제로는 **float 표현값**을 기준으로 반올림한다. 두 특성이 겹치면 정확히 절반인 값의 처리 방향이 사람의 직관과 어긋나고, 인접한 입력끼리도 방향이 갈린다.

  ```text
  exact 2.675 -> 2.67   (내림)
  exact 0.135 -> 0.14   (올림)
  exact 0.125 -> 0.12   (내림)
  exact 1.005 -> 1.0    (내림)
  exact 0.045 -> 0.04   (내림)
  ```

  금액 계산에서 "절반을 어느 쪽으로 보낼지"는 구현 부작용으로 결정될 사안이 아니라 명시적으로 선택되어야 하는 정책이다(회계 규칙, 고객 유리/불리 방향). 현재 diff는 이 정책을 **암묵적으로, 그리고 float 표현 오차에 의존하는 형태로** 도입한다.

  또한 이 정책 변경은 PR description에 "소수점 둘째 자리로 맞춰 반환합니다"라고만 적혀 있고, `calculate_discount()`의 docstring에는 반영되지 않았다 (docstring은 여전히 `calculate_discount(100, 20) -> 80.0`만 예시로 들고 반올림을 언급하지 않는다).
- Recommendation:
  반올림이 요구사항이라면 정책을 명시한다. 금액이면 `decimal.Decimal` + `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`를 사용해 float 표현 오차와 half-to-even 문제를 동시에 제거한다. 그리고 선택한 정책(자릿수, 방향, tie-breaking)을 docstring에 문서화하고, 경계값(`2.675`, `0.135`, `1.005`)에 대한 테스트를 추가한다.

### Issue 3 — 연산 순서 변경이 기존 식이 피하던 부동소수점 오차를 새로 도입한다 (설명에 언급 없음)

- Severity: **MEDIUM**
- File: `app/calculator.py`
- Line: 46
- Reason:
  기존 식 `price * (100 - discount_percent) / 100`은 **정수 뺄셈 → 곱셈 → 나눗셈** 순서로, 마지막 한 번만 나눈다. 새 식 `price * (1 - discount_percent / 100)`은 **먼저 `discount_percent / 100`을 float로 나눠** 표현 불가능한 값(예: `7/100 -> 0.07`, 내부적으로 `0.07000000000000000666...`)을 만든 뒤 곱한다. 즉 오차가 곱셈에 의해 증폭된다.

  이 오차는 `round()`에 대체로 가려지지만 항상 가려지지는 않는다. 두 식에 **동일하게** `round(..., 2)`를 적용해 비교해도(= 반올림 효과를 제거하고 연산 순서 효과만 남겨도) 80만 개 샘플 중 **2,933건에서 결과가 갈린다.**

  ```text
  price=0.5,  d=7%  : round(기존식)=0.47  PR=0.46
  price=0.5,  d=33% : round(기존식)=0.34  PR=0.33
  price=2.5,  d=7%  : round(기존식)=2.33  PR=2.32
  price=1.5,  d=99% : round(기존식)=0.01  PR=0.02
  ```

  PR description은 이 연산 순서 변경을 "비율로 직접 적용하는 형태로 바꿨다"고만 서술하며 정밀도 영향은 언급하지 않는다. 가독성 측면의 근거는 이해할 수 있으나, 수치적으로는 기존 형태가 더 정확하므로 이는 개선이 아니라 후퇴다.
- Recommendation:
  반올림 여부와 별개로, 곱셈을 먼저 하고 나눗셈을 마지막에 한 번만 하는 기존 형태(`price * (100 - discount_percent) / 100`)를 유지한다. 가독성이 목적이라면 식을 바꾸는 대신 중간 변수에 이름을 붙인다(`remaining_percent = 100 - discount_percent`).

### Issue 4 — 숫자 타입 계약이 깨진다 (`Decimal` 입력이 TypeError로 실패)

- Severity: **MEDIUM**
- File: `app/calculator.py`
- Line: 46
- Reason:
  `discount_percent / 100`이 항상 `float`를 만들기 때문에, `price`가 `Decimal`이면 `Decimal * float` 연산에서 예외가 발생한다. 기존 식은 `Decimal * int / int`이므로 정상 동작했고 정확한 `Decimal`을 반환했다.

  ```text
  기존: calculate_discount(Decimal("19.99"), 10) -> Decimal('17.991')
  PR  : calculate_discount(Decimal("19.99"), 10) -> TypeError:
        unsupported operand type(s) for *: 'decimal.Decimal' and 'float'

  기존: calculate_discount(Fraction(1999,100), 10) -> Fraction(17991, 1000)
  PR  : calculate_discount(Fraction(1999,100), 10) -> 17.99   (조용히 float로 격하)
  ```

  현재 repository 안에는 `Decimal`로 호출하는 코드가 없어(호출부는 `tests/test_calculator.py`뿐) 즉시 깨지는 곳은 없다. 그러나 `calculate_discount()`는 금액을 다루는 공개 함수이고 금액 코드에서 `Decimal`은 표준적인 선택이므로, 이는 실질적인 공개 계약 축소다. 그리고 `TypeError`는 이 함수가 문서화한 예외(`ValueError` 두 가지)에 포함되지 않는다.
- Recommendation:
  `price`의 숫자 타입을 보존하려면 `discount_percent`를 float로 나누지 않는 형태를 유지한다(Issue 3의 권고와 동일). 반대로 float-only가 의도된 계약이라면 docstring과 type hint에 명시하고, 지원 타입 밖의 입력을 명시적으로 거부한다.

### Issue 5 — 새로 도입된 반올림 동작을 검증하는 테스트가 전혀 없다

- Severity: **MEDIUM**
- File: `tests/test_calculator.py`
- Line: 39-64
- Reason:
  `calculate_discount` 관련 테스트 6개가 사용하는 입력은 `(100,20)`, `(250,10)`, `(100,0)`, `(100,100)` 뿐이며, 정확한 결과가 각각 `80`, `225`, `100`, `0`으로 모두 소수점 이하가 없다. 따라서 `round(..., 2)`는 **어떤 테스트에서도 값을 바꾸지 않는다.** 이 PR의 핵심 변경(반올림)과 부작용(정밀도 손실, 연산 순서 오차)은 전부 테스트되지 않은 경로에 있다.

  결과적으로 PR description의 "기존 테스트는 모두 통과했습니다"는 사실이지만, 이 변경의 안전성에 대한 증거로는 성립하지 않는다. 이 파일의 docstring이 스스로 밝힌 의도("a legitimate refactor stays green while a behavioural regression turns red")가 이 변경에 대해서는 작동하지 않는다.

  또한 저자가 테스트를 수정하지 않은 것 자체는 올바른 태도지만, 동작을 바꾸면서 그 동작을 고정하는 테스트를 **추가하지도** 않았다.
- Recommendation:
  반올림 정책을 확정한 뒤 다음을 추가한다.
  - `calculate_discount(19.99, 10)`처럼 정확한 결과가 2자리를 넘는 케이스의 기대값
  - tie-breaking 경계값(`5.35, 50` → `2.675`)
  - `calculate_discount(0.996, 0) == 0.996` 같은 0%-항등 케이스
  - `0 <= result <= price` property test

### Issue 6 — docstring이 새 동작을 반영하지 않는다

- Severity: **LOW**
- File: `app/calculator.py`
- Line: 33-41
- Reason:
  docstring은 여전히 "Return `price` after applying `discount_percent` percent off"이고 예시는 `calculate_discount(100, 20) -> 80.0`뿐이다. 반올림한다는 사실, 자릿수, 반환 타입이 항상 float가 된다는 점이 문서화되지 않았다. 동작 변경이 PR description에만 존재하고 코드에는 남지 않으면, 이후 유지보수자가 반올림을 의도된 계약이 아닌 실수로 오해할 수 있다.
- Recommendation:
  반올림을 유지한다면 docstring에 자릿수·반올림 방향·반환 타입을 명시하고, 반올림이 관찰되는 예시(`calculate_discount(19.99, 10) -> 17.99`)를 추가한다.

## Merge Recommendation

**현재 상태로 Merge하지 않는 것을 권장한다.**

`refactor:` / "반환식 정리"로 제시되었으나 실제로는 동작 변경 PR이다. 소수점 2자리 price 입력 기준으로 약 99%의 호출에서 반환값이 달라지며, 그중 일부는 반올림 정책과 무관하게 명백한 결함이다 — `calculate_discount(0.996, 0)`이 `1.0`(원래 price보다 큼)을 돌려주고, `calculate_discount(0.001, 50)`이 `0.0`(전액 소실)을 돌려준다. 여기에 설명에 언급되지 않은 연산 순서 변경이 기존 식보다 정밀도를 떨어뜨리고, `Decimal` 입력은 `TypeError`로 깨진다.

pytest 10 passed는 이 변경을 검증하지 못한다. 테스트 입력의 정확한 결과가 모두 정수여서 새 반올림 경로를 한 번도 지나지 않기 때문이다.

Merge 전에 필요한 것: (1) 반올림이 실제 요구사항인지 확인, (2) 요구사항이라면 `Decimal` + 명시적 rounding mode로 정책을 확정하고 0%-항등 및 `result <= price` 불변식을 보장, (3) 연산 순서는 기존 형태 유지, (4) 반올림 동작을 고정하는 테스트 추가. 반올림이 요구사항이 아니라면 이 diff는 되돌려야 한다.

---

### Review Transparency Note

- 이 리뷰는 PR metadata(number/title/description/base/head/changed files), 실제 diff (`gh pr diff 4` 및 `git diff main...<head>` 교차 확인), 관련 소스(`app/calculator.py`, `tests/test_calculator.py`), 호출부 검색 결과, PR head에서 직접 실행한 pytest 결과 및 직접 수행한 수치 비교만을 근거로 작성했다.
- benchmark task 정의 파일(`prompt/pr-00*.md`), `benchmark/README.md`, `benchmark/reviews/*`의 **내용은 읽지 않았고**, 다른 PR의 diff나 리뷰 결과도 참조하지 않았다.
- 다만 PR metadata에 포함된 head branch 이름이 `experiment/pr-004-hidden-bug`임을 확인했다. 이 문자열은 결함의 존재나 성격에 대한 근거로 사용하지 않았다. 위 모든 Issue는 diff와 직접 실행한 수치 검증만으로 독립적으로 도출되었으며, branch 이름이 달랐어도 결론은 동일하다.
- 코드, 테스트, PR은 수정하지 않았고 merge하지 않았다. 테스트는 현재 작업 트리를 건드리지 않기 위해 별도 git worktree에서 실행했다.
