#!/usr/bin/env bash
# 🔧 Quick Setup Script for One-Command Deployment
# Bank of India Loan Portal

set -e

echo "🏦 Bank of India Loan Portal - Quick Setup"
echo "=========================================="

# Make deployment script executable
chmod +x deploy.sh

# Install required dependencies
echo "📦 Installing dependencies..."

# Check if Homebrew is installed (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v brew >/dev/null 2>&1; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # Install required tools
    echo "Installing required tools..."
    brew install jq curl git || true
    
    echo "Installing Render CLI..."
    brew install renderinc/tap/render || true
else
    # Linux setup
    echo "Setting up for Linux..."
    
    # Install jq if not present
    if ! command -v jq >/dev/null 2>&1; then
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update && sudo apt-get install -y jq curl git
        elif command -v yum >/dev/null 2>&1; then
            sudo yum install -y jq curl git
        else
            echo "Please install jq, curl, and git manually"
            exit 1
        fi
    fi
    
    # Install Render CLI
    echo "Installing Render CLI..."
    curl -fsSL https://cli.render.com/install | sh
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Edit deploy.config.json with your settings (especially SECRET_KEY values)"
echo "2. Run: ./deploy.sh"
echo ""
echo "📖 Or follow the quick start:"
echo "./setup.sh && ./deploy.sh"