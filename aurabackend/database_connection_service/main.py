
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel

db_connection_app = FastAPI()

# Add CORS middleware to allow frontend connections
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:5174,http://localhost:3000").split(",")
db_connection_app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionDetails(BaseModel):
    type: str
    host: str
    port: int
    user: str
    password: str
    dbname: str

@db_connection_app.get("/")
def root():
    return {"message": "Database Connection Service is running."}

@db_connection_app.get("/health")
def health_check():
    return {"status": "healthy", "service": "database_connection_service"}

@db_connection_app.post("/connect")
async def connect_to_database(details: ConnectionDetails):
    # TODO: Implement actual database connection logic
    print(f"Received connection request for {details.type} database at {details.host}:{details.port}")
    return {"status": "success", "message": "Connection successful"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("DB_CONNECTION_PORT", 8007))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🔌 Starting Database Connection Service on {host}:{port}...")
    if debug:
        print("🐛 Debug mode enabled")
    
    uvicorn.run("main:db_connection_app", host=host, port=port, reload=debug)
