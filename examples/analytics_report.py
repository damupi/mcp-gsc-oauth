"""
Example: Generate Analytics Report

This example demonstrates how to generate a comprehensive analytics report
for a website using the Google Search Console MCP server.
"""

import asyncio
from datetime import datetime, timedelta

from fastmcp.client import MCPClient


async def generate_report(client: MCPClient, site_url: str, days: int = 30):
    """
    Generate a comprehensive analytics report for a site.
    
    Args:
        client: MCP client instance
        site_url: Site URL to analyze
        days: Number of days to analyze (default: 30)
    """
    end_date = datetime.now() - timedelta(days=3)  # GSC has ~3 day delay
    start_date = end_date - timedelta(days=days)
    
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    print(f"\n{'=' * 70}")
    print(f"Analytics Report for {site_url}")
    print(f"Period: {start_str} to {end_str} ({days} days)")
    print(f"{'=' * 70}\n")
    
    # 1. Overall Performance
    print("📊 OVERALL PERFORMANCE")
    print("-" * 70)
    
    overall = await client.call_tool(
        "query_search_analytics",
        site_url=site_url,
        start_date=start_str,
        end_date=end_str,
        row_limit=1
    )
    
    if overall['rows']:
        row = overall['rows'][0]
        print(f"Total Clicks:       {row['clicks']:,}")
        print(f"Total Impressions:  {row['impressions']:,}")
        print(f"Average CTR:        {row['ctr']:.2f}%")
        print(f"Average Position:   {row['position']:.1f}")
    
    # 2. Top Queries
    print(f"\n🔍 TOP 10 SEARCH QUERIES")
    print("-" * 70)
    
    queries = await client.call_tool(
        "query_search_analytics",
        site_url=site_url,
        start_date=start_str,
        end_date=end_str,
        dimensions=["query"],
        row_limit=10
    )
    
    print(f"{'Rank':<6} {'Query':<40} {'Clicks':<10} {'Impr.':<10} {'CTR':<8}")
    print("-" * 70)
    for i, row in enumerate(queries['rows'][:10], 1):
        query = row['dimension_0'][:38]  # Truncate long queries
        print(f"{i:<6} {query:<40} {row['clicks']:<10} "
              f"{row['impressions']:<10} {row['ctr']:<8.2f}%")
    
    # 3. Top Pages
    print(f"\n📄 TOP 10 LANDING PAGES")
    print("-" * 70)
    
    pages = await client.call_tool(
        "query_search_analytics",
        site_url=site_url,
        start_date=start_str,
        end_date=end_str,
        dimensions=["page"],
        row_limit=10
    )
    
    print(f"{'Rank':<6} {'Page':<50} {'Clicks':<10}")
    print("-" * 70)
    for i, row in enumerate(pages['rows'][:10], 1):
        page = row['dimension_0'][:48]  # Truncate long URLs
        print(f"{i:<6} {page:<50} {row['clicks']:<10}")
    
    # 4. Performance by Device
    print(f"\n📱 PERFORMANCE BY DEVICE")
    print("-" * 70)
    
    devices = await client.call_tool(
        "query_search_analytics",
        site_url=site_url,
        start_date=start_str,
        end_date=end_str,
        dimensions=["device"],
        row_limit=10
    )
    
    print(f"{'Device':<15} {'Clicks':<10} {'Impressions':<15} {'CTR':<8} {'Pos.':<8}")
    print("-" * 70)
    for row in devices['rows']:
        device = row['dimension_0'].capitalize()
        print(f"{device:<15} {row['clicks']:<10} {row['impressions']:<15} "
              f"{row['ctr']:<8.2f}% {row['position']:<8.1f}")
    
    # 5. Performance by Country (Top 5)
    print(f"\n🌍 TOP 5 COUNTRIES")
    print("-" * 70)
    
    countries = await client.call_tool(
        "query_search_analytics",
        site_url=site_url,
        start_date=start_str,
        end_date=end_str,
        dimensions=["country"],
        row_limit=5
    )
    
    print(f"{'Country':<10} {'Clicks':<10} {'Impressions':<15} {'CTR':<8}")
    print("-" * 70)
    for row in countries['rows']:
        country = row['dimension_0'].upper()
        print(f"{country:<10} {row['clicks']:<10} {row['impressions']:<15} "
              f"{row['ctr']:<8.2f}%")
    
    print(f"\n{'=' * 70}")
    print("Report generated successfully!")
    print(f"{'=' * 70}\n")


async def main():
    """Main function to run the analytics report."""
    
    # Connect to the MCP server
    async with MCPClient("http://localhost:8000") as client:
        
        # Get the first available site
        sites_result = await client.call_tool("list_sites")
        
        if sites_result['total'] > 0:
            site_url = sites_result['sites'][0]['siteUrl']
            
            # Generate report for last 30 days
            await generate_report(client, site_url, days=30)
            
        else:
            print("No sites found. Please add a site to Google Search Console first.")


if __name__ == "__main__":
    asyncio.run(main())
