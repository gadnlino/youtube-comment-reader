import json
import os
from transformers import pipeline

# Modelo multilingue que funciona com portugues
classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

EXPECTED_KEY = os.environ.get("EXPECTED_KEY")

def lambda_handler(event, context):
    try:
        # headers = event.get("headers", {})
        # api_key = headers.get("x-api-key")

        # if EXPECTED_KEY and api_key != EXPECTED_KEY:
        #     return _response(403, {"error": "Unauthorized"})

        # Suporte tanto a chamada remota quanto teste local
        body = json.loads(event.get("body", "{}"))
        comments = body.get("comments", [])

        if not isinstance(comments, list) or not comments:
            return _response(400, {"error": "Expected a non-empty list of 'comments'"})

        results = classifier(comments)

        def classify(label):
            if "1" in label or "2" in label:
                return "negative"
            elif "4" in label or "5" in label:
                return "positive"
            return "neutral"

        output = []
        for text, result in zip(comments, results):
            output.append({
                "text": text,
                "label": result["label"],
                "score": result["score"],
                "sentiment": classify(result["label"]),
            })

        return _response(200, {"results": output})

    except Exception as e:
        return _response(500, {"error": str(e)})

def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps(body)
    }
    
if(__name__ == "__main__"):
    custom_event = {
        'body': {
            'comments': ["abcde test comment"]
        }
    }
    
    lambda_handler(custom_event, None)