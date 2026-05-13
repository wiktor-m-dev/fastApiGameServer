# FastAPI Game Server - Complete Integration Guide

This guide explains how to connect and run the entire stack: Frontend (React), Backend (FastAPI), and Database (MySQL).

## Project Structure

```
fastApiGameServer/
├── backend/              # FastAPI Server
│   ├── main.py          # API endpoints
│   ├── database.py      # Database connection & methods
│   ├── schemas.py       # Pydantic models
│   └── __init__.py
├── frontend/            # React + Vite
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── services/    # API calls
│   │   ├── hooks/       # Custom hooks (auth)
│   │   ├── components/  # Reusable components
│   │   └── App.jsx      # Main router
│   ├── package.json
│   └── vite.config.js
├── database_schema.sql  # Database schema
├── requirements.txt     # Python dependencies
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL Server
- Git

## Step 1: Database Setup

### 1.1 Create MySQL Database

```bash
mysql -u root -p
```

In MySQL console:

```sql
CREATE DATABASE game_server CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 1.2 Load Schema

```bash
mysql -u root -p game_server < database_schema.sql
```

Or manually run the SQL file contents in MySQL console.

### 1.3 Verify Database

```bash
mysql -u root -p game_server -e "SHOW TABLES;"
```

You should see: `matches` and `users` tables.

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=game_server

# Frontend URL
FRONTEND_URL=http://localhost:5173
```

### 2.5 Test Backend Server

```bash
python -m uvicorn main:app --reload
```

The server should start at `http://localhost:8000`

Visit `http://localhost:8000/docs` to see the interactive API documentation.

## Step 3: Frontend Setup

### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 3.2 Create Environment File

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

### 3.3 Install Dependencies

```bash
npm install
```

### 3.4 Run Development Server

```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

## Step 4: Test the Integration

### 4.1 Test Registration

1. Go to `http://localhost:5173`
2. Click "Create Account"
3. Enter:
   - Username: `testplayer`
   - Password: `password123`
   - Confirm Password: `password123`
4. Click "Register"

Expected: You should be redirected to the profile page.

### 4.2 Test Login

1. Logout or go to `http://localhost:5173/login`
2. Enter:
   - Username: `testplayer`
   - Password: `password123`
3. Click "Login"

Expected: You should see your profile page with character stats.

### 4.3 Test Matchmaking

1. From profile page, click "Find Match"
2. Click "Find Opponent"

Expected: You should see opponent data loaded from the database.

### 4.4 Test Match History

1. From profile page, click "Match History"

Expected: You should see a table of matches (if any exist).

### 4.5 Check Database

```bash
mysql -u root -p game_server
```

```sql
SELECT * FROM users;
SELECT * FROM matches;
```

## Troubleshooting

### Frontend can't connect to backend

**Problem:** "Failed to find match" or CORS errors

**Solution:**
1. Ensure backend is running: `http://localhost:8000/health`
2. Check CORS configuration in `backend/main.py`
3. Verify `VITE_API_URL` in frontend `.env`

### Database connection failed

**Problem:** "Error: Database connection closed" or similar

**Solution:**
1. Verify MySQL is running
2. Check `.env` database credentials
3. Ensure `game_server` database exists
4. Check connection with: `mysql -u root -p game_server -e "SELECT 1;"`

### API returns 500 error

**Problem:** Internal Server Error from backend

**Solution:**
1. Check backend console for error messages
2. Verify database tables exist: `SHOW TABLES;`
3. Check user data is being inserted: `SELECT * FROM users;`

### Port already in use

**Problem:** "Address already in use"

**Solution:**
- Change port in vite.config.js for frontend (port 5173)
- Change port in main.py for backend (port 8000)

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user

### User
- `GET /user/{user_id}` - Get user profile

### Match
- `POST /match` - Find and start match
- `GET /match/history/{user_id}` - Get match history
- `GET /match/{match_id}` - Get specific match

### System
- `GET /health` - Health check
- `GET /` - API info

All endpoints return JSON with standard response format.

## Development Workflow

1. **Start MySQL:**
   ```bash
   # Windows (if installed as service)
   net start MySQL80
   
   # macOS (if installed with Homebrew)
   brew services start mysql
   ```

2. **Terminal 1 - Backend:**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python -m uvicorn main:app --reload
   ```

3. **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Terminal 3 - Database Monitoring (optional):**
   ```bash
   mysql -u root -p game_server
   SELECT * FROM users; -- Check periodically
   ```

## Deployment (Production)

### Backend
```bash
# Build
python -m venv venv_prod
source venv_prod/bin/activate
pip install -r requirements.txt

# Run with Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

### Frontend
```bash
npm run build
# Deploy 'dist' folder to static hosting or server
```

## Next Steps

1. Add WebSocket support for real-time battles
2. Implement game mechanics (turn-based combat)
3. Add leaderboard
4. Implement player profiles and character customization
5. Add friend system
6. Implement seasonal rankings

## Support

For issues or questions, check:
1. Console error messages in browser DevTools
2. Backend server logs
3. MySQL error logs
4. GitHub issues (if applicable)

---

Happy gaming! 🎮
