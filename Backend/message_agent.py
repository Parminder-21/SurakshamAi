"""
Message analysis agent to assess text/message content for risks.
"""

from typing import Tuple, List
from risk_engine import RiskEngine
from privacy_scrubber import scrub_sensitive_data, contains_sensitive_data

# Import taxonomy for India-specific scam indicators
from taxonomy import TAXONOMY


class MessageAgent:
    """
    Agent responsible for analyzing messages for phishing, scams, and malware references.
    """
    
    def __init__(self):
        """Initialize the message agent."""
        self.risk_engine = RiskEngine()
        
        # Keywords and patterns for different risk categories
        self.phishing_keywords = [
            'verify', 'confirm', 'update', 'validate', 'click here', 'urgent',
            'action required', 'act now', 'expire', 'suspended', 'limited time',
            'unusual activity', 'confirm identity', 'verify account'
        ]
        
        self.scam_keywords = [
            'winning', 'congratulations', 'claim', 'prize', 'money', 'free',
            'bonus', 'inheritance', 'transfer', 'wire', 'urgent payment',
            'bitcoin', 'cryptocurrency', 'investment opportunity'
        ]
        
        self.malware_keywords = [
            'download', 'install', 'execute', 'run', 'extension', 'plugin',
            'attachment', 'zip', 'exe'
        ]
        
        # Extend keyword lists using taxonomy entries (Indian scam categories)
        try:
            # Map taxonomy categories to either phishing or scam keyword lists
            mapping = {
                'fake_kyc': 'phishing_keywords',
                'authority_impersonation': 'phishing_keywords',
                'otp_theft': 'phishing_keywords',
                'upi_collect_request_scam': 'phishing_keywords',

                'electricity_bill_scam': 'scam_keywords',
                'courier_scam': 'scam_keywords',
                'job_scam': 'scam_keywords',
                'lottery_scam': 'scam_keywords',
            }

            for cat, list_name in mapping.items():
                entry = TAXONOMY.get(cat)
                if not entry:
                    continue
                keywords = entry.get('keywords', [])
                # Add keywords if not already present
                target_list = getattr(self, list_name, None)
                if isinstance(target_list, list):
                    for kw in keywords:
                        if kw not in target_list:
                            target_list.append(kw)
        except Exception:
            # If taxonomy is not available or any error occurs, ignore and continue
            pass
    
    def analyze(self, message: str) -> Tuple[str, float, List[str]]:
        """
        Analyze a message for security risks.
        
        Args:
            message: The message text to analyze
            
        Returns:
            Tuple of (category, risk_score, reasons)
        """
        message_lower = message.lower()
        reasons = []
        scores = []
        
        # Check for suspicious patterns
        has_urls = self._check_for_urls(message)
        has_sensitive_data = contains_sensitive_data(message)
        
        # Phishing checks
        phishing_score = self._check_phishing(message_lower, reasons)
        if phishing_score > 0:
            scores.append(phishing_score)
        
        # Scam checks
        scam_score = self._check_scam(message_lower, reasons)
        if scam_score > 0:
            scores.append(scam_score)
        
        # Sensitive data checks
        if has_sensitive_data:
            reasons.append("Message contains sensitive personal information")
            scores.append(35)
        
        # URL checks
        if has_urls:
            reasons.append("Message contains URLs that require verification")
            scores.append(25)
        
        # Determine category and combined score
        if not scores:
            return ('safe', 0.0, ['No concerning patterns detected'])
        
        combined_score = self.risk_engine.combine_scores(scores)
        
        # Determine primary category
        if phishing_score and phishing_score >= scam_score:
            category = 'phishing'
        elif scam_score and scam_score >= phishing_score:
            category = 'scam'
        else:
            category = 'spam'
        
        return (category, combined_score, reasons)
    
    def _check_phishing(self, message_lower: str, reasons: List[str]) -> float:
        """Check for phishing indicators."""
        score = 0
        keyword_count = 0
        
        for keyword in self.phishing_keywords:
            if keyword in message_lower:
                keyword_count += 1
        
        if keyword_count >= 3:
            score = 75
            reasons.append(f"Multiple phishing keywords detected ({keyword_count})")
        elif keyword_count >= 2:
            score = 50
            reasons.append(f"Some phishing keywords detected ({keyword_count})")
        elif keyword_count >= 1:
            score = 25
        
        # Additional checks for urgency and threats
        if any(word in message_lower for word in ['immediately', 'immediately', 'now']):
            score += 15
            reasons.append("Message uses urgency tactics")
        
        return min(100.0, score)
    
    def _check_scam(self, message_lower: str, reasons: List[str]) -> float:
        """Check for scam indicators."""
        score = 0
        keyword_count = 0
        
        for keyword in self.scam_keywords:
            if keyword in message_lower:
                keyword_count += 1
        
        if keyword_count >= 4:
            score = 80
            reasons.append(f"Multiple scam keywords detected ({keyword_count})")
        elif keyword_count >= 2:
            score = 60
            reasons.append(f"Potential scam indicators detected ({keyword_count})")
        elif keyword_count >= 1:
            score = 30
        
        # Check for money/payment requests
        if any(word in message_lower for word in ['send money', 'wire funds', 'payment', 'transfer money']):
            score += 20
            reasons.append("Suspicious payment request detected")
        
        return min(100.0, score)
    
    def _check_for_urls(self, message: str) -> bool:
        """Check if message contains URLs."""
        import re
        url_pattern = r'https?://\S+|www\.\S+'
        return bool(re.search(url_pattern, message, re.IGNORECASE))
