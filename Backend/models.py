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
    severity: str = Field(..., description="Severity level (safe, suspicious, high_risk)")
    reasons: List[str] = Field(default_factory=list, description="List of reasons for the risk assessment")
    advice: str = Field(..., description="Actionable advice for the user")
    url: Optional[str] = Field(None, description="Original or analyzed URL for URL analyses")
    suspicious_flags: List[str] = Field(default_factory=list, description="Suspicious URL flags for URL analyses")
    scrubbed_text: Optional[str] = Field(None, description="Scrubbed version of the analyzed message or URL")
    timestamp: str = Field(..., description="ISO format timestamp of analysis")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Status of the service")
    version: str = Field(..., description="API version")

class AnalyzeCallRequest(BaseModel):
    """Request model for call summary analysis."""
    call_summary: str = Field(..., min_length=1, max_length=5000, description="The summary or transcript of the call")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class ReportScamRequest(BaseModel):
    """Request model for community scam reporting."""
    content: str = Field(..., description="The message, URL, or call summary being reported")
    category: str = Field(..., description="The scam category reported by the user")
    evidence: Optional[str] = Field(None, description="Any additional context or evidence")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class SubmitSampleRequest(BaseModel):
    """Request model for submitting data for training."""
    scrubbed_content: str = Field(..., description="The already scrubbed message or URL")
    label: str = Field(..., description="The known true scam category")

class NewsFeedArticle(BaseModel):
    """Model for a single trending scam article."""
    id: str
    title: str
    category: str
    description: str
    reported_count: int
    date: str

class NewsFeedResponse(BaseModel):
    """Response model for trending scams feed."""
    articles: List[NewsFeedArticle]
