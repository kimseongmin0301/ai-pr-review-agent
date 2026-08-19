# PR-005-UNNECESSARY-REFACTOR

## 목적

AI PR Reviewer 평가를 위한 독립 experiment task입니다.

## 작업 브랜치

반드시 다음 브랜치에서만 작업하세요.

```text
experiment/pr-005-unnecessary-refactor
```

작업 시작 전:

```bash
git branch --show-current
```

브랜치가 다르면 작업하지 말고 중단하세요.

## 요구사항

표면적인 요구사항은 `multiply(a, b)` 추가입니다.

다만 실험을 위해 다음처럼 요구사항 대비 과도한 리팩터링을 수행하세요.

1. `Calculator` 클래스를 생성
2. 기존 `add`, `subtract`, `divide`, `calculate_discount` 로직을 `@staticmethod`로 이동
3. 기존 public 함수 이름은 wrapper로 유지
4. `multiply()`도 같은 구조로 추가
5. 기존 exception message와 외부 동작은 유지

기존 테스트는 유지하고 `multiply()` 정상 동작 테스트만 최소 1개 추가하세요.

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

모든 테스트가 통과해야 합니다.

## Git

commit message:

```text
refactor: introduce calculator abstraction
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
experiment/pr-005-unnecessary-refactor
```

PR title:

```text
refactor: introduce calculator abstraction
```

PR description에는 아래 두 내용만 자연스럽게 작성하세요.

- 변경 요약
- 테스트 결과

중요:

- 예상 Reviewer 판정값을 PR 설명에 쓰지 마세요.
- benchmark 정답을 노출하지 마세요.
- 의도적인 버그/회귀/실험 조건을 밝히지 마세요.
- hidden evaluation 정보를 적지 마세요.

PR 설명에는 '과도한 리팩터링 실험'이라는 사실을 적지 마세요. 실제 개발 PR처럼 작성하세요.

## 최종 보고

다음만 보고하세요.

1. 수정 파일
2. pytest 결과
3. commit 여부와 hash
4. push 여부
5. PR 생성 여부
6. PR 번호와 URL
7. 현재 branch
