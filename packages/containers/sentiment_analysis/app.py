import json
from flask import Flask, request, jsonify
from pydantic import ValidationError
from models.models import CommentAnalysisRequest
import os
from get_classifiers import get_classifier

app = Flask(__name__)

SENTIMENT_ANALYSIS_API_KEY = os.environ.get("SENTIMENT_ANALYSIS_API_KEY")


@app.route('/', methods=['GET'])
def home():
    print("Application is running")
    return "Application is running"


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the input data from the request
        data = request.json
        
        api_key = request.headers.get("x-api-key")
        
        if SENTIMENT_ANALYSIS_API_KEY and api_key != SENTIMENT_ANALYSIS_API_KEY:
            return {"error": "Unauthorized"}, 403
        
        print(f"Received event: {json.dumps(data)}")
        comment_analysis_request = None
        
        try:
            comment_analysis_request = CommentAnalysisRequest.model_validate(data)
        except ValidationError as e:
            print(f"Validation error: {str(e)}")
            return {"error": f"Invalid request format: {str(e)}"}, 400
        
        classifier_name = 'vader'
        
        classifier = get_classifier(classifier_name)

        # Process the comments using your existing logic
        result = classifier.analyse_comments(comment_analysis_request)

        # Return the results as a JSON response
        return jsonify([r.model_dump() for r in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
