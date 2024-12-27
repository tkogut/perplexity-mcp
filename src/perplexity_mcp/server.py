import asyncio
import aiohttp
import sys
import logging

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio
import os


server = Server("perplexity-mcp")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="perplexity_search_web",
            description="Use Perplexity to search the web for a query and return results from the last specified time frame",
            arguments=[
                types.PromptArgument(
                    name="query",
                    description="The query to search for",
                    required=True,
                ),
                types.PromptArgument(
                    name="timeframe",
                    description="The time frame to search for. Allowed options are: 'day', 'week', 'month', 'year'. Defaults to 'month'.",
                    required=False,
                ),
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    """
    if name != "perplexity_search_web":
        raise ValueError(f"Unknown prompt: {name}")

    query = (arguments or {}).get("query", "")
    timeframe = (arguments or {}).get("timeframe", "month")
    return types.GetPromptResult(
        description="Search the web for the query",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Search the web for the query: {query}",
                ),
            ),
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Search for the last: {timeframe}",
                ),
            ),
        ],
    )


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="perplexity_search_web",
            description="Use Perplexity to search the web",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"],
            },
        )
    ]


@server.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "perplexity_search_web":
        query = arguments["query"]
        timeframe = arguments.get("timeframe", "month")
        result = await call_perplexity(query, timeframe)
        return [types.TextContent(type="text", text=str(result))]
    raise ValueError(f"Tool not found: {name}")


async def call_perplexity(query: str, timeframe: str) -> str:

    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": query},
        ],
        "max_tokens": "512",
        "temperature": 0.2,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": timeframe,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]


async def main():
    API_KEY = os.getenv("PERPLEXITY_API_KEY")
    if not API_KEY:
        raise ValueError("PERPLEXITY_API_KEY environment variable is required")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="perplexity-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def cli():
    """CLI entry point for perplexity-mcp"""
    logging.basicConfig(level=logging.INFO)

    API_KEY = os.getenv("PERPLEXITY_API_KEY")
    if not API_KEY:
        print(
            "Error: PERPLEXITY_API_KEY environment variable is required",
            file=sys.stderr,
        )
        sys.exit(1)

    asyncio.run(main())


if __name__ == "__main__":
    cli()
