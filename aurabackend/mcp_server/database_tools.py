"""
Database Tools Integration
Connects MCP tool registry with actual database service implementations
"""

import os
import sys
import httpx
from typing import Dict, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection_manager import db_manager

class DatabaseTools:
    """Integration layer between tool registry and database service"""
    
    def __init__(self):
        self.db_service_url = os.getenv("DATABASE_SERVICE_URL", "http://localhost:8002")
        self.timeout = httpx.Timeout(30.0)
    
    async def connect_database_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for database connection - integrates with actual DB service"""
        try:
            connection_id = parameters.get("connection_id")
            if not connection_id:
                raise ValueError("connection_id is required")
            
            # Use the database manager directly
            connection = await db_manager.get_connection(connection_id)
            if not connection:
                return {
                    "status": "error",
                    "error": f"Connection {connection_id} not found"
                }
            
            # Test the connection
            is_valid = await db_manager.test_connection(connection)
            
            return {
                "status": "connected" if is_valid else "failed",
                "connection_id": connection_id,
                "connection_name": connection.name,
                "database_type": connection.type.value,
                "is_valid": is_valid
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def list_database_connections_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for listing database connections"""
        try:
            connections = await db_manager.list_connections()
            
            return {
                "status": "success",
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
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def query_database_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for database queries"""
        try:
            connection_id = parameters.get("connection_id")
            query = parameters.get("query")
            limit = parameters.get("limit", 1000)
            
            if not connection_id or not query:
                raise ValueError("connection_id and query are required")
            
            result = await db_manager.execute_query(connection_id, query, limit)
            
            return {
                "status": "success",
                "connection_id": connection_id,
                "query": query,
                "result": result
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_database_schema_handler(self, parameters: Dict[str, Any]) -> Any:
        """Handler for getting database schema"""
        try:
            connection_id = parameters.get("connection_id")
            refresh = parameters.get("refresh", False)
            
            if not connection_id:
                raise ValueError("connection_id is required")
            
            schema = await db_manager.get_database_schema(connection_id, refresh=refresh)
            
            if not schema:
                return {
                    "status": "error",
                    "error": f"Schema not available for connection {connection_id}"
                }
            
            return {
                "status": "success",
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
                "table_count": len(schema.tables)
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

# Global instance
database_tools = DatabaseTools()
