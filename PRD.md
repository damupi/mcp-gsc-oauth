# Product Requirements Document: Google Search Console MCP Server

## 1. Overview

### 1.1 Product Description
A Model Context Protocol (MCP) server built with FastMCP that provides LLMs with programmatic access to Google Search Console (GSC) data and functionality. This server enables AI assistants to query search analytics, manage sitemaps, inspect URLs, and manage site properties through a standardized MCP interface.

### 1.2 Purpose
Enable LLMs and AI assistants to help users with SEO tasks, search performance analysis, and site management by providing direct access to Google Search Console API capabilities through the MCP protocol.

### 1.3 Target Users
- SEO professionals using AI assistants for data analysis
- Web developers integrating search analytics into AI workflows
- Content creators analyzing search performance with AI tools
- Digital marketers automating SEO reporting and insights

## 2. Technical Stack

### 2.1 Core Technologies
- **Framework**: FastMCP v2.x (Python)
- **API**: Google Search Console API (Webmaster Tools API v3)
- **Authentication**: Google OAuth 2.0
- **Python Version**: 3.10+

### 2.2 Dependencies
- `fastmcp` - MCP server framework
- `google-auth` - Google authentication
- `google-auth-oauthlib` - OAuth flow handling
- `google-auth-httplib2` - HTTP transport
- `google-api-python-client` - Google API client library

## 3. Functional Requirements

### 3.1 MCP Tools (Actions)

#### 3.1.1 Search Analytics Tools
**Tool: `query_search_analytics`**
- **Purpose**: Query search traffic data with filters and parameters
- **Parameters**:
  - `site_url` (str, required): The site URL (e.g., "https://example.com/")
  - `start_date` (str, required): Start date in YYYY-MM-DD format
  - `end_date` (str, required): End date in YYYY-MM-DD format
  - `dimensions` (list[str], optional): Dimensions to group by (query, page, country, device, searchAppearance, date)
  - `filters` (list[dict], optional): Filters to apply (dimension, operator, expression)
  - `row_limit` (int, optional): Maximum rows to return (default: 1000, max: 25000)
  - `start_row` (int, optional): Zero-based index of first row to return
  - `aggregation_type` (str, optional): How to aggregate data (auto, byProperty, byPage)
- **Returns**: Search analytics data with clicks, impressions, CTR, and position metrics
- **Use Cases**: 
  - Analyze top performing queries
  - Compare device performance
  - Track country-specific search trends
  - Monitor page-level search metrics

#### 3.1.2 Sitemap Management Tools

**Tool: `list_sitemaps`**
- **Purpose**: List all sitemaps for a site
- **Parameters**:
  - `site_url` (str, required): The site URL
- **Returns**: List of sitemaps with submission status and error information

**Tool: `get_sitemap`**
- **Purpose**: Get information about a specific sitemap
- **Parameters**:
  - `site_url` (str, required): The site URL
  - `feedpath` (str, required): The sitemap URL
- **Returns**: Sitemap details including submission date, errors, and warnings

**Tool: `submit_sitemap`**
- **Purpose**: Submit a sitemap to Google
- **Parameters**:
  - `site_url` (str, required): The site URL
  - `feedpath` (str, required): The sitemap URL to submit
- **Returns**: Confirmation of submission

**Tool: `delete_sitemap`**
- **Purpose**: Delete a sitemap from Google Search Console
- **Parameters**:
  - `site_url` (str, required): The site URL
  - `feedpath` (str, required): The sitemap URL to delete
- **Returns**: Confirmation of deletion

#### 3.1.3 Site Management Tools

**Tool: `list_sites`**
- **Purpose**: List all sites in the user's Search Console account
- **Parameters**: None
- **Returns**: List of sites with permission levels

**Tool: `get_site`**
- **Purpose**: Get information about a specific site
- **Parameters**:
  - `site_url` (str, required): The site URL
- **Returns**: Site details and permission level

**Tool: `add_site`**
- **Purpose**: Add a site to Search Console account
- **Parameters**:
  - `site_url` (str, required): The site URL to add
- **Returns**: Confirmation of site addition

**Tool: `delete_site`**
- **Purpose**: Remove a site from Search Console account
- **Parameters**:
  - `site_url` (str, required): The site URL to remove
- **Returns**: Confirmation of site removal

#### 3.1.4 URL Inspection Tools

**Tool: `inspect_url`**
- **Purpose**: Inspect the Google index status of a specific URL
- **Parameters**:
  - `inspection_url` (str, required): The URL to inspect
  - `site_url` (str, required): The site URL that owns the inspection URL
  - `language_code` (str, optional): Language code (default: "en-US")
- **Returns**: Detailed index status including:
  - Coverage state (indexed, not indexed, etc.)
  - Indexing issues
  - Mobile usability
  - Rich results
  - AMP status
  - Crawl information

### 3.2 MCP Resources (Data Access)

#### 3.2.1 Static Resources

**Resource: `gsc://sites`**
- **Purpose**: List all available sites
- **Returns**: JSON array of site URLs and permission levels

**Resource: `gsc://config`**
- **Purpose**: Server configuration and status
- **Returns**: Server version, authentication status, API quota information

#### 3.2.2 Dynamic Resource Templates

**Resource: `gsc://sites/{site_url}/analytics/summary`**
- **Purpose**: Get a summary of recent search analytics for a site
- **Parameters**:
  - `site_url` (str): The site URL (URL-encoded)
- **Returns**: Last 28 days summary with total clicks, impressions, CTR, position

**Resource: `gsc://sites/{site_url}/sitemaps`**
- **Purpose**: Get all sitemaps for a specific site
- **Parameters**:
  - `site_url` (str): The site URL (URL-encoded)
- **Returns**: List of sitemaps with status

**Resource: `gsc://sites/{site_url}/top-queries`**
- **Purpose**: Get top performing queries for a site
- **Parameters**:
  - `site_url` (str): The site URL (URL-encoded)
- **Returns**: Top 10 queries by clicks from last 7 days

**Resource: `gsc://sites/{site_url}/top-pages`**
- **Purpose**: Get top performing pages for a site
- **Parameters**:
  - `site_url` (str): The site URL (URL-encoded)
- **Returns**: Top 10 pages by clicks from last 7 days

### 3.3 MCP Prompts

**Prompt: `analyze_search_performance`**
- **Purpose**: Generate a prompt for analyzing search performance
- **Parameters**:
  - `site_url` (str): The site to analyze
  - `time_period` (str): Time period (e.g., "last 30 days")
- **Returns**: Structured prompt asking LLM to analyze search data

**Prompt: `seo_recommendations`**
- **Purpose**: Generate a prompt for SEO recommendations
- **Parameters**:
  - `site_url` (str): The site to analyze
  - `focus_area` (str, optional): Specific area to focus on (queries, pages, technical)
- **Returns**: Prompt for generating SEO recommendations

**Prompt: `compare_periods`**
- **Purpose**: Generate a prompt for comparing two time periods
- **Parameters**:
  - `site_url` (str): The site to analyze
  - `period1_start` (str): First period start date
  - `period1_end` (str): First period end date
  - `period2_start` (str): Second period start date
  - `period2_end` (str): Second period end date
- **Returns**: Prompt for period-over-period comparison

## 4. Authentication & Authorization

### 4.1 OAuth 2.0 Flow
- Use Google OAuth 2.0 for user authentication
- Required scopes:
  - `https://www.googleapis.com/auth/webmasters` (full access)
  - `https://www.googleapis.com/auth/webmasters.readonly` (read-only option)

### 4.2 Credential Management
- Support multiple authentication methods:
  - Service account credentials (for automated workflows)
  - OAuth 2.0 user credentials (for individual users)
  - Application default credentials
- Store credentials securely using FastMCP's authentication features
- Support credential refresh automatically

### 4.3 Configuration
- Accept credentials via:
  - Environment variables (`GOOGLE_APPLICATION_CREDENTIALS`)
  - Configuration file path
  - Interactive OAuth flow (for development)

## 5. Error Handling

### 5.1 API Error Handling
- Handle Google API errors gracefully:
  - Rate limiting (quota exceeded)
  - Authentication errors
  - Permission denied
  - Invalid parameters
  - Resource not found
- Return user-friendly error messages through MCP context logging

### 5.2 Data Validation
- Validate date formats (YYYY-MM-DD)
- Validate site URLs (proper format and encoding)
- Validate dimension and filter parameters
- Check row limits and constraints

### 5.3 Logging
- Use FastMCP Context for logging:
  - `ctx.info()` for informational messages
  - `ctx.warning()` for warnings
  - `ctx.error()` for errors
- Log API calls and responses for debugging

## 6. Performance & Optimization

### 6.1 Caching
- Implement caching for frequently accessed data:
  - Site list (cache for 5 minutes)
  - Sitemap status (cache for 1 hour)
  - Search analytics summaries (cache for 1 hour)
- Use in-memory caching with TTL

### 6.2 Rate Limiting
- Respect Google Search Console API quotas:
  - 1,200 queries per minute per project
  - Handle rate limit errors with exponential backoff
- Implement client-side rate limiting to prevent quota exhaustion

### 6.3 Pagination
- Support pagination for large result sets
- Use `start_row` and `row_limit` parameters effectively
- Provide guidance on optimal pagination strategies

## 7. Data Privacy & Security

### 7.1 Data Handling
- Do not store user search data permanently
- Only cache data temporarily for performance
- Clear sensitive data from logs

### 7.2 Credential Security
- Never log or expose credentials
- Use secure credential storage mechanisms
- Support credential rotation

### 7.3 Compliance
- Follow Google API Terms of Service
- Respect user data privacy
- Implement proper data retention policies

## 8. Testing Requirements

### 8.1 Unit Tests
- Test all tools with mock Google API responses
- Test authentication flows
- Test error handling scenarios
- Test data validation

### 8.2 Integration Tests
- Test against Google Search Console API sandbox (if available)
- Test with real credentials in development environment
- Verify all API endpoints work correctly

### 8.3 MCP Protocol Tests
- Verify MCP tool schemas are correct
- Test resource URI templates
- Validate prompt generation
- Test context usage (logging, sampling)

## 9. Documentation Requirements

### 9.1 User Documentation
- README with installation instructions
- Authentication setup guide
- Usage examples for each tool
- Common use cases and workflows
- Troubleshooting guide

### 9.2 Developer Documentation
- Code documentation (docstrings)
- Architecture overview
- API mapping documentation
- Contributing guidelines

### 9.3 Examples
- Example: Analyze top queries for a site
- Example: Compare search performance month-over-month
- Example: Monitor indexing status for new pages
- Example: Automated sitemap submission workflow

## 10. Deployment & Distribution

### 10.1 Package Distribution
- Publish to PyPI as `fastmcp-gsc` or `mcp-google-search-console`
- Include all dependencies in `pyproject.toml` or `setup.py`
- Support Python 3.10+

### 10.2 Configuration
- Provide example configuration files
- Support environment variable configuration
- Document all configuration options

### 10.3 Running the Server
- Support running via `fastmcp run` command
- Provide systemd service example
- Docker container support (optional)

## 11. Future Enhancements (Out of Scope for v1)

### 11.1 Advanced Analytics
- Automated trend detection
- Anomaly detection in search metrics
- Predictive analytics for search performance

### 11.2 Reporting
- Automated report generation
- Custom dashboard data preparation
- Export to various formats (CSV, Excel, PDF)

### 11.3 Multi-Site Management
- Bulk operations across multiple sites
- Cross-site comparison tools
- Portfolio-level analytics

### 11.4 Integration Features
- Webhook support for real-time notifications
- Integration with other SEO tools
- Custom alert configurations

## 12. Success Metrics

### 12.1 Functionality
- All Google Search Console API endpoints covered
- 100% of core tools working correctly
- Proper error handling for all edge cases

### 12.2 Usability
- Clear, helpful error messages
- Comprehensive documentation
- Easy authentication setup
- Intuitive tool naming and parameters

### 12.3 Performance
- API calls complete within 5 seconds (95th percentile)
- Effective caching reduces redundant API calls by 50%+
- No rate limit errors under normal usage

### 12.4 Reliability
- 99%+ uptime for server availability
- Graceful degradation when API is unavailable
- Automatic credential refresh works reliably

## 13. Project Structure

```
mcp-gsc/
├── README.md
├── pyproject.toml
├── LICENSE
├── .gitignore
├── .env.example
├── src/
│   └── mcp_gsc/
│       ├── __init__.py
│       ├── server.py          # Main FastMCP server
│       ├── auth.py            # Authentication handling
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── analytics.py   # Search analytics tools
│       │   ├── sitemaps.py    # Sitemap management tools
│       │   ├── sites.py       # Site management tools
│       │   └── inspection.py  # URL inspection tools
│       ├── resources/
│       │   ├── __init__.py
│       │   └── gsc_resources.py
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── seo_prompts.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── cache.py       # Caching utilities
│       │   ├── validation.py  # Input validation
│       │   └── formatting.py  # Data formatting
│       └── config.py          # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_tools.py
│   ├── test_resources.py
│   ├── test_auth.py
│   └── fixtures/
│       └── mock_responses.py
├── examples/
│   ├── basic_usage.py
│   ├── analytics_report.py
│   └── sitemap_management.py
└── docs/
    ├── authentication.md
    ├── usage.md
    └── api_mapping.md
```

## 14. Acceptance Criteria

### 14.1 Minimum Viable Product (MVP)
- [ ] All search analytics tools implemented and working
- [ ] All sitemap management tools implemented and working
- [ ] All site management tools implemented and working
- [ ] URL inspection tool implemented and working
- [ ] OAuth 2.0 authentication working
- [ ] Basic error handling implemented
- [ ] Core resources implemented (sites list, analytics summary)
- [ ] README with setup and usage instructions
- [ ] Published to PyPI
- [ ] At least 3 working examples provided

### 14.2 Quality Standards
- [ ] All tools have proper docstrings
- [ ] Type hints used throughout codebase
- [ ] Unit tests cover >80% of code
- [ ] No hardcoded credentials in code
- [ ] All API errors handled gracefully
- [ ] Logging implemented for debugging
- [ ] Code follows PEP 8 style guidelines

### 14.3 User Experience
- [ ] Clear error messages for common issues
- [ ] Authentication setup documented clearly
- [ ] Tool parameters are intuitive and well-documented
- [ ] Examples cover common use cases
- [ ] Troubleshooting guide addresses common problems
