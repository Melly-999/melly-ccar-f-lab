# Lab 01 – Architecture Notes

## High-level flow

1. User sends a query to the Coordinator.
2. Coordinator analyzes the query and decides which subagents are needed.
3. Coordinator builds a **minimal context package** for each required subagent.
4. Subagents run (can be sequential or parallel).
5. Coordinator receives structured results from each subagent.
6. Coordinator decides:
   - Is the task complete? → produce final JSON answer
   - Do we need another round? → call more agents or the same ones again with new context
   - Is there a hard failure? → escalate or return error with clear category

## Context isolation rules

| Agent | Receives | Does **not** receive |
|-------|----------|----------------------|
| Research | Original query + any previous research findings that are relevant | Full conversation history, developer code, reviewer comments |
| Developer | Specific files / paths + the exact question about code | Full research dump, unrelated history |
| Reviewer | The artifacts that need review + clear review criteria | Everything else |

This is one of the most important points the exam tests.

## Tool scoping (least privilege)

```python
RESEARCH_TOOLS = ["web_search", "fetch_url"]
DEVELOPER_TOOLS = ["read_file", "list_directory", "search_code"]
REVIEWER_TOOLS = ["analyze_text", "check_consistency"]
```

Even if a prompt tries to make the Research agent edit a file, the runtime simply does not give it that tool.

## Stop / continue decision

The Coordinator uses a simple internal schema:

```json
{
  "status": "complete" | "need_more_info" | "failed",
  "confidence": 0.0-1.0,
  "next_actions": ["research", "developer", ...],
  "reason": "..."
}
```

## Failure handling

- **Transient** (network, rate limit) → retry with backoff
- **Permanent** (tool not found, invalid arguments, policy violation) → stop and report
- **No useful data** → Coordinator must still produce a valid answer (possibly with `requires_human_review: true`)

## Why this design scores well on the exam

- Clear separation of concerns
- Explicit context isolation
- Tool scoping enforced at runtime, not only in prompts
- Structured outputs everywhere
- Conscious handling of the “empty result” case
- Easy to extend later with hooks, session persistence, or human escalation
