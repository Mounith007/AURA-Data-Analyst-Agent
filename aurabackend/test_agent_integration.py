#!/usr/bin/env python
"""
Integration test for AURA AI Agent infrastructure
Tests MCP server, agent tools, and database agent
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_tools import DatabaseTool, QueryValidator, SchemaAnalyzer, RecursiveReasoner
from mcp_server.context_manager import context_manager


def test_query_validator():
    """Test query validator functionality"""
    print("\n🧪 Testing Query Validator...")
    validator = QueryValidator()
    
    # Test 1: Valid query
    result1 = validator.validate_query("SELECT * FROM users LIMIT 10")
    assert result1["is_valid"], "Valid query should pass"
    print("  ✓ Valid query test passed")
    
    # Test 2: Dangerous query
    result2 = validator.validate_query("DROP TABLE users")
    assert not result2["is_valid"], "Dangerous query should fail"
    print("  ✓ Dangerous query detection passed")
    
    # Test 3: SQL injection
    result3 = validator.validate_query("SELECT * FROM users WHERE id = '' OR '1'='1'")
    assert len(result3["warnings"]) > 0, "Should detect SQL injection attempt"
    print("  ✓ SQL injection detection passed")
    
    print("✅ Query Validator: All tests passed!")


def test_schema_analyzer():
    """Test schema analyzer functionality"""
    print("\n🧪 Testing Schema Analyzer...")
    analyzer = SchemaAnalyzer()
    
    # Mock schema
    schema = {
        "tables": [
            {
                "name": "users",
                "schema": "public",
                "columns": [
                    {"name": "id", "type": "integer"},
                    {"name": "email", "type": "varchar"}
                ],
                "primary_keys": ["id"],
                "row_count": 100000
            }
        ]
    }
    
    result = analyzer.analyze_schema(schema)
    assert result["statistics"]["total_tables"] == 1, "Should count 1 table"
    assert "quality_score" in result, "Should have quality score"
    print("  ✓ Schema analysis passed")
    
    # Test relationship finding
    relationships = analyzer.find_relationships(schema)
    assert "total_relationships" in relationships, "Should return relationships"
    print("  ✓ Relationship finding passed")
    
    print("✅ Schema Analyzer: All tests passed!")


def test_recursive_reasoner():
    """Test recursive reasoner functionality"""
    print("\n🧪 Testing Recursive Reasoner...")
    reasoner = RecursiveReasoner(max_depth=3)
    
    problem = "Find top 10 products by sales"
    result = reasoner.reason(problem, context={})
    
    assert result["problem"] == problem, "Should preserve problem"
    assert "solution" in result, "Should have solution"
    assert "confidence" in result, "Should have confidence"
    assert result["steps_taken"] >= 1, "Should have at least 1 step"
    print("  ✓ Reasoning test passed")
    
    # Test explanation
    explanation = reasoner.explain_reasoning(result)
    assert len(explanation) > 0, "Should generate explanation"
    print("  ✓ Explanation generation passed")
    
    print("✅ Recursive Reasoner: All tests passed!")


def test_context_manager():
    """Test context manager functionality"""
    print("\n🧪 Testing Context Manager...")
    
    # Create context
    context_key = context_manager.create_context(
        agent_id="test_agent",
        session_id="test_session",
        context_type="database",
        context_data={"test": "data"}
    )
    assert context_key, "Should create context"
    print("  ✓ Context creation passed")
    
    # Retrieve context
    context = context_manager.get_context(context_key)
    assert context is not None, "Should retrieve context"
    assert context.agent_id == "test_agent", "Should have correct agent_id"
    print("  ✓ Context retrieval passed")
    
    # Update context
    success = context_manager.update_context(
        context_key,
        {"updated": "data"}
    )
    assert success, "Should update context"
    print("  ✓ Context update passed")
    
    # List contexts
    contexts = context_manager.list_contexts(agent_id="test_agent")
    assert len(contexts) >= 1, "Should list contexts"
    print("  ✓ Context listing passed")
    
    # Delete context
    success = context_manager.delete_context(context_key)
    assert success, "Should delete context"
    print("  ✓ Context deletion passed")
    
    print("✅ Context Manager: All tests passed!")


async def test_database_tool():
    """Test database tool functionality"""
    print("\n🧪 Testing Database Tool...")
    tool = DatabaseTool(db_manager=None)  # No real db manager needed for this test
    
    # Test tool definition
    definition = tool.get_tool_definition()
    assert definition["name"] == "database_tool", "Should have correct name"
    assert len(definition["operations"]) > 0, "Should have operations"
    print("  ✓ Tool definition passed")
    
    # Test dry run query
    result = await tool.execute_query(
        connection_id="test",
        query="SELECT * FROM test",
        dry_run=True
    )
    assert result["success"], "Dry run should succeed"
    assert result["dry_run"], "Should be marked as dry run"
    print("  ✓ Dry run query passed")
    
    print("✅ Database Tool: All tests passed!")


def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("🚀 AURA AI Agent Infrastructure - Integration Tests")
    print("=" * 60)
    
    try:
        # Synchronous tests
        test_query_validator()
        test_schema_analyzer()
        test_recursive_reasoner()
        test_context_manager()
        
        # Async tests
        asyncio.run(test_database_tool())
        
        print("\n" + "=" * 60)
        print("🎉 All Integration Tests Passed!")
        print("=" * 60)
        return True
    
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
