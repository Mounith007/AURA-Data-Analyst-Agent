
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_GATEWAY_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🌐 Starting AURA API Gateway on {host}:{port}...")
    if debug:
        print("🐛 Debug mode enabled")
    
    uvicorn.run("main:api_gateway", host=host, port=port, reload=debug)
