"""
Database Connection Agent
Specialized AI agent for database connections and schema management using Gemini Flash (tiny recursive model)
"""

import os
import sys
from typing import Dict, Any, List, Optional
import asyncio
import google.generativeai as genai
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from database.connection_manager import db_manager, DatabaseConnection, DatabaseType
except ImportError:
    db_manager = None
    DatabaseConnection = None
    DatabaseType = None

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class DatabaseConnectionAgent:
    """
    AI Agent specialized in database connections and management
    Uses Gemini 1.5 Flash (tiny recursive model) for efficient processing
    """
    
    def __init__(self):
        self.agent_id = "db-agent-001"
        self.name = "Database Connection Agent"
        self.model_name = "gemini-1.5-flash"  # Tiny recursive model
        
        # Initialize the Gemini model
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            print(f"Warning: Could not initialize Gemini model: {e}")
            self.model = None
        
        self.capabilities = [
            "connect_to_databases",
            "manage_connections",
            "retrieve_schema",
            "execute_queries",
            "validate_connections",
            "suggest_optimizations"
        ]
        
        self.supported_databases = [
            "postgresql", "mysql", "sqlite", "mssql", "oracle",
            "mongodb", "snowflake", "bigquery", "redshift",
            "databricks", "clickhouse", "cassandra"
        ]
    
    async def connect_database(
        self, 
        name: str,
        db_type: str,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        ssl_enabled: bool = False,
        connection_string: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Connect to a database and register the connection
        """
        try:
            if not db_manager:
                return {
                    "status": "error",
                    "error": "Database manager not available",
                    "agent_id": self.agent_id
                }
            
            # Create connection object
            from database.connection_manager import DatabaseConnection, DatabaseType
            
            # Convert string type to enum
            try:
                db_type_enum = DatabaseType(db_type.lower())
            except ValueError:
                return {
                    "status": "error",
                    "error": f"Unsupported database type: {db_type}. Supported types: {self.supported_databases}",
                    "agent_id": self.agent_id
                }
            
            # Generate connection ID
            import uuid
            connection_id = str(uuid.uuid4())
            
            connection = DatabaseConnection(
                id=connection_id,
                name=name,
                type=db_type_enum,
                host=host,
                port=port,
                database=database,
                username=username,
                password=password,
                ssl_enabled=ssl_enabled,
                connection_string=connection_string,
                metadata=metadata or {}
            )
            
            # Add connection using the manager
            connection_id = await db_manager.add_connection(connection)
            
            # Generate AI insights about the connection
            insights = await self._generate_connection_insights(connection)
            
            return {
                "status": "success",
                "connection_id": connection_id,
                "message": f"Successfully connected to {name}",
                "insights": insights,
                "agent_id": self.agent_id
            }
        
        except ConnectionError as e:
            return {
                "status": "error",
                "error": f"Connection failed: {str(e)}",
                "agent_id": self.agent_id
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "agent_id": self.agent_id
            }
    
    async def list_connections(self) -> Dict[str, Any]:
        """
        List all available database connections
        """
        try:
            if not db_manager:
                return {
                    "status": "error",
                    "error": "Database manager not available",
                    "agent_id": self.agent_id
                }
            
            connections = await db_manager.list_connections()
            
            return {
                "status": "success",
                "connections": [
                    {
                        "id": conn.id,
                        "name": conn.name,
                        "type": conn.type.value,
                        "host": conn.host,
                        "port": conn.port,
                        "database": conn.database,
                        "is_active": conn.is_active
                    }
                    for conn in connections
                ],
                "count": len(connections),
                "agent_id": self.agent_id
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def get_connection_info(self, connection_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific connection
        """
        try:
            if not db_manager:
                return {
                    "status": "error",
                    "error": "Database manager not available",
                    "agent_id": self.agent_id
                }
            
            connection = await db_manager.get_connection(connection_id)
            if not connection:
                return {
                    "status": "error",
                    "error": f"Connection {connection_id} not found",
                    "agent_id": self.agent_id
                }
            
            return {
                "status": "success",
                "connection": {
                    "id": connection.id,
                    "name": connection.name,
                    "type": connection.type.value,
                    "host": connection.host,
                    "port": connection.port,
                    "database": connection.database,
                    "username": connection.username,
                    "ssl_enabled": connection.ssl_enabled,
                    "is_active": connection.is_active,
                    "created_at": connection.created_at.isoformat() if connection.created_at else None,
                    "metadata": connection.metadata
                },
                "agent_id": self.agent_id
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def test_connection(self, connection_id: str) -> Dict[str, Any]:
        """
        Test a database connection
        """
        try:
            if not db_manager:
                return {
                    "status": "error",
                    "error": "Database manager not available",
                    "agent_id": self.agent_id
                }
            
            connection = await db_manager.get_connection(connection_id)
            if not connection:
                return {
                    "status": "error",
                    "error": f"Connection {connection_id} not found",
                    "agent_id": self.agent_id
                }
            
            is_valid = await db_manager.test_connection(connection)
            
            return {
                "status": "success",
                "connection_id": connection_id,
                "is_valid": is_valid,
                "message": "Connection is valid" if is_valid else "Connection failed",
                "agent_id": self.agent_id
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def get_database_schema(
        self, 
        connection_id: str, 
        refresh: bool = False
    ) -> Dict[str, Any]:
        """
        Get database schema information with AI-powered insights
        """
        try:
            if not db_manager:
                return {
                    "status": "error",
                    "error": "Database manager not available",
                    "agent_id": self.agent_id
                }
            
            schema = await db_manager.get_database_schema(connection_id, refresh=refresh)
            if not schema:
                return {
                    "status": "error",
                    "error": f"Schema not available for connection {connection_id}",
                    "agent_id": self.agent_id
                }
            
            # Generate AI insights about the schema
            insights = await self._generate_schema_insights(schema)
            
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
                "insights": insights,
                "agent_id": self.agent_id
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def execute_query(
        self, 
        connection_id: str, 
        query: str, 
        limit: int = 1000
    ) -> Dict[str, Any]:
        """
        Execute a query on a database connection
        """
        try:
            if not db_manager:
                return {
                    "status": "error",
                    "error": "Database manager not available",
                    "agent_id": self.agent_id
                }
            
            result = await db_manager.execute_query(connection_id, query, limit)
            
            return {
                "status": "success",
                "connection_id": connection_id,
                "query": query,
                "result": result,
                "agent_id": self.agent_id
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def _generate_connection_insights(self, connection: Any) -> List[str]:
        """
        Generate AI-powered insights about the connection
        """
        if not self.model:
            return ["AI insights not available - Gemini API not configured"]
        
        try:
            prompt = f"""
            Analyze this database connection and provide 3-5 brief insights or recommendations:
            
            Database Type: {connection.type.value}
            Host: {connection.host}
            Port: {connection.port}
            Database: {connection.database}
            SSL Enabled: {connection.ssl_enabled}
            
            Provide practical insights about:
            1. Security considerations
            2. Performance optimization tips
            3. Best practices for this database type
            
            Format as a bullet point list with brief, actionable insights.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            # Parse response into list
            insights_text = response.text.strip()
            insights = [line.strip("- ").strip() for line in insights_text.split("\n") if line.strip()]
            
            return insights[:5]  # Return max 5 insights
        
        except Exception as e:
            print(f"Error generating insights: {e}")
            return [f"Connected to {connection.type.value} database successfully"]
    
    async def _generate_schema_insights(self, schema: Any) -> List[str]:
        """
        Generate AI-powered insights about the database schema
        """
        if not self.model:
            return ["AI insights not available - Gemini API not configured"]
        
        try:
            table_summary = "\n".join([
                f"- {table.name}: {len(table.columns)} columns, {table.row_count or 'unknown'} rows"
                for table in schema.tables[:10]  # Limit to first 10 tables
            ])
            
            prompt = f"""
            Analyze this database schema and provide 3-5 brief insights:
            
            Number of schemas: {len(schema.schemas)}
            Number of tables: {len(schema.tables)}
            
            Sample tables:
            {table_summary}
            
            Provide insights about:
            1. Schema organization
            2. Potential optimization opportunities
            3. Data modeling patterns observed
            
            Format as a bullet point list with brief insights.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            # Parse response into list
            insights_text = response.text.strip()
            insights = [line.strip("- ").strip() for line in insights_text.split("\n") if line.strip()]
            
            return insights[:5]  # Return max 5 insights
        
        except Exception as e:
            print(f"Error generating schema insights: {e}")
            return [f"Schema contains {len(schema.tables)} tables across {len(schema.schemas)} schemas"]
    
    async def suggest_query_optimization(self, query: str, connection_id: str) -> Dict[str, Any]:
        """
        Analyze a query and suggest optimizations using AI
        """
        if not self.model:
            return {
                "status": "error",
                "error": "AI model not available - Gemini API not configured",
                "agent_id": self.agent_id
            }
        
        try:
            # Get schema for context
            schema = await db_manager.get_database_schema(connection_id) if db_manager else None
            
            schema_context = ""
            if schema:
                schema_context = f"Available tables: {', '.join([t.name for t in schema.tables[:5]])}"
            
            prompt = f"""
            Analyze this SQL query and provide optimization suggestions:
            
            Query:
            {query}
            
            {schema_context}
            
            Provide:
            1. Potential performance issues
            2. Optimization suggestions
            3. Index recommendations (if applicable)
            4. Best practice improvements
            
            Format as a structured analysis with clear recommendations.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            return {
                "status": "success",
                "query": query,
                "analysis": response.text.strip(),
                "agent_id": self.agent_id
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "agent_id": self.agent_id
            }

# Global instance
database_agent = DatabaseConnectionAgent()
