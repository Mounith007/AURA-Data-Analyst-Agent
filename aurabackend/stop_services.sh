#!/bin/bash
# AURA Backend Services Stop Script
# Stops all backend services

echo "🛑 Stopping AURA Backend Services..."

# Function to stop a service
stop_service() {
    local service_name=$1
    local pid_file="/tmp/aura_${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping $service_name (PID: $pid)..."
            kill $pid
            rm "$pid_file"
        else
            echo "$service_name not running"
            rm "$pid_file"
        fi
    else
        echo "No PID file found for $service_name"
    fi
}

# Stop all services
stop_service "api_gateway"
stop_service "database_service"
stop_service "mcp_server"
stop_service "database_agent"

echo ""
echo "✅ All AURA Backend Services stopped"
echo ""
