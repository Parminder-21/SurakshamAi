"""
URL analysis agent for Suraksha Agent.

This module is intentionally simple and deterministic:
- inspect the URL with a few rule-based checks
- score each suspicious feature in a transparent way
- return a structured dictionary that is easy to explain in demos
"""

from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

from risk_engine import RiskEngine


class URLAgent:
    """Analyze a URL using straightforward, explainable rules."""

    def __init__(self):
        self.risk_engine = RiskEngine()

        self.suspicious_keywords = [
            "login",
            "verify",
            "reward",
            "update-kyc",
            "kyc",
            "account",
            "secure",
            "confirm",
            "claim",
            "bonus",
        ]

        self.shortener_domains = [
            "bit.ly",
            "tinyurl.com",
            "ow.ly",
            "t.co",
            "goo.gl",
            "is.gd",
        ]

        self.suspicious_extensions = [
            ".exe",
            ".bat",
            ".cmd",
            ".com",
            ".scr",
            ".vbs",
            ".js",
            ".zip",
            ".rar",
        ]

        self.trusted_like_words = [
            "login",
            "secure",
            "verify",
            "update",
            "bank",
            "support",
            "reward",
            "wallet",
        ]

    def analyze(self, url: str) -> Dict[str, Any]:
        """Analyze a URL and return a structured risk result."""
        raw_url = (url or "").strip()
        if not raw_url:
            return self._build_result(
                category="safe",
                risk_score=0.0,
                reasons=["URL is empty"],
                flags=[],
            )

        normalized_url = self._normalize_url(raw_url)
        parsed = urlparse(normalized_url)

        domain = (parsed.netloc or "").lower()
        path = (parsed.path or "").lower()
        full_url = normalized_url.lower()

        reasons: List[str] = []
        flags: List[str] = []
        scores: List[float] = []

        shortener_flag, shortener_score = self._check_shortener_domain(domain)
        if shortener_flag:
            flags.append("shortener_domain")
            scores.append(shortener_score)
            reasons.append("URL uses a shortening service")

        ip_flag, ip_score = self._check_ip_based_url(domain)
        if ip_flag:
            flags.append("ip_based_url")
            scores.append(ip_score)
            reasons.append("URL uses an IP address instead of a domain name")

        hyphen_flag, hyphen_score = self._check_hyphen_count(domain)
        if hyphen_flag:
            flags.append("too_many_hyphens")
            scores.append(hyphen_score)
            reasons.append("Domain contains too many hyphens")

        long_flag, long_score = self._check_url_length(full_url)
        if long_flag:
            flags.append("too_long_url")
            scores.append(long_score)
            reasons.append("URL is unusually long")

        keyword_flags, keyword_score, keyword_reasons = self._check_keywords(full_url)
        if keyword_flags:
            flags.extend(keyword_flags)
            scores.append(keyword_score)
            reasons.extend(keyword_reasons)

        domain_flag, domain_score, domain_reasons = self._check_misleading_domain(domain)
        if domain_flag:
            flags.extend(domain_flag)
            scores.append(domain_score)
            reasons.extend(domain_reasons)

        extension_flag, extension_score = self._check_extensions(path)
        if extension_flag:
            flags.append("suspicious_file_extension")
            scores.append(extension_score)
            reasons.append(f"URL ends with a risky file extension ({extension_flag})")

        if not scores:
            return self._build_result(
                category="safe",
                risk_score=0.0,
                reasons=["No suspicious URL features detected"],
                flags=[],
            )

        risk_score = self.risk_engine.combine_scores(scores)
        severity = self._score_to_severity(risk_score)
        category = self._select_category(flags, reasons)

        return self._build_result(
            category=category,
            risk_score=risk_score,
            reasons=self._unique_keep_order(reasons),
            flags=self._unique_keep_order(flags),
            severity=severity,
        )

    def analyze_legacy(self, url: str) -> Tuple[str, float, List[str]]:
        """Backward-compatible tuple output for older callers."""
        result = self.analyze(url)
        return result["category"], result["risk_score"], result["reasons"]

    def _normalize_url(self, url: str) -> str:
        """Add a scheme if the URL is missing one."""
        if "://" not in url:
            return f"http://{url}"
        return url

    def _check_ip_based_url(self, domain: str) -> Tuple[bool, float]:
        """Detect URLs that use an IP address instead of a domain."""
        parts = domain.split(":")[0].split(".")
        if len(parts) != 4:
            return False, 0.0

        try:
            octets = [int(part) for part in parts]
        except ValueError:
            return False, 0.0

        if all(0 <= octet <= 255 for octet in octets):
            return True, 30.0
        return False, 0.0

    def _check_hyphen_count(self, domain: str) -> Tuple[bool, float]:
        """Flag domains with too many hyphens."""
        hyphen_count = domain.count("-")
        if hyphen_count >= 3:
            return True, min(20.0 + (hyphen_count - 3) * 5.0, 35.0)
        return False, 0.0

    def _check_url_length(self, url: str) -> Tuple[bool, float]:
        """Flag URLs that are unusually long."""
        if len(url) > 180:
            return True, 15.0
        if len(url) > 120:
            return True, 10.0
        return False, 0.0

    def _check_shortener_domain(self, domain: str) -> Tuple[bool, float]:
        """Detect common URL shortener domains."""
        for shortener in self.shortener_domains:
            if shortener in domain:
                return True, 18.0
        return False, 0.0

    def _check_keywords(self, url: str) -> Tuple[List[str], float, List[str]]:
        """Find suspicious keywords in the URL path, host, or query string."""
        hits: List[str] = []
        reasons: List[str] = []

        for keyword in self.suspicious_keywords:
            if keyword in url:
                hits.append(f"keyword:{keyword}")
                reasons.append(f"Suspicious keyword detected in URL: {keyword}")

        if not hits:
            return [], 0.0, []

        score = min(12.0 * len(hits), 30.0)
        return hits, score, reasons

    def _check_misleading_domain(self, domain: str) -> Tuple[List[str], float, List[str]]:
        """Flag domains that look misleading or try to imitate a legitimate service."""
        if not domain:
            return [], 0.0, []

        flags: List[str] = []
        reasons: List[str] = []
        score = 0.0

        # Many subdomains often hide the real destination.
        subdomain_count = domain.count(".")
        if subdomain_count >= 3:
            flags.append("many_subdomains")
            score += 12.0
            reasons.append("Domain has many subdomains")

        # Punycode domains are often used in look-alike attacks.
        if domain.startswith("xn--") or ".xn--" in domain:
            flags.append("punycode_domain")
            score += 20.0
            reasons.append("Domain uses punycode and may be misleading")

        # Look-alike domains often combine trusted words with extra hyphens or odd TLDs.
        trusted_word_hits = [word for word in self.trusted_like_words if word in domain]
        if trusted_word_hits and (domain.count("-") >= 2 or subdomain_count >= 2):
            flags.append("lookalike_domain")
            score += 15.0
            reasons.append("Domain looks like a legitimate service but has extra structure")

        # Random-looking domains with trusted terms can be misleading too.
        if trusted_word_hits and len(domain) > 20:
            flags.append("suspicious_brand_like_domain")
            score += 10.0
            reasons.append("Domain mixes trusted words with a long random-looking name")

        return flags, min(score, 35.0), reasons

    def _check_extensions(self, path: str) -> Tuple[str, float]:
        """Detect risky file extensions in the URL path."""
        for ext in self.suspicious_extensions:
            if path.endswith(ext):
                return ext, 25.0 if ext in {".zip", ".rar", ".js", ".vbs", ".exe", ".bat", ".cmd", ".scr"} else 15.0
        return "", 0.0

    def _select_category(self, flags: List[str], reasons: List[str]) -> str:
        """Pick a simple label based on the strongest signals."""
        joined = " ".join(flags + reasons).lower()

        if any(flag in flags for flag in ["shortener_domain", "ip_based_url", "keyword:login", "keyword:verify", "lookalike_domain"]):
            return "phishing"
        if any(flag in flags for flag in ["suspicious_file_extension", "punycode_domain"]):
            return "malware"
        if any(flag in flags for flag in ["keyword:reward", "keyword:claim", "keyword:bonus"]):
            return "scam"
        if any(word in joined for word in ["login", "verify", "reward", "kyc"]):
            return "suspicious_url"
        return "suspicious_url"

    def _score_to_severity(self, risk_score: float) -> str:
        """Map a score to the simple labels used in the app."""
        if risk_score >= 65:
            return "high_risk"
        if risk_score >= 25:
            return "suspicious"
        return "safe"

    def _build_result(
        self,
        category: str,
        risk_score: float,
        reasons: List[str],
        flags: List[str],
        severity: str = "safe",
    ) -> Dict[str, Any]:
        """Build the structured response dictionary."""
        return {
            "category": category,
            "risk_score": round(max(0.0, min(100.0, risk_score)), 2),
            "severity": severity,
            "reasons": self._unique_keep_order(reasons),
            "flags": self._unique_keep_order(flags),
        }

    def _unique_keep_order(self, items: List[str]) -> List[str]:
        """Remove duplicates without changing order."""
        seen = set()
        unique_items: List[str] = []

        for item in items:
            if item in seen:
                continue
            seen.add(item)
            unique_items.append(item)

        return unique_items
