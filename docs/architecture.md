# Suraksham AI - Architecture Documentation

## Overview
Suraksham AI is a privacy-first cyber safety assistant designed to protect Indian users from phishing, scams, and malicious URLs. The project is built using a modern mobile frontend and an agentic AI backend.

## System Architecture

### 1. Frontend (Android)
- **Framework**: Kotlin & Jetpack Compose.
- **UI/UX**: Premium, dark-mode focused design with high-impact visual indicators for risk levels.
- **Key Features**:
  - Manual Scan: Users can paste messages or URLs.
  - History: Local storage of previous scans for user reference.
  - Education: A section for cyber safety tips tailored for the Indian context.

### 2. Backend (FastAPI)
- **Language**: Python 3.10+
- **API**: Async endpoints for low-latency AI processing.
- **Role**: Serves as the orchestration layer between the mobile app and the AI agents.

### 3. AI Engine (LangGraph)
The heart of the system is a multi-agent graph:
- **Linguistic Analyzer Agent**: Detects scam patterns, urgency, and threat language. Specializes in Hinglish and Indian context (e.g., "Electricity bill scam," "KYC fraud").
- **URL Intel Agent**: Scans URLs for phishing signatures, redirects, and known malicious domains.
- **Risk Scorer**: A specialized node that weighs findings from other agents to produce a final 0-100 risk score.
- **Prevention Advisor**: Generates personalized guidance based on the threat type.

## Data Flow
1. User submits content via the Android App.
2. App sends a request to the FastAPI `/v1/analyze` endpoint.
3. FastAPI triggers the LangGraph workflow.
4. Agents collaborate and return a structured JSON response.
5. Android App renders the result with color-coded risk indicators and guidance.

## Execution Plan (24-Hour Hackathon)

### Milestones
- **H 0-2**: Project scaffolding and API contract definition.
- **H 2-6**: LangGraph implementation and Agent logic.
- **H 6-10**: Frontend UI development (Dashboard & Results).
- **H 10-14**: End-to-End Integration.
- **H 14-20**: Prompt tuning for local context and UI polish.
- **H 20-24**: Demo preparation and final testing.

## Folder Structure
```text
SurakshamAI/
├── android/               # Android App (Kotlin/Compose)
├── backend/               # FastAPI Backend
│   ├── app/
│   │   ├── agents/        # LangGraph nodes
│   │   ├── routes/        # API routes
│   └── main.py
├── docs/                  # Documentation
└── scripts/               # Helper scripts
```

## Future Scope (Stretch Features)
- Real-time notification scanning.
- OCR for screenshot analysis.
- Multi-lingual support for 10+ Indian regional languages.
