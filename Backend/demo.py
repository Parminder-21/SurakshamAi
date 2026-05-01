"""
Demo script to test the Suraksha Agent modules independently.
Run this to verify all components work correctly before starting the FastAPI server.
"""

from message_agent import MessageAgent
from url_agent import URLAgent
from risk_engine import RiskEngine
from guidance_agent import GuidanceAgent


def test_message_analysis():
    """Test message analysis functionality."""
    print("\n" + "=" * 60)
    print("MESSAGE ANALYSIS DEMO")
    print("=" * 60)
    
    agent = MessageAgent()
    
    test_messages = [
        "Click here to verify your account: https://malicious-site.com/verify",
        "Congratulations! You've won $5000! Send your bank details to claim.",
        "Hi, just wanted to check in. How are you?",
        "Update your password immediately or your account will be suspended!",
    ]
    
    for msg in test_messages:
        print(f"\n📧 Message: {msg[:80]}...")
        category, score, reasons = agent.analyze(msg)
        print(f"   Category: {category}")
        print(f"   Risk Score: {score:.1f}")
        print(f"   Reasons: {reasons}")


def test_url_analysis():
    """Test URL analysis functionality."""
    print("\n" + "=" * 60)
    print("URL ANALYSIS DEMO")
    print("=" * 60)
    
    agent = URLAgent()
    
    test_urls = [
        "https://bit.ly/malicious-link",
        "https://google.com",
        "https://suspicious-domain-with-many-hyphens.com/download.exe",
        "http://192.168.1.1/admin",
    ]
    
    for url in test_urls:
        print(f"\n🔗 URL: {url}")
        category, score, reasons = agent.analyze(url)
        print(f"   Category: {category}")
        print(f"   Risk Score: {score:.1f}")
        print(f"   Reasons: {reasons}")


def test_risk_engine():
    """Test risk engine functionality."""
    print("\n" + "=" * 60)
    print("RISK ENGINE DEMO")
    print("=" * 60)
    
    engine = RiskEngine()
    
    test_scores = [45, 60, 85]
    print(f"\nTest Scores: {test_scores}")
    combined = engine.combine_scores(test_scores)
    severity = engine.calculate_severity(combined)
    print(f"Combined Score: {combined:.1f}")
    print(f"Severity: {severity}")
    
    # Test severity calculations
    print("\nSeverity Thresholds:")
    for score in [15, 35, 50, 65, 85, 95]:
        severity = engine.calculate_severity(score)
        print(f"   Score {score}: {severity}")


def test_guidance_agent():
    """Test guidance agent functionality."""
    print("\n" + "=" * 60)
    print("GUIDANCE AGENT DEMO")
    print("=" * 60)
    
    agent = GuidanceAgent()
    
    test_cases = [
        ("phishing", "CRITICAL", ["Multiple phishing keywords detected", "Urgency tactics used"]),
        ("scam", "HIGH", ["Monetary request detected", "Too good to be true offer"]),
        ("malware", "MEDIUM", ["Suspicious file extension detected"]),
    ]
    
    for category, severity, reasons in test_cases:
        print(f"\n{category.upper()} - {severity}")
        guidance = agent.get_detailed_guidance(category, severity, reasons)
        print(guidance[:500] + "..." if len(guidance) > 500 else guidance)


def main():
    """Run all demo tests."""
    print("\n🛡️  SURAKSHA AGENT - MODULE TESTS 🛡️")
    
    try:
        test_message_analysis()
        test_url_analysis()
        test_risk_engine()
        test_guidance_agent()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nThe FastAPI backend is ready to use.")
        print("Run: python main.py")
        print("Then visit: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
