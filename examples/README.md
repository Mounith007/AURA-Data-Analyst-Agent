# AURA Agent System Examples

This directory contains example scripts demonstrating the AURA AI Agent System capabilities.

## Prerequisites

1. Install required packages:
```bash
pip install httpx asyncio
```

2. Start the MCP server:
```bash
cd ../aurabackend/mcp_server
python main.py
```

## Running Examples

### Complete Demo
Run all examples in sequence:
```bash
python agent_system_examples.py
```

## What the Examples Demonstrate

### Example 1: List All Agents
- Shows how to retrieve all registered agents
- Displays agent information including ID, name, type, status, and available tools

### Example 2: MCP Server Tools
- Lists all tools available from the Database MCP server
- Shows tool descriptions and required parameters

### Example 3: Execute Agent Task
- Demonstrates executing a task on an agent
- Shows how to retrieve task results and history

### Example 4: Create New Agent
- Shows how to dynamically create new agents
- Demonstrates agent initialization and tool loading

### Example 5: Call MCP Tool Directly
- Demonstrates direct MCP server tool invocation
- Bypasses agent layer for direct tool access

## Expected Output

When you run the examples, you should see:
- Agent listings with their capabilities
- Available MCP tools and their schemas
- Task execution results
- Agent creation confirmation
- Tool call responses

## Troubleshooting

If you get connection errors:
1. Make sure the MCP server is running on port 8007
2. Check that no other service is using port 8007
3. Verify the server started without errors

If agents aren't found:
1. The MCP server automatically creates a default database agent on startup
2. You can create additional agents using the API

## Next Steps

After running these examples:
1. Review the [AGENT_SYSTEM_DOCS.md](../AGENT_SYSTEM_DOCS.md) for detailed documentation
2. Explore creating custom agents by extending `BaseAgent`
3. Create custom tools by extending `AgentTool`
4. Integrate agents with your application using the REST API
