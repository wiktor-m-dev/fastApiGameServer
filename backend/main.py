from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .schemas import RegisterRequest, LoginRequest, AuthResponse, UserResponse, MatchRequest, MatchResponse, MatchHistoryEntry
from .database import db

load_dotenv()

app = FastAPI(title="Game Server", version="1.0.0")

# Add CORS middleware FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Root
@app.get("/")
async def root():
    return {"message": "Game Server API"}

# Auth Endpoints
@app.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    try:
        user = db.create_user(request.username, request.password)
        if not user:
            raise HTTPException(status_code=400, detail="Username exists or invalid")
        return AuthResponse(
            status="success",
            message="Registered",
            user_id=user['user_id'],
            username=user['username']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    try:
        user = db.authenticate_user(request.username, request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return AuthResponse(
            status="success",
            message="Logged in",
            user_id=user['user_id'],
            username=user['username']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User Endpoint
@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    try:
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(
            user_id=user['user_id'],
            username=user['username'],
            level=user.get('level', 1),
            attack=user.get('attack', 10),
            defense=user.get('defense', 10),
            health=user.get('health', 100)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Match Queue Endpoints
@app.post("/queue/join")
async def join_queue(request: MatchRequest):
    try:
        user = db.get_user(request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user is already in an active match
        existing_match = db.get_active_match(request.user_id)
        if existing_match:
            opponent_id = existing_match['player2_id'] if existing_match['player1_id'] == request.user_id else existing_match['player1_id']
            opponent = db.get_user(opponent_id)
            return {
                "status": "matched",
                "message": "Already in a match!",
                "match_id": existing_match['match_id'],
                "opponent": {
                    "user_id": opponent['user_id'],
                    "username": opponent['username'],
                    "level": opponent.get('level', 1),
                    "attack": opponent.get('attack', 10),
                    "defense": opponent.get('defense', 10),
                    "health": opponent.get('health', 100)
                }
            }
        
        # Add to queue
        db.add_to_queue(request.user_id)
        
        # Try to find an opponent
        opponent = db.find_opponent_in_queue(request.user_id)
        
        if opponent:
            # Check if opponent is already in an active match (race condition check)
            opponent_match = db.get_active_match(opponent['user_id'])
            if opponent_match:
                # Opponent was already matched, return queued status
                return {"status": "queued", "message": "Waiting for opponent..."}
            
            # Remove both from queue
            db.remove_from_queue(request.user_id)
            db.remove_from_queue(opponent['user_id'])
            
            # Create match
            match = db.create_match(request.user_id, opponent['user_id'])
            
            # Verify match was created successfully
            if not match or not match.get('match_id'):
                # If match creation failed, add user back to queue
                db.add_to_queue(request.user_id)
                return {"status": "queued", "message": "Waiting for opponent..."}
            
            return {
                "status": "matched",
                "message": "Match found!",
                "match_id": match['match_id'],
                "opponent": {
                    "user_id": opponent['user_id'],
                    "username": opponent['username'],
                    "level": opponent.get('level', 1),
                    "attack": opponent.get('attack', 10),
                    "defense": opponent.get('defense', 10),
                    "health": opponent.get('health', 100)
                }
            }
        else:
            return {"status": "queued", "message": "Waiting for opponent..."}
    except HTTPException:
        raise
    except Exception as e:
        # If an error occurs, try to remove from queue to prevent stuck users
        try:
            db.remove_from_queue(request.user_id)
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/queue/status/{user_id}")
async def queue_status(user_id: int):
    try:
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if in queue
        queue_status = db.get_queue_status(user_id)
        if queue_status:
            return {"status": "queued", "in_queue": True}
        
        # Check for active match
        match = db.get_active_match(user_id)
        if match:
            opponent_id = match['player2_id'] if match['player1_id'] == user_id else match['player1_id']
            opponent = db.get_user(opponent_id)
            return {
                "status": "matched",
                "in_queue": False,
                "match_id": match['match_id'],
                "opponent": {
                    "user_id": opponent['user_id'],
                    "username": opponent['username'],
                    "level": opponent.get('level', 1),
                    "attack": opponent.get('attack', 10),
                    "defense": opponent.get('defense', 10),
                    "health": opponent.get('health', 100)
                }
            }
        
        return {"status": "idle", "in_queue": False}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/queue/leave/{user_id}")
async def leave_queue(user_id: int):
    try:
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.remove_from_queue(user_id)
        return {"status": "success", "message": "Left queue"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/match/{match_id}")
async def get_match(match_id: int):
    try:
        match = db.get_match(match_id)
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        
        player1 = db.get_user(match['player1_id'])
        player2 = db.get_user(match['player2_id'])
        
        return {
            "match_id": match['match_id'],
            "status": match.get('status', 'active'),
            "player1": {
                "user_id": player1['user_id'],
                "username": player1['username'],
                "level": player1.get('level', 1),
                "attack": player1.get('attack', 10),
                "defense": player1.get('defense', 10),
                "health": player1.get('health', 100)
            },
            "player2": {
                "user_id": player2['user_id'],
                "username": player2['username'],
                "level": player2.get('level', 1),
                "attack": player2.get('attack', 10),
                "defense": player2.get('defense', 10),
                "health": player2.get('health', 100)
            },
            "winner_id": match.get('winner_id')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match/{match_id}/end")
async def end_match(match_id: int, user_id: int):
    try:
        match = db.get_match(match_id)
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        
        # End match with current user as winner
        db.end_match(match_id, user_id)
        match = db.get_match(match_id)
        
        return {"status": "success", "message": "Match ended", "winner_id": match.get('winner_id')}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/match/history/{user_id}")
async def get_history(user_id: int):
    try:
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        matches = db.get_match_history(user_id)
        return {"status": "success", "matches": matches or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
