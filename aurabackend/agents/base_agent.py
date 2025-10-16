"""
Base Agent Class
Foundation for all AI agents in the AURA system
Supports tiny recursive model and scalable agent architecture
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class AgentTask:
    """Represents a task for an agent to execute"""
    task_id: str
    task_type: str
    description: str
    parameters: Dict[str, Any]
    status: AgentStatus = AgentStatus.IDLE
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMessage:
    """Message for inter-agent communication"""
    message_id: str
    sender_id: str
    receiver_id: str
    message_type: str
    content: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class BaseAgent(ABC):
    """
    Base class for all AI agents
    Implements tiny recursive model pattern and agent lifecycle management
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        name: str,
        description: str,
        version: str = "1.0.0"
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.name = name
        self.description = description
        self.version = version
        self.status = AgentStatus.IDLE
        self.tasks: Dict[str, AgentTask] = {}
        self.tools: List[str] = []
        self.messages: List[AgentMessage] = []
        self.metadata: Dict[str, Any] = {}
        self.created_at = datetime.now()
        self.last_active = datetime.now()
    
    @abstractmethod
    async def initialize(self):
        """Initialize the agent (load models, setup tools, etc.)"""
        pass
    
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> AgentTask:
        """
        Execute a task
        Must be implemented by subclasses
        """
        pass
    
    async def run_task(self, task_type: str, **parameters) -> AgentTask:
        """
        Run a task with tiny recursive pattern
        Breaks down complex tasks into smaller subtasks if needed
        """
        task_id = str(uuid.uuid4())
        task = AgentTask(
            task_id=task_id,
            task_type=task_type,
            description=parameters.get("description", f"Execute {task_type}"),
            parameters=parameters
        )
        
        self.tasks[task_id] = task
        self.status = AgentStatus.RUNNING
        self.last_active = datetime.now()
        
        try:
            # Execute the task (may recursively break into subtasks)
            result_task = await self.execute_task(task)
            result_task.status = AgentStatus.COMPLETED
            result_task.completed_at = datetime.now().isoformat()
            
            self.status = AgentStatus.IDLE
            return result_task
            
        except Exception as e:
            task.status = AgentStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now().isoformat()
            self.status = AgentStatus.FAILED
            return task
    
    async def recursive_decompose(
        self,
        task: AgentTask,
        max_depth: int = 3,
        current_depth: int = 0
    ) -> List[AgentTask]:
        """
        Tiny recursive model: Decompose a task into subtasks
        This allows agents to break down complex problems
        """
        if current_depth >= max_depth:
            return [task]
        
        # Check if task needs decomposition
        if await self.should_decompose(task):
            subtasks = await self.decompose_task(task)
            
            # Recursively decompose subtasks
            all_subtasks = []
            for subtask in subtasks:
                decomposed = await self.recursive_decompose(
                    subtask,
                    max_depth,
                    current_depth + 1
                )
                all_subtasks.extend(decomposed)
            
            return all_subtasks
        else:
            return [task]
    
    async def should_decompose(self, task: AgentTask) -> bool:
        """
        Determine if a task should be decomposed into subtasks
        Override in subclasses for custom logic
        """
        # Default: don't decompose
        return False
    
    async def decompose_task(self, task: AgentTask) -> List[AgentTask]:
        """
        Decompose a task into subtasks
        Override in subclasses for custom decomposition logic
        """
        return [task]
    
    async def send_message(self, receiver_id: str, message_type: str, content: Dict[str, Any]):
        """Send a message to another agent"""
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content
        )
        self.messages.append(message)
        return message
    
    async def receive_message(self, message: AgentMessage):
        """Receive and process a message from another agent"""
        self.messages.append(message)
        await self.process_message(message)
    
    async def process_message(self, message: AgentMessage):
        """
        Process a received message
        Override in subclasses for custom message handling
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "status": self.status.value,
            "tools": self.tools,
            "task_count": len(self.tasks),
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "metadata": self.metadata
        }
    
    def get_task_history(self) -> List[Dict[str, Any]]:
        """Get task execution history"""
        return [
            {
                "task_id": task.task_id,
                "task_type": task.task_type,
                "status": task.status.value,
                "created_at": task.created_at,
                "completed_at": task.completed_at,
                "error": task.error
            }
            for task in self.tasks.values()
        ]


class AgentRegistry:
    """
    Registry for managing multiple agents
    Enables scalable multi-agent architecture
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_types: Dict[str, List[str]] = {}
    
    def register(self, agent: BaseAgent):
        """Register an agent"""
        self.agents[agent.agent_id] = agent
        
        # Track by type
        if agent.agent_type not in self.agent_types:
            self.agent_types[agent.agent_type] = []
        self.agent_types[agent.agent_type].append(agent.agent_id)
    
    def unregister(self, agent_id: str) -> bool:
        """Unregister an agent"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            del self.agents[agent_id]
            
            # Remove from type tracking
            if agent.agent_type in self.agent_types:
                self.agent_types[agent.agent_type].remove(agent_id)
            
            return True
        return False
    
    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """Get an agent by ID"""
        return self.agents.get(agent_id)
    
    def get_by_type(self, agent_type: str) -> List[BaseAgent]:
        """Get all agents of a specific type"""
        agent_ids = self.agent_types.get(agent_type, [])
        return [self.agents[aid] for aid in agent_ids if aid in self.agents]
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents"""
        return [agent.get_info() for agent in self.agents.values()]
    
    def get_agent_types(self) -> List[str]:
        """Get list of all agent types"""
        return list(self.agent_types.keys())
    
    async def route_message(self, message: AgentMessage):
        """Route a message to the appropriate agent"""
        receiver = self.get(message.receiver_id)
        if receiver:
            await receiver.receive_message(message)
        else:
            print(f"Warning: Receiver agent {message.receiver_id} not found")


# Global agent registry
global_agent_registry = AgentRegistry()
