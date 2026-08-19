# ai-pr-review-agent

An experimental repository for a system that reviews Pull Requests
automatically and decides whether they are safe to merge.

## The problem

Code review is the slowest step in most teams' delivery pipeline, and CI only
answers one narrow question: *did the tests pass?* A green build says nothing
about a change that is logically wrong in a path no test covers, and nothing
about a change whose scope is far larger than its stated intent. Meanwhile a
human reviewer's time is spent mostly on trivial, obviously-fine diffs.

This project explores how far an AI reviewer can be trusted to take that first
pass: approve the obviously safe changes, block the clearly broken ones, and —
importantly — hand the genuinely ambiguous ones back to a human instead of
guessing.

## Current stage

**Phase 1 — single reviewer workflow.**

On top of the known-good baseline and its contract tests, this repository now
carries the reviewer instructions themselves: `prompt/reviewer/SINGLE_REVIEWER.md`
defines how a single reviewer reads a Pull Request and reaches a decision. The
reviewer is Claude Code following that document — there is no reviewer service
to deploy and no model call in this repository.

Not implemented yet, on purpose:

- no LLM API call and no LLM SDK dependency
- no GitHub Actions workflow
- no unattended review (a human starts every run)
- no automatic merge
- no multi-agent orchestration
- no web framework, database, or container

## Repository structure

```
ai-pr-review-agent/
├── app/
│   ├── __init__.py
│   └── calculator.py        # known-good baseline, the subject under review
├── tests/
│   └── test_calculator.py   # contract tests for the baseline
├── reviewer/
│   ├── __init__.py
│   └── reviewer.py          # ReviewResult + Reviewer interface (no implementation)
├── prompt/
│   ├── AGENT_WORKFLOW.md    # rules every agent task in this repo follows
│   └── reviewer/
│       └── SINGLE_REVIEWER.md   # the single reviewer's fixed instructions
├── benchmark/
│   ├── README.md            # specification of the experimental PRs (PR-001..PR-005)
│   └── reviews/             # saved review outputs, one file per PR
├── conftest.py              # makes `pytest -q` importable from the repo root
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the tests

Python 3.12 is the target version.

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

All tests must pass on `main`. A red `main` invalidates every benchmark run,
because the reviewer would then be judging a broken baseline.

## Planned workflow

```
Pull Request
  -> Test
  -> Diff Collection
  -> AI Reviewer
  -> APPROVE / REQUEST_CHANGES / HUMAN_REVIEW
  -> PR Review
```

**This workflow is not implemented yet.** Nothing in this repository runs
automatically at the moment; the diagram describes the target design that the
following stages will build toward.

The three decisions mean:

| Decision | Meaning |
| --- | --- |
| `APPROVE` | The change is safe to merge as-is. |
| `REQUEST_CHANGES` | A concrete defect was found; the change must not merge. |
| `HUMAN_REVIEW` | The reviewer is not confident enough to decide alone. |

## Single Reviewer

Claude Code acts as the Single Reviewer Agent, following the fixed instructions
in `prompt/reviewer/SINGLE_REVIEWER.md`. Nothing else is required to run a
review — no API key, no reviewer process.

Input the reviewer is allowed to use:

```
PR metadata (number, title, description, base, head, changed files)
diff between base and head
repository context (the source and tests it needs to judge the diff)
pytest result
```

Output:

```
APPROVE
REQUEST_CHANGES
HUMAN_REVIEW
```

together with a confidence score, a test-result block, and a severity-tagged
issue list, in the report format the reviewer document specifies.

**A human decides the final merge at this stage.** The reviewer never commits,
never edits code, and never merges — an `APPROVE` is a recommendation to a
person, not an action.

To run one review, point Claude Code at a Pull Request and ask it to review
that PR under `prompt/reviewer/SINGLE_REVIEWER.md`. Saved results go to
`benchmark/reviews/pr-<n>-single.md`.

The reviewer must not read the benchmark task documents or `benchmark/README.md`
while reviewing: those state the expected verdict for each experimental PR, so
reading them would invalidate the measurement.

See `benchmark/README.md` for the experiments that will measure how well the
reviewer produces these decisions.
