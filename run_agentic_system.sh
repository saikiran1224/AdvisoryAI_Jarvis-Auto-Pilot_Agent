#!/bin/bash

echo "🤖 Jarvis Multi-Agent System (LangGraph)"
echo "=========================================="
echo ""

cd backend

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env not found!"
    echo "Please create backend/.env and add your GOOGLE_API_KEY"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || true

# Install dependencies if needed
pip install -q -r requirements.txt

echo "🧠 Initializing Multi-Agent System..."
echo "✅ Research Agent (RAG)"
echo "✅ Analysis Agent (Gemini)"
echo "✅ Email Writer Agent (Gemini)"
echo ""

# Run the agentic system
python agentic_system.py

echo ""
echo "=========================================="
echo "✅ Multi-Agent Workflow Complete!"
echo ""
echo "Check data/emails_sent.json for results"
echo ""
