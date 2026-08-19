# INIT — AI PR Review Agent Baseline

## 목적

이 문서는 `ai-pr-review-agent` 프로젝트의 **최초 정상 baseline**을 구축하기 위한 초기 작업 정의입니다.

이 프로젝트의 최종 목표는 Pull Request가 생성되었을 때 자동으로 다음 흐름을 수행하는 AI Code Review 시스템을 만드는 것입니다.

```text
Pull Request
→ Test
→ Diff Collection
→ AI Reviewer
→ APPROVE / REQUEST_CHANGES / HUMAN_REVIEW
→ PR Review
```

이번 INIT 단계에서는 아직 AI Reviewer 자체를 구현하지 않습니다.

이번 단계의 목표는 오직:

```text
정상 코드
+
정상 테스트
+
Reviewer 인터페이스
+
PR Benchmark 준비 구조
```

를 만드는 것입니다.

---

## 프로젝트명

```text
ai-pr-review-agent
```

---

## 기술 스택

Python 3.12 기준

필수:

- Python
- pytest

이번 단계에서는 다음을 사용하지 마세요.

- FastAPI
- Database
- Docker
- RAG
- OpenAI API
- GitHub Actions
- 외부 서비스
- 불필요한 dependency

최대한 단순하게 구성하세요.

---

## Repository 구조

최소한 다음 구조를 만드세요.

```text
ai-pr-review-agent/
├── app/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   └── test_calculator.py
├── reviewer/
│   ├── __init__.py
│   └── reviewer.py
├── benchmark/
│   └── README.md
├── requirements.txt
├── .gitignore
└── README.md
```

필요하다면 작은 보조 파일을 추가할 수 있지만,
불필요하게 구조를 확장하지 마세요.

---

# 1. 정상 Baseline 코드

`app/calculator.py`에 다음 기능을 구현하세요.

## add

```python
add(a, b)
```

동작:

```text
add(2, 3) -> 5
```

---

## subtract

```python
subtract(a, b)
```

동작:

```text
subtract(5, 3) -> 2
```

---

## divide

```python
divide(a, b)
```

정상적인 나눗셈을 수행합니다.

단:

```text
b == 0
```

이면 반드시 다음 예외를 발생시키세요.

```python
ValueError("Cannot divide by zero")
```

---

## calculate_discount

```python
calculate_discount(price, discount_percent)
```

정상 가격과 할인율을 받아 최종 가격을 반환합니다.

계산식:

```text
price * (1 - discount_percent / 100)
```

Validation:

```text
price < 0
→ ValueError("Price must be non-negative")
```

```text
discount_percent < 0 또는 discount_percent > 100
→ ValueError("Discount percent must be between 0 and 100")
```

예:

```text
calculate_discount(100, 20)
→ 80
```

계산 결과를 임의로 반올림하거나 정수로 변환하지 마세요.

---

# 2. 테스트

`tests/test_calculator.py`를 작성하세요.

최소 다음 10개 케이스를 검증하세요.

1. add 정상 동작
2. subtract 정상 동작
3. divide 정상 동작
4. divide by zero
5. calculate_discount 정상 동작
6. 음수 price
7. 100 초과 discount
8. 음수 discount
9. discount 0
10. discount 100

테스트는 구현 세부사항보다 **외부 동작과 계약**을 검증해야 합니다.

기존 함수의 반환값과 exception message를 명확하게 검증하세요.

---

# 3. Reviewer 기본 인터페이스

이번 단계에서는 실제 LLM API를 호출하지 않습니다.

다만 향후 다음 두 구현을 교체할 수 있어야 합니다.

```text
Single-Agent Reviewer
Multi-Agent Reviewer
```

따라서 `reviewer/reviewer.py`에는 최소한 다음 개념을 정의하세요.

## ReviewResult

필드:

```text
decision
confidence
summary
issues
```

향후 `decision`은 다음 세 값을 사용합니다.

```text
APPROVE
REQUEST_CHANGES
HUMAN_REVIEW
```

그리고 다음 입력을 받을 수 있는 review 함수 또는 인터페이스를 정의하세요.

```text
diff
test_result
pr_description
```

이번 단계에서는 실제 Review 로직은 구현하지 않습니다.

`NotImplementedError` 또는 명확한 placeholder를 사용하세요.

과도한 abstraction은 만들지 마세요.

---

# 4. Benchmark 문서

`benchmark/README.md`에는 향후 생성할 실험 PR 유형을 정리하세요.

최소 다음 5개를 포함하세요.

## PR-001 — Valid Change

정상적인 작은 기능 추가

예상 결과:

```text
APPROVE
```

---

## PR-002 — Obvious Logic Bug

테스트는 통과하지만 diff만 보면 명확한 로직 오류

예상 결과:

```text
REQUEST_CHANGES
```

---

## PR-003 — Test-detectable Regression

기존 테스트가 실패하는 regression

예상 결과:

```text
REQUEST_CHANGES
```

---

## PR-004 — Hidden Behavior Regression

기존 visible test는 통과하지만 기존 동작 계약을 미묘하게 깨는 변경

예상 결과:

```text
REQUEST_CHANGES
```

---

## PR-005 — Unnecessary Large Refactor

기능적으로는 정상이고 테스트도 통과하지만 요구사항보다 변경 범위가 지나치게 큰 PR

예상 결과:

```text
HUMAN_REVIEW
```

또는:

```text
APPROVE + scope warning
```

각 PR의 실험 목적도 간단히 설명하세요.

---

# 5. Root README

루트 `README.md`에는 최소 다음 내용을 작성하세요.

- 프로젝트 목적
- AI PR Review Agent가 해결하려는 문제
- 현재 단계
- Repository 구조
- 테스트 실행 방법
- 향후 Workflow
- Benchmark 방향

향후 Workflow는 다음과 같이 표현하세요.

```text
Pull Request
→ Test
→ Diff Collection
→ AI Reviewer
→ APPROVE / REQUEST_CHANGES / HUMAN_REVIEW
→ PR Review
```

이번 INIT 단계에서는 아직 위 자동화가 구현되지 않았음을 명확히 적으세요.

---

# 6. requirements.txt

필요한 dependency만 추가하세요.

현재 단계에서는 가능하면 다음만 사용하세요.

```text
pytest
```

불필요한 dependency를 추가하지 마세요.

---

# 7. .gitignore

Python 프로젝트에 필요한 최소 항목을 추가하세요.

예:

```text
__pycache__/
*.pyc
.venv/
.pytest_cache/
.env
```

필요한 일반 항목은 추가할 수 있지만 과도하게 늘리지 마세요.

---

# 8. 검증

모든 구현 후 반드시 실행하세요.

```bash
pytest -q
```

모든 테스트가 통과해야 합니다.

이번 INIT baseline은 향후 모든 실험 PR의 기준점이므로,
테스트 실패 상태로 작업을 종료하면 안 됩니다.

---

# 9. Git 작업

현재 Repository 상태를 먼저 확인하세요.

```bash
git status
git branch --show-current
```

작업 완료 후 변경 파일을 검토하고,
불필요한 파일이 포함되지 않았는지 확인하세요.

commit message:

```text
chore: initialize AI PR review benchmark
```

원격 Repository와 push 권한이 있다면 `main`에 push하세요.

```text
main = 정상 baseline
```

향후 모든 실험 브랜치는 이 `main`에서 독립적으로 생성합니다.

```text
main
├── experiment/pr-001-valid
├── experiment/pr-002-obvious-bug
├── experiment/pr-003-test-failure
├── experiment/pr-004-hidden-bug
└── experiment/pr-005-unnecessary-refactor
```

기존 다른 Repository나 프로젝트는 수정하지 마세요.

---

# 10. 중요한 제한

반드시 지켜주세요.

- LLM API 구현 금지
- GitHub Actions 구현 금지
- 실제 PR 자동 Review 구현 금지
- Multi-Agent 구현 금지
- FastAPI 추가 금지
- DB 추가 금지
- Docker 추가 금지
- 불필요한 dependency 금지
- 과도한 설계/추상화 금지
- 테스트를 통과시키기 위한 꼼수 금지

이번 INIT 작업은 향후 AI Reviewer를 검증하기 위한 **정상 기준점 생성**이 목적입니다.

---

# 11. 최종 보고

작업 완료 후 채팅에는 전체 코드를 붙이지 마세요.

다음만 보고하세요.

1. 생성/수정한 파일 목록
2. `pytest -q` 결과
3. 최종 테스트 개수
4. commit 여부
5. push 여부
6. 현재 branch
