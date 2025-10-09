#!/bin/bash

# AURA Backend Docker Startup Script
echo "🚀 Starting AURA Backend Services in Docker..."

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🏗️ Building and starting services..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
echo ""
echo "📊 Database Service (Port 8002):"
curl -s http://localhost:8002/health || echo "❌ Database service not ready"

echo ""
echo "🌐 API Gateway (Port 8000):"
curl -s http://localhost:8000/health || echo "❌ API Gateway not ready"

echo ""
echo "🤖 Orchestration Service (Port 8001):"
curl -s http://localhost:8001/health || echo "❌ Orchestration service not ready"

echo ""
echo "📋 Service Status:"
docker-compose ps

echo ""
echo "📚 API Documentation:"
echo "🔗 Database Service: http://localhost:8002/docs"
echo "🔗 API Gateway: http://localhost:8000/docs"
echo "🔗 Orchestration: http://localhost:8001/docs"

echo ""
echo "✅ AURA Backend is running in Docker!"
echo "💡 Use 'docker-compose logs -f [service_name]' to view logs"
echo "🛑 Use 'docker-compose down' to stop all services"