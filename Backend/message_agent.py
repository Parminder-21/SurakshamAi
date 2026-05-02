"""
Message analysis agent for Suraksha Agent.

This version keeps the logic deterministic and beginner-friendly:
- scan the message for scam-taxonomy keywords and red flags
- derive a few simple signals
- send those signals to the risk engine
- return a structured dictionary
"""

from typing import Any, Dict, List, Tuple

from privacy_scrubber import contains_sensitive_data
from risk_engine import RiskEngine
from taxonomy import TAXONOMY


class MessageAgent:
    """Analyze message text and return a structured scam assessment."""

    def __init__(self):
        self.risk_engine = RiskEngine()
        self.taxonomy = TAXONOMY

        # Categories are grouped so we can convert keyword matches into a scam label.
        self.category_priority = [
            "otp_theft",
            "authority_impersonation",
            "upi_collect_request_scam",
            "fake_kyc",
            "electricity_bill_scam",
            "courier_scam",
            "job_scam",
            "lottery_scam",
        ]

        self.general_urgency_terms = [
            "urgent",
            "immediately",
            "now",
            "within 24 hours",
            "last chance",
            "expire",
            "suspended",
            "limited time",
            "act fast",
            "respond quickly",
        ]

        self.authority_terms = [
            "police",
            "court",
            "income tax",
            "rbi",
            "bank",
            "government",
            "official notice",
            "legal action",
            "fined",
            "authority",
        ]

        self.deception_terms = [
            "congratulations",
            "you won",
            "claim your prize",
            "free gift",
            "reward",
            "bonus",
            "verified",
            "confirm your details",
            "update kyc",
            "too good to be true",
        ]

        self.payment_terms = [
            "pay now",
            "payment",
            "send money",
            "transfer money",
            "fee",
            "charges",
            "deposit",
            "upi pin",
            "collect request",
            "scan qr",
        ]

        self.otp_terms = [
            "otp",
            "one time password",
            "verification code",
            "enter otp",
            "share otp",
        ]

    def analyze(self, message: str) -> Dict[str, Any]:
        """Analyze message text and return a structured result."""
        text = message or ""
        message_lower = text.lower()

        matched_keywords: List[str] = []
        reasons: List[str] = []

        category, category_keywords, category_red_flags = self._detect_category(message_lower)
        matched_keywords.extend(category_keywords)

        urgency_score, urgency_hits = self._score_terms(message_lower, self.general_urgency_terms, 25.0)
        authority_score, authority_hits = self._score_terms(message_lower, self.authority_terms, 25.0)
        deception_score, deception_hits = self._score_terms(message_lower, self.deception_terms, 25.0)
        payment_score, payment_hits = self._score_terms(message_lower, self.payment_terms, 25.0)
        payment_pressure = bool(payment_hits)
        otp_request, otp_hits = self._flag_terms(message_lower, self.otp_terms)
        suspicious_link = self._has_suspicious_link(message_lower)
        reward_promise = self._has_reward_promise(message_lower)

        # Add category-specific matches to the output and reasons.
        matched_keywords.extend(urgency_hits)
        matched_keywords.extend(authority_hits)
        matched_keywords.extend(deception_hits)
        matched_keywords.extend(payment_hits)
        matched_keywords.extend(otp_hits)

        if category != "safe":
            reasons.append(f"Matched scam taxonomy category: {category}")
            reasons.append(category_red_flags)

        if urgency_hits:
            reasons.append("Urgency language detected")
        if authority_hits:
            reasons.append("Authority impersonation language detected")
        if deception_hits:
            reasons.append("Deceptive or reward-based language detected")
        if payment_pressure:
            reasons.append("Payment pressure detected")
        if suspicious_link:
            reasons.append("Suspicious link detected")
        if otp_request:
            reasons.append("OTP request detected")
        if reward_promise:
            reasons.append("Suspicious reward promise detected")
        if contains_sensitive_data(text):
            reasons.append("Sensitive personal data present in the message")
            deception_score = max(deception_score, 25.0)

        # Signal if any scam category was matched by taxonomy
        category_match = (category != "safe")

        # Keep output deterministic and easy to explain.
        risk_score, severity = self.risk_engine.calculate_risk_score(
            urgency_score=urgency_score,
            authority_score=authority_score,
            deception_score=deception_score,
            payment_score=payment_score,
            suspicious_link=suspicious_link,
            otp_request=otp_request,
            category_match=category_match,
            unrealistic_promise=reward_promise
        )

        if suspicious_link:
            matched_keywords.append("suspicious_link")
        if reward_promise:
            matched_keywords.append("reward_promise")

        if category == "safe" and risk_score < 25:
            category = "safe"
        elif category == "safe":
            category = self._category_from_signals(urgency_score, authority_score, deception_score)

        return {
            "category": category,
            "risk_score": risk_score,
            "severity": severity,
            "reasons": self._unique_keep_order([r for r in reasons if r]),
            "matched_keywords": self._unique_keep_order(matched_keywords),
        }

    def analyze_legacy(self, message: str) -> Tuple[str, float, List[str]]:
        """Backward-compatible tuple output for older callers."""
        result = self.analyze(message)
        return result["category"], result["risk_score"], result["reasons"]

    def _detect_category(self, message_lower: str) -> Tuple[str, List[str], str]:
        """Pick the most likely scam taxonomy category."""
        best_category = "safe"
        best_score = 0
        matched_keywords: List[str] = []
        matched_red_flags: List[str] = []

        for category_name in self.category_priority:
            entry = self.taxonomy.get(category_name, {})
            keywords = entry.get("keywords", [])
            red_flags = entry.get("red_flags", [])

            keyword_hits = [keyword for keyword in keywords if keyword.lower() in message_lower]
            red_flag_hits = [flag for flag in red_flags if flag.lower() in message_lower]

            score = (len(keyword_hits) * 2) + (len(red_flag_hits) * 4)
            if score > best_score:
                best_category = category_name
                best_score = score
                matched_keywords = keyword_hits
                matched_red_flags = red_flag_hits

        red_flag_text = ", ".join(matched_red_flags) if matched_red_flags else "No explicit taxonomy red flags matched"
        if best_score == 0:
            return "safe", [], red_flag_text
        return best_category, matched_keywords, red_flag_text

    def _score_terms(self, message_lower: str, terms: List[str], max_score: float) -> Tuple[float, List[str]]:
        """Return a simple score based on matched terms."""
        hits = [term for term in terms if term in message_lower]
        if not hits:
            return 0.0, []
        score = min(max_score, 8.0 * len(hits))
        return score, hits

    def _flag_terms(self, message_lower: str, terms: List[str]) -> Tuple[bool, List[str]]:
        """Return whether any term is present and the matched terms."""
        hits = [term for term in terms if term in message_lower]
        return bool(hits), hits

    def _has_suspicious_link(self, message_lower: str) -> bool:
        """Detect a link that should be treated as suspicious."""
        import re

        link_pattern = r"https?://\S+|www\.\S+|bit\.ly|tinyurl\.com|goo\.gl|shorturl"
        return bool(re.search(link_pattern, message_lower, re.IGNORECASE))

    def _has_reward_promise(self, message_lower: str) -> bool:
        """Detect suspicious reward/lottery-style promises."""
        reward_terms = [
            "you won",
            "claim your prize",
            "lottery",
            "reward",
            "cash prize",
            "free gift",
            "selected winner",
            "bonus amount",
        ]
        return any(term in message_lower for term in reward_terms)

    def _category_from_signals(self, urgency_score: float, authority_score: float, deception_score: float) -> str:
        """Fallback category when taxonomy did not match exactly."""
        if authority_score >= urgency_score and authority_score >= deception_score:
            return "authority_impersonation"
        if deception_score >= urgency_score:
            return "lottery_scam"
        return "job_scam"

    def _unique_keep_order(self, items: List[str]) -> List[str]:
        """Remove duplicates without changing order."""
        seen = set()
        unique_items = []
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)
        return unique_items
