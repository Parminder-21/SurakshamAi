# Suraksha Agent — AI-Powered Cyber Safety Companion
**Protecting India's 900M+ Smartphone Users from Digital Fraud.**

Suraksha Agent is a comprehensive ecosystem designed for the Agentic AI Hackathon by Microsoft. It actively scans SMS, URLs, and phone calls to identify local scams (like Fake KYC, Electricity Bill Fraud, and Job Scams) using an intelligent, orchestrated LangGraph architecture.

---

## 🏗️ The Ecosystem Architecture

Our MVP consists of three primary layers:

### 1. The Brain (FastAPI + LangGraph)
Located in `/Backend`.
- **LangGraph Orchestrator**: The central nervous system. A `StateGraph` that passes "Shared Risk Registry" context sequentially between the URL Agent and Message Agent.
- **Scam Taxonomy Engine**: Custom-built logic recognizing 8 India-specific fraud categories with dynamic 0-100 risk scoring matrices.
- **Privacy Scrubber**: Enforces DPDP Act compliance by masking Aadhaar, PAN, Emails, Phones, and uses `spaCy` NLP for Name Entity Recognition (NER) to redact names (`[Name Redacted]`) and organizations.

### 2. The Shield (Android App)
Located in `/android`.
- Built with **Jetpack Compose** (Material 3).
- Features an elegant **Tabbed Navigation** interface (Message, URL, Call Scanners).
- Displays animated **Risk Cards** with circular progress bars, clear warning reasons, and safe action checklists.

### 3. The Radar (Cyber Awareness Website)
Located in `/website`.
- A hyper-optimized, premium **Glassmorphism Vanilla UI**.
- Connects to the backend to display a live feed of trending scams (`/news-feed`).
- Allows users to crowd-source scam reports via the community reporting tool (`/report-scam`).

---

## 🚀 How to Run Locally

### Starting the Backend (The Brain)
```bash
cd Backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python main.py
```
*The API will be available at `http://localhost:8000`*

### Starting the Website (The Radar)
No build steps required! Simply open the `website/index.html` file in your preferred web browser. It will automatically connect to `http://localhost:8000` to fetch live data.

### Starting the Android App (The Shield)
Open the `/android` folder in **Android Studio**. Sync the gradle files and run on an emulator or physical device.

---

## 🧪 Quick Test Scenarios
Try sending these through the Android App or via a POST request to `http://localhost:8000/analyze-message`:

- **Fake KYC**: *"Dear SBI Customer, your PAN KYC is expiring today. Your account will be blocked. Update immediately here: https://bit.ly/sbi-update"*
- **Electricity Scam**: *"Dear Consumer, your power will be disconnected at 9:30 PM tonight because your previous month bill was not updated. Call electricity officer immediately."*
- **Safe Message**: *"Hey, what time are we meeting for dinner tomorrow?"*

---
*Built for the Agentic AI Hackathon by Microsoft.*
