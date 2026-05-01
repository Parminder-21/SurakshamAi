# Quick Start Guide - Suraksha Agent Backend

## 1. Install Dependencies (First Time Only)

```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Run Demo (Optional - Verify Installation)

```bash
python demo.py
```

You should see test results for message analysis, URL analysis, risk engine, and guidance agent.

## 3. Start the Server

```bash
python main.py
```

You'll see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

## 4. Test the API

### Option A: Using Interactive Swagger UI (Easiest)
Open in browser: http://localhost:8000/docs

### Option B: Using cURL

```bash
# Test health endpoint
curl http://localhost:8000/health

# Analyze a message
curl -X POST "http://localhost:8000/analyze-message" \
  -H "Content-Type: application/json" \
  -d '{"message": "Click here to verify your account!"}'

# Analyze a URL
curl -X POST "http://localhost:8000/analyze-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://malicious-site.com"}'
```

### Option C: Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze-message",
    json={"message": "Congratulations! You won $1000!"}
)
print(response.json())
```

## 5. Stop the Server

Press `Ctrl+C` in the terminal

## Common Issues

### "ModuleNotFoundError: No module named 'fastapi'"
→ Make sure you've activated the virtual environment and installed requirements

### "Address already in use"
→ The port 8000 is in use. Try: `uvicorn main:app --port 8001`

### "Virtual environment not activated"
→ Run: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)

## Next Steps

- Read [Backend/README.md](README.md) for detailed documentation
- Explore the API at http://localhost:8000/docs
- Study the modular structure to understand each component
- Run `demo.py` to test modules independently
