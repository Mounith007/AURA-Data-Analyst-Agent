"""
Base classes for agent tools
Provides foundation for creating reusable agent tools
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class ToolExecutionResult:
    """Result of a tool execution"""
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "execution_time_ms": self.execution_time_ms,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }


class AgentTool(ABC):
    """
    Base class for agent tools
    All agent tools should inherit from this class
    """
    
    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.usage_count = 0
        self.last_used = None
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolExecutionResult:
        """
        Execute the tool with given parameters
        Must be implemented by subclasses
        """
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the JSON schema for tool parameters
        Must be implemented by subclasses
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the tool"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "schema": self.get_schema(),
            "usage_count": self.usage_count,
            "last_used": self.last_used
        }
    
    async def run(self, **kwargs) -> ToolExecutionResult:
        """
        Run the tool and track usage
        Wrapper around execute() that adds tracking
        """
        start_time = datetime.now()
        self.usage_count += 1
        self.last_used = start_time.isoformat()
        
        try:
            result = await self.execute(**kwargs)
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            result.execution_time_ms = execution_time
            return result
        except Exception as e:
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            return ToolExecutionResult(
                success=False,
                data=None,
                error=str(e),
                execution_time_ms=execution_time,
                metadata={"tool_name": self.name}
            )


class ToolRegistry:
    """
    Registry for managing agent tools
    Provides centralized tool management and discovery
    """
    
    def __init__(self):
        self.tools: Dict[str, AgentTool] = {}
    
    def register(self, tool: AgentTool):
        """Register a tool"""
        self.tools[tool.name] = tool
    
    def unregister(self, tool_name: str) -> bool:
        """Unregister a tool"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            return True
        return False
    
    def get(self, tool_name: str) -> Optional[AgentTool]:
        """Get a tool by name"""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools"""
        return [tool.get_info() for tool in self.tools.values()]
    
    def get_tool_names(self) -> List[str]:
        """Get list of all tool names"""
        return list(self.tools.keys())
    
    async def execute_tool(self, tool_name: str, **kwargs) -> ToolExecutionResult:
        """Execute a tool by name"""
        tool = self.get(tool_name)
        if not tool:
            return ToolExecutionResult(
                success=False,
                data=None,
                error=f"Tool '{tool_name}' not found",
                metadata={"available_tools": self.get_tool_names()}
            )
        return await tool.run(**kwargs)
    
    def get_tools_by_category(self, category: str) -> List[AgentTool]:
        """Get tools by category"""
        return [
            tool for tool in self.tools.values()
            if category in tool.get_info().get("schema", {}).get("categories", [])
        ]


# Global tool registry
global_tool_registry = ToolRegistry()
