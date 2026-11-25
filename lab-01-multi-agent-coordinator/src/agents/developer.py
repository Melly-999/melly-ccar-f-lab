from typing import Any, Dict
from .base import BaseAgent
from ..schemas import SubAgentResult
from ..tools import read_file, list_directory, search_code


class DeveloperAgent(BaseAgent):
    name = "developer"

    def run(self, task: str, context: Dict[str, Any]) -> SubAgentResult:
        """
        Developer agent receives only:
        - the specific coding question
        - paths / files that are relevant
        """
        try:
            path = context.get("path", ".")
            query = context.get("code_query") or task

            listing = list_directory(path)
            matches = search_code(query, path)

            content = (
                f"Developer analysis for '{query}':\n"
                f"Directory contents: {listing['entries']}\n"
                f"Code matches: {matches['matches']}\n"
            )

            # Optionally read one file if requested
            if context.get("read_path"):
                file_data = read_file(context["read_path"])
                content += f"\nFile content of {context['read_path']}:\n{file_data['content'][:400]}..."

            return SubAgentResult(
                agent="developer",
                success=True,
                content=content,
                sources=[m["file"] for m in matches["matches"]],
            )

        except Exception as e:
            return SubAgentResult(
                agent="developer",
                success=False,
                content="",
                error=str(e),
                error_category="transient",
            )
