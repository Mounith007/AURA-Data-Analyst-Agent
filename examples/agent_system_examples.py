#!/usr/bin/env python3
"""
AURA AI Agent System - Example Usage
Demonstrates the MCP server and AI agents functionality
"""

import asyncio
import httpx
import sys

BASE_URL = "http://localhost:8007"

async def example_1_list_agents():
    """Example 1: List all available agents"""
    print("=" * 60)
    print("Example 1: List All Agents")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/agents")
        data = response.json()
        
        print(f"\nTotal agents: {data['count']}")
        for agent in data['agents']:
            print(f"\n  Agent ID: {agent['agent_id']}")
            print(f"  Name: {agent['name']}")
            print(f"  Type: {agent['agent_type']}")
            print(f"  Status: {agent['status']}")
            print(f"  Tools: {', '.join(agent['tools'])}")

async def example_2_mcp_tools():
    """Example 2: List MCP server tools"""
    print("\n" + "=" * 60)
    print("Example 2: MCP Server Tools")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/mcp/servers/database/tools")
        data = response.json()
        
        print(f"\nDatabase MCP Server Tools ({len(data['tools'])} available):\n")
        for tool in data['tools']:
            print(f"  • {tool['name']}")
            print(f"    Description: {tool['description']}")
            print(f"    Required params: {tool['inputSchema'].get('required', [])}")
            print()

async def example_3_execute_task():
    """Example 3: Execute a task with an agent"""
    print("=" * 60)
    print("Example 3: Execute Agent Task")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # Get first agent
        response = await client.get(f"{BASE_URL}/agents")
        agents = response.json()['agents']
        
        if not agents:
            print("\nNo agents available!")
            return
        
        agent_id = agents[0]['agent_id']
        print(f"\nUsing agent: {agent_id}")
        
        # Execute a test connection task
        print("\nExecuting 'test_connection' task...")
        response = await client.post(
            f"{BASE_URL}/agents/{agent_id}/tasks",
            json={
                "task_type": "test_connection",
                "parameters": {
                    "connection_id": "demo_connection"
                }
            }
        )
        result = response.json()
        
        print(f"\n  Task ID: {result['task_id']}")
        print(f"  Status: {result['status']}")
        print(f"  Error: {result.get('error', 'None')}")
        
        # Get task history
        print("\nTask History:")
        response = await client.get(f"{BASE_URL}/agents/{agent_id}/tasks")
        history = response.json()
        
        for task in history['tasks']:
            print(f"  • {task['task_type']} - {task['status']}")

async def example_4_create_agent():
    """Example 4: Create a new agent"""
    print("\n" + "=" * 60)
    print("Example 4: Create New Agent")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        print("\nCreating new database agent...")
        response = await client.post(
            f"{BASE_URL}/agents",
            json={
                "agent_type": "database",
                "agent_id": "my_custom_agent"
            }
        )
        
        if response.status_code == 200:
            agent = response.json()['agent']
            print(f"\n  ✅ Agent created successfully!")
            print(f"  Agent ID: {agent['agent_id']}")
            print(f"  Name: {agent['name']}")
            print(f"  Tools loaded: {agent['metadata']['tools_loaded']}")
        else:
            print(f"\n  ❌ Failed to create agent: {response.text}")

async def example_5_call_mcp_tool():
    """Example 5: Call an MCP server tool directly"""
    print("\n" + "=" * 60)
    print("Example 5: Call MCP Tool Directly")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        print("\nCalling 'list_database_connections' tool...")
        response = await client.post(
            f"{BASE_URL}/mcp/servers/database/call-tool",
            json={
                "tool_name": "list_database_connections",
                "arguments": {}
            }
        )
        result = response.json()
        
        print(f"\n  Success: {result.get('success', False)}")
        if result.get('success'):
            connections = result['result']['connections']
            print(f"  Connections found: {len(connections)}")
            for conn in connections[:3]:
                print(f"    • {conn['name']} ({conn['type']})")

async def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("AURA AI Agent System - Examples")
    print("=" * 60)
    print("\nMake sure the MCP server is running on port 8007")
    print("Start it with: cd aurabackend/mcp_server && python main.py")
    print()
    
    try:
        # Check if server is running
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.get(f"{BASE_URL}/health")
    except Exception as e:
        print(f"❌ Error: Cannot connect to MCP server at {BASE_URL}")
        print(f"   Please start the server first.")
        sys.exit(1)
    
    # Run examples
    await example_1_list_agents()
    await example_2_mcp_tools()
    await example_3_execute_task()
    await example_4_create_agent()
    await example_5_call_mcp_tool()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed successfully!")
    print("=" * 60)
    print("\nFor more information, see AGENT_SYSTEM_DOCS.md")
    print()

if __name__ == "__main__":
    asyncio.run(main())
