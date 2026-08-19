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

**Stage 1 — baseline only.**

This repository currently contains a known-good code baseline, a test suite
that describes its contract, an empty reviewer interface, and the
specification for the benchmark Pull Requests we will review later.

Not implemented yet, on purpose:

- no LLM API call
- no GitHub Actions workflow
- no automatic PR review
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
├── benchmark/
│   └── README.md            # specification of the experimental PRs (PR-001..PR-005)
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

See `benchmark/README.md` for the experiments that will measure how well the
reviewer produces these decisions.
