"""
Guidance agent to provide short preventive advice for Suraksha Agent.

The module keeps the guidance simple:
- input: category, risk_score, severity, reasons
- output: 3 to 5 short action-focused bullets
- if severity is high_risk, the wording becomes urgent and direct
"""

from typing import List, Optional, Union


class GuidanceAgent:
    """Generate short, plain-English prevention guidance."""

    def __init__(self):
        """Initialize the guidance agent."""
        self._category_guidance = {
            "phishing": [
                "Do not click unknown links or open unexpected attachments.",
                "Verify the sender using an official website or phone number.",
                "Change your password if you already shared details.",
            ],
            "scam": [
                "Do not send money or share bank details.",
                "Verify the offer through a trusted official source.",
                "Report the message if it asks for payment quickly.",
            ],
            "malware": [
                "Do not open the link or download the file.",
                "Scan your device with updated security software.",
                "Keep the device offline if you suspect infection.",
            ],
            "spam": [
                "Ignore the message and avoid replying.",
                "Mark it as spam or block the sender.",
                "Delete the message if it keeps repeating.",
            ],
            "safe": [
                "No urgent action is needed.",
                "Still avoid sharing personal details in chat.",
                "Use normal caution with unknown senders.",
            ],
        }

        self._taxonomy_guidance = {
            "fake_kyc": [
                "Do not upload Aadhaar, PAN, or selfie documents through a link.",
                "Check the request only inside the official app or website.",
                "Report anyone asking for documents over chat or SMS.",
            ],
            "electricity_bill_scam": [
                "Check your bill only on the official utility app or website.",
                "Do not pay from an unknown payment link.",
                "Call customer care before taking any action.",
            ],
            "courier_scam": [
                "Verify the tracking number on the courier's official site.",
                "Do not pay release fees from a random link.",
                "Do not share card or OTP details to clear a parcel.",
            ],
            "job_scam": [
                "Do not pay any registration or training fee first.",
                "Check the company on its official career page.",
                "Be careful with offers that look too good.",
            ],
            "upi_collect_request_scam": [
                "Reject unknown UPI collect requests right away.",
                "Check the sender and amount before approving anything.",
                "Never share your UPI PIN or OTP.",
            ],
            "lottery_scam": [
                "Do not pay a fee to claim a prize.",
                "Verify the claim through the official contest source.",
                "Ignore messages that promise easy winnings.",
            ],
            "authority_impersonation": [
                "Do not trust pressure from someone claiming to be police or bank staff.",
                "Call the official office using a trusted number.",
                "Never share OTP, PIN, or account details on demand.",
            ],
            "otp_theft": [
                "Never share OTPs with anyone.",
                "Assume the request is fake if it is urgent or unexpected.",
                "Secure the account immediately if an OTP was requested.",
            ],
        }

    def generate_guidance_bullets(
        self,
        category: str,
        risk_score: float,
        severity: str,
        reasons: List[str],
    ) -> List[str]:
        """
        Return 3 to 5 short preventive guidance bullets.

        Args:
            category: Scam or safety category.
            risk_score: Numeric risk score from the risk engine.
            severity: safe, suspicious, or high_risk.
            reasons: Reasons from the analysis.

        Returns:
            A list of short guidance bullets.
        """
        normalized_category = self._normalize_category(category)
        normalized_severity = (severity or "safe").lower()

        bullets: List[str] = []

        if normalized_severity == "high_risk":
            bullets.append("Stop now and do not interact with the message.")

        bullets.extend(self._category_guidance.get(normalized_category, self._category_guidance["safe"]))

        if normalized_category in self._taxonomy_guidance:
            bullets.extend(self._taxonomy_guidance[normalized_category])

        # Add one reason-based bullet if it helps the user act quickly.
        reason_bullet = self._reason_to_bullet(reasons)
        if reason_bullet:
            bullets.append(reason_bullet)

        if normalized_severity == "high_risk":
            bullets.extend([
                "Report it to the right platform or authority immediately.",
                "Change passwords or freeze payments if anything was shared.",
            ])
        elif normalized_severity == "suspicious":
            bullets.append("Verify everything through an official channel before acting.")
        else:
            bullets.append("Keep normal caution and check unknown requests carefully.")

        return self._limit_bullets(bullets, 5)

    def get_detailed_guidance(
        self,
        category: str,
        risk_score: Union[float, str] = 0.0,
        severity: Union[str, List[str]] = "safe",
        reasons: Optional[List[str]] = None,
    ) -> str:
        """Return the bullet guidance as a single plain-text string."""
        # Backward compatibility:
        # Older code called get_detailed_guidance(category, severity, reasons).
        if reasons is None and isinstance(severity, list):
            reasons = severity
            severity = str(risk_score)
            risk_score = 0.0

        reasons = reasons or []
        bullets = self.generate_guidance_bullets(category, risk_score, severity, reasons)
        return "\n".join(f"- {bullet}" for bullet in bullets)

    def _reason_to_bullet(self, reasons: List[str]) -> str:
        """Convert the strongest reason into a short action tip."""
        if not reasons:
            return ""

        joined = " ".join(reasons).lower()

        if "otp" in joined:
            return "Do not share any OTP or verification code."
        if "payment" in joined or "upi" in joined:
            return "Do not approve payment or UPI requests from this message."
        if "link" in joined:
            return "Do not click the link until it is verified on a trusted site."
        if "urgency" in joined:
            return "Pause before acting because urgency is a common scam tactic."
        if "authority" in joined:
            return "Verify the caller or sender through an official contact number."
        return "Review the message carefully before taking any action."

    def _limit_bullets(self, bullets: List[str], max_count: int) -> List[str]:
        """Remove duplicates and keep only the first few bullets."""
        seen = set()
        unique_bullets: List[str] = []

        for bullet in bullets:
            cleaned = bullet.strip()
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            unique_bullets.append(cleaned)
            if len(unique_bullets) >= max_count:
                break

        # Guarantee at least 3 bullets if possible.
        if len(unique_bullets) < 3:
            fallback = [
                "Do not share personal information.",
                "Verify the sender through an official source.",
                "Report the message if it looks suspicious.",
            ]
            for item in fallback:
                if item not in seen:
                    unique_bullets.append(item)
                if len(unique_bullets) >= 3:
                    break

        return unique_bullets[:max_count]

    def _normalize_category(self, category: str) -> str:
        """Map taxonomy categories onto the short guidance buckets."""
        normalized = (category or "safe").lower()

        phishing_like = {
            "fake_kyc",
            "authority_impersonation",
            "otp_theft",
            "upi_collect_request_scam",
            "phishing",
        }
        scam_like = {
            "electricity_bill_scam",
            "courier_scam",
            "job_scam",
            "lottery_scam",
            "scam",
        }
        malware_like = {"malware"}
        spam_like = {"spam"}

        if normalized in phishing_like:
            return "phishing"
        if normalized in scam_like:
            return "scam"
        if normalized in malware_like:
            return "malware"
        if normalized in spam_like:
            return "spam"
        return "safe"
