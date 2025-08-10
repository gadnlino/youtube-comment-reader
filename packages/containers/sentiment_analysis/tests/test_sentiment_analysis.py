import sys
import os
import uuid
import pytest
from pydantic import ValidationError
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.models import Comment, CommentAnalysisRequest, CommentAnalysisResult
from classifiers.llm_classifier import LlmClassifier

# Mock data
mock_comments = [
    Comment(
        text="This is amazing!", 
        videoTitle="Great Video", 
        id=str(uuid.uuid4())
    ),
    Comment(
        text="I didn't like it.", 
        videoTitle="Bad Video", 
        id=str(uuid.uuid4())
    ),
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


class TestLlmClassifierIntegration:
    """Integration tests for LlmClassifier using the new class structure."""
    
    def test_analyze_comments_in_batch_success(self):
        """Test successful batch analysis using LlmClassifier."""
        with patch.object(LlmClassifier, '_get_classifier') as mock_get_classifier:
            # Mock the classifier
            mock_classifier = MagicMock()
            mock_classifier.return_value = mock_results
            mock_get_classifier.return_value = mock_classifier
            
            classifier = LlmClassifier()
            results = classifier._analyze_comments_in_batch(
                "cardiffnlp/twitter-xlm-roberta-base-sentiment", 
                mock_comments
            )
            
            # Assertions
            assert len(results) == 2
            assert results[0].label == "POSITIVE"
            assert results[0].score == 0.99
            assert results[1].label == "NEGATIVE"
            assert results[1].score == 0.95
    
    def test_analyze_comments_in_batch_exception(self):
        """Test batch analysis with exception handling."""
        with patch.object(LlmClassifier, '_get_classifier') as mock_get_classifier:
            # Mock the classifier to raise an exception
            mock_classifier = MagicMock()
            mock_classifier.side_effect = Exception("Test error")
            mock_get_classifier.return_value = mock_classifier
            
            classifier = LlmClassifier()
            results = classifier._analyze_comments_in_batch(
                "test-model", 
                mock_comments
            )
            
            # Verify error results
            assert len(results) == 2
            for result in results:
                assert "error" in result
                assert "Test error" in result["error"]
                assert "comment" in result
    
    def test_analyse_comments_with_valid_request(self):
        """Test comment analysis with valid request using LlmClassifier."""
        request = CommentAnalysisRequest(
            model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment",
            comments=mock_comments,
        )
        
        with patch.object(LlmClassifier, '_analyze_comments_in_batch') as mock_batch:
            mock_batch.return_value = [
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
            
            classifier = LlmClassifier()
            results = classifier.analyse_comments(request)
            
            # Assertions
            assert len(results) == 2
            assert results[0].label == "POSITIVE"
            assert results[1].label == "NEGATIVE"
            assert all(hasattr(result, 'total_processing_time') for result in results)
    
    def test_analyse_comments_with_invalid_request(self):
        """Test comment analysis with invalid request."""
        # Test with empty comments
        empty_request = CommentAnalysisRequest(
            model_name="test-model",
            comments=[],
        )
        
        classifier = LlmClassifier()
        results = classifier.analyse_comments(empty_request)
        
        assert len(results) == 0
    
    def test_model_validation_error_handling(self):
        """Test handling of model validation errors."""
        # Test with invalid request data
        invalid_request_data = {
            "model_name": "invalid-model",
            "comments": "not a list"  # This should cause validation error
        }
        
        # This should raise a ValidationError
        with pytest.raises(ValidationError):
            CommentAnalysisRequest.model_validate(invalid_request_data)
    
    def test_classifier_initialization_with_different_models(self):
        """Test classifier initialization with different model names."""
        # Test default model
        classifier1 = LlmClassifier()
        assert classifier1.model_name == "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        
        # Test custom model
        classifier2 = LlmClassifier("microsoft/deberta-v3-small")
        assert classifier2.model_name == "microsoft/deberta-v3-small"
    
    def test_comment_content_mapping(self):
        """Test comment content mapping functionality."""
        classifier = LlmClassifier()
        
        # Test with video title
        comment_with_title = Comment(
            text="Great video!",
            videoTitle="Amazing Tutorial",
            id=str(uuid.uuid4())
        )
        mapped_content = classifier._map_comment_content(comment_with_title)
        assert "VideoTitle: amazing tutorial" in mapped_content
        assert "Comment: great video!" in mapped_content
        
        # Test without video title
        comment_without_title = Comment(
            text="Great video!",
            videoTitle=None,
            id=str(uuid.uuid4())
        )
        mapped_content = classifier._map_comment_content(comment_without_title)
        assert mapped_content == "great video!"


# Mock handler function for testing the lambda pattern
def mock_handler(body, context):
    """Mock handler function that uses LlmClassifier."""
    try:
        comment_analysis_request = CommentAnalysisRequest.model_validate(body)
        classifier = LlmClassifier(comment_analysis_request.model_name)
        results = classifier.analyse_comments(comment_analysis_request)
        return [result.model_dump() for result in results], 200
    except ValidationError as e:
        return {"error": f"Invalid request format: {str(e)}"}, 400
    except Exception as e:
        return {"error": str(e)}, 500


class TestHandlerIntegration:
    """Tests for the handler function pattern."""
    
    def test_handler_with_valid_input(self):
        """Test handler with valid input."""
        with patch.object(LlmClassifier, 'analyse_comments') as mock_analyse:
            mock_analyse.return_value = [
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
            
            response, status_code = mock_handler(mock_request_body, None)
            
            # Assertions
            assert status_code == 200
            assert len(response) == 2
            assert response[0]["label"] == "POSITIVE"
            assert response[1]["label"] == "NEGATIVE"
    
    def test_handler_with_invalid_input(self):
        """Test handler with invalid input."""
        invalid_body = {"invalid": "data"}
        
        response, status_code = mock_handler(invalid_body, None)
        
        # Assertions
        assert status_code == 400
        assert "Invalid request format" in response["error"]
    
    def test_handler_with_exception(self):
        """Test handler with exception."""
        with patch.object(LlmClassifier, 'analyse_comments') as mock_analyse:
            mock_analyse.side_effect = Exception("Test error")
            
            response, status_code = mock_handler(mock_request_body, None)
            
            # Assertions
            assert status_code == 500
            assert "Test error" in response["error"]


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])