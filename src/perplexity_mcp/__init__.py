from . import server
import asyncio


def main():
    """Main entry point for the package."""
    asyncio.run(server.main())


# Optionally expose other important items at package level
__all__ = ["main", "server"]

"""Perplexity MCP package."""

__version__ = "0.1.4"
