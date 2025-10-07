@echo off
REM Bank Loan Portal Backend Startup Script for Windows

echo 🏛️  Bank Loan Portal Backend Setup
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7+
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy .env.example .env
    echo 📝 Please edit .env file with your configuration if needed
)

echo.
echo 🚀 Starting Bank Loan Portal Backend...
echo 🌐 Server will be available at: http://localhost:5000
echo 📚 API Documentation: http://localhost:5000/api/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause
