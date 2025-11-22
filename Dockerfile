# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install dependencies using uv
RUN uv pip install --system -e .

# Expose port for HTTP transport
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
# Set PYTHONPATH so Python can find the mcp_gsc package
ENV PYTHONPATH=/app/src

# Run the MCP server with HTTP transport
CMD ["fastmcp", "run", "src/mcp_gsc/server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
