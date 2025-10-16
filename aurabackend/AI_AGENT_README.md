# AI Agent Infrastructure - MCP Server & Tools

## Overview

This directory contains the enhanced AI Agent infrastructure for AURA, including:

1. **MCP Server** - Model Context Protocol server for agent coordination
2. **Agent Tools** - Reusable tools for AI agents
3. **Enhanced Database Agent** - AI agent with recursive reasoning

## Components

### MCP Server (`mcp_server/`)

The Model Context Protocol (MCP) server provides centralized context management and agent coordination.

**Features:**
- Context management for AI agents
- Database context tracking
- Conversation history management
- Protocol message routing
- Agent-to-agent communication

**Endpoints:**
- `POST /contexts` - Create new context
- `GET /contexts/{context_key}` - Retrieve context
- `PUT /contexts/{context_key}` - Update context
- `DELETE /contexts/{context_key}` - Delete context
- `POST /database-contexts` - Create database-specific context
- `POST /conversations` - Add conversation turn
- `POST /messages` - Send protocol message
- `GET /stats/contexts` - Get context statistics

**Running:**
```bash
cd aurabackend
uvicorn mcp_server.mcp_main:app --host 0.0.0.0 --port 8007
```

Access API docs at: `http://localhost:8007/docs`

### Agent Tools (`agent_tools/`)

Reusable tools that AI agents can use to perform operations.

#### 1. DatabaseTool
- Execute database queries
- Get schema information
- Test connections
- List available connections

#### 2. QueryValidator
- Validate SQL queries for security
- Detect SQL injection attempts
- Check for dangerous operations
- Suggest query improvements
- Sanitize queries

#### 3. SchemaAnalyzer
- Analyze database schemas
- Suggest indexes
- Find table relationships
- Calculate schema quality scores
- Provide optimization recommendations

#### 4. RecursiveReasoner
- Break complex problems into sub-problems
- Apply recursive reasoning (tiny recursive model)
- Generate reasoning trees
- Synthesize solutions from sub-problems
- Explain reasoning process

**Usage Example:**
```python
from agent_tools import DatabaseTool, QueryValidator, RecursiveReasoner

# Use database tool
db_tool = DatabaseTool(db_manager)
result = await db_tool.execute_query(
    connection_id="conn_123",
    query="SELECT * FROM users LIMIT 10"
)

# Validate query
validator = QueryValidator()
validation = validator.validate_query(
    query="SELECT * FROM users WHERE id = 1",
    allow_modifications=False
)

# Apply recursive reasoning
reasoner = RecursiveReasoner(max_depth=3)
reasoning = reasoner.reason(
    problem="Find top 10 customers by revenue and their order counts",
    context={"schema": schema_info}
)
```

### Enhanced Database Agent

The database agent combines all tools with recursive reasoning for intelligent database operations.

**Features:**
- Natural language to SQL conversion
- Recursive problem decomposition
- Automatic query validation
- Schema analysis and insights
- Query optimization suggestions
- Self-correcting query generation

**Usage Example:**
```python
from orchestration_service.agents.database_agent import DatabaseAgent

agent = DatabaseAgent(db_manager)

# Process user query
result = await agent.process_request(
    user_query="Show me the top 10 products by revenue",
    connection_id="conn_123",
    context={"additional": "context"}
)

# Analyze database
analysis = await agent.analyze_database(connection_id="conn_123")
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  MCP Server                      │
│  (Context Management & Agent Coordination)       │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼──────────┐
│ Database Agent │  │  Other Agents   │
│ (Enhanced)     │  │  (Future)       │
└───────┬────────┘  └─────────────────┘
        │
        │ Uses Tools:
        │
  ┌─────┴─────┬──────────┬──────────┬─────────────┐
  │           │          │          │             │
┌─▼──────┐ ┌─▼─────┐ ┌─▼────┐  ┌──▼────┐  ┌─────▼─────┐
│Database│ │Query  │ │Schema│  │Recur- │  │   More    │
│Tool    │ │Valid. │ │Analyz│  │sive   │  │  Tools    │
└────────┘ └───────┘ └──────┘  │Reason │  │  (Future) │
                                └───────┘  └───────────┘
```

## Recursive Reasoning

The recursive reasoner implements a "tiny recursive model" approach:

1. **Analyze** - Understand the problem
2. **Decompose** - Break into sub-problems
3. **Solve** - Solve each sub-problem recursively
4. **Verify** - Validate solutions
5. **Synthesize** - Combine into final solution

**Example Reasoning Tree:**
```
Problem: "Find top 10 customers by revenue and their order counts"
├── Sub-problem 1: "Identify tables (customers, orders)"
│   └── Solution: "Use customers and orders tables"
├── Sub-problem 2: "Calculate revenue per customer"
│   └── Solution: "SUM(orders.amount) GROUP BY customer_id"
├── Sub-problem 3: "Count orders per customer"
│   └── Solution: "COUNT(orders.id) GROUP BY customer_id"
└── Synthesized: "SELECT customers.name, SUM(orders.amount) as revenue,
                  COUNT(orders.id) as order_count FROM customers
                  JOIN orders ON customers.id = orders.customer_id
                  GROUP BY customers.id ORDER BY revenue DESC LIMIT 10"
```

## Integration with Existing Services

The MCP server and tools integrate with:

1. **Database Service** (`database/`) - Provides connection management
2. **API Gateway** (`api_gateway/`) - Routes requests to agents
3. **Orchestration Service** (`orchestration_service/`) - Manages agent workflows

## Configuration

Environment variables:
```bash
GEMINI_API_KEY=your_api_key_here  # For AI model
PYTHONPATH=/app                    # For imports
```

## Testing

Run tests for individual components:
```bash
# Test MCP server
python -m pytest aurabackend/mcp_server/tests/

# Test agent tools
python -m pytest aurabackend/agent_tools/tests/

# Test database agent
python -m pytest aurabackend/orchestration_service/tests/
```

## Docker Deployment

The MCP server is included in docker-compose:

```bash
# Start all services including MCP
docker-compose up -d

# Check MCP server health
curl http://localhost:8007/health

# View MCP server logs
docker-compose logs -f mcp_server
```

## API Examples

### Create Context
```bash
curl -X POST http://localhost:8007/contexts \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent_001",
    "session_id": "session_123",
    "context_type": "database",
    "context_data": {
      "connection_id": "conn_456",
      "schema": {...}
    }
  }'
```

### Send Protocol Message
```bash
curl -X POST http://localhost:8007/messages \
  -H "Content-Type: application/json" \
  -d '{
    "message_type": "tool_call",
    "sender_id": "agent_001",
    "session_id": "session_123",
    "payload": {
      "tool_name": "database_tool",
      "tool_parameters": {...}
    }
  }'
```

## Future Enhancements

- [ ] Add more specialized agents (visualization, analytics)
- [ ] Implement agent learning from feedback
- [ ] Add distributed context storage (Redis)
- [ ] Create agent marketplace for custom agents
- [ ] Implement agent performance monitoring
- [ ] Add multi-language support for agents
- [ ] Create visual agent workflow designer

## Contributing

When adding new agents or tools:
1. Follow the existing tool interface pattern
2. Include comprehensive documentation
3. Add unit tests
4. Update this README
5. Add integration examples

## License

MIT License - See main repository LICENSE file
