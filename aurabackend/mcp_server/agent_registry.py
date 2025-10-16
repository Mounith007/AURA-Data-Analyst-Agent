"""
Agent Registry
Central registry for managing AI agents with different capabilities
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class AgentType(Enum):
    """Types of agents in the system"""
    DATABASE = "database"
    GENERATOR = "generator"
    CRITIC = "critic"
    ANALYST = "analyst"
    ORCHESTRATOR = "orchestrator"

@dataclass
class AgentDefinition:
    """Agent definition with capabilities and configuration"""
    id: str
    name: str
    type: AgentType
    description: str
    model: str  # e.g., "gemini-flash", "gemini-pro"
    capabilities: List[str]
    tools_available: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

class AgentRegistry:
    """Registry for managing AI agents"""
    
    def __init__(self):
        self.agents: Dict[str, AgentDefinition] = {}
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """Initialize default agents"""
        
        # Database Connection Agent
        self.register_agent(
            AgentDefinition(
                id="db-agent-001",
                name="Database Connection Agent",
                type=AgentType.DATABASE,
                description="Specialized agent for database connections and schema management",
                model="gemini-1.5-flash",  # Using tiny recursive model
                capabilities=[
                    "connect_to_databases",
                    "manage_connections",
                    "retrieve_schema",
                    "execute_queries",
                    "validate_connections"
                ],
                tools_available=[
                    "connect_database",
                    "list_database_connections",
                    "query_database",
                    "get_database_schema"
                ],
                metadata={
                    "max_concurrent_connections": 10,
                    "supported_databases": [
                        "postgresql", "mysql", "sqlite", "mssql", "oracle",
                        "mongodb", "snowflake", "bigquery", "redshift",
                        "databricks", "clickhouse", "cassandra"
                    ]
                }
            )
        )
        
        # SQL Generator Agent
        self.register_agent(
            AgentDefinition(
                id="gen-agent-001",
                name="SQL Generator Agent",
                type=AgentType.GENERATOR,
                description="Generates SQL queries from natural language",
                model="gemini-pro",
                capabilities=[
                    "generate_sql",
                    "optimize_queries",
                    "explain_queries"
                ],
                tools_available=[
                    "generate_sql",
                    "get_database_schema"
                ],
                metadata={
                    "supported_dialects": ["postgresql", "mysql", "sqlite", "mssql"]
                }
            )
        )
        
        # SQL Critic Agent
        self.register_agent(
            AgentDefinition(
                id="critic-agent-001",
                name="SQL Critic Agent",
                type=AgentType.CRITIC,
                description="Validates and provides feedback on SQL queries",
                model="gemini-pro",
                capabilities=[
                    "validate_sql",
                    "security_check",
                    "performance_analysis"
                ],
                tools_available=[
                    "get_database_schema"
                ],
                metadata={
                    "validation_rules": ["syntax", "security", "performance"]
                }
            )
        )
        
        # Data Analyst Agent
        self.register_agent(
            AgentDefinition(
                id="analyst-agent-001",
                name="Data Analyst Agent",
                type=AgentType.ANALYST,
                description="Analyzes data and provides insights",
                model="gemini-1.5-flash",  # Using tiny recursive model
                capabilities=[
                    "analyze_data",
                    "generate_insights",
                    "create_visualizations"
                ],
                tools_available=[
                    "analyze_data",
                    "query_database"
                ],
                metadata={
                    "analysis_types": ["summary", "trend", "correlation", "anomaly"]
                }
            )
        )
        
        # Orchestrator Agent
        self.register_agent(
            AgentDefinition(
                id="orch-agent-001",
                name="Orchestrator Agent",
                type=AgentType.ORCHESTRATOR,
                description="Orchestrates multiple agents to complete complex tasks",
                model="gemini-pro",
                capabilities=[
                    "task_decomposition",
                    "agent_coordination",
                    "result_aggregation"
                ],
                tools_available=[
                    "connect_database",
                    "query_database",
                    "generate_sql",
                    "analyze_data"
                ],
                metadata={
                    "max_subtasks": 10
                }
            )
        )
    
    def register_agent(self, agent: AgentDefinition) -> None:
        """Register a new agent"""
        self.agents[agent.id] = agent
    
    def get_agent(self, agent_id: str) -> Optional[AgentDefinition]:
        """Get an agent by ID"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[AgentDefinition]:
        """List all registered agents"""
        return list(self.agents.values())
    
    def get_agents_by_type(self, agent_type: AgentType) -> List[AgentDefinition]:
        """Get agents by type"""
        if isinstance(agent_type, str):
            agent_type = AgentType(agent_type)
        return [agent for agent in self.agents.values() if agent.type == agent_type]
    
    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the registry"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False
    
    async def execute_task(
        self, 
        agent_id: str, 
        task: str, 
        context: Dict[str, Any],
        tools_allowed: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Execute a task using an agent"""
        agent = self.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        
        # Validate tools
        if tools_allowed:
            invalid_tools = set(tools_allowed) - set(agent.tools_available)
            if invalid_tools:
                raise ValueError(f"Agent does not have access to tools: {invalid_tools}")
        
        # This is a mock implementation
        # In production, this would integrate with actual agent execution logic
        return {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "task": task,
            "status": "completed",
            "result": f"Task completed by {agent.name}",
            "tools_used": tools_allowed or [],
            "context": context
        }
