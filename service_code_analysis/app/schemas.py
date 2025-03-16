from pydantic import BaseModel
from typing import List

class AnalyzeStartRequest(BaseModel):
    repo_url: str

class AnalyzeStartResponse(BaseModel):
    job_id: str

class AnalyzeFunctionRequest(BaseModel):
    job_id: str
    function_name: str

class AnalyzeFunctionResponse(BaseModel):
    suggestions: List[str]
