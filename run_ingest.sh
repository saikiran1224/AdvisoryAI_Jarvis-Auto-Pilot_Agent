#!/bin/bash
# Dedicated Document Ingestion Runner
# Use this when you want to update your ChromaDB knowledge base

echo "🚀 Starting Jarvis Document Ingestion..."
echo "======================================"

# Install dependencies (ignoring errors as we just want ingestion to work)
echo "📦 Installing Requirements..."
pip install -q -r backend/requirements.txt --no-deps

# Run the python ingestion script
echo "📄 Running Python Ingestion Script..."
python ingest.py

echo ""
echo "======================================"
echo "✅ Done!"
