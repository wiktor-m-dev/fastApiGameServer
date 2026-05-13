@echo off
REM FastAPI Game Server - Quick Start Script for Windows

echo.
echo ========================================
echo FastAPI Game Server - Starting Stack
echo ========================================
echo.

REM Check if MySQL is running
echo [1/3] Checking MySQL connection...
mysql -u root -e "SELECT 1" >nul 2>&1
if errorlevel 1 (
    echo WARNING: MySQL might not be running or credentials are wrong
    echo Please ensure MySQL is running and .env credentials are correct
    echo.
) else (
    echo MySQL connection OK
)

REM Start Backend
echo.
echo [2/3] Starting FastAPI Backend...
echo Opening new terminal for backend...
start cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn main:app --reload"

REM Give backend time to start
timeout /t 3 /nobreak

REM Start Frontend
echo.
echo [3/3] Starting React Frontend...
echo Opening new terminal for frontend...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Stack starting up!
echo ========================================
echo.
echo Backend:   http://localhost:8000
echo Frontend:  http://localhost:5173
echo API Docs:  http://localhost:8000/docs
echo.
echo Press any key to continue...
pause
