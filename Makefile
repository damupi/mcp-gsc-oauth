.PHONY: help build up down restart logs clean test

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Google Search Console MCP Server - Docker Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

build: ## Build the Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Build complete$(NC)"

up: ## Start the MCP server
	@echo "$(BLUE)Starting MCP server...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)Warning: .env file not found. Creating from .env.example...$(NC)"; \
		cp .env.example .env; \
		echo "$(YELLOW)Please edit .env with your Google OAuth credentials before running again.$(NC)"; \
		exit 1; \
	fi
	docker-compose up -d
	@echo "$(GREEN)✓ MCP server is running at http://localhost:8000$(NC)"
	@echo "$(BLUE)Run 'make logs' to view logs$(NC)"

down: ## Stop the MCP server
	@echo "$(BLUE)Stopping MCP server...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ MCP server stopped$(NC)"

restart: ## Restart the MCP server
	@echo "$(BLUE)Restarting MCP server...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✓ MCP server restarted$(NC)"

logs: ## View server logs (follow mode)
	@echo "$(BLUE)Viewing logs (Ctrl+C to exit)...$(NC)"
	docker-compose logs -f

logs-tail: ## View last 100 lines of logs
	@echo "$(BLUE)Last 100 log lines:$(NC)"
	docker-compose logs --tail=100

status: ## Check server status
	@echo "$(BLUE)Server status:$(NC)"
	@docker-compose ps

clean: ## Remove containers, images, and volumes
	@echo "$(BLUE)Cleaning up Docker resources...$(NC)"
	docker-compose down -v --rmi all
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

shell: ## Open a shell in the running container
	@echo "$(BLUE)Opening shell in container...$(NC)"
	docker-compose exec mcp-gsc /bin/bash

test: ## Test the MCP server endpoint
	@echo "$(BLUE)Testing MCP server...$(NC)"
	@curl -f http://localhost:8000/health && echo "$(GREEN)✓ Server is healthy$(NC)" || echo "$(YELLOW)Server is not responding$(NC)"

rebuild: down build up ## Rebuild and restart the server

dev: ## Run in development mode with live logs
	@echo "$(BLUE)Starting in development mode...$(NC)"
	docker-compose up
