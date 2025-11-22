"""
Example: Basic Usage of Google Search Console MCP Server

This example demonstrates how to use the MCP client to interact with
the Google Search Console server.
"""

import asyncio
from datetime import datetime, timedelta

from fastmcp.client import MCPClient


async def main():
    """Demonstrate basic usage of the GSC MCP server."""
    
    # Connect to the MCP server
    async with MCPClient("http://localhost:8000") as client:
        
        print("=" * 60)
        print("Google Search Console MCP Server - Basic Usage Example")
        print("=" * 60)
        
        # 1. List all sites
        print("\n1. Listing all sites...")
        sites_result = await client.call_tool("list_sites")
        print(f"Found {sites_result['total']} sites")
        
        if sites_result['total'] > 0:
            site_url = sites_result['sites'][0]['siteUrl']
            print(f"Using site: {site_url}")
            
            # 2. Get analytics summary via resource
            print("\n2. Getting analytics summary...")
            from urllib.parse import quote
            encoded_url = quote(site_url, safe='')
            summary = await client.read_resource(
                f"gsc://sites/{encoded_url}/analytics/summary"
            )
            print(f"Summary: {summary}")
            
            # 3. Query search analytics
            print("\n3. Querying search analytics...")
            end_date = datetime.now() - timedelta(days=3)
            start_date = end_date - timedelta(days=7)
            
            analytics_result = await client.call_tool(
                "query_search_analytics",
                site_url=site_url,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                dimensions=["query"],
                row_limit=5
            )
            
            print(f"Top 5 queries:")
            for row in analytics_result['rows'][:5]:
                print(f"  - {row['dimension_0']}: {row['clicks']} clicks, "
                      f"{row['impressions']} impressions, "
                      f"{row['ctr']}% CTR")
            
            # 4. List sitemaps
            print("\n4. Listing sitemaps...")
            sitemaps_result = await client.call_tool(
                "list_sitemaps",
                site_url=site_url
            )
            print(f"Found {sitemaps_result['total']} sitemaps")
            
            # 5. Get top pages via resource
            print("\n5. Getting top pages...")
            top_pages = await client.read_resource(
                f"gsc://sites/{encoded_url}/top-pages"
            )
            print(f"Top pages: {top_pages}")
            
            # 6. Use a prompt
            print("\n6. Using SEO analysis prompt...")
            prompt_result = await client.get_prompt(
                "analyze_search_performance",
                site_url=site_url,
                time_period="last 7 days"
            )
            print(f"Generated prompt:\n{prompt_result[:200]}...")
            
        else:
            print("No sites found. Please add a site to Google Search Console first.")
        
        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
