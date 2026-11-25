from abc import ABC, abstractmethod
from typing import Any, Dict
from ..schemas import SubAgentResult


class BaseAgent(ABC):
    name: str

    @abstractmethod
    def run(self, task: str, context: Dict[str, Any]) -> SubAgentResult:
        """Execute the agent with a focused task and minimal context."""
        ...
