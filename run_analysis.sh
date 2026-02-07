#!/bin/bash

echo "🤖 Jarvis AI Agent - Overnight Analysis"
echo "========================================"
echo ""

cd backend

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env not found!"
    echo "Please create backend/.env and add your GOOGLE_API_KEY"
    exit 1
fi

# Install new dependencies
pip install -q -r requirements.txt



echo "🔄 Step 0: Syncing Client List from Documents..."
python sync_clients.py

echo ""
echo "🧠 Step 1: Running Multi-Agent Analysis (LangGraph)..."
echo "   Agents: Research → Analysis → Email Writer"
python agentic_system.py

echo ""
echo "========================================"
echo "✅ Workflow Complete!"
echo ""
echo "Check data/emails_sent.json for generated emails"
echo "Run the dashboard to see warm leads: ./run.sh"
echo ""
