import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import uuid

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
    Comment(
        text="It was okay.", 
        videoTitle="Average Video", 
        id=str(uuid.uuid4())
    ),
]

mock_results = [
    {"label": "POSITIVE", "score": 0.99},
    {"label": "NEGATIVE", "score": 0.95},
    {"label": "NEUTRAL", "score": 0.70},
]

mock_request = CommentAnalysisRequest(
    model_name="cardiffnlp/twitter-xlm-roberta-base-sentiment",
    comments=mock_comments,
)


class TestLlmClassifier:
    """Test suite for LlmClassifier class."""
    
    def test_init_default_model(self):
        """Test initialization with default model."""
        classifier = LlmClassifier()
        assert classifier.model_name == "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        assert classifier._classifiers is not None
    
    def test_init_custom_model(self):
        """Test initialization with custom model."""
        classifier = LlmClassifier("microsoft/deberta-v3-small")
        assert classifier.model_name == "microsoft/deberta-v3-small"
        assert classifier._classifiers is not None
    
    @patch('transformers.pipeline')
    def test_initialize_classifiers(self, mock_pipeline):
        """Test classifier initialization."""
        mock_pipeline.return_value = MagicMock()
        
        # Create classifier to trigger initialization
        LlmClassifier()
        
        # Verify pipeline was called for both models
        assert mock_pipeline.call_count == 2
        calls = mock_pipeline.call_args_list
        default_model = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        microsoft_model = "microsoft/deberta-v3-small"
        assert any(default_model in str(call) for call in calls)
        assert any(microsoft_model in str(call) for call in calls)
    
    def test_get_classifier_existing_model(self):
        """Test getting an existing classifier."""
        classifier = LlmClassifier("microsoft/deberta-v3-small")
        result = classifier._get_classifier("microsoft/deberta-v3-small")
        assert result is not None
    
    def test_get_classifier_nonexistent_model(self):
        """Test getting a classifier for a non-existent model."""
        classifier = LlmClassifier()
        result = classifier._get_classifier("nonexistent-model")
        # Should return default model classifier
        assert result is not None
    
    def test_get_classifier_none_model(self):
        """Test getting a classifier with None model name."""
        classifier = LlmClassifier()
        result = classifier._get_classifier(None)
        # Should return default model classifier
        assert result is not None
    
    def test_map_comment_content_with_video_title(self):
        """Test comment content mapping with video title."""
        classifier = LlmClassifier()
        comment = Comment(
            text="Great video!",
            videoTitle="Amazing Tutorial",
            id=str(uuid.uuid4())
        )
        
        result = classifier._map_comment_content(comment)
        expected = "VideoTitle: amazing tutorial Comment: great video!"
        assert result == expected
    
    def test_map_comment_content_without_video_title(self):
        """Test comment content mapping without video title."""
        classifier = LlmClassifier()
        comment = Comment(
            text="Great video!",
            videoTitle=None,
            id=str(uuid.uuid4())
        )
        
        result = classifier._map_comment_content(comment)
        assert result == "great video!"
    
    def test_map_comment_content_empty_text(self):
        """Test comment content mapping with empty text."""
        classifier = LlmClassifier()
        comment = Comment(
            text="",
            videoTitle="Test Video",
            id=str(uuid.uuid4())
        )
        
        result = classifier._map_comment_content(comment)
        expected = "VideoTitle: test video Comment: "
        assert result == expected
    
    @patch.object(LlmClassifier, '_get_classifier')
    def test_analyze_comments_in_batch_success(self, mock_get_classifier):
        """Test successful batch analysis."""
        # Mock the classifier
        mock_classifier = MagicMock()
        mock_classifier.return_value = mock_results
        mock_get_classifier.return_value = mock_classifier
        
        classifier = LlmClassifier()
        results = classifier._analyze_comments_in_batch("test-model", mock_comments)
        
        # Verify results
        assert len(results) == 3
        assert results[0].label == "POSITIVE"
        assert results[0].score == 0.99
        assert results[0].sentiment == "POSITIVE"
        assert results[1].label == "NEGATIVE"
        assert results[1].score == 0.95
        assert results[2].label == "NEUTRAL"
        assert results[2].score == 0.70
        
        # Verify classifier was called with mapped texts
        mock_classifier.assert_called_once()
        call_args = mock_classifier.call_args[0][0]
        assert len(call_args) == 3
        assert "amazing" in call_args[0].lower()
        assert "didn't like" in call_args[1].lower()
        assert "okay" in call_args[2].lower()
    
    @patch.object(LlmClassifier, '_get_classifier')
    def test_analyze_comments_in_batch_exception(self, mock_get_classifier):
        """Test batch analysis with exception handling."""
        # Mock the classifier to raise an exception
        mock_classifier = MagicMock()
        mock_classifier.side_effect = Exception("Test error")
        mock_get_classifier.return_value = mock_classifier
        
        classifier = LlmClassifier()
        results = classifier._analyze_comments_in_batch("test-model", mock_comments)
        
        # Verify error results
        assert len(results) == 3
        for result in results:
            assert "error" in result
            assert "Test error" in result["error"]
            assert "comment" in result
    
    def test_analyse_comments_single_batch(self):
        """Test comment analysis with single batch."""
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
            results = classifier.analyse_comments(mock_request)
            
            # Verify results
            assert len(results) == 2
            assert results[0].label == "POSITIVE"
            assert results[1].label == "NEGATIVE"
            assert all(hasattr(result, 'total_processing_time') for result in results)
    
    def test_analyse_comments_multiple_batches(self):
        """Test comment analysis with multiple batches."""
        # Create more comments to trigger multiple batches
        many_comments = mock_comments * 10  # 30 comments total
        request = CommentAnalysisRequest(
            model_name="test-model",
            comments=many_comments,
        )
        
        with patch.object(LlmClassifier, '_analyze_comments_in_batch') as mock_batch:
            # Mock batch results - each batch returns 3 results
            mock_batch.return_value = [
                CommentAnalysisResult(
                    request=comment,
                    text=comment.text,
                    label="POSITIVE",
                    score=0.99,
                    sentiment="POSITIVE",
                )
                for comment in mock_comments  # Return 3 results per batch
            ]
            
            classifier = LlmClassifier()
            results = classifier.analyse_comments(request)
            
            # Verify results - should be 6 total (2 batches * 3 results each)
            assert len(results) == 6
            assert all(result.label == "POSITIVE" for result in results)
            assert all(hasattr(result, 'total_processing_time') for result in results)
    
    def test_analyse_comments_empty_request(self):
        """Test comment analysis with empty request."""
        empty_request = CommentAnalysisRequest(
            model_name="test-model",
            comments=[],
        )
        
        classifier = LlmClassifier()
        results = classifier.analyse_comments(empty_request)
        
        assert len(results) == 0
    
    @patch('classifiers.llm_classifier.ThreadPoolExecutor')
    def test_analyse_comments_concurrent_processing(self, mock_executor):
        """Test that concurrent processing is used."""
        mock_executor_instance = MagicMock()
        mock_executor.return_value.__enter__.return_value = mock_executor_instance
        
        classifier = LlmClassifier()
        classifier.analyse_comments(mock_request)
        
        # Verify ThreadPoolExecutor was used
        mock_executor.assert_called_once()
        mock_executor_instance.map.assert_called_once()
    
    def test_analyse_comments_processing_time(self):
        """Test that processing time is recorded."""
        with patch.object(LlmClassifier, '_analyze_comments_in_batch') as mock_batch:
            mock_batch.return_value = [
                CommentAnalysisResult(
                    request=mock_comments[0],
                    text="Test",
                    label="POSITIVE",
                    score=0.99,
                    sentiment="POSITIVE",
                )
            ]
            
            classifier = LlmClassifier()
            results = classifier.analyse_comments(mock_request)
            
            # Verify processing time is set
            assert len(results) == 1
            assert results[0].total_processing_time is not None
            assert results[0].total_processing_time > 0


class TestLlmClassifierIntegration:
    """Integration tests for LlmClassifier."""
    
    @patch('transformers.pipeline')
    def test_full_classification_flow(self, mock_pipeline):
        """Test the complete classification flow."""
        # Mock the pipeline
        mock_classifier = MagicMock()
        mock_classifier.return_value = mock_results
        mock_pipeline.return_value = mock_classifier
        
        classifier = LlmClassifier()
        results = classifier.analyse_comments(mock_request)
        
        # Verify the complete flow works
        assert len(results) == 3
        assert all(hasattr(result, 'label') for result in results)
        assert all(hasattr(result, 'score') for result in results)
        assert all(hasattr(result, 'total_processing_time') for result in results)
    
    def test_model_name_persistence(self):
        """Test that model name is correctly stored and used."""
        custom_model = "microsoft/deberta-v3-small"
        classifier = LlmClassifier(custom_model)
        
        assert classifier.model_name == custom_model
        
        # Test that the model name is used in analysis
        with patch.object(classifier, '_analyze_comments_in_batch') as mock_batch:
            mock_batch.return_value = []
            classifier.analyse_comments(mock_request)
            
            # Verify the correct model name was passed
            mock_batch.assert_called_once()
            call_args = mock_batch.call_args
            assert call_args[0][0] == mock_request.model_name


if __name__ == "__main__":
    pytest.main([__file__]) 