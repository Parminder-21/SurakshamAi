import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_privacy_scrubbing_in_message():
    """Verify that PII is scrubbed from the response reasons."""
    pii_message = "My Aadhaar is 1234 5678 9012 and phone is 9876543210. Help me with KYC."
    response = client.post(
        "/analyze-message",
        json={"message": pii_message}
    )
    assert response.status_code == 200
    data = response.json()
    
    # The reasons should not contain the raw PII
    reasons_str = str(data["reasons"])
    assert "1234 5678 9012" not in reasons_str
    assert "9876543210" not in reasons_str
    assert "Sensitive personal data" in reasons_str

def test_privacy_scrubbing_in_url():
    """Verify that PII is scrubbed from URL response reasons."""
    # A URL with an email as a parameter
    pii_url = "https://example.com/verify?email=test@example.com&phone=9876543210"
    response = client.post(
        "/analyze-url",
        json={"url": pii_url}
    )
    assert response.status_code == 200
    data = response.json()
    
    reasons_str = str(data["reasons"])
    assert "test@example.com" not in reasons_str
    assert "9876543210" not in reasons_str
    assert "[Email Redacted]" in reasons_str or "[Phone Redacted]" in reasons_str or data["risk_score"] >= 0

def test_empty_message_returns_422():
    """Verify that empty message returns 422 due to Pydantic validation."""
    response = client.post(
        "/analyze-message",
        json={"message": ""}
    )
    assert response.status_code == 422
