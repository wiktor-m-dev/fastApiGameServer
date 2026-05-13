# Fast API Game Server - RPG Edition

## Project Overview
A complete multiplayer RPG game server with real-time matchmaking, user authentication, and character progression. Built with FastAPI backend, React frontend, and MySQL database.

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **MySQL** - Relational database for users and matches
- **Pydantic** - Data validation using Python type annotations
- **BCrypt** - Password hashing and security

### Frontend
- **React 19** - JavaScript library for building user interfaces
- **React Router** - Client-side routing
- **React Bootstrap** - Responsive UI components
- **Vite** - Next generation frontend tooling

### Database
- **MySQL 8.0+** - Relational database with user and match tables

## Features

### User Management
- **Login/Register** - Secure user authentication with bcrypt password hashing
- **User Profiles** - View and manage character stats and progression

### Character Management
- **Character Stats** - Health, Attack, Defense, Level
- **Dynamic Stats** - Stats can be adjusted based on gameplay

### Game Mechanics
- **Matchmaking System** - Find opponents and initiate matches
- **Match History** - View past matches and results
- **Real-time Opponent Info** - See opponent stats before battle

## Project Structure

```
fastApiGameServer/
├── backend/
│   ├── main.py              # FastAPI app and endpoints
│   ├── database.py          # MySQL connection and queries
│   ├── schemas.py           # Pydantic models
│   ├── requirements.txt      # Python dependencies
│   └── .env.example         # Environment template
├── frontend/
│   ├── src/
│   │   ├── pages/           # Login, Register, Profile, Matchmaking
│   │   ├── services/        # API communication
│   │   ├── hooks/           # useAuth custom hook
│   │   ├── components/      # Navbar, etc
│   │   └── App.jsx          # Main routing
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
├── database_schema.sql      # Database table definitions
├── INTEGRATION_GUIDE.md     # Complete setup instructions
├── start-windows.bat        # Quick start script (Windows)
└── start-linux-mac.sh       # Quick start script (macOS/Linux)
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL Server running
- Git

### Option 1: Quick Start Scripts

**Windows:**
```bash
start-windows.bat
```

**macOS/Linux:**
```bash
chmod +x start-linux-mac.sh
./start-linux-mac.sh
```

### Option 2: Manual Setup

#### 1. Database Setup
```bash
mysql -u root -p
CREATE DATABASE game_server;
```
```bash
mysql -u root -p game_server < database_schema.sql
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` file in backend:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=game_server
FRONTEND_URL=http://localhost:5173
```

Run backend:
```bash
python -m uvicorn main:app --reload
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
```

Create `.env` file in frontend:
```env
VITE_API_URL=http://localhost:8000
```

Run frontend:
```bash
npm run dev
```

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user

### User
- `GET /user/{user_id}` - Get user profile and stats

### Matches
- `POST /match` - Find opponent and create match
- `GET /match/history/{user_id}` - Get user's match history

### System
- `GET /health` - Health check
- `GET /` - API information

Interactive API documentation available at `http://localhost:8000/docs`

## Usage

1. **Register Account**
   - Navigate to `http://localhost:5173/register`
   - Create username and password
   - Account created with default stats (Health: 100, Attack: 10, Defense: 10)

2. **Login**
   - Use credentials to login
   - View your profile with character stats

3. **Find Match**
   - Click "Find Opponent"
   - See opponent's stats
   - Match created in database

4. **View History**
   - See all past matches
   - View match status and details

## Development

### File Structure
- Backend routing in `backend/main.py`
- Frontend routing in `frontend/src/App.jsx`
- API calls in `frontend/src/services/api.js`
- Auth state in `frontend/src/hooks/useAuth.jsx`

### Database Schema
- `users` table: User accounts and character stats
- `matches` table: Match history and results

### Adding New Features

1. **Backend**: Add endpoint in `main.py`, create schema in `schemas.py`
2. **Database**: Add method in `database.py`
3. **Frontend**: Create page component, add API call in `services/api.js`

## Troubleshooting

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for detailed troubleshooting and setup information.

## Next Steps

- [ ] Implement turn-based combat system
- [ ] Add leaderboard
- [ ] Add WebSocket for real-time updates
- [ ] Implement character upgrades
- [ ] Add friend system
- [ ] Add seasonal rankings
- [ ] Deploy to production

## License

MIT

---

For detailed integration guide and troubleshooting, see [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **Combat System** - Battle mechanics where stats influence win probability
- **Stat Progression** - Winners can upgrade one of two stats (Defense or Attack)
- **Probability-Based Outcomes** - Players with better stats have higher chances of winning

### Database structure
```
CREATE TABLE `users` (
  `user_id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `character_name` VARCHAR(50) DEFAULT NULL,
  `level` INT DEFAULT 1,
  `attack` INT DEFAULT 10,
  `defense` INT DEFAULT 10,
  `health` INT DEFAULT 100
)
```
