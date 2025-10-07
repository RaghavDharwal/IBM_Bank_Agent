#!/usr/bin/env bash
# 🔍 Deployment Verification Script
# Verifies that the application is properly deployed and working

set -e

echo "🏦 Bank of India Loan Portal - Deployment Verification"
echo "======================================================"

# Load config
if [ -f "deploy.config.json" ]; then
    if command -v jq >/dev/null 2>&1; then
        BACKEND_NAME=$(jq -r '.backend.name' deploy.config.json)
        FRONTEND_NAME=$(jq -r '.frontend.name' deploy.config.json)
    else
        echo "⚠️  jq not found. Using default names..."
        BACKEND_NAME="bank-portal-backend"
        FRONTEND_NAME="bank-portal-frontend"
    fi
else
    echo "⚠️  Config file not found. Using default names..."
    BACKEND_NAME="bank-portal-backend"
    FRONTEND_NAME="bank-portal-frontend"
fi

BACKEND_URL="https://$BACKEND_NAME.onrender.com"
FRONTEND_URL="https://$FRONTEND_NAME.onrender.com"

echo
echo "🔧 Testing Backend API..."
echo "URL: $BACKEND_URL"

# Test backend health
if curl -f "$BACKEND_URL/health" >/dev/null 2>&1; then
    echo "✅ Backend health check passed"
    
    # Test API endpoints
    echo "🧪 Testing API endpoints..."
    
    # Test basic endpoints
    if curl -f "$BACKEND_URL/api/loan-schemes" >/dev/null 2>&1; then
        echo "✅ Loan schemes endpoint working"
    else
        echo "⚠️  Loan schemes endpoint may not be ready"
    fi
    
else
    echo "❌ Backend health check failed"
    echo "   This is normal if deployment is still in progress"
fi

echo
echo "🎨 Testing Frontend..."
echo "URL: $FRONTEND_URL"

if curl -f "$FRONTEND_URL" >/dev/null 2>&1; then
    echo "✅ Frontend is accessible"
    
    # Check if it's actually serving the React app
    if curl -s "$FRONTEND_URL" | grep -q "Bank.*Loan" >/dev/null 2>&1; then
        echo "✅ Frontend serving Bank Loan Portal"
    else
        echo "⚠️  Frontend may still be building"
    fi
else
    echo "❌ Frontend not accessible"
    echo "   This is normal if deployment is still in progress"
fi

echo
echo "📊 Deployment Status Summary"
echo "============================"
echo "📱 Frontend: $FRONTEND_URL"
echo "🔧 Backend:  $BACKEND_URL/health"
echo "📚 Docs:     $BACKEND_URL/api/docs (when ready)"

echo
echo "🎯 Next Steps:"
echo "1. Wait 5-10 minutes for initial deployment to complete"
echo "2. Check Render dashboard for detailed logs"
echo "3. Test the application manually at the URLs above"
echo "4. Set up monitoring and alerts if needed"

echo
echo "🔄 To re-run this verification:"
echo "   ./verify.sh"

echo
echo "🚀 Happy Banking! 🏦"