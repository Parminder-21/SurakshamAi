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
        
        # Base keywords for different risk categories
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
        
        # Store taxonomy for later use in analysis
        self.taxonomy = TAXONOMY
        
        # Extend keyword lists using taxonomy entries (Indian scam categories)
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
            entry = self.taxonomy.get(cat)
            if not entry:
                continue
            keywords = entry.get('keywords', [])
            target_list = getattr(self, list_name, None)
            if isinstance(target_list, list):
                for kw in keywords:
                    if kw.lower() not in target_list:
                        target_list.append(kw.lower())
    
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
        
        # 1. Check for suspicious patterns
        has_urls = self._check_for_urls(message)
        has_sensitive_data = contains_sensitive_data(message)
        
        # 2. Check for taxonomy-specific red flags (P1 Improvement)
        taxonomy_score, taxonomy_reasons = self._check_taxonomy_red_flags(message_lower)
        if taxonomy_score > 0:
            scores.append(taxonomy_score)
            reasons.extend(taxonomy_reasons)
        
        # 3. Phishing checks
        phishing_score = self._check_phishing(message_lower, reasons)
        if phishing_score > 0:
            scores.append(phishing_score)
        
        # 4. Scam checks
        scam_score = self._check_scam(message_lower, reasons)
        if scam_score > 0:
            scores.append(scam_score)
        
        # 5. Sensitive data checks
        if has_sensitive_data:
            reasons.append("Message contains sensitive personal information (risk of data theft)")
            scores.append(40) # Increased from 35
        
        # 6. URL checks
        if has_urls:
            reasons.append("Message contains URLs that require verification")
            scores.append(30) # Increased from 25
        
        # Determine category and combined score
        if not scores:
            return ('safe', 0.0, ['No concerning patterns detected'])
        
        combined_score = self.risk_engine.combine_scores(scores)
        
        # Determine primary category
        if phishing_score and phishing_score >= scam_score:
            category = 'phishing'
        elif scam_score and scam_score >= phishing_score:
            category = 'scam'
        elif taxonomy_reasons:
            # If taxonomy matched, use the first matching category
            category = 'scam' 
        else:
            category = 'spam'
        
        return (category, combined_score, list(set(reasons))) # Deduplicate reasons
    
    def _check_taxonomy_red_flags(self, message_lower: str) -> Tuple[float, List[str]]:
        """Check for specific red flags defined in the Indian scam taxonomy."""
        score = 0
        reasons = []
        
        for cat_id, entry in self.taxonomy.items():
            red_flags = entry.get('red_flags', [])
            for flag in red_flags:
                if flag.lower() in message_lower:
                    score = max(score, 70) # High base score for explicit red flags
                    reasons.append(f"Detected {entry['description'].lower()}")
                    break
        
        return score, reasons

    def _check_phishing(self, message_lower: str, reasons: List[str]) -> float:
        """Check for phishing indicators."""
        score = 0
        keyword_count = 0
        
        for keyword in self.phishing_keywords:
            if keyword in message_lower:
                keyword_count += 1
        
        if keyword_count >= 3:
            score = 85 # Increased from 75
            reasons.append(f"High number of phishing keywords detected ({keyword_count})")
        elif keyword_count >= 2:
            score = 60 # Increased from 50
            reasons.append(f"Multiple phishing keywords detected ({keyword_count})")
        elif keyword_count >= 1:
            score = 30 # Increased from 25
        
        # Additional checks for urgency and threats
        if any(word in message_lower for word in ['immediately', 'urgent', 'now', 'quickly']):
            score += 15
            reasons.append("Message uses urgency tactics to pressure response")
        
        return min(100.0, score)
    
    def _check_scam(self, message_lower: str, reasons: List[str]) -> float:
        """Check for scam indicators."""
        score = 0
        keyword_count = 0
        
        for keyword in self.scam_keywords:
            if keyword in message_lower:
                keyword_count += 1
        
        if keyword_count >= 4:
            score = 90 # Increased from 80
            reasons.append(f"High number of scam-related terms detected ({keyword_count})")
        elif keyword_count >= 2:
            score = 65 # Increased from 60
            reasons.append(f"Potential scam indicators detected ({keyword_count})")
        elif keyword_count >= 1:
            score = 35 # Increased from 30
        
        # Check for money/payment requests
        if any(word in message_lower for word in ['send money', 'wire funds', 'payment', 'transfer money', 'upi pin', 'otp']):
            score += 25 # Increased from 20
            reasons.append("Suspicious request for payment or sensitive credentials detected")
        
        return min(100.0, score)
    
    def _check_for_urls(self, message: str) -> bool:
        """Check if message contains URLs."""
        import re
        url_pattern = r'https?://\S+|www\.\S+'
        return bool(re.search(url_pattern, message, re.IGNORECASE))
