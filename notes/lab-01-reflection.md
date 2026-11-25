# Lab 01 Reflection

**Date:** 2026-11-25

## What I implemented

- Coordinator + 3 specialized subagents (Research, Developer, Reviewer)
- Strict context isolation (each agent gets only what it needs)
- Tool scoping enforced by which tools are imported into each agent
- Structured Pydantic models for all I/O
- Explicit handling of “no data” and failure cases
- Simple decision heuristic inside the Coordinator

## Key architectural lessons for the exam

1. **Context isolation is not optional** – giving every agent the full history is an anti-pattern.
2. **Tool availability is stronger than prompt instructions** – the runtime must enforce least privilege.
3. **Always return structured output** – even on failure.
4. **The Coordinator owns the conversation** – subagents should not talk to each other directly.
5. **Empty / failed research is a first-class case** that must still produce a coherent FinalAnswer.

## What I would improve next

- Replace the heuristic `_decide()` with a real structured LLM call.
- Add parallel execution of independent subagents.
- Add session / state persistence so a conversation can be resumed.
- Add deterministic safety hooks (e.g. block certain tools completely).

## Mapping to exam domains

- Agentic Loop & Orchestration → covered
- Context isolation → covered
- Tool scoping → covered
- Structured output → covered
- Error categories (transient / permanent / no_data) → covered
