"""
Integration tests for the Suraksha Agent FastAPI backend.
Run with: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_check_success(self):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_health_check_response_format(self):
        """Test that health response has correct format."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data["status"], str)
        assert isinstance(data["version"], str)


class TestMessageAnalysisEndpoint:
    """Test cases for the message analysis endpoint."""
    
    def test_analyze_phishing_message(self):
        """Test detection of phishing message."""
        response = client.post(
            "/analyze-message",
            json={
                "message": "Click here to verify your account immediately!",
                "user_id": "test-user"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "category" in data
        assert "risk_score" in data
        assert "severity" in data
        assert "reasons" in data
        assert "advice" in data
        assert "timestamp" in data
    
    def test_analyze_scam_message(self):
        """Test detection of scam message."""
        response = client.post(
            "/analyze-message",
            json={"message": "Congratulations! You've won $1000! Send your bank details to claim."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "scam"
        assert data["risk_score"] >= 50
    
    def test_analyze_safe_message(self):
        """Test legitimate message."""
        response = client.post(
            "/analyze-message",
            json={"message": "Hi, how are you doing today?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] == 0.0
        assert data["severity"] == "LOW"
    
    def test_analyze_message_empty_message(self):
        """Test error handling for empty message."""
        response = client.post(
            "/analyze-message",
            json={"message": ""}
        )
        assert response.status_code == 400
    
    def test_analyze_message_missing_field(self):
        """Test error handling for missing message field."""
        response = client.post(
            "/analyze-message",
            json={"user_id": "test-user"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_risk_score_in_valid_range(self):
        """Test that risk score is between 0 and 100."""
        response = client.post(
            "/analyze-message",
            json={"message": "Some test message"}
        )
        data = response.json()
        assert 0 <= data["risk_score"] <= 100
    
    def test_severity_levels(self):
        """Test that severity is one of valid levels."""
        valid_severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        response = client.post(
            "/analyze-message",
            json={"message": "Click here now!"}
        )
        data = response.json()
        assert data["severity"] in valid_severities


class TestURLAnalysisEndpoint:
    """Test cases for the URL analysis endpoint."""
    
    def test_analyze_safe_url(self):
        """Test analysis of safe URL."""
        response = client.post(
            "/analyze-url",
            json={
                "url": "https://google.com",
                "user_id": "test-user"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] == 0.0
        assert data["severity"] == "LOW"
    
    def test_analyze_shortener_url(self):
        """Test detection of URL shortener."""
        response = client.post(
            "/analyze-url",
            json={"url": "https://bit.ly/test123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] > 0
    
    def test_analyze_malware_url(self):
        """Test detection of URL with malware indicators."""
        response = client.post(
            "/analyze-url",
            json={"url": "https://example.com/file.exe"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] > 50
        assert "exe" in str(data["reasons"]).lower()
    
    def test_analyze_ip_address_url(self):
        """Test detection of IP address URL."""
        response = client.post(
            "/analyze-url",
            json={"url": "http://192.168.1.1/admin"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] > 0
    
    def test_analyze_url_missing_field(self):
        """Test error handling for missing URL field."""
        response = client.post(
            "/analyze-url",
            json={"user_id": "test-user"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_analyze_url_invalid_url(self):
        """Test error handling for invalid URL format."""
        response = client.post(
            "/analyze-url",
            json={"url": "not-a-valid-url"}
        )
        assert response.status_code == 422  # Validation error


class TestResponseFormats:
    """Test cases for response format consistency."""
    
    def test_message_analysis_response_keys(self):
        """Test that message analysis response has all required keys."""
        response = client.post(
            "/analyze-message",
            json={"message": "Test message"}
        )
        data = response.json()
        required_keys = ["category", "risk_score", "severity", "reasons", "advice", "timestamp"]
        for key in required_keys:
            assert key in data
    
    def test_url_analysis_response_keys(self):
        """Test that URL analysis response has all required keys."""
        response = client.post(
            "/analyze-url",
            json={"url": "https://example.com"}
        )
        data = response.json()
        required_keys = ["category", "risk_score", "severity", "reasons", "advice", "timestamp"]
        for key in required_keys:
            assert key in data
    
    def test_reasons_is_list(self):
        """Test that reasons field is a list."""
        response = client.post(
            "/analyze-message",
            json={"message": "Test message"}
        )
        data = response.json()
        assert isinstance(data["reasons"], list)
    
    def test_advice_is_string(self):
        """Test that advice field is a string."""
        response = client.post(
            "/analyze-message",
            json={"message": "Test message"}
        )
        data = response.json()
        assert isinstance(data["advice"], str)


if __name__ == "__main__":
    # Run tests with: python test_api.py -v
    # Or install pytest and run: pytest test_api.py -v
    pytest.main([__file__, "-v"])
