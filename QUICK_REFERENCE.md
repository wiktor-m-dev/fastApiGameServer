# Quick Reference - FastAPI Game Server

## 🚀 Quick Start

### Windows
```bash
start-windows.bat
```

### macOS/Linux
```bash
chmod +x start-linux-mac.sh
./start-linux-mac.sh
```

### Manual
```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: MySQL (if needed)
mysql -u root -p game_server
```

## 📍 URLs

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend | http://localhost:5173 | React app |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | Alternative API docs |

## 🔌 API Endpoints

### Authentication
```
POST /register
  body: { username, password }
  
POST /login
  body: { username, password }
```

### User
```
GET /user/{user_id}
```

### Matches
```
POST /match
  body: { user_id }
  
GET /match/history/{user_id}
```

### System
```
GET /health
GET /
```

## 📁 Project Files

### Backend
```
backend/
├── main.py          # FastAPI app & endpoints
├── database.py      # MySQL queries & operations
├── schemas.py       # Pydantic models
├── requirements.txt # Python dependencies
└── .env             # Configuration
```

### Frontend
```
frontend/
├── src/
│   ├── pages/              # Page components
│   ├── services/api.js     # API calls
│   ├── hooks/useAuth.jsx   # Auth state
│   ├── components/         # UI components
│   └── App.jsx             # Router setup
├── package.json
└── .env
```

### Database
```
database_schema.sql  # Table definitions
```

## 🗄️ Database Tables

### users
```sql
- user_id (PRIMARY KEY)
- username (UNIQUE)
- password (bcrypt hash)
- character_name
- level, attack, defense, health
- created_at, updated_at
```

### matches
```sql
- match_id (PRIMARY KEY)
- player1_id, player2_id (FOREIGN KEY)
- status (enum)
- winner_id
- player1_damage, player2_damage
- created_at, completed_at
```

## 🔐 Authentication

- Password hashing: **bcrypt**
- Session storage: **localStorage** (frontend)
- CORS: **localhost:5173** (frontend)

## 📦 Key Dependencies

### Backend
- fastapi==0.104.1
- uvicorn==0.24.0
- mysql-connector-python==8.2.0
- bcrypt==4.1.1
- pydantic==2.5.0

### Frontend
- react==19.2.5
- react-router-dom==6.20.0
- react-bootstrap==2.10.10
- bootstrap==5.3.8

## 🧪 Testing

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for complete testing walkthrough

Quick test:
```bash
# 1. Register user
# 2. Login
# 3. View profile
# 4. Find match
# 5. Check history
```

## ⚙️ Configuration

### Backend (.env)
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=game_server
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Can't connect to backend" | Verify backend running at :8000 and CORS configured |
| "Database connection failed" | Check MySQL running, credentials in .env, database exists |
| "Port already in use" | Change port in vite.config.js (frontend) or main.py (backend) |
| "CORS error" | Ensure FRONTEND_URL in backend .env matches frontend URL |

## 📝 Common Commands

### Backend
```bash
# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload

# Run tests (when added)
pytest
```

### Frontend
```bash
# Install dependencies
npm install

# Development
npm run dev

# Build
npm run build

# Preview
npm run preview

# Lint
npm run lint
```

### Database
```bash
# Create database
mysql -u root -p < database_schema.sql

# Access database
mysql -u root -p game_server

# Check tables
SHOW TABLES;

# Check users
SELECT * FROM users;

# Check matches
SELECT * FROM matches;
```

## 🎯 Data Flow

### Registration
```
Frontend Form → Backend /register → Hash Password → Save User → Return user_id
```

### Login
```
Frontend Form → Backend /login → Verify Password → Return user_id → Store in context
```

### Find Match
```
Button Click → POST /match → Find Opponent → Create Match → Return opponent data
```

### View Profile
```
GET /user/{user_id} → Query Database → Return Stats → Display on page
```

## 📚 Documentation

- [README.md](README.md) - Project overview
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Setup instructions
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing walkthrough
- [INTEGRATION_CHECKLIST.md](INTEGRATION_CHECKLIST.md) - Feature checklist

## 🔄 Git Workflow

```bash
# Create branch
git checkout -b feature/your-feature

# Commit
git add .
git commit -m "feature: description"

# Push
git push origin feature/your-feature

# Pull request (GitHub)
```

## 📊 API Response Format

### Success
```json
{
  "status": "success",
  "message": "Operation completed",
  "data": { /* ... */ }
}
```

### Error
```json
{
  "status": "error",
  "message": "Error description",
  "error_code": "ERROR_CODE",
  "severity": "error"
}
```

## 🚨 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful request |
| 201 | Created | User registered |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Wrong password |
| 404 | Not Found | User doesn't exist |
| 500 | Server Error | Database error |

## 💡 Tips

1. **Use Swagger UI** (`/docs`) to test API endpoints
2. **Check browser console** (F12) for frontend errors
3. **Check backend terminal** for server logs
4. **Use MySQL console** to verify database changes
5. **Use VS Code extensions** for better development experience
6. **Enable debug mode** for verbose logging
7. **Use Postman** for advanced API testing

## 🎓 Next Features to Implement

- [ ] Battle system
- [ ] Experience & leveling
- [ ] Leaderboard
- [ ] WebSockets for real-time updates
- [ ] Friend system
- [ ] Chat
- [ ] Tournaments

---

**Status:** ✅ Fully Connected & Ready to Use
