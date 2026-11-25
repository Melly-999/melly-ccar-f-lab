from typing import List, Dict, Any
from .schemas import SubAgentResult, CoordinatorDecision, FinalAnswer
from .agents import ResearchAgent, DeveloperAgent, ReviewerAgent


class Coordinator:
    """
    Simple but exam-relevant coordinator.

    Responsibilities:
    - Decide which subagents to call
    - Build minimal context for each
    - Aggregate results
    - Decide whether to finish or continue
    - Always return structured FinalAnswer
    """

    def __init__(self):
        self.research = ResearchAgent()
        self.developer = DeveloperAgent()
        self.reviewer = ReviewerAgent()
        self.max_rounds = 3

    def run(self, user_query: str) -> FinalAnswer:
        results: List[SubAgentResult] = []
        agents_used = set()

        # Round 1 – always start with research for most queries
        research_ctx = {"query": user_query}
        research_result = self.research.run(user_query, research_ctx)
        results.append(research_result)
        agents_used.add("research")

        # Simple decision logic (in a real system this would be another LLM call)
        decision = self._decide(user_query, results)

        if decision.status == "need_more_info" and "developer" in decision.next_actions:
            dev_ctx = {
                "code_query": user_query,
                "path": ".",
            }
            dev_result = self.developer.run(user_query, dev_ctx)
            results.append(dev_result)
            agents_used.add("developer")

        if decision.status == "need_more_info" and "reviewer" in decision.next_actions:
            # Review the research summary
            text_to_review = results[0].content if results else user_query
            rev_ctx = {
                "text_to_review": text_to_review,
                "criteria": "accuracy and usefulness",
            }
            rev_result = self.reviewer.run("Review the research findings", rev_ctx)
            results.append(rev_result)
            agents_used.add("reviewer")

        return self._build_final_answer(user_query, results, list(agents_used))

    def _decide(self, query: str, results: List[SubAgentResult]) -> CoordinatorDecision:
        """
        Very simple heuristic decision maker.
        On the exam you would replace this with a proper structured LLM call.
        """
        research = next((r for r in results if r.agent == "research"), None)

        if research is None or not research.success:
            return CoordinatorDecision(
                status="need_more_info",
                confidence=0.3,
                next_actions=["developer", "reviewer"],
                reason="Research failed or returned no data – trying other agents",
            )

        if "no relevant" in research.content.lower() or research.error_category == "no_data":
            return CoordinatorDecision(
                status="need_more_info",
                confidence=0.4,
                next_actions=["developer"],
                reason="Research returned no useful data",
            )

        # For this lab we often stop after research + optional review
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
