"""
MCP Server API
FastAPI service for Model Context Protocol server operations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.database_mcp import database_mcp_server
from agents.database_agent import DatabaseAgent
from agents.base_agent import global_agent_registry

app = FastAPI(
    title="AURA MCP Server",
    description="Model Context Protocol server for AI agent operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ToolCallRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the tool to call")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Tool arguments")

class AgentTaskRequest(BaseModel):
    agent_id: Optional[str] = Field(None, description="ID of the agent (optional, can be provided in URL)")
    task_type: str = Field(..., description="Type of task to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")

class CreateAgentRequest(BaseModel):
    agent_type: str = Field(..., description="Type of agent to create")
    agent_id: Optional[str] = Field(None, description="Optional custom agent ID")

# Initialize database agent on startup
@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    # Create and register database agent
    db_agent = DatabaseAgent()
    await db_agent.initialize()
    global_agent_registry.register(db_agent)
    print(f"✅ Database agent initialized: {db_agent.agent_id}")

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "mcp_server",
        "mcp_servers": ["database"],
        "agents": len(global_agent_registry.agents)
    }

# MCP Server endpoints
@app.get("/mcp/servers")
async def list_mcp_servers():
    """List all available MCP servers"""
    return {
        "servers": [
            {
                "name": "database",
                "info": database_mcp_server.get_server_info()
            }
        ]
    }

@app.get("/mcp/servers/{server_name}/tools")
async def list_server_tools(server_name: str):
    """List tools for a specific MCP server"""
    if server_name == "database":
        return {
            "server": server_name,
            "tools": database_mcp_server.list_tools()
        }
    else:
        raise HTTPException(status_code=404, detail=f"MCP server '{server_name}' not found")

@app.post("/mcp/servers/{server_name}/call-tool")
async def call_server_tool(server_name: str, request: ToolCallRequest):
    """Call a tool on a specific MCP server"""
    if server_name == "database":
        result = await database_mcp_server.call_tool(request.tool_name, request.arguments)
        return result
    else:
        raise HTTPException(status_code=404, detail=f"MCP server '{server_name}' not found")

# Agent endpoints
@app.get("/agents")
async def list_agents():
    """List all registered agents"""
    return {
        "agents": global_agent_registry.list_agents(),
        "count": len(global_agent_registry.agents)
    }

@app.post("/agents")
async def create_agent(request: CreateAgentRequest):
    """Create a new agent"""
    if request.agent_type == "database":
        agent = DatabaseAgent(agent_id=request.agent_id)
        await agent.initialize()
        global_agent_registry.register(agent)
        
        return {
            "status": "success",
            "agent": agent.get_info()
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unknown agent type: {request.agent_type}")

@app.get("/agents/{agent_id}")
async def get_agent_info(agent_id: str):
    """Get information about a specific agent"""
    agent = global_agent_registry.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    return agent.get_info()

@app.post("/agents/{agent_id}/tasks")
async def execute_agent_task(agent_id: str, request: AgentTaskRequest):
    """Execute a task on a specific agent"""
    # Override agent_id from path parameter
    request.agent_id = agent_id
    
    agent = global_agent_registry.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    # Execute task
    result_task = await agent.run_task(
        task_type=request.task_type,
        **request.parameters
    )
    
    return {
        "task_id": result_task.task_id,
        "status": result_task.status.value,
        "result": result_task.result,
        "error": result_task.error,
        "completed_at": result_task.completed_at
    }

@app.get("/agents/{agent_id}/tasks")
async def get_agent_tasks(agent_id: str):
    """Get task history for an agent"""
    agent = global_agent_registry.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    
    return {
        "agent_id": agent_id,
        "tasks": agent.get_task_history()
    }

@app.get("/agents/types")
async def list_agent_types():
    """List all available agent types"""
    return {
        "agent_types": global_agent_registry.get_agent_types(),
        "available_types": ["database"]  # Can be extended for future agents
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
