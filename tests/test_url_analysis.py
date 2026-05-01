from url_agent import URLAgent


agent = URLAgent()


def test_url_analysis_detects_suspicious_url():
    result = agent.analyze("https://bit.ly/verify-account-now")

    assert result["risk_score"] > 0
    assert result["severity"] in {"safe", "suspicious", "high_risk"}
    assert isinstance(result["reasons"], list)
    assert isinstance(result["flags"], list)


def test_url_analysis_safe_url_has_low_risk():
    result = agent.analyze("https://example.org")

    assert result["category"] == "safe"
    assert result["risk_score"] == 0.0
    assert result["severity"] == "safe"
