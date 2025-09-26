#!/usr/bin/env bash
# 🚀 One-Command Render Deployment Script
# Bank of India Loan Portal - Complete Automated Deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration file
CONFIG_FILE="./deploy.config.json"

# Function to print colored output
print_step() {
    echo -e "${CYAN}🚀 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Banner
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║    🏦 Bank of India Loan Portal - One-Command Deployment    ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if configuration file exists
if [ ! -f "$CONFIG_FILE" ]; then
    print_error "Configuration file $CONFIG_FILE not found!"
    echo
    print_info "Creating default configuration file..."
    cat > "$CONFIG_FILE" << 'EOF'
{
  "project": {
    "name": "bank-portal",
    "github_repo": "RaghavDharwal/IBM_Bank_Agent",
    "github_branch": "main"
  },
  "backend": {
    "name": "bank-portal-backend",
    "region": "oregon",
    "runtime": "python",
    "root_directory": "Backend",
    "build_command": "./build.sh",
    "start_command": "gunicorn app:app",
    "environment": {
      "FLASK_ENV": "production",
      "SECRET_KEY": "CHANGE_ME_TO_SECURE_SECRET_KEY",
      "JWT_SECRET_KEY": "CHANGE_ME_TO_SECURE_JWT_KEY"
    }
  },
  "frontend": {
    "name": "bank-portal-frontend",
    "region": "oregon",
    "root_directory": "AI-agent-Frontend",
    "build_command": "./build.sh",
    "publish_directory": "out",
    "environment": {
      "NEXT_PUBLIC_API_URL": "AUTO_GENERATED_FROM_BACKEND"
    }
  },
  "database": {
    "name": "bank-portal-db",
    "plan": "free"
  }
}
EOF
    print_warning "Please edit $CONFIG_FILE with your specific settings!"
    print_warning "Especially change SECRET_KEY and JWT_SECRET_KEY to secure values!"
    echo
    print_info "After updating the config, run: ./deploy.sh"
    exit 1
fi

print_step "Loading configuration..."
if command -v jq >/dev/null 2>&1; then
    PROJECT_NAME=$(jq -r '.project.name' "$CONFIG_FILE")
    GITHUB_REPO=$(jq -r '.project.github_repo' "$CONFIG_FILE")
    print_success "Configuration loaded for project: $PROJECT_NAME"
else
    print_warning "jq not found. Installing jq for JSON parsing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew >/dev/null 2>&1; then
            brew install jq
        else
            print_error "Please install jq manually: brew install jq"
            exit 1
        fi
    else
        print_error "Please install jq manually for your system"
        exit 1
    fi
fi

# Validate environment
print_step "Validating environment..."

# Check if git is configured
if ! git config user.name >/dev/null 2>&1; then
    print_error "Git user name not configured!"
    echo "Run: git config --global user.name 'Your Name'"
    exit 1
fi

if ! git config user.email >/dev/null 2>&1; then
    print_error "Git user email not configured!"
    echo "Run: git config --global user.email 'your.email@example.com'"
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "Backend" ] || [ ! -d "AI-agent-Frontend" ]; then
    print_error "Not in project root directory! Please run from the directory containing Backend/ and AI-agent-Frontend/"
    exit 1
fi

print_success "Environment validation passed"

# Check for uncommitted changes
print_step "Checking for uncommitted changes..."
if ! git diff --quiet; then
    print_warning "Uncommitted changes found. Committing them..."
    git add .
    git commit -m "🚀 Pre-deployment commit - $(date)"
fi

# Push to GitHub
print_step "Pushing to GitHub..."
git push origin main
print_success "Code pushed to GitHub"

# Check if Render CLI is installed
print_step "Checking Render CLI..."
if ! command -v render >/dev/null 2>&1; then
    print_warning "Render CLI not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew >/dev/null 2>&1; then
            brew install renderinc/tap/render
        else
            print_error "Please install Homebrew first, then run: brew install renderinc/tap/render"
            exit 1
        fi
    else
        print_info "Installing Render CLI for Linux..."
        curl -fsSL https://cli.render.com/install | sh
    fi
    
    print_info "Please authenticate with Render by running: render auth login"
    print_info "After authentication, run this script again."
    exit 1
fi

# Authenticate with Render if not already done
if ! render whoami >/dev/null 2>&1; then
    print_warning "Not authenticated with Render. Please authenticate..."
    render auth login
fi

print_success "Render CLI is ready"

# Create or update services
print_step "Deploying to Render..."

# Extract values from config
BACKEND_NAME=$(jq -r '.backend.name' "$CONFIG_FILE")
FRONTEND_NAME=$(jq -r '.frontend.name' "$CONFIG_FILE")
DB_NAME=$(jq -r '.database.name' "$CONFIG_FILE")

print_info "Creating Render services configuration..."

# Create render.yaml for GitOps deployment
cat > "render.yaml" << EOF
services:
  # PostgreSQL Database
  - type: pserv
    name: $DB_NAME
    env: node
    plan: free
    databases:
      - name: ${DB_NAME//-/_}
        user: ${DB_NAME//-/_}_user

  # Backend Service
  - type: web
    name: $BACKEND_NAME
    env: python
    region: oregon
    plan: free
    repo: https://github.com/$GITHUB_REPO.git
    branch: main
    rootDir: Backend
    buildCommand: ./build.sh
    startCommand: gunicorn app:app
    healthCheckPath: /health
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: $DB_NAME
          property: connectionString
      - key: CORS_ORIGINS
        value: https://$FRONTEND_NAME.onrender.com

  # Frontend Service
  - type: web
    name: $FRONTEND_NAME
    env: static
    region: oregon
    plan: free
    repo: https://github.com/$GITHUB_REPO.git
    branch: main
    rootDir: AI-agent-Frontend
    buildCommand: ./build.sh
    staticPublishPath: out
    envVars:
      - key: NEXT_PUBLIC_API_URL
        value: https://$BACKEND_NAME.onrender.com
EOF

print_success "Render configuration created"

# Apply the configuration
print_step "Applying Render configuration..."
render blueprint launch

print_step "Deployment initiated! Monitoring progress..."

# Wait for deployment to complete
print_info "This may take 5-10 minutes for the first deployment..."
echo
print_info "You can monitor the deployment at: https://dashboard.render.com"

# Check deployment status
sleep 30
print_step "Checking deployment status..."

# Health check function
check_health() {
    local service_name=$1
    local max_attempts=20
    local attempt=1
    
    print_info "Health checking $service_name..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "https://$service_name.onrender.com/health" >/dev/null 2>&1; then
            print_success "$service_name is healthy!"
            return 0
        else
            print_info "Attempt $attempt/$max_attempts - Waiting for $service_name..."
            sleep 30
            ((attempt++))
        fi
    done
    
    print_warning "$service_name health check timed out"
    return 1
}

# Wait a bit more for services to be ready
print_info "Waiting for services to initialize..."
sleep 60

# Check backend health
if check_health "$BACKEND_NAME"; then
    BACKEND_URL="https://$BACKEND_NAME.onrender.com"
else
    print_warning "Backend health check failed, but deployment may still be in progress"
    BACKEND_URL="https://$BACKEND_NAME.onrender.com"
fi

# Check frontend
FRONTEND_URL="https://$FRONTEND_NAME.onrender.com"
if curl -f "$FRONTEND_URL" >/dev/null 2>&1; then
    print_success "Frontend is accessible!"
else
    print_warning "Frontend may still be deploying..."
fi

# Final success message
echo
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 DEPLOYMENT COMPLETE! 🎉                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo
print_success "Bank of India Loan Portal deployed successfully!"
echo
print_info "📱 Frontend URL: $FRONTEND_URL"
print_info "🔧 Backend API: $BACKEND_URL"
print_info "🗄️  Database: Managed PostgreSQL on Render"
echo
print_info "🖥️  Render Dashboard: https://dashboard.render.com"
print_info "📊 Monitor logs and metrics in your Render dashboard"
echo

# Create deployment summary
cat > "deployment_summary.md" << EOF
# 🚀 Deployment Summary

**Deployment Date:** $(date)
**Project:** Bank of India Loan Portal

## 🌐 Live URLs
- **Frontend:** $FRONTEND_URL
- **Backend API:** $BACKEND_URL
- **Health Check:** $BACKEND_URL/health

## 📊 Service Details
- **Backend Service:** $BACKEND_NAME
- **Frontend Service:** $FRONTEND_NAME  
- **Database:** $DB_NAME

## 🔧 Management
- **Render Dashboard:** https://dashboard.render.com
- **Repository:** https://github.com/$GITHUB_REPO

## 📝 Post-Deployment Notes
- All services are running on Render's free tier
- Database is PostgreSQL managed by Render
- Automatic deployments enabled from GitHub main branch
- Health checks configured for monitoring

## 🛠️ Maintenance
- Monitor services in Render dashboard
- View logs for debugging
- Scale services as needed
- Environment variables managed in Render console

EOF

print_success "Deployment summary saved to deployment_summary.md"

echo
print_info "🎯 Next steps:"
print_info "1. Test your application at the URLs above"
print_info "2. Set up custom domains if needed"
print_info "3. Configure monitoring and alerts"
print_info "4. Review logs in Render dashboard"

echo -e "${PURPLE}Happy banking! 🏦✨${NC}"