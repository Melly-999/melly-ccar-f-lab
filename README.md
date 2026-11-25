# Melly CCAR-F Lab

Isolated laboratory environment for preparing to the **Claude Certified Architect – Foundations (CCAR-F)** exam.

This repository is intentionally separate from production projects (MellyCore, Hermes, Yuzuki, Melly IDE) so we can experiment freely with agent patterns, MCP servers, Claude Code configurations and reliability techniques.

## Structure

```
melly-ccar-f-lab/
├── lab-01-multi-agent-coordinator/   # Domain 1 (27%) – Agentic Architecture
├── lab-02-claude-code-workspace/     # Domain 3 (20%) – Claude Code Config
├── lab-03-mcp-server/                # Domain 2 (18%) – Tool Design & MCP
├── lab-04-structured-extraction/     # Domain 4 (20%) – Prompt Engineering
├── lab-05-context-reliability/       # Domain 5 (15%) – Context & Reliability
├── progress.md                       # Competence matrix
└── notes/                            # Obsidian-style study notes
```

## Current Focus

**Lab 01 – Multi-Agent Research Coordinator**

A production-minded implementation of the classic coordinator + specialized subagents pattern that appears heavily on the exam.

See `lab-01-multi-agent-coordinator/README.md` for full details, acceptance criteria and how to run it.

## How to use this repo

1. Work only inside the `lab-0X-...` folders.
2. After finishing a lab, update `progress.md`.
3. Keep evidence (logs, sample runs, screenshots) inside each lab's `evidence/` folder.
4. Never mix this code with production Melly/Hermes repositories.

---

Prepared for CCAR-F (Exam Guide v1.1, November 2026).
