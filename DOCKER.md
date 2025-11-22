# Docker Deployment Guide

## Prerequisites

1. **Docker Desktop** must be installed and running
   - Download from: https://www.docker.com/products/docker-desktop
   - Make sure Docker daemon is running (check Docker Desktop app)

2. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Add your Google OAuth credentials

## Quick Start

```bash
# 1. Make sure Docker is running
docker --version

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Build and start
make build
make up

# 4. Check status
make status

# 5. View logs
make logs
```

## Available Commands

### Basic Operations
- `make build` - Build the Docker image
- `make up` - Start the server in background
- `make down` - Stop the server
- `make restart` - Restart the server

### Monitoring
- `make logs` - View logs (follow mode, Ctrl+C to exit)
- `make logs-tail` - View last 100 lines
- `make status` - Check if server is running

### Development
- `make dev` - Run with live logs (foreground)
- `make shell` - Open bash shell in container
- `make test` - Test server health endpoint

### Maintenance
- `make rebuild` - Rebuild and restart (after code changes)
- `make clean` - Remove all Docker resources

## Configuration

### Environment Variables

The server requires these environment variables in `.env`:

```bash
FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.google.GoogleProvider
FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
FASTMCP_SERVER_AUTH_GOOGLE_CLIENT_SECRET=GOCSPX-your-client-secret
FASTMCP_SERVER_AUTH_GOOGLE_BASE_URL=http://localhost:8000
FASTMCP_SERVER_AUTH_GOOGLE_REQUIRED_SCOPES=openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/webmasters
```

### Port Configuration

By default, the server runs on port 8000. To change:

1. Edit `docker-compose.yml`:
   ```yaml
   ports:
     - "8080:8000"  # External:Internal
   ```

2. Update `FASTMCP_SERVER_AUTH_GOOGLE_BASE_URL` in `.env`:
   ```bash
   FASTMCP_SERVER_AUTH_GOOGLE_BASE_URL=http://localhost:8080
   ```

## Testing the Server

### 1. Health Check
```bash
make test
# Or manually:
curl http://localhost:8000/health
```

### 2. Access MCP Endpoint
```bash
curl http://localhost:8000/mcp
```

### 3. Connect with Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-search-console": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Troubleshooting

### Docker Daemon Not Running

**Error**: `Cannot connect to the Docker daemon`

**Solution**: Start Docker Desktop application

### Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**: 
1. Stop the conflicting service
2. Or change the port in `docker-compose.yml`

### Container Keeps Restarting

**Solution**:
```bash
# Check logs for errors
make logs

# Common issues:
# - Missing or invalid .env file
# - Invalid Google OAuth credentials
# - Network connectivity issues
```

### Permission Errors

**Solution**:
```bash
# On Linux, you may need to run with sudo
sudo make build
sudo make up
```

## Production Deployment

### Security Considerations

1. **Never commit `.env` file** - It contains secrets
2. **Use environment-specific configs** - Different credentials for dev/prod
3. **Enable HTTPS** - Use a reverse proxy (nginx, Caddy) for SSL
4. **Restrict network access** - Use firewall rules

### Example with Reverse Proxy (nginx)

```nginx
server {
    listen 443 ssl;
    server_name mcp.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Scaling

For multiple instances:

```yaml
# docker-compose.yml
services:
  mcp-gsc:
    # ... existing config ...
    deploy:
      replicas: 3
```

## Monitoring

### View Resource Usage

```bash
docker stats mcp-gsc-server
```

### Persistent Logs

Logs are stored in Docker volumes. To export:

```bash
docker-compose logs > mcp-server.log
```

## Updating

After code changes:

```bash
# Rebuild and restart
make rebuild

# Or manually:
make down
make build
make up
```

## Cleanup

Remove all Docker resources:

```bash
make clean
```

This removes:
- Container
- Image
- Volumes
- Network
