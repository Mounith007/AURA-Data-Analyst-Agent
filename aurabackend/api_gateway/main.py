
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import sys
import os
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
api_gateway.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
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

if __name__ == "__main__":
    import uvicorn
    print("🌐 Starting AURA API Gateway on port 8000...")
    uvicorn.run("main:api_gateway", host="0.0.0.0", port=8000, reload=True)
