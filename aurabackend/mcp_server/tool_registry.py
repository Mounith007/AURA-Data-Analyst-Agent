"""
Tool Registry
Central registry for agent tools with execution capabilities
"""

from typing import Dict, Any, List, Optional, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@dataclass
class Tool:
    """Tool definition with execution handler"""
    name: str
    description: str
    category: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Awaitable[Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """Execute the tool with given parameters"""
        try:
            # Validate parameters (basic validation)
            for param_name, param_spec in self.parameters.items():
                if param_spec.get("required", False) and param_name not in parameters:
                    raise ValueError(f"Missing required parameter: {param_name}")
            
            # Execute the handler
            result = await self.handler(parameters)
            return result
        
        except Exception as e:
            raise Exception(f"Tool execution failed: {str(e)}")

class ToolRegistry:
    """Registry for managing agent tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.db_tools = None
        self._initialize_default_tools()
    
    def _get_db_tools(self):
        """Lazy load database tools to avoid circular imports"""
        if self.db_tools is None:
            try:
                from mcp_server.database_tools import database_tools
                self.db_tools = database_tools
            except ImportError:
                pass
        return self.db_tools
    
    def _initialize_default_tools(self):
        """Initialize default tools"""
        # Database connection tools
        self.register_tool(
            Tool(
                name="connect_database",
                description="Connect to a database",
                category="database",
                parameters={
                    "connection_id": {"type": "string", "required": True, "description": "Database connection ID"},
                },
                returns={"type": "object", "description": "Connection status"},
                handler=self._connect_database_handler
            )
        )
        
        self.register_tool(
            Tool(
                name="list_database_connections",
                description="List all available database connections",
                category="database",
                parameters={},
                returns={"type": "array", "description": "List of database connections"},
                handler=self._list_database_connections_handler
            )
        )
        
        self.register_tool(
            Tool(
                name="query_database",
                description="Execute a SQL query on a database",
                category="database",
                parameters={
                    "connection_id": {"type": "string", "required": True, "description": "Database connection ID"},
                    "query": {"type": "string", "required": True, "description": "SQL query to execute"},
                    "limit": {"type": "integer", "required": False, "description": "Result limit", "default": 1000}
                },
                returns={"type": "object", "description": "Query results"},
                handler=self._query_database_handler
            )
        )
        
        self.register_tool(
            Tool(
                name="get_database_schema",
                description="Get database schema information",
                category="database",
                parameters={
                    "connection_id": {"type": "string", "required": True, "description": "Database connection ID"},
                    "refresh": {"type": "boolean", "required": False, "description": "Refresh schema cache", "default": False}
                },
                returns={"type": "object", "description": "Database schema"},
                handler=self._get_database_schema_handler
            )
        )
        
        # Data analysis tools
        self.register_tool(
            Tool(
                name="analyze_data",
                description="Analyze data and provide insights",
                category="analysis",
                parameters={
                    "data": {"type": "array", "required": True, "description": "Data to analyze"},
                    "analysis_type": {"type": "string", "required": False, "description": "Type of analysis", "default": "summary"}
                },
                returns={"type": "object", "description": "Analysis results"},
                handler=self._analyze_data_handler
            )
        )
        
        # Code generation tools
        self.register_tool(
            Tool(
                name="generate_sql",
                description="Generate SQL query from natural language",
                category="code_generation",
                parameters={
                    "prompt": {"type": "string", "required": True, "description": "Natural language prompt"},
                    "context": {"type": "string", "required": False, "description": "Database context"}
                },
                returns={"type": "string", "description": "Generated SQL query"},
                handler=self._generate_sql_handler
            )
        )
    
    # Tool handlers (these integrate with actual services)
    async def _connect_database_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for database connection"""
        db_tools = self._get_db_tools()
        if db_tools:
            return await db_tools.connect_database_handler(parameters)
        return {
            "status": "error",
            "error": "Database tools not available"
        }
    
    async def _list_database_connections_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for listing database connections"""
        db_tools = self._get_db_tools()
        if db_tools:
            return await db_tools.list_database_connections_handler(parameters)
        return {
            "status": "error",
            "error": "Database tools not available"
        }
    
    async def _query_database_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for database queries"""
        db_tools = self._get_db_tools()
        if db_tools:
            return await db_tools.query_database_handler(parameters)
        return {
            "status": "error",
            "error": "Database tools not available"
        }
    
    async def _get_database_schema_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for getting database schema"""
        db_tools = self._get_db_tools()
        if db_tools:
            return await db_tools.get_database_schema_handler(parameters)
        return {
            "status": "error",
            "error": "Database tools not available"
        }
    
    async def _analyze_data_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for data analysis"""
        # This would integrate with data analysis services
        return {
            "analysis_type": parameters.get("analysis_type", "summary"),
            "insights": [],
            "statistics": {}
        }
    
    async def _generate_sql_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for SQL generation"""
        # This would integrate with code generation service
        return {
            "sql": "SELECT * FROM table LIMIT 10;",
            "confidence": 0.85
        }
    
    def register_tool(self, tool: Tool) -> None:
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[Tool]:
        """List all registered tools"""
        return list(self.tools.values())
    
    def get_tools_by_category(self, category: str) -> List[Tool]:
        """Get tools by category"""
        return [tool for tool in self.tools.values() if tool.category == category]
    
    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool from the registry"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False
