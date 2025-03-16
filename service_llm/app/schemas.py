from pydantic import BaseModel
from typing import List

class AnalyzeRequest(BaseModel):
    function_code: str

class AnalyzeResponse(BaseModel):
    suggestions: List[str]
