#!/bin/bash

echo "🚀 Jarvis Auto-Pilot Agent - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✅ Python and Node.js are installed"
echo ""

# Setup Backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Backend setup complete"
echo ""

# Check for API key
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found in backend/"
    echo "Please create backend/.env and add your GOOGLE_API_KEY"
    echo "Example: GOOGLE_API_KEY=your_key_here"
    echo ""
fi

cd ..

# Setup Frontend
echo "📦 Setting up frontend..."
cd frontend

# Install Node dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

echo "✅ Frontend setup complete"
echo ""

cd ..

echo "=========================================="
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Add your Google Gemini API key to backend/.env"
echo "2. Add your client DOCX files to backend/data/client_documents/"
echo "3. Run: ./run.sh"
echo ""
