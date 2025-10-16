"""
Database Tools for AI Agents
Tools for database operations, schema introspection, and query execution
"""

import sys
import os
from typing import Any, Dict, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_tools.base_tool import AgentTool, ToolExecutionResult
from database.connection_manager import db_manager


class DatabaseQueryTool(AgentTool):
    """Tool for executing database queries"""
    
    def __init__(self):
        super().__init__(
            name="database_query",
            description="Execute SQL queries against connected databases",
            version="1.0.0"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
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
            "required": ["connection_id", "query"],
            "categories": ["database", "query"]
        }
    
    async def execute(self, **kwargs) -> ToolExecutionResult:
        connection_id = kwargs.get("connection_id")
        query = kwargs.get("query")
        limit = kwargs.get("limit", 1000)
        
        if not connection_id or not query:
            return ToolExecutionResult(
                success=False,
                data=None,
                error="Missing required parameters: connection_id and query"
            )
        
        try:
            result = await db_manager.execute_query(
                connection_id=connection_id,
                query=query,
                limit=limit
            )
            
            return ToolExecutionResult(
                success=True,
                data=result,
                metadata={
                    "row_count": result.get("row_count", 0),
                    "connection_id": connection_id
                }
            )
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                data=None,
                error=f"Query execution failed: {str(e)}"
            )


class SchemaIntrospectionTool(AgentTool):
    """Tool for introspecting database schemas"""
    
    def __init__(self):
        super().__init__(
            name="schema_introspection",
            description="Introspect database schemas to understand structure",
            version="1.0.0"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
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
                },
                "table_name": {
                    "type": "string",
                    "description": "Specific table name to introspect (optional)"
                }
            },
            "required": ["connection_id"],
            "categories": ["database", "schema"]
        }
    
    async def execute(self, **kwargs) -> ToolExecutionResult:
        connection_id = kwargs.get("connection_id")
        refresh = kwargs.get("refresh", False)
        table_name = kwargs.get("table_name")
        
        if not connection_id:
            return ToolExecutionResult(
                success=False,
                data=None,
                error="Missing required parameter: connection_id"
            )
        
        try:
            schema = await db_manager.get_database_schema(connection_id, refresh=refresh)
            
            if not schema:
                return ToolExecutionResult(
                    success=False,
                    data=None,
                    error=f"Schema not available for connection {connection_id}"
                )
            
            # If specific table requested, filter to that table
            if table_name:
                table = next((t for t in schema.tables if t.name == table_name), None)
                if not table:
                    return ToolExecutionResult(
                        success=False,
                        data=None,
                        error=f"Table {table_name} not found"
                    )
                
                data = {
                    "table": {
                        "name": table.name,
                        "schema": table.schema,
                        "columns": table.columns,
                        "primary_keys": table.primary_keys,
                        "foreign_keys": table.foreign_keys,
                        "indexes": table.indexes,
                        "row_count": table.row_count
                    }
                }
            else:
                # Return full schema
                data = {
                    "schemas": schema.schemas,
                    "tables": [
                        {
                            "name": t.name,
                            "schema": t.schema,
                            "columns": t.columns,
                            "primary_keys": t.primary_keys,
                            "row_count": t.row_count
                        }
                        for t in schema.tables
                    ],
                    "views": [
                        {
                            "name": v.name,
                            "schema": v.schema,
                            "columns": v.columns
                        }
                        for v in schema.views
                    ]
                }
            
            return ToolExecutionResult(
                success=True,
                data=data,
                metadata={
                    "connection_id": connection_id,
                    "table_count": len(schema.tables),
                    "view_count": len(schema.views)
                }
            )
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                data=None,
                error=f"Schema introspection failed: {str(e)}"
            )


class ConnectionTestTool(AgentTool):
    """Tool for testing database connections"""
    
    def __init__(self):
        super().__init__(
            name="connection_test",
            description="Test database connections for validity and reachability",
            version="1.0.0"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "connection_id": {
                    "type": "string",
                    "description": "The ID of the database connection to test"
                }
            },
            "required": ["connection_id"],
            "categories": ["database", "connection"]
        }
    
    async def execute(self, **kwargs) -> ToolExecutionResult:
        connection_id = kwargs.get("connection_id")
        
        if not connection_id:
            return ToolExecutionResult(
                success=False,
                data=None,
                error="Missing required parameter: connection_id"
            )
        
        try:
            connection = await db_manager.get_connection(connection_id)
            
            if not connection:
                return ToolExecutionResult(
                    success=False,
                    data=None,
                    error=f"Connection {connection_id} not found"
                )
            
            is_valid = await db_manager.test_connection(connection)
            
            return ToolExecutionResult(
                success=True,
                data={
                    "is_valid": is_valid,
                    "connection_id": connection_id,
                    "connection_name": connection.name,
                    "database_type": connection.type.value,
                    "host": connection.host,
                    "database": connection.database
                },
                metadata={
                    "status": "connected" if is_valid else "failed"
                }
            )
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                data=None,
                error=f"Connection test failed: {str(e)}"
            )
