"""
AWS Lambda handler for sentiment analysis service.

This module provides sentiment analysis functionality using VADER classifier
for YouTube comments. It replaces the Flask-based container service with
a serverless Lambda function.
"""

import json
import os
from typing import Dict, Any
from pydantic import ValidationError
from models.models import CommentAnalysisRequest
from get_classifiers import get_classifier


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for sentiment analysis requests.
    
    Args:
        event: Lambda event containing the request data
        context: Lambda context object
        
    Returns:
        Dict containing the response with sentiment analysis results
    """
    try:
        # Extract request data from Lambda event
        # Handle both direct invocation and API Gateway events
        if 'body' in event:
            # API Gateway event format
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
        else:
            # Direct Lambda invocation
            body = event

        # Validate API key if configured
        if 'headers' in event:
            api_key = event.get('headers', {}).get('x-api-key')
        else:
            api_key = None
        sentiment_analysis_api_key = os.environ.get("SENTIMENT_ANALYSIS_API_KEY")

        if sentiment_analysis_api_key and api_key != sentiment_analysis_api_key:
            return {
                'statusCode': 403,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': (
                        'Content-Type,X-Amz-Date,Authorization,'
                        'X-Api-Key,X-Amz-Security-Token'
                    ),
                    'Access-Control-Allow-Methods': 'POST,OPTIONS'
                },
                'body': json.dumps({"error": "Unauthorized"})
            }
        
        print(f"Received event: {json.dumps(body)}")
        
        # Validate request data
        try:
            comment_analysis_request = CommentAnalysisRequest.model_validate(body)
        except ValidationError as e:
            print(f"Validation error: {str(e)}")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': (
                        'Content-Type,X-Amz-Date,Authorization,'
                        'X-Api-Key,X-Amz-Security-Token'
                    ),
                    'Access-Control-Allow-Methods': 'POST,OPTIONS'
                },
                'body': json.dumps({
                    "error": f"Invalid request format: {str(e)}"
                })
            }
        
        # Initialize TF-IDF classifier (high accuracy, 66.14% vs VADER's 53.43%)
        classifier_name = 'tfidf'
        classifier = get_classifier(classifier_name)
        
        # Process the comments
        results = classifier.analyse_comments(comment_analysis_request)
        
        # Convert results to serializable format
        response_data = [result.model_dump() for result in results]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': (
                    'Content-Type,X-Amz-Date,Authorization,'
                    'X-Api-Key,X-Amz-Security-Token'
                ),
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': (
                    'Content-Type,X-Amz-Date,Authorization,'
                    'X-Api-Key,X-Amz-Security-Token'
                ),
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({"error": str(e)})
        }


def handle_cors_preflight(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle CORS preflight requests for OPTIONS method.
    
    Args:
        event: Lambda event containing the request data
        context: Lambda context object
        
    Returns:
        Dict containing the CORS preflight response
    """
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': (
                'Content-Type,X-Amz-Date,Authorization,'
                'X-Api-Key,X-Amz-Security-Token'
            ),
            'Access-Control-Allow-Methods': 'POST,OPTIONS'
        },
        'body': ''
    }
