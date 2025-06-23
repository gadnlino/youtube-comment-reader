from typing import Optional
from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    text: str
    videoTitle: Optional[str]

class CommentAnalysisRequest(BaseModel):
    comments: list[Comment]
    model_name: str

class CommentAnalysisResult(BaseModel):
    request: Comment
    text: str
    label: str
    score: float
    sentiment: str
    total_processing_time: Optional[int] = None