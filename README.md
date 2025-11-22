# Google Search Console MCP Server

A Model Context Protocol (MCP) server that provides LLMs with programmatic access to Google Search Console data and functionality. Built with [FastMCP](https://github.com/jlowin/fastmcp).

## Features

### 🛠️ Tools (13 Actions)

**Search Analytics**
- `query_search_analytics` - Query search traffic data with filters and dimensions

**Sitemap Management**
- `list_sitemaps` - List all sitemaps for a site
- `get_sitemap` - Get details about a specific sitemap
- `submit_sitemap` - Submit a sitemap to Google
- `delete_sitemap` - Remove a sitemap

**Site Management**
- `list_sites` - List all sites in your Search Console account
- `get_site` - Get information about a specific site
- `add_site` - Add a site to Search Console
- `delete_site` - Remove a site from Search Console

**URL Inspection**
- `inspect_url` - Inspect the Google index status of a specific URL

### 📊 Resources (6 Data Sources)

- `gsc://sites` - List all available sites
- `gsc://config` - Server configuration and status
- `gsc://sites/{site_url}/analytics/summary` - Recent analytics summary (28 days)
- `gsc://sites/{site_url}/sitemaps` - Site sitemaps
- `gsc://sites/{site_url}/top-queries` - Top 10 queries (7 days)
- `gsc://sites/{site_url}/top-pages` - Top 10 pages (7 days)

### 💬 Prompts (4 Templates)

- `analyze_search_performance` - Generate SEO performance analysis prompt
- `seo_recommendations` - Generate SEO recommendations prompt
- `compare_periods` - Generate period-over-period comparison prompt
- `indexing_health_check` - Generate indexing health check prompt

## Installation

### Prerequisites

- Python 3.10 or higher
- Google Cloud Project with Search Console API enabled
- OAuth 2.0 credentials from Google Cloud Console

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-gsc.git
cd mcp-gsc

# Install with uv (recommended)
uv sync

# Or install in development mode
uv pip install -e .
```

## Authentication Setup

### Step 1: Create Google OAuth 2.0 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select an existing one
3. Enable the **Google Search Console API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen if prompted
6. Choose **Web application** as application type
7. Add authorized redirect URI: `http://localhost:8000/auth/callback`
8. Save your **Client ID** and **Client Secret**

### Step 2: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.google.GoogleProvider
FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET=GOCSPX-your-client-secret
FASTMCP_SERVER_AUTH_GOOGLE_REQUIRED_SCOPES=openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/webmasters
```

## Usage

### Running the Server

**Development Mode (STDIO)**
```bash
fastmcp dev src/mcp_gsc/server.py
```

**Production Mode (HTTP Transport)**
```bash
# Run with HTTP transport for remote access
fastmcp run src/mcp_gsc/server.py --transport http

# Specify custom host and port
fastmcp run src/mcp_gsc/server.py --transport http --host 0.0.0.0 --port 8080
```

The server will start on `http://localhost:8000` by default (HTTP mode).

### Running with Docker

**Quick Start:**
```bash
# Build the Docker image
make build

# Start the server
make up

# View logs
make logs

# Stop the server
make down
```

**Available Make Commands:**
- `make build` - Build the Docker image
- `make up` - Start the MCP server in background
- `make down` - Stop the MCP server
- `make restart` - Restart the server
- `make logs` - View server logs (follow mode)
- `make logs-tail` - View last 100 lines of logs
- `make status` - Check server status
- `make clean` - Remove all Docker resources
- `make shell` - Open a shell in the running container
- `make rebuild` - Rebuild and restart
- `make dev` - Run with live logs
- `make test` - Test server health endpoint

**Docker Configuration:**

The server runs in a Docker container with:
- Python 3.12 slim base image
- UV for fast dependency management
- HTTP transport on port 8000
- Automatic restart on failure
- Health checks every 30 seconds

Make sure your `.env` file is configured before running `make up`.

### Authentication Flow

1. Start the server
2. Connect with an MCP client (e.g., Claude Desktop)
3. You'll be redirected to Google OAuth login
4. Grant permissions to access Search Console data
5. You'll be redirected back and authenticated

### Using with Claude Desktop

**Option 1: STDIO Transport (Local)**

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "gsc-mcp-server": {
      "command": "fastmcp",
      "args": ["run", "src/mcp_gsc/server.py"],
      "env": {
        "FASTMCP_SERVER_AUTH": "fastmcp.server.auth.providers.google.GoogleProvider",
        "FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID": "your-client-id.apps.googleusercontent.com",
        "FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET": "GOCSPX-your-client-secret",
        "FASTMCP_SERVER_AUTH_GOOGLE_REQUIRED_SCOPES": "openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/webmasters"
      }
    }
  }
}
```

**Option 2: HTTP Transport (Remote)**

First, start the server with HTTP transport:
```bash
fastmcp run src/mcp_gsc/server.py --transport http
```

Then configure Claude Desktop to connect via HTTP:
```json
{
  "mcpServers": {
    "gsc-mcp-server": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://localhost:8000/mcp"
      ]  
    }
  }
} 
```

### Debugging with MCP Inspector

You can use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to test and debug the server.

**For Local Development:**
```bash
npx @modelcontextprotocol/inspector fastmcp dev src/mcp_gsc/server.py
```

**For Docker/Remote Server:**
```bash
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

## Example Usage

### Query Search Analytics

```python
# Ask Claude:
"Show me the top 10 search queries for https://example.com/ 
from 2024-01-01 to 2024-01-31"

# Claude will use:
query_search_analytics(
    site_url="https://example.com/",
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimensions=["query"],
    row_limit=10
)
```

### Get Analytics Summary

```python
# Ask Claude:
"What's the recent search performance for https://example.com/?"

# Claude will access the resource:
gsc://sites/https%3A%2F%2Fexample.com%2F/analytics/summary
```

### SEO Analysis

```python
# Ask Claude:
"Analyze the search performance for https://example.com/ 
and give me SEO recommendations"

# Claude will use the prompt:
analyze_search_performance(
    site_url="https://example.com/",
    time_period="last 30 days"
)
```

## Available Dimensions for Analytics

When using `query_search_analytics`, you can group data by:

- `query` - Search queries
- `page` - Landing pages
- `country` - Countries
- `device` - Device types (desktop, mobile, tablet)
- `searchAppearance` - How the result appeared in search
- `date` - Dates

## API Scopes

The server requires these OAuth scopes:

- `openid` - User identification
- `https://www.googleapis.com/auth/userinfo.email` - User email
- `https://www.googleapis.com/auth/webmasters` - Full Search Console access

For read-only access, modify `src/mcp_gsc/auth.py` to use `webmasters.readonly` scope.

## Development

### Project Structure

```
mcp-gsc/
├── src/mcp_gsc/
│   ├── __init__.py       # Package initialization
│   ├── server.py         # Main FastMCP server
│   ├── auth.py           # Google OAuth authentication
│   ├── tools.py          # MCP tools (13 actions)
│   ├── resources.py      # MCP resources (6 data sources)
│   ├── prompts.py        # MCP prompts (4 templates)
│   └── utils.py          # Utility functions
├── examples/             # Usage examples
├── pyproject.toml        # Project configuration
├── .env.example          # Environment variables template
└── README.md             # This file
```

### Running Tests

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
pytest

# Run linting
ruff check src/
```

## Troubleshooting

### Authentication Errors

**Problem**: "Authentication failed" or "401 Unauthorized"

**Solution**: 
- Verify your OAuth credentials are correct
- Check that the redirect URI matches exactly: `http://localhost:8000/auth/callback`
- Ensure the Search Console API is enabled in your Google Cloud project

### Permission Denied (403)

**Problem**: "Permission denied" when accessing a site

**Solution**:
- Verify you have access to the site in Google Search Console
- Check that you're using the correct site URL format (e.g., `https://example.com/`)
- Ensure your OAuth token has the required scopes

### Rate Limiting (429)

**Problem**: "Rate limit exceeded"

**Solution**:
- Google Search Console API has a limit of 1,200 queries per minute
- Reduce the frequency of requests
- Implement exponential backoff in your client

### Site URL Encoding

When using resources with site URLs, the URL must be URL-encoded:

```
# Correct
gsc://sites/https%3A%2F%2Fexample.com%2F/analytics/summary

# Incorrect
gsc://sites/https://example.com//analytics/summary
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- [FastMCP Documentation](https://fastmcp.wiki)
- [Google Search Console API](https://developers.google.com/webmaster-tools/v1/api_reference_index)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [FastMCP Discord](https://discord.gg/fastmcp)
- Review [Google Search Console API docs](https://developers.google.com/webmaster-tools)
