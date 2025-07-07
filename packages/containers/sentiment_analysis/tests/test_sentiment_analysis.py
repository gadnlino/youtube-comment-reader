from pydantic import ValidationError
import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment_analysis import analyze_comments_in_batch, handler
from models.models import Comment, CommentAnalysisRequest, CommentAnalysisResult

# Mock data
mock_comments = [
    Comment(text="This is amazing!", videoTitle="Great Video", id=str(uuid.uuid4())),
    Comment(text="I didn't like it.", videoTitle="Bad Video", id=str(uuid.uuid4())),
]

mock_results = [
    {"label": "POSITIVE", "score": 0.99},
    {"label": "NEGATIVE", "score": 0.95},
]

mock_request_body = {
    "model_name": "cardiffnlp/twitter-xlm-roberta-base-sentiment",
    "comments": [
        {"text": "This is amazing!", "videoTitle": "Great Video", "id": str(uuid.uuid4())},
        {"text": "I didn't like it.", "videoTitle": "Bad Video", "id": str(uuid.uuid4())},
    ],
}

# Test analyze_comments_in_batch
@patch("sentiment_analysis.CLASSIFIERS")
def test_analyze_comments_in_batch(mock_classifiers):
    # Mock the classifier
    mock_classifier = MagicMock()
    mock_classifier.return_value = mock_results
    mock_classifiers.get.return_value = mock_classifier

    # Call the function
    results = analyze_comments_in_batch("cardiffnlp/twitter-xlm-roberta-base-sentiment", mock_comments)

    # Assertions
    assert len(results) == 2
    assert results[0].label == "POSITIVE"
    assert results[0].score == 0.99
    assert results[1].label == "NEGATIVE"
    assert results[1].score == 0.95

# Test lambda_handler with valid input
@patch("sentiment_analysis.analyze_comments_in_batch")
@patch("models.models.CommentAnalysisRequest.model_validate")
def test_lambda_handler_valid(mock_model_validate, mock_analyze_comments_in_batch):
    # Mock the model validation
    mock_model_validate.return_value = CommentAnalysisRequest(
        model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment",
        comments=mock_comments,
    )

    # Mock the batch analysis
    mock_analyze_comments_in_batch.return_value = [
        CommentAnalysisResult(
            request=mock_comments[0],
            text="This is amazing!",
            label="POSITIVE",
            score=0.99,
            sentiment="POSITIVE",
        ),
        CommentAnalysisResult(
            request=mock_comments[1],
            text="I didn't like it.",
            label="NEGATIVE",
            score=0.95,
            sentiment="NEGATIVE",
        ),
    ]

    # Call the lambda_handler
    response, status_code = handler(mock_request_body, None)

    # Assertions
    assert status_code == 200
    assert len(response) == 2
    assert response[0].label == "POSITIVE"
    assert response[1].label == "NEGATIVE"

# Test lambda_handler with invalid input
@patch("models.models.CommentAnalysisRequest.model_validate")
def test_lambda_handler_invalid(mock_model_validate):
    # Mock the model validation to raise a ValidationError
    mock_model_validate.side_effect = ValidationError("Invalid request format")

    # Call the lambda_handler
    response, status_code = handler({}, None)

    # Assertions
    assert status_code == 400
    assert "Invalid request format" in response["error"]