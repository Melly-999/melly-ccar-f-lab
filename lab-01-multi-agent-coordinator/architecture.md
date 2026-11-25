# Lab 01 – Architecture Notes (updated)

## High-level flow

1. User sends a query to the Coordinator.
2. Coordinator always starts with the Research agent (minimal context).
3. Coordinator asks Claude (structured output) what to do next.
4. Based on the decision it may call Developer and/or Reviewer.
5. Loop continues up to `max_rounds` or until the decision is `complete` / `failed`.
6. Always returns a valid `FinalAnswer` (even on total failure).

## Context isolation rules (exam critical)

| Agent     | Receives                                      | Does **not** receive                  |
|-----------|-----------------------------------------------|---------------------------------------|
| Research  | Original query + optional previous findings   | Full history, code, reviewer notes    |
| Developer | Specific coding question + relevant paths     | Full research dump, unrelated history |
| Reviewer  | Artifacts to review + clear criteria         | Everything else                       |

## Tool scoping (least privilege)

Tools are imported only into the agents that are allowed to use them.
Even if a prompt tries to make Research edit a file, the runtime simply does not give it that capability.

## Decision logic (now real Claude call)

The method `_decide()` can run in two modes:

- `use_llm_decision=True` (default) → Claude returns a structured `CoordinatorDecision`
- `use_llm_decision=False` → simple heuristic (useful for unit tests / offline)

This is the most important architectural piece for the exam:
the Coordinator owns the conversation and makes explicit, inspectable decisions.

## Failure handling

- Transient errors → can be retried (future improvement)
- Permanent / no_data → reported cleanly in `FinalAnswer`
- Empty useful results → still produces a coherent structured answer

## Relation to MCP (for later labs)

In a full production system the tools used by Research / Developer / Reviewer
would typically come from MCP servers instead of the current mock implementations.

MCP gives us:
- standardized tool discovery (`tools/list`)
- structured input schemas
- resources (read-only data)
- prompts / skills (new in 2026)
- Tasks & Elicitation for long-running work

See `notes/mcp-overview.md` for a short summary of the current MCP landscape.
