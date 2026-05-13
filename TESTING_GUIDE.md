# Testing Guide - Complete Walkthrough

## Prerequisites
- MySQL running with `game_server` database created
- Backend virtual environment set up
- Frontend dependencies installed

## Part 1: Backend Testing

### 1.1 Start Backend Server

```bash
cd backend
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

python -m uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 1.2 Test Health Endpoint

Visit `http://localhost:8000/health`

Expected response:
```json
{
  "status": "healthy",
  "message": "Server is running properly",
  "version": "1.0.0",
  "database_connected": true
}
```

### 1.3 Access API Documentation

Visit `http://localhost:8000/docs`

You should see an interactive Swagger UI with all endpoints listed.

### 1.4 Test Registration Endpoint

In Swagger UI:
1. Find `/register` endpoint
2. Click "Try it out"
3. Enter:
```json
{
  "username": "testplayer1",
  "password": "password123"
}
```
4. Click "Execute"

Expected response (201):
```json
{
  "status": "success",
  "message": "User registered successfully",
  "user_id": 1,
  "username": "testplayer1"
}
```

### 1.5 Test Login Endpoint

In Swagger UI:
1. Find `/login` endpoint
2. Click "Try it out"
3. Enter same username/password from registration
4. Click "Execute"

Expected response (200):
```json
{
  "status": "success",
  "message": "Login successful",
  "user_id": 1,
  "username": "testplayer1"
}
```

### 1.6 Test User Profile Endpoint

In Swagger UI:
1. Find `/user/{user_id}` endpoint
2. Click "Try it out"
3. Enter `user_id: 1`
4. Click "Execute"

Expected response (200):
```json
{
  "user_id": 1,
  "username": "testplayer1",
  "character_name": null,
  "level": 1,
  "attack": 10,
  "defense": 10,
  "health": 100
}
```

### 1.7 Create Second User (for matchmaking)

Register another user:
- Username: `testplayer2`
- Password: `password123`

This should return `user_id: 2`

### 1.8 Test Matchmaking Endpoint

In Swagger UI:
1. Find `/match` endpoint
2. Click "Try it out"
3. Enter:
```json
{
  "user_id": 1
}
```
4. Click "Execute"

Expected response (200):
```json
{
  "status": "success",
  "message": "Match found successfully",
  "match_id": 1,
  "match_status": "in_progress",
  "opponent": {
    "user_id": 2,
    "username": "testplayer2",
    "character_name": null,
    "level": 1,
    "attack": 10,
    "defense": 10,
    "health": 100
  }
}
```

### 1.9 Test Match History Endpoint

In Swagger UI:
1. Find `/match/history/{user_id}` endpoint
2. Click "Try it out"
3. Enter `user_id: 1`
4. Click "Execute"

Expected response (200):
```json
{
  "status": "success",
  "message": "Match history retrieved successfully",
  "total_matches": 1,
  "matches": [
    {
      "match_id": 1,
      "player1_id": 1,
      "player2_id": 2,
      "status": "in_progress",
      "winner_id": null,
      "player1_damage": 0,
      "player2_damage": 0,
      "created_at": "2026-05-13T10:30:00",
      "completed_at": null
    }
  ]
}
```

### 1.10 Verify Database Inserts

Open MySQL console:
```bash
mysql -u root -p game_server
```

Check users:
```sql
SELECT * FROM users;
```

Expected output:
```
+--------+---------------+----+----------+-------+--------+--------+
| user_id| username      | ... | level   | attack| defense| health |
+--------+---------------+----+----------+-------+--------+--------+
| 1      | testplayer1   | ... | 1       | 10    | 10     | 100    |
| 2      | testplayer2   | ... | 1       | 10    | 10     | 100    |
+--------+---------------+----+----------+-------+--------+--------+
```

Check matches:
```sql
SELECT * FROM matches;
```

Expected output:
```
+--------+----------+----------+--------+----------+
|match_id|player1_id|player2_id|status      |
+--------+----------+----------+--------+----------+
| 1      | 1        | 2        | in_progress|
+--------+----------+----------+--------+----------+
```

## Part 2: Frontend Testing

### 2.1 Start Frontend Server

In new terminal:
```bash
cd frontend
npm run dev
```

Expected output:
```
VITE v5.0.0  ready in XXX ms

➜  Local:   http://localhost:5173/
```

### 2.2 Test Home Page

Visit `http://localhost:5173`

You should see:
- "Welcome to the RPG Realm" heading
- "Login" and "Create Account" buttons
- Navbar with FastAPI RPG branding

### 2.3 Test Registration Page

1. Click "Create Account" button
2. You should be redirected to `http://localhost:5173/register`
3. Fill in:
   - Username: `frontenduser1`
   - Password: `password123`
   - Confirm: `password123`
4. Click "Register"

Expected:
- Account created
- Redirected to profile page
- User info displayed

### 2.4 Test Login Page

1. Click logout or navigate to `http://localhost:5173/login`
2. You should see login form
3. Enter:
   - Username: `frontenduser1`
   - Password: `password123`
4. Click "Login"

Expected:
- Logged in successfully
- Redirected to profile page
- User info displayed

### 2.5 Test Profile Page

On profile page, you should see:
- Username displayed
- Character stats: Health, Attack, Defense
- Three buttons: "Find Match", "Match History", "Logout"
- Stats should match database values

### 2.6 Test Matchmaking

1. From profile page, click "Find Match"
2. You should be redirected to `http://localhost:5173/matchmaking`
3. See "Find Opponent" button
4. Click "Find Opponent"

Expected:
- Loading spinner appears
- Opponent data loads
- VS screen shows:
  - Your character (testplayer1)
  - Opponent character (testplayer2)
  - Both characters' stats

### 2.7 Test Match History

1. From profile page, click "Match History"
2. You should be redirected to `http://localhost:5173/match-history`
3. See table with matches

Expected:
- Table shows match ID
- Shows player IDs
- Shows match status
- Shows creation date

### 2.8 Test Navigation

Try all navbar links:
- "Profile" → Should go to `/profile`
- "Matchmaking" → Should go to `/matchmaking`
- "History" → Should go to `/match-history`
- "Logout" → Should logout and redirect to login

### 2.9 Test Protected Routes

1. Logout (or open private window)
2. Try accessing `http://localhost:5173/profile` directly
3. You should be redirected to login page

Expected: Cannot access protected routes without authentication

## Part 3: Full Integration Testing

### 3.1 Complete User Journey

1. **Start at home:** `http://localhost:5173`
2. **Register:** Click "Create Account"
   - Username: `integrationtest`
   - Password: `test12345`
3. **View profile:** Should see character with stats
4. **Find match:** Click "Find Match" → "Find Opponent"
   - Should see opponent data from database
5. **View history:** Click "Back" → "Match History"
   - Should see the match created
6. **Logout:** Click "Logout"
7. **Login:** Login with same credentials
   - Should retrieve same user from database

### 3.2 Test Error Handling

Test error scenarios:

**Duplicate username:**
1. Try registering with same username twice
2. Expected: "Username already exists" error

**Invalid login:**
1. Try logging in with wrong password
2. Expected: "Invalid username or password" error

**Non-existent user:**
1. Via Swagger: Try `/user/999`
2. Expected: 404 "User not found"

**No opponents:**
1. Clear all other users from database
2. Try finding match
3. Expected: "No opponents available" error

### 3.3 Test CORS

Backend should accept requests from frontend without CORS errors.

Check browser console (F12 → Console tab):
- Should NOT see CORS-related errors
- Network tab should show 200/201 status codes

## Part 4: Database Verification

### 4.1 Verify Data Integrity

```sql
-- Check password is hashed
SELECT user_id, username, LEFT(password, 20) AS password_hash FROM users;

-- Check matches have correct player IDs
SELECT * FROM matches WHERE player1_id = 1;

-- Check timestamps are recorded
SELECT match_id, created_at FROM matches ORDER BY created_at DESC;
```

### 4.2 Check Foreign Keys

```sql
-- This should fail (referential integrity)
INSERT INTO matches (player1_id, player2_id) VALUES (999, 999);

-- This should succeed
INSERT INTO matches (player1_id, player2_id) VALUES (1, 2);
```

## Troubleshooting

### Frontend can't connect to backend

**Error:** "Failed to find match" or network errors

**Checks:**
1. Backend running? `curl http://localhost:8000/health`
2. CORS enabled? Check backend console
3. API URL correct? Check frontend `.env`
4. Firewall blocking? Try without VPN

### Database errors

**Error:** "Database connection closed"

**Checks:**
1. MySQL running? `mysql -u root -p`
2. Database exists? `mysql -u root -p -e "SHOW DATABASES;"`
3. Tables exist? `mysql -u root -p game_server -e "SHOW TABLES;"`
4. Credentials correct in `.env`?

### Password hashing issues

**Error:** "Invalid username or password"

**Checks:**
1. Password stored as hash in database
2. Try login after fresh registration
3. Check bcrypt version compatibility

### Port conflicts

**Error:** "Address already in use"

**Solution:**
- Backend: Change port in `main.py`
- Frontend: Change port in `vite.config.js`

## Performance Testing

### Load Testing (optional)

Test with multiple users:

```bash
# Register 5 users via Swagger
for i in {1..5}; do
  # Register user_$i
done

# Check database load
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM matches;

# Try concurrent matches
# Find match from user 1, 2, 3 simultaneously
```

## Success Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Health check returns healthy
- [ ] Can register new user
- [ ] User data saved in database
- [ ] Can login with registered account
- [ ] Profile page displays correct stats
- [ ] Can find opponent
- [ ] Match created in database
- [ ] Can view match history
- [ ] Navigation works correctly
- [ ] Protected routes redirect to login
- [ ] Logout clears session
- [ ] No CORS errors in console
- [ ] Database integrity maintained

---

**All tests passing = System Ready for Development! 🎉**
