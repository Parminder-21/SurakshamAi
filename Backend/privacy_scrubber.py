"""
Privacy scrubber utility to remove sensitive information.
"""

import re


def scrub_sensitive_data(text: str) -> str:
    """
    Remove sensitive information from text.
    
    Args:
        text: Input text to scrub
        
    Returns:
        Text with sensitive data redacted
    """
    # Scrub email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # Scrub phone numbers (various formats)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    text = re.sub(r'\+\d{1,3}\s?\d{1,14}', '[PHONE]', text)
    
    # Scrub credit card-like patterns (16 digits)
    text = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[CARD]', text)
    
    # Scrub SSN-like patterns (xxx-xx-xxxx)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
    
    # Scrub API keys and tokens (simple pattern)
    text = re.sub(r'\b[A-Za-z0-9_-]{40,}\b', '[TOKEN]', text)
    
    return text


def contains_sensitive_data(text: str) -> bool:
    """
    Check if text contains sensitive information.
    
    Args:
        text: Input text to check
        
    Returns:
        True if sensitive data is detected, False otherwise
    """
    patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone
        r'\+\d{1,3}\s?\d{1,14}',  # International phone
        r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
    ]
    
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    
    return False
