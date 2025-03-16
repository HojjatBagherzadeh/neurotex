from fastapi import FastAPI, BackgroundTasks, HTTPException
from .schemas import AnalyzeStartRequest, AnalyzeStartResponse, AnalyzeFunctionRequest, AnalyzeFunctionResponse
from . import repo_manager, function_extractor
import os
import requests

app = FastAPI()

# LLM Service URL (set via docker-compose or environment)
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8000")

@app.post("/analyze/start", response_model=AnalyzeStartResponse)
async def analyze_start(request: AnalyzeStartRequest, background_tasks: BackgroundTasks):
    job_id = repo_manager.create_job(request.repo_url)
    background_tasks.add_task(repo_manager.download_repo, job_id)
    return AnalyzeStartResponse(job_id=job_id)

@app.post("/analyze/function", response_model=AnalyzeFunctionResponse)
async def analyze_function(request: AnalyzeFunctionRequest):
    job = repo_manager.jobs.get(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Repository not downloaded yet or failed")
    try:
        function_code = function_extractor.extract_function_code(job["repo_path"], request.function_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        # Call the LLM Service via its API (simulating an OpenAI-like call)
        llm_response = requests.post(f"{LLM_SERVICE_URL}/analyze", json={"function_code": function_code})
        llm_response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail="LLM service error: " + str(e))
    
    suggestions = llm_response.json().get("suggestions", [])
    return AnalyzeFunctionResponse(suggestions=suggestions)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
