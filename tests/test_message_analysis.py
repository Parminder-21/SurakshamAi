from message_agent import MessageAgent


agent = MessageAgent()


def test_message_analysis_detects_suspicious_content():
    result = agent.analyze("Urgent! Share OTP now and pay fee immediately to avoid account block.")

    assert result["risk_score"] >= 25
    assert result["severity"] in {"safe", "suspicious", "high_risk"}
    assert isinstance(result["reasons"], list)
    assert len(result["reasons"]) > 0


def test_message_analysis_safe_text_has_low_risk():
    result = agent.analyze("Hi team, meeting moved to 4 PM. Please join on time.")

    assert result["category"] == "safe"
    assert result["risk_score"] <= 25
