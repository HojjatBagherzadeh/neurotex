from fastapi import FastAPI
from .schemas import AnalyzeRequest, AnalyzeResponse
from .llm_client import analyze_function

app = FastAPI()

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    suggestions = analyze_function(request.function_code)
    return AnalyzeResponse(suggestions=suggestions)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
