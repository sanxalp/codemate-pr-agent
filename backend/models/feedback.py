from pydantic import BaseModel
from typing import List, Optional, Literal

class Issue(BaseModel):
    type: Literal["error", "warning", "info"]
    file: str
    line: Optional[int] = None
    message: str
    suggestion: Optional[str] = None

class ReviewFeedback(BaseModel):
    summary: str
    issues: List[Issue]
    score: int  # 0-100
    recommendations: List[str]

class PRData(BaseModel):
    title: str
    description: str
    files_changed: List[dict]
    diff: str
    author: str
    url: str
    provider: str