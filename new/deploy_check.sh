#!/usr/bin/env bash
# 🚀 Quick Deployment Checklist Script

echo "🏦 Bank of India Loan Portal - Deployment Checklist"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ "$2" = "✅" ]; then
        echo -e "${GREEN}$2 $1${NC}"
    elif [ "$2" = "❌" ]; then
        echo -e "${RED}$2 $1${NC}"
    elif [ "$2" = "⚠️" ]; then
        echo -e "${YELLOW}$2 $1${NC}"
    else
        echo -e "${BLUE}$2 $1${NC}"
    fi
}

echo
echo "📋 Pre-Deployment Checklist:"
echo

# Check if in correct directory
if [ -d "Backend" ] && [ -d "AI-agent-Frontend" ]; then
    print_status "Project structure verified" "✅"
else
    print_status "Not in project root directory" "❌"
    exit 1
fi

# Check Backend files
echo
echo "🔧 Backend Configuration:"
if [ -f "Backend/requirements.txt" ]; then
    print_status "requirements.txt exists" "✅"
else
    print_status "requirements.txt missing" "❌"
fi

if [ -f "Backend/build.sh" ] && [ -x "Backend/build.sh" ]; then
    print_status "build.sh exists and is executable" "✅"
else
    print_status "build.sh missing or not executable" "❌"
fi

if [ -f "Backend/gunicorn.conf.py" ]; then
    print_status "gunicorn.conf.py exists" "✅"
else
    print_status "gunicorn.conf.py missing" "❌"
fi

if [ -f "Backend/Procfile" ]; then
    print_status "Procfile exists" "✅"
else
    print_status "Procfile missing" "❌"
fi

if [ -f "Backend/.env.example" ]; then
    print_status ".env.example exists" "✅"
else
    print_status ".env.example missing" "❌"
fi

# Check Frontend files
echo
echo "🎨 Frontend Configuration:"
if [ -f "AI-agent-Frontend/package.json" ]; then
    print_status "package.json exists" "✅"
else
    print_status "package.json missing" "❌"
fi

if [ -f "AI-agent-Frontend/build.sh" ] && [ -x "AI-agent-Frontend/build.sh" ]; then
    print_status "build.sh exists and is executable" "✅"
else
    print_status "build.sh missing or not executable" "❌"
fi

if [ -f "AI-agent-Frontend/next.config.mjs" ]; then
    print_status "next.config.mjs exists" "✅"
else
    print_status "next.config.mjs missing" "❌"
fi

if [ -f "AI-agent-Frontend/.env.example" ]; then
    print_status ".env.example exists" "✅"
else
    print_status ".env.example missing" "❌"
fi

# Check documentation
echo
echo "📚 Documentation:"
if [ -f "RENDER_DEPLOYMENT.md" ]; then
    print_status "RENDER_DEPLOYMENT.md exists" "✅"
else
    print_status "RENDER_DEPLOYMENT.md missing" "❌"
fi

if [ -f "README.md" ]; then
    print_status "README.md exists" "✅"
else
    print_status "README.md missing" "❌"
fi

echo
echo "=================================================="
echo "🚀 Ready for Render Deployment!"
echo
echo "Next steps:"
echo "1. Push code to GitHub repository"
echo "2. Create Render account at https://render.com"
echo "3. Follow RENDER_DEPLOYMENT.md guide"
echo "4. Configure environment variables"
echo "5. Deploy backend service first"
echo "6. Deploy frontend service"
echo "7. Test full application"
echo
echo "📖 Complete guide: ./RENDER_DEPLOYMENT.md"
echo "🔧 Production check: cd Backend && python production_check.py"
echo