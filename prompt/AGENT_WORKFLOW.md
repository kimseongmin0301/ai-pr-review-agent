# Agent Workflow Rules

모든 작업은 아래 공통 규칙을 따른다.

## 1. 작업 문서 확인

작업을 시작하기 전에 `prompt/` 폴더에서 현재 작업에 해당하는 Markdown 문서를 먼저 읽는다.

예:

```text
prompt/init.md
prompt/pr-001-valid.md
prompt/pr-002-obvious-bug.md
prompt/pr-003-test-failure.md
prompt/pr-004-hidden-bug.md
prompt/pr-005-unnecessary-refactor.md
```

현재 작업에 해당하는 문서의 요구사항, 제한사항, 테스트 조건, Git 지침을 작업 기준으로 사용한다.

---

## 2. Branch 확인

작업 시작 전에 반드시 현재 Git branch를 확인한다.

```bash
git branch --show-current
```

작업 문서에 지정된 branch와 현재 branch가 다르면 작업하지 말고 중단한다.

다른 experiment branch에서 작업을 이어서 하지 않는다.

각 experiment branch는 반드시 `main`에서 독립적으로 생성되어야 한다.

예:

```text
main
├── experiment/pr-001-valid
├── experiment/pr-002-obvious-bug
├── experiment/pr-003-test-failure
├── experiment/pr-004-hidden-bug
└── experiment/pr-005-unnecessary-refactor
```

---

## 3. 작업 범위

작업 문서에 명시된 범위만 수정한다.

다음 원칙을 지킨다.

- 문서에 없는 기능을 임의로 추가하지 않는다.
- 불필요한 리팩터링을 하지 않는다.
- 작업 목적과 관계없는 파일을 수정하지 않는다.
- 다른 experiment branch의 변경사항을 가져오지 않는다.
- `main`의 정상 baseline을 임의로 변경하지 않는다.
- 신규 dependency는 작업 문서에서 요구하는 경우에만 추가한다.
- reviewer 관련 코드는 작업 문서에서 명시한 경우에만 수정한다.
- GitHub Actions는 작업 문서에서 명시한 경우에만 수정한다.

---

## 4. 테스트

작업 문서에 정의된 테스트 명령을 반드시 실행한다.

기본 테스트 명령:

```bash
pytest -q
```

테스트의 성공/실패 기대값은 각 작업 문서의 정의를 따른다.

예를 들어 일부 benchmark task는 의도적으로 regression을 포함하므로 테스트 실패가 정상일 수 있다.

테스트를 통과시키기 위해 다음 행동을 하지 않는다.

- 기존 테스트 삭제
- 기존 테스트 skip 처리
- assertion 완화
- 요구사항 변경
- 의도된 benchmark defect 수정

---

## 5. Benchmark 의도 보존

이 Repository는 AI PR Reviewer를 평가하기 위한 benchmark를 포함한다.

따라서 각 experiment branch에 정의된 의도적인 버그, regression, scope 문제 등을 Agent가 임의로 개선하거나 제거하면 안 된다.

작업 문서에서 의도적으로 잘못된 구현을 요구하는 경우에도 해당 요구사항을 그대로 따른다.

Agent의 역할은 benchmark task를 수정하는 것이 아니라 **정확히 재현하는 것**이다.

---

## 6. Git 작업

작업 완료 후 다음을 확인한다.

```bash
git status
git diff
```

불필요한 변경이 포함되지 않았는지 검토한다.

commit message는 각 작업 문서에서 지정한 값을 사용한다.

push 권한이 있다면 현재 작업 branch만 push한다.

다른 branch를 push하거나 수정하지 않는다.

---

## 7. Commit / Push 제한

다음 원칙을 지킨다.

- 현재 experiment branch에만 commit한다.
- 다른 experiment branch를 수정하지 않는다.
- `main`에 직접 실험 변경을 commit하지 않는다.
- force push는 작업 문서에서 명시하지 않는 한 사용하지 않는다.
- 다른 branch를 merge하지 않는다.
- rebase로 다른 실험 변경사항을 섞지 않는다.

---

## 8. 최종 검토

작업을 종료하기 전에 최소한 다음을 확인한다.

1. 현재 branch가 올바른가
2. 작업 문서의 요구사항을 모두 반영했는가
3. 금지된 변경을 하지 않았는가
4. 테스트를 실행했는가
5. 테스트 결과가 작업 문서의 기대와 일치하는가
6. 불필요한 파일이 변경되지 않았는가
7. 올바른 commit message를 사용했는가

---

## 9. 최종 응답

채팅에 전체 소스 코드를 복사하지 않는다.

각 작업 문서에 정의된 최종 보고 형식을 따른다.

별도 형식이 없다면 다음만 보고한다.

1. 수정한 파일
2. 테스트 결과
3. commit 여부
4. push 여부
5. 현재 branch

---

## 핵심 원칙

```text
Read Task
→ Verify Branch
→ Modify Only Required Scope
→ Run Tests
→ Verify Diff
→ Commit
→ Push Current Branch
→ Report Result
```

이 Repository에서 가장 중요한 것은 Agent가 더 많은 일을 하는 것이 아니라,
**각 benchmark task의 조건을 정확하게 재현하고 실험 간 독립성을 유지하는 것**이다.
