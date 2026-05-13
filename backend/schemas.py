from pydantic import BaseModel
from typing import Optional

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    status: str
    message: str
    user_id: Optional[int] = None
    username: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    level: int
    attack: int
    defense: int
    health: int

class MatchRequest(BaseModel):
    user_id: int

class MatchResponse(BaseModel):
    status: str
    message: str
    match_id: Optional[int] = None
    opponent: Optional[dict] = None

class MatchHistoryEntry(BaseModel):
    match_id: int
    opponent_username: str
    result: str
