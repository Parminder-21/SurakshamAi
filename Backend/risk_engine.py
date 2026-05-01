"""
Risk engine to calculate risk scores and severity levels.
"""

from typing import Tuple


class RiskEngine:
    """
    Engine to evaluate and score risks.
    """
    
    # Standardized risk labels matching API contract
    SEVERITY_THRESHOLDS = {
        'high_risk': 65.0,
        'suspicious': 25.0,
        'safe': 0.0,
    }
    
    @staticmethod
    def calculate_severity(risk_score: float) -> str:
        """
        Determine severity level based on risk score.
        Standardized to: safe, suspicious, high_risk
        """
        if risk_score >= RiskEngine.SEVERITY_THRESHOLDS['high_risk']:
            return 'high_risk'
        elif risk_score >= RiskEngine.SEVERITY_THRESHOLDS['suspicious']:
            return 'suspicious'
        else:
            return 'safe'
    
    @staticmethod
    def combine_scores(scores: list) -> float:
        """
        Combine multiple risk scores into a single score.
        Uses a weighted average approach that emphasizes higher risks.
        """
        if not scores:
            return 0.0
        
        # Ensure scores are within 0-100
        valid_scores = [max(0.0, min(100.0, s)) for s in scores]
        
        if len(valid_scores) == 1:
            return valid_scores[0]
        
        # Give 75% weight to max score, 25% to average (aggressive weighting)
        max_score = max(valid_scores)
        avg_score = sum(valid_scores) / len(valid_scores)
        
        combined = (max_score * 0.75) + (avg_score * 0.25)
        
        return min(100.0, combined)
    
    @staticmethod
    def get_advice(category: str, risk_score: float, severity: str) -> str:
        """
        Generate advice based on category, score, and severity.
        """
        advice_map = {
            'phishing': {
                'high_risk': "This appears to be a phishing attack. Do NOT click links or provide information. Report to your email provider immediately.",
                'suspicious': "This message shows suspicious phishing indicators. Be cautious. Verify requests through official channels.",
                'safe': "While unlikely to be phishing, always maintain standard security practices.",
            },
            'scam': {
                'high_risk': "This is likely a scam. Do NOT send money or personal information. Report to authorities if finances are involved.",
                'suspicious': "This message exhibits scam characteristics. Be very cautious and verify through independent channels.",
                'safe': "No obvious scam indicators detected, but always verify unexpected offers.",
            },
            'malware': {
                'high_risk': "This link may contain malware. Do NOT click it. Ensure your antivirus is updated.",
                'suspicious': "This URL shows suspicious characteristics. Avoid clicking. Use a safe browsing tool to verify.",
                'safe': "URL appears relatively safe, but maintain standard security practices.",
            },
            'unknown': {
                'high_risk': "Significant security concerns detected. Proceed with extreme caution.",
                'suspicious': "Some concerning aspects detected. Verify information independently.",
                'safe': "No major concerns detected.",
            },
        }
        
        cat = category.lower()
        if 'scam' in cat: cat = 'scam'
        elif 'phishing' in cat: cat = 'phishing'
        elif 'malware' in cat: cat = 'malware'
        else: cat = 'unknown'
        
        category_advice = advice_map.get(cat, advice_map['unknown'])
        return category_advice.get(severity, "Unable to assess this content appropriately.")

    @staticmethod
    def calculate_risk_score(
        urgency_score: float,
        authority_score: float,
        deception_score: float,
        payment_pressure: bool = False,
        suspicious_link: bool = False,
        otp_request: bool = False,
        category_match: bool = False,
    ) -> Tuple[float, str]:
        """
        Hardened risk scoring function.
        Returns: (risk_score, severity_label)
        """
        def _clamp(v: float) -> float:
            try:
                v = float(v)
            except Exception:
                v = 0.0
            return max(0.0, min(100.0, v))

        u = _clamp(urgency_score)
        a = _clamp(authority_score)
        d = _clamp(deception_score)

        # Step 1: Base score uses aggressive combination
        base = RiskEngine.combine_scores([u, a, d])

        # Step 2: Add transparent bonuses for critical boolean flags
        bonus = 0.0
        if payment_pressure:
            bonus += 30.0
        if suspicious_link:
            bonus += 25.0
        if otp_request:
            bonus += 50.0 # Extremely critical
        if category_match:
            # If taxonomy matched a scam category, we start with a strong suspicion
            bonus += 30.0

        raw_score = base + bonus
        risk_score = round(max(0.0, min(100.0, raw_score)), 2)

        # Step 3: Use standardized severity mapping
        severity = RiskEngine.calculate_severity(risk_score)

        return (risk_score, severity)

