"""
Privacy scrubber utility to remove sensitive information.
Uses regex for patterns (Aadhaar, PAN, Phone, Email)
Uses spaCy for Name Entity Recognition (PERSON, ORG).
"""

import re
import logging

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except (ImportError, OSError):
    SPACY_AVAILABLE = False
    logging.warning("spaCy or en_core_web_sm not installed. NLP Name redaction disabled. "
                    "Run: pip install spacy && python -m spacy download en_core_web_sm")

def scrub_sensitive_data(text: str) -> str:
    """
    Redact common Indian personal identifiers, emails, and names from `text`.

    Replacements use explicit tags:
    - [Phone Redacted]
    - [Aadhaar Redacted]
    - [PAN Redacted]
    - [Email Redacted]
    - [Name Redacted]
    - [Org Redacted]

    Args:
        text: Input text to scrub

    Returns:
        Scrubbed text with sensitive values replaced by tags.
    """
    if not text:
        return text

    # Step 1: Regex Redaction for strict patterns
    # Aadhaar: 12 digits, may be grouped like 1234 5678 9012 or 123456789012
    aadhaar_pattern = re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b")
    # PAN: 5 letters, 4 digits, 1 letter (case-insensitive)
    pan_pattern = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", re.IGNORECASE)
    # Indian phone numbers: optional +91 / 91 / 0 prefix, then 10 digits (starting 6-9)
    phone_pattern = re.compile(r"(?:(?:\+91|91|0)[\-\s]?)?[6-9]\d{9}\b")
    # Email addresses
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE)

    scrubbed = aadhaar_pattern.sub("[Aadhaar Redacted]", text)
    scrubbed = pan_pattern.sub("[PAN Redacted]", scrubbed)
    scrubbed = phone_pattern.sub("[Phone Redacted]", scrubbed)
    scrubbed = email_pattern.sub("[Email Redacted]", scrubbed)

    # Step 2: NLP Redaction for Names and Organizations (spaCy)
    if SPACY_AVAILABLE:
        doc = nlp(scrubbed)
        # Process from right to left to avoid index shifting when replacing text
        entities = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        entities.sort(key=lambda x: x[0], reverse=True)
        
        for start_char, end_char, label in entities:
            if label == "PERSON":
                scrubbed = scrubbed[:start_char] + "[Name Redacted]" + scrubbed[end_char:]
            elif label == "ORG":
                # Only redact organization if it doesn't overlap with known entities we want to keep
                # For a hackathon, aggressive redaction is fine for privacy.
                scrubbed = scrubbed[:start_char] + "[Org Redacted]" + scrubbed[end_char:]

    return scrubbed

def contains_sensitive_data(text: str) -> bool:
    """
    Check presence of any supported sensitive data patterns or redaction tags.
    Returns True if any known pattern or tag is found.
    """
    if not text:
        return False

    # Check for redaction tags first
    tags = ["[Aadhaar Redacted]", "[PAN Redacted]", "[Phone Redacted]", "[Email Redacted]", "[Name Redacted]", "[Org Redacted]"]
    if any(tag in text for tag in tags):
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
            
    if SPACY_AVAILABLE:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                return True

    return False
