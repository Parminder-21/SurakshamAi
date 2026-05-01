from risk_engine import RiskEngine


def test_calculate_severity_thresholds():
    assert RiskEngine.calculate_severity(0) == "safe"
    assert RiskEngine.calculate_severity(24.99) == "safe"
    assert RiskEngine.calculate_severity(25) == "suspicious"
    assert RiskEngine.calculate_severity(65) == "high_risk"


def test_combine_scores_returns_bounded_value():
    score = RiskEngine.combine_scores([20, 80, 120])
    assert 0 <= score <= 100
    assert score > 50


def test_calculate_risk_score_with_critical_flags():
    score, severity = RiskEngine.calculate_risk_score(
        urgency_score=10,
        authority_score=10,
        deception_score=10,
        payment_pressure=True,
        suspicious_link=True,
        otp_request=True,
        category_match=True,
    )
    assert 0 <= score <= 100
    assert severity in {"safe", "suspicious", "high_risk"}
    assert severity == "high_risk"
