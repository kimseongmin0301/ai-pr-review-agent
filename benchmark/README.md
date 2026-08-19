# PR Benchmark

This folder describes the experimental Pull Requests that will be used to
evaluate the AI PR Review Agent. **None of them exist yet** — this document is
the specification we will build them from in a later step.

Each benchmark PR is a small, deliberate change to `app/calculator.py`
(and sometimes to `tests/`) with a known, agreed-upon expected verdict.
Comparing the reviewer's actual decision against the expected decision is how
we measure whether the reviewer is useful or not.

## How to read a benchmark entry

| Field | Meaning |
| --- | --- |
| Change | What the PR does to the baseline code |
| Test result | What `pytest -q` is expected to report for that PR |
| Expected decision | The verdict a good reviewer should reach |
| Purpose | The reviewer capability this case is designed to probe |

## Benchmark cases

### PR-001 — Normal change

- **Change**: A correct, small, well-scoped change. For example, adding a
  `multiply(a, b)` function together with its test.
- **Test result**: PASS
- **Expected decision**: `APPROVE`
- **Purpose**: Establish the false-positive baseline. If the reviewer blocks a
  clean PR, it is too strict and developers will stop trusting it.

### PR-002 — Obvious logic bug

- **Change**: A clearly wrong implementation, for example `subtract` returning
  `b - a`, or `divide` dropping the zero check.
- **Test result**: FAIL (or PASS, if the case is built so no existing test
  covers the broken path)
- **Expected decision**: `REQUEST_CHANGES`
- **Purpose**: Verify the reviewer can read a diff and recognise incorrect
  logic — the most basic capability we need.

### PR-003 — Regression caught immediately by pytest

- **Change**: A change that breaks behaviour already covered by the existing
  suite, for example `calculate_discount` returning the discount amount
  instead of the discounted price.
- **Test result**: FAIL
- **Expected decision**: `REQUEST_CHANGES`
- **Purpose**: Verify the reviewer actually consumes the test output and
  refuses to approve a red build, and that its explanation points at the
  failing test rather than inventing an unrelated reason.

### PR-004 — Passes the existing tests but is logically wrong

- **Change**: A change no current test covers, for example accepting
  `discount_percent` above 100 by silently clamping it, or treating a
  `None` price as `0`.
- **Test result**: PASS
- **Expected decision**: `REQUEST_CHANGES`
- **Purpose**: The hardest and most valuable case. A green build is not proof
  of correctness — this measures whether the reviewer adds signal beyond CI.
  A reviewer that only echoes the test result will fail here.

### PR-005 — Correct behaviour, unnecessarily large refactor

- **Change**: Behaviour is preserved, but the diff is disproportionate:
  renaming everything, splitting the module into several files, or introducing
  a class hierarchy for four small functions.
- **Test result**: PASS
- **Expected decision**: `APPROVE` or `HUMAN_REVIEW` — both are acceptable
- **Purpose**: Measure review *quality*, not just correctness. Whichever
  decision it picks, the reviewer must explicitly call out that the change
  scope is larger than the stated intent. A verdict of `APPROVE` with no
  mention of the scope problem counts as a failure for this case.

## Scoring notes

- A case counts as passed only when both the decision **and** the stated
  reason are acceptable. A right answer for a wrong reason is not a pass.
- `HUMAN_REVIEW` is the correct escape hatch for genuine ambiguity. Using it
  on PR-001 through PR-004 counts as a failure, because those cases are not
  ambiguous.
