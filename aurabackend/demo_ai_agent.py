#!/usr/bin/env python
"""
AURA AI Agent Quick Start Demo
Demonstrates the enhanced AI agent capabilities with recursive reasoning
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_tools import DatabaseTool, QueryValidator, SchemaAnalyzer, RecursiveReasoner
from mcp_server.context_manager import context_manager

# Display constants for consistent formatting
MAX_QUESTION_LENGTH = 60
MAX_ANSWER_LENGTH = 80
MAX_QUERY_LENGTH = 60


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


async def demo_recursive_reasoning():
    """Demonstrate recursive reasoning capabilities"""
    print_section("🧠 Recursive Reasoning Demo")
    
    reasoner = RecursiveReasoner(max_depth=3)
    
    # Complex query that will be decomposed
    problem = "Show top 10 customers by total revenue and count their orders from the database"
    
    print(f"\n📝 Problem: {problem}")
    print("\n🔄 Applying recursive reasoning...")
    
    result = reasoner.reason(problem, context={
        "schema": {
            "tables": [
                {"name": "customers", "columns": ["id", "name"]},
                {"name": "orders", "columns": ["id", "customer_id", "amount"]}
            ]
        }
    })
    
    print(f"\n✨ Solution: {result['solution']}")
    print(f"🎯 Confidence: {result['confidence']:.2%}")
    print(f"📊 Steps taken: {result['steps_taken']}")
    print(f"🔍 Max depth reached: {result['max_depth_reached']}")
    
    # Show reasoning tree
    print("\n🌳 Reasoning Tree:")
    print_tree(result['reasoning_tree'], indent=0)


def print_tree(node, indent=0):
    """Print reasoning tree recursively"""
    prefix = "  " * indent
    question = node['question'][:MAX_QUESTION_LENGTH]
    print(f"{prefix}├─ {node['step_type'].upper()}: {question}...")
    
    if node.get('answer'):
        answer = node['answer'][:MAX_ANSWER_LENGTH]
        print(f"{prefix}│  ✓ {answer}...")
    
    for sub in node.get('sub_questions', []):
        print_tree(sub, indent + 1)


async def demo_query_validation():
    """Demonstrate query validation"""
    print_section("🔒 Query Validation Demo")
    
    validator = QueryValidator()
    
    queries = [
        ("Valid query", "SELECT name, email FROM users WHERE active = true LIMIT 10"),
        ("SQL injection attempt", "SELECT * FROM users WHERE id = '' OR '1'='1'"),
        ("Dangerous operation", "DROP TABLE users; SELECT * FROM data"),
    ]
    
    for label, query in queries:
        print(f"\n📝 {label}:")
        query_display = query[:MAX_QUERY_LENGTH]
        print(f"   Query: {query_display}...")
        
        result = validator.validate_query(query, allow_modifications=False)
        
        print(f"   ✓ Valid: {result['is_valid']}")
        print(f"   🛡️  Security score: {result['security_score']:.0f}/100")
        
        if result['errors']:
            print(f"   ❌ Errors: {', '.join(result['errors'][:2])}")
        if result['warnings']:
            print(f"   ⚠️  Warnings: {', '.join(result['warnings'][:2])}")


async def demo_schema_analysis():
    """Demonstrate schema analysis"""
    print_section("📊 Schema Analysis Demo")
    
    analyzer = SchemaAnalyzer()
    
    # Mock schema for demonstration
    schema = {
        "tables": [
            {
                "name": "users",
                "schema": "public",
                "columns": [
                    {"name": "id", "type": "integer"},
                    {"name": "email", "type": "varchar(255)"},
                    {"name": "created_at", "type": "timestamp"}
                ],
                "primary_keys": ["id"],
                "indexes": [{"name": "idx_email", "columns": ["email"]}],
                "row_count": 150000
            },
            {
                "name": "orders",
                "schema": "public",
                "columns": [
                    {"name": "id", "type": "integer"},
                    {"name": "user_id", "type": "integer"},
                    {"name": "total_amount", "type": "decimal(10,2)"},
                    {"name": "created_at", "type": "timestamp"}
                ],
                "primary_keys": [],
                "indexes": [],
                "row_count": 250000
            },
            {
                "name": "products",
                "schema": "public",
                "columns": [
                    {"name": "id", "type": "integer"},
                    {"name": "name", "type": "varchar(255)"},
                    {"name": "price", "type": "decimal(10,2)"}
                ],
                "primary_keys": ["id"],
                "indexes": [],
                "row_count": 5000
            }
        ]
    }
    
    print("\n🔍 Analyzing database schema...")
    result = analyzer.analyze_schema(schema)
    
    print(f"\n📈 Statistics:")
    print(f"   • Total tables: {result['statistics']['total_tables']}")
    print(f"   • Total columns: {result['statistics']['total_columns']}")
    print(f"   • Quality score: {result['quality_score']:.1f}/100")
    
    print(f"\n💡 Insights ({len(result['insights'])}):")
    for insight in result['insights'][:3]:
        print(f"   • [{insight['type']}] {insight['message']}")
    
    print(f"\n🎯 Recommendations:")
    for rec in result['recommendations'][:3]:
        print(f"   • {rec}")
    
    # Relationship analysis
    print("\n🔗 Analyzing table relationships...")
    relationships = analyzer.find_relationships(schema)
    print(f"   • Total relationships found: {relationships['total_relationships']}")
    print(f"   • Explicit (foreign keys): {relationships['explicit_relationships']}")
    print(f"   • Implicit (naming patterns): {relationships['implicit_relationships']}")


async def demo_context_management():
    """Demonstrate context management"""
    print_section("📦 Context Management Demo")
    
    print("\n🔄 Creating agent context...")
    context_key = context_manager.create_context(
        agent_id="demo_agent",
        session_id="demo_session_001",
        context_type="database",
        context_data={
            "connection_id": "demo_conn_123",
            "database_type": "postgresql",
            "current_query": "SELECT * FROM users",
            "user_preference": "detailed_results"
        },
        metadata={
            "created_by": "demo_script",
            "purpose": "demonstration"
        },
        ttl_seconds=3600
    )
    
    print(f"   ✓ Context created: {context_key}")
    
    # Retrieve context
    print("\n📥 Retrieving context...")
    context = context_manager.get_context(context_key)
    print(f"   ✓ Agent: {context.agent_id}")
    print(f"   ✓ Session: {context.session_id}")
    print(f"   ✓ Type: {context.context_type}")
    print(f"   ✓ Data keys: {list(context.context_data.keys())}")
    
    # Update context
    print("\n🔄 Updating context...")
    context_manager.update_context(
        context_key,
        {"execution_count": 1, "last_result": "success"}
    )
    print("   ✓ Context updated")
    
    # Get statistics
    print("\n📊 Context Statistics:")
    stats = context_manager.get_context_stats()
    print(f"   • Total contexts: {stats['total_contexts']}")
    print(f"   • Contexts by type: {stats['contexts_by_type']}")
    print(f"   • Contexts by agent: {stats['contexts_by_agent']}")
    
    # Cleanup
    context_manager.delete_context(context_key)
    print("\n🗑️  Context cleaned up")


async def demo_complete_workflow():
    """Demonstrate a complete workflow"""
    print_section("🚀 Complete AI Agent Workflow")
    
    print("\n📋 Scenario: User asks for customer analytics")
    print("   'Show me the top 5 customers by revenue this year'")
    
    # Step 1: Recursive reasoning
    print("\n1️⃣  Applying recursive reasoning...")
    reasoner = RecursiveReasoner(max_depth=2)
    reasoning = reasoner.reason(
        "Show me the top 5 customers by revenue this year",
        context={"schema": {"tables": ["customers", "orders"]}}
    )
    print(f"   ✓ Problem decomposed into {reasoning['steps_taken']} steps")
    print(f"   ✓ Confidence: {reasoning['confidence']:.2%}")
    
    # Step 2: Generate SQL (mock)
    print("\n2️⃣  Generating SQL query...")
    sql_query = """
    SELECT c.name, SUM(o.amount) as total_revenue
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    WHERE YEAR(o.order_date) = YEAR(CURRENT_DATE)
    GROUP BY c.id, c.name
    ORDER BY total_revenue DESC
    LIMIT 5
    """.strip()
    print(f"   ✓ SQL generated")
    
    # Step 3: Validate query
    print("\n3️⃣  Validating SQL query...")
    validator = QueryValidator()
    validation = validator.validate_query(sql_query)
    print(f"   ✓ Query is valid: {validation['is_valid']}")
    print(f"   ✓ Security score: {validation['security_score']:.0f}/100")
    
    # Step 4: Create execution context
    print("\n4️⃣  Creating execution context...")
    context_key = context_manager.create_context(
        agent_id="workflow_agent",
        session_id="workflow_001",
        context_type="task",
        context_data={
            "user_query": "Show me the top 5 customers by revenue this year",
            "generated_sql": sql_query,
            "validation": validation,
            "reasoning": reasoning
        }
    )
    print(f"   ✓ Context created: {context_key}")
    
    # Step 5: Summary
    print("\n✅ Workflow complete!")
    print("   • Query analyzed and decomposed")
    print("   • SQL generated and validated")
    print("   • Context saved for execution")
    print("   • Ready for database execution")
    
    # Cleanup
    context_manager.delete_context(context_key)


async def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("  🌟 AURA AI Agent System - Interactive Demo")
    print("  Enterprise Database AI with Recursive Reasoning")
    print("=" * 70)
    
    try:
        # Run all demos
        await demo_recursive_reasoning()
        await demo_query_validation()
        await demo_schema_analysis()
        await demo_context_management()
        await demo_complete_workflow()
        
        print("\n" + "=" * 70)
        print("  🎉 Demo Complete!")
        print("  " + "=" * 70)
        print("\n📚 Next Steps:")
        print("   1. Check out aurabackend/AI_AGENT_README.md for detailed docs")
        print("   2. Run integration tests: python test_agent_integration.py")
        print("   3. Start MCP server: uvicorn mcp_server.mcp_main:app --port 8007")
        print("   4. Explore API at http://localhost:8007/docs")
        print("\n")
        
    except (ValueError, KeyError, TypeError) as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Ensure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
