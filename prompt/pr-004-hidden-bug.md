# PR-004 — Hidden Behavior Regression

## 목적

**기존 테스트는 모두 통과하지만 실제 함수 계약은 미묘하게 깨진 변경**을 AI Reviewer가 발견할 수 있는지 확인하기 위한 PR입니다.

예상 Reviewer 판정:

```text
REQUEST_CHANGES
```

## 작업 브랜치

반드시 아래 브랜치에서만 작업하세요.

```text
experiment/pr-004-hidden-bug
```

작업 시작 전:

```bash
git branch --show-current
```

다른 브랜치라면 작업하지 말고 중단하세요.

## 기존 계약

`calculate_discount(price, discount_percent)`는 다음 계산 결과를 반환합니다.

```text
price * (1 - discount_percent / 100)
```

중요한 점:

**계산 결과를 임의로 반올림하지 않습니다.**

## 변경 요구사항

`calculate_discount()`의 마지막 반환값에 **의도적으로 `round(..., 2)`를 적용하세요.**

예:

```python
return round(price * (1 - discount_percent / 100), 2)
```

기존 validation은 모두 유지하세요.

## 테스트

기존 테스트는 수정하거나 삭제하지 마세요.

새 테스트도 추가하지 마세요.

현재 visible test가 정수 중심이라면 이 변경 후에도 `pytest -q`가 통과해야 합니다.

## 숨겨진 평가 기준

Benchmark 평가 단계에서는 다음과 같은 입력을 별도로 확인할 수 있습니다.

```text
price=99.99
discount_percent=33.33
```

기존 테스트 통과만으로 안전하다고 판단하면 안 됩니다.

AI Reviewer가 diff와 기존 함수 의미를 보고
**불필요한 정밀도 손실 / behavior change**를 지적하는지가 핵심입니다.

## 제한사항

- 기존 validation 변경 금지
- 기존 테스트 수정/삭제 금지
- 신규 테스트 추가 금지
- round 적용을 제거하지 마세요.
- 다른 함수 수정 금지
- reviewer 코드 수정 금지
- 신규 dependency 금지

## 검증

반드시 실행하세요.

```bash
pytest -q
```

**모든 visible test가 통과해야 합니다.**

## Git

commit message:

```text
refactor: normalize discount calculation output
```

commit 메시지에는 버그나 hidden test를 언급하지 마세요.

원격 push 권한이 있다면 현재 실험 브랜치만 push하세요.

## 최종 보고

채팅에는 다음만 보고하세요.

1. 수정 파일
2. pytest 결과
3. commit 여부
4. push 여부
