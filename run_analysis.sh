#!/bin/bash

# Ensure we're in the backend directory
cd "$(dirname "$0")/backend"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the analysis
python ai_agent.py
