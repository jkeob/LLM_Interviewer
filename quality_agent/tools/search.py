# quality_agent/tools/search.py

import os
import httpx

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_URL = "https://api.tavily.com/search"

async def search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web using Tavily and return a list of results."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TAVILY_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()

    return [
        {
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content"),
        }
        for r in data.get("results", [])
    ]
