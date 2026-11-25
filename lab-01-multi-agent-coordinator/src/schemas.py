from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class SubAgentResult(BaseModel):
    agent: Literal["research", "developer", "reviewer"]
    success: bool
    content: str
    sources: List[str] = Field(default_factory=list)
    error: Optional[str] = None
    error_category: Optional[Literal["transient", "permanent", "no_data"]] = None


class CoordinatorDecision(BaseModel):
    status: Literal["complete", "need_more_info", "failed"]
    confidence: float = Field(ge=0.0, le=1.0)
    next_actions: List[Literal["research", "developer", "reviewer"]] = Field(default_factory=list)
    reason: str


class FinalAnswer(BaseModel):
    status: Literal["success", "partial", "failed"]
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)
    agents_used: List[str] = Field(default_factory=list)
    requires_human_review: bool = False
    notes: Optional[str] = None
