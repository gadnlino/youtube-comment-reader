import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.models import Comment, CommentAnalysisRequest, CommentAnalysisResult
from classifiers.vader_classifier import VaderClassifier

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

mock_vader_scores = [
    {"compound": 0.8, "pos": 0.6, "neg": 0.0, "neu": 0.4},  # Positive
    {"compound": -0.7, "pos": 0.0, "neg": 0.8, "neu": 0.2},  # Negative
    {"compound": 0.0, "pos": 0.2, "neg": 0.2, "neu": 0.6},   # Neutral
]

mock_request = CommentAnalysisRequest(
    model_name="vader",
    comments=mock_comments,
)

# Global patch for all tests that instantiate VaderClassifier
@pytest.fixture(autouse=True)
def patch_vader_analyzer():
    with patch('nltk.sentiment.vader.SentimentIntensityAnalyzer') as mock_analyzer, \
         patch('nltk.download') as mock_download:
        mock_analyzer_instance = MagicMock()
        # Default: always return neutral
        mock_analyzer_instance.polarity_scores.return_value = {"compound": 0.0, "pos": 0.0, "neg": 0.0, "neu": 1.0}
        mock_analyzer.return_value = mock_analyzer_instance
        yield

class TestVaderClassifier:
    """Test suite for VaderClassifier class."""
    
    def test_init_default_model(self):
        classifier = VaderClassifier()
        assert classifier.model_name == "vader"
        assert classifier._analyzer is not None
    
    def test_init_custom_model(self):
        classifier = VaderClassifier("custom-vader")
        assert classifier.model_name == "custom-vader"
        assert classifier._analyzer is not None
    
    def test_map_comment_content_with_video_title(self):
        classifier = VaderClassifier()
        comment = Comment(
            text="Great video!",
            videoTitle="Amazing Tutorial",
            id=str(uuid.uuid4())
        )
        result = classifier._map_comment_content(comment)
        expected = "VideoTitle: Amazing Tutorial Comment: Great video!"
        assert result == expected
    
    def test_map_comment_content_without_video_title(self):
        classifier = VaderClassifier()
        comment = Comment(
            text="Great video!",
            videoTitle=None,
            id=str(uuid.uuid4())
        )
        result = classifier._map_comment_content(comment)
        assert result == "Great video!"
    
    def test_map_comment_content_empty_text(self):
        classifier = VaderClassifier()
        comment = Comment(
            text="",
            videoTitle="Test Video",
            id=str(uuid.uuid4())
        )
        result = classifier._map_comment_content(comment)
        expected = "VideoTitle: Test Video Comment: "
        assert result == expected
    
    def test_analyze_single_comment_positive(self):
        classifier = VaderClassifier()
        classifier._analyzer.polarity_scores.return_value = {
            "compound": 0.8,
            "pos": 0.6,
            "neg": 0.0,
            "neu": 0.4
        }
        comment = mock_comments[0]
        result = classifier._analyze_single_comment(comment)
        assert result.label == "POSITIVE"
        assert result.sentiment == "POSITIVE"
        assert result.score == 0.8
        assert result.text == comment.text
    
    def test_analyze_single_comment_negative(self):
        classifier = VaderClassifier()
        classifier._analyzer.polarity_scores.return_value = {
            "compound": -0.7,
            "pos": 0.0,
            "neg": 0.8,
            "neu": 0.2
        }
        comment = mock_comments[1]
        result = classifier._analyze_single_comment(comment)
        assert result.label == "NEGATIVE"
        assert result.sentiment == "NEGATIVE"
        assert result.score == 0.7
        assert result.text == comment.text
    
    def test_analyze_single_comment_neutral(self):
        classifier = VaderClassifier()
        classifier._analyzer.polarity_scores.return_value = {
            "compound": 0.0,
            "pos": 0.2,
            "neg": 0.2,
            "neu": 0.6
        }
        comment = mock_comments[2]
        result = classifier._analyze_single_comment(comment)
        assert result.label == "NEUTRAL"
        assert result.sentiment == "NEUTRAL"
        assert result.score == 0.0
        assert result.text == comment.text
    
    def test_analyze_single_comment_exception(self):
        classifier = VaderClassifier()
        classifier._analyzer.polarity_scores.side_effect = Exception("Test error")
        comment = mock_comments[0]
        result = classifier._analyze_single_comment(comment)
        assert result.label == "ERROR"
        assert result.sentiment == "ERROR"
        assert result.score == 0.0
        assert result.text == comment.text
    
    def test_analyze_comments_in_batch(self):
        with patch.object(VaderClassifier, '_analyze_single_comment') as mock_single:
            mock_single.side_effect = [
                CommentAnalysisResult(
                    request=mock_comments[0],
                    text=mock_comments[0].text,
                    label="POSITIVE",
                    score=0.8,
                    sentiment="POSITIVE"
                ),
                CommentAnalysisResult(
                    request=mock_comments[1],
                    text=mock_comments[1].text,
                    label="NEGATIVE",
                    score=0.7,
                    sentiment="NEGATIVE"
                ),
            ]
            classifier = VaderClassifier()
            results = classifier._analyze_comments_in_batch(mock_comments[:2])
            assert len(results) == 2
            assert results[0].label == "POSITIVE"
            assert results[1].label == "NEGATIVE"
    
    def test_analyse_comments_single_batch(self):
        with patch.object(VaderClassifier, '_analyze_comments_in_batch') as mock_batch:
            mock_batch.return_value = [
                CommentAnalysisResult(
                    request=mock_comments[0],
                    text="This is amazing!",
                    label="POSITIVE",
                    score=0.8,
                    sentiment="POSITIVE",
                ),
                CommentAnalysisResult(
                    request=mock_comments[1],
                    text="I didn't like it.",
                    label="NEGATIVE",
                    score=0.7,
                    sentiment="NEGATIVE",
                ),
            ]
            classifier = VaderClassifier()
            results = classifier.analyse_comments(mock_request)
            assert len(results) == 2
            assert results[0].label == "POSITIVE"
            assert results[1].label == "NEGATIVE"
            assert all(hasattr(result, 'total_processing_time') for result in results)
    
    def test_analyse_comments_empty_request(self):
        empty_request = CommentAnalysisRequest(
            model_name="vader",
            comments=[],
        )
        classifier = VaderClassifier()
        results = classifier.analyse_comments(empty_request)
        assert len(results) == 0
    
    def test_analyse_comments_concurrent_processing(self):
        with patch('classifiers.vader_classifier.ThreadPoolExecutor') as mock_executor:
            mock_executor_instance = MagicMock()
            mock_executor.return_value.__enter__.return_value = mock_executor_instance
            classifier = VaderClassifier()
            classifier.analyse_comments(mock_request)
            mock_executor.assert_called_once()
            mock_executor_instance.map.assert_called_once()
    
    def test_analyse_comments_processing_time(self):
        with patch.object(VaderClassifier, '_analyze_comments_in_batch') as mock_batch:
            mock_batch.return_value = [
                CommentAnalysisResult(
                    request=mock_comments[0],
                    text="Test",
                    label="POSITIVE",
                    score=0.8,
                    sentiment="POSITIVE",
                )
            ]
            classifier = VaderClassifier()
            results = classifier.analyse_comments(mock_request)
            assert len(results) == 1
            assert results[0].total_processing_time is not None
            assert results[0].total_processing_time > 0
    
    def test_get_detailed_scores(self):
        classifier = VaderClassifier()
        classifier._analyzer.polarity_scores.return_value = {
            "compound": 0.8,
            "pos": 0.6,
            "neg": 0.0,
            "neu": 0.4
        }
        scores = classifier.get_detailed_scores("This is great!")
        assert scores["compound"] == 0.8
        assert scores["pos"] == 0.6
        assert scores["neg"] == 0.0
        assert scores["neu"] == 0.4

class TestVaderClassifierIntegration:
    """Integration tests for VaderClassifier."""
    
    def test_full_classification_flow(self):
        classifier = VaderClassifier()
        classifier._analyzer.polarity_scores.side_effect = [
            {"compound": 0.8, "pos": 0.6, "neg": 0.0, "neu": 0.4},
            {"compound": -0.7, "pos": 0.0, "neg": 0.8, "neu": 0.2},
            {"compound": 0.0, "pos": 0.2, "neg": 0.2, "neu": 0.6},
        ]
        results = classifier.analyse_comments(mock_request)
        assert len(results) == 3
        assert all(hasattr(result, 'label') for result in results)
        assert all(hasattr(result, 'score') for result in results)
        assert all(hasattr(result, 'total_processing_time') for result in results)
    
    def test_sentiment_thresholds(self):
        classifier = VaderClassifier()
        # Test positive threshold (>= 0.05)
        classifier._analyzer.polarity_scores.return_value = {"compound": 0.05}
        result = classifier._analyze_single_comment(mock_comments[0])
        assert result.label == "POSITIVE"
        # Test negative threshold (<= -0.05)
        classifier._analyzer.polarity_scores.return_value = {"compound": -0.05}
        result = classifier._analyze_single_comment(mock_comments[0])
        assert result.label == "NEGATIVE"
        # Test neutral threshold (-0.05 < compound < 0.05)
        classifier._analyzer.polarity_scores.return_value = {"compound": 0.0}
        result = classifier._analyze_single_comment(mock_comments[0])
        assert result.label == "NEUTRAL"

if __name__ == "__main__":
    pytest.main([__file__]) 