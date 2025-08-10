from typing import Optional
from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    text: str
    videoTitle: Optional[str]


class CommentAnalysisRequest(BaseModel):
    comments: list[Comment]
    model_name: Optional[str]


class CommentAnalysisResult(BaseModel):
    request: Optional[Comment]
    text: Optional[str]
    label: Optional[str]
    score: Optional[float]
    sentiment: Optional[str]
    total_processing_time: Optional[float] = None