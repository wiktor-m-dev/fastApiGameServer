#!/bin/bash

# FastAPI Game Server - Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "FastAPI Game Server - Starting Stack"
echo "========================================"
echo ""

# Check if MySQL is running
echo "[1/3] Checking MySQL connection..."
if mysql -u root -e "SELECT 1" >/dev/null 2>&1; then
    echo "MySQL connection OK"
else
    echo "WARNING: MySQL might not be running or credentials are wrong"
    echo "Please ensure MySQL is running and .env credentials are correct"
fi

# Start Backend
echo ""
echo "[2/3] Starting FastAPI Backend..."
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload &
BACKEND_PID=$!
cd ..

# Give backend time to start
sleep 3

# Start Frontend
echo ""
echo "[3/3] Starting React Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "Stack starting up!"
echo "========================================"
echo ""
echo "Backend:   http://localhost:8000"
echo "Frontend:  http://localhost:5173"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
wait
