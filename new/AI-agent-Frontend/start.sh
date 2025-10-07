#!/bin/bash

# Bank Loan Portal Frontend Startup Script

echo "🏛️  Bank Loan Portal Frontend Setup"
echo "===================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "📦 Installing pnpm..."
    npm install -g pnpm
fi

echo "✅ pnpm found: $(pnpm --version)"

# Install dependencies
echo "📥 Installing dependencies..."
pnpm install

echo ""
echo "🚀 Starting Bank Loan Portal Frontend..."
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "🔗 Make sure Backend is running at: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Next.js development server
pnpm dev
