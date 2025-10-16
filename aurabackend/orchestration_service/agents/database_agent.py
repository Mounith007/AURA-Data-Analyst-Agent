"""
Enhanced Database Agent
AI Agent with recursive reasoning and tool usage for database operations
"""

import os
from typing import Dict, List, Any, Optional
import google.generativeai as genai

from agent_tools.database_tool import DatabaseTool
from agent_tools.query_validator import QueryValidator
from agent_tools.schema_analyzer import SchemaAnalyzer
from agent_tools.recursive_reasoner import RecursiveReasoner


class DatabaseAgent:
    """
    Enhanced AI Agent for database operations with recursive reasoning
    Uses tiny recursive model approach for complex problem solving
    """
    
    def __init__(self, db_manager=None):
        # Initialize AI model
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
        
        # Initialize tools
        self.database_tool = DatabaseTool(db_manager)
        self.query_validator = QueryValidator()
        self.schema_analyzer = SchemaAnalyzer()
        self.recursive_reasoner = RecursiveReasoner(max_depth=3)
        
        self.agent_id = "database_agent_001"
        self.agent_type = "database_specialist"
        self.capabilities = [
            "database_connection",
            "query_generation",
            "schema_analysis",
            "recursive_reasoning",
            "query_validation"
        ]
    
    async def process_request(
        self,
        user_query: str,
        connection_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user request using recursive reasoning and tools
        
        Args:
            user_query: User's natural language query
            connection_id: Database connection identifier
            context: Additional context information
        
        Returns:
            Processing results with SQL query and insights
        """
        context = context or {}
        
        # Step 1: Use recursive reasoner to break down the problem
        reasoning_result = self.recursive_reasoner.reason(
            problem=user_query,
            context=context,
            max_depth=3
        )
        
        # Step 2: Get database schema if connection provided
        schema_context = {}
        if connection_id:
            schema_result = await self.database_tool.get_schema(
                connection_id=connection_id,
                include_samples=False
            )
            
            if schema_result.get("success"):
                schema_context = schema_result.get("schema", {})
                
                # Analyze schema
                schema_analysis = self.schema_analyzer.analyze_schema(schema_context)
                context["schema_analysis"] = schema_analysis
        
        # Step 3: Generate SQL query
        sql_query = await self._generate_sql_query(
            user_query=user_query,
            schema=schema_context,
            reasoning=reasoning_result
        )
        
        # Step 4: Validate the query
        validation_result = self.query_validator.validate_query(
            query=sql_query,
            allow_modifications=False
        )
        
        # Step 5: If query is invalid, attempt to fix it
        if not validation_result.get("is_valid"):
            sql_query = await self._fix_invalid_query(
                query=sql_query,
                validation=validation_result,
                schema=schema_context
            )
            
            # Validate again
            validation_result = self.query_validator.validate_query(
                query=sql_query,
                allow_modifications=False
            )
        
        return {
            "success": True,
            "agent_id": self.agent_id,
            "user_query": user_query,
            "sql_query": sql_query,
            "validation": validation_result,
            "reasoning": reasoning_result,
            "schema_insights": context.get("schema_analysis", {}),
            "confidence": self._calculate_overall_confidence(
                reasoning_result.get("confidence", 0),
                validation_result.get("security_score", 0) / 100
            )
        }
    
    async def _generate_sql_query(
        self,
        user_query: str,
        schema: Dict[str, Any],
        reasoning: Dict[str, Any]
    ) -> str:
        """
        Generate SQL query using AI model or fallback logic
        """
        if not self.model:
            return self._generate_fallback_query(user_query, schema)
        
        try:
            # Build context for AI model
            schema_description = self._format_schema_for_prompt(schema)
            reasoning_steps = reasoning.get("solution", "")
            
            prompt = f"""
            You are a database expert. Generate a SQL query based on the following:
            
            User Query: {user_query}
            
            Reasoning Steps:
            {reasoning_steps}
            
            Database Schema:
            {schema_description}
            
            Generate ONLY the SQL query, without any explanation or markdown formatting.
            The query should be optimized, secure, and follow best practices.
            """
            
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # Clean up the response
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            return sql_query
        
        except Exception as e:
            print(f"Error generating SQL with AI model: {e}")
            return self._generate_fallback_query(user_query, schema)
    
    def _generate_fallback_query(
        self,
        user_query: str,
        schema: Dict[str, Any]
    ) -> str:
        """
        Generate a basic SQL query without AI model
        """
        tables = schema.get("tables", [])
        
        if not tables:
            return "SELECT 1 as result;"
        
        # Get first table for simple query
        first_table = tables[0]
        table_name = f"{first_table.get('schema', 'public')}.{first_table.get('name', 'table')}"
        columns = first_table.get("columns", [])
        
        if columns:
            column_names = [col.get("name", "*") for col in columns[:5]]
            columns_str = ", ".join(column_names)
        else:
            columns_str = "*"
        
        query_lower = user_query.lower()
        
        # Simple pattern matching
        if "count" in query_lower or "how many" in query_lower:
            return f"SELECT COUNT(*) as total_count FROM {table_name} LIMIT 1000;"
        elif "top" in query_lower or "highest" in query_lower:
            return f"SELECT {columns_str} FROM {table_name} ORDER BY {column_names[0] if columns else 'id'} DESC LIMIT 10;"
        elif "recent" in query_lower or "latest" in query_lower:
            date_col = next((col.get("name") for col in columns if "date" in col.get("name", "").lower()), None)
            if date_col:
                return f"SELECT {columns_str} FROM {table_name} ORDER BY {date_col} DESC LIMIT 10;"
        
        return f"SELECT {columns_str} FROM {table_name} LIMIT 10;"
    
    async def _fix_invalid_query(
        self,
        query: str,
        validation: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> str:
        """
        Attempt to fix an invalid query
        """
        errors = validation.get("errors", [])
        
        if not errors:
            return query
        
        # Sanitize the query first
        sanitized = self.query_validator.sanitize_query(query)
        fixed_query = sanitized.get("sanitized_query", query)
        
        # Apply simple fixes
        if "Dangerous operation detected" in str(errors):
            # Remove dangerous operations
            fixed_query = fixed_query.replace("DROP", "-- DROP")
            fixed_query = fixed_query.replace("TRUNCATE", "-- TRUNCATE")
        
        if "Unbalanced parentheses" in str(errors):
            # Try to balance parentheses
            open_count = fixed_query.count("(")
            close_count = fixed_query.count(")")
            if open_count > close_count:
                fixed_query += ")" * (open_count - close_count)
        
        return fixed_query
    
    def _format_schema_for_prompt(self, schema: Dict[str, Any]) -> str:
        """
        Format schema information for AI prompt
        """
        if not schema:
            return "No schema information available"
        
        tables = schema.get("tables", [])
        
        if not tables:
            return "No tables found in schema"
        
        schema_lines = []
        
        for table in tables[:5]:  # Limit to first 5 tables
            table_name = f"{table.get('schema', 'public')}.{table.get('name', 'unknown')}"
            columns = table.get("columns", [])
            
            schema_lines.append(f"\nTable: {table_name}")
            schema_lines.append("Columns:")
            
            for col in columns[:10]:  # Limit to first 10 columns
                col_name = col.get("name", "unknown")
                col_type = col.get("type", "unknown")
                nullable = "NULL" if col.get("nullable", True) else "NOT NULL"
                schema_lines.append(f"  - {col_name} ({col_type}) {nullable}")
        
        return "\n".join(schema_lines)
    
    def _calculate_overall_confidence(
        self,
        reasoning_confidence: float,
        validation_score: float
    ) -> float:
        """
        Calculate overall confidence score
        """
        # Weighted average: reasoning 60%, validation 40%
        return (reasoning_confidence * 0.6) + (validation_score * 0.4)
    
    async def analyze_database(
        self,
        connection_id: str
    ) -> Dict[str, Any]:
        """
        Perform comprehensive database analysis
        
        Args:
            connection_id: Database connection identifier
        
        Returns:
            Analysis results
        """
        # Get schema
        schema_result = await self.database_tool.get_schema(
            connection_id=connection_id,
            refresh=True,
            include_samples=True
        )
        
        if not schema_result.get("success"):
            return {
                "success": False,
                "error": schema_result.get("error", "Failed to get schema")
            }
        
        schema = schema_result.get("schema", {})
        
        # Analyze schema
        schema_analysis = self.schema_analyzer.analyze_schema(schema)
        
        # Find relationships
        relationships = self.schema_analyzer.find_relationships(schema)
        
        # Test connection
        connection_test = await self.database_tool.test_connection(connection_id)
        
        return {
            "success": True,
            "connection_id": connection_id,
            "connection_status": connection_test,
            "schema_analysis": schema_analysis,
            "relationships": relationships,
            "recommendations": schema_analysis.get("recommendations", [])
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get agent information and capabilities
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "capabilities": self.capabilities,
            "tools": [
                self.database_tool.get_tool_definition(),
                self.query_validator.get_tool_definition(),
                self.schema_analyzer.get_tool_definition(),
                self.recursive_reasoner.get_tool_definition()
            ],
            "status": "ready",
            "model_available": self.model is not None
        }
