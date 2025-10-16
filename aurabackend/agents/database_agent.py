"""
Database Agent
AI agent specialized in database operations and schema analysis
Uses tiny recursive model to break down complex database tasks
"""

import sys
import os
from typing import Any, Dict, List, Optional
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent, AgentTask, AgentStatus
from agent_tools.base_tool import global_tool_registry
from agent_tools.database_tools import (
    DatabaseQueryTool,
    SchemaIntrospectionTool,
    ConnectionTestTool
)
from database.connection_manager import db_manager


class DatabaseAgent(BaseAgent):
    """
    Database Agent for intelligent database operations
    
    Features:
    - Connection management and testing
    - Schema analysis and recommendations
    - Query generation and optimization
    - Tiny recursive task decomposition
    """
    
    def __init__(self, agent_id: str = None):
        if agent_id is None:
            import uuid
            agent_id = f"db_agent_{str(uuid.uuid4())[:8]}"
        
        super().__init__(
            agent_id=agent_id,
            agent_type="database",
            name="Database Agent",
            description="AI agent for database connection and schema analysis",
            version="1.0.0"
        )
        
        self.llm_model = None  # Placeholder for tiny recursive model
        self.connection_cache = {}
    
    async def initialize(self):
        """Initialize the database agent"""
        # Register database tools
        query_tool = DatabaseQueryTool()
        schema_tool = SchemaIntrospectionTool()
        connection_tool = ConnectionTestTool()
        
        global_tool_registry.register(query_tool)
        global_tool_registry.register(schema_tool)
        global_tool_registry.register(connection_tool)
        
        self.tools = [
            query_tool.name,
            schema_tool.name,
            connection_tool.name
        ]
        
        self.metadata["tools_loaded"] = True
        self.metadata["model_type"] = "tiny_recursive"
    
    async def execute_task(self, task: AgentTask) -> AgentTask:
        """
        Execute a database task
        Uses tiny recursive model to break down complex tasks
        """
        task_type = task.task_type
        
        # Route to appropriate handler
        if task_type == "test_connection":
            return await self._test_connection(task)
        elif task_type == "analyze_schema":
            return await self._analyze_schema(task)
        elif task_type == "execute_query":
            return await self._execute_query(task)
        elif task_type == "recommend_optimizations":
            return await self._recommend_optimizations(task)
        elif task_type == "validate_connection":
            return await self._validate_connection(task)
        else:
            task.error = f"Unknown task type: {task_type}"
            task.status = AgentStatus.FAILED
            return task
    
    async def should_decompose(self, task: AgentTask) -> bool:
        """
        Determine if task should be decomposed using tiny recursive model
        """
        # Complex tasks that benefit from decomposition
        complex_tasks = [
            "analyze_schema",
            "recommend_optimizations",
            "validate_connection"
        ]
        
        # Check if task is complex and has parameters indicating depth
        if task.task_type in complex_tasks:
            # If task has many parameters or deep analysis requested
            param_count = len(task.parameters)
            deep_analysis = task.parameters.get("deep_analysis", False)
            
            return param_count > 3 or deep_analysis
        
        return False
    
    async def decompose_task(self, task: AgentTask) -> List[AgentTask]:
        """
        Decompose task into subtasks using tiny recursive model
        """
        subtasks = []
        
        if task.task_type == "analyze_schema":
            # Break down into: connection test, schema fetch, analysis
            connection_id = task.parameters.get("connection_id")
            
            subtasks.append(AgentTask(
                task_id=f"{task.task_id}_test",
                task_type="test_connection",
                description="Test database connection",
                parameters={"connection_id": connection_id}
            ))
            
            subtasks.append(AgentTask(
                task_id=f"{task.task_id}_schema",
                task_type="fetch_schema",
                description="Fetch database schema",
                parameters={
                    "connection_id": connection_id,
                    "refresh": task.parameters.get("refresh", False)
                }
            ))
            
            subtasks.append(AgentTask(
                task_id=f"{task.task_id}_analyze",
                task_type="analyze_structure",
                description="Analyze schema structure",
                parameters={"connection_id": connection_id}
            ))
        
        elif task.task_type == "validate_connection":
            # Break down into: basic test, schema check, query test
            connection_id = task.parameters.get("connection_id")
            
            subtasks.append(AgentTask(
                task_id=f"{task.task_id}_basic",
                task_type="test_connection",
                description="Basic connection test",
                parameters={"connection_id": connection_id}
            ))
            
            subtasks.append(AgentTask(
                task_id=f"{task.task_id}_query",
                task_type="execute_query",
                description="Test query execution",
                parameters={
                    "connection_id": connection_id,
                    "query": "SELECT 1 as test",
                    "limit": 1
                }
            ))
        
        return subtasks if subtasks else [task]
    
    async def _test_connection(self, task: AgentTask) -> AgentTask:
        """Test a database connection"""
        connection_id = task.parameters.get("connection_id")
        
        if not connection_id:
            task.error = "Missing connection_id parameter"
            task.status = AgentStatus.FAILED
            return task
        
        # Use connection test tool
        result = await global_tool_registry.execute_tool(
            "connection_test",
            connection_id=connection_id
        )
        
        if result.success:
            task.result = result.data
            task.status = AgentStatus.COMPLETED
        else:
            task.error = result.error
            task.status = AgentStatus.FAILED
        
        return task
    
    async def _analyze_schema(self, task: AgentTask) -> AgentTask:
        """Analyze database schema"""
        connection_id = task.parameters.get("connection_id")
        refresh = task.parameters.get("refresh", False)
        
        if not connection_id:
            task.error = "Missing connection_id parameter"
            task.status = AgentStatus.FAILED
            return task
        
        # Use schema introspection tool
        result = await global_tool_registry.execute_tool(
            "schema_introspection",
            connection_id=connection_id,
            refresh=refresh
        )
        
        if result.success:
            schema_data = result.data
            
            # Perform analysis
            analysis = {
                "schema_data": schema_data,
                "insights": await self._generate_schema_insights(schema_data),
                "recommendations": await self._generate_recommendations(schema_data)
            }
            
            task.result = analysis
            task.status = AgentStatus.COMPLETED
        else:
            task.error = result.error
            task.status = AgentStatus.FAILED
        
        return task
    
    async def _execute_query(self, task: AgentTask) -> AgentTask:
        """Execute a database query"""
        connection_id = task.parameters.get("connection_id")
        query = task.parameters.get("query")
        limit = task.parameters.get("limit", 1000)
        
        if not connection_id or not query:
            task.error = "Missing required parameters: connection_id and query"
            task.status = AgentStatus.FAILED
            return task
        
        # Use database query tool
        result = await global_tool_registry.execute_tool(
            "database_query",
            connection_id=connection_id,
            query=query,
            limit=limit
        )
        
        if result.success:
            task.result = result.data
            task.status = AgentStatus.COMPLETED
        else:
            task.error = result.error
            task.status = AgentStatus.FAILED
        
        return task
    
    async def _recommend_optimizations(self, task: AgentTask) -> AgentTask:
        """Recommend database optimizations"""
        connection_id = task.parameters.get("connection_id")
        
        # First, analyze the schema
        schema_result = await global_tool_registry.execute_tool(
            "schema_introspection",
            connection_id=connection_id
        )
        
        if not schema_result.success:
            task.error = schema_result.error
            task.status = AgentStatus.FAILED
            return task
        
        schema_data = schema_result.data
        
        # Generate optimization recommendations
        recommendations = []
        
        # Check for missing indexes
        for table in schema_data.get("tables", []):
            if not table.get("primary_keys"):
                recommendations.append({
                    "type": "missing_primary_key",
                    "table": table["name"],
                    "severity": "high",
                    "recommendation": f"Add a primary key to table {table['name']}"
                })
            
            # Check for large tables without indexes
            if table.get("row_count", 0) > 10000 and len(table.get("indexes", [])) == 0:
                recommendations.append({
                    "type": "missing_indexes",
                    "table": table["name"],
                    "severity": "medium",
                    "recommendation": f"Consider adding indexes to table {table['name']} for better query performance"
                })
        
        task.result = {
            "recommendations": recommendations,
            "schema_summary": {
                "table_count": len(schema_data.get("tables", [])),
                "view_count": len(schema_data.get("views", []))
            }
        }
        task.status = AgentStatus.COMPLETED
        
        return task
    
    async def _validate_connection(self, task: AgentTask) -> AgentTask:
        """Comprehensive connection validation"""
        connection_id = task.parameters.get("connection_id")
        
        # Decompose into subtasks if needed
        if await self.should_decompose(task):
            subtasks = await self.decompose_task(task)
            
            # Execute subtasks
            results = []
            for subtask in subtasks:
                result = await self.execute_task(subtask)
                results.append(result)
            
            # Aggregate results
            all_passed = all(r.status == AgentStatus.COMPLETED for r in results)
            
            task.result = {
                "validation_passed": all_passed,
                "subtask_results": [
                    {
                        "task_type": r.task_type,
                        "status": r.status.value,
                        "result": r.result
                    }
                    for r in results
                ]
            }
            task.status = AgentStatus.COMPLETED if all_passed else AgentStatus.FAILED
        else:
            # Simple validation
            test_result = await self._test_connection(AgentTask(
                task_id=f"{task.task_id}_simple",
                task_type="test_connection",
                description="Simple connection test",
                parameters={"connection_id": connection_id}
            ))
            
            task.result = test_result.result
            task.status = test_result.status
        
        return task
    
    async def _generate_schema_insights(self, schema_data: Dict[str, Any]) -> List[str]:
        """Generate insights about schema using tiny recursive analysis"""
        insights = []
        
        table_count = len(schema_data.get("tables", []))
        view_count = len(schema_data.get("views", []))
        
        insights.append(f"Database contains {table_count} tables and {view_count} views")
        
        # Analyze relationships
        total_foreign_keys = sum(
            len(table.get("foreign_keys", []))
            for table in schema_data.get("tables", [])
        )
        
        if total_foreign_keys > 0:
            insights.append(f"Found {total_foreign_keys} foreign key relationships")
        else:
            insights.append("No foreign key relationships detected - consider adding for data integrity")
        
        # Analyze data volume
        total_rows = sum(
            table.get("row_count", 0)
            for table in schema_data.get("tables", [])
        )
        
        if total_rows > 1000000:
            insights.append(f"Large dataset detected ({total_rows:,} total rows) - consider partitioning strategies")
        
        return insights
    
    async def _generate_recommendations(self, schema_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on schema analysis"""
        recommendations = []
        
        for table in schema_data.get("tables", []):
            # Check for timestamp columns
            has_timestamp = any(
                "timestamp" in col.get("type", "").lower() or "date" in col.get("type", "").lower()
                for col in table.get("columns", [])
            )
            
            if not has_timestamp:
                recommendations.append(
                    f"Consider adding timestamp columns (created_at, updated_at) to table {table['name']}"
                )
            
            # Check for very wide tables
            if len(table.get("columns", [])) > 30:
                recommendations.append(
                    f"Table {table['name']} has {len(table['columns'])} columns - consider normalization"
                )
        
        return recommendations
