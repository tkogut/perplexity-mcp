# perplexity-mcp MCP server

A Model Context Protocol (MCP) server that provides web search functionality using [Perplexity AI's](https://www.perplexity.ai/) API.  Works with the [Anthropic](https://www.anthropic.com/news/model-context-protocol) Claude desktop client. 

## Example
Let's you use prompts like,  "Search the web to find out what's new at Anthropic in the past week."

## Glama Scores
<a href="https://glama.ai/mcp/servers/ebg0za4hn9"><img width="380" height="200" src="https://glama.ai/mcp/servers/ebg0za4hn9/badge" alt="Perplexity Server MCP server" /></a>

## Components

### Prompts

The server provides a single prompt:
- perplexity_search_web: Search the web using Perplexity AI
  - Required "query" argument for the search query
  - Optional "recency" argument to filter results by time period:
    - 'day': last 24 hours
    - 'week': last 7 days
    - 'month': last 30 days (default)
    - 'year': last 365 days
  - Uses Perplexity's API to perform web searches

### Tools

The server implements one tool:
- perplexity_search_web: Search the web using Perplexity AI
  - Takes "query" as a required string argument
  - Optional "recency" parameter to filter results (day/week/month/year)
  - Returns search results from Perplexity's API

## Installation


### Requires [UV](https://github.com/astral-sh/uv) (Fast Python package and project manager)

If uv isn't installed. 

```bash 
# Using Homebrew on macOS 
brew install uv
```

or

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```


Next, install the MCP server

```bash
# Install from PyPi
uv pip install perplexity-mcp
```
or 

```bash
# Install from source
uv pip install git+https://github.com/jsonallen/perplexity-mcp.git
```

### Environment Variables

The following environment variable is required in your claude_desktop_config.json. You can obtain an API key from [Perplexity](https://perplexity.ai)

- `PERPLEXITY_API_KEY`: Your Perplexity AI API key


#### Claude Desktop

Add this tool as a mcp server by editing the Claude config file.

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`


  ```json
    "perplexity-mcp": {
      "env": {
        "PERPLEXITY_API_KEY": "XXXXXXXXXXXXXXXXXXXX"
      },
      "command": "uv",
      "args": [
        "run",
        "perplexity-mcp"
      ]
    }
  ```
  To verify the server is working.  Open the Claude client and use a prompt like "search the web for news about openai in the past week".  You should see an alert box open to confirm tool usage. Click "Allow for this chat".
  
  <img width="800" alt="mcp_screenshot" src="https://github.com/user-attachments/assets/096fec0c-5022-4aec-96f0-c52c0efd7084" />

