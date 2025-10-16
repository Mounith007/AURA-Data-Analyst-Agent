"""
Protocol Handler for MCP Server
Implements the Model Context Protocol for agent communication
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import json


class MessageType(Enum):
    """Types of MCP messages"""
    CONTEXT_REQUEST = "context_request"
    CONTEXT_RESPONSE = "context_response"
    CONTEXT_UPDATE = "context_update"
    TOOL_CALL = "tool_call"
    TOOL_RESPONSE = "tool_response"
    AGENT_HANDOFF = "agent_handoff"
    ERROR = "error"


class MCPMessage(BaseModel):
    """Base MCP message structure"""
    message_id: str = Field(..., description="Unique message identifier")
    message_type: MessageType = Field(..., description="Type of message")
    sender_id: str = Field(..., description="ID of the sending agent")
    recipient_id: Optional[str] = Field(None, description="ID of the recipient agent")
    session_id: str = Field(..., description="Session identifier")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Message payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ContextRequest(BaseModel):
    """Request for context information"""
    context_type: str = Field(..., description="Type of context requested")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Filters for context")


class ContextResponse(BaseModel):
    """Response with context information"""
    context_data: Dict[str, Any] = Field(..., description="The requested context")
    context_key: str = Field(..., description="Key to retrieve this context")


class ToolCall(BaseModel):
    """Request to execute a tool"""
    tool_name: str = Field(..., description="Name of the tool to execute")
    tool_parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters for tool")
    requires_approval: bool = Field(default=False, description="Whether human approval is needed")


class ToolResponse(BaseModel):
    """Response from tool execution"""
    tool_name: str = Field(..., description="Name of the executed tool")
    success: bool = Field(..., description="Whether execution was successful")
    result: Any = Field(None, description="Result of the tool execution")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class AgentHandoff(BaseModel):
    """Handoff task to another agent"""
    target_agent_id: str = Field(..., description="ID of the agent to hand off to")
    task_description: str = Field(..., description="Description of the task")
    context_keys: List[str] = Field(default_factory=list, description="Context keys to transfer")


class ProtocolHandler:
    """Handles MCP protocol messages and routing"""
    
    def __init__(self):
        self.message_handlers: Dict[MessageType, Any] = {
            MessageType.CONTEXT_REQUEST: self._handle_context_request,
            MessageType.CONTEXT_UPDATE: self._handle_context_update,
            MessageType.TOOL_CALL: self._handle_tool_call,
            MessageType.AGENT_HANDOFF: self._handle_agent_handoff,
        }
        self.message_queue: List[MCPMessage] = []
        self.processed_messages: List[str] = []
    
    def create_message(
        self,
        message_type: MessageType,
        sender_id: str,
        session_id: str,
        payload: Dict[str, Any],
        recipient_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MCPMessage:
        """Create a new MCP message"""
        import uuid
        
        message = MCPMessage(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            sender_id=sender_id,
            recipient_id=recipient_id,
            session_id=session_id,
            payload=payload,
            metadata=metadata or {}
        )
        
        return message
    
    def route_message(self, message: MCPMessage) -> Dict[str, Any]:
        """Route message to appropriate handler"""
        handler = self.message_handlers.get(message.message_type)
        
        if not handler:
            return {
                "success": False,
                "error": f"No handler for message type: {message.message_type}"
            }
        
        # Add to queue
        self.message_queue.append(message)
        
        # Process message
        try:
            result = handler(message)
            self.processed_messages.append(message.message_id)
            return {
                "success": True,
                "result": result,
                "message_id": message.message_id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message_id": message.message_id
            }
    
    def _handle_context_request(self, message: MCPMessage) -> Dict[str, Any]:
        """Handle context request message"""
        request = ContextRequest(**message.payload)
        
        # This would integrate with ContextManager
        return {
            "message_type": "context_response",
            "context_type": request.context_type,
            "filters_applied": request.filters,
            "note": "Context retrieval to be implemented with ContextManager integration"
        }
    
    def _handle_context_update(self, message: MCPMessage) -> Dict[str, Any]:
        """Handle context update message"""
        return {
            "message_type": "context_update_ack",
            "updated": True,
            "context_key": message.payload.get("context_key")
        }
    
    def _handle_tool_call(self, message: MCPMessage) -> Dict[str, Any]:
        """Handle tool call message"""
        tool_call = ToolCall(**message.payload)
        
        # This would integrate with tool execution system
        return {
            "message_type": "tool_response",
            "tool_name": tool_call.tool_name,
            "execution_status": "queued" if tool_call.requires_approval else "executing",
            "note": "Tool execution to be implemented with agent tool system"
        }
    
    def _handle_agent_handoff(self, message: MCPMessage) -> Dict[str, Any]:
        """Handle agent handoff message"""
        handoff = AgentHandoff(**message.payload)
        
        return {
            "message_type": "handoff_ack",
            "target_agent": handoff.target_agent_id,
            "task_queued": True,
            "context_keys_transferred": handoff.context_keys
        }
    
    def get_message_queue(self, session_id: Optional[str] = None) -> List[MCPMessage]:
        """Get messages from queue"""
        if session_id:
            return [msg for msg in self.message_queue if msg.session_id == session_id]
        return self.message_queue
    
    def clear_processed_messages(self, older_than_count: int = 1000):
        """Clear old processed messages"""
        if len(self.processed_messages) > older_than_count:
            self.processed_messages = self.processed_messages[-older_than_count:]
    
    def get_protocol_stats(self) -> Dict[str, Any]:
        """Get protocol statistics"""
        message_type_counts = {}
        
        for message in self.message_queue:
            msg_type = message.message_type.value
            message_type_counts[msg_type] = message_type_counts.get(msg_type, 0) + 1
        
        return {
            "total_messages": len(self.message_queue),
            "processed_messages": len(self.processed_messages),
            "message_types": message_type_counts,
            "active_sessions": len(set(msg.session_id for msg in self.message_queue))
        }


# Global protocol handler instance
protocol_handler = ProtocolHandler()
