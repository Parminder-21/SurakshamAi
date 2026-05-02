# Suraksha Agent Demo Scenarios

Use these scenarios during your hackathon presentation to showcase the capabilities of the Risk Engine, Scam Taxonomy, Privacy Scrubber, and LangGraph Orchestrator.

## 1. Fake KYC with Privacy Data
**Goal**: Show how the AI recognizes Fake KYC scams, and how the **Privacy Scrubber** masks PII (Name, Aadhaar, Phone) before processing.

**Input Type**: Message
**Copy & Paste:**
> "Dear Rahul Sharma, your SBI account KYC is pending. Update your Aadhaar 1234-5678-9012 immediately or your account will be frozen. Call us at 9876543210 or visit https://bit.ly/sbi-kyc-update-secure to update."

**Expected Result**:
- `severity`: high_risk
- `risk_score`: 100/100 (Payment pressure + OTP/Urgency + Shortener Link)
- `category`: fake_kyc
- `scrubbed_text`: Watch how "Rahul Sharma" becomes `[Name Redacted]`, the Aadhaar becomes `[Aadhaar Redacted]`, and the phone number becomes `[Phone Redacted]`.

---

## 2. Electricity Bill Extortion
**Goal**: Show how the system handles offline urgency threats.

**Input Type**: Call Summary / Message
**Copy & Paste:**
> "Dear Customer, your electricity power will be disconnected tonight at 9:30 PM from the main office because your previous month bill was not updated. Please immediately contact our electricity officer to pay the pending due."

**Expected Result**:
- `category`: electricity_bill_scam
- `reasons`: Will flag the extreme urgency and authority impersonation.

---

## 3. The "Too Good To Be True" Job Scam
**Goal**: Demonstrate the detection of unrealistic promises combined with payment pressure.

**Input Type**: Message
**Copy & Paste:**
> "Congratulations! You have been selected for a part-time Work From Home job. Earn Rs 5000 to Rs 10000 daily. Just like YouTube videos. Pay a one-time refundable registration fee of Rs 1500 to start."

**Expected Result**:
- `category`: job_scam
- `severity`: suspicious or high_risk

---

## 4. Phishing URL Scan
**Goal**: Show the URL Agent independently catching misleading domains and punycode.

**Input Type**: URL
**Copy & Paste:**
> "http://www.hdfcbank-secure-update-portal-xyz.com/login"

**Expected Result**:
- `category`: phishing
- `reasons`: Will flag "lookalike domain", "suspicious keywords (login, secure, update)", and domain length.

---

## 5. Safe Communication
**Goal**: Prove that the AI doesn't yield false positives for regular chat.

**Input Type**: Message
**Copy & Paste:**
> "Hey Ravi, I sent you the 500 rupees I owed you for dinner last night. Let me know if you got it!"

**Expected Result**:
- `category`: safe
- `severity`: safe
- `risk_score`: Low
- `reasons`: No manipulation or urgency tactics found.
