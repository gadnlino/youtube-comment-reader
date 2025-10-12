"""
Classifier factory for sentiment analysis.

This module provides a factory function to get the appropriate sentiment
analysis classifier based on the specified name.
"""

from classifiers.base_comment_classifier import BaseCommentClassifier
from classifiers.tfidf_classifier import TfidfClassifier


classifiers: dict[str, BaseCommentClassifier] = {
    "tfidf": TfidfClassifier()
}


def get_classifier(classifier_name: str) -> BaseCommentClassifier:
    """
    Get a sentiment analysis classifier by name.
    
    Args:
        classifier_name: Name of the classifier to retrieve
        
    Returns:
        BaseCommentClassifier instance
        
    Raises:
        KeyError: If classifier_name is not found
    """
    return classifiers[classifier_name]
