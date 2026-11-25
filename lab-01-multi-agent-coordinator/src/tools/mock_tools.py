"""
Simple mock tools so the lab runs without external dependencies.
Replace these with real implementations or MCP tools later.
"""

from typing import List, Dict, Any
import time


def web_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Mock web search."""
    time.sleep(0.3)  # simulate latency
    return {
        "query": query,
        "results": [
            {
                "title": f"Result about {query} #{i+1}",
                "url": f"https://example.com/{query.replace(' ', '-')}-{i+1}",
                "snippet": f"This is a simulated search result for '{query}'. Useful information here.",
            }
            for i in range(min(max_results, 3))
        ],
    }


def fetch_url(url: str) -> Dict[str, Any]:
    """Mock URL fetch."""
    return {
        "url": url,
        "content": f"Simulated content fetched from {url}. This would be the page text in a real system.",
        "status_code": 200,
    }


def read_file(path: str) -> Dict[str, Any]:
    """Mock file read."""
    return {
        "path": path,
        "content": f"# Simulated content of {path}\n\ndef example():\n    return 'hello from {path}'\n",
        "exists": True,
    }


def list_directory(path: str = ".") -> Dict[str, Any]:
    """Mock directory listing."""
    return {
        "path": path,
        "entries": ["src/", "tests/", "README.md", "architecture.md", "requirements.txt"],
    }


def search_code(query: str, path: str = ".") -> Dict[str, Any]:
    """Mock code search."""
    return {
        "query": query,
        "matches": [
            {"file": "src/coordinator.py", "line": 42, "snippet": f"# contains {query}"},
            {"file": "src/agents/research.py", "line": 15, "snippet": f"def search_{query}():"},
        ],
    }


def analyze_text(text: str, criteria: str = "clarity") -> Dict[str, Any]:
    """Mock text analysis."""
    return {
        "criteria": criteria,
        "score": 0.82,
        "comments": [
            "The text is generally clear.",
            "Consider adding more concrete examples.",
        ],
    }


def check_consistency(items: List[str]) -> Dict[str, Any]:
    """Mock consistency check."""
    return {
        "consistent": True,
        "issues": [],
        "summary": "No major inconsistencies found in the provided items.",
    }
