# 🚀 One-Command Deployment Guide

The Bank of India Loan Portal now supports **ONE-COMMAND DEPLOYMENT** to Render!

## ⚡ Quick Start (30 seconds)

```bash
# Clone and navigate to your project
git clone https://github.com/RaghavDharwal/IBM_Bank_Agent.git
cd IBM_Bank_Agent

# One-command setup and deployment
./setup.sh && ./deploy.sh
```

That's it! Your entire application will be deployed automatically! 🎉

## 📋 What Happens Automatically

### 🔧 Setup Phase (`./setup.sh`)
- ✅ Installs all required tools (jq, curl, Render CLI)
- ✅ Configures deployment environment
- ✅ Sets up permissions

### 🚀 Deployment Phase (`./deploy.sh`)
- ✅ **Validates Environment** - Checks git config, dependencies
- ✅ **Commits & Pushes** - Auto-commits any changes to GitHub
- ✅ **Creates Services** - Backend, Frontend, Database on Render
- ✅ **Configures Environment** - Production settings, secrets
- ✅ **Health Checks** - Monitors deployment progress
- ✅ **Success Report** - Provides live URLs and dashboard links

## 🎯 Deployment Process

```bash
./deploy.sh
```

### What it deploys:
1. **🗄️  PostgreSQL Database** - Free tier, managed by Render
2. **🖥️  Flask Backend** - Python with Gunicorn, health checks
3. **🎨 Next.js Frontend** - Static site with optimized builds
4. **🔐 Security** - JWT auth, CORS, environment variables
5. **📊 Monitoring** - Health endpoints, logging

## ⚙️ Configuration

The deployment is controlled by `deploy.config.json`:

```json
{
  "project": {
    "name": "bank-portal",
    "github_repo": "RaghavDharwal/IBM_Bank_Agent"
  },
  "backend": {
    "name": "bank-portal-backend"
  },
  "frontend": {
    "name": "bank-portal-frontend"
  },
  "database": {
    "name": "bank-portal-db"
  }
}
```

### 🔐 Security Configuration

**IMPORTANT:** Before first deployment, update these in `deploy.config.json`:

```json
{
  "backend": {
    "environment": {
      "SECRET_KEY": "your-super-secure-secret-key-here",
      "JWT_SECRET_KEY": "your-jwt-secret-key-here"
    }
  }
}
```

## 📊 After Deployment

The script provides:
- ✅ **Live URLs** for frontend and backend
- ✅ **Render Dashboard** links for monitoring  
- ✅ **Health Check** endpoints
- ✅ **Deployment Summary** in `deployment_summary.md`

## 🔧 Advanced Usage

### Custom Configuration
```bash
# Edit deployment settings
vim deploy.config.json

# Deploy with custom config
./deploy.sh
```

### Re-deployment
```bash
# Just run again - it handles updates automatically
./deploy.sh
```

### Environment Variables
The script automatically handles:
- Database connection strings
- API URLs between services  
- CORS origins
- Production settings

## 🛠️ Manual Steps (Optional)

If you prefer manual control:

1. **Edit Configuration:**
   ```bash
   vim deploy.config.json
   ```

2. **Run Setup:**
   ```bash
   ./setup.sh
   ```

3. **Deploy:**
   ```bash
   ./deploy.sh
   ```

## 📱 What Gets Deployed

### Frontend: `https://bank-portal-frontend.onrender.com`
- Next.js static site
- Optimized builds
- Environment-based API connections

### Backend: `https://bank-portal-backend.onrender.com`  
- Flask API with Gunicorn
- PostgreSQL database
- JWT authentication
- Health monitoring at `/health`

### Database:
- Managed PostgreSQL on Render
- Automatic backups
- Connection pooling

## 🚨 Troubleshooting

### Authentication Issues
```bash
render auth login
```

### Deployment Failures
- Check `deployment_summary.md` for details
- Monitor in Render dashboard
- View service logs for debugging

### Configuration Problems
- Verify `deploy.config.json` syntax
- Ensure GitHub repository access
- Check environment variable values

## 🎉 Success!

After deployment, you'll see:
```
╔══════════════════════════════════════════════════════════════╗
║                    🎉 DEPLOYMENT COMPLETE! 🎉                ║  
╚══════════════════════════════════════════════════════════════╝

📱 Frontend URL: https://bank-portal-frontend.onrender.com
🔧 Backend API: https://bank-portal-backend.onrender.com
🗄️  Database: Managed PostgreSQL on Render
```

Your **Bank of India Loan Portal** is now live and ready for users! 🏦✨

## 🔄 Automatic Updates

- **Auto-deploy enabled** from your GitHub main branch
- Push changes to trigger automatic redeployment
- Zero-downtime updates
- Rollback capability through Render dashboard

---

**One command. Full deployment. Enterprise ready.** 🚀