# 🌟 AURA - Enterprise Data Analysis Platform

> **Analyst in a Box** - Your AI-powered enterprise data analysis solution with universal database connectivity and interactive visualizations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

## 🎯 What is AURA?

AURA is a comprehensive enterprise data analysis platform that combines AI-powered conversations with universal database connectivity and interactive visualizations. Built with a microservices architecture, it provides four core modes:

- **💬 Chat Mode** - AI-powered data analysis conversations
- **🗄️ Database Mode** - Universal database connectivity (12+ database types)
- **📊 Visualization Mode** - Interactive charts and dashboards  
- **🚀 Strategy Mode** - Enterprise competitive demonstrations

## 🚀 Quick Start

### 🛠️ Development Setup (One-Command)

```powershell
git clone https://github.com/Mounith007/AURA-Data-Analyst-Agent.git
cd AURA-Data-Analyst-Agent
.\setup-team-fixed.ps1
```

### 🐳 Docker Deployment (Production Ready)

```powershell
# Clone and start with Docker
git clone https://github.com/Mounith007/AURA-Data-Analyst-Agent.git
cd AURA-Data-Analyst-Agent
docker-compose up -d

# Check container health
docker ps
```

### ✅ Automated Setup Features:
- ✅ Checks prerequisites (Python 3.11+, Node.js 18+, Git, Docker)
- ✅ Sets up Python virtual environment  
- ✅ Installs all dependencies
- ✅ Configures environment variables
- ✅ Starts all services (Development or Docker)
- ✅ Health checks for all containers
- ✅ Opens your browser to http://localhost:5173

## 🌐 Service Endpoints

| Service | Development URL | Docker URL | Purpose |
|---------|----------------|------------|---------|
| **Frontend** | http://localhost:5173 | http://localhost:5173 | React UI Interface |
| **API Gateway** | http://localhost:8000 | http://localhost:8000 | Backend coordination |
| **Database API** | http://localhost:8002 | http://localhost:8002 | Universal DB connectivity |
| **MCP Server** | http://localhost:8007 | http://localhost:8007 | AI Agent operations |
| **Health Checks** | `/health` endpoints | Container health monitoring | Service status |

### 🔄 Deployment Status: **✅ FULLY OPERATIONAL**
- ✅ Development Environment: Ready
- ✅ Docker Environment: Ready  
- ✅ Health Checks: Working
- ✅ Team Collaboration: Ready

## 🗄️ Supported Databases

- **PostgreSQL, MySQL, SQLite** - SQL databases
- **MongoDB, Cassandra** - NoSQL databases  
- **Snowflake, BigQuery, Redshift** - Cloud warehouses
- **Databricks, ClickHouse** - Analytics platforms

## 📊 Features

- **🤖 AI Chat** - Natural language data analysis with Google Gemini
- **🤖 AI Agents** - Multi-agent system with database agent and MCP servers
- **📊 Visualizations** - Interactive charts (Bar, Line, Pie, Radar) with Chart.js
- **🔌 Universal Connectivity** - 12+ database types (SQL/NoSQL/Cloud)
- **🛠️ Agent Tools** - Reusable tools for database operations and schema analysis
- **🔄 Tiny Recursive Model** - Smart task decomposition for complex operations
- **🐳 Docker Support** - Production-ready containerized deployment
- **👥 Team Ready** - Automated setup scripts with health monitoring
- **⚡ Microservices** - FastAPI backend with React TypeScript frontend
- **🔒 Enterprise Ready** - Environment configuration and security features

## � Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Docker containers not healthy** | Use `setup-team-fixed.ps1` (has latest health check fixes) |
| **Port conflicts** | Stop conflicting services: `docker-compose down` |
| **PowerShell script errors** | Use `setup-team-fixed.ps1` instead of `setup-for-team.ps1` |
| **Missing environment variables** | Check `.env` file in `aurabackend/` directory |

### Health Check Commands
```powershell
# Check container status
docker ps

# Test API endpoints
Invoke-WebRequest http://localhost:8000/health
Invoke-WebRequest http://localhost:8002/health

# Restart Docker services
docker-compose down && docker-compose up -d
```

## �📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - 5-minute setup
- **[Team Setup Guide](README-TEAM.md)** - Detailed instructions  
- **[AI Agent System](AGENT_SYSTEM_DOCS.md)** - AI agents and MCP servers documentation
- **[API Documentation](http://localhost:8002/docs)** - Interactive API docs
