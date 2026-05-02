"""
FastAPI backend for Suraksha Agent - A security analysis service.
Routes: GET /health, POST /analyze-message, POST /analyze-url, POST /analyze (StateGraph)
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
    AnalyzeCallRequest,
    ReportScamRequest,
    SubmitSampleRequest,
    NewsFeedResponse,
    NewsFeedArticle
)
from orchestrator import analyze_input

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
        result = analyze_input(request.message, input_type="message")
        
        return RiskAnalysisResponse(
            category=result.get("detected_category", "safe"),
            risk_score=round(float(result.get("risk_score", 0.0)), 2),
            severity=result.get("severity", "safe"),
            reasons=result.get("reasons", []),
            advice=result.get("advice", ""),
            scrubbed_text=result.get("scrubbed_text", ""),
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
        raw_url = str(request.url)
        result = analyze_input(raw_url, input_type="url")
        
        return RiskAnalysisResponse(
            category=result.get("detected_category", "safe"),
            risk_score=round(float(result.get("risk_score", 0.0)), 2),
            severity=result.get("severity", "safe"),
            reasons=result.get("reasons", []),
            advice=result.get("advice", ""),
            url=raw_url,
            suspicious_flags=result.get("suspicious_flags", []),
            scrubbed_text=result.get("scrubbed_text", ""),
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
            "POST /analyze": "Unified StateGraph-based analysis (message or URL)",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "Alternative API documentation (ReDoc)",
        },
    }


@app.post("/analyze", response_model=RiskAnalysisResponse)
async def analyze_unified(request: AnalyzeMessageRequest | AnalyzeUrlRequest) -> RiskAnalysisResponse:
    """
    Unified LangGraph-powered analysis endpoint.
    Auto-detects input_type based on request fields.
    
    Args:
        request: Either AnalyzeMessageRequest or AnalyzeUrlRequest
        
    Returns:
        RiskAnalysisResponse with unified analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Determine input type based on which field is present
        if hasattr(request, "url") and request.url:
            input_type = "url"
            raw_text = str(request.url)
        else:
            input_type = "message"
            raw_text = request.message
        
        # Run through StateGraph orchestrator
        result = analyze_input(raw_text, input_type=input_type)
        
        return RiskAnalysisResponse(
            category=result.get("detected_category", "safe"),
            risk_score=round(float(result.get("risk_score", 0.0)), 2),
            severity=result.get("severity", "safe"),
            reasons=result.get("reasons", []),
            advice=result.get("advice", ""),
            scrubbed_text=result.get("scrubbed_text", ""),
            url=raw_text if input_type == "url" else None,
            suspicious_flags=result.get("suspicious_flags", []),
            timestamp=datetime.utcnow().isoformat(),
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in unified analysis: {str(e)}"
        )


@app.post("/analyze-call", response_model=RiskAnalysisResponse)
async def analyze_call(request: AnalyzeCallRequest) -> RiskAnalysisResponse:
    """Analyze a call transcript or summary."""
    try:
        # Reusing analyze_input as a placeholder for Call Context Agent
        result = analyze_input(request.call_summary, input_type="message")
        return RiskAnalysisResponse(
            category=result.get("detected_category", "safe"),
            risk_score=round(float(result.get("risk_score", 0.0)), 2),
            severity=result.get("severity", "safe"),
            reasons=result.get("reasons", []),
            advice=result.get("advice", ""),
            scrubbed_text=result.get("scrubbed_text", ""),
            timestamp=datetime.utcnow().isoformat(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report-scam")
async def report_scam(request: ReportScamRequest) -> dict:
    """Submit a scam to the community reporting database."""
    # In a real app, save to Database. For hackathon MVP, return success.
    return {"status": "success", "message": "Scam reported successfully. Thank you for protecting the community."}

@app.post("/submit-sample")
async def submit_sample(request: SubmitSampleRequest) -> dict:
    """Submit a scrubbed sample to the training pipeline."""
    return {"status": "success", "message": "Sample ingested for model fine-tuning."}

@app.get("/news-feed", response_model=NewsFeedResponse)
async def news_feed() -> NewsFeedResponse:
    """Get the trending scams feed for the app and website."""
    # Hardcoded trending scams for MVP presentation
    articles = [
        NewsFeedArticle(
            id="1",
            title="Fake KYC via WhatsApp",
            category="fake_kyc",
            description="Users are receiving WhatsApp messages claiming their bank KYC is expiring today. Do not click the links.",
            reported_count=2341,
            date=datetime.utcnow().isoformat()
        ),
        NewsFeedArticle(
            id="2",
            title="Electricity Bill Scam SMS",
            category="electricity_bill_scam",
            description="Fraudsters are sending SMS threatening immediate power cut if a 'pending' bill isn't paid via their malicious link.",
            reported_count=1892,
            date=datetime.utcnow().isoformat()
        )
    ]
    return NewsFeedResponse(articles=articles)


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
