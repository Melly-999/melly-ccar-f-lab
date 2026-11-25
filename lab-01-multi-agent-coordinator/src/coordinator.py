from typing import List, Dict, Any
from .schemas import SubAgentResult, CoordinatorDecision, FinalAnswer
from .agents import ResearchAgent, DeveloperAgent, ReviewerAgent
from .llm import ClaudeClient


class Coordinator:
    """
    Production-oriented coordinator for the CCAR-F lab.

    Key exam points demonstrated:
    - Clear ownership of the conversation
    - Minimal context passed to each subagent
    - Structured decision making (now powered by Claude)
    - Explicit handling of failure / no-data cases
    - Always returns a valid FinalAnswer
    """

    def __init__(self, use_llm_decision: bool = True):
        self.research = ResearchAgent()
        self.developer = DeveloperAgent()
        self.reviewer = ReviewerAgent()
        self.max_rounds = 3
        self.use_llm_decision = use_llm_decision
        self.llm = ClaudeClient() if use_llm_decision else None

    def run(self, user_query: str) -> FinalAnswer:
        results: List[SubAgentResult] = []
        agents_used = set()
        round_count = 0

        # Always start with research for most queries (can be made smarter later)
        research_ctx = {"query": user_query}
        research_result = self.research.run(user_query, research_ctx)
        results.append(research_result)
        agents_used.add("research")
        round_count += 1

        while round_count < self.max_rounds:
            decision = self._decide(user_query, results)

            if decision.status == "complete" or decision.status == "failed":
                break

            if not decision.next_actions:
                break

            # Execute requested agents (can be parallelized later)
            if "developer" in decision.next_actions and "developer" not in agents_used:
                dev_ctx = {
                    "code_query": user_query,
                    "path": ".",
                }
                dev_result = self.developer.run(user_query, dev_ctx)
                results.append(dev_result)
                agents_used.add("developer")

            if "reviewer" in decision.next_actions and "reviewer" not in agents_used:
                text_to_review = "\n\n".join(r.content for r in results if r.success)
                rev_ctx = {
                    "text_to_review": text_to_review or user_query,
                    "criteria": "accuracy, usefulness and completeness",
                }
                rev_result = self.reviewer.run("Review the findings so far", rev_ctx)
                results.append(rev_result)
                agents_used.add("reviewer")

            # Avoid infinite loops if the same agents keep being requested
            if set(decision.next_actions).issubset(agents_used):
                break

            round_count += 1

        return self._build_final_answer(user_query, results, list(agents_used))

    def _decide(self, query: str, results: List[SubAgentResult]) -> CoordinatorDecision:
        """
        Decision point – the most important architectural piece for the exam.

        When use_llm_decision=True we ask Claude for a structured decision.
        Otherwise we fall back to the simple heuristic (useful for offline tests).
        """
        if self.use_llm_decision and self.llm is not None:
            summary_parts = []
            for r in results:
                status = "SUCCESS" if r.success else f"FAILED ({r.error_category or 'unknown'})"
                summary_parts.append(
                    f"[{r.agent.upper()}] {status}\n{r.content[:600]}"
                )
            results_summary = "\n\n---\n\n".join(summary_parts)
            return self.llm.decide(query, results_summary)

        # Fallback heuristic (kept for tests / offline mode)
        research = next((r for r in results if r.agent == "research"), None)

        if research is None or not research.success:
            return CoordinatorDecision(
                status="need_more_info",
                confidence=0.3,
                next_actions=["developer", "reviewer"],
                reason="Research failed or returned no data",
            )

        if research.error_category == "no_data" or "no relevant" in research.content.lower():
            return CoordinatorDecision(
                status="need_more_info",
                confidence=0.4,
                next_actions=["developer"],
                reason="Research returned no useful data",
            )

        return CoordinatorDecision(
            status="complete",
            confidence=0.75,
            next_actions=[],
            reason="Research produced usable information",
        )

    def _build_final_answer(
        self, query: str, results: List[SubAgentResult], agents_used: List[str]
    ) -> FinalAnswer:
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        if not successful:
            return FinalAnswer(
                status="failed",
                answer="All agents failed to produce useful output.",
                confidence=0.1,
                agents_used=agents_used,
                requires_human_review=True,
                notes="; ".join(r.error or "unknown error" for r in failed),
            )

        combined = "\n\n".join(r.content for r in successful)
        sources = []
        for r in successful:
            sources.extend(r.sources)

        confidence = 0.8 if len(successful) >= 2 else 0.65

        return FinalAnswer(
            status="success" if not failed else "partial",
            answer=combined,
            confidence=confidence,
            sources=list(set(sources)),
            agents_used=agents_used,
            requires_human_review=any(r.error_category == "no_data" for r in results),
            notes=f"Used agents: {', '.join(agents_used)}",
        )
