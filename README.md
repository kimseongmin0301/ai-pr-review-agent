# AI PR Review Agent (AI PR 리뷰 에이전트)

Claude Code를 이용해 Pull Request를 자동으로 검토하고, **Merge 가능 여부를 판단하는 AI Code Review Workflow**를 실험한 프로젝트입니다.

---

# 결론 (Conclusion)

이번 실험에서는 **Claude Code 기반 Single Reviewer가 준비한 5개 PR Benchmark를 모두 기대한 방향으로 판정했습니다.**

| PR | 검증 목적 | 기대 판정 (Expected) | 실제 판정 (Actual) | 결과 |
|---|---|---:|---:|---:|
| PR-001 | 정상 변경 | APPROVE (승인 가능) | APPROVE | ✅ |
| PR-002 | 테스트는 통과하지만 명확한 로직 버그 | REQUEST_CHANGES (수정 필요) | REQUEST_CHANGES | ✅ |
| PR-003 | 테스트에서 직접 발견되는 regression (회귀 오류) | REQUEST_CHANGES (수정 필요) | REQUEST_CHANGES | ✅ |
| PR-004 | 테스트는 통과하지만 기존 동작을 깨는 hidden regression (회귀 오류) (테스트에서 바로 드러나지 않는 동작 회귀) | REQUEST_CHANGES (수정 필요) | REQUEST_CHANGES | ✅ |
| PR-005 | 기능은 정상이나 요구사항 대비 과도한 refactor | HUMAN_REVIEW (사람 검토 필요) | HUMAN_REVIEW | ✅ |

**Decision Accuracy (판정 정확도): 5 / 5**

이번 결과에서 가장 의미 있었던 부분은 단순히 테스트 실패를 감지한 것이 아니라,

- 테스트가 통과해도 실제 구현이 틀린 경우
- visible test (일반 테스트)가 놓친 behavior regression (회귀 오류) (동작 회귀)
- 기능 자체는 정상이어도 변경 범위가 과도한 경우

까지 서로 다른 유형으로 구분했다는 점입니다.

따라서 현재 실험 범위에서는 다음과 같이 정리할 수 있습니다.

> **Claude Code Single Reviewer는 단순한 테스트 결과 확인을 넘어, PR diff (PR 변경 내역)와 코드 문맥을 함께 분석해 Merge 가능 여부를 판단할 수 있었습니다.**

하지만 이번 실험의 결론을 단순히 **“AI가 코드 리뷰를 잘하니 이제 사람 없이도 된다”**로 정리하고 싶지는 않습니다.

이번 결과를 통해 AI는 반복적인 diff (변경 내역) 확인, 테스트 결과 해석, 눈에 잘 띄지 않는 오류 탐지, 회귀 가능성 확인처럼 사람이 놓치기 쉬운 부분을 빠르게 점검하는 데 충분히 도움이 될 수 있다는 점을 확인했습니다. 특히 PR-002와 PR-004처럼 `pytest`가 통과했음에도 실제 코드에는 문제가 있는 경우를 찾아낸 점은 AI Reviewer의 실용적인 장점을 보여줍니다.

반면 PR-005처럼 코드 자체는 정상적으로 동작하지만, 변경 범위가 적절한지 또는 새로운 구조를 도입하는 것이 팀의 방향과 맞는지를 판단해야 하는 경우에는 하나의 기술적인 정답만 존재하지 않습니다. 이런 문제는 프로젝트의 맥락, 팀의 convention (개발 규칙), 향후 유지보수 방향까지 알고 있는 사람의 판단이 필요합니다.

그래서 AI에게 **모든 판단과 책임을 맡기는 것도 적절하지 않고**, 반대로 AI가 완벽하지 않다는 이유로 개발이나 리뷰 과정에서 **AI 활용 자체를 불신하는 것도 좋은 선택은 아니라고 생각합니다.**

AI가 잘하는 부분은 적극적으로 활용하고, 사람이 판단해야 하는 부분은 명확하게 남겨두는 식으로 역할을 나누는 것이 현실적인 방향이라고 봤습니다.

```text
반복적인 코드 변경 확인
Diff 분석
테스트 결과 해석
잠재 버그 / 회귀 탐색
        ↓
AI 활용

설계 방향
비즈니스 / 프로젝트 맥락
변경 범위의 적절성
위험도가 높은 변경
최종 Merge 결정
        ↓
Human Review (사람 검토)
```

결국 중요한 것은 **“AI가 사람을 대체할 수 있는가”**가 아니라,

> **어디까지 AI에게 맡기고, 어느 지점부터 사람이 검증해야 가장 효율적이고 안전한가를 찾아가는 것**

이라고 생각합니다.

AI 활용이 빠르게 보편화되는 환경에서는 무조건적인 신뢰와 무조건적인 불신 중 하나를 선택하기보다, 실제 사용과 검증을 통해 적절한 경계를 찾고 그 범위를 계속 조정해 나가는 것이 더 중요하다고 봤습니다.

이번 프로젝트에서는 그 타협점을 다음과 같이 두었습니다.

```text
AI Reviewer
→ 코드 변경 분석
→ 테스트 결과 확인
→ 문제점 탐지
→ APPROVE (승인 가능)
   / REQUEST_CHANGES (수정 필요)
   / HUMAN_REVIEW (사람 검토 필요) 제안

Human
→ AI가 제시한 근거 확인
→ 설계 / 맥락 판단
→ 최종 Merge 결정
```

즉, **AI는 Reviewer이자 의사결정 보조자이고, 최종 책임과 결정은 사람에게 남겨두는 구조가 현재로서는 가장 현실적이라고 판단했습니다.**

다만 이 프로젝트는 5개의 고정 Benchmark (벤치마크 / 평가 시나리오)를 이용한 소규모 실험이며, 모든 Repository와 모든 유형의 PR에서 동일한 성능을 보장한다는 의미는 아닙니다.

---

# 사용 모델 및 역할 (Models & Roles)

이번 프로젝트에서는 계획과 구현 역할을 분리했습니다.

| 역할 | 사용 모델 | 역할 |
|---|---|---|
| Planner (계획 수립) | GPT-5.6 Sol — Medium | 실험 구조, Benchmark 설계, Reviewer Workflow 설계 |
| Coding / Execution Agent (코드 작성·실행 에이전트) | Claude Code — Opus High | Repository 수정, 테스트 실행, Commit / Push / PR 생성, Reviewer 실행 |
| Single PR Reviewer (단일 PR 리뷰어) | Claude Code — Opus High | PR metadata, diff, 관련 코드, pytest 결과를 기반으로 Merge 가능 여부 판단 |

별도의 OpenAI API 또는 Anthropic API 직접 호출은 사용하지 않았습니다.

Claude Code 자체를 Coding Agent 및 Reviewer Agent로 사용했습니다.


---

# 실제 실행 방식 (How It Was Executed)

이번 프로젝트는 단순히 결과만 수동으로 정리한 것이 아니라, **Claude Code가 Git Repository와 GitHub MCP를 직접 사용해 각 단계를 수행하도록 구성**했습니다.

전체 실행 흐름은 다음과 같습니다.

```text
1. main에서 정상 baseline (기준 상태) 준비
2. 각 benchmark PR용 experiment branch 생성
3. Claude Code가 작업 문서(prompt/*.md)를 읽고 코드 수정
4. pytest 실행
5. 변경사항 확인
6. commit
7. push
8. Pull Request 생성
9. PR은 merge하지 않고 open 상태 유지
10. 별도의 Claude Code 세션에서 Single Reviewer 실행
11. Reviewer가 PR metadata / diff / 관련 코드 / pytest 결과 분석
12. APPROVE (승인 가능) / REQUEST_CHANGES (수정 필요) / HUMAN_REVIEW (사람 검토 필요) 판정
13. review 결과를 benchmark/reviews/*.md에 저장
14. 최종 merge 여부는 사람이 판단
```

## Benchmark PR 생성 방식

각 PR은 다른 실험의 영향을 받지 않도록 **동일한 기준 상태에서 독립적으로 분기**했습니다.

```text
baseline
├── experiment/pr-001-valid
├── experiment/pr-002-obvious-bug
├── experiment/pr-003-test-failure
├── experiment/pr-004-hidden-bug
└── experiment/pr-005-unnecessary-refactor
```

PR 하나를 만든 뒤 다음 PR을 그 브랜치에서 이어서 만들지 않았습니다.

즉:

```text
PR-001 → PR-002 → PR-003
```

처럼 누적하지 않고,

```text
baseline → PR-001
baseline → PR-002
baseline → PR-003
...
```

형태로 구성했습니다.

이렇게 한 이유는 **앞선 실험의 코드가 다음 실험의 결과에 영향을 주는 것을 막기 위해서**입니다.

## 작업 지시 방식

Claude Code에는 긴 지시를 매번 직접 입력하지 않고, Repository의 Markdown 문서를 작업 기준으로 사용했습니다.

예:

```text
prompt/
├── AGENT_WORKFLOW.md
├── pr-001-valid.md
├── pr-002-obvious-bug.md
├── pr-003-test-failure.md
├── pr-004-hidden-bug.md
└── pr-005-unnecessary-refactor.md
```

실행 시에는 다음과 같이 지시했습니다.

```text
prompt/AGENT_WORKFLOW.md와
현재 작업에 해당하는 prompt/pr-XXX.md를 읽고,
두 문서를 기준으로 전체 작업을 수행해주세요.
```

`AGENT_WORKFLOW.md`에는 공통적으로 다음 규칙을 정의했습니다.

```text
Read Task (작업 문서 읽기)
→ Verify Branch (브랜치 확인)
→ Modify (코드 수정)
→ Test (테스트 실행)
→ Verify Diff (변경사항 검토)
→ Commit
→ Push
→ Create PR (PR 생성)
→ Report (결과 보고)
```

각 PR별 문서에는 실제로 어떤 변경을 만들지, 테스트는 성공해야 하는지 실패해야 하는지, commit message와 PR title은 무엇인지 등을 별도로 정의했습니다.

---

# 테스트 방법 (How It Was Tested)

테스트는 두 층으로 나눴습니다.

```text
1. pytest 기반 자동 테스트
2. Claude Code Single Reviewer의 코드 리뷰
```

둘을 분리한 이유는 **테스트가 통과했다고 해서 PR이 반드시 안전한 것은 아니기 때문**입니다.

## 1. pytest

기본 명령은 다음과 같습니다.

```bash
python -m pytest -q
```

정상 baseline (기준 상태)에서는 모든 기존 테스트가 통과해야 합니다.

각 benchmark PR에서는 실험 목적에 따라 예상 결과가 달랐습니다.

| PR | pytest 기대 결과 | 이유 |
|---|---|---|
| PR-001 | PASS (통과) | 정상 기능 추가 |
| PR-002 | PASS (통과) | 신규 버그 코드에 대한 테스트가 없음 |
| PR-003 | FAIL (실패) | 기존 예외 계약을 깨는 회귀 오류 |
| PR-004 | PASS (통과) | 기존 테스트가 미묘한 동작 변경을 잡지 못함 |
| PR-005 | PASS (통과) | 기능 자체는 정상이고 구조만 과도하게 변경 |

즉 PR-003을 제외하면 대부분 pytest가 통과하도록 설계했습니다.

이렇게 해야 Reviewer가 단순히:

```text
pytest PASS → APPROVE (승인 가능)
pytest FAIL → REQUEST_CHANGES (수정 필요)
```

처럼 판단하는 것이 아니라, **실제 diff와 코드 의미를 분석하는지** 확인할 수 있기 때문입니다.

## 2. Single Reviewer 실행

Reviewer는 Claude Code 자체를 사용했습니다.

별도의 OpenAI API나 Anthropic API 호출 코드는 만들지 않았습니다.

Reviewer 실행 시에는 다음 고정 문서를 먼저 읽도록 했습니다.

```text
prompt/reviewer/SINGLE_REVIEWER.md
```

리뷰 대상 PR마다 **새 Claude Code 세션을 사용**했습니다.

예:

```text
prompt/reviewer/SINGLE_REVIEWER.md를 읽고
PR #6을 Single Reviewer로 독립적으로 검토해주세요.
```

Reviewer가 확인한 정보는 다음과 같습니다.

```text
PR title (PR 제목)
PR description (PR 설명)
Base / Head branch
GitHub PR diff (GitHub PR 변경 내역)
Local git diff (로컬 Git 변경 비교)
변경된 실제 코드
관련 테스트 코드
pytest 실행 결과
```

반대로 아래 정보는 **정답 유출을 막기 위해 읽지 않도록 제한**했습니다.

```text
prompt/pr-*.md
benchmark/README.md
benchmark/reviews/*의 이전 리뷰 결과
다른 PR의 diff 및 리뷰 결과
```

각 PR을 새 세션에서 검토한 이유도 동일합니다.

이전 PR의 판단이나 결론이 다음 PR의 판단에 섞이지 않도록 하기 위해서입니다.

## 3. Reviewer가 직접 수행한 추가 검증

Reviewer는 pytest 결과만 확인하지 않았습니다.

PR 성격에 따라 추가로 다음과 같은 read-only 검증을 수행했습니다.

```text
GitHub PR diff와 local git diff 교차 확인
변경 함수의 실제 구현 확인
Repository 내 호출부 검색
기존 exception behavior 비교
base와 head의 pytest 결과 비교
경계값 / 소수 입력 직접 실행
기존 동작과 변경 후 동작 비교
```

예를 들어 PR-004에서는 pytest가 모두 통과했지만, Reviewer가 직접 소수 입력을 비교해 `round(..., 2)`로 인해 기존 반환값이 달라지는 경우를 확인했습니다.

PR-005에서는 기존 함수들이 실제로 동작 보존적인지 확인하기 위해 base와 head의 반환값 및 예외 동작을 추가로 비교한 뒤, 기능 오류가 아니라 **설계 / 변경 범위 판단 문제**라고 결론냈습니다.

---

# 실험 시나리오 생성 → 리뷰까지의 예시

예를 들어 PR-002의 실행 과정은 다음과 같았습니다.

```text
1. 독립 experiment branch 생성
2. Claude Code가 multiply(a, b)를 추가
3. 구현은 의도적으로 return a + b
4. multiply 테스트는 추가하지 않음
5. pytest 실행 → 10 passed
6. commit / push
7. Pull Request 생성
8. PR은 open 상태 유지
9. 새 Claude Code Reviewer 세션 실행
10. Reviewer가 diff 확인
11. multiply 이름 / docstring과 실제 return a + b 불일치 발견
12. 테스트에 multiply가 없다는 것도 확인
13. REQUEST_CHANGES 판정
```

이 케이스를 통해 **CI 테스트가 통과하더라도 AI Reviewer가 코드 자체의 논리 오류를 탐지할 수 있는지** 확인했습니다.


---

# 프로젝트 목적 (Project Goal)

이 프로젝트의 목표는 배포 자동화가 아닙니다.

목표는 다음과 같습니다.

```text
Pull Request
      ↓
AI Reviewer
      ↓
PR Metadata (PR 메타데이터) 확인
      ↓
Diff / 관련 코드 확인
      ↓
pytest 실행
      ↓
Code Review
      ↓
APPROVE (승인 가능)
REQUEST_CHANGES (수정 필요)
HUMAN_REVIEW (사람 검토 필요)
      ↓
Human Final Decision (사람 최종 결정)
```

AI는 PR의 상태를 검토하고 Merge 가능 여부를 추천합니다.

**최종 Merge 여부는 사람이 결정합니다.**

---

# Review Decision (리뷰 판정) (리뷰 판정 기준)

Reviewer는 PR을 세 가지 상태 중 하나로 판정합니다.

## APPROVE (승인 가능)

다음 조건을 만족할 때 사용합니다.

- 요구사항과 실제 변경이 일치
- merge-blocking correctness 문제 없음
- regression (회귀 오류) 위험 없음
- 테스트 결과가 적절함
- 변경 범위가 합리적임

## REQUEST_CHANGES (수정 필요)

Merge 전에 수정이 필요한 경우입니다.

예:

- 명백한 로직 오류
- 기존 behavior regression (회귀 오류) (동작 회귀)
- API / exception contract (예외 처리 계약) 위반
- 실제 코드 결함으로 인한 테스트 실패
- 중요한 요구사항 누락

## HUMAN_REVIEW (사람 검토 필요)

코드가 명백히 잘못됐다고 보기 어렵지만 AI가 단독으로 Merge 여부를 결정하기 어려운 경우입니다.

예:

- 요구사항 대비 과도한 구조 변경
- architecture (아키텍처) 판단
- 팀 convention에 의존하는 설계 변경
- 추가 business context가 필요한 경우

---

# Benchmark (벤치마크 / 평가 시나리오)

모든 PR은 동일한 정상 baseline (기준 상태)을 기준으로 독립적으로 구성했습니다.

각 실험 PR은 다른 실험 PR의 변경사항에 의존하지 않도록 분리했습니다.

## PR-001 — Valid Change

정상적인 `multiply(a, b)` 기능과 테스트를 추가했습니다.

```text
pytest: PASS
Expected: APPROVE (승인 가능)
Actual: APPROVE (승인 가능)
Confidence: 0.95
```

Reviewer는 기존 함수의 동작과 계약이 변경되지 않았고, 신규 기능과 테스트가 정상적으로 추가되었다고 판단했습니다.

---

## PR-002 — Obvious Logic Bug

`multiply(a, b)`라는 함수를 추가했지만 실제 구현은 다음과 같았습니다.

```python
def multiply(a, b):
    return a + b
```

`multiply()`에 대한 테스트가 없었기 때문에 기존 pytest는 모두 통과했습니다.

```text
pytest: PASS
Expected: REQUEST_CHANGES (수정 필요)
Actual: REQUEST_CHANGES (수정 필요)
Confidence: 0.98
```

Reviewer는 테스트 PASS에 의존하지 않고 함수명, docstring, 실제 구현의 불일치를 확인해 HIGH severity correctness bug (정확성 오류)로 판정했습니다.

---

## PR-003 — Test-detectable Regression

`divide()`에서 기존 zero division validation을 제거했습니다.

기존:

```python
if b == 0:
    raise ValueError("Cannot divide by zero")
```

변경 후에는 Python 기본 `ZeroDivisionError`가 발생합니다.

```text
pytest: FAIL
9 passed / 1 failed
Expected: REQUEST_CHANGES (수정 필요)
Actual: REQUEST_CHANGES (수정 필요)
Confidence: 0.96
```

Reviewer는 단순히 테스트가 실패했다는 이유가 아니라, 기존 `ValueError` exception contract (예외 처리 계약)가 깨졌다는 점을 근거로 regression (회귀 오류)을 판정했습니다.

---

## PR-004 — Hidden Behavior Regression

`calculate_discount()`의 반환값에 다음 변경을 적용했습니다.

```python
return round(price * (1 - discount_percent / 100), 2)
```

visible test (일반 테스트)는 모두 통과했습니다.

```text
pytest: PASS
Expected: REQUEST_CHANGES (수정 필요)
Actual: REQUEST_CHANGES (수정 필요)
Confidence: 0.90
```

Reviewer는 테스트 결과만으로 승인하지 않고 다음과 같은 behavior change를 발견했습니다.

- 결과를 항상 소수점 둘째 자리로 반올림
- 0% 할인에서도 원래 price가 변할 수 있음
- 매우 작은 금액이 0으로 사라질 수 있음
- 기존 계산식 대비 floating-point (부동소수점) behavior 변경
- 변경된 rounding (반올림) behavior를 검증하는 테스트 부재

이번 Benchmark에서 **AI Code Review가 단순 CI 테스트보다 추가적인 가치를 제공할 수 있음을 가장 잘 보여준 케이스**였습니다.

---

## PR-005 — Unnecessary Large Refactor

요구사항은 단순히 `multiply()` 추가였지만 다음 구조 변경을 함께 수행했습니다.

```text
Calculator class 도입
기존 함수 → staticmethod (정적 메서드) 이동
기존 module-level 함수 → wrapper (호환용 래퍼 함수) 유지
multiply 추가
```

기능적으로는 기존 동작이 유지됐고 테스트도 모두 통과했습니다.

```text
pytest: PASS
Expected: HUMAN_REVIEW (사람 검토 필요)
Actual: HUMAN_REVIEW (사람 검토 필요)
Confidence: 0.82
```

Reviewer는 correctness bug (정확성 오류)는 없다고 판단했지만, 단순 기능 추가에 비해 변경 범위가 지나치게 크고 새로운 공개 API 및 구조적 의사결정이 포함됐다고 판단했습니다.

따라서 자동 승인이나 자동 거절 대신 사람의 설계 판단이 필요한 `HUMAN_REVIEW`를 선택했습니다.

---

# Single Reviewer Workflow (단일 리뷰어 워크플로우)

Reviewer는 Claude Code 자체를 사용합니다.

별도의 LLM API 호출 코드는 없습니다.

```text
PR
 ↓
Claude Code
 ↓
PR Metadata (PR 메타데이터)
 ↓
GitHub PR Diff (PR 변경 내역)
 ↓
Local Git Diff (로컬 Git 변경 비교)
 ↓
관련 코드 확인
 ↓
pytest
 ↓
Review
 ↓
APPROVE (승인 가능) / REQUEST_CHANGES (수정 필요) / HUMAN_REVIEW (사람 검토 필요)
```

Reviewer Prompt:

```text
prompt/reviewer/SINGLE_REVIEWER.md
```

Reviewer는 PR을 검토할 때 Benchmark 정답을 알 수 있는 파일을 읽지 않도록 제한했습니다.

예:

```text
prompt/pr-*.md
benchmark/README.md
benchmark/reviews/*
```

각 PR Review는 독립적인 Claude Code 세션에서 실행하여 이전 PR의 Review 결과가 다음 판단에 영향을 주지 않도록 했습니다.

---

# Benchmark (벤치마크 / 평가 시나리오) 결과 요약

| 항목 | 결과 |
|---|---|
| Total PR | 5 |
| Correct Decision (정답 판정 수) | 5 |
| Decision Accuracy (판정 정확도) | 100% |
| Normal PR correctly approved | 1 / 1 |
| Bug / Regression correctly rejected | 3 / 3 |
| Architecture / Scope (아키텍처 / 변경 범위) case escalated to human | 1 / 1 |

이번 Benchmark에서 Reviewer는 다음 세 종류를 구분했습니다.

```text
정상 변경
→ APPROVE (승인 가능)

명확한 correctness / regression (회귀 오류) 문제
→ REQUEST_CHANGES (수정 필요)

정답이 코드 자체보다 설계 판단에 가까운 경우
→ HUMAN_REVIEW (사람 검토 필요)
```

---

# Human-in-the-loop (사람 최종 승인 구조)

이 프로젝트에서는 AI가 직접 Merge하지 않습니다.

```text
Claude Reviewer
        ↓
Review Decision (리뷰 판정)
        ↓
Human
        ↓
Merge / Reject / Request Changes
```

AI Reviewer는 의사결정을 지원하고, 최종 책임은 사람에게 남겨두는 구조입니다.

---

# Repository 구조 (Repository Structure)

```text
ai-pr-review-agent/
├── app/
├── tests/
├── prompt/
│   ├── AGENT_WORKFLOW.md
│   ├── reviewer/
│   │   └── SINGLE_REVIEWER.md
│   ├── pr-001-valid.md
│   ├── pr-002-obvious-bug.md
│   ├── pr-003-test-failure.md
│   ├── pr-004-hidden-bug.md
│   └── pr-005-unnecessary-refactor.md
│
├── benchmark/
│   ├── README.md
│   └── reviews/
│       ├── pr-001-single.md
│       ├── pr-002-single.md
│       ├── pr-003-single.md
│       ├── pr-004-single.md
│       └── pr-005-single.md
│
└── README.md
```

---

# 이번 프로젝트에서 확인한 점

### 1. 테스트 통과만으로 Merge 가능 여부를 판단할 수 없다

PR-002와 PR-004는 pytest가 통과했지만 Reviewer는 실제 문제를 발견했습니다.

### 2. AI Review는 코드 문맥을 함께 봐야 한다

단순 PASS / FAIL 판정이 아니라 diff, 기존 계약, 함수 의미, 테스트 범위를 함께 분석해야 유의미한 판단이 가능했습니다.

### 3. 모든 문제를 REQUEST_CHANGES로 처리하면 안 된다

PR-005처럼 기능은 정상이나 팀의 설계 판단이 필요한 경우가 존재합니다.

이 경우 `HUMAN_REVIEW`가 유용했습니다.

### 4. AI Reviewer는 최종 Merge 주체가 아니다

현재 구조에서는 AI가 판단 근거를 제공하고 사람이 최종 Merge 여부를 결정합니다.

---

# Scope (이번 실험 범위)

이번 프로젝트는 아래 범위까지만 수행했습니다.

```text
PR Benchmark 생성
→ Single Reviewer Workflow 구축
→ Claude Code 기반 독립 Review
→ 5개 PR 평가
→ 결과 비교
```

Benchmark를 더 어렵게 확장하거나 대규모 평가로 확장하지 않았습니다.

현재 결과는 **이 프로젝트에서 정의한 5개의 고정 PR Benchmark에 대한 결과**입니다.

---

# Next Step (다음 확장 방향)

향후 확장한다면 다음 방향을 고려할 수 있습니다.

```text
GitHub PR
→ Claude Code Reviewer 자동 실행
→ PR Review 자동 작성
→ Human Approval
```

또는 역할을 분리한 Multi-Agent Review 구조와 비교할 수 있습니다.

```text
Correctness (정확성) Reviewer
Test / Regression Reviewer
Scope / Design Reviewer
        ↓
Final Judge
```

하지만 이번 프로젝트의 1차 목표는 **Single AI Reviewer가 실제 Pull Request에서 Merge 가능 여부를 얼마나 잘 판단할 수 있는지 확인하는 것**이며, 해당 범위까지 완료했습니다.
