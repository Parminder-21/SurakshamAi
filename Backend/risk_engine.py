"""
Risk engine to calculate risk scores and severity levels.
"""

from typing import Tuple


class RiskEngine:
    """
    Engine to evaluate and score risks.
    """
    
    # Risk threshold mappings
    SEVERITY_THRESHOLDS = {
        'CRITICAL': 80,
        'HIGH': 60,
        'MEDIUM': 40,
        'LOW': 0,
    }
    
    @staticmethod
    def calculate_severity(risk_score: float) -> str:
        """
        Determine severity level based on risk score.
        
        Args:
            risk_score: Risk score from 0-100
            
        Returns:
            Severity level (LOW, MEDIUM, HIGH, CRITICAL)
        """
        if risk_score >= RiskEngine.SEVERITY_THRESHOLDS['CRITICAL']:
            return 'CRITICAL'
        elif risk_score >= RiskEngine.SEVERITY_THRESHOLDS['HIGH']:
            return 'HIGH'
        elif risk_score >= RiskEngine.SEVERITY_THRESHOLDS['MEDIUM']:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def combine_scores(scores: list) -> float:
        """
        Combine multiple risk scores into a single score.
        Uses a weighted average approach that emphasizes higher risks.
        
        Args:
            scores: List of risk scores (0-100)
            
        Returns:
            Combined risk score (0-100)
        """
        if not scores:
            return 0.0
        
        # Use weighted average, giving more weight to higher scores
        if len(scores) == 1:
            return min(100.0, max(0.0, scores[0]))
        
        # Simple average with boost for high scores
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        
        # Give 70% weight to average, 30% weight to max (to catch critical issues)
        combined = (avg_score * 0.7) + (max_score * 0.3)
        
        return min(100.0, max(0.0, combined))
    
    @staticmethod
    def get_advice(category: str, risk_score: float, severity: str) -> str:
        """
        Generate advice based on category, score, and severity.
        
        Args:
            category: Risk category
            risk_score: Risk score
            severity: Severity level
            
        Returns:
            Actionable advice string
        """
        advice_map = {
            'phishing': {
                'CRITICAL': "This appears to be a phishing attack. Do NOT click links or provide information. Report to your email provider immediately.",
                'HIGH': "This message shows strong phishing indicators. Be cautious. Verify requests through official channels before responding.",
                'MEDIUM': "This message has some phishing characteristics. Verify the sender's identity independently before clicking links.",
                'LOW': "While unlikely to be phishing, always verify unexpected requests for information.",
            },
            'scam': {
                'CRITICAL': "This is likely a scam. Do NOT send money or personal information. Report to authorities if finances are involved.",
                'HIGH': "This message exhibits scam characteristics. Be very cautious and verify through independent channels.",
                'MEDIUM': "This message may be a scam attempt. Verify legitimacy before taking action.",
                'LOW': "No obvious scam indicators, but always verify unexpected offers.",
            },
            'malware': {
                'CRITICAL': "This link may contain malware. Do NOT click it. Ensure your antivirus is updated.",
                'HIGH': "This URL shows high risk of malicious content. Avoid clicking. Use a safe browsing tool to verify.",
                'MEDIUM': "This URL may pose a security risk. Verify its legitimacy before visiting.",
                'LOW': "URL appears relatively safe, but maintain standard security practices.",
            },
            'spam': {
                'CRITICAL': "This is unsolicited bulk content. Mark as spam and delete.",
                'HIGH': "This appears to be spam. Mark as spam to protect your inbox.",
                'MEDIUM': "This message may be spam. Delete if unwanted.",
                'LOW': "Non-critical message, likely legitimate.",
            },
            'unknown': {
                'CRITICAL': "Unable to fully assess this content. Be cautious and verify information independently.",
                'HIGH': "Some concerning aspects detected. Proceed with caution.",
                'MEDIUM': "Unable to fully assess all aspects. Use your judgment.",
                'LOW': "No major concerns detected.",
            },
        }
        
        category_advice = advice_map.get(category.lower(), advice_map['unknown'])
        return category_advice.get(severity, "Unable to assess this content appropriately.")
