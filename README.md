# Suraksham AI 🛡️

**Suraksham AI** is a privacy-first cyber safety assistant designed for Indian users. It detects suspicious messages and risky URLs, assigns a risk score, and provides preventive guidance using a multi-agent AI backend.

## 🚀 Overview

- **Android App**: A modern, reactive interface built with Kotlin and Jetpack Compose.
- **FastAPI Backend**: A high-performance Python backend serving as the gateway to AI agents.
- **Agentic AI**: A LangGraph-powered multi-agent system that collaborates to analyze threats and provide actionable advice.

## ✨ Key Features

- **Message Analysis**: Paste suspicious SMS or chat messages for instant risk assessment.
- **URL Scanning**: Real-time reputation checks for links using specialized AI agents.
- **Risk Scoring**: Visual risk indicators (Low, Medium, High) with detailed findings.
- **Preventive Guidance**: Actionable steps in English and Hindi, including links to the 1930 Cyber Helpline.

## 🏗️ Architecture

- **Frontend**: Kotlin, Jetpack Compose, Retrofit, Lottie.
- **Backend**: Python, FastAPI, LangGraph, LangChain.
- **Deployment**: Local testing for hackathon demo.

## 📂 Folder Structure

- `android/`: Jetpack Compose Android application.
- `backend/`: FastAPI backend and LangGraph agents.
- `docs/`: Project documentation and architecture details.

## 🛠️ Setup

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python app/main.py`

### Android
1. Open `android/` in Android Studio.
2. Build and run the app.

---

Made for the Hackathon 2026.
