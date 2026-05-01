"""
Guidance agent to provide personalized security advice.
"""

from typing import List, Dict


class GuidanceAgent:
    """
    Agent responsible for generating personalized security guidance.
    """
    
    def __init__(self):
        """Initialize the guidance agent."""
        pass
    
    def get_detailed_guidance(self, category: str, severity: str, reasons: List[str]) -> str:
        """
        Generate detailed guidance based on analysis results.
        
        Args:
            category: Risk category (phishing, scam, malware, spam, safe)
            severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
            reasons: List of reasons from the analysis
            
        Returns:
            Detailed guidance string
        """
        guidance = self._get_base_guidance(category, severity)
        
        # Add context-specific advice
        if reasons:
            guidance += f"\n\nSpecific issues detected:\n"
            for i, reason in enumerate(reasons, 1):
                guidance += f"• {reason}\n"
        
        # Add general security tips
        guidance += self._get_general_tips()
        
        return guidance.strip()
    
    def _get_base_guidance(self, category: str, severity: str) -> str:
        """Get base guidance for a category and severity combination."""
        guidance_map = {
            'phishing': {
                'CRITICAL': (
                    "⚠️ CRITICAL PHISHING ALERT\n"
                    "This is a confirmed phishing attempt. Take immediate action:\n"
                    "1. Do NOT click any links or download attachments\n"
                    "2. Do NOT provide personal or financial information\n"
                    "3. Forward the suspicious email to your email provider's phishing team\n"
                    "4. Mark as spam and delete\n"
                    "5. If you clicked a link, change your password immediately"
                ),
                'HIGH': (
                    "🔴 HIGH RISK - Likely Phishing\n"
                    "This message shows strong phishing characteristics:\n"
                    "1. Verify the sender by checking official channels\n"
                    "2. Do NOT click links – instead visit websites directly in your browser\n"
                    "3. Look for spelling errors and suspicious sender addresses\n"
                    "4. Report phishing emails to your email provider\n"
                    "5. Consider updating your password as a precaution"
                ),
                'MEDIUM': (
                    "🟡 MEDIUM RISK - Possible Phishing\n"
                    "This message has some phishing indicators:\n"
                    "1. Verify any requests through official communication channels\n"
                    "2. Be cautious with links – hover to see the actual URL\n"
                    "3. Check sender address carefully for slight misspellings\n"
                    "4. Delete if the sender is unexpected"
                ),
                'LOW': (
                    "ℹ️ LOW RISK - Minimal Phishing Indicators\n"
                    "While this message poses minimal phishing risk:\n"
                    "1. Always verify unexpected requests before responding\n"
                    "2. Check sender addresses on unfamiliar communications\n"
                    "3. Legitimate organizations rarely ask for sensitive info via email"
                ),
            },
            'scam': {
                'CRITICAL': (
                    "💰 CRITICAL SCAM ALERT\n"
                    "This is almost certainly a financial scam:\n"
                    "1. Do NOT send money, gift cards, or cryptocurrency\n"
                    "2. Do NOT provide bank account or payment information\n"
                    "3. Do NOT wire funds to any account\n"
                    "4. Report to the FTC at reportfraud.ftc.gov\n"
                    "5. If money was sent, contact your bank/payment provider immediately"
                ),
                'HIGH': (
                    "🔴 HIGH RISK - Likely Scam\n"
                    "This message exhibits classic scam characteristics:\n"
                    "1. Offers that seem too good are always too good\n"
                    "2. Scammers create urgency to prevent thinking\n"
                    "3. Never wire money, use gift cards, or send cryptocurrency\n"
                    "4. Legitimate organizations don't request payment this way\n"
                    "5. Report to FTC and relevant authorities"
                ),
                'MEDIUM': (
                    "🟡 MEDIUM RISK - Possible Scam\n"
                    "This message may be a scam attempt:\n"
                    "1. Be skeptical of unsolicited offers or prizes\n"
                    "2. Never provide financial information to unknown sources\n"
                    "3. Verify through official channels before taking action\n"
                    "4. Legitimate businesses have standard verification processes"
                ),
                'LOW': (
                    "ℹ️ LOW RISK - Minimal Scam Indicators\n"
                    "While this message poses minimal scam risk:\n"
                    "1. Always verify unexpected financial offers\n"
                    "2. Never rush into financial decisions\n"
                    "3. When in doubt, contact the organization directly"
                ),
            },
            'malware': {
                'CRITICAL': (
                    "🔒 CRITICAL MALWARE ALERT\n"
                    "This URL likely contains malware:\n"
                    "1. Do NOT click the link under any circumstances\n"
                    "2. Do NOT download anything from this URL\n"
                    "3. Run a full antivirus scan on your device\n"
                    "4. Update all software and security tools\n"
                    "5. Consider professional help if your system was compromised"
                ),
                'HIGH': (
                    "🔴 HIGH RISK - Likely Malicious Content\n"
                    "This URL shows high risk of malware:\n"
                    "1. Avoid clicking this link\n"
                    "2. Use a safe browsing checker before visiting\n"
                    "3. Ensure antivirus software is active\n"
                    "4. Keep your operating system and software updated"
                ),
                'MEDIUM': (
                    "🟡 MEDIUM RISK - Potential Malware\n"
                    "This URL may pose security risks:\n"
                    "1. Verify the URL is legitimate before visiting\n"
                    "2. Use safe browsing tools to check\n"
                    "3. Keep security software updated"
                ),
                'LOW': (
                    "ℹ️ LOW RISK - Minimal Malware Indicators\n"
                    "While risk is minimal:\n"
                    "1. Always keep antivirus software active\n"
                    "2. Maintain regular security updates\n"
                    "3. Be cautious with downloads from unknown sources"
                ),
            },
            'spam': {
                'CRITICAL': "This is unsolicited bulk content. Mark as spam and delete. Block the sender if possible.",
                'HIGH': "This appears to be spam. Delete and mark as spam to improve your email filters.",
                'MEDIUM': "This message has spam characteristics. Delete if unwanted.",
                'LOW': "This message appears legitimate. No action needed.",
            },
            'safe': {
                'LOW': "✅ This message appears safe. No immediate security concerns detected.",
                'MEDIUM': "",
                'HIGH': "",
                'CRITICAL': "",
            },
        }
        
        category_guidance = guidance_map.get(category, guidance_map.get('safe', {}))
        return category_guidance.get(severity, "Unable to provide specific guidance.")
    
    def _get_general_tips(self) -> str:
        """Get general security tips for all messages."""
        return (
            "\n📚 GENERAL SECURITY TIPS:\n"
            "• Be suspicious of unexpected messages, especially those requesting action\n"
            "• Legitimate organizations rarely request passwords or sensitive info via email\n"
            "• Check sender email addresses carefully (scammers often use similar addresses)\n"
            "• Look for spelling and grammar errors\n"
            "• When in doubt, contact the organization directly via official channels\n"
            "• Hover over links to see the actual URL before clicking\n"
            "• Enable two-factor authentication on important accounts\n"
            "• Keep security software and browsers updated"
        )
