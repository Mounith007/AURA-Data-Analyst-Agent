
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import sys
import os
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import file service
try:
    from shared.file_service import file_service
except ImportError as e:
    print(f"Warning: File service not available - {e}")
    file_service = None

# Define models directly here to avoid import issues
class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class QueryRequest(BaseModel):
    session_id: str
    prompt: str
    context: Optional[str] = None

class AgentResponse(BaseModel):
    response: str
    confidence: float
    suggestions: List[str] = []
    metadata: Dict[str, Any] = {}

api_gateway = FastAPI()

# Add CORS middleware to allow frontend connections
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:3000").split(",")
api_gateway.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_gateway.get("/")
def root():
	return {"message": "API Gateway is running."}

@api_gateway.get("/health")
def health_check():
    return {"status": "healthy", "service": "api_gateway"}

@api_gateway.get("/files/supported-formats")
def get_supported_formats():
    """Get list of supported file formats"""
    try:
        return {
            "status": "success",
            "supported_formats": {
                "csv": {"extensions": [".csv"], "description": "Comma-separated values", "icon": "📊"},
                "excel": {"extensions": [".xlsx", ".xls"], "description": "Microsoft Excel", "icon": "📈"},
                "json": {"extensions": [".json"], "description": "JavaScript Object Notation", "icon": "🔗"},
                "text": {"extensions": [".txt"], "description": "Plain text files", "icon": "📄"},
                "parquet": {"extensions": [".parquet"], "description": "Apache Parquet columnar storage", "icon": "🗃️"}
            },
            "max_file_size": "25MB",
            "notes": {
                "parquet": "Optimized for analytics workloads, supports compression and efficient querying",
                "csv": "Most common format, human-readable",
                "excel": "Supports multiple sheets and formatting",
                "json": "Flexible structure, good for nested data"
            }
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@api_gateway.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for AI interactions"""
    try:
        # For now, return a simple response
        # Later this will integrate with AI services
        return {
            "response": f"Received your message: {request.message}",
            "confidence": 0.95,
            "suggestions": ["Try asking about data analysis", "Connect to a database", "Create visualizations"],
            "metadata": {"timestamp": "now", "service": "api_gateway"}
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}

@api_gateway.post("/generate_query")
async def generate_query_proxy(request: QueryRequest):
    """Generate SQL query from natural language prompt"""
    try:
        # For now, return a mock response since code generation service isn't running
        # Later this will integrate with actual AI services
        mock_sql = f"""
        -- Generated SQL for: {request.prompt}
        -- Session: {request.session_id}
        SELECT product_name, total_revenue, sale_date 
        FROM sales_table 
        WHERE sale_date >= '2024-01-01'
        ORDER BY total_revenue DESC
        LIMIT 10;
        """
        
        return {
            "status": "Success",
            "final_query": mock_sql.strip(),
            "job_id": f"job_{request.session_id}_{int(__import__('time').time())}",
            "confidence": 0.85,
            "explanation": f"Generated SQL query for analyzing: {request.prompt}"
        }
    except Exception as e:
        return {
            "status": "Error", 
            "error_message": str(e),
            "final_query": "-- Error generating query"
        }

@api_gateway.get("/databases/test/{db_type}")
async def test_database_connection(db_type: str):
    """Proxy to database service for connection testing"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"http://localhost:8002/databases/test/{db_type}")
            return response.json()
    except Exception as e:
        return {"error": f"Database service unavailable: {str(e)}", "status": "error"}

# MCP Server Integration Endpoints
@api_gateway.post("/agent/context")
async def create_agent_context(context_data: Dict[str, Any]):
    """Create context in MCP server for agent use"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:8007/contexts",
                json=context_data
            )
            return response.json()
    except Exception as e:
        return {"error": f"MCP server unavailable: {str(e)}", "status": "error"}

@api_gateway.get("/agent/context/{context_key}")
async def get_agent_context(context_key: str):
    """Retrieve context from MCP server"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"http://localhost:8007/contexts/{context_key}")
            return response.json()
    except Exception as e:
        return {"error": f"MCP server unavailable: {str(e)}", "status": "error"}

@api_gateway.get("/agent/stats")
async def get_agent_stats():
    """Get agent and context statistics from MCP server"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            context_stats = await client.get("http://localhost:8007/stats/contexts")
            protocol_stats = await client.get("http://localhost:8007/stats/protocol")
            
            return {
                "context_stats": context_stats.json(),
                "protocol_stats": protocol_stats.json(),
                "status": "success"
            }
    except Exception as e:
        return {"error": f"MCP server unavailable: {str(e)}", "status": "error"}

# File Upload Endpoints
@api_gateway.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a data file (CSV, JSON, Excel, TXT, Parquet)"""
    if file_service is None:
        raise HTTPException(status_code=503, detail="File service not available")
    
    try:
        # Save file
        file_metadata = await file_service.save_file(file)
        
        # Process file
        processed_metadata = await file_service.process_file(file_metadata)
        
        return {
            "status": "success",
            "message": "File uploaded and processed successfully",
            "file_info": {
                "file_id": processed_metadata["file_id"],
                "original_filename": processed_metadata["original_filename"],
                "file_size": processed_metadata["file_size"],
                "rows_count": processed_metadata["rows_count"],
                "columns_count": processed_metadata["columns_count"],
                "upload_time": processed_metadata["upload_time"],
                "processed_time": processed_metadata["processed_time"]
            },
            "preview": processed_metadata.get("preview_data", [])
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@api_gateway.get("/files")
async def list_files():
    """List all uploaded files"""
    if file_service is None:
        return {"status": "error", "error": "File service not available"}
    
    try:
        files = file_service.list_files()
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@api_gateway.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """Get information about a specific file"""
    if file_service is None:
        return {"status": "error", "error": "File service not available"}
    
    try:
        file_info = file_service.get_file_info(file_id)
        if file_info:
            return {"status": "success", "file_info": file_info}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"status": "error", "error": str(e)}

@api_gateway.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete a file and its processed data"""
    if file_service is None:
        return {"status": "error", "error": "File service not available"}
    
    try:
        success = file_service.delete_file(file_id)
        if success:
            return {"status": "success", "message": "File deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found or deletion failed")
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"status": "error", "error": str(e)}

# Enhanced Agent Endpoints
@api_gateway.post("/agent/database/query")
async def process_database_query(request: Dict[str, Any]):
    """
    Process natural language query using enhanced database agent
    Uses recursive reasoning and validation
    """
    try:
        user_query = request.get("query", "")
        connection_id = request.get("connection_id")
        session_id = request.get("session_id", "default")
        
        if not user_query:
            return {"error": "Query is required", "status": "error"}
        
        # For now, return enhanced response structure
        # In production, this would integrate with the actual DatabaseAgent
        return {
            "status": "success",
            "query": user_query,
            "connection_id": connection_id,
            "session_id": session_id,
            "sql_generated": f"-- Enhanced SQL for: {user_query}\nSELECT * FROM table LIMIT 10;",
            "validation": {
                "is_valid": True,
                "security_score": 95,
                "warnings": [],
                "suggestions": ["Consider adding specific column names"]
            },
            "reasoning": {
                "steps": [
                    "Analyzed user query",
                    "Identified required tables",
                    "Generated optimized SQL"
                ],
                "confidence": 0.85
            },
            "agent_info": {
                "agent_id": "database_agent_001",
                "capabilities": ["query_generation", "validation", "recursive_reasoning"]
            }
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}

@api_gateway.post("/agent/database/analyze")
async def analyze_database(request: Dict[str, Any]):
    """
    Perform comprehensive database analysis using enhanced agent
    """
    try:
        connection_id = request.get("connection_id")
        
        if not connection_id:
            return {"error": "Connection ID is required", "status": "error"}
        
        # For now, return mock analysis
        # In production, this would use DatabaseAgent.analyze_database()
        return {
            "status": "success",
            "connection_id": connection_id,
            "analysis": {
                "schema_quality": 85,
                "total_tables": 15,
                "total_columns": 120,
                "recommendations": [
                    "Add indexes on frequently queried columns",
                    "Consider partitioning large tables",
                    "Review tables without primary keys"
                ],
                "relationships": {
                    "explicit": 12,
                    "implicit": 5
                },
                "performance_insights": [
                    "3 large tables detected (>100k rows)",
                    "Queries on these tables may benefit from optimization"
                ]
            }
        }
    except Exception as e:
        return {"error": str(e), "status": "error"}

@api_gateway.get("/agent/tools")
async def get_available_tools():
    """Get list of available agent tools"""
    return {
        "status": "success",
        "tools": [
            {
                "name": "database_tool",
                "description": "Execute database operations",
                "operations": ["execute_query", "get_schema", "test_connection", "list_connections"]
            },
            {
                "name": "query_validator",
                "description": "Validate SQL queries for security",
                "operations": ["validate_query", "sanitize_query"]
            },
            {
                "name": "schema_analyzer",
                "description": "Analyze database schemas",
                "operations": ["analyze_schema", "suggest_indexes", "find_relationships"]
            },
            {
                "name": "recursive_reasoner",
                "description": "Apply recursive reasoning to problems",
                "operations": ["reason", "explain_reasoning"]
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_GATEWAY_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🌐 Starting AURA API Gateway on {host}:{port}...")
    if debug:
        print("🐛 Debug mode enabled")
    
    uvicorn.run("main:api_gateway", host=host, port=port, reload=debug)
