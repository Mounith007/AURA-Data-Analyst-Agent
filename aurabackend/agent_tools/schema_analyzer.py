"""
Schema Analyzer Tool
Analyzes database schemas and suggests optimal query strategies
"""

from typing import Dict, List, Any, Optional


class SchemaAnalyzer:
    """Tool for analyzing database schemas"""
    
    def __init__(self):
        self.tool_name = "schema_analyzer"
        self.tool_description = "Analyze database schemas and suggest optimal query strategies"
    
    def analyze_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze database schema and provide insights
        
        Args:
            schema: Database schema information
        
        Returns:
            Analysis results with insights and recommendations
        """
        insights = []
        recommendations = []
        statistics = {}
        
        tables = schema.get("tables", [])
        views = schema.get("views", [])
        
        # Basic statistics
        statistics["total_tables"] = len(tables)
        statistics["total_views"] = len(views)
        statistics["total_columns"] = sum(len(t.get("columns", [])) for t in tables)
        
        # Analyze tables
        large_tables = []
        tables_without_pk = []
        tables_with_many_columns = []
        
        for table in tables:
            table_name = f"{table.get('schema', 'public')}.{table.get('name', 'unknown')}"
            columns = table.get("columns", [])
            primary_keys = table.get("primary_keys", [])
            row_count = table.get("row_count", 0)
            
            # Check for large tables
            if row_count and row_count > 100000:
                large_tables.append({
                    "table": table_name,
                    "rows": row_count
                })
            
            # Check for tables without primary keys
            if not primary_keys:
                tables_without_pk.append(table_name)
            
            # Check for tables with many columns
            if len(columns) > 30:
                tables_with_many_columns.append({
                    "table": table_name,
                    "columns": len(columns)
                })
        
        # Generate insights
        if large_tables:
            insights.append({
                "type": "performance",
                "message": f"Found {len(large_tables)} large tables that may benefit from indexing",
                "details": large_tables[:5]  # Show top 5
            })
            recommendations.append(
                "Consider using LIMIT clauses when querying large tables"
            )
        
        if tables_without_pk:
            insights.append({
                "type": "schema_quality",
                "message": f"Found {len(tables_without_pk)} tables without primary keys",
                "details": tables_without_pk[:5]
            })
            recommendations.append(
                "Tables without primary keys may cause performance issues"
            )
        
        if tables_with_many_columns:
            insights.append({
                "type": "schema_design",
                "message": f"Found {len(tables_with_many_columns)} tables with many columns",
                "details": tables_with_many_columns[:5]
            })
            recommendations.append(
                "SELECT only required columns instead of SELECT * for wide tables"
            )
        
        return {
            "statistics": statistics,
            "insights": insights,
            "recommendations": recommendations,
            "quality_score": self._calculate_quality_score(
                len(tables_without_pk),
                len(tables),
                len(large_tables)
            )
        }
    
    def suggest_indexes(
        self,
        table_schema: Dict[str, Any],
        common_queries: List[str]
    ) -> Dict[str, Any]:
        """
        Suggest indexes based on table schema and common query patterns
        
        Args:
            table_schema: Table schema information
            common_queries: List of common queries on this table
        
        Returns:
            Index suggestions
        """
        suggestions = []
        
        columns = table_schema.get("columns", [])
        existing_indexes = table_schema.get("indexes", [])
        
        # Analyze columns for index candidates
        for column in columns:
            col_name = column.get("name", "")
            col_type = column.get("type", "")
            
            # Check if column is already indexed
            is_indexed = any(
                col_name in idx.get("columns", [])
                for idx in existing_indexes
            )
            
            if not is_indexed:
                # Suggest indexes for foreign keys
                if "id" in col_name.lower() and col_name != "id":
                    suggestions.append({
                        "column": col_name,
                        "type": "single_column",
                        "reason": "Appears to be a foreign key",
                        "priority": "high"
                    })
                
                # Suggest indexes for date/timestamp columns
                if any(t in col_type.lower() for t in ["date", "timestamp", "time"]):
                    suggestions.append({
                        "column": col_name,
                        "type": "single_column",
                        "reason": "Date columns are often used in WHERE and ORDER BY",
                        "priority": "medium"
                    })
                
                # Suggest indexes for string columns that might be used in searches
                if "varchar" in col_type.lower() or "text" in col_type.lower():
                    if any(keyword in col_name.lower() for keyword in ["email", "name", "code"]):
                        suggestions.append({
                            "column": col_name,
                            "type": "single_column",
                            "reason": "Commonly searched string column",
                            "priority": "medium"
                        })
        
        return {
            "table": table_schema.get("name", "unknown"),
            "existing_indexes": len(existing_indexes),
            "suggestions": suggestions,
            "total_suggestions": len(suggestions)
        }
    
    def find_relationships(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find relationships between tables based on column names and foreign keys
        
        Args:
            schema: Database schema information
        
        Returns:
            Discovered relationships
        """
        relationships = []
        tables = schema.get("tables", [])
        
        # Build a map of tables and their columns
        table_map = {}
        for table in tables:
            table_name = table.get("name", "")
            columns = [col.get("name", "") for col in table.get("columns", [])]
            foreign_keys = table.get("foreign_keys", [])
            
            table_map[table_name] = {
                "columns": columns,
                "foreign_keys": foreign_keys
            }
        
        # Find explicit foreign keys
        for table_name, table_info in table_map.items():
            for fk in table_info.get("foreign_keys", []):
                relationships.append({
                    "type": "explicit",
                    "from_table": table_name,
                    "from_column": fk.get("column", ""),
                    "to_table": fk.get("referenced_table", ""),
                    "to_column": fk.get("referenced_column", ""),
                    "confidence": "high"
                })
        
        # Find implicit relationships based on naming patterns
        for table_name, table_info in table_map.items():
            for column in table_info.get("columns", []):
                # Look for columns ending with _id
                if column.endswith("_id") and column != "id":
                    potential_table = column[:-3]  # Remove _id suffix
                    
                    # Check if a table with this name exists
                    if potential_table in table_map:
                        # Check if this relationship is not already explicit
                        is_explicit = any(
                            r["from_table"] == table_name and
                            r["from_column"] == column and
                            r["to_table"] == potential_table
                            for r in relationships
                        )
                        
                        if not is_explicit:
                            relationships.append({
                                "type": "implicit",
                                "from_table": table_name,
                                "from_column": column,
                                "to_table": potential_table,
                                "to_column": "id",
                                "confidence": "medium"
                            })
        
        return {
            "total_relationships": len(relationships),
            "explicit_relationships": len([r for r in relationships if r["type"] == "explicit"]),
            "implicit_relationships": len([r for r in relationships if r["type"] == "implicit"]),
            "relationships": relationships
        }
    
    def _calculate_quality_score(
        self,
        tables_without_pk: int,
        total_tables: int,
        large_tables: int
    ) -> float:
        """Calculate schema quality score (0-100)"""
        if total_tables == 0:
            return 0.0
        
        score = 100.0
        
        # Deduct points for tables without primary keys
        pk_ratio = tables_without_pk / total_tables
        score -= pk_ratio * 40
        
        # Deduct points for many large tables (potential performance issues)
        large_table_ratio = large_tables / total_tables
        if large_table_ratio > 0.5:
            score -= 20
        
        return max(0.0, min(100.0, score))
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for agent use"""
        return {
            "name": self.tool_name,
            "description": self.tool_description,
            "operations": [
                {
                    "name": "analyze_schema",
                    "description": "Analyze database schema and provide insights",
                    "parameters": {
                        "schema": "object (required) - Schema information"
                    }
                },
                {
                    "name": "suggest_indexes",
                    "description": "Suggest indexes for a table",
                    "parameters": {
                        "table_schema": "object (required) - Table schema",
                        "common_queries": "array (optional) - Common queries"
                    }
                },
                {
                    "name": "find_relationships",
                    "description": "Find relationships between tables",
                    "parameters": {
                        "schema": "object (required) - Schema information"
                    }
                }
            ]
        }
