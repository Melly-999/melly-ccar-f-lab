# MCP – Short Overview (November 2026)

## What is MCP?

Model Context Protocol is an open standard (originally from Anthropic) that lets LLM applications connect to external tools and data sources in a standardized way.

Think of it as "USB-C for AI agents".

### Core roles

- **Host** – the AI application (Claude Desktop, Claude Code, your own agent runtime)
- **Client** – the connector inside the host that talks to a server
- **Server** – the service that exposes tools, resources and (now) skills

### Main features a server can offer

| Feature     | Purpose                                      |
|-------------|----------------------------------------------|
| Tools       | Actions the model can call (with JSON schema)|
| Resources   | Read-only data the model can pull            |
| Prompts     | Reusable prompt templates                    |
| Skills      | Multi-step guidance (public beta late 2026)  |
| Tasks       | Long-running background work (GA Nov 2026)   |
| Elicitation | Ask the user for missing info mid-task       |

## Popular / reference servers (useful for labs)

Official / reference (modelcontextprotocol/servers):
- Filesystem
- Fetch
- Git
- Memory / Knowledge Graph
- Sequential Thinking
- Time

Highly used community / vendor servers:
- GitHub (official)
- Playwright (Microsoft)
- Context7 (Upstash) – up-to-date library docs
- Chrome DevTools
- Various database, Notion, Linear, Sentry servers

There are now tens of thousands of MCP servers across registries (Glama, mcp.so, Official Registry, etc.).

## Relevance for CCAR-F

Domain 2 (Tool Design & MCP Integration – 18%) tests exactly:
- good tool descriptions + input schemas
- structured error responses
- least-privilege / tool scoping
- when to use MCP vs direct tools
- handling of transient vs permanent failures

In Lab 03 we will replace the mock tools in this repository with a real MCP server.
