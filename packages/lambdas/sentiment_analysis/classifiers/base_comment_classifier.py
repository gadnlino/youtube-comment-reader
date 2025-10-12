"""
Base class for comment sentiment analysis classifiers.

This module provides the abstract base class that all sentiment analysis
classifiers must implement.
"""

from abc import ABC, abstractmethod
from models.models import CommentAnalysisRequest, CommentAnalysisResult


class BaseCommentClassifier(ABC):
    """Abstract base class for sentiment analysis classifiers."""
    
    def __init__(self, model_name: str):
        """
        Initialize the classifier with a model name.
        
        Args:
            model_name: Name of the model to use for classification
        """
        self.model_name = model_name
    
    @abstractmethod
    def analyse_comments(self, request: CommentAnalysisRequest) -> list[CommentAnalysisResult]:
        """
        Analyze a list of comments and return sentiment analysis results.
        
        Args:
            request: CommentAnalysisRequest containing comments to analyze
            
        Returns:
            List of CommentAnalysisResult objects with sentiment analysis results
        """
        pass
