# 🌟 AURA - Quick Start for Team Members

Hey team! Welcome to AURA - our enterprise data analysis platform. This guide will get you up and running in **5 minutes**.

## 🚀 ONE-COMMAND SETUP

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Data-Analyst-Agent
   ```

2. **Run the team setup script:**
   ```powershell
   .\setup-for-team.ps1
   ```

That's it! The script will:
- ✅ Check all prerequisites (Python, Node.js, Git)
- ✅ Set up Python virtual environment
- ✅ Install all backend dependencies
- ✅ Install all frontend dependencies  
- ✅ Create environment configuration
- ✅ Start all development services
- ✅ Open your browser to the application

## 🎯 What You Get

Once running, you'll have access to:

| Service | URL | Purpose |
|---------|-----|---------|
| **Main App** | http://localhost:5174 | Full AURA interface |
| **Database API** | http://localhost:8002/docs | Database connectivity docs |
| **API Gateway** | http://localhost:8000 | Backend coordination |

## 💻 Development Modes

AURA has 4 main interfaces:

1. **💬 Chat Mode** - AI-powered data analysis conversations
2. **🗄️ Database Mode** - Connect to any database (PostgreSQL, MySQL, MongoDB, etc.)
3. **📊 Visualization Mode** - Interactive charts and dashboards
4. **🚀 Strategy Mode** - Enterprise competitive demonstrations

## 🛠️ Daily Development

After the initial setup, you can restart services anytime:

```powershell
# Start all services
.\setup-for-team.ps1 -StartOnly

# Or start individually:
cd frontend && npm run dev                    # Frontend only
cd aurabackend\database && python -m uvicorn main:app --port 8002 --reload  # Database service
```

## 🔧 Project Structure

```
Data-Analyst-Agent/
├── frontend/              # React + TypeScript app
│   ├── src/components/   # UI components
│   └── package.json      # Frontend dependencies
├── aurabackend/          # Python FastAPI services
│   ├── database/         # Database connectivity service
│   ├── api_gateway/      # Main coordination service
│   └── requirements.txt  # Backend dependencies
└── setup-for-team.ps1   # One-click setup script
```

## 🆘 Common Issues & Solutions

**"Services won't start"**
- Check the individual terminal windows that open
- Make sure ports 8000, 8002, and 5174 are free

**"Python virtual environment issues"**
- Delete `.venv` folder and run setup script again
- Make sure Python 3.11+ is installed

**"Frontend won't load"**
- Try `cd frontend && npm cache clean --force && npm install`
- Check if another service is using port 5174

**"Database connections failing"**
- Ensure you've configured your database credentials
- Check the database service at http://localhost:8002/docs

## 💡 Development Tips

- **Hot Reload:** Frontend automatically refreshes when you edit files
- **API Documentation:** Visit http://localhost:8002/docs to see all database endpoints
- **Debugging:** Check browser console and terminal windows for errors
- **Testing:** Use `npm test` in frontend/ or `pytest` in aurabackend/

## 🤝 Contributing

1. Create a new branch for your feature: `git checkout -b feature/amazing-feature`
2. Make your changes
3. Test everything works: `.\setup-for-team.ps1`
4. Commit and push: `git commit -m "Add amazing feature" && git push`
5. Create a Pull Request

## 🎉 You're Ready!

The setup script handles everything automatically. If you see the green "AURA DEVELOPMENT ENVIRONMENT READY!" message, you're good to go!

**Need help?** Check the detailed README-TEAM.md or ask the team in our chat.

**Happy coding! 🚀**