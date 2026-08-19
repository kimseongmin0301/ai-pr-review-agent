# Agent Workflow Rules

모든 작업은 아래 공통 규칙을 따른다.

## 1. 작업 문서 확인

작업을 시작하기 전에 `prompt/` 폴더에서 현재 작업에 해당하는 Markdown 문서를 먼저 읽는다.

현재 작업 문서의 요구사항, 제한사항, 테스트 조건, Git 지침을 작업 기준으로 사용한다.

## 2. Branch 확인

작업 시작 전에 반드시 현재 Git branch를 확인한다.

```bash
git branch --show-current
```

작업 문서에 지정된 branch와 현재 branch가 다르면 작업하지 말고 중단한다.

각 experiment branch는 반드시 `main`에서 독립적으로 생성되어야 하며, 다른 experiment branch의 변경사항을 가져오거나 의존하면 안 된다.

## 3. 작업 범위

- 작업 문서에 명시된 범위만 수정한다.
- 문서에 없는 기능을 임의로 추가하지 않는다.
- 불필요한 리팩터링을 하지 않는다.
- 작업 목적과 관계없는 파일을 수정하지 않는다.
- `main`의 정상 baseline을 임의로 변경하지 않는다.
- reviewer 관련 코드는 작업 문서에서 명시한 경우에만 수정한다.
- GitHub Actions는 작업 문서에서 명시한 경우에만 수정한다.
- 신규 dependency는 작업 문서에서 요구한 경우에만 추가한다.

## 4. 테스트

작업 문서에 정의된 테스트 명령을 반드시 실행한다.

기본:

```bash
pytest -q
```

테스트 성공/실패의 기대값은 각 작업 문서의 정의를 따른다.

테스트를 통과시키기 위해 기존 테스트를 삭제, skip, 완화하거나 benchmark defect를 임의로 수정하지 않는다.

## 5. Benchmark 의도 보존

이 Repository는 AI PR Reviewer 평가용 benchmark를 포함한다.

각 experiment branch에 정의된 의도적인 버그, regression, scope 문제를 임의로 고치거나 제거하지 않는다.

Agent의 역할은 benchmark task를 개선하는 것이 아니라 정확히 재현하는 것이다.

## 6. Git 작업

작업 완료 후 다음을 확인한다.

```bash
git status
git diff
```

문서에 지정된 commit message를 사용한다.

현재 experiment branch에만 commit한다.

다른 branch를 merge하거나 수정하지 않는다.

force push는 문서에서 명시하지 않는 한 사용하지 않는다.

## 7. Push

원격 저장소에 접근 가능하고 push 권한이 있으면 현재 experiment branch만 push한다.

예:

```bash
git push -u origin <current-branch>
```

push가 불가능하면 그 이유를 최종 보고에 남긴다.

## 8. Pull Request 생성

push가 성공했고 GitHub MCP 또는 사용 가능한 GitHub 도구가 PR 생성을 지원하면 Pull Request를 직접 생성한다.

규칙:

- Base branch: `main`
- Head branch: 현재 experiment branch
- PR title: 작업 문서에 지정된 값을 사용
- PR description에는 변경 요약과 테스트 결과만 포함
- benchmark의 기대 판정값을 적지 않는다.
- 의도적으로 삽입된 버그나 regression 사실을 적지 않는다.
- hidden evaluation 기준을 적지 않는다.
- Reviewer의 정답을 유도할 수 있는 표현을 적지 않는다.

PR 생성 후 PR 번호와 URL을 기록한다.

PR 생성 권한이나 도구가 없으면 그 이유를 최종 보고에 남긴다.

## 9. 최종 검토

작업 종료 전에 확인한다.

1. 현재 branch가 올바른가
2. 작업 요구사항을 모두 반영했는가
3. 금지된 변경을 하지 않았는가
4. 테스트를 실행했는가
5. 결과가 task 기대와 일치하는가
6. 불필요한 파일이 변경되지 않았는가
7. 올바른 commit message를 사용했는가
8. 가능하면 push를 수행했는가
9. 가능하면 PR을 생성했는가

## 10. 최종 응답

전체 소스 코드를 채팅에 복사하지 않는다.

별도 형식이 없다면 다음만 보고한다.

1. 수정한 파일
2. 테스트 결과
3. commit 여부와 hash
4. push 여부
5. PR 생성 여부
6. PR 번호/URL
7. 현재 branch

## 핵심 흐름

```text
Read Task
→ Verify Branch
→ Modify
→ Test
→ Verify Diff
→ Commit
→ Push
→ Create PR
→ Report
```
