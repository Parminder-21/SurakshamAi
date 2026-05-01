"""
Privacy scrubber utility to remove sensitive information.
"""

import re


def scrub_sensitive_data(text: str) -> str:
    """
    Redact common Indian personal identifiers and emails from `text`.

    Replacements use explicit tags:
    - [Phone Redacted]
    - [Aadhaar Redacted]
    - [PAN Redacted]
    - [Email Redacted]

    Args:
        text: Input text to scrub

    Returns:
        Scrubbed text with sensitive values replaced by tags.
    """
    if not text:
        return text

    # Aadhaar: 12 digits, may be grouped like 1234 5678 9012 or 123456789012
    aadhaar_pattern = re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b")

    # PAN: 5 letters, 4 digits, 1 letter (case-insensitive)
    pan_pattern = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", re.IGNORECASE)

    # Indian phone numbers: optional +91 / 91 / 0 prefix, then 10 digits (starting 6-9)
    phone_pattern = re.compile(r"(?:(?:\+91|91|0)[\-\s]?)?[6-9]\d{9}\b")

    # Email addresses
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE)

    # Order matters: redact Aadhaar (12-digit) before phone (10-digit) to avoid partial matches
    scrubbed = aadhaar_pattern.sub("[Aadhaar Redacted]", text)
    scrubbed = pan_pattern.sub("[PAN Redacted]", scrubbed)
    scrubbed = phone_pattern.sub("[Phone Redacted]", scrubbed)
    scrubbed = email_pattern.sub("[Email Redacted]", scrubbed)

    return scrubbed


def contains_sensitive_data(text: str) -> bool:
    """
    Check presence of any supported sensitive data patterns or redaction tags.

    Returns True if any known pattern or tag is found.
    """
    if not text:
        return False

    # Check for redaction tags first
    if any(tag in text for tag in ["[Aadhaar Redacted]", "[PAN Redacted]", "[Phone Redacted]", "[Email Redacted]"]):
        return True

    checks = [
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE),
        re.compile(r"(?:(?:\+91|91|0)[\-\s]?)?[6-9]\d{9}\b"),
        re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"),
        re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", re.IGNORECASE),
    ]

    for patt in checks:
        if patt.search(text):
            return True
    return False


# ----------------------
# Temporary test cases (docs / examples)
# ----------------------
"""
Test Cases (examples) - Kya karna hai: These are example inputs and expected redacted outputs.

1) Phone number with country code
   Input: "Call me at +91 9876543210 or 09876543210"
   Output: "Call me at [Phone Redacted] or [Phone Redacted]"

2) Aadhaar in groups
   Input: "My Aadhaar is 1234 5678 9012, please keep it safe."
   Output: "My Aadhaar is [Aadhaar Redacted], please keep it safe."

3) PAN mixed case
   Input: "PAN: aaapl1234c is linked"
   Output: "PAN: [PAN Redacted] is linked"

4) Email and phone together
   Input: "Contact: rahul@example.com or 9123456789"
   Output: "Contact: [Email Redacted] or [Phone Redacted]"

5) Multiple sensitive items
   Input: "Send KYC docs: 123456789012, PAN AAAPL1234C, email abc@mail.com"
   Output: "Send KYC docs: [Aadhaar Redacted], PAN [PAN Redacted], email [Email Redacted]"

Notes:
- Keep these examples here temporarily to avoid sending raw PI to external services.
"""
