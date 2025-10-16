"""
AURA MCP Server Main Application
FastAPI application for Model Context Protocol server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from .context_manager import context_manager, AgentContext
from .protocol_handler import protocol_handler, MessageType, MCPMessage


app = FastAPI(
    title="AURA MCP Server",
    description="Model Context Protocol server for AI agent coordination and context management",
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


# API Models
class CreateContextRequest(BaseModel):
    agent_id: str = Field(..., description="Agent identifier")
    session_id: str = Field(..., description="Session identifier")
    context_type: str = Field(..., description="Type of context (database, conversation, task, tool)")
    context_data: Dict[str, Any] = Field(..., description="Context data")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    ttl_seconds: Optional[int] = Field(default=3600)


class UpdateContextRequest(BaseModel):
    context_data: Dict[str, Any] = Field(..., description="Updated context data")
    merge: bool = Field(default=True, description="Whether to merge or replace")


class CreateDatabaseContextRequest(BaseModel):
    connection_id: str = Field(..., description="Database connection ID")
    database_type: str = Field(..., description="Type of database")
    schema_info: Dict[str, Any] = Field(..., description="Schema information")
    available_tables: List[str] = Field(..., description="Available tables")


class ConversationTurnRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    role: str = Field(..., description="Role (user, assistant, system)")
    message: str = Field(..., description="Message content")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SendMessageRequest(BaseModel):
    message_type: MessageType = Field(..., description="Type of message")
    sender_id: str = Field(..., description="Sender agent ID")
    session_id: str = Field(..., description="Session ID")
    payload: Dict[str, Any] = Field(..., description="Message payload")
    recipient_id: Optional[str] = Field(None, description="Recipient agent ID")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# Health Check
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mcp_server",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


# Context Management Endpoints
@app.post("/contexts")
async def create_context(request: CreateContextRequest) -> Dict[str, Any]:
    """Create a new context for an agent"""
    try:
        context_key = context_manager.create_context(
            agent_id=request.agent_id,
            session_id=request.session_id,
            context_type=request.context_type,
            context_data=request.context_data,
            metadata=request.metadata,
            ttl_seconds=request.ttl_seconds
        )
        
        return {
            "success": True,
            "context_key": context_key,
            "message": "Context created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/contexts/{context_key}")
async def get_context(context_key: str) -> Dict[str, Any]:
    """Get context by key"""
    context = context_manager.get_context(context_key)
    
    if not context:
        raise HTTPException(status_code=404, detail="Context not found or expired")
    
    return {
        "success": True,
        "context": {
            "agent_id": context.agent_id,
            "session_id": context.session_id,
            "context_type": context.context_type,
            "context_data": context.context_data,
            "metadata": context.metadata,
            "created_at": context.created_at.isoformat(),
            "updated_at": context.updated_at.isoformat(),
            "ttl_seconds": context.ttl_seconds
        }
    }


@app.put("/contexts/{context_key}")
async def update_context(context_key: str, request: UpdateContextRequest) -> Dict[str, Any]:
    """Update existing context"""
    success = context_manager.update_context(
        context_key=context_key,
        context_data=request.context_data,
        merge=request.merge
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Context not found")
    
    return {
        "success": True,
        "message": "Context updated successfully"
    }


@app.delete("/contexts/{context_key}")
async def delete_context(context_key: str) -> Dict[str, Any]:
    """Delete a context"""
    success = context_manager.delete_context(context_key)
    
    if not success:
        raise HTTPException(status_code=404, detail="Context not found")
    
    return {
        "success": True,
        "message": "Context deleted successfully"
    }


@app.get("/contexts")
async def list_contexts(
    agent_id: Optional[str] = None,
    session_id: Optional[str] = None,
    context_type: Optional[str] = None
) -> Dict[str, Any]:
    """List contexts with optional filtering"""
    contexts = context_manager.list_contexts(
        agent_id=agent_id,
        session_id=session_id,
        context_type=context_type
    )
    
    return {
        "success": True,
        "count": len(contexts),
        "contexts": [
            {
                "agent_id": ctx.agent_id,
                "session_id": ctx.session_id,
                "context_type": ctx.context_type,
                "created_at": ctx.created_at.isoformat(),
                "updated_at": ctx.updated_at.isoformat()
            }
            for ctx in contexts
        ]
    }


# Database Context Endpoints
@app.post("/database-contexts")
async def create_database_context(request: CreateDatabaseContextRequest) -> Dict[str, Any]:
    """Create database-specific context"""
    try:
        connection_id = context_manager.create_database_context(
            connection_id=request.connection_id,
            database_type=request.database_type,
            schema_info=request.schema_info,
            available_tables=request.available_tables
        )
        
        return {
            "success": True,
            "connection_id": connection_id,
            "message": "Database context created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/database-contexts/{connection_id}")
async def get_database_context(connection_id: str) -> Dict[str, Any]:
    """Get database context"""
    db_context = context_manager.get_database_context(connection_id)
    
    if not db_context:
        raise HTTPException(status_code=404, detail="Database context not found")
    
    return {
        "success": True,
        "database_context": {
            "connection_id": db_context.connection_id,
            "database_type": db_context.database_type,
            "schema_info": db_context.schema_info,
            "available_tables": db_context.available_tables,
            "table_relationships": db_context.table_relationships,
            "recent_queries": db_context.recent_queries[-10:],  # Last 10 queries
            "query_patterns": db_context.query_patterns
        }
    }


@app.post("/database-contexts/{connection_id}/queries")
async def add_query_to_history(connection_id: str, query: Dict[str, str]) -> Dict[str, Any]:
    """Add a query to database context history"""
    try:
        context_manager.add_query_to_history(connection_id, query.get("query", ""))
        return {
            "success": True,
            "message": "Query added to history"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Conversation History Endpoints
@app.post("/conversations")
async def add_conversation_turn(request: ConversationTurnRequest) -> Dict[str, Any]:
    """Add a conversation turn to history"""
    try:
        context_manager.add_conversation_turn(
            session_id=request.session_id,
            role=request.role,
            message=request.message,
            metadata=request.metadata
        )
        
        return {
            "success": True,
            "message": "Conversation turn added"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversations/{session_id}")
async def get_conversation_history(
    session_id: str,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """Get conversation history for a session"""
    history = context_manager.get_conversation_history(session_id, limit)
    
    return {
        "success": True,
        "session_id": session_id,
        "turn_count": len(history),
        "history": history
    }


# Protocol Message Endpoints
@app.post("/messages")
async def send_message(request: SendMessageRequest) -> Dict[str, Any]:
    """Send an MCP protocol message"""
    try:
        message = protocol_handler.create_message(
            message_type=request.message_type,
            sender_id=request.sender_id,
            session_id=request.session_id,
            payload=request.payload,
            recipient_id=request.recipient_id,
            metadata=request.metadata
        )
        
        result = protocol_handler.route_message(message)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/messages")
async def get_messages(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Get messages from queue"""
    messages = protocol_handler.get_message_queue(session_id)
    
    return {
        "success": True,
        "count": len(messages),
        "messages": [
            {
                "message_id": msg.message_id,
                "message_type": msg.message_type.value,
                "sender_id": msg.sender_id,
                "recipient_id": msg.recipient_id,
                "session_id": msg.session_id,
                "payload": msg.payload
            }
            for msg in messages
        ]
    }


# Statistics Endpoints
@app.get("/stats/contexts")
async def get_context_stats() -> Dict[str, Any]:
    """Get context usage statistics"""
    stats = context_manager.get_context_stats()
    return {
        "success": True,
        "stats": stats
    }


@app.get("/stats/protocol")
async def get_protocol_stats() -> Dict[str, Any]:
    """Get protocol statistics"""
    stats = protocol_handler.get_protocol_stats()
    return {
        "success": True,
        "stats": stats
    }


# Maintenance Endpoints
@app.post("/maintenance/clear-expired")
async def clear_expired_contexts() -> Dict[str, Any]:
    """Clear expired contexts"""
    count = context_manager.clear_expired_contexts()
    protocol_handler.clear_processed_messages()
    
    return {
        "success": True,
        "expired_contexts_cleared": count,
        "message": "Maintenance completed"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
