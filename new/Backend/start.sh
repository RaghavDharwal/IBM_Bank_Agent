#!/bin/bash

# Bank Loan Portal Backend Startup Script

echo "🏛️  Bank Loan Portal Backend Setup"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration if needed"
fi

echo ""
echo "🚀 Starting Bank Loan Portal Backend..."
echo "🌐 Server will be available at: http://localhost:5000"
echo "📚 API Documentation: http://localhost:5000/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python app.py
