from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from enum import Enum


class ErrorSeverity(str, Enum):
    """Error severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorResponse(BaseModel):
    """Global error response schema"""
    status: str = Field(..., description="Status code")
    message: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Internal error code")
    severity: ErrorSeverity = Field(default=ErrorSeverity.ERROR, description="Error severity level")
    details: Optional[dict[str, Any]] = Field(default=None, description="Additional error details")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Internal server error",
                "error_code": "INTERNAL_ERROR",
                "severity": "error",
                "details": None
            }
        }


class SuccessResponse(BaseModel):
    """Generic success response schema"""
    status: str = Field(default="success", description="Status code")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(default=None, description="Response data")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": None
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check endpoint response"""
    status: str = Field(..., description="Server health status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")
    database_connected: bool = Field(..., description="Database connection status")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "Server is running properly",
                "version": "1.0.0",
                "database_connected": True
            }
        }


# Authentication Schemas
class RegisterRequest(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50, description="Username for the account")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "player123",
                "password": "secure_password"
            }
        }


class LoginRequest(BaseModel):
    """User login request"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "player123",
                "password": "secure_password"
            }
        }


class AuthResponse(BaseModel):
    """Authentication response with user data"""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    user_id: Optional[int] = Field(default=None, description="User ID")
    username: Optional[str] = Field(default=None, description="Username")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "User registered successfully",
                "user_id": 1,
                "username": "player123"
            }
        }


class UserResponse(BaseModel):
    """User data response"""
    user_id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    character_name: Optional[str] = Field(default=None, description="Character name")
    level: int = Field(default=1, description="Character level")
    attack: int = Field(default=10, description="Attack stat")
    defense: int = Field(default=10, description="Defense stat")
    health: int = Field(default=100, description="Health stat")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "username": "player123",
                "character_name": "Hero",
                "level": 1,
                "attack": 10,
                "defense": 10,
                "health": 100
            }
        }


# Match Schemas
class MatchStatus(str, Enum):
    """Match status states"""
    SEARCHING = "searching"
    FOUND = "found"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OpponentInfo(BaseModel):
    """Opponent player information"""
    user_id: int = Field(..., description="Opponent user ID")
    username: str = Field(..., description="Opponent username")
    character_name: Optional[str] = Field(default=None, description="Opponent character name")
    level: int = Field(default=1, description="Opponent level")
    attack: int = Field(default=10, description="Opponent attack stat")
    defense: int = Field(default=10, description="Opponent defense stat")
    health: int = Field(default=100, description="Opponent health stat")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 2,
                "username": "opponent",
                "character_name": "Warrior",
                "level": 5,
                "attack": 15,
                "defense": 12,
                "health": 120
            }
        }


class MatchRequest(BaseModel):
    """Request to find or start a match"""
    user_id: int = Field(..., description="User ID requesting match")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1
            }
        }


class MatchResponse(BaseModel):
    """Match response with opponent information"""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    match_id: Optional[int] = Field(default=None, description="Match ID")
    match_status: Optional[MatchStatus] = Field(default=None, description="Current match status")
    opponent: Optional[OpponentInfo] = Field(default=None, description="Opponent information")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Match found",
                "match_id": 1,
                "match_status": "found",
                "opponent": {
                    "user_id": 2,
                    "username": "opponent",
                    "character_name": "Warrior",
                    "level": 5,
                    "attack": 15,
                    "defense": 12,
                    "health": 120
                }
            }
        }


class MatchHistoryEntry(BaseModel):
    """Match history entry"""
    match_id: int = Field(..., description="Match ID")
    opponent_username: str = Field(..., description="Opponent username")
    opponent_level: int = Field(..., description="Opponent level")
    result: str = Field(..., description="Match result: win, loss, or draw")
    created_at: str = Field(..., description="Match creation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "match_id": 1,
                "opponent_username": "opponent",
                "opponent_level": 5,
                "result": "win",
                "created_at": "2026-05-13T10:00:00Z"
            }
        }
