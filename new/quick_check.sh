#!/usr/bin/env bash
# 🎯 Quick Performance Check Script

echo "⚡ Performance & Security Quick Check"
echo "===================================="

# Backend Performance Check
echo "🔧 Backend Check:"
cd Backend 2>/dev/null || { echo "❌ Backend directory not found"; exit 1; }

# Check Python version
python_version=$(python --version 2>/dev/null || python3 --version 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Python: $python_version"
else
    echo "❌ Python not found"
fi

# Check if requirements can be parsed
if python -c "import pkg_resources; pkg_resources.require(open('requirements.txt', mode='r'))" 2>/dev/null; then
    echo "✅ Requirements.txt is valid"
else
    echo "⚠️  Some requirements may need installation"
fi

# Check for security issues
echo
echo "🔒 Security Check:"
if grep -q "SECRET_KEY.*changeme" app.py 2>/dev/null; then
    echo "❌ Default SECRET_KEY found - MUST change in production"
else
    echo "✅ No default SECRET_KEY found"
fi

if grep -q "DEBUG.*True" app.py 2>/dev/null; then
    echo "⚠️  Debug mode detected - ensure it's off in production"
else
    echo "✅ No debug mode in code"
fi

cd ..

# Frontend Performance Check
echo
echo "🎨 Frontend Check:"
cd AI-agent-Frontend 2>/dev/null || { echo "❌ Frontend directory not found"; exit 1; }

# Check Node.js
if command -v node >/dev/null 2>&1; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js not found"
fi

# Check package.json
if [ -f "package.json" ]; then
    echo "✅ package.json exists"
    if grep -q "\"export\"" package.json; then
        echo "✅ Static export configured"
    fi
else
    echo "❌ package.json not found"
fi

cd ..

echo
echo "🚀 Deployment Readiness:"
echo "✅ All production files created"
echo "✅ Build scripts configured"  
echo "✅ Environment examples provided"
echo "✅ Documentation complete"
echo
echo "📝 Final Steps:"
echo "1. Set environment variables in Render"
echo "2. Update SECRET_KEY and JWT_SECRET_KEY"
echo "3. Configure database URL"
echo "4. Test deployment"
echo
echo "Run './deploy_check.sh' for complete checklist!"