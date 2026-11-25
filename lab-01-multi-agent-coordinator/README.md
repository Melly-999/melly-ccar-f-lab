# Lab 01 – Multi-Agent Research Coordinator

**Exam Domain:** Agentic Architecture & Orchestration (27%)  
**Goal:** Implement a clean, production-oriented coordinator + subagents pattern with strict context isolation and tool scoping.

This lab is deliberately simplified so you can focus on the architectural decisions the exam tests, not on production complexity.

---

## Architecture Overview

```
User Query
    │
    ▼
┌─────────────────────┐
│   Coordinator       │  ← owns the conversation, decides next steps
│                     │
│  - decomposes task  │
│  - calls subagents  │
│  - aggregates       │
│  - decides finish   │
└─────────┬───────────┘
          │
    ┌─────┴─────┬─────────────────┐
    ▼           ▼                 ▼
┌────────┐  ┌──────────┐   ┌──────────┐
│Research│  │Developer │   │ Reviewer │
│Agent   │  │Agent     │   │ Agent    │
└────────┘  └──────────┘   └──────────┘
```

### Key Design Decisions (exam-relevant)

| Decision | Why it matters on the exam |
|----------|---------------------------|
| Each subagent gets **only** the context it needs | Prevents context pollution and token waste |
| Tools are scoped per role | Least privilege – classic security/architecture question |
| Coordinator never lets subagents talk to each other directly | Clear ownership and easier debugging |
| Final output is always structured JSON | Makes the result machine-readable and testable |
| Explicit handling of “no useful results” | Forces you to think about failure modes |

---

## Acceptance Criteria

A lab is considered complete when all of the following are true:

- [x] Coordinator can call any combination of the three subagents
- [x] Each subagent receives a **minimal** context package (not the full history)
- [x] Research agent only has search-related tools
- [x] Developer agent only has read/list tools (no write in this lab)
- [x] Reviewer agent only has analysis tools
- [x] Coordinator decides whether to finish or iterate
- [x] Final answer is always valid JSON according to the schema in `schemas.py`
- [x] Transient errors are retried, permanent errors are reported cleanly
- [x] There is at least one test case where Research returns nothing useful and the system still produces a coherent response

---

## How to run

```bash
cd lab-01-multi-agent-coordinator
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-...

# Run the interactive demo
python main.py

# Or run the test suite
pytest tests/ -v
```

---

## Files

| File | Purpose |
|------|---------|
| `architecture.md` | Detailed design notes + trade-offs |
| `src/coordinator.py` | Main orchestration loop |
| `src/agents/` | The three specialized agents |
| `src/tools/` | Tool implementations (mocked for lab) |
| `src/schemas.py` | Pydantic models for structured I/O |
| `tests/` | Unit + scenario tests |
| `evidence/` | Sample runs and logs (add your own) |

---

## Next steps after this lab

1. Update `progress.md`
2. Write a short reflection in `notes/lab-01-reflection.md`
3. Move to Lab 02 (Claude Code workspace) or Lab 03 (MCP Server)
