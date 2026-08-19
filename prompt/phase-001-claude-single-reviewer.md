# Phase 1 — Claude Code Single PR Reviewer

## 목적

`ai-pr-review-agent` 프로젝트의 다음 단계로
**Claude Code 자체를 Single AI Pull Request Reviewer로 사용**하는 Review Workflow를 구축한다.

이번 단계에서는 별도의 LLM API를 사용하지 않는다.

사용하지 않는 것:

```text
OpenAI API
Anthropic API 직접 호출
별도 API Key
외부 LLM SDK
LangChain
LangGraph
CrewAI
AutoGen
```

Claude Code가 현재 Repository와 GitHub MCP를 직접 사용하여
Pull Request를 읽고, diff와 테스트 결과를 분석한 뒤 최종 판단한다.

최종 판정은 다음 세 가지다.

```text
APPROVE
REQUEST_CHANGES
HUMAN_REVIEW
```

---

# 1. 전체 목표

이번 Phase의 목표 Workflow:

```text
Open Pull Request
        ↓
Claude Code
        ↓
PR Metadata 확인
        ↓
Base / Head Diff 확인
        ↓
관련 코드 및 테스트 확인
        ↓
pytest 실행
        ↓
변경 내용 분석
        ↓
APPROVE / REQUEST_CHANGES / HUMAN_REVIEW
        ↓
Structured Review Report
```

이번 단계에서는 **자동 Merge를 수행하지 않는다.**

Reviewer는 Merge 여부를 판단하는 역할만 한다.

---

# 2. 작업 위치

이번 작업은 experiment branch가 아니라
정상 baseline을 관리하는 `main`에서 수행한다.

작업 시작 전에 반드시 확인한다.

```bash
git branch --show-current
git status
```

조건:

```text
branch == main
working tree == clean
```

조건이 맞지 않으면 기존 변경을 덮어쓰지 말고 중단한다.

---

# 3. 구현 방향

이번 Phase에서는 LLM 호출 코드를 작성하지 않는다.

대신 Claude Code가 읽고 따를 수 있는 Reviewer Prompt와
Review 결과를 저장할 구조를 Repository에 추가한다.

권장 구조:

```text
prompt/
├── AGENT_WORKFLOW.md
├── reviewer/
│   └── SINGLE_REVIEWER.md
├── pr-001-valid.md
├── pr-002-obvious-bug.md
├── pr-003-test-failure.md
├── pr-004-hidden-bug.md
└── pr-005-unnecessary-refactor.md

benchmark/
├── README.md
└── reviews/
    └── .gitkeep
```

기존 구조를 확인하고 필요한 파일만 추가한다.

불필요하게 Python Reviewer framework를 새로 만들지 않는다.

---

# 4. SINGLE_REVIEWER.md 작성

다음 파일을 만든다.

```text
prompt/reviewer/SINGLE_REVIEWER.md
```

이 문서는 Claude Code가 PR을 검토할 때 따라야 하는
**고정 Reviewer System Prompt 역할**을 한다.

반드시 아래 내용을 포함한다.

---

## Reviewer Role

Claude Code는 Senior Code Reviewer 역할을 수행한다.

목표:

```text
현재 Pull Request가 main에 Merge 가능한 상태인지 판단
```

단순 스타일 리뷰보다 다음 항목을 우선한다.

1. Correctness
2. Regression
3. Requirement compliance
4. Test result
5. Test coverage / missing cases
6. Backward compatibility
7. Scope
8. Maintainability
9. Security
10. Merge risk

---

# 5. PR 확인 절차

Reviewer는 반드시 다음 순서를 따른다.

## Step 1 — PR 확인

GitHub MCP 또는 현재 사용 가능한 GitHub 도구를 통해
검토 대상 Pull Request의 정보를 확인한다.

최소 확인:

```text
PR number
PR title
PR description
base branch
head branch
changed files
```

Reviewer가 어떤 PR을 검토해야 하는지 명확하지 않으면
임의로 선택하지 말고 사용자에게 확인한다.

---

## Step 2 — Diff 확인

base와 head 사이의 실제 코드 diff를 확인한다.

가능하면 GitHub PR diff와 local git diff를 교차 확인한다.

예:

```bash
git diff <base>...<head>
```

단순 PR 설명만 읽고 판단하지 않는다.

실제 변경 코드를 반드시 확인한다.

---

## Step 3 — 관련 코드 확인

diff만 보고 문맥이 부족하면
변경된 함수, 호출부, 테스트 등 관련 코드를 추가로 읽는다.

하지만 Repository 전체를 무조건 읽지 않는다.

Review에 필요한 최소 context만 추가로 확인한다.

---

## Step 4 — 테스트 확인

가능하면 PR의 head branch 기준으로 테스트를 실행한다.

기본:

```bash
pytest -q
```

다음 정보를 확인한다.

```text
passed
failed
error
exit status
```

중요:

```text
pytest PASS != 자동 APPROVE
pytest FAIL != 분석 없이 자동 REQUEST_CHANGES
```

테스트 결과의 원인을 diff와 함께 분석한다.

---

# 6. 판정 기준

최종 decision은 반드시 다음 중 하나다.

```text
APPROVE
REQUEST_CHANGES
HUMAN_REVIEW
```

## APPROVE

다음 조건을 모두 만족할 때 사용한다.

- 요구사항과 변경 내용이 일치한다.
- merge-blocking correctness 문제가 없다.
- regression 위험이 발견되지 않는다.
- 테스트 결과가 적절하다.
- 변경 범위가 합리적이다.
- 사람이 추가로 판단해야 할 중요한 불확실성이 없다.

작은 스타일 문제만 있는 경우
무조건 REQUEST_CHANGES하지 않는다.

---

## REQUEST_CHANGES

Merge 전에 수정이 반드시 필요한 경우 사용한다.

예:

- 명백한 로직 버그
- 기존 동작 regression
- 기존 contract 위반
- 핵심 요구사항 누락
- 테스트 실패가 실제 코드 결함을 의미함
- 잘못된 exception behavior
- 데이터 손실 가능성
- critical/high severity security 문제
- 결과 정확성을 깨뜨리는 변경

Reviewer는 반드시 구체적인 근거를 제시한다.

---

## HUMAN_REVIEW

코드 자체가 명백하게 틀렸다고 말하기 어렵지만
사람의 설계/비즈니스 판단이 필요한 경우 사용한다.

예:

- 요구사항에 비해 변경 범위가 지나치게 큼
- architecture 변경
- business requirement가 불명확함
- merge 가능 여부가 팀의 정책/의사결정에 의존함
- 제공된 context만으로 안전성을 판단하기 어려움

HUMAN_REVIEW는 실패 판정이 아니다.

```text
AI가 자동 승인/거절하기에는 판단 범위를 넘어선다
```

는 의미다.

---

# 7. Severity

Issue severity는 다음 중 하나를 사용한다.

```text
LOW
MEDIUM
HIGH
CRITICAL
```

기준:

### LOW
스타일, 작은 가독성 문제, merge를 막지 않는 개선사항

### MEDIUM
유지보수성, 테스트 부족, 제한적인 edge case 위험

### HIGH
실제 기능 오류, regression, contract 위반

### CRITICAL
보안 사고, 데이터 손실, 서비스 중단 등 즉시 차단해야 하는 문제

---

# 8. Review 출력 형식

Claude Code의 최종 응답은 반드시 아래 형태를 따른다.

```markdown
# AI PR Review

## Decision

APPROVE | REQUEST_CHANGES | HUMAN_REVIEW

## Confidence

0.00 ~ 1.00

## Summary

PR에 대한 간결한 최종 평가.

## Test Result

- command:
- result:
- passed:
- failed:

## Issues

### Issue 1

- Severity:
- File:
- Line:
- Reason:
- Recommendation:

## Merge Recommendation

최종적으로 사람이 Merge를 진행해도 되는지 한두 문장으로 설명.
```

Issue가 없다면:

```text
No blocking issues found.
```

라고 명시한다.

---

# 9. Confidence 기준

confidence는 Reviewer가 자신의 판단에 얼마나 확신하는지 나타낸다.

예:

```text
0.90 ~ 1.00
근거가 명확함

0.70 ~ 0.89
판단 가능하지만 일부 불확실성 존재

0.50 ~ 0.69
추가 context가 있으면 좋음

< 0.50
HUMAN_REVIEW를 적극 고려
```

confidence가 높다고 자동 merge하지 않는다.

---

# 10. Benchmark 오염 방지

매우 중요하다.

Reviewer는 다음 task 문서를
**정답 자료로 사용하면 안 된다.**

```text
prompt/pr-001-valid.md
prompt/pr-002-obvious-bug.md
prompt/pr-003-test-failure.md
prompt/pr-004-hidden-bug.md
prompt/pr-005-unnecessary-refactor.md
```

이 파일들은 benchmark PR 생성용 문서다.

Reviewer가 이 문서들을 읽으면
어떤 PR이 정상이고 어떤 PR이 의도적인 버그인지 알 수 있기 때문에
실험이 오염된다.

따라서 PR 리뷰 시에는 다음 정보만 사용한다.

```text
PR title
PR description
actual diff
repository code
tests
test result
```

Reviewer Prompt에 다음 금지 규칙을 명시한다.

```text
Do NOT read benchmark task definition files
to infer the expected answer.
```

---

# 11. 다른 PR 결과 참조 금지

각 PR은 독립적으로 검토한다.

PR-001을 리뷰한 결과를 PR-002 판단에 사용하지 않는다.

금지:

```text
이전 PR이 정상 케이스였으므로 이번 PR은 버그 케이스일 것이다.
```

또는:

```text
5개 benchmark 중 하나니까 예상 정답은 ...
```

각 Review는 새로운 독립 Code Review로 수행한다.

---

# 12. 자동 수정 금지

Reviewer는 Review 도중 코드를 수정하지 않는다.

금지:

```text
코드 수정
commit
push
PR 수정
test 수정
```

Reviewer 역할은:

```text
Read
Analyze
Test
Review
```

까지만이다.

코드 수정은 별도의 Coding Agent가 담당한다.

---

# 13. 자동 Merge 금지

Reviewer가 APPROVE를 선택하더라도
직접 Merge하지 않는다.

Workflow:

```text
AI Reviewer
        ↓
Decision
        ↓
Human
        ↓
Merge / Reject
```

Human-in-the-loop 구조를 유지한다.

---

# 14. GitHub Review 작성

이번 Phase에서는 우선 Claude Code의 Review 결과가
정확하게 생성되는 것까지 구현한다.

GitHub MCP가 이미 Review comment 작성 기능을 안정적으로 사용할 수 있다면
추가로 PR에 Review 결과를 남겨도 된다.

하지만 자동 GitHub Review가 핵심 구현을 방해한다면
이번 Phase에서는 생략한다.

다음 Phase에서 별도로 자동화한다.

---

# 15. Review 결과 저장

Benchmark 비교를 위해 Review 결과를 파일로 저장할 수 있는 구조를 만든다.

예:

```text
benchmark/reviews/
├── pr-001-single.md
├── pr-002-single.md
├── pr-003-single.md
├── pr-004-single.md
└── pr-005-single.md
```

이번 Phase에서는 디렉터리와 규칙만 준비해도 된다.

Review 실행 시 사용자가 요청하면 해당 PR 결과를 저장한다.

---

# 16. README 수정

README에 다음 내용을 간단히 추가한다.

## Single Reviewer

```text
Claude Code를 Single Reviewer Agent로 사용
```

입력:

```text
PR metadata
diff
repository context
pytest result
```

출력:

```text
APPROVE
REQUEST_CHANGES
HUMAN_REVIEW
```

그리고 반드시 명시한다.

```text
현재 단계에서는 사람이 최종 Merge를 결정한다.
```

---

# 17. 테스트

이번 Phase는 Reviewer prompt/workflow 구축이 핵심이므로
별도 LLM unit test framework를 만들지 않는다.

기존 application 테스트가 깨지지 않았는지 확인한다.

```bash
pytest -q
```

main baseline의 모든 기존 테스트가 통과해야 한다.

---

# 18. Dependency

이번 Phase에서는 새로운 Python dependency를 추가하지 않는다.

특히 다음은 추가하지 않는다.

```text
openai
anthropic
langchain
langgraph
crewai
autogen
```

Claude Code 자체가 Reviewer이기 때문이다.

---

# 19. Git 작업

작업 완료 후:

```bash
git status
git diff
pytest -q
```

를 확인한다.

commit message:

```text
feat: add single PR reviewer workflow
```

현재 `main`에 commit한다.

push 권한이 있다면 `main`을 push한다.

---

# 20. Phase 완료 조건

다음 조건을 모두 만족하면 완료다.

- `prompt/reviewer/SINGLE_REVIEWER.md` 존재
- Reviewer 역할과 판정 기준 정의
- PR 확인 절차 정의
- pytest 검증 절차 정의
- structured Review format 정의
- benchmark task 파일 참조 금지 규칙 존재
- 자동 코드 수정 금지
- 자동 Merge 금지
- README 업데이트
- 기존 pytest 전체 PASS
- 신규 LLM API dependency 없음

---

# 21. 다음 Phase

이번 단계 완료 후:

```text
Phase 2 — Execute Single Reviewer Benchmark
```

진행:

```text
PR-001
↓
Claude Single Reviewer
↓
Review 저장

PR-002
↓
Claude Single Reviewer
↓
Review 저장

...

PR-005
↓
Claude Single Reviewer
↓
Review 저장
```

그 결과를 기준으로:

```text
Expected Decision
vs
Claude Decision
```

을 비교한다.

그 이후:

```text
Phase 3
GitHub Review 자동 작성

Phase 4
Multi-Agent Reviewer

Phase 5
Single vs Multi Benchmark
```

순서로 확장한다.

---

# 22. 최종 보고

작업 완료 후 전체 파일 내용을 채팅에 복사하지 않는다.

다음만 보고한다.

1. 생성/수정한 파일
2. SINGLE_REVIEWER.md 구성 요약
3. README 변경 내용
4. pytest 결과
5. 신규 dependency 추가 여부
6. commit hash
7. push 여부
8. 현재 branch
9. 다음 Phase 실행 방법
