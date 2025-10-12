"""
Pydantic models for sentiment analysis requests and responses.

This module defines the data structures used for sentiment analysis
requests and responses in the Lambda function.
"""

from typing import Optional
from pydantic import BaseModel


class Comment(BaseModel):
    """Represents a single comment to be analyzed."""
    id: str
    text: str
    videoTitle: Optional[str] = None


class CommentAnalysisRequest(BaseModel):
    """Request model for sentiment analysis containing comments to analyze."""
    comments: list[Comment]
    model_name: Optional[str] = None


class CommentAnalysisResult(BaseModel):
    """Result model containing sentiment analysis results for a comment."""
    request: Optional[Comment]
    text: Optional[str]
    label: Optional[str]
    score: Optional[float]
    sentiment: Optional[str]
    total_processing_time: Optional[float] = None
