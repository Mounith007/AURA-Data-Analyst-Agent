# AURA AI Agent System - Technical Documentation

## Overview

AURA now includes a sophisticated multi-agent AI system with MCP (Model Context Protocol) servers, designed for enterprise-level database operations and analysis.

## Architecture

### Core Components

1. **MCP Servers** - Model Context Protocol servers providing standardized interfaces for AI agents
2. **AI Agents** - Intelligent agents that use tools to perform complex tasks
3. **Agent Tools** - Reusable tools for common operations
4. **Tiny Recursive Model** - Task decomposition pattern for complex problem solving

## MCP Server

### Database MCP Server

The Database MCP Server provides tools for database operations:

**Location**: `aurabackend/mcp_server/`

**Available Tools**:
- `test_database_connection` - Test database connectivity
- `list_database_connections` - List all available connections
- `get_database_connection_info` - Get detailed connection info
- `get_database_schema` - Introspect database schema
- `get_table_info` - Get detailed table information
- `execute_database_query` - Execute SQL queries

**API Endpoint**: `http://localhost:8007`

### Using the MCP Server

```python
# List available tools
GET http://localhost:8007/mcp/servers/database/tools

# Call a tool
POST http://localhost:8007/mcp/servers/database/call-tool
{
    "tool_name": "test_database_connection",
    "arguments": {
        "connection_id": "conn_123"
    }
}
```

## AI Agents

### Database Agent

The Database Agent is an intelligent agent specialized in database operations.

**Location**: `aurabackend/agents/database_agent.py`

**Capabilities**:
- Connection testing and validation
- Schema analysis and introspection
- Query execution and optimization
- Recommendations for database improvements
- Tiny recursive task decomposition

### Creating and Using Agents

```python
# Create a database agent
POST http://localhost:8007/agents
{
    "agent_type": "database"
}

# Execute a task
POST http://localhost:8007/agents/{agent_id}/tasks
{
    "task_type": "analyze_schema",
    "parameters": {
        "connection_id": "conn_123",
        "deep_analysis": true
    }
}

# Get agent info
GET http://localhost:8007/agents/{agent_id}

# List all agents
GET http://localhost:8007/agents
```

## Agent Tools

### Tool Framework

The tool framework provides reusable components for agents.

**Location**: `aurabackend/agent_tools/`

**Available Tools**:
1. **DatabaseQueryTool** - Execute database queries
2. **SchemaIntrospectionTool** - Analyze database schemas
3. **ConnectionTestTool** - Test database connections

### Creating Custom Tools

```python
from agent_tools.base_tool import AgentTool, ToolExecutionResult

class MyCustomTool(AgentTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="My custom tool description"
        )
    
    def get_schema(self):
        return {
            "type": "object",
            "properties": {
                "param1": {"type": "string"}
            }
        }
    
    async def execute(self, **kwargs):
        # Your tool logic here
        return ToolExecutionResult(
            success=True,
            data={"result": "success"}
        )
```

## Tiny Recursive Model

The tiny recursive model enables agents to break down complex tasks into smaller subtasks.

### How It Works

1. **Task Submission** - Agent receives a complex task
2. **Decomposition Check** - Agent determines if task should be decomposed
3. **Recursive Breakdown** - Task is broken into subtasks (up to max depth)
4. **Execution** - Subtasks are executed in order
5. **Aggregation** - Results are combined and returned

### Example

```python
# Complex task: Validate a database connection
# This gets decomposed into:
# 1. Basic connection test
# 2. Schema introspection
# 3. Test query execution

result = await agent.run_task(
    task_type="validate_connection",
    connection_id="conn_123",
    deep_analysis=True
)
```

## Configuration

Configuration is managed in `aurabackend/config/agent_config.py`:

```python
# Recursive model settings
RECURSIVE_MODEL = {
    "max_depth": 3,
    "enable_caching": True,
    "decomposition_threshold": 3
}

# Scalability settings
SCALABILITY = {
    "max_agents_per_type": 10,
    "enable_auto_scaling": False,
    "agent_pool_size": 5
}
```

## Scalability

The system is designed for enterprise scalability:

1. **Agent Registry** - Centralized agent management
2. **Tool Registry** - Reusable tool sharing across agents
3. **Agent Pool** - Multiple agents of the same type
4. **Inter-Agent Communication** - Agents can communicate via messages

### Adding New Agent Types

```python
# 1. Create new agent class
class MyNewAgent(BaseAgent):
    async def initialize(self):
        # Setup code
        pass
    
    async def execute_task(self, task):
        # Task execution logic
        pass

# 2. Register agent type in config
AGENT_TYPES["my_new_agent"] = {
    "class": "MyNewAgent",
    "module": "agents.my_new_agent",
    "capabilities": ["capability1", "capability2"]
}

# 3. Agents are now available via API
POST /agents {"agent_type": "my_new_agent"}
```

## API Reference

### MCP Server Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mcp/servers` | GET | List all MCP servers |
| `/mcp/servers/{name}/tools` | GET | List server tools |
| `/mcp/servers/{name}/call-tool` | POST | Call a server tool |

### Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/agents` | GET | List all agents |
| `/agents` | POST | Create new agent |
| `/agents/{id}` | GET | Get agent info |
| `/agents/{id}/tasks` | POST | Execute task |
| `/agents/{id}/tasks` | GET | Get task history |
| `/agents/types` | GET | List agent types |

## Running the System

### Start MCP Server

```bash
cd aurabackend/mcp_server
python main.py
# Server starts on http://localhost:8007
```

### Start All Services

```bash
# Start API Gateway (port 8000)
cd aurabackend/api_gateway
python main.py

# Start Database Service (port 8002)
cd aurabackend/database
python main.py

# Start MCP Server (port 8007)
cd aurabackend/mcp_server
python main.py
```

### Docker Deployment

The MCP server will be automatically included in Docker deployment:

```bash
docker-compose up -d
```

## Examples

### Complete Workflow Example

```python
import httpx

# 1. Create a database agent
async with httpx.AsyncClient() as client:
    response = await client.post("http://localhost:8007/agents", json={
        "agent_type": "database"
    })
    agent_id = response.json()["agent"]["agent_id"]
    
    # 2. Test a database connection
    response = await client.post(
        f"http://localhost:8007/agents/{agent_id}/tasks",
        json={
            "task_type": "test_connection",
            "parameters": {"connection_id": "conn_123"}
        }
    )
    print(response.json())
    
    # 3. Analyze the schema
    response = await client.post(
        f"http://localhost:8007/agents/{agent_id}/tasks",
        json={
            "task_type": "analyze_schema",
            "parameters": {
                "connection_id": "conn_123",
                "refresh": True
            }
        }
    )
    print(response.json())
```

## Future Extensions

The architecture supports easy addition of:

1. **New Agent Types** - Analysis agents, optimization agents, security agents
2. **New Tools** - Query optimization, performance monitoring, security scanning
3. **New MCP Servers** - File operations, API integrations, ML model serving
4. **Advanced Features** - Agent collaboration, learning from feedback, automated optimization

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes parent directories
2. **Port Conflicts**: Check if ports 8000, 8002, 8003 are available
3. **Agent Not Found**: Verify agent was created successfully
4. **Tool Execution Fails**: Check tool parameters match schema

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When adding new features:

1. Follow the existing patterns (BaseAgent, AgentTool, MCPServer)
2. Add comprehensive documentation
3. Include usage examples
4. Update configuration files
5. Ensure backward compatibility

## License

MIT License - See LICENSE file for details
