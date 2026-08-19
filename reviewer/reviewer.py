"""Reviewer interface for the AI PR Review Agent.

This baseline step defines *only* the contract. No LLM call, no prompt,
no agent orchestration is implemented here on purpose.

A future Single-Agent reviewer and a future Multi-Agent reviewer are both
expected to subclass :class:`Reviewer` and return a :class:`ReviewResult`,
so the rest of the pipeline can swap implementations without changing.
"""

from dataclasses import dataclass, field
from enum import Enum


class Decision(str, Enum):
    """Final verdict the reviewer produces for a Pull Request."""

    APPROVE = "APPROVE"
    REQUEST_CHANGES = "REQUEST_CHANGES"
    HUMAN_REVIEW = "HUMAN_REVIEW"


@dataclass
class ReviewResult:
    """Structured output of a review.

    Attributes:
        decision: One of :class:`Decision`.
        confidence: How confident the reviewer is, from 0.0 to 1.0.
        summary: Short human readable explanation of the decision.
        issues: Concrete problems found. Empty when nothing was found.
    """

    decision: Decision
    confidence: float
    summary: str
    issues: list[str] = field(default_factory=list)


class Reviewer:
    """Base interface every reviewer implementation must satisfy."""

    def review(self, diff: str, test_result: str, pr_description: str) -> ReviewResult:
        """Review a Pull Request and return a :class:`ReviewResult`.

        Args:
            diff: Unified diff of the Pull Request.
            test_result: Raw output of the test run for this Pull Request.
            pr_description: Title and body written by the PR author.

        Raises:
            NotImplementedError: Always, in this baseline step.
        """
        raise NotImplementedError(
            "No reviewer implementation exists yet. "
            "Subclass Reviewer and implement review() in a later step."
        )
