
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from aurabackend.shared.models import ChatRequest, AgentResponse

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

@api_gateway.post("/generate_query")
async def generate_query_proxy(request: ChatRequest):
	async with httpx.AsyncClient() as client:
		response = await client.post("http://localhost:8001/generate_query", json=request.model_dump())
		return response.json()

# TODO: Add authentication, authorization, and more routing logic
