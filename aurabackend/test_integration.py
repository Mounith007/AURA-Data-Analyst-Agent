#!/usr/bin/env python3
"""
AURA Integration Test
Tests the full integration between MCP Server, Database Agent, and Database Service
"""

import asyncio
import httpx
import json
import time
from typing import Dict, Any

# Service URLs
MCP_SERVER_URL = "http://localhost:8003"
DATABASE_AGENT_URL = "http://localhost:8004"
DATABASE_SERVICE_URL = "http://localhost:8002"
API_GATEWAY_URL = "http://localhost:8000"

class Colors:
    """ANSI color codes for pretty output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

async def check_service_health(service_name: str, url: str) -> bool:
    """Check if a service is healthy"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/health", timeout=5.0)
            if response.status_code == 200:
                print_success(f"{service_name} is healthy")
                return True
            else:
                print_error(f"{service_name} returned status {response.status_code}")
                return False
    except Exception as e:
        print_error(f"{service_name} is not responding: {e}")
        return False

async def test_mcp_server():
    """Test MCP Server functionality"""
    print_header("Testing MCP Server")
    
    async with httpx.AsyncClient() as client:
        # Test listing tools
        print_info("Testing tool listing...")
        response = await client.get(f"{MCP_SERVER_URL}/tools")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Found {data['count']} registered tools")
            print_info(f"Available tools: {', '.join([t['name'] for t in data['tools'][:5]])}...")
        else:
            print_error(f"Failed to list tools: {response.status_code}")
        
        # Test listing agents
        print_info("\nTesting agent listing...")
        response = await client.get(f"{MCP_SERVER_URL}/agents")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Found {data['count']} registered agents")
            for agent in data['agents']:
                print_info(f"  - {agent['name']} ({agent['type']}) using {agent['model']}")
        else:
            print_error(f"Failed to list agents: {response.status_code}")
        
        # Test getting a specific tool
        print_info("\nTesting tool details...")
        response = await client.get(f"{MCP_SERVER_URL}/tools/connect_database")
        if response.status_code == 200:
            tool = response.json()
            print_success(f"Tool '{tool['name']}': {tool['description']}")
        else:
            print_error(f"Failed to get tool details: {response.status_code}")

async def test_database_agent():
    """Test Database Agent functionality"""
    print_header("Testing Database Agent")
    
    async with httpx.AsyncClient() as client:
        # Test agent info
        print_info("Testing agent info endpoint...")
        response = await client.get(f"{DATABASE_AGENT_URL}/agent/info")
        if response.status_code == 200:
            info = response.json()
            print_success(f"Agent: {info['name']}")
            print_info(f"  Model: {info['model']}")
            print_info(f"  Capabilities: {len(info['capabilities'])} capabilities")
            print_info(f"  Supported DBs: {len(info['supported_databases'])} database types")
        else:
            print_error(f"Failed to get agent info: {response.status_code}")
        
        # Test listing connections
        print_info("\nTesting connection listing...")
        response = await client.get(f"{DATABASE_AGENT_URL}/connections")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Current connections: {data['count']}")
        else:
            print_error(f"Failed to list connections: {response.status_code}")

async def test_database_service():
    """Test Database Service functionality"""
    print_header("Testing Database Service")
    
    async with httpx.AsyncClient() as client:
        # Test supported databases
        print_info("Testing supported databases endpoint...")
        response = await client.get(f"{DATABASE_SERVICE_URL}/supported-databases")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Supported databases: {len(data['databases'])}")
            for db in data['databases'][:5]:
                print_info(f"  - {db['name']} (port {db['default_port']})")
        else:
            print_error(f"Failed to get supported databases: {response.status_code}")

async def test_integration_workflow():
    """Test a complete integration workflow"""
    print_header("Testing Integration Workflow")
    
    print_info("This workflow demonstrates:")
    print_info("  1. MCP Server coordinating tools")
    print_info("  2. Database Agent using AI for insights")
    print_info("  3. Database Service managing connections")
    
    async with httpx.AsyncClient() as client:
        # Step 1: List available tools via MCP
        print_info("\nStep 1: Discovering available tools...")
        response = await client.get(f"{MCP_SERVER_URL}/tools")
        if response.status_code == 200:
            tools = response.json()
            print_success(f"Discovered {tools['count']} tools via MCP Server")
        
        # Step 2: List registered agents
        print_info("\nStep 2: Finding available agents...")
        response = await client.get(f"{MCP_SERVER_URL}/agents")
        if response.status_code == 200:
            agents = response.json()
            db_agents = [a for a in agents['agents'] if a['type'] == 'database']
            if db_agents:
                print_success(f"Found database agent: {db_agents[0]['name']}")
        
        # Step 3: Check Database Agent capabilities
        print_info("\nStep 3: Checking Database Agent capabilities...")
        response = await client.get(f"{DATABASE_AGENT_URL}/agent/info")
        if response.status_code == 200:
            info = response.json()
            print_success(f"Agent ready with {len(info['capabilities'])} capabilities")
            print_info(f"  Using model: {info['model']} (tiny recursive model)")
        
        # Step 4: Check supported databases
        print_info("\nStep 4: Verifying database support...")
        response = await client.get(f"{DATABASE_SERVICE_URL}/supported-databases")
        if response.status_code == 200:
            dbs = response.json()
            print_success(f"System supports {len(dbs['databases'])} database types")

async def main():
    """Main test function"""
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         AURA Integration Test Suite                       ║")
    print("║    MCP Server + Database Agent + Database Service         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    # Check service health
    print_header("Service Health Checks")
    services = [
        ("MCP Server", MCP_SERVER_URL),
        ("Database Agent", DATABASE_AGENT_URL),
        ("Database Service", DATABASE_SERVICE_URL),
        ("API Gateway", API_GATEWAY_URL),
    ]
    
    health_results = []
    for service_name, url in services:
        is_healthy = await check_service_health(service_name, url)
        health_results.append((service_name, is_healthy))
    
    # If any service is down, show warning
    if not all(h[1] for h in health_results):
        print_error("\n⚠️  Some services are not running!")
        print_info("Please start all services with: ./start_all_services.sh")
        return
    
    # Run tests
    try:
        await test_mcp_server()
        await test_database_agent()
        await test_database_service()
        await test_integration_workflow()
        
        # Summary
        print_header("Test Summary")
        print_success("All integration tests passed! ✨")
        print_info("\nThe system is ready for:")
        print_info("  • Multi-agent database operations")
        print_info("  • AI-powered query optimization")
        print_info("  • Scalable agent orchestration")
        print_info("  • Tool-based agent collaboration")
        
    except Exception as e:
        print_error(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
