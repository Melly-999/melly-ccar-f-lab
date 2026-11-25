# Lab 01 – Multi-Agent Research Coordinator

**Exam Domain:** Agentic Architecture & Orchestration (27%)  
**Status:** Real Claude decision logic added (Nov 2026)

---

## What changed in the latest update

- Decision logic is now powered by a real Claude structured call (`src/llm.py`)
- Coordinator can run multiple rounds until the decision is `complete` or `failed`
- Clear separation between LLM decision mode and heuristic fallback (for tests)
- Architecture notes updated with MCP context

## How to run

```bash
cd lab-01-multi-agent-coordinator
pip install -r requirements.txt

# Required
export ANTHROPIC_API_KEY=sk-ant-...

# Interactive demo
python main.py

# Tests (heuristic mode, no API key needed if you set use_llm_decision=False in tests)
pytest tests/ -v
```

## Acceptance Criteria (still the same)

- [x] Coordinator owns the conversation
- [x] Each subagent receives minimal context
- [x] Tool scoping per role
- [x] Structured FinalAnswer always returned
- [x] Explicit handling of no-data / failure cases
- [x] Decision point is now a real Claude call (exam-relevant)

## Next recommended steps for you

1. Read `architecture.md` and `src/coordinator.py` carefully
2. Run a few queries and observe the decision JSON
3. Give feedback / request changes
4. Then we move to Lab 03 (real MCP server) or improve parallel execution
