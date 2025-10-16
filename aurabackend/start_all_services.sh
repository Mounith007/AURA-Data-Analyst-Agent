#!/bin/bash
# AURA Backend Services Startup Script
# Starts all backend services including MCP server and Database Agent

echo "🚀 Starting AURA Backend Services..."

# Set environment variables
export API_HOST="${API_HOST:-0.0.0.0}"
export DEBUG="${DEBUG:-true}"
export API_GATEWAY_PORT="${API_GATEWAY_PORT:-8000}"
export DATABASE_SERVICE_PORT="${DATABASE_SERVICE_PORT:-8002}"
export MCP_SERVER_PORT="${MCP_SERVER_PORT:-8003}"
export DATABASE_AGENT_PORT="${DATABASE_AGENT_PORT:-8004}"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv "$SCRIPT_DIR/venv"
fi

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Install dependencies if needed
if [ ! -f "$SCRIPT_DIR/venv/.dependencies_installed" ]; then
    echo "📦 Installing dependencies..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
    touch "$SCRIPT_DIR/venv/.dependencies_installed"
fi

# Function to start a service
start_service() {
    local service_name=$1
    local service_dir=$2
    local port=$3
    
    echo "🔧 Starting $service_name on port $port..."
    cd "$SCRIPT_DIR/$service_dir"
    python main.py &
    echo $! > "/tmp/aura_${service_name}.pid"
    cd "$SCRIPT_DIR"
}

# Start all services
start_service "api_gateway" "api_gateway" "$API_GATEWAY_PORT"
sleep 2

start_service "database_service" "database" "$DATABASE_SERVICE_PORT"
sleep 2

start_service "mcp_server" "mcp_server" "$MCP_SERVER_PORT"
sleep 2

start_service "database_agent" "agents" "$DATABASE_AGENT_PORT"
sleep 2

echo ""
echo "✅ All AURA Backend Services are starting up..."
echo ""
echo "Service Endpoints:"
echo "  🌐 API Gateway:       http://localhost:$API_GATEWAY_PORT"
echo "  🗄️  Database Service:  http://localhost:$DATABASE_SERVICE_PORT"
echo "  🔧 MCP Server:        http://localhost:$MCP_SERVER_PORT"
echo "  🤖 Database Agent:    http://localhost:$DATABASE_AGENT_PORT"
echo ""
echo "Health Check URLs:"
echo "  http://localhost:$API_GATEWAY_PORT/health"
echo "  http://localhost:$DATABASE_SERVICE_PORT/health"
echo "  http://localhost:$MCP_SERVER_PORT/health"
echo "  http://localhost:$DATABASE_AGENT_PORT/health"
echo ""
echo "To stop all services, run: ./stop_services.sh"
echo ""
