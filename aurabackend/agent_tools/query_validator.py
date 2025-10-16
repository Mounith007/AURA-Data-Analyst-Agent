"""
Query Validator Tool
Validates SQL queries for security and correctness
"""

from typing import Dict, List, Any, Optional
import re


class QueryValidator:
    """Tool for validating SQL queries"""
    
    def __init__(self):
        self.tool_name = "query_validator"
        self.tool_description = "Validate SQL queries for security vulnerabilities and syntax correctness"
        
        # Dangerous SQL patterns
        self.dangerous_patterns = [
            r'\bDROP\s+TABLE\b',
            r'\bDROP\s+DATABASE\b',
            r'\bTRUNCATE\b',
            r'\bDELETE\s+FROM\b.*\bWHERE\s+1\s*=\s*1\b',
            r'\bEXEC\s*\(',
            r'\bEXECUTE\s*\(',
            r';\s*DROP\b',
            r'--\s*DROP\b',
            r'/\*.*DROP.*\*/',
        ]
        
        # Suspicious patterns (SQL injection attempts)
        self.suspicious_patterns = [
            r"'\s*OR\s+'1'\s*=\s*'1",
            r"'\s*OR\s+1\s*=\s*1",
            r"'\s*;\s*--",
            r"'\s*UNION\s+SELECT",
            r"'\s*AND\s+'1'\s*=\s*'1",
        ]
    
    def validate_query(
        self,
        query: str,
        allow_modifications: bool = False,
        allow_drops: bool = False
    ) -> Dict[str, Any]:
        """
        Validate SQL query for security and correctness
        
        Args:
            query: SQL query to validate
            allow_modifications: Allow INSERT, UPDATE, DELETE operations
            allow_drops: Allow DROP operations (dangerous)
        
        Returns:
            Validation results with warnings and errors
        """
        errors = []
        warnings = []
        suggestions = []
        
        if not query or not query.strip():
            return {
                "is_valid": False,
                "errors": ["Query is empty"],
                "warnings": [],
                "suggestions": []
            }
        
        query_upper = query.upper()
        
        # Check for dangerous patterns
        if not allow_drops:
            for pattern in self.dangerous_patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    errors.append(f"Dangerous operation detected: {pattern}")
        
        # Check for suspicious patterns (SQL injection)
        for pattern in self.suspicious_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                warnings.append(f"Suspicious pattern detected (possible SQL injection): {pattern}")
        
        # Check for modification operations
        modification_keywords = ['INSERT', 'UPDATE', 'DELETE', 'MERGE']
        if not allow_modifications:
            for keyword in modification_keywords:
                if re.search(rf'\b{keyword}\b', query, re.IGNORECASE):
                    errors.append(f"Modification operation '{keyword}' not allowed")
        
        # Check for multiple statements (potential SQL injection)
        semicolon_count = query.count(';')
        if semicolon_count > 1:
            warnings.append("Multiple SQL statements detected - ensure this is intentional")
        
        # Check for missing WHERE clause in UPDATE/DELETE
        if re.search(r'\bUPDATE\b', query, re.IGNORECASE):
            if not re.search(r'\bWHERE\b', query, re.IGNORECASE):
                warnings.append("UPDATE without WHERE clause - will affect all rows")
        
        if re.search(r'\bDELETE\s+FROM\b', query, re.IGNORECASE):
            if not re.search(r'\bWHERE\b', query, re.IGNORECASE):
                warnings.append("DELETE without WHERE clause - will delete all rows")
        
        # Check for SELECT *
        if re.search(r'\bSELECT\s+\*\b', query, re.IGNORECASE):
            suggestions.append("Consider specifying column names instead of SELECT *")
        
        # Check for missing LIMIT in SELECT
        if re.search(r'\bSELECT\b', query, re.IGNORECASE):
            if not re.search(r'\bLIMIT\b', query, re.IGNORECASE):
                suggestions.append("Consider adding LIMIT clause to prevent large result sets")
        
        # Basic syntax checks
        if query_upper.count('(') != query_upper.count(')'):
            errors.append("Unbalanced parentheses")
        
        if query_upper.count("'") % 2 != 0:
            warnings.append("Unmatched single quotes - check string literals")
        
        is_valid = len(errors) == 0
        
        return {
            "is_valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions,
            "query_type": self._detect_query_type(query),
            "security_score": self._calculate_security_score(errors, warnings)
        }
    
    def _detect_query_type(self, query: str) -> str:
        """Detect the type of SQL query"""
        query_upper = query.upper().strip()
        
        if query_upper.startswith('SELECT'):
            return "SELECT"
        elif query_upper.startswith('INSERT'):
            return "INSERT"
        elif query_upper.startswith('UPDATE'):
            return "UPDATE"
        elif query_upper.startswith('DELETE'):
            return "DELETE"
        elif query_upper.startswith('CREATE'):
            return "CREATE"
        elif query_upper.startswith('ALTER'):
            return "ALTER"
        elif query_upper.startswith('DROP'):
            return "DROP"
        else:
            return "UNKNOWN"
    
    def _calculate_security_score(self, errors: List[str], warnings: List[str]) -> float:
        """Calculate security score (0-100, higher is better)"""
        score = 100.0
        
        # Deduct points for errors and warnings
        score -= len(errors) * 30  # Major deduction for errors
        score -= len(warnings) * 10  # Minor deduction for warnings
        
        return max(0.0, min(100.0, score))
    
    def sanitize_query(self, query: str) -> Dict[str, Any]:
        """
        Attempt to sanitize a query by removing dangerous elements
        
        Args:
            query: SQL query to sanitize
        
        Returns:
            Sanitized query and changes made
        """
        original_query = query
        changes = []
        
        # Remove SQL comments that might hide malicious code
        if '--' in query:
            query = re.sub(r'--[^\n]*', '', query)
            changes.append("Removed SQL comments")
        
        if '/*' in query:
            query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
            changes.append("Removed block comments")
        
        # Remove trailing semicolons (except the last one)
        semicolons = query.count(';')
        if semicolons > 1:
            query = query.replace(';', ' ', semicolons - 1)
            changes.append("Removed multiple statement separators")
        
        return {
            "original_query": original_query,
            "sanitized_query": query.strip(),
            "changes": changes,
            "was_modified": len(changes) > 0
        }
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for agent use"""
        return {
            "name": self.tool_name,
            "description": self.tool_description,
            "operations": [
                {
                    "name": "validate_query",
                    "description": "Validate SQL query for security and correctness",
                    "parameters": {
                        "query": "string (required)",
                        "allow_modifications": "boolean (optional)",
                        "allow_drops": "boolean (optional)"
                    }
                },
                {
                    "name": "sanitize_query",
                    "description": "Attempt to sanitize SQL query",
                    "parameters": {
                        "query": "string (required)"
                    }
                }
            ]
        }
