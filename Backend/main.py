"""
FastAPI backend for Suraksha Agent - A security analysis service.
Routes: GET /health, POST /analyze-message, POST /analyze-url
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
# Import agents and models
from models import (
    AnalyzeMessageRequest,
    AnalyzeUrlRequest,
    RiskAnalysisResponse,
    HealthResponse,
)
from message_agent import MessageAgent
from url_agent import URLAgent
from risk_engine import RiskEngine
from guidance_agent import GuidanceAgent
from privacy_scrubber import scrub_sensitive_data

# Initialize FastAPI app
app = FastAPI(
    title="Suraksha Agent",
    description="Security analysis backend for phishing, scams, and malware detection",
    version="1.0.0",
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents and engines
message_agent = MessageAgent()
url_agent = URLAgent()
risk_engine = RiskEngine()
guidance_agent = GuidanceAgent()


def _simple_severity_label(risk_score: float) -> str:
    """Map a numeric score to the simple labels used in the frontend response."""
    if risk_score >= 65:
        return "high_risk"
    if risk_score >= 25:
        return "suspicious"
    return "safe"


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse with service status
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
    )


@app.post("/analyze-message", response_model=RiskAnalysisResponse)
async def analyze_message(request: AnalyzeMessageRequest) -> RiskAnalysisResponse:
    """
    Analyze a message for security risks (phishing, scams, spam).
    
    Args:
        request: AnalyzeMessageRequest containing message and optional user_id
        
    Returns:
        RiskAnalysisResponse with risk assessment
        
    Raises:
        HTTPException: If message is invalid or analysis fails
    """
    try:
        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # P0 FIX: Scrub input BEFORE analysis
        scrubbed_message = scrub_sensitive_data(request.message)
        
        # Analyze the message
        analysis = message_agent.analyze(scrubbed_message)
        category = analysis["category"]
        risk_score = analysis["risk_score"]
        reasons = analysis["reasons"]
        severity = _simple_severity_label(risk_score)

        # Guidance agent returns short, action-focused advice.
        advice = guidance_agent.get_detailed_guidance(
            category=category,
            risk_score=risk_score,
            severity=severity,
            reasons=reasons,
        )

        # Scrub sensitive data from reasons for privacy (double-check)
        scrubbed_reasons = [scrub_sensitive_data(reason) for reason in reasons]
        
        return RiskAnalysisResponse(
            category=category,
            risk_score=round(risk_score, 2),
            severity=severity,
            reasons=scrubbed_reasons,
            advice=advice,
            scrubbed_text=scrubbed_message,
            timestamp=datetime.utcnow().isoformat(),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing message: {str(e)}"
        )


@app.post("/analyze-url", response_model=RiskAnalysisResponse)
async def analyze_url(request: AnalyzeUrlRequest) -> RiskAnalysisResponse:
    """
    Analyze a URL for security risks (malware, phishing, suspicious characteristics).
    
    Args:
        request: AnalyzeUrlRequest containing URL and optional user_id
        
    Returns:
        RiskAnalysisResponse with risk assessment
        
    Raises:
        HTTPException: If URL is invalid or analysis fails
    """
    try:
        # P0 FIX: Scrub input BEFORE analysis
        url_str = scrub_sensitive_data(str(request.url))
        
        # Analyze the URL
        analysis = url_agent.analyze(url_str)
        category = analysis["category"]
        risk_score = analysis["risk_score"]
        reasons = analysis["reasons"]
        severity = analysis["severity"]
        suspicious_flags = analysis["flags"]

        # Keep URL guidance short and action-focused too.
        advice = guidance_agent.get_detailed_guidance(
            category=category,
            risk_score=risk_score,
            severity=severity,
            reasons=reasons,
        )
        
        # P1 FIX: Scrub sensitive data from reasons for privacy
        scrubbed_reasons = [scrub_sensitive_data(reason) for reason in reasons]
        
        return RiskAnalysisResponse(
            category=category,
            risk_score=round(risk_score, 2),
            severity=severity,
            reasons=scrubbed_reasons,
            advice=advice,
            url=str(request.url),
            suspicious_flags=suspicious_flags,
            scrubbed_text=url_str,
            timestamp=datetime.utcnow().isoformat(),
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing URL: {str(e)}"
        )


# Root endpoint for documentation
@app.get("/")
async def root() -> dict:
    """
    Root endpoint with API information.
    
    Returns:
        Dictionary with API details and endpoint information
    """
    return {
        "name": "Suraksha Agent API",
        "version": "1.0.0",
        "description": "Security analysis backend for phishing, scams, and malware detection",
        "endpoints": {
            "GET /health": "Health check",
            "POST /analyze-message": "Analyze message for security risks",
            "POST /analyze-url": "Analyze URL for security risks",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "Alternative API documentation (ReDoc)",
        },
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
