from flask import Flask, request, jsonify
import sentiment_analysis  # Import your existing Lambda logic
import os

app = Flask(__name__)

SENTIMENT_ANALYSIS_API_KEY = os.environ.get("SENTIMENT_ANALYSIS_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "Application is running"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the input data from the request
        data = request.json
        
        api_key = request.headers.get("x-api-key")
        
        #if not SENTIMENT_ANALYSIS_API_KEY or api_key != SENTIMENT_ANALYSIS_API_KEY:
        if SENTIMENT_ANALYSIS_API_KEY and api_key != SENTIMENT_ANALYSIS_API_KEY:
            return {"error": "Unauthorized"}, 403

        # Process the comments using your existing logic
        result, status_code = sentiment_analysis.handler(request.json, None)

        # Return the results as a JSON response
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)