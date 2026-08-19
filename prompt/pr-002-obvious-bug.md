# PR-002-OBVIOUS-BUG

## 목적

AI PR Reviewer 평가를 위한 독립 experiment task입니다.

## 작업 브랜치

반드시 다음 브랜치에서만 작업하세요.

```text
experiment/pr-002-obvious-bug
```

작업 시작 전:

```bash
git branch --show-current
```

브랜치가 다르면 작업하지 말고 중단하세요.

## 요구사항

기존 코드에 `multiply(a, b)`를 새로 추가하세요.

실험을 위해 의도적으로 아래처럼 구현하세요.

```python
def multiply(a, b):
    return a + b
```

`multiply()`에 대한 신규 테스트는 추가하지 마세요.
기존 테스트는 수정하거나 삭제하지 마세요.

## 제한사항

- 작업 문서 범위 밖 수정 금지
- 다른 experiment branch의 변경을 가져오지 않기
- reviewer 코드 수정 금지
- GitHub Actions 수정 금지
- 신규 dependency 추가 금지
- benchmark 의도를 임의로 변경하지 않기

## 테스트

반드시 실행하세요.

```bash
pytest -q
```

기존 visible test는 모두 통과해야 합니다.

## Git

commit message:

```text
feat: add multiplication operation
```

현재 branch에만 commit하세요.

push 권한이 있으면 현재 branch만 push하세요.

## Pull Request

push가 성공하고 GitHub MCP 또는 사용 가능한 GitHub 도구가 PR 생성을 지원하면 직접 PR을 생성하세요.

Base:

```text
main
```

Head:

```text
experiment/pr-002-obvious-bug
```

PR title:

```text
feat: add multiplication operation
```

PR description에는 아래 두 내용만 자연스럽게 작성하세요.

- 변경 요약
- 테스트 결과

중요:

- 예상 Reviewer 판정값을 PR 설명에 쓰지 마세요.
- benchmark 정답을 노출하지 마세요.
- 의도적인 버그/회귀/실험 조건을 밝히지 마세요.
- hidden evaluation 정보를 적지 마세요.

PR 설명에는 이 구현이 의도적인 버그라는 사실을 절대 적지 마세요.

## 최종 보고

다음만 보고하세요.

1. 수정 파일
2. pytest 결과
3. commit 여부와 hash
4. push 여부
5. PR 생성 여부
6. PR 번호와 URL
7. 현재 branch
