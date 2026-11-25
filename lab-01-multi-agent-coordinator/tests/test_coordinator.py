import pytest
from src.coordinator import Coordinator
from src.schemas import FinalAnswer


def test_basic_research_flow():
    coord = Coordinator()
    result = coord.run("What is Model Context Protocol?")

    assert isinstance(result, FinalAnswer)
    assert result.status in {"success", "partial"}
    assert "research" in result.agents_used
    assert result.confidence > 0.0
    assert len(result.answer) > 20


def test_empty_query_handling():
    coord = Coordinator()
    result = coord.run("")

    assert isinstance(result, FinalAnswer)
    # Even empty query should produce a structured response
    assert result.status in {"success", "partial", "failed"}


def test_final_answer_schema():
    coord = Coordinator()
    result = coord.run("Explain agentic loops")

    data = result.model_dump()
    assert "status" in data
    assert "answer" in data
    assert "confidence" in data
    assert "agents_used" in data
    assert "requires_human_review" in data
