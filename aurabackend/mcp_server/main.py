"""
AURA MCP Server
Model Context Protocol server for multi-agent communication and tool orchestration
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.tool_registry import ToolRegistry, Tool
from mcp_server.agent_registry import AgentRegistry, AgentDefinition

app = FastAPI(
    title="AURA MCP Server",
    description="Model Context Protocol server for agent communication and tool orchestration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize registries
tool_registry = ToolRegistry()
agent_registry = AgentRegistry()

# Request/Response Models
class ToolExecutionRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the tool to execute")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters")
    agent_id: Optional[str] = Field(None, description="ID of the agent making the request")

class ToolExecutionResponse(BaseModel):
    execution_id: str
    tool_name: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: int
    timestamp: datetime

class AgentTaskRequest(BaseModel):
    agent_type: str = Field(..., description="Type of agent to use")
    task: str = Field(..., description="Task description")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Task context")
    tools_allowed: Optional[List[str]] = Field(None, description="List of tool names the agent can use")

class AgentTaskResponse(BaseModel):
    task_id: str
    agent_id: str
    status: str
    result: Optional[Any] = None
    tools_used: List[str] = []
    execution_time_ms: int
    timestamp: datetime

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mcp_server",
        "timestamp": datetime.now(),
        "registered_tools": len(tool_registry.list_tools()),
        "registered_agents": len(agent_registry.list_agents())
    }

# Tool Management
@app.get("/tools")
async def list_tools() -> Dict[str, Any]:
    """List all registered tools"""
    tools = tool_registry.list_tools()
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "category": tool.category,
                "parameters": tool.parameters,
                "returns": tool.returns
            }
            for tool in tools
        ],
        "count": len(tools)
    }

@app.get("/tools/{tool_name}")
async def get_tool(tool_name: str) -> Dict[str, Any]:
    """Get tool details"""
    tool = tool_registry.get_tool(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    
    return {
        "name": tool.name,
        "description": tool.description,
        "category": tool.category,
        "parameters": tool.parameters,
        "returns": tool.returns,
        "metadata": tool.metadata
    }

@app.post("/tools/execute")
async def execute_tool(request: ToolExecutionRequest) -> ToolExecutionResponse:
    """Execute a tool"""
    start_time = datetime.now()
    execution_id = str(uuid.uuid4())
    
    try:
        tool = tool_registry.get_tool(request.tool_name)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool {request.tool_name} not found")
        
        # Execute the tool
        result = await tool.execute(request.parameters)
        
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return ToolExecutionResponse(
            execution_id=execution_id,
            tool_name=request.tool_name,
            status="success",
            result=result,
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        return ToolExecutionResponse(
            execution_id=execution_id,
            tool_name=request.tool_name,
            status="error",
            error=str(e),
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now()
        )

# Agent Management
@app.get("/agents")
async def list_agents() -> Dict[str, Any]:
    """List all registered agents"""
    agents = agent_registry.list_agents()
    return {
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "type": agent.type.value if hasattr(agent.type, 'value') else agent.type,
                "description": agent.description,
                "capabilities": agent.capabilities,
                "model": agent.model
            }
            for agent in agents
        ],
        "count": len(agents)
    }

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str) -> Dict[str, Any]:
    """Get agent details"""
    agent = agent_registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    return {
        "id": agent.id,
        "name": agent.name,
        "type": agent.type.value if hasattr(agent.type, 'value') else agent.type,
        "description": agent.description,
        "capabilities": agent.capabilities,
        "model": agent.model,
        "tools_available": agent.tools_available,
        "metadata": agent.metadata
    }

@app.post("/agents/execute")
async def execute_agent_task(request: AgentTaskRequest) -> AgentTaskResponse:
    """Execute an agent task"""
    start_time = datetime.now()
    task_id = str(uuid.uuid4())
    
    try:
        # Get an agent of the requested type
        agents = agent_registry.get_agents_by_type(request.agent_type)
        if not agents:
            raise HTTPException(status_code=404, detail=f"No agents of type {request.agent_type} found")
        
        agent = agents[0]  # Use the first available agent
        
        # Execute the task (this would integrate with actual agent logic)
        result = await agent_registry.execute_task(
            agent_id=agent.id,
            task=request.task,
            context=request.context,
            tools_allowed=request.tools_allowed
        )
        
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return AgentTaskResponse(
            task_id=task_id,
            agent_id=agent.id,
            status="success",
            result=result,
            tools_used=result.get("tools_used", []) if isinstance(result, dict) else [],
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        return AgentTaskResponse(
            task_id=task_id,
            agent_id="",
            status="error",
            result={"error": str(e)},
            tools_used=[],
            execution_time_ms=execution_time_ms,
            timestamp=datetime.now()
        )

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "AURA MCP Server is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tools": "/tools",
            "agents": "/agents"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_SERVER_PORT", 8003))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🔧 Starting AURA MCP Server on {host}:{port}...")
    if debug:
        print("🐛 Debug mode enabled")
    
    uvicorn.run("main:app", host=host, port=port, reload=debug)
