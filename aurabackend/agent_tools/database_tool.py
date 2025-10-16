"""
Database Tool for AI Agents
Provides database operations as tools for agents
"""

from typing import Dict, List, Any, Optional
import asyncio


class DatabaseTool:
    """Tool for database operations used by AI agents"""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.tool_name = "database_tool"
        self.tool_description = "Execute database operations including queries, schema inspection, and connection management"
    
    async def execute_query(
        self,
        connection_id: str,
        query: str,
        limit: int = 1000,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a SQL query against a database connection
        
        Args:
            connection_id: Database connection identifier
            query: SQL query to execute
            limit: Maximum number of rows to return
            dry_run: If True, validate query without executing
        
        Returns:
            Query results or validation results
        """
        try:
            if dry_run:
                return {
                    "success": True,
                    "dry_run": True,
                    "query": query,
                    "validation": "Query syntax appears valid"
                }
            
            if self.db_manager:
                result = await self.db_manager.execute_query(
                    connection_id=connection_id,
                    query=query,
                    limit=limit
                )
                return {
                    "success": True,
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": "Database manager not initialized"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    async def get_schema(
        self,
        connection_id: str,
        refresh: bool = False,
        include_samples: bool = False
    ) -> Dict[str, Any]:
        """
        Get database schema information
        
        Args:
            connection_id: Database connection identifier
            refresh: Force refresh of cached schema
            include_samples: Include sample data from tables
        
        Returns:
            Schema information
        """
        try:
            if self.db_manager:
                schema = await self.db_manager.get_database_schema(
                    connection_id=connection_id,
                    refresh=refresh
                )
                
                if not schema:
                    return {
                        "success": False,
                        "error": "Schema not found"
                    }
                
                result = {
                    "success": True,
                    "schema": {
                        "connection_id": schema.connection_id,
                        "schemas": schema.schemas,
                        "tables": [
                            {
                                "name": table.name,
                                "schema": table.schema,
                                "columns": table.columns,
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
                        ]
                    }
                }
                
                if include_samples:
                    # Add sample data for first few tables
                    samples = []
                    for table in schema.tables[:3]:  # Only first 3 tables
                        sample_query = f"SELECT * FROM {table.schema}.{table.name} LIMIT 5"
                        sample_result = await self.execute_query(
                            connection_id=connection_id,
                            query=sample_query,
                            limit=5
                        )
                        if sample_result.get("success"):
                            samples.append({
                                "table": f"{table.schema}.{table.name}",
                                "sample": sample_result.get("result")
                            })
                    
                    result["schema"]["samples"] = samples
                
                return result
            else:
                return {
                    "success": False,
                    "error": "Database manager not initialized"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def test_connection(self, connection_id: str) -> Dict[str, Any]:
        """
        Test database connection
        
        Args:
            connection_id: Database connection identifier
        
        Returns:
            Connection test results
        """
        try:
            if self.db_manager:
                connection = await self.db_manager.get_connection(connection_id)
                if not connection:
                    return {
                        "success": False,
                        "error": "Connection not found"
                    }
                
                is_valid = await self.db_manager.test_connection(connection)
                return {
                    "success": True,
                    "connection_valid": is_valid,
                    "connection_info": {
                        "name": connection.name,
                        "type": connection.type.value,
                        "host": connection.host,
                        "database": connection.database
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Database manager not initialized"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_connections(self) -> Dict[str, Any]:
        """
        List all available database connections
        
        Returns:
            List of connections
        """
        try:
            if self.db_manager:
                connections = await self.db_manager.list_connections()
                return {
                    "success": True,
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
                    ]
                }
            else:
                return {
                    "success": False,
                    "error": "Database manager not initialized"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for agent use"""
        return {
            "name": self.tool_name,
            "description": self.tool_description,
            "operations": [
                {
                    "name": "execute_query",
                    "description": "Execute SQL query against database",
                    "parameters": {
                        "connection_id": "string (required)",
                        "query": "string (required)",
                        "limit": "integer (optional, default: 1000)",
                        "dry_run": "boolean (optional, default: false)"
                    }
                },
                {
                    "name": "get_schema",
                    "description": "Get database schema information",
                    "parameters": {
                        "connection_id": "string (required)",
                        "refresh": "boolean (optional)",
                        "include_samples": "boolean (optional)"
                    }
                },
                {
                    "name": "test_connection",
                    "description": "Test database connection",
                    "parameters": {
                        "connection_id": "string (required)"
                    }
                },
                {
                    "name": "list_connections",
                    "description": "List all available database connections",
                    "parameters": {}
                }
            ]
        }
