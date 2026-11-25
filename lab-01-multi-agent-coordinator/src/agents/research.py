from typing import Any, Dict
from .base import BaseAgent
from ..schemas import SubAgentResult
from ..tools import web_search, fetch_url


class ResearchAgent(BaseAgent):
    name = "research"

    def run(self, task: str, context: Dict[str, Any]) -> SubAgentResult:
        """
        Research agent receives only:
        - the research question
        - optional previous findings that are relevant
        """
        try:
            query = context.get("query") or task
            search_result = web_search(query)

            if not search_result["results"]:
                return SubAgentResult(
                    agent="research",
                    success=False,
                    content="No relevant results found.",
                    error_category="no_data",
                )

            # In a real system you might fetch the top 1-2 pages.
            top = search_result["results"][0]
            page = fetch_url(top["url"])

            summary = (
                f"Research summary for '{query}':\n"
                f"- Top result: {top['title']}\n"
                f"- Snippet: {top['snippet']}\n"
                f"- Content preview: {page['content'][:200]}..."
            )

            return SubAgentResult(
                agent="research",
                success=True,
                content=summary,
                sources=[r["url"] for r in search_result["results"]],
            )

        except Exception as e:
            return SubAgentResult(
                agent="research",
                success=False,
                content="",
                error=str(e),
                error_category="transient",
            )
