# AURA Developer Quick Reference

## Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│                   http://localhost:5173                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   API Gateway (FastAPI)                      │
│                   http://localhost:8000                      │
└─────────────────────────────────────────────────────────────┘
            │                 │                  │
            ▼                 ▼                  ▼
┌──────────────────┐  ┌──────────────┐  ┌─────────────────┐
│ Database Service │  │  MCP Server  │  │ Database Agent  │
│   Port 8002      │  │  Port 8003   │  │   Port 8004     │
└──────────────────┘  └──────────────┘  └─────────────────┘
            │                 │                  │
            └─────────────────┴──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Tool Registry   │
                    │  Agent Registry  │
                    └──────────────────┘
```

## Starting Services

### All Services
```bash
cd aurabackend
./start_all_services.sh
```

### Individual Services
```bash
# API Gateway
cd aurabackend/api_gateway
python main.py

# Database Service
cd aurabackend/database
python main.py

# MCP Server
cd aurabackend/mcp_server
python main.py

# Database Agent
cd aurabackend/agents
python main.py
```

### Stop All Services
```bash
cd aurabackend
./stop_services.sh
```

## Environment Configuration

Create `.env` in `aurabackend/`:

```env
# AI Model
GEMINI_API_KEY=your_api_key_here

# Service Ports
API_GATEWAY_PORT=8000
DATABASE_SERVICE_PORT=8002
MCP_SERVER_PORT=8003
DATABASE_AGENT_PORT=8004

# API Configuration
API_HOST=0.0.0.0
DEBUG=true

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:3000
```

## Quick API Reference

### MCP Server (Port 8003)

```bash
# Health check
GET /health

# List all tools
GET /tools

# Get tool details
GET /tools/{tool_name}

# Execute tool
POST /tools/execute
{
  "tool_name": "connect_database",
  "parameters": {...},
  "agent_id": "db-agent-001"
}

# List all agents
GET /agents

# Get agent details
GET /agents/{agent_id}

# Execute agent task
POST /agents/execute
{
  "agent_type": "database",
  "task": "Connect to database",
  "context": {...}
}
```

### Database Agent (Port 8004)

```bash
# Agent info
GET /agent/info

# Connect to database
POST /connect
{
  "name": "My Database",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "database": "mydb",
  "username": "user",
  "password": "pass"
}

# List connections
GET /connections

# Get connection info
GET /connections/{connection_id}

# Test connection
POST /connections/{connection_id}/test

# Get schema with AI insights
GET /connections/{connection_id}/schema?refresh=false

# Execute query
POST /query
{
  "connection_id": "uuid",
  "query": "SELECT * FROM users",
  "limit": 1000
}

# Optimize query (AI-powered)
POST /query/optimize
{
  "connection_id": "uuid",
  "query": "SELECT * FROM users WHERE email LIKE '%@%'"
}
```

### Database Service (Port 8002)

```bash
# Health check
GET /health

# Supported databases
GET /supported-databases

# Create connection
POST /connections
{...}

# List connections
GET /connections

# Get connection
GET /connections/{connection_id}

# Test connection
POST /connections/{connection_id}/test

# Get schema
GET /connections/{connection_id}/schema

# Execute query
POST /connections/{connection_id}/query
```

## Agent Types

| Agent Type | ID | Model | Purpose |
|-----------|-----|-------|---------|
| Database | db-agent-001 | gemini-1.5-flash | Database operations |
| Generator | gen-agent-001 | gemini-pro | SQL generation |
| Critic | critic-agent-001 | gemini-pro | SQL validation |
| Analyst | analyst-agent-001 | gemini-1.5-flash | Data analysis |
| Orchestrator | orch-agent-001 | gemini-pro | Multi-agent coordination |

## Available Tools

| Tool Name | Category | Description |
|-----------|----------|-------------|
| connect_database | database | Connect to a database |
| list_database_connections | database | List all connections |
| query_database | database | Execute SQL query |
| get_database_schema | database | Get database schema |
| analyze_data | analysis | Analyze data |
| generate_sql | code_generation | Generate SQL from NL |

## Supported Databases

### SQL Databases
- PostgreSQL (port 5432)
- MySQL (port 3306)
- SQLite (file-based)
- MSSQL (port 1433)
- Oracle (port 1521)

### NoSQL Databases
- MongoDB (port 27017)
- Cassandra (port 9042)

### Cloud Data Warehouses
- Snowflake (port 443)
- BigQuery (port 443)
- Redshift (port 5439)
- Databricks (port 443)
- ClickHouse (port 8123)

## Testing

### Integration Test
```bash
cd aurabackend
python3 test_integration.py
```

### Health Checks
```bash
# Check all services
curl http://localhost:8000/health  # API Gateway
curl http://localhost:8002/health  # Database Service
curl http://localhost:8003/health  # MCP Server
curl http://localhost:8004/health  # Database Agent
```

### Manual Testing
```bash
# List available agents
curl http://localhost:8003/agents | jq

# Get Database Agent info
curl http://localhost:8004/agent/info | jq

# List available tools
curl http://localhost:8003/tools | jq

# Get tool details
curl http://localhost:8003/tools/connect_database | jq
```

## Adding Custom Agents

```python
from mcp_server.agent_registry import AgentDefinition, AgentType, agent_registry

new_agent = AgentDefinition(
    id="custom-agent-001",
    name="Custom Agent",
    type=AgentType.CUSTOM,
    description="My custom agent",
    model="gemini-1.5-flash",
    capabilities=["custom_capability"],
    tools_available=["custom_tool"],
    metadata={}
)

agent_registry.register_agent(new_agent)
```

## Adding Custom Tools

```python
from mcp_server.tool_registry import Tool, tool_registry

async def custom_handler(parameters):
    # Implement tool logic
    return {"result": "success"}

tool = Tool(
    name="custom_tool",
    description="My custom tool",
    category="custom",
    parameters={
        "param1": {"type": "string", "required": True}
    },
    returns={"type": "object"},
    handler=custom_handler
)

tool_registry.register_tool(tool)
```

## Common Issues

### Port Already in Use
```bash
# Find and kill process using port
lsof -ti:8003 | xargs kill -9
```

### Module Not Found
```bash
cd aurabackend
pip install -r requirements.txt
```

### API Key Not Configured
```bash
# Add to .env file
echo "GEMINI_API_KEY=your_key" >> aurabackend/.env
```

## Performance Tips

1. **Use Gemini Flash** for fast operations (Database Agent, Data Analyst)
2. **Enable schema caching** to reduce database overhead
3. **Use connection pooling** for better performance
4. **Set appropriate query limits** to avoid large result sets

## Security Checklist

- [ ] Set `GEMINI_API_KEY` via environment variables
- [ ] Enable SSL for production database connections
- [ ] Implement authentication for API endpoints
- [ ] Use secrets manager for sensitive credentials
- [ ] Enable CORS only for trusted origins
- [ ] Add rate limiting for production
- [ ] Validate all SQL queries before execution

## Documentation

- [Main README](../README.md)
- [MCP & Database Agent Guide](MCP_DATABASE_AGENT.md)
- [Quick Start Guide](../QUICKSTART.md)
- [Team Setup](../README-TEAM.md)

## Support

For issues:
1. Check service health: `/health` endpoints
2. Review logs in service output
3. Verify environment variables
4. Check port availability
5. Consult documentation

## Useful Commands

```bash
# View service logs (if using Docker)
docker logs aura-api-gateway
docker logs aura-database

# Check Python packages
pip list | grep -E "fastapi|google-generativeai"

# Test endpoint with curl
curl -X POST http://localhost:8004/connect \
  -H "Content-Type: application/json" \
  -d @test_connection.json

# Format JSON output
curl http://localhost:8003/agents | python -m json.tool

# Watch logs in real-time
tail -f /tmp/aura_*.log
```
