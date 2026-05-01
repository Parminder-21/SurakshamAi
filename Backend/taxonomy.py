"""
Indian scam taxonomy for Suraksha Agent.

Each category contains:
- description: short description of the scam
- keywords: list of indicative keywords/phrases
- red_flags: list of specific red flags to look for
- advice: short "Kya karna hai" guidance in Hindi

This file is intended to be imported by analysis agents (e.g., message_agent.py).
"""

from typing import Dict


TAXONOMY: Dict[str, Dict] = {
    "fake_kyc": {
        "description": "Scammers ask users to complete a fake KYC by sharing personal documents or links.",
        "keywords": ["kyc", "complete kyc", "verify kyc", "upload documents", "submit id", "aadhar", "pan"],
        "red_flags": ["requests for scanned IDs or selfies via chat", "links asking to upload documents", "pressure to complete immediately"],
        "advice": "Kya karna hai: Kisi bhi anjaane link par apna KYC na bhejein. Official app/website par directly login karke hi verify karein. Agar kisi ne personal documents maangein to report karein."
    },
    "electricity_bill_scam": {
        "description": "Fraudulent messages claiming unpaid electricity bills or disconnection threats to extract payment.",
        "keywords": ["bill unpaid", "electricity bill", "disconnection", "pay now", "arrears", "immediate payment"],
        "red_flags": ["threats of immediate disconnection", "requests for payment via unfamiliar channels", "links to non-official payment pages"],
        "advice": "Kya karna hai: Utility company ki official website/app par login karke bill check karein. Unofficial payment links par paisa na bhejein. Payment karne se pehle customer care se confirm karein."
    },
    "courier_scam": {
        "description": "Messages claiming a parcel is held and asking for payment or personal details to release it.",
        "keywords": ["parcel held", "delivery failed", "customs fee", "pay to release", "courier charge", "tracking"],
        "red_flags": ["requests for payment to release parcel", "asks for bank/gateway details", "unexpected tracking links or shorteners"],
        "advice": "Kya karna hai: Tracking number courier ki official website par verify karein. Agar parcel expected nahi hai to links par click na karein aur personal details share na karein."
    },
    "job_scam": {
        "description": "Fraudulent job offers asking for fees, bank details, or personal documents upfront.",
        "keywords": ["job offer", "work from home", "earn", "pay for training", "registration fee", "interview link"],
        "red_flags": ["requests for upfront fees", "generic company email addresses (gmail/yahoo)", "too-good-to-be-true salary offers"],
        "advice": "Kya karna hai: Official company channels se verify karein. Kisi ko paise bhejne se pehle research karein. Interview links aur attachments ko carefully check karein."
    },
    "upi_collect_request_scam": {
        "description": "Fraud where attackers send UPI collect requests (or fake screenshots) to trick users into approving payments.",
        "keywords": ["collect request", "upi request", "approve collect", "pay via upi", "scan qr", "complete payment"],
        "red_flags": ["unexpected collect request from unknown number", "pressure to approve quickly", "amounts that change on confirmation"],
        "advice": "Kya karna hai: UPI notifications ko dhyan se check karein. Agar request anjaani ho to reject karein aur sender ko verify karein. Kabhi bhi OTP ya UPI PIN share na karein."
    },
    "lottery_scam": {
        "description": "Messages claiming the user has won a lottery/prize and asking for fees to claim it.",
        "keywords": ["congratulations", "you won", "prize", "claim your prize", "pay fee to claim", "tax to claim"],
        "red_flags": ["requests for payment to receive prize", "asks for bank details or fees", "unexpected notifications claiming big wins"],
        "advice": "Kya karna hai: Agar aapne kisi contest me hissa nahi liya to ye scam ho sakta hai. Kisi bhi prize ke liye paise na bhejein. Official channels se confirm karein."
    },
    "authority_impersonation": {
        "description": "Scammers impersonate banks, government agencies, or police to coerce users into sharing information or paying fines.",
        "keywords": ["income tax", "police", "court notice", "fine", "payment due", "suspended account", "govt notice"],
        "red_flags": ["urgent legal threats via SMS/WhatsApp", "requests for bank transfers to avoid penalty", "official-sounding but unofficial contact details"],
        "advice": "Kya karna hai: Official portals ya registered helplines par contact karein. Kabhi bhi call/ message par bank details ya OTP share na karein. Agar legal action ka dar hai to directly concerned authority se verify karein."
    },
    "otp_theft": {
        "description": "Attacker tricks user into revealing OTPs through social engineering, fake verification prompts, or malicious links. These OTPs are then used to complete transactions or take over accounts.",
        "keywords": ["otp", "one time password", "verification code", "enter otp", "did you request"],
        "red_flags": ["ask for OTP over chat/call", "unexpected OTP messages", "links asking to enter OTP on third-party sites"],
        "advice": "Kya karna hai: OTP kisi ko share na karein. Agar aapko unexpected OTP aaya hai to kisi ne aapke account ke liye request kiya ho sakta hai — immediately check and secure your account."
    }
}


__all__ = ["TAXONOMY"]
