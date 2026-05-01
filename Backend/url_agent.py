"""
URL analysis agent to assess URLs for malware and phishing risks.
"""

from typing import Tuple, List
from urllib.parse import urlparse
from risk_engine import RiskEngine


class URLAgent:
    """
    Agent responsible for analyzing URLs for malware, phishing, and suspicious characteristics.
    """
    
    def __init__(self):
        """Initialize the URL agent."""
        self.risk_engine = RiskEngine()
        
        # Known malicious domains (simplified for demo)
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'ow.ly',  # URL shorteners are risky
        ]
        
        # Suspicious file extensions commonly associated with malware
        self.suspicious_extensions = [
            '.exe', '.bat', '.cmd', '.com', '.scr',
            '.vbs', '.js', '.zip', '.rar'
        ]
    
    def analyze(self, url: str) -> Tuple[str, float, List[str]]:
        """
        Analyze a URL for security risks.
        
        Args:
            url: The URL to analyze (should be a valid URL)
            
        Returns:
            Tuple of (category, risk_score, reasons)
        """
        reasons = []
        scores = []
        
        try:
            parsed_url = urlparse(str(url))
            domain = parsed_url.netloc.lower()
            path = parsed_url.path.lower()
            
            # Check domain reputation
            domain_score = self._check_domain(domain, reasons)
            if domain_score > 0:
                scores.append(domain_score)
            
            # Check for suspicious file extensions
            extension_score = self._check_extensions(path, reasons)
            if extension_score > 0:
                scores.append(extension_score)
            
            # Check for suspicious characteristics
            char_score = self._check_url_characteristics(str(url), domain, reasons)
            if char_score > 0:
                scores.append(char_score)
            
        except Exception as e:
            reasons.append(f"Error parsing URL: {str(e)}")
            return ('unknown', 50.0, reasons)
        
        # Determine results
        if not scores:
            return ('safe', 0.0, ['URL appears legitimate'])
        
        combined_score = self.risk_engine.combine_scores(scores)
        
        # Determine category based on highest risk
        if any('malware' in r.lower() or 'malicious' in r.lower() for r in reasons):
            category = 'malware'
        elif any('phishing' in r.lower() for r in reasons):
            category = 'phishing'
        else:
            category = 'spam'
        
        return (category, combined_score, reasons)
    
    def _check_domain(self, domain: str, reasons: List[str]) -> float:
        """Check domain for suspicious characteristics."""
        score = 0
        
        # Check for known suspicious domains
        for suspicious in self.suspicious_domains:
            if suspicious.lower() in domain:
                score = 55
                reasons.append(f"URL uses shortening service ({domain})")
                break
        
        # Check for domains with many hyphens (often used in phishing)
        hyphen_count = domain.count('-')
        if hyphen_count >= 2:
            score += 20
            reasons.append("Domain name contains multiple hyphens (phishing indicator)")
        
        # Check for homograph attacks (domains that look like legitimate ones)
        if domain.startswith('.'):
            score += 15
            reasons.append("Suspicious domain structure detected")
        
        return min(100.0, score)
    
    def _check_extensions(self, path: str, reasons: List[str]) -> float:
        """Check for suspicious file extensions."""
        score = 0
        
        for ext in self.suspicious_extensions:
            if path.endswith(ext):
                score = 85
                reasons.append(f"URL contains potentially malicious file extension ({ext})")
                break
        
        return min(100.0, score)
    
    def _check_url_characteristics(self, url: str, domain: str, reasons: List[str]) -> float:
        """Check general URL characteristics."""
        score = 0
        
        # Check for excessive subdomains
        subdomain_count = domain.count('.')
        if subdomain_count > 3:
            score += 15
            reasons.append("URL has unusually many subdomains")
        
        # Check for IP address instead of domain name
        if self._is_ip_address(domain):
            score += 30
            reasons.append("URL uses IP address instead of domain name")
        
        # Check URL length (extremely long URLs can be suspicious)
        if len(url) > 200:
            score += 10
            reasons.append("URL is unusually long")
        
        # Check for hex encoding in URL (often used to obfuscate)
        if '%' in url and sum(1 for c in url if c == '%') > 3:
            score += 15
            reasons.append("URL contains extensive character encoding")
        
        return min(100.0, score)
    
    @staticmethod
    def _is_ip_address(domain: str) -> bool:
        """Check if domain is an IP address."""
        parts = domain.split('.')
        if len(parts) == 4:
            try:
                for part in parts:
                    num = int(part)
                    if num < 0 or num > 255:
                        return False
                return True
            except ValueError:
                return False
        return False
