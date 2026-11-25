"""
Thin wrapper around Anthropic Claude API for structured decisions.
Used by the Coordinator for the critical "decide next step" call.
"""

import os
import json
from typing import Optional
from anthropic import Anthropic
from .schemas import CoordinatorDecision


class ClaudeClient:
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def decide(self, user_query: str, results_summary: str) -> CoordinatorDecision:
        """
        Ask Claude to decide the next orchestration step.
        Returns a structured CoordinatorDecision.
        """
        system = """You are the decision brain of a multi-agent system.
Your only job is to decide what should happen next based on the user query and the results so far.

You MUST reply with valid JSON only, matching this exact schema:
{
  "status": "complete" | "need_more_info" | "failed",
  "confidence": float between 0 and 1,
  "next_actions": list of "research" | "developer" | "reviewer",
  "reason": short explanation
}

Rules:
- Prefer "complete" when the information is already good enough to answer.
- Use "need_more_info" only when a specific agent can clearly add value.
- Use "failed" only when continuing is pointless.
- Be conservative with next_actions – do not call agents unnecessarily.
- Never invent tools or agents that do not exist.
"""

        user_content = f"""User query:
{user_query}

Results from agents so far:
{results_summary}

Decide the next step."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            system=system,
            messages=[{"role": "user", "content": user_content}],
        )

        text = response.content[0].text.strip()

        # Try to extract JSON even if the model wraps it
        try:
            # Find the first { ... }
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                data = json.loads(text[start:end])
            else:
                data = json.loads(text)
        except Exception:
            # Fallback if parsing fails
            return CoordinatorDecision(
                status="complete",
                confidence=0.5,
                next_actions=[],
                reason="Failed to parse decision JSON – stopping with current results",
            )

        return CoordinatorDecision(
            status=data.get("status", "complete"),
            confidence=float(data.get("confidence", 0.6)),
            next_actions=data.get("next_actions", []),
            reason=data.get("reason", "No reason provided"),
        )
