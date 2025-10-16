"""
Database Agent Service
RESTful API for the Database Connection Agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.database_agent import database_agent

app = FastAPI(
    title="AURA Database Agent Service",
    description="AI-powered database connection and management agent",
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

# Request Models
class ConnectDatabaseRequest(BaseModel):
    name: str = Field(..., description="Connection name")
    db_type: str = Field(..., description="Database type")
    host: str = Field(..., description="Database host")
    port: int = Field(..., description="Database port")
    database: str = Field(..., description="Database name")
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    ssl_enabled: bool = Field(default=False, description="Enable SSL")
    connection_string: Optional[str] = Field(None, description="Custom connection string")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ExecuteQueryRequest(BaseModel):
    connection_id: str = Field(..., description="Database connection ID")
    query: str = Field(..., description="SQL query to execute")
    limit: int = Field(default=1000, description="Result limit")

class OptimizeQueryRequest(BaseModel):
    connection_id: str = Field(..., description="Database connection ID")
    query: str = Field(..., description="SQL query to optimize")

# Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "database_agent",
        "agent_id": database_agent.agent_id,
        "agent_name": database_agent.name,
        "model": database_agent.model_name
    }

@app.get("/agent/info")
async def get_agent_info():
    """Get agent information"""
    return {
        "agent_id": database_agent.agent_id,
        "name": database_agent.name,
        "model": database_agent.model_name,
        "capabilities": database_agent.capabilities,
        "supported_databases": database_agent.supported_databases
    }

@app.post("/connect")
async def connect_database(request: ConnectDatabaseRequest):
    """Connect to a database"""
    result = await database_agent.connect_database(
        name=request.name,
        db_type=request.db_type,
        host=request.host,
        port=request.port,
        database=request.database,
        username=request.username,
        password=request.password,
        ssl_enabled=request.ssl_enabled,
        connection_string=request.connection_string,
        metadata=request.metadata
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@app.get("/connections")
async def list_connections():
    """List all database connections"""
    result = await database_agent.list_connections()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.get("/connections/{connection_id}")
async def get_connection_info(connection_id: str):
    """Get connection information"""
    result = await database_agent.get_connection_info(connection_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

@app.post("/connections/{connection_id}/test")
async def test_connection(connection_id: str):
    """Test a database connection"""
    result = await database_agent.test_connection(connection_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.get("/connections/{connection_id}/schema")
async def get_database_schema(connection_id: str, refresh: bool = False):
    """Get database schema with AI insights"""
    result = await database_agent.get_database_schema(connection_id, refresh=refresh)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result

@app.post("/query")
async def execute_query(request: ExecuteQueryRequest):
    """Execute a database query"""
    result = await database_agent.execute_query(
        connection_id=request.connection_id,
        query=request.query,
        limit=request.limit
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.post("/query/optimize")
async def optimize_query(request: OptimizeQueryRequest):
    """Get AI-powered query optimization suggestions"""
    result = await database_agent.suggest_query_optimization(
        query=request.query,
        connection_id=request.connection_id
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "AURA Database Agent Service is running",
        "agent": database_agent.name,
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("DATABASE_AGENT_PORT", 8004))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🤖 Starting AURA Database Agent Service on {host}:{port}...")
    print(f"🧠 Using model: {database_agent.model_name}")
    if debug:
        print("🐛 Debug mode enabled")
    
    uvicorn.run("main:app", host=host, port=port, reload=debug)
