from privacy_scrubber import contains_sensitive_data, scrub_sensitive_data


def test_scrub_sensitive_data_redacts_known_patterns():
    text = "Aadhaar 1234 5678 9012 PAN AAAPL1234C Phone +91 9876543210 Email user@example.com"
    scrubbed = scrub_sensitive_data(text)

    assert "1234 5678 9012" not in scrubbed
    assert "AAAPL1234C" not in scrubbed
    assert "9876543210" not in scrubbed
    assert "user@example.com" not in scrubbed
    assert "[Aadhaar Redacted]" in scrubbed
    assert "[PAN Redacted]" in scrubbed
    assert "[Phone Redacted]" in scrubbed
    assert "[Email Redacted]" in scrubbed


def test_contains_sensitive_data_detects_and_ignores_clean_text():
    assert contains_sensitive_data("Please call me at 9876543210") is True
    assert contains_sensitive_data("No PII here") is False
