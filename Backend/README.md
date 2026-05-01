# Suraksha Agent - Backend

A beginner-friendly FastAPI backend for security analysis, providing risk assessment for messages and URLs against phishing, scams, malware, and spam threats.

## Features

- 🔍 **Message Analysis**: Detect phishing, scams, and suspicious content
- 🔗 **URL Analysis**: Identify malicious URLs and suspicious domains
- 📊 **Risk Scoring**: Quantified risk assessment (0-100 scale)
- 🎯 **Severity Levels**: Clear categorization (LOW, MEDIUM, HIGH, CRITICAL)
- 💡 **Actionable Advice**: Detailed security guidance based on risk analysis
- 🔐 **Privacy Protection**: Automatic scrubbing of sensitive data
- 📚 **Modular Architecture**: Well-organized, maintainable code structure

## Project Structure

```
Backend/
├── main.py               # FastAPI application entry point
├── models.py            # Pydantic request/response models
├── message_agent.py     # Message analysis logic
├── url_agent.py         # URL analysis logic
├── risk_engine.py       # Risk scoring and severity calculation
├── guidance_agent.py    # Security guidance generation
├── privacy_scrubber.py  # Sensitive data removal utility
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Navigate to the Backend directory**:
   ```bash
   cd Backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

## Running the Server

### Development Mode (with auto-reload)

```bash
python main.py
```

Or alternatively:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### Production Mode (without auto-reload)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### 1. Health Check
Get the healthiness and version of the service.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Analyze Message
Analyze a text message for security risks.

**Endpoint**: `POST /analyze-message`

**Request Body**:
```json
{
  "message": "Click here to verify your account: http://malicious-site.com",
  "user_id": "optional-user-123"
}
```

**Response**:
```json
{
  "category": "phishing",
  "risk_score": 72.5,
  "severity": "HIGH",
  "reasons": [
    "Some phishing keywords detected (2)",
    "Message uses urgency tactics",
    "Message contains URLs that require verification"
  ],
  "advice": "🔴 HIGH RISK - Likely Phishing\nThis message shows strong phishing characteristics:\n1. Verify the sender by checking official channels\n2. Do NOT click links – instead visit websites directly in your browser\n3. Look for spelling errors and suspicious sender addresses\n4. Report phishing emails to your email provider\n5. Consider updating your password as a precaution",
  "timestamp": "2024-05-01T12:34:56.789012"
}
```

### 3. Analyze URL
Analyze a URL for malware and suspicious characteristics.

**Endpoint**: `POST /analyze-url`

**Request Body**:
```json
{
  "url": "https://bit.ly/malicious-link",
  "user_id": "optional-user-123"
}
```

**Response**:
```json
{
  "category": "malware",
  "risk_score": 55.0,
  "severity": "MEDIUM",
  "reasons": [
    "URL uses shortening service (bit.ly)"
  ],
  "advice": "🟡 MEDIUM RISK - Potential Malware\nThis URL may pose security risks:\n1. Verify the URL is legitimate before visiting\n2. Use safe browsing tools to check\n3. Keep security software updated",
  "timestamp": "2024-05-01T12:34:56.789012"
}
```

## API Documentation

Once the server is running, interactive API documentation is available:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Module Overview

### `models.py`
Defines Pydantic models for request/response validation:
- `AnalyzeMessageRequest`: Validates message input
- `AnalyzeUrlRequest`: Validates URL input
- `RiskAnalysisResponse`: Standardizes all analysis responses
- `HealthResponse`: Health check response model

### `message_agent.py`
Analyzes messages for phishing, scams, and other threats:
- Keyword-based detection
- Pattern matching for suspicious behaviors
- Sensitive data detection
- Risk score calculation

### `url_agent.py`
Analyzes URLs for malware and suspicious characteristics:
- Domain reputation checking
- File extension analysis
- URL structure validation
- IP address detection

### `risk_engine.py`
Calculates risk scores and generates severity levels:
- Combines multiple risk indicators
- Maps scores to severity levels
- Provides context-specific advice

### `guidance_agent.py`
Generates detailed, actionable security guidance:
- Category-specific advice
- Severity-level appropriate messaging
- General security tips

### `privacy_scrubber.py`
Removes sensitive information from outputs:
- Email address scrubbing
- Phone number removal
- Credit card pattern removal
- API token redaction

## Usage Examples

### Example 1: Python Client

```python
import requests
import json

# Analyze a message
response = requests.post(
    "http://localhost:8000/analyze-message",
    json={
        "message": "Congratulations! You've won a $1000 prize! Click here to claim.",
        "user_id": "user-123"
    }
)

result = response.json()
print(f"Category: {result['category']}")
print(f"Risk Score: {result['risk_score']}")
print(f"Severity: {result['severity']}")
print(f"Advice: {result['advice']}")
```

### Example 2: cURL

```bash
# Analyze a message
curl -X POST "http://localhost:8000/analyze-message" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Verify your account immediately or it will be suspended!",
    "user_id": "user-123"
  }'

# Analyze a URL
curl -X POST "http://localhost:8000/analyze-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://suspicious-domain-123.com/login.exe",
    "user_id": "user-123"
  }'
```

## Risk Categories

1. **Phishing**: Attempts to trick users into revealing sensitive information
2. **Scam**: Financial or fraudulent schemes
3. **Malware**: Links to potentially harmful software or compromised systems
4. **Spam**: Unsolicited bulk communications
5. **Safe**: No significant security concerns detected
6. **Unknown**: Unable to fully assess

## Severity Levels

| Level | Score Range | Recommended Action |
|-------|------------|-------------------|
| CRITICAL | 80-100 | Immediate action required; avoid completely |
| HIGH | 60-79 | Proceed with caution; verify before acting |
| MEDIUM | 40-59 | Be cautious; additional verification recommended |
| LOW | 0-39 | Minimal risk; standard security practices sufficient |

## Future Enhancements

- Database integration for threat intelligence
- Machine learning models for improved detection
- User feedback loop for continuous improvement
- Rate limiting and authentication
- Caching for repeated analyses
- Integration with external threat databases
- Admin dashboard for monitoring
- Audit logging for security events

## Development Tips

### Adding New Analysis Rules

1. Add keywords/patterns to the agent class
2. Implement a new check method (e.g., `_check_new_threat`)
3. Update the main `analyze()` method to include the check
4. Test with various inputs

### Testing Endpoints

Use the interactive Swagger UI at `/docs` to test endpoints directly, or use tools like Postman or Insomnia.

### Debugging

- Check server logs for detailed error information
- Use `print()` statements or Python debugger
- Verify input formatting matches model requirements

## Security Considerations

- This is a demonstration backend without authentication
- For production, add:
  - User authentication and authorization
  - Rate limiting
  - HTTPS/TLS encryption
  - API key management
  - Input validation and sanitization
  - Audit logging
  - Error handling without information leakage

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --port 8001
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## License

This project is part of the Suraksha Agent security initiative.

## Support

For issues, questions, or contributions, please refer to the main project documentation or contact the development team.
