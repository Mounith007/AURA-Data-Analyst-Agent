# AURA MCP Server & Database Agent

## Overview

The AURA MCP (Model Context Protocol) Server provides a centralized infrastructure for multi-agent communication and tool orchestration in the AURA Data Analyst platform. It enables AI agents to discover, register, and execute tools in a standardized way.

## Architecture

### Components

1. **MCP Server** - Central server for agent communication and tool management
2. **Database Connection Agent** - AI-powered agent for database operations
3. **Tool Registry** - Registry of available tools for agents
4. **Agent Registry** - Registry of available AI agents

### Services

- **MCP Server**: Port 8003 - `http://localhost:8003`
- **Database Agent**: Port 8004 - `http://localhost:8004`
- **Database Service**: Port 8002 - `http://localhost:8002`
- **API Gateway**: Port 8000 - `http://localhost:8000`

## Database Connection Agent

The Database Connection Agent is an AI-powered agent specialized in database connectivity and management. It uses **Google Gemini 1.5 Flash** (fast, lightweight model) for efficient AI-powered insights and recommendations.

### Features

- **Multi-Database Support**: Connect to 12+ database types
  - SQL: PostgreSQL, MySQL, SQLite, MSSQL, Oracle
  - NoSQL: MongoDB, Cassandra
  - Cloud: Snowflake, BigQuery, Redshift, Databricks, ClickHouse

- **AI-Powered Insights**: 
  - Connection recommendations
  - Security considerations
  - Performance optimization tips
  - Schema analysis
  - Query optimization suggestions

- **Capabilities**:
  - Connect to databases
  - Manage connections
  - Retrieve database schemas
  - Execute queries
  - Validate connections
  - Suggest optimizations

### API Endpoints

#### Agent Info
```bash
GET /agent/info
```

Response:
```json
{
  "agent_id": "db-agent-001",
  "name": "Database Connection Agent",
  "model": "gemini-1.5-flash",
  "capabilities": ["connect_to_databases", "manage_connections", ...],
  "supported_databases": ["postgresql", "mysql", ...]
}
```

#### Connect to Database
```bash
POST /connect
```

Request:
```json
{
  "name": "My PostgreSQL DB",
  "db_type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "database": "mydb",
  "username": "user",
  "password": "pass",
  "ssl_enabled": false
}
```

Response:
```json
{
  "status": "success",
  "connection_id": "uuid",
  "message": "Successfully connected to My PostgreSQL DB",
  "insights": [
    "Consider enabling SSL for production environments",
    "PostgreSQL 15+ offers improved query performance",
    ...
  ],
  "agent_id": "db-agent-001"
}
```

#### List Connections
```bash
GET /connections
```

#### Get Connection Info
```bash
GET /connections/{connection_id}
```

#### Test Connection
```bash
POST /connections/{connection_id}/test
```

#### Get Database Schema with AI Insights
```bash
GET /connections/{connection_id}/schema?refresh=false
```

Response includes AI-powered insights about the schema:
```json
{
  "status": "success",
  "connection_id": "uuid",
  "schemas": ["public", "analytics"],
  "tables": [...],
  "insights": [
    "Well-organized schema with clear separation of concerns",
    "Consider adding indexes on frequently queried columns",
    ...
  ]
}
```

#### Execute Query
```bash
POST /query
```

Request:
```json
{
  "connection_id": "uuid",
  "query": "SELECT * FROM users LIMIT 10",
  "limit": 1000
}
```

#### Optimize Query (AI-Powered)
```bash
POST /query/optimize
```

Request:
```json
{
  "connection_id": "uuid",
  "query": "SELECT * FROM users WHERE email LIKE '%@example.com'"
}
```

Response includes AI analysis and optimization suggestions:
```json
{
  "status": "success",
  "query": "...",
  "analysis": "Performance Analysis:\n1. Full table scan detected\n2. Recommend adding index on email column\n3. Consider using email prefix search for better performance...",
  "agent_id": "db-agent-001"
}
```

## MCP Server

The MCP Server provides a unified interface for tool management and agent orchestration.

### API Endpoints

#### Health Check
```bash
GET /health
```

#### List Tools
```bash
GET /tools
```

Returns all registered tools available for agents:
```json
{
  "tools": [
    {
      "name": "connect_database",
      "description": "Connect to a database",
      "category": "database",
      "parameters": {...},
      "returns": {...}
    },
    ...
  ],
  "count": 10
}
```

#### Get Tool Details
```bash
GET /tools/{tool_name}
```

#### Execute Tool
```bash
POST /tools/execute
```

Request:
```json
{
  "tool_name": "connect_database",
  "parameters": {
    "connection_id": "uuid"
  },
  "agent_id": "db-agent-001"
}
```

#### List Agents
```bash
GET /agents
```

Returns all registered agents:
```json
{
  "agents": [
    {
      "id": "db-agent-001",
      "name": "Database Connection Agent",
      "type": "database",
      "description": "Specialized agent for database connections",
      "capabilities": [...],
      "model": "gemini-1.5-flash"
    },
    ...
  ],
  "count": 5
}
```

#### Get Agent Details
```bash
GET /agents/{agent_id}
```

#### Execute Agent Task
```bash
POST /agents/execute
```

Request:
```json
{
  "agent_type": "database",
  "task": "Connect to PostgreSQL database at localhost",
  "context": {...},
  "tools_allowed": ["connect_database", "test_connection"]
}
```

## Tool Registry

The Tool Registry manages all tools available for agents to use.

### Default Tools

1. **Database Tools**:
   - `connect_database` - Connect to a database
   - `list_database_connections` - List all connections
   - `query_database` - Execute SQL query
   - `get_database_schema` - Get database schema

2. **Analysis Tools**:
   - `analyze_data` - Analyze data and provide insights

3. **Code Generation Tools**:
   - `generate_sql` - Generate SQL from natural language

### Adding Custom Tools

```python
from mcp_server.tool_registry import Tool, tool_registry

async def custom_handler(parameters):
    # Tool implementation
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

## Agent Registry

The Agent Registry manages all AI agents in the system.

### Default Agents

1. **Database Connection Agent** (`db-agent-001`)
   - Model: gemini-1.5-flash (fast, lightweight model)
   - Specialization: Database connectivity

2. **SQL Generator Agent** (`gen-agent-001`)
   - Model: gemini-pro
   - Specialization: SQL query generation

3. **SQL Critic Agent** (`critic-agent-001`)
   - Model: gemini-pro
   - Specialization: SQL validation

4. **Data Analyst Agent** (`analyst-agent-001`)
   - Model: gemini-1.5-flash (fast, lightweight model)
   - Specialization: Data analysis

5. **Orchestrator Agent** (`orch-agent-001`)
   - Model: gemini-pro
   - Specialization: Multi-agent coordination

## Starting the Services

### Development Mode

Start all services:
```bash
cd aurabackend
./start_all_services.sh
```

Stop all services:
```bash
cd aurabackend
./stop_services.sh
```

### Start Individual Services

```bash
# MCP Server
cd aurabackend/mcp_server
python main.py

# Database Agent
cd aurabackend/agents
python main.py
```

## Environment Variables

Create a `.env` file in the `aurabackend` directory:

```env
# AI Model Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Service Ports
API_GATEWAY_PORT=8000
DATABASE_SERVICE_PORT=8002
MCP_SERVER_PORT=8003
DATABASE_AGENT_PORT=8004

# API Configuration
API_HOST=0.0.0.0
DEBUG=true

# CORS Origins
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:3000
```

## Scalability

The architecture is designed for scalability:

1. **Agent Registration**: New agents can be registered dynamically
2. **Tool Registry**: Custom tools can be added at runtime
3. **Model Flexibility**: Supports multiple AI models (Gemini Flash, Pro, etc.)
4. **Microservices**: Each component is independently scalable
5. **MCP Protocol**: Standard protocol for agent communication

### Adding New Agents

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

## Testing

### Health Checks

```bash
# Test all services
curl http://localhost:8003/health  # MCP Server
curl http://localhost:8004/health  # Database Agent
curl http://localhost:8002/health  # Database Service
curl http://localhost:8000/health  # API Gateway
```

### Example Workflow

1. **List Available Agents**:
```bash
curl http://localhost:8003/agents
```

2. **Connect to Database**:
```bash
curl -X POST http://localhost:8004/connect \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test DB",
    "db_type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "database": "testdb",
    "username": "user",
    "password": "pass"
  }'
```

3. **Get Schema with AI Insights**:
```bash
curl http://localhost:8004/connections/{connection_id}/schema
```

4. **Optimize Query**:
```bash
curl -X POST http://localhost:8004/query/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": "uuid",
    "query": "SELECT * FROM users WHERE email LIKE '%@%'"
  }'
```

## Performance

- **Gemini 1.5 Flash**: Fast response times (~1-2s) for AI insights
- **Connection Pooling**: Efficient database connection management
- **Schema Caching**: Reduced database overhead
- **Async Operations**: Non-blocking I/O for better throughput

## Security Considerations

1. **Credentials**: Store sensitive credentials securely (use environment variables or secrets manager)
2. **SSL**: Enable SSL for production database connections
3. **Query Validation**: Agents validate queries before execution
4. **Access Control**: Implement authentication/authorization for production use
5. **API Rate Limiting**: Add rate limiting for production deployments

## Troubleshooting

### Common Issues

1. **"Gemini API not configured"**
   - Solution: Set `GEMINI_API_KEY` in `.env` file

2. **"Database manager not available"**
   - Solution: Ensure database service is running on port 8002

3. **Connection timeouts**
   - Solution: Check database credentials and network connectivity

4. **Port conflicts**
   - Solution: Update port numbers in `.env` file

## Future Enhancements

- [ ] Support for more AI models (Claude, GPT-4, etc.)
- [ ] Advanced agent orchestration patterns
- [ ] Real-time agent collaboration
- [ ] Agent learning and adaptation
- [ ] Enhanced security features
- [ ] Distributed agent execution
- [ ] Agent performance monitoring
- [ ] Custom agent templates

## Support

For issues or questions:
- Check the main README.md
- Review API documentation at `/docs` endpoints
- Check service health at `/health` endpoints
