"""
VADER sentiment analysis classifier implementation.

This module provides sentiment analysis using NLTK's VADER (Valence Aware 
Dictionary and sEntiment Reasoner) classifier, which is lightweight and
suitable for serverless environments.
"""

import datetime
from typing import Dict
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from models.models import (
    Comment, CommentAnalysisRequest, CommentAnalysisResult
)
from classifiers.base_comment_classifier import BaseCommentClassifier


class VaderClassifier(BaseCommentClassifier):
    """A sentiment analysis classifier using NLTK's VADER."""
    
    def __init__(self, model_name: str = "vader"):
        """
        Initialize the VADER classifier.
        
        Args:
            model_name: Name of the model (defaults to "vader")
        """
        super().__init__(model_name)
        self._analyzer = None
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """Initialize the VADER sentiment analyzer."""
        try:
            # Download VADER lexicon if not already downloaded
            nltk.download('vader_lexicon', quiet=True)
            self._analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Error initializing VADER analyzer: {e}")
            # Fallback to basic initialization
            self._analyzer = SentimentIntensityAnalyzer()
    
    def _map_comment_content(self, comment: Comment) -> str:
        """
        Map comment content for analysis, including video title if available.
        
        Args:
            comment: Comment object to analyze
            
        Returns:
            String containing the text to analyze
        """
        text = comment.text if comment.text else ""
        
        if comment.videoTitle:
            return f"VideoTitle: {comment.videoTitle} Comment: {text}"
        
        return text
    
    def _analyze_single_comment(self, comment: Comment) -> CommentAnalysisResult:
        """
        Analyze a single comment using VADER.
        
        Args:
            comment: Comment object to analyze
            
        Returns:
            CommentAnalysisResult with sentiment analysis results
        """
        try:
            text = self._map_comment_content(comment)
            scores = self._analyzer.polarity_scores(text)
            
            # VADER provides compound, pos, neg, neu scores
            compound_score = scores['compound']
            
            # Determine sentiment label based on compound score
            if compound_score >= 0.05:
                label = "POSITIVE"
            elif compound_score <= -0.05:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"
            
            return CommentAnalysisResult(
                request=comment,
                text=comment.text,
                label=label,
                score=abs(compound_score),  # Use absolute value
                sentiment=label
            )
        except Exception as e:
            raise e
    
    def _analyze_comments_in_batch(self, comments: list) -> list[CommentAnalysisResult]:
        """
        Analyze a batch of comments using VADER.
        
        Args:
            comments: List of Comment objects to analyze
            
        Returns:
            List of CommentAnalysisResult objects
        """
        results = []
        for comment in comments:
            result = self._analyze_single_comment(comment)
            results.append(result)
        return results
    
    def analyse_comments(self, request: CommentAnalysisRequest) -> list[CommentAnalysisResult]:
        """
        Analyze comments sequentially using VADER sentiment analysis.
        
        Args:
            request: CommentAnalysisRequest containing comments to analyze
            
        Returns:
            List of CommentAnalysisResult objects with sentiment analysis
        """
        comments = request.comments
        comment_count = len(comments)
        
        start_time = datetime.datetime.now().timestamp()
        
        # Process comments sequentially one by one
        results: list[CommentAnalysisResult] = []
        
        for comment in comments:
            result = self._analyze_single_comment(comment)
            results.append(result)
        
        total_time = datetime.datetime.now().timestamp() - start_time
        
        # Set processing time for all results
        for item in results:
            item.total_processing_time = total_time
        
        print(
            f"Sequential processing time: {comment_count} comments "
            f"in {total_time} seconds"
        )
        
        return results
    
    def get_detailed_scores(self, text: str) -> Dict[str, float]:
        """
        Get detailed VADER scores for a text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing detailed VADER scores
        """
        if not self._analyzer:
            self._initialize_analyzer()
        
        return self._analyzer.polarity_scores(text)
