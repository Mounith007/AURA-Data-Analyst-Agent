# 🌟 AURA - Analyst in a Box Enterprise Platform

## 🚀 Quick Start Guide for Team Members

This guide will help you set up the AURA project on your machine and start contributing immediately.

## 📋 Prerequisites

Before you start, make sure you have these installed:

### Required Software
- **Python 3.11+** - [Download here](https://python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/downloads)
- **VS Code** (recommended) - [Download here](https://code.visualstudio.com/)

### Windows Users
- **PowerShell 5.1+** (usually pre-installed)
- **Windows Terminal** (recommended) - [Get from Microsoft Store](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701)

## 🛠️ Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/rohithtul/Data-Analyst-Agent.git
cd Data-Analyst-Agent/Data-Analyst-Agent
```

### 2. Backend Setup
```powershell
# Create Python virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r aurabackend/requirements.txt
```

### 3. Frontend Setup
```powershell
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Go back to root directory
cd ..
```

### 4. Environment Configuration
```powershell
# Copy environment template
copy aurabackend\.env.example aurabackend\.env

# Edit the .env file with your API keys (optional for development)
```

## 🚀 Running the Application

### Option 1: Automated Startup (Recommended)
```powershell
# Run the complete setup script
.\setup-for-team.ps1
```

### Option 2: Manual Startup

#### Backend Services
```powershell
# Terminal 1 - Database Service
cd aurabackend\database
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 2 - API Gateway  
cd aurabackend\api_gateway
python main.py
```

#### Frontend
```powershell
# Terminal 3 - Frontend
cd frontend
npm run dev
```

## 🌐 Access Points

After successful startup, access the application at:

- **📱 Main Application**: http://localhost:5174/ (or auto-detected port)
- **📊 Database API Docs**: http://localhost:8002/docs
- **🌐 API Gateway**: http://localhost:8000/

## 🏗️ Project Structure

```
Data-Analyst-Agent/
├── frontend/                 # React + TypeScript UI
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── types.ts         # TypeScript definitions
│   │   └── App.tsx          # Main application
│   └── package.json         # Node.js dependencies
├── aurabackend/             # Python backend services
│   ├── database/            # Database connectivity service
│   ├── api_gateway/         # Main API coordination
│   ├── orchestration_service/ # AI agents
│   └── requirements.txt     # Python dependencies
├── setup-for-team.ps1      # Automated setup script
├── start-backend.ps1        # Backend startup script
└── README-TEAM.md          # This file
```

## 🧭 Navigation Guide

### Frontend Features:
- **💬 AI Chat**: Interactive AI assistant for data analysis
- **🗄️ Databases**: Connect and manage database connections
- **📊 Visualize**: Create interactive charts from any database
- **🚀 Strategy**: View strategic demos and competitive advantages

### Backend Services:
- **Database Service (Port 8002)**: Universal database connectivity
- **API Gateway (Port 8000)**: Request routing and coordination
- **Orchestration Service**: Multi-agent AI system

## 🔧 Development Workflow

### Making Changes

1. **Frontend Development**:
   ```powershell
   cd frontend
   npm run dev      # Hot reload enabled
   ```

2. **Backend Development**:
   ```powershell
   cd aurabackend\database
   python -m uvicorn main:app --reload  # Auto-restart on changes
   ```

### Code Style
- **Frontend**: ESLint + TypeScript strict mode
- **Backend**: Python PEP 8 + FastAPI standards
- **Git**: Create feature branches for new work

### Testing
```powershell
# Frontend tests
cd frontend
npm test

# Backend tests
cd aurabackend
python -m pytest
```

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Python Virtual Environment Issues
```powershell
# If activation fails
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Recreate virtual environment
rm -rf .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### 2. Node.js Dependency Issues
```powershell
# Clear npm cache
npm cache clean --force

# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 3. Port Conflicts
- **Frontend**: Vite will auto-select available ports (5173, 5174, 5175, etc.)
- **Database Service**: Change port in startup command if 8002 is taken
- **API Gateway**: Modify port in `main.py` if 8000 is taken

#### 4. Import Errors in Backend
```powershell
# Ensure PYTHONPATH is set
$env:PYTHONPATH = "C:\path\to\Data-Analyst-Agent\Data-Analyst-Agent"
```

#### 5. Windows Firewall/Defender
- Allow Python and Node.js through Windows Firewall
- Temporarily disable real-time protection if needed

### Getting Help
- Check the terminal output for detailed error messages
- Look at the browser console for frontend issues
- Use the API documentation at http://localhost:8002/docs

## 🔄 Git Workflow

### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add: description of changes"

# Push to remote
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### Syncing with Main
```bash
# Update your local main
git checkout main
git pull origin main

# Update your feature branch
git checkout feature/your-feature-name
git merge main
```

## 📦 Key Dependencies

### Frontend
- **React 19**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **Chart.js**: Data visualization
- **ESLint**: Code linting

### Backend
- **FastAPI**: REST API framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: Database ORM
- **Pandas**: Data manipulation
- **Pydantic**: Data validation

## 🌟 Enterprise Features

AURA includes enterprise-grade features:

### Database Connectivity
- **12+ Database Types**: PostgreSQL, MySQL, MongoDB, Snowflake, BigQuery, etc.
- **Schema Introspection**: Automatic table and column discovery
- **Connection Pooling**: Efficient database connections

### AI & Analytics
- **Glass Box IDE**: Transparent SQL editing and approval
- **Multi-Agent System**: AI query generation and validation
- **Context-Aware Suggestions**: Smart query recommendations

### Visualization & Reporting
- **Interactive Charts**: Bar, line, pie, radar, polar area charts
- **Real-time Updates**: Live data refresh capabilities
- **Export Options**: PNG, data export, sharing features

### Architecture
- **Microservices**: Scalable service-oriented design
- **Plugin System**: Extensible marketplace architecture
- **Strategic Demos**: Vertical market demonstrations

## 🎯 Contributing

1. **Pick an Issue**: Look at GitHub Issues or ask the team lead
2. **Create Branch**: Use descriptive branch names
3. **Make Changes**: Follow coding standards
4. **Test Locally**: Ensure everything works
5. **Submit PR**: Include description and screenshots
6. **Code Review**: Address feedback promptly

## 📞 Support

If you encounter any issues:
1. Check this README first
2. Look at existing GitHub Issues
3. Ask in the team chat
4. Create a new GitHub Issue with:
   - Operating system
   - Error messages
   - Steps to reproduce
   - Screenshots (if applicable)

## 🎉 Welcome to the Team!

You're now ready to contribute to AURA - the enterprise data platform that competes with Azure, AWS, and other cloud giants! 

Happy coding! 🚀