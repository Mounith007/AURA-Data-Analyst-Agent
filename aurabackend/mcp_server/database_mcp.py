"""
Database MCP Server
Provides database connection and schema introspection tools for AI agents
"""

import sys
import os
from typing import Any, Dict, List, Optional
import asyncio

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.base import MCPServer, MCPTool, MCPResource
from database.connection_manager import db_manager, DatabaseConnection, DatabaseType


class DatabaseMCPServer(MCPServer):
    """
    MCP Server for database operations
    Provides tools for connecting, querying, and introspecting databases
    """
    
    def __init__(self):
        super().__init__(name="database", version="1.0.0")
    
    def _initialize(self):
        """Initialize database-specific tools"""
        # Connection management tools
        self._register_connection_tools()
        
        # Schema introspection tools
        self._register_schema_tools()
        
        # Query execution tools
        self._register_query_tools()
    
    def _register_connection_tools(self):
        """Register connection management tools"""
        
        # Test connection tool
        test_connection_tool = MCPTool(
            name="test_database_connection",
            description="Test if a database connection is valid and reachable",
            input_schema={
                "type": "object",
                "properties": {
                    "connection_id": {
                        "type": "string",
                        "description": "The ID of the database connection to test"
                    }
                },
                "required": ["connection_id"]
            },
            handler=self._test_connection_handler
        )
        self.register_tool(test_connection_tool)
        
        # List connections tool
        list_connections_tool = MCPTool(
            name="list_database_connections",
            description="List all available database connections",
            input_schema={
                "type": "object",
                "properties": {}
            },
            handler=self._list_connections_handler
        )
        self.register_tool(list_connections_tool)
        
        # Get connection info tool
        get_connection_tool = MCPTool(
            name="get_database_connection_info",
            description="Get detailed information about a specific database connection",
            input_schema={
                "type": "object",
                "properties": {
                    "connection_id": {
                        "type": "string",
                        "description": "The ID of the database connection"
                    }
                },
                "required": ["connection_id"]
            },
            handler=self._get_connection_handler
        )
        self.register_tool(get_connection_tool)
    
    def _register_schema_tools(self):
        """Register schema introspection tools"""
        
        # Get schema tool
        get_schema_tool = MCPTool(
            name="get_database_schema",
            description="Get the schema of a database including tables, columns, and relationships",
            input_schema={
                "type": "object",
                "properties": {
                    "connection_id": {
                        "type": "string",
                        "description": "The ID of the database connection"
                    },
                    "refresh": {
                        "type": "boolean",
                        "description": "Whether to refresh the schema cache",
                        "default": False
                    }
                },
                "required": ["connection_id"]
            },
            handler=self._get_schema_handler
        )
        self.register_tool(get_schema_tool)
        
        # Get table info tool
        get_table_tool = MCPTool(
            name="get_table_info",
            description="Get detailed information about a specific table",
            input_schema={
                "type": "object",
                "properties": {
                    "connection_id": {
                        "type": "string",
                        "description": "The ID of the database connection"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "The name of the table"
                    },
                    "schema_name": {
                        "type": "string",
                        "description": "The schema name (optional)",
                        "default": "public"
                    }
                },
                "required": ["connection_id", "table_name"]
            },
            handler=self._get_table_info_handler
        )
        self.register_tool(get_table_tool)
    
    def _register_query_tools(self):
        """Register query execution tools"""
        
        # Execute query tool
        execute_query_tool = MCPTool(
            name="execute_database_query",
            description="Execute a SQL query against a database connection",
            input_schema={
                "type": "object",
                "properties": {
                    "connection_id": {
                        "type": "string",
                        "description": "The ID of the database connection"
                    },
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of rows to return",
                        "default": 1000
                    }
                },
                "required": ["connection_id", "query"]
            },
            handler=self._execute_query_handler
        )
        self.register_tool(execute_query_tool)
    
    # Handler implementations
    
    async def _test_connection_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Test database connection handler"""
        connection_id = arguments.get("connection_id")
        connection = await db_manager.get_connection(connection_id)
        
        if not connection:
            return {
                "is_valid": False,
                "message": f"Connection {connection_id} not found"
            }
        
        is_valid = await db_manager.test_connection(connection)
        return {
            "is_valid": is_valid,
            "connection_id": connection_id,
            "connection_name": connection.name,
            "database_type": connection.type.value,
            "message": "Connection successful" if is_valid else "Connection failed"
        }
    
    async def _list_connections_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """List connections handler"""
        connections = await db_manager.list_connections()
        return {
            "connections": [
                {
                    "id": conn.id,
                    "name": conn.name,
                    "type": conn.type.value,
                    "host": conn.host,
                    "database": conn.database,
                    "is_active": conn.is_active
                }
                for conn in connections
            ],
            "count": len(connections)
        }
    
    async def _get_connection_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get connection info handler"""
        connection_id = arguments.get("connection_id")
        connection = await db_manager.get_connection(connection_id)
        
        if not connection:
            raise ValueError(f"Connection {connection_id} not found")
        
        return {
            "id": connection.id,
            "name": connection.name,
            "type": connection.type.value,
            "host": connection.host,
            "port": connection.port,
            "database": connection.database,
            "username": connection.username,
            "ssl_enabled": connection.ssl_enabled,
            "is_active": connection.is_active,
            "metadata": connection.metadata or {}
        }
    
    async def _get_schema_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get database schema handler"""
        connection_id = arguments.get("connection_id")
        refresh = arguments.get("refresh", False)
        
        schema = await db_manager.get_database_schema(connection_id, refresh=refresh)
        
        if not schema:
            raise ValueError(f"Schema not available for connection {connection_id}")
        
        return {
            "connection_id": schema.connection_id,
            "schemas": schema.schemas,
            "tables": [
                {
                    "name": table.name,
                    "schema": table.schema,
                    "columns": table.columns,
                    "primary_keys": table.primary_keys,
                    "foreign_keys": table.foreign_keys,
                    "row_count": table.row_count
                }
                for table in schema.tables
            ],
            "views": [
                {
                    "name": view.name,
                    "schema": view.schema,
                    "columns": view.columns
                }
                for view in schema.views
            ],
            "table_count": len(schema.tables),
            "view_count": len(schema.views)
        }
    
    async def _get_table_info_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get table info handler"""
        connection_id = arguments.get("connection_id")
        table_name = arguments.get("table_name")
        schema_name = arguments.get("schema_name", "public")
        
        schema = await db_manager.get_database_schema(connection_id)
        
        if not schema:
            raise ValueError(f"Schema not available for connection {connection_id}")
        
        # Find the table
        table = None
        for t in schema.tables:
            if t.name == table_name and t.schema == schema_name:
                table = t
                break
        
        if not table:
            raise ValueError(f"Table {schema_name}.{table_name} not found")
        
        return {
            "name": table.name,
            "schema": table.schema,
            "columns": table.columns,
            "primary_keys": table.primary_keys,
            "foreign_keys": table.foreign_keys,
            "indexes": table.indexes,
            "row_count": table.row_count,
            "table_type": table.table_type,
            "description": table.description
        }
    
    async def _execute_query_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute query handler"""
        connection_id = arguments.get("connection_id")
        query = arguments.get("query")
        limit = arguments.get("limit", 1000)
        
        result = await db_manager.execute_query(
            connection_id=connection_id,
            query=query,
            limit=limit
        )
        
        return result
    
    def get_capabilities(self) -> List[str]:
        """Get server capabilities"""
        return [
            "database_connection",
            "schema_introspection",
            "query_execution",
            "multi_database_support"
        ]


# Global instance
database_mcp_server = DatabaseMCPServer()
