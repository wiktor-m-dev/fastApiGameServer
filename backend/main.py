from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from .schemas import (
    HealthCheckResponse, ErrorResponse, ErrorSeverity,
    RegisterRequest, LoginRequest, AuthResponse, UserResponse
)
from .database import DatabaseConnection

# Load environment variables
load_dotenv()

# Initialize database connection
db = DatabaseConnection()

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting FastAPI server...")
    db.connect()
    yield
    # Shutdown
    print("Shutting down FastAPI server...")
    db.disconnect()


# Create FastAPI app
app = FastAPI(
    title="Game Server API",
    description="FastAPI backend for game server with Firebase integration",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    os.getenv("FRONTEND_URL", "http://localhost:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check Endpoint
@app.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"]
)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint to verify server status and database connection.
    
    Returns:
        HealthCheckResponse: Server health status with database connection info
    """
    # Check database connection
    db_connected = db.connection is not None and db.connection.is_connected()
    
    return HealthCheckResponse(
        status="healthy",
        message="Server is running properly",
        version="1.0.0",
        database_connected=db_connected
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions"""
    error_response = ErrorResponse(
        status="error",
        message=str(exc),
        error_code="INTERNAL_ERROR",
        severity=ErrorSeverity.CRITICAL,
        details=None
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Game Server API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Authentication Endpoints
@app.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"]
)
async def register(request: RegisterRequest) -> AuthResponse:
    """
    Register a new user account.
    
    Args:
        request: RegisterRequest containing username and password
        
    Returns:
        AuthResponse: Registration status with user ID and username
    """
    # Check if user already exists
    if db.user_exists(request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Create new user
    user = db.create_user(request.username, request.password)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user"
        )
    
    return AuthResponse(
        status="success",
        message="User registered successfully",
        user_id=user['user_id'],
        username=user['username']
    )


@app.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    tags=["Authentication"]
)
async def login(request: LoginRequest) -> AuthResponse:
    """
    Authenticate a user with username and password.
    
    Args:
        request: LoginRequest containing username and password
        
    Returns:
        AuthResponse: Login status with user ID and username
    """
    # Authenticate user
    user = db.authenticate_user(request.username, request.password)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return AuthResponse(
        status="success",
        message="Login successful",
        user_id=user['user_id'],
        username=user['username']
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
