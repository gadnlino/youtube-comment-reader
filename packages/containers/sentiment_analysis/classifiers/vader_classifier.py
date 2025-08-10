import datetime
import os
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
        """Map comment content for analysis, including video title if available."""
        text = comment.text if comment.text else ""
        
        if comment.videoTitle:
            return f"VideoTitle: {comment.videoTitle} Comment: {text}"
        
        return text
    
    def _analyze_single_comment(self, comment: Comment) -> CommentAnalysisResult:
        """Analyze a single comment using VADER."""
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
                score=abs(compound_score),  # Use absolute value for confidence
                sentiment=label
            )
        except Exception as e:
            raise e
    
    def _analyze_comments_in_batch(self, comments: list) -> list[CommentAnalysisResult]:
        """Analyze a batch of comments using VADER."""
        results = []
        for comment in comments:
            result = self._analyze_single_comment(comment)
            results.append(result)
        return results
    
    def analyse_comments(self, request: CommentAnalysisRequest) -> list[CommentAnalysisResult]:
        """Analyze comments sequentially using VADER sentiment analysis."""
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
        """Get detailed VADER scores for a text."""
        if not self._analyzer:
            self._initialize_analyzer()
        
        return self._analyzer.polarity_scores(text)


if __name__ == "__main__":
    # Test the VADER classifier
    test_comments = [
        Comment(
            id="1",
            text="This is amazing!",
            videoTitle="Great Video"
        ),
        Comment(
            id="2", 
            text="I didn't like it.",
            videoTitle="Bad Video"
        ),
        Comment(
            id="3",
            text="It was okay.",
            videoTitle="Average Video"
        ),
    ]
    
    request = CommentAnalysisRequest(
        model_name="vader",
        comments=test_comments
    )
    
    classifier = VaderClassifier()
    results = classifier.analyse_comments(request)
    
    print("VADER Classification Results:")
    for result in results:
        print(f"Text: {result.text}")
        print(f"Sentiment: {result.sentiment}")
        print(f"Score: {result.score}")
        print(f"Label: {result.label}")
        print("---") 