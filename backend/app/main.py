from fastapi import FastAPI

app = FastAPI(title="Suraksham AI Backend")

@app.get("/")
async def root():
    return {"message": "Welcome to Suraksham AI API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
