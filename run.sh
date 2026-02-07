#!/bin/bash

echo "🚀 Starting Jarvis Auto-Pilot Agent"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ backend/.env not found!"
    echo "Please create it and add your GOOGLE_API_KEY"
    exit 1
fi

# Start backend in background
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate 2>/dev/null || true
python app.py &
BACKEND_PID=$!
echo "✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)"
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend running on http://localhost:5173 (PID: $FRONTEND_PID)"
cd ..

echo ""
echo "===================================="
echo "✅ Jarvis is running!"
echo ""
echo "📊 Dashboard: http://localhost:5173"
echo "🔧 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "===================================="

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
