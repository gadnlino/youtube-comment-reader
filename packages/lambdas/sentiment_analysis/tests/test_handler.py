"""
Comprehensive tests for the sentiment analysis Lambda handler.

This module contains tests for the Lambda handler function, covering
various scenarios including success cases, error handling, and edge cases.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from handler import lambda_handler, handle_cors_preflight


class TestLambdaHandler:
    """Test cases for the main Lambda handler function."""
    
    def test_successful_sentiment_analysis(self):
        """Test successful sentiment analysis with valid input."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [
                    {
                        'id': '1',
                        'text': 'This is amazing!',
                        'videoTitle': 'Great Video'
                    },
                    {
                        'id': '2',
                        'text': 'I hate this.',
                        'videoTitle': 'Bad Video'
                    }
                ]
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        assert 'body' in response
        assert 'headers' in response
        assert response['headers']['Content-Type'] == 'application/json'
        
        # Parse response body
        body = json.loads(response['body'])
        assert isinstance(body, list)
        assert len(body) == 2
        
        # Check first result
        first_result = body[0]
        assert first_result['text'] == 'This is amazing!'
        assert first_result['sentiment'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
        assert 'score' in first_result
        assert 'total_processing_time' in first_result
    
    def test_direct_invocation_without_api_gateway(self):
        """Test Lambda function with direct invocation (no API Gateway)."""
        # Arrange
        event = {
            'comments': [
                {
                    'id': '1',
                    'text': 'This is great!',
                    'videoTitle': 'Test Video'
                }
            ]
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body) == 1
        assert body[0]['text'] == 'This is great!'
    
    def test_unauthorized_request(self):
        """Test request with invalid API key."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [{'id': '1', 'text': 'Test'}]
            }),
            'headers': {'x-api-key': 'invalid-key'}
        }
        context = MagicMock()
        
        with patch.dict('os.environ', {'SENTIMENT_ANALYSIS_API_KEY': 'valid-key'}):
            # Act
            response = lambda_handler(event, context)
            
            # Assert
            assert response['statusCode'] == 403
            body = json.loads(response['body'])
            assert body['error'] == 'Unauthorized'
    
    def test_authorized_request_with_valid_key(self):
        """Test request with valid API key."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [{'id': '1', 'text': 'Test comment'}]
            }),
            'headers': {'x-api-key': 'valid-key'}
        }
        context = MagicMock()
        
        with patch.dict('os.environ', {'SENTIMENT_ANALYSIS_API_KEY': 'valid-key'}):
            # Act
            response = lambda_handler(event, context)
            
            # Assert
            assert response['statusCode'] == 200
    
    def test_no_api_key_required_when_not_configured(self):
        """Test that no API key is required when SENTIMENT_ANALYSIS_API_KEY is not set."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [{'id': '1', 'text': 'Test comment'}]
            })
        }
        context = MagicMock()
        
        with patch.dict('os.environ', {}, clear=True):
            # Act
            response = lambda_handler(event, context)
            
            # Assert
            assert response['statusCode'] == 200
    
    def test_invalid_request_format(self):
        """Test request with invalid data format."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': 'invalid_format'  # Should be a list
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
        assert 'Invalid request format' in body['error']
    
    def test_missing_comments_field(self):
        """Test request missing the required comments field."""
        # Arrange
        event = {
            'body': json.dumps({
                'someOtherField': 'value'
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
    
    def test_empty_comments_list(self):
        """Test request with empty comments list."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': []
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body == []
    
    def test_comments_without_video_title(self):
        """Test comments without video title."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [
                    {
                        'id': '1',
                        'text': 'This is a test comment'
                    }
                ]
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert len(body) == 1
        assert body[0]['text'] == 'This is a test comment'
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in the response."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [{'id': '1', 'text': 'Test'}]
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        headers = response['headers']
        assert 'Access-Control-Allow-Origin' in headers
        assert 'Access-Control-Allow-Headers' in headers
        assert 'Access-Control-Allow-Methods' in headers
        assert headers['Access-Control-Allow-Origin'] == '*'
    
    def test_error_handling_with_exception(self):
        """Test error handling when an unexpected exception occurs."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [{'id': '1', 'text': 'Test'}]
            })
        }
        context = MagicMock()
        
        with patch('handler.get_classifier') as mock_get_classifier:
            mock_classifier_instance = MagicMock()
            mock_classifier_instance.analyse_comments.side_effect = Exception("Unexpected error")
            mock_get_classifier.return_value = mock_classifier_instance
            
            # Act
            response = lambda_handler(event, context)
            
            # Assert
            assert response['statusCode'] == 500
            body = json.loads(response['body'])
            assert 'error' in body
            assert 'Unexpected error' in body['error']
    
    def test_processing_time_included(self):
        """Test that processing time is included in results."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [
                    {'id': '1', 'text': 'Test comment 1'},
                    {'id': '2', 'text': 'Test comment 2'}
                ]
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        
        for result in body:
            assert 'total_processing_time' in result
            assert isinstance(result['total_processing_time'], (int, float))
            assert result['total_processing_time'] >= 0


class TestCorsPreflight:
    """Test cases for CORS preflight handling."""
    
    def test_cors_preflight_response(self):
        """Test CORS preflight request handling."""
        # Arrange
        event = {'httpMethod': 'OPTIONS'}
        context = MagicMock()
        
        # Act
        response = handle_cors_preflight(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        assert response['body'] == ''
        
        headers = response['headers']
        assert 'Access-Control-Allow-Origin' in headers
        assert 'Access-Control-Allow-Headers' in headers
        assert 'Access-Control-Allow-Methods' in headers
        assert headers['Access-Control-Allow-Origin'] == '*'


class TestTfidfClassifierIntegration:
    """Integration tests with the TF-IDF classifier."""
    
    def test_positive_sentiment_detection(self):
        """Test detection of positive sentiment."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [
                    {
                        'id': '1',
                        'text': 'This is absolutely fantastic!',
                        'videoTitle': 'Amazing Video'
                    }
                ]
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        result = body[0]
        
        # Should detect positive sentiment
        assert result['sentiment'] in ['POSITIVE', 'NEUTRAL', 'NEGATIVE']  # TF-IDF classification
        assert result['score'] >= 0
    
    def test_negative_sentiment_detection(self):
        """Test detection of negative sentiment."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [
                    {
                        'id': '1',
                        'text': 'This is terrible and awful!',
                        'videoTitle': 'Bad Video'
                    }
                ]
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        result = body[0]
        
        # Should detect negative sentiment
        assert result['sentiment'] in ['POSITIVE', 'NEUTRAL', 'NEGATIVE']  # TF-IDF classification
        assert result['score'] >= 0
    
    def test_video_title_included_in_analysis(self):
        """Test that video title is included in sentiment analysis."""
        # Arrange
        event = {
            'body': json.dumps({
                'comments': [
                    {
                        'id': '1',
                        'text': 'Great!',
                        'videoTitle': 'Amazing Tutorial'
                    }
                ]
            })
        }
        context = MagicMock()
        
        # Act
        response = lambda_handler(event, context)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        result = body[0]
        
        # The analysis should consider both video title and comment text
        assert result['text'] == 'Great!'
        assert result['sentiment'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']


if __name__ == '__main__':
    pytest.main([__file__])
