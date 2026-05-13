from pydantic import BaseModel, Field
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
