# AURA Multi-Agent System Configuration

## Agent Types
AGENT_TYPES = {
    "database": {
        "class": "DatabaseAgent",
        "module": "agents.database_agent",
        "description": "AI agent for database operations and schema analysis",
        "capabilities": [
            "connection_testing",
            "schema_introspection",
            "query_execution",
            "optimization_recommendations"
        ],
        "max_concurrent_tasks": 10
    }
}

## MCP Server Configuration
MCP_SERVERS = {
    "database": {
        "port": 8007,
        "host": "0.0.0.0",
        "description": "Database MCP server for database operations",
        "tools": [
            "test_database_connection",
            "list_database_connections",
            "get_database_connection_info",
            "get_database_schema",
            "get_table_info",
            "execute_database_query"
        ]
    }
}

## Tiny Recursive Model Settings
RECURSIVE_MODEL = {
    "max_depth": 3,  # Maximum recursion depth for task decomposition
    "enable_caching": True,
    "decomposition_threshold": 3  # Number of parameters to trigger decomposition
}

## Tool Registry Settings
TOOL_REGISTRY = {
    "auto_register": True,
    "enable_versioning": True,
    "cache_results": True
}

## Agent Communication
AGENT_COMMUNICATION = {
    "enable_inter_agent_messaging": True,
    "message_queue_size": 100,
    "message_timeout_seconds": 30
}

## Scalability Settings
SCALABILITY = {
    "max_agents_per_type": 10,
    "enable_auto_scaling": False,
    "agent_pool_size": 5
}
