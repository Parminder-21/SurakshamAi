"""
Pydantic models for request and response validation.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


class AnalyzeMessageRequest(BaseModel):
    """Request model for message analysis."""
    message: str = Field(..., min_length=1, max_length=5000, description="The message to analyze")
    user_id: Optional[str] = Field(None, description="Optional user identifier")


class AnalyzeUrlRequest(BaseModel):
    """Request model for URL analysis."""
    url: HttpUrl = Field(..., description="The URL to analyze")
    user_id: Optional[str] = Field(None, description="Optional user identifier")


class RiskAnalysisResponse(BaseModel):
    """Response model for risk analysis results."""
    category: str = Field(..., description="Category of risk (e.g., phishing, scam, malware, spam)")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score from 0-100")
    severity: str = Field(..., description="Severity level (LOW, MEDIUM, HIGH, CRITICAL)")
    reasons: List[str] = Field(default_factory=list, description="List of reasons for the risk assessment")
    advice: str = Field(..., description="Actionable advice for the user")
    timestamp: str = Field(..., description="ISO format timestamp of analysis")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Status of the service")
    version: str = Field(..., description="API version")
