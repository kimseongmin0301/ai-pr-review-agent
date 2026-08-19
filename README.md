# AI PR Review Agent
### AI가 작성한 Pull Request를 AI Reviewer가 어디까지 검증할 수 있는가?

ChatGPT에서 설계한 실험을 MCP(Model Context Protocol)로 연결된 Claude Agent 환경에서 실행해 Pull Request(PR, 풀 리퀘스트)의 실제 변경사항과 테스트 결과를 검토하고, **APPROVE(승인 가능) / REQUEST_CHANGES(수정 필요) / HUMAN_REVIEW(사람 검토 필요)** 중 하나를 제안하도록 구성한 AI Code Review 실험 프로젝트입니다.

최종 Merge(병합)는 AI가 수행하지 않고 **사람이 결정하는 Human-in-the-loop(사람 최종 승인) 구조**를 사용했습니다.

> **중요:** 이 연구에서도 Claude Code CLI를 터미널에서 직접 실행하지 않았습니다. ChatGPT에서 연구와 Reviewer Workflow를 설계하고, MCP로 연결된 환경을 통해 Coding / Execution과 Review를 실행했습니다. README 역시 실험 과정과 결과를 바탕으로 ChatGPT와의 대화를 통해 작성했습니다.

---

# 결론 (Conclusion)

준비한 5개의 고정 PR Benchmark(벤치마크 / 평가 시나리오)에서 Claude Code 기반 Single Reviewer(단일 리뷰어)는 **5개 모두 기대한 판정과 일치하는 결과**를 냈습니다.

| PR | 검증 목적 | 기대 판정 | 실제 판정 | 결과 |
|---|---|---|---|---|
| PR-001 | 정상적인 기능 추가 | APPROVE (승인 가능) | APPROVE | ✅ |
| PR-002 | 테스트는 통과하지만 명확한 로직 오류 | REQUEST_CHANGES (수정 필요) | REQUEST_CHANGES | ✅ |
| PR-003 | 기존 테스트에서 드러나는 회귀 오류 | REQUEST_CHANGES (수정 필요) | REQUEST_CHANGES | ✅ |
| PR-004 | 테스트가 놓친 기존 동작 변경 | REQUEST_CHANGES (수정 필요) | REQUEST_CHANGES | ✅ |
| PR-005 | 기능은 정상이지만 요구사항 대비 과도한 리팩터링 | HUMAN_REVIEW (사람 검토 필요) | HUMAN_REVIEW | ✅ |

**Expected-decision alignment(기대 판정 일치): 5 / 5**

이 결과에서 가장 의미 있었던 부분은 단순히 테스트 실패를 감지한 것이 아닙니다.

```text
PR-002
pytest PASS
→ 실제 구현 오류 탐지

PR-004
pytest PASS
→ 테스트가 놓친 behavior regression(동작 회귀) 탐지

PR-005
기능상 오류 없음
→ 설계 / 변경 범위 문제를 HUMAN_REVIEW로 구분
```

즉 AI Reviewer는 단순한:

```text
pytest PASS → APPROVE
pytest FAIL → REQUEST_CHANGES
```

판정기가 아니라, **PR diff(변경 내역), 관련 코드, 테스트 결과와 코드의 의미를 함께 검토할 수 있었습니다.**

하지만 이번 실험의 결론을:

> **“AI 리뷰가 잘 되므로 사람 없이 자동 Merge해도 된다.”**

라고 보지는 않습니다.

오히려 결과는 반대에 가깝습니다.

AI는 반복적인 코드 확인, diff 분석, 테스트 결과 해석, 잠재적인 오류 탐지처럼 사람이 놓칠 수 있는 부분을 빠르게 검토하는 데 유용했습니다.

반면 PR-005처럼 코드가 정상 동작하더라도:

- 이 구조가 팀의 방향과 맞는가?
- 요구사항 대비 변경 범위가 적절한가?
- 유지보수 관점에서 이 설계를 받아들일 것인가?

와 같은 질문에는 하나의 기술적인 정답이 존재하지 않습니다.

이 부분은 프로젝트의 맥락을 알고 있는 사람이 판단해야 합니다.

따라서 이번 연구의 결론은 다음과 같습니다.

> **AI에게 모든 판단을 맡기는 것도 적절하지 않고, AI가 완벽하지 않다는 이유로 활용 자체를 불신하는 것도 적절하지 않다.**

중요한 것은:

> **어디까지 AI에게 맡기고 어느 지점부터 사람이 검증해야 가장 효율적이고 안전한가를 찾는 것**

이라고 생각합니다.

이번 프로젝트에서는 그 경계를 다음과 같이 두었습니다.

```text
AI Reviewer
→ PR 변경 분석
→ 테스트 결과 확인
→ 잠재 오류 탐지
→ Review Decision(리뷰 판정) 제안

        ↓

Human
→ AI가 제시한 근거 확인
→ 설계 / 비즈니스 / 프로젝트 맥락 판단
→ 최종 Merge 결정
```

즉 **AI는 Reviewer이자 의사결정 보조자이고, 최종 책임과 결정은 사람에게 남겨두는 구조**입니다.

다만 5개의 고정 PR을 사용한 소규모 실험이므로 모든 Repository와 모든 PR에서 동일한 성능을 보장한다는 의미는 아닙니다.

---

# 연구 배경 (Why This Project)

이 프로젝트는 첫 번째 연구인 **AI Coding Agent Benchmark**에서 이어진 후속 실험입니다. 두 연구 모두 CLI를 직접 조작하는 방식이 아니라, **ChatGPT에서 연구를 설계하고 MCP로 연결된 Agent와 도구를 통해 실제 Repository 작업을 수행하는 방식**으로 진행했습니다.

첫 번째 연구에서는 Codex CLI와 Claude Code를 비교하며 다음 질문을 다뤘습니다.

> **“어떤 개발 업무에서 어떤 Coding Agent를 사용하는 것이 더 적절한가?”**

그 결과:

```text
명확한 구현 / 빠른 실행
→ Codex

조사 / 분석 / 깊은 검토
→ Claude
```

라는 상대적인 특성을 관찰했습니다.

하지만 첫 번째 실험을 진행하면서 더 중요한 질문이 생겼습니다.

AI Coding Agent가 코드를 빠르게 작성할 수 있다고 하더라도:

- 실제 요구사항을 정확하게 구현했는가?
- 기존 기능을 깨뜨리지는 않았는가?
- 테스트가 통과하면 정말 안전한가?
- 테스트가 잡지 못하는 문제는 없는가?
- 코드 자체는 정상이어도 변경 범위가 과도하지 않은가?
- 최종 Merge 결정까지 AI에게 맡겨도 되는가?

라는 문제는 여전히 남았습니다.

그래서 두 번째 연구에서는 **Coding Agent 간 성능 비교를 중단하고, AI Code Review 자체를 독립된 연구 대상으로 분리했습니다.**

핵심 질문은 다음과 같습니다.

> **AI가 작성한 코드를 다시 AI가 리뷰하게 하면 실제 Merge 판단에 도움이 될 수 있을까?**

---

# 첫 번째 연구와의 관계

여기서 중요한 점이 하나 있습니다.

첫 번째 연구에서는 구현 업무에 대해 **Codex가 상대적으로 효율적**이라는 결과를 얻었습니다.

그런데 이번 프로젝트의 Coding / Execution Agent(코드 작성·실행 에이전트)는 Claude Code입니다.

이것은 첫 번째 연구 결과를 무시하거나 반대로 적용한 것이 아닙니다.

두 프로젝트의 목적이 다르기 때문입니다.

```text
연구 1
Codex vs Claude
→ Coding Agent의 상대적인 특성 비교

연구 2
AI PR Review
→ Reviewer 자체의 검증 능력 평가
```

이번 실험에서는 **Codex와 Claude 중 누가 더 잘 구현하는지를 다시 비교하지 않습니다.**

Review 성능을 중심으로 보기 위해 작업 실행 모델을 Claude로 통일하고, **Coding 역할과 Reviewer 역할을 별도의 세션과 지침으로 분리**했습니다.

```text
Claude Code
Coding / Execution Session
        ↓
Pull Request
        ↓
별도 Claude Reviewer Session
(MCP 연동)
        ↓
APPROVE / REQUEST_CHANGES / HUMAN_REVIEW
        ↓
Human Final Decision
```

따라서 이번 프로젝트는:

```text
첫 번째 연구에서 제안한
Codex + Claude 최적 조합을 그대로 구현한 Multi-Agent 실험
X
```

이 아니라:

```text
첫 번째 연구를 진행하며 발견한
“AI가 만든 결과물을 AI가 검증할 수 있는가?”
라는 새로운 질문을 독립적으로 검증한 후속 연구
O
```

입니다.

이 차이가 두 프로젝트를 연결하는 핵심입니다.

---

# 왜 Single Reviewer부터 실험했는가?

첫 번째 연구의 결과만 보면 다음과 같은 Multi-Agent(멀티 에이전트) 구조를 생각할 수 있습니다.

```text
Claude
→ Requirement Analysis

Codex
→ Implementation

Claude
→ Deep Review

Human
→ Final Approval
```

하지만 여러 Agent를 한 번에 연결하면 문제가 발생했을 때:

```text
Coding Agent 문제인가?
Reviewer 문제인가?
Agent 간 전달 문제인가?
Workflow 설계 문제인가?
```

를 구분하기 어려워집니다.

그래서 이번 연구에서는 Multi-Agent 구조로 바로 확장하기보다 **Reviewer 하나의 역할이 실제로 유효한지 먼저 확인하는 것**을 목표로 했습니다.

```text
1단계
Single Reviewer 자체의 가능성 검증

        ↓

필요할 경우

2단계
역할별 Multi-Agent 구조로 확장
```

즉 이번 프로젝트의 평가 대상은 **“Claude가 Coding까지 잘하는가?”가 아니라 “독립된 AI Reviewer가 PR을 얼마나 유효하게 검증하는가?”**입니다.

---

# 사용 모델 및 역할 (Models & Roles)

| 역할 | 사용 모델 | 수행 내용 |
|---|---|---|
| Planner / Research Organizer (계획·연구 정리) | ChatGPT — GPT-5.6 Sol Medium | 연구 질문, 실험 구조, PR Benchmark, Reviewer Workflow, Prompt 및 README 설계 |
| Coding / Execution Agent (코드 작성·실행) | Claude — Opus High + MCP | 코드 변경, 테스트, Commit, Push, PR 생성 |
| Single PR Reviewer (단일 PR 리뷰어) | Claude — Opus High + MCP | PR metadata, diff, 관련 코드, pytest 결과 분석 및 판정 |
| Human (사람) | 사용자 | 실험 방향 결정, 결과 확인, 최종 Merge 여부 판단 |

별도의 OpenAI API 또는 Anthropic API를 직접 호출하는 Reviewer 프로그램은 만들지 않았습니다.

실험 제어와 문서화는 ChatGPT에서 진행하고, 실제 Repository / GitHub 작업은 **MCP로 연결된 Claude Agent와 도구**를 통해 수행했습니다.

---

# 전체 Workflow (작업 흐름)

```text
ChatGPT
GPT-5.6 Sol — Medium
→ Research / Benchmark / Prompt / README 설계
        ↓
MCP
        ↓
Coding / Execution Agent
Claude — Opus High
        ↓
Code Change
        ↓
pytest
        ↓
Commit / Push
        ↓
Pull Request 생성
        ↓
별도 Claude Reviewer Session
(MCP 연동)
        ↓
PR Metadata
Diff
Related Code
pytest
추가 검증
        ↓
APPROVE
REQUEST_CHANGES
HUMAN_REVIEW
        ↓
Human Final Decision
```

중요한 원칙은 **AI가 최종 Merge를 수행하지 않는 것**입니다.

---

# 판정 기준 (Review Decisions)

## APPROVE (승인 가능)

코드 변경이 요구사항에 맞고, 치명적인 문제나 의미 있는 회귀가 없다고 판단한 경우입니다.

AI의 의미는:

> **현재 확인한 범위에서는 Merge 가능한 변경으로 보인다.**

이지 자동 Merge 명령이 아닙니다.

---

## REQUEST_CHANGES (수정 필요)

Merge 전에 반드시 수정해야 할 문제를 발견한 경우입니다.

예:

- 명확한 로직 오류
- 기존 동작 회귀
- 테스트 실패
- 요구사항 불일치
- 중요한 예외 처리 누락

---

## HUMAN_REVIEW (사람 검토 필요)

기술적으로 명확한 오류라고 단정하기 어렵지만 사람이 판단해야 하는 경우입니다.

예:

- 요구사항 대비 과도한 리팩터링
- 새로운 abstraction(추상화) 도입
- API 설계 변경
- 유지보수 방향
- 팀 convention(개발 규칙)
- 비즈니스 맥락이 필요한 결정

이 판정을 별도로 둔 이유는 **AI가 모든 애매한 상황을 억지로 승인 또는 거절하지 않도록 하기 위해서**입니다.

---

# Benchmark 구성

5개의 PR을 서로 다른 유형으로 만들었습니다.

| PR | 시나리오 | pytest | 기대 판정 |
|---|---|---|---|
| PR-001 | 정상적인 `multiply()` 추가 | PASS | APPROVE |
| PR-002 | `multiply()`가 실제로는 덧셈 수행 | PASS | REQUEST_CHANGES |
| PR-003 | `divide()`의 기존 예외 처리 제거 | FAIL | REQUEST_CHANGES |
| PR-004 | 할인 계산에 임의의 2자리 반올림 도입 | PASS | REQUEST_CHANGES |
| PR-005 | 기능은 정상이나 Calculator class로 과도하게 구조 변경 | PASS | HUMAN_REVIEW |

PR-003을 제외한 대부분의 케이스가 pytest를 통과하도록 만든 이유는 Reviewer가 단순히 테스트 결과만 따라가는지 확인하기 위해서입니다.

---

# Benchmark PR 생성 방식

각 PR은 다른 실험의 영향을 받지 않도록 동일한 baseline에서 독립적으로 생성했습니다.

```text
baseline
├── experiment/pr-001-valid
├── experiment/pr-002-obvious-bug
├── experiment/pr-003-test-failure
├── experiment/pr-004-hidden-bug
└── experiment/pr-005-unnecessary-refactor
```

즉:

```text
PR-001
   ↓
PR-002
   ↓
PR-003
```

처럼 누적하지 않았습니다.

모든 PR은 같은 기준 상태에서 각각 분기했습니다.

---

# Coding / Execution 실행 방식

실제 실행은 터미널에서 Claude CLI를 직접 조작하는 방식이 아니라, **ChatGPT에서 준비한 Task / Prompt와 MCP로 연결된 Agent 환경을 이용하는 방식**으로 진행했습니다.

```text
ChatGPT
→ 작업 목표와 Prompt 정리
→ Benchmark Task 정의

        ↓ MCP

Claude Agent
→ Repository 확인
→ 코드 변경
→ pytest 실행
→ diff 확인
→ commit / push
→ Pull Request 생성
```

공통 실행 규칙은 Markdown 문서로 정의했습니다.

```text
prompt/
├── AGENT_WORKFLOW.md
├── pr-001-valid.md
├── pr-002-obvious-bug.md
├── pr-003-test-failure.md
├── pr-004-hidden-bug.md
└── pr-005-unnecessary-refactor.md
```

`AGENT_WORKFLOW.md`에는 다음 공통 흐름을 정의했습니다.

```text
Read Task (작업 읽기)
→ Verify Branch (브랜치 확인)
→ Modify (코드 수정)
→ Test (테스트)
→ Verify Diff (변경사항 확인)
→ Commit
→ Push
→ Create PR (PR 생성)
→ Report (결과 보고)
```

각 PR 문서는 해당 Benchmark에 필요한 변경 조건만 별도로 정의했습니다.

PR description(설명)에는 Reviewer가 정답을 추론할 수 있는 Benchmark 의도나 기대 판정을 노출하지 않도록 했습니다.

---

# 테스트 방법 (Testing)

## 1. pytest

기본 테스트 명령:

```bash
python -m pytest -q
```

PR별 예상 결과:

| PR | pytest 결과 | 의미 |
|---|---|---|
| PR-001 | PASS | 정상 구현 |
| PR-002 | PASS | 신규 함수 테스트가 없어 오류가 드러나지 않음 |
| PR-003 | FAIL | 기존 예외 계약을 깨뜨린 회귀 |
| PR-004 | PASS | 기존 테스트가 동작 변경을 잡지 못함 |
| PR-005 | PASS | 기능은 정상이나 구조적 판단이 필요 |

이 구성을 통해:

```text
Test Result
≠
Review Decision
```

인지 확인했습니다.

---

# Single Reviewer 실행 방식

Reviewer는 `prompt/reviewer/SINGLE_REVIEWER.md`의 고정 규칙을 사용했습니다.

각 PR은 이전 리뷰의 영향을 줄이기 위해 **별도의 Claude Reviewer 세션**에서 독립적으로 검토했습니다. 이 Reviewer 역시 CLI를 직접 실행한 것이 아니라 MCP로 Repository / GitHub 정보를 확인할 수 있는 환경에서 실행했습니다.

예:

```text
prompt/reviewer/SINGLE_REVIEWER.md를 읽고
PR #6을 Single Reviewer로 독립적으로 검토해주세요.
```

Reviewer가 확인하도록 허용한 정보:

```text
PR title / description
Base / Head branch
GitHub PR diff
Local git diff
변경된 실제 코드
관련 코드
관련 테스트
pytest 결과
```

Reviewer가 읽지 않도록 제한한 정보:

```text
prompt/pr-*.md
benchmark/README.md
benchmark/reviews/*의 이전 리뷰 결과
다른 PR의 리뷰 결과
```

이 제한을 둔 이유는 **Benchmark 정답 유출과 이전 리뷰에 의한 판단 오염을 막기 위해서**입니다.

---

# Reviewer의 추가 검증

Reviewer는 pytest 결과만 확인하지 않았습니다.

PR 성격에 따라 다음과 같은 read-only(읽기 전용) 검증을 추가로 수행했습니다.

```text
GitHub PR diff와 local git diff 비교
변경 함수의 실제 구현 확인
관련 호출부 검색
기존 exception behavior 비교
base와 head의 테스트 결과 비교
경계값 / 소수 입력 직접 확인
변경 전후 동작 비교
```

특히 PR-004에서는 테스트가 모두 통과했지만 `round(..., 2)` 도입으로 기존 반환값이 달라지는 입력을 직접 확인했습니다.

PR-005에서는 기존 기능이 실제로 유지되는지 비교한 뒤, 기능 오류가 아니라 **Architecture / Scope(아키텍처 / 변경 범위) 판단 문제**로 구분했습니다.

---

# Benchmark 상세 결과

## PR-001 — 정상 변경

변경:

```python
def multiply(a, b):
    return a * b
```

테스트도 추가했습니다.

결과:

```text
pytest: PASS
Reviewer: APPROVE
Confidence: 0.95
```

Reviewer는 기능과 테스트가 일치하며 기존 코드에 영향을 주지 않는다고 판단했습니다.

---

## PR-002 — 테스트는 통과하지만 구현 오류

표면적으로는 `multiply()` 함수 추가입니다.

그러나 실제 구현은:

```python
def multiply(a, b):
    return a + b
```

였습니다.

새 함수에 대한 테스트는 추가하지 않았기 때문에 기존 pytest는 통과했습니다.

```text
pytest
→ 10 passed

Reviewer
→ 실제 코드 확인
→ multiply 이름 / 목적과 return a + b 불일치 발견
→ REQUEST_CHANGES
```

이 케이스는 **CI 테스트가 통과해도 AI Reviewer가 코드의 의미를 확인할 수 있는지** 보기 위한 실험이었습니다.

---

## PR-003 — 테스트에서 발견되는 회귀 오류

기존 `divide()`의 0 나누기 처리를 제거했습니다.

기존 동작:

```text
divide(..., 0)
→ ValueError("Cannot divide by zero")
```

변경 후:

```text
divide(..., 0)
→ ZeroDivisionError
```

결과:

```text
pytest
→ 1 failed, 9 passed

Reviewer
→ REQUEST_CHANGES
```

이 케이스는 가장 전형적인 CI + Review 실패 케이스입니다.

---

## PR-004 — 테스트가 놓친 동작 변경

변경 전:

```python
return price * (100 - discount_percent) / 100
```

변경 후:

```python
return round(price * (1 - discount_percent / 100), 2)
```

기존 테스트는 모두 통과했습니다.

그러나 Reviewer는 추가 입력을 직접 확인하며:

- 2자리 반올림 강제
- 소수 정밀도 변경
- 0% 할인에서도 일부 값 변경 가능
- 기존 반환 동작과의 불일치

를 확인했습니다.

```text
pytest
→ PASS

Reviewer
→ REQUEST_CHANGES
```

이번 Benchmark에서 **AI Review가 CI 테스트 이상의 역할을 보여준 가장 중요한 사례 중 하나**입니다.

---

## PR-005 — 기능은 정상, 설계 판단이 필요한 변경

표면 요구사항은 `multiply()` 추가였습니다.

하지만 PR은 Calculator class를 도입하고 기존 함수를 staticmethod와 wrapper 형태로 다시 구성했습니다.

기능 자체는 정상 동작했습니다.

```text
pytest
→ PASS
```

Reviewer는 기존 동작과 변경 후 동작을 추가로 비교했고 기능적인 문제는 없다고 판단했습니다.

그러나:

```text
작은 기능 추가 요구사항
        ↓
Module 전체 구조 변경
        ↓
새로운 abstraction 도입
        ↓
API / 유지보수 범위 확대
```

라는 문제가 있어 자동 APPROVE나 REQUEST_CHANGES보다:

```text
HUMAN_REVIEW
```

가 적절하다고 판단했습니다.

이 사례는 AI Reviewer가 **Correctness(정확성) 문제와 Architecture / Scope(설계 / 변경 범위) 문제를 구분할 수 있는지** 보기 위한 실험이었습니다.

---

# Benchmark 결과 요약

```text
PR-001
Expected: APPROVE
Actual  : APPROVE
✅

PR-002
Expected: REQUEST_CHANGES
Actual  : REQUEST_CHANGES
✅

PR-003
Expected: REQUEST_CHANGES
Actual  : REQUEST_CHANGES
✅

PR-004
Expected: REQUEST_CHANGES
Actual  : REQUEST_CHANGES
✅

PR-005
Expected: HUMAN_REVIEW
Actual  : HUMAN_REVIEW
✅
```

**Expected-decision alignment: 5 / 5**

다만 이를 **“AI Code Review 정확도 100%”**라고 일반화하지 않습니다.

정확한 표현은:

> **이 프로젝트에서 정의한 5개의 고정 Benchmark에서 기대 판정과 5/5 일치했다.**

입니다.

---

# 첫 번째 연구와 두 번째 연구에서 얻은 흐름

두 프로젝트를 함께 보면 연구 질문이 다음처럼 변화했습니다.

```text
연구 1
AI Coding Agent Benchmark

“어떤 Agent가 더 좋은가?”
        ↓
“아니, 어떤 업무에서 어떤 Agent가 더 적합한가?”

        ↓

새로운 문제

“Agent가 코드를 잘 작성해도
그 결과물이 정말 안전한지는 누가 확인하는가?”

        ↓

연구 2
AI PR Review Agent

“AI Reviewer가 실제 PR을 검증할 수 있는가?”

        ↓

이번 실험의 결론

“AI Review는 유용하지만
최종 판단까지 모두 AI에게 넘겨서는 안 된다.”
```

첫 번째 연구의 결과를 그대로 구현한 프로젝트가 아니라 **첫 번째 연구에서 생긴 새로운 질문을 분리해서 검증한 두 번째 연구**입니다.

---

# AI와 사람의 역할

이번 프로젝트에서 가장 중요하게 본 부분입니다.

## AI가 잘할 수 있었던 영역

```text
반복적인 변경 확인
Diff 분석
테스트 결과 확인
코드와 테스트의 불일치 탐색
잠재 버그 탐색
회귀 가능성 확인
검토해야 할 지점 정리
```

## 사람이 계속 판단해야 하는 영역

```text
제품 / 비즈니스 맥락
팀의 개발 규칙
Architecture 방향
변경 범위의 적절성
장기 유지보수 판단
위험도가 높은 변경
최종 Merge
```

그래서 이번 프로젝트의 구조는:

```text
AI
→ 판단 보조

Human
→ 최종 판단
```

입니다.

AI가 활성화되는 환경에서 **무조건적으로 신뢰하는 것도, 무조건적으로 불신하는 것도 적절하지 않다**고 생각합니다.

AI가 잘하는 영역은 적극적으로 활용하면서, 사람이 책임져야 하는 구간을 명확히 두고 실제 사용 과정에서 그 경계를 계속 조정하는 것이 더 현실적인 방향이라고 봤습니다.

---

# ChatGPT와 MCP의 역할

이 프로젝트에서 ChatGPT와 MCP의 역할을 구분하면 다음과 같습니다.

```text
ChatGPT
→ 연구 질문 정리
→ Benchmark 설계
→ Prompt / Reviewer 규칙 작성
→ 결과 해석
→ README 작성 및 수정

MCP
→ Agent와 Repository / GitHub / 도구 연결

Claude Agent
→ 실제 코드 변경
→ 테스트
→ Commit / Push / PR 생성
→ 별도 Reviewer 역할에서 PR 검토

Human
→ 실험 방향 결정
→ 결과 확인
→ 최종 Merge 판단
```

즉 README에서 말하는 `Agent 실행`은 **CLI를 사람이 직접 실행했다는 뜻이 아니라, ChatGPT에서 설계한 작업을 MCP로 연결된 Agent가 수행했다는 의미**입니다.

README 또한 실험 외부의 별도 작성자가 만든 문서가 아니라, **두 연구의 계획과 결과 정리에 참여한 ChatGPT를 통해 작성하고 반복 수정한 문서**입니다.

실제 실험 근거는 Repository의 PR, diff, test 결과, benchmark review 파일 등으로 남기고, README는 그 과정과 결론을 설명하는 문서로 사용했습니다.

---

# 한계 (Limitations)

이번 결과에는 다음 한계가 있습니다.

- Benchmark PR은 5개입니다.
- 작은 Calculator Repository를 사용했습니다.
- 의도적으로 설계한 고정 시나리오입니다.
- 실제 대규모 서비스 PR보다 변경 범위가 작습니다.
- Claude Code와 현재 Reviewer Prompt 조건에서의 결과입니다.
- 모델 또는 Prompt가 변경되면 결과도 달라질 수 있습니다.
- PR-004처럼 Reviewer가 필요 이상으로 많은 가능성을 제기할 수도 있습니다.

따라서 이번 결과는:

> **Single AI Reviewer가 PR 검증 과정에서 실제로 유용한 신호를 제공할 수 있는지를 확인한 소규모 실험**

으로 보는 것이 적절합니다.

---

# Repository 구조 (Repository Structure)

```text
.
├── app/
│   └── calculator.py
│
├── tests/
│   └── test_calculator.py
│
├── prompt/
│   ├── AGENT_WORKFLOW.md
│   ├── pr-001-valid.md
│   ├── pr-002-obvious-bug.md
│   ├── pr-003-test-failure.md
│   ├── pr-004-hidden-bug.md
│   ├── pr-005-unnecessary-refactor.md
│   └── reviewer/
│       └── SINGLE_REVIEWER.md
│
├── benchmark/
│   └── reviews/
│
└── README.md
```

---

# Final Summary (최종 요약)

첫 번째 연구에서는:

> **어떤 Coding Agent가 어떤 업무에 상대적으로 강한가?**

를 확인했습니다.

두 번째 연구에서는:

> **AI가 만든 결과물을 AI Reviewer가 실제로 어디까지 검증할 수 있는가?**

를 확인했습니다.

5개의 고정 Benchmark에서는 Reviewer가 모두 기대한 판정을 제안했으며, 특히 테스트가 통과한 PR에서도 실제 문제를 찾아냈습니다.

하지만 동시에 설계와 변경 범위처럼 사람의 판단이 필요한 영역도 확인했습니다.

따라서 현재의 결론은 다음과 같습니다.

```text
AI를 무조건 신뢰한다
X

AI를 완전히 불신한다
X

AI가 잘하는 검증은 적극 활용한다
+
사람이 판단해야 하는 영역은 남겨둔다
O
```

> **중요한 것은 AI가 사람을 완전히 대체할 수 있는지를 묻는 것이 아니라, 어디까지 AI에게 맡기고 어디에서 사람이 검증해야 가장 효율적이고 안전한지를 찾아가는 것이라고 생각합니다.**
