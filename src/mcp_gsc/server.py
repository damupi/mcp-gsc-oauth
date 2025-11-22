"""Google Search Console MCP Server - Main Server Module"""

from fastmcp import FastMCP

from mcp_gsc import prompts, resources, tools

# Create FastMCP server instance
# Authentication is automatically configured from environment variables:
# - FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.google.GoogleProvider
# - FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID
# - FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET
# - FASTMCP_SERVER_AUTH_GOOGLE_REQUIRED_SCOPES
# See .env.example for full configuration options
mcp = FastMCP(
    name="Google Search Console",
    description="Provides programmatic access to Google Search Console. "
                "Capabilities include querying search analytics, managing sitemaps, "
                "inspecting URL indexing status, and managing sites."
)


# ============================================================================
# CUSTOM ROUTES - Additional HTTP endpoints
# ============================================================================

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request) -> dict:
    """Health check endpoint for monitoring and load balancers."""
    from starlette.responses import JSONResponse
    return JSONResponse({
        "status": "healthy",
        "service": "Google Search Console MCP Server",
        "version": "1.0.0"
    })


# ============================================================================
# TOOLS - Actions that LLMs can perform
# ============================================================================

@mcp.tool(tags=["Analytics"], metadata={"author": "damupi", "version": "0.1.0"})
async def query_search_analytics(
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: list[str] | None = None,
    row_limit: int = 1000,
    start_row: int = 0,
) -> dict:
    """
    Query search analytics data for a site with filters and parameters.
    
    Args:
        site_url: The site URL (e.g., "https://example.com/")
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        dimensions: Dimensions to group by (query, page, country, device, searchAppearance, date)
        row_limit: Maximum rows to return (default: 1000, max: 25000)
        start_row: Zero-based index of first row to return
        
    Returns:
        Search analytics data with clicks, impressions, CTR, and position metrics
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.query_search_analytics(
        site_url, start_date, end_date, dimensions, row_limit, start_row, ctx
    )


@mcp.tool(tags=["Sitemaps"], metadata={"author": "damupi", "version": "0.1.0"})
async def list_sitemaps(site_url: str) -> dict:
    """
    List all sitemaps for a site.
    
    Args:
        site_url: The site URL
        
    Returns:
        List of sitemaps with submission status and error information
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.list_sitemaps(site_url, ctx)


@mcp.tool(tags=["Sitemaps"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_sitemap(site_url: str, feedpath: str) -> dict:
    """
    Get information about a specific sitemap.
    
    Args:
        site_url: The site URL
        feedpath: The sitemap URL
        
    Returns:
        Sitemap details including submission date, errors, and warnings
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.get_sitemap(site_url, feedpath, ctx)


@mcp.tool(tags=["Sitemaps"], metadata={"author": "damupi", "version": "0.1.0"})
async def submit_sitemap(site_url: str, feedpath: str) -> dict:
    """
    Submit a sitemap to Google.
    
    Args:
        site_url: The site URL
        feedpath: The sitemap URL to submit
        
    Returns:
        Confirmation of submission
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.submit_sitemap(site_url, feedpath, ctx)


@mcp.tool(tags=["Sitemaps"], metadata={"author": "damupi", "version": "0.1.0"})
async def delete_sitemap(site_url: str, feedpath: str) -> dict:
    """
    Delete a sitemap from Google Search Console.
    
    Args:
        site_url: The site URL
        feedpath: The sitemap URL to delete
        
    Returns:
        Confirmation of deletion
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.delete_sitemap(site_url, feedpath, ctx)


@mcp.tool(tags=["Sites"], metadata={"author": "damupi", "version": "0.1.0"})
async def list_sites() -> dict:
    """
    List all sites in the user's Search Console account.
    
    Returns:
        List of sites with permission levels
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.list_sites(ctx)


@mcp.tool(tags=["Sites"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_site(site_url: str) -> dict:
    """
    Get information about a specific site.
    
    Args:
        site_url: The site URL
        
    Returns:
        Site details and permission level
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.get_site(site_url, ctx)


@mcp.tool(tags=["Sites"], metadata={"author": "damupi", "version": "0.1.0"})
async def add_site(site_url: str) -> dict:
    """
    Add a site to Search Console account.
    
    Args:
        site_url: The site URL to add
        
    Returns:
        Confirmation of site addition
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.add_site(site_url, ctx)


@mcp.tool(tags=["Sites"], metadata={"author": "damupi", "version": "0.1.0"})
async def delete_site(site_url: str) -> dict:
    """
    Remove a site from Search Console account.
    
    Args:
        site_url: The site URL to remove
        
    Returns:
        Confirmation of site removal
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.delete_site(site_url, ctx)


@mcp.tool(tags=["Inspection"], metadata={"author": "damupi", "version": "0.1.0"})
async def inspect_url(
    inspection_url: str,
    site_url: str,
    language_code: str = "en-US"
) -> dict:
    """
    Inspect the Google index status of a specific URL.
    
    Args:
        inspection_url: The URL to inspect
        site_url: The site URL that owns the inspection URL
        language_code: Language code (default: "en-US")
        
    Returns:
        Detailed index status including coverage, indexing issues, mobile usability, etc.
    """
    from fastmcp import Context
    ctx = Context.get_current()
    return await tools.inspect_url(inspection_url, site_url, language_code, ctx)


# ============================================================================
# RESOURCES - Read-only data sources
# ============================================================================

@mcp.resource("gsc://sites", tags=["Sites"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_sites_resource() -> str:
    """List all available sites in the user's Search Console account."""
    return await resources.get_sites_list()


@mcp.resource("gsc://config", tags=["Configuration"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_config_resource() -> str:
    """Get server configuration and status."""
    return await resources.get_config()


@mcp.resource("gsc://sites/{site_url}/analytics/summary", tags=["Analytics"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_analytics_summary_resource(site_url: str) -> str:
    """Get a summary of recent search analytics for a site (last 28 days)."""
    return await resources.get_analytics_summary(site_url)


@mcp.resource("gsc://sites/{site_url}/sitemaps", tags=["Sitemaps"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_sitemaps_resource(site_url: str) -> str:
    """Get all sitemaps for a specific site."""
    return await resources.get_site_sitemaps(site_url)


@mcp.resource("gsc://sites/{site_url}/top-queries", tags=["Analytics"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_top_queries_resource(site_url: str) -> str:
    """Get top performing queries for a site (last 7 days, top 10)."""
    return await resources.get_top_queries(site_url)


@mcp.resource("gsc://sites/{site_url}/top-pages", tags=["Analytics"], metadata={"author": "damupi", "version": "0.1.0"})
async def get_top_pages_resource(site_url: str) -> str:
    """Get top performing pages for a site (last 7 days, top 10)."""
    return await resources.get_top_pages(site_url)


# ============================================================================
# PROMPTS - Reusable templates for LLM interactions
# ============================================================================

@mcp.prompt(tags=["Analytics"], metadata={"author": "damupi", "version": "0.1.0"})
def analyze_search_performance(site_url: str, time_period: str = "last 30 days") -> str:
    """
    Generate a prompt for analyzing search performance.
    
    Args:
        site_url: The site to analyze
        time_period: Time period description (e.g., "last 30 days")
    """
    return prompts.analyze_search_performance(site_url, time_period)


@mcp.prompt(tags=["SEO"], metadata={"author": "damupi", "version": "0.1.0"})
def seo_recommendations(site_url: str, focus_area: str = "general") -> str:
    """
    Generate a prompt for SEO recommendations.
    
    Args:
        site_url: The site to analyze
        focus_area: Specific area to focus on (queries, pages, technical, general)
    """
    return prompts.seo_recommendations(site_url, focus_area)


@mcp.prompt(tags=["Analytics"], metadata={"author": "damupi", "version": "0.1.0"})
def compare_periods(
    site_url: str,
    period1_start: str,
    period1_end: str,
    period2_start: str,
    period2_end: str
) -> str:
    """
    Generate a prompt for comparing two time periods.
    
    Args:
        site_url: The site to analyze
        period1_start: First period start date (YYYY-MM-DD)
        period1_end: First period end date (YYYY-MM-DD)
        period2_start: Second period start date (YYYY-MM-DD)
        period2_end: Second period end date (YYYY-MM-DD)
    """
    return prompts.compare_periods(
        site_url, period1_start, period1_end, period2_start, period2_end
    )


@mcp.prompt(tags=["Inspection"], metadata={"author": "damupi", "version": "0.1.0"})
def indexing_health_check(site_url: str) -> str:
    """
    Generate a prompt for checking indexing health.
    
    Args:
        site_url: The site to check
    """
    return prompts.indexing_health_check(site_url)


# ============================================================================
# Entry point for running the server
# ============================================================================

if __name__ == "__main__":
    # Run the server with HTTP transport support
    # Usage:
    #   Development (STDIO): fastmcp dev src/mcp_gsc/server.py
    #   Production (HTTP): fastmcp run src/mcp_gsc/server.py --transport http --host localhost --port 8000
    mcp.run()

