"""
Base classes for MCP (Model Context Protocol) Server
Provides foundation for AI agent tools and resources
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class MCPResource:
    """Represents a resource that can be accessed by AI agents"""
    uri: str
    name: str
    description: str
    mime_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "mimeType": self.mime_type,
            "metadata": self.metadata
        }


@dataclass
class MCPTool:
    """Represents a tool that AI agents can use"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Callable
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
            "metadata": self.metadata
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments"""
        try:
            result = await self.handler(arguments)
            return {
                "success": True,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


class MCPServer(ABC):
    """
    Base class for MCP servers
    Implements the Model Context Protocol for AI agent interactions
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self._initialize()
    
    @abstractmethod
    def _initialize(self):
        """Initialize server-specific tools and resources"""
        pass
    
    def register_tool(self, tool: MCPTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    def register_resource(self, resource: MCPResource):
        """Register a new resource"""
        self.resources[resource.uri] = resource
    
    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def get_resource(self, uri: str) -> Optional[MCPResource]:
        """Get a resource by URI"""
        return self.resources.get(uri)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources"""
        return [resource.to_dict() for resource in self.resources.values()]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool by name with arguments"""
        tool = self.get_tool(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }
        return await tool.execute(arguments)
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.name,
            "version": self.version,
            "tools": [tool.name for tool in self.tools.values()],
            "resources": [resource.uri for resource in self.resources.values()],
            "capabilities": self.get_capabilities()
        }
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get server capabilities"""
        pass
