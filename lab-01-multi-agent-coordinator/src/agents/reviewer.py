from typing import Any, Dict
from .base import BaseAgent
from ..schemas import SubAgentResult
from ..tools import analyze_text, check_consistency


class ReviewerAgent(BaseAgent):
    name = "reviewer"

    def run(self, task: str, context: Dict[str, Any]) -> SubAgentResult:
        """
        Reviewer agent receives only:
        - the artifacts to review
        - clear review criteria
        """
        try:
            text = context.get("text_to_review") or task
            criteria = context.get("criteria", "clarity and correctness")

            analysis = analyze_text(text, criteria)
            consistency = check_consistency([text])

            content = (
                f"Review against criteria '{criteria}':\n"
                f"Score: {analysis['score']}\n"
                f"Comments: {analysis['comments']}\n"
                f"Consistency: {consistency['summary']}\n"
            )

            return SubAgentResult(
                agent="reviewer",
                success=True,
                content=content,
                sources=[],
            )

        except Exception as e:
            return SubAgentResult(
                agent="reviewer",
                success=False,
                content="",
                error=str(e),
                error_category="transient",
            )
