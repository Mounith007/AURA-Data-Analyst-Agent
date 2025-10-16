"""
Context Manager for MCP Server
Manages context for AI agents including database schema, conversation history, and metadata
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class AgentContext:
    """Context information for an AI agent"""
    agent_id: str
    session_id: str
    context_type: str  # 'database', 'conversation', 'task', 'tool'
    context_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    ttl_seconds: Optional[int] = 3600  # Context expires after 1 hour by default


@dataclass
class DatabaseContext:
    """Database-specific context"""
    connection_id: str
    database_type: str
    schema_info: Dict[str, Any]
    available_tables: List[str]
    table_relationships: Dict[str, List[str]] = field(default_factory=dict)
    recent_queries: List[str] = field(default_factory=list)
    query_patterns: Dict[str, int] = field(default_factory=dict)


class ContextManager:
    """Manages context for AI agents in the MCP protocol"""
    
    def __init__(self):
        self.contexts: Dict[str, AgentContext] = {}
        self.database_contexts: Dict[str, DatabaseContext] = {}
        self.conversation_history: Dict[str, List[Dict[str, Any]]] = {}
    
    def create_context(
        self, 
        agent_id: str, 
        session_id: str, 
        context_type: str, 
        context_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        ttl_seconds: Optional[int] = 3600
    ) -> str:
        """Create a new context for an agent"""
        context_key = f"{agent_id}:{session_id}:{context_type}"
        
        context = AgentContext(
            agent_id=agent_id,
            session_id=session_id,
            context_type=context_type,
            context_data=context_data,
            metadata=metadata or {},
            ttl_seconds=ttl_seconds
        )
        
        self.contexts[context_key] = context
        return context_key
    
    def get_context(self, context_key: str) -> Optional[AgentContext]:
        """Retrieve context by key"""
        context = self.contexts.get(context_key)
        
        # Check if context has expired
        if context and context.ttl_seconds:
            age_seconds = (datetime.now() - context.created_at).total_seconds()
            if age_seconds > context.ttl_seconds:
                del self.contexts[context_key]
                return None
        
        return context
    
    def update_context(
        self, 
        context_key: str, 
        context_data: Dict[str, Any],
        merge: bool = True
    ) -> bool:
        """Update existing context"""
        context = self.get_context(context_key)
        
        if not context:
            return False
        
        if merge:
            context.context_data.update(context_data)
        else:
            context.context_data = context_data
        
        context.updated_at = datetime.now()
        return True
    
    def delete_context(self, context_key: str) -> bool:
        """Delete a context"""
        if context_key in self.contexts:
            del self.contexts[context_key]
            return True
        return False
    
    def list_contexts(
        self, 
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        context_type: Optional[str] = None
    ) -> List[AgentContext]:
        """List contexts with optional filtering"""
        contexts = []
        
        for context in self.contexts.values():
            # Check if context has expired
            if context.ttl_seconds:
                age_seconds = (datetime.now() - context.created_at).total_seconds()
                if age_seconds > context.ttl_seconds:
                    continue
            
            # Apply filters
            if agent_id and context.agent_id != agent_id:
                continue
            if session_id and context.session_id != session_id:
                continue
            if context_type and context.context_type != context_type:
                continue
            
            contexts.append(context)
        
        return contexts
    
    def create_database_context(
        self,
        connection_id: str,
        database_type: str,
        schema_info: Dict[str, Any],
        available_tables: List[str]
    ) -> str:
        """Create database-specific context"""
        db_context = DatabaseContext(
            connection_id=connection_id,
            database_type=database_type,
            schema_info=schema_info,
            available_tables=available_tables
        )
        
        self.database_contexts[connection_id] = db_context
        return connection_id
    
    def get_database_context(self, connection_id: str) -> Optional[DatabaseContext]:
        """Get database context"""
        return self.database_contexts.get(connection_id)
    
    def add_query_to_history(self, connection_id: str, query: str):
        """Add a query to database context history"""
        db_context = self.database_contexts.get(connection_id)
        if db_context:
            db_context.recent_queries.append(query)
            # Keep only last 50 queries
            if len(db_context.recent_queries) > 50:
                db_context.recent_queries.pop(0)
            
            # Track query patterns
            query_type = query.strip().split()[0].upper()
            db_context.query_patterns[query_type] = \
                db_context.query_patterns.get(query_type, 0) + 1
    
    def add_conversation_turn(
        self,
        session_id: str,
        role: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add a conversation turn to history"""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        turn = {
            "role": role,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversation_history[session_id].append(turn)
        
        # Keep only last 100 turns
        if len(self.conversation_history[session_id]) > 100:
            self.conversation_history[session_id].pop(0)
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        history = self.conversation_history.get(session_id, [])
        
        if limit:
            return history[-limit:]
        return history
    
    def clear_expired_contexts(self) -> int:
        """Remove all expired contexts and return count"""
        expired_keys = []
        
        for key, context in self.contexts.items():
            if context.ttl_seconds:
                age_seconds = (datetime.now() - context.created_at).total_seconds()
                if age_seconds > context.ttl_seconds:
                    expired_keys.append(key)
        
        for key in expired_keys:
            del self.contexts[key]
        
        return len(expired_keys)
    
    def get_context_stats(self) -> Dict[str, Any]:
        """Get statistics about context usage"""
        stats = {
            "total_contexts": len(self.contexts),
            "database_contexts": len(self.database_contexts),
            "conversation_sessions": len(self.conversation_history),
            "contexts_by_type": {},
            "contexts_by_agent": {}
        }
        
        for context in self.contexts.values():
            # Count by type
            stats["contexts_by_type"][context.context_type] = \
                stats["contexts_by_type"].get(context.context_type, 0) + 1
            
            # Count by agent
            stats["contexts_by_agent"][context.agent_id] = \
                stats["contexts_by_agent"].get(context.agent_id, 0) + 1
        
        return stats


# Global context manager instance
context_manager = ContextManager()
