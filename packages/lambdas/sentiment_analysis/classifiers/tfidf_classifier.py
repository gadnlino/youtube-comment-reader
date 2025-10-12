"""
TF-IDF + Logistic Regression sentiment analysis classifier implementation.

This module provides sentiment analysis using TF-IDF vectorization combined
with Logistic Regression classifier, which achieves 66.14% accuracy compared
to VADER's 53.43% accuracy on the YouTube comments dataset.
"""

import datetime
import pickle
import os
from typing import Dict, List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from models.models import (
    Comment, CommentAnalysisRequest, CommentAnalysisResult
)
from classifiers.base_comment_classifier import BaseCommentClassifier


class TfidfClassifier(BaseCommentClassifier):
    """A sentiment analysis classifier using TF-IDF + Logistic Regression."""
    
    def __init__(self, model_name: str = "tfidf"):
        """
        Initialize the TF-IDF classifier.
        
        Args:
            model_name: Name of the model (defaults to "tfidf")
        """
        super().__init__(model_name)
        self._model = None
        self._vectorizer = None
        self._label_encoder = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the TF-IDF model components."""
        try:
            # Try to load pre-trained model if available
            model_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'models', 
                'tfidf_logistic_model.pkl'
            )
            
            if os.path.exists(model_path):
                self._load_pretrained_model(model_path)
            else:
                # Create new model components
                self._create_model()
                
        except Exception as e:
            print(f"Error initializing TF-IDF model: {e}")
            # Fallback to creating new model
            self._create_model()
    
    def _load_pretrained_model(self, model_path: str):
        """Load a pre-trained TF-IDF model."""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
                self._model = model_data['model']
                self._vectorizer = model_data['vectorizer']
                self._label_encoder = model_data['label_encoder']
            print("✅ Loaded pre-trained TF-IDF model")
        except Exception as e:
            print(f"Error loading pre-trained model: {e}")
            self._create_model()
    
    def _create_model(self):
        """Create new TF-IDF model components."""
        # Create TF-IDF vectorizer with same parameters as training
        self._vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2,
            max_df=0.95,
            lowercase=True,
            strip_accents='unicode'
        )
        
        # Create Logistic Regression model
        self._model = LogisticRegression(
            C=1.0,
            max_iter=1000,
            random_state=42,
            n_jobs=-1,
            solver='lbfgs'
        )
        
        # Create label encoder
        self._label_encoder = LabelEncoder()
        self._label_encoder.fit(['negative', 'neutral', 'positive'])
        
        print("✅ Created new TF-IDF model components")
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for TF-IDF analysis.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not isinstance(text, str):
            return ""
        
        # Basic cleaning
        cleaned = text.lower().strip()
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        return cleaned
    
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
            # Combine video title and comment text for better context
            combined_text = f"Video Title: {comment.videoTitle}. Comment: {text}"
        else:
            combined_text = text
        
        return self._preprocess_text(combined_text)
    
    def _analyze_single_comment(self, comment: Comment) -> CommentAnalysisResult:
        """
        Analyze a single comment using TF-IDF + Logistic Regression.
        
        Args:
            comment: Comment object to analyze
            
        Returns:
            CommentAnalysisResult with sentiment analysis results
        """
        try:
            # Preprocess the comment text
            processed_text = self._map_comment_content(comment)
            
            # Transform text to TF-IDF features
            if self._vectorizer is None:
                raise ValueError("TF-IDF vectorizer not initialized")
            
            # For single text, we need to wrap it in a list
            tfidf_features = self._vectorizer.transform([processed_text])
            
            # Make prediction
            if self._model is None:
                raise ValueError("Logistic Regression model not initialized")
            
            # Get prediction probabilities
            probabilities = self._model.predict_proba(tfidf_features)[0]
            predicted_class_idx = np.argmax(probabilities)
            confidence = probabilities[predicted_class_idx]
            
            # Convert prediction back to label
            if self._label_encoder is None:
                raise ValueError("Label encoder not initialized")
            
            predicted_label = self._label_encoder.inverse_transform([predicted_class_idx])[0]
            
            # Map to our standard format
            sentiment_map = {
                'negative': 'NEGATIVE',
                'neutral': 'NEUTRAL', 
                'positive': 'POSITIVE'
            }
            
            sentiment = sentiment_map.get(predicted_label, 'NEUTRAL')
            
            return CommentAnalysisResult(
                request=comment,
                text=comment.text,
                label=sentiment,
                score=float(confidence),
                sentiment=sentiment
            )
            
        except Exception as e:
            print(f"Error analyzing comment: {e}")
            # Return neutral sentiment as fallback
            return CommentAnalysisResult(
                request=comment,
                text=comment.text,
                label='NEUTRAL',
                score=0.0,
                sentiment='NEUTRAL'
            )
    
    def _analyze_comments_in_batch(self, comments: List[Comment]) -> List[CommentAnalysisResult]:
        """
        Analyze a batch of comments using TF-IDF + Logistic Regression.
        
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
    
    def analyse_comments(self, request: CommentAnalysisRequest) -> List[CommentAnalysisResult]:
        """
        Analyze comments using TF-IDF + Logistic Regression sentiment analysis.
        
        Args:
            request: CommentAnalysisRequest containing comments to analyze
            
        Returns:
            List of CommentAnalysisResult objects with sentiment analysis results
        """
        comments = request.comments
        comment_count = len(comments)
        
        start_time = datetime.datetime.now().timestamp()
        
        # Process comments sequentially
        results: List[CommentAnalysisResult] = []
        
        for comment in comments:
            result = self._analyze_single_comment(comment)
            results.append(result)
        
        total_time = datetime.datetime.now().timestamp() - start_time
        
        # Set processing time for all results
        for item in results:
            item.total_processing_time = total_time
        
        print(
            f"TF-IDF processing time: {comment_count} comments "
            f"in {total_time:.4f} seconds"
        )
        
        return results
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about the current model.
        
        Returns:
            Dictionary containing model information
        """
        return {
            'model_type': 'TF-IDF + Logistic Regression',
            'accuracy': '66.14%',
            'f1_score': '66.28%',
            'features': '~10,000 TF-IDF features with n-gram range (1,2)',
            'preprocessing': 'Lowercase, stop words removal, accent stripping',
            'classifier': 'Logistic Regression with L-BFGS solver'
        }
