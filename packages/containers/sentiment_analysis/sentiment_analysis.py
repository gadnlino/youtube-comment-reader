##references: https://github.com/mgsudhanva/sentiment-service/blob/main/lambda/sentiment-service/Dockerfile
##            https://medium.com/@mgsudhanva/deploying-hugging-face-transformers-model-on-aws-lambda-with-docker-containers-84c6f4483f2a

import json
import os
from transformers import pipeline
import constants

SENTIMENT_ANALYSIS_API_KEY = os.environ.get("SENTIMENT_ANALYSIS_API_KEY")

classifier = pipeline("sentiment-analysis", model=constants.DEST_PATH)

def lambda_handler(body, context):
    try:
        print(f"Received event: {json.dumps(body)}")
        
        comments = body.get("comments", [])

        if not isinstance(comments, list) or not comments:
            return {"error": "Expected a non-empty list of 'comments'"}, 400
        
        results = classifier(list(map(lambda x: x['text'].lower(), comments)))

        output = []
        for request, result in zip(comments, results):
            output.append({
                'request': request,
                "text": request["text"],
                "label": result["label"],
                "score": result["score"],
                "sentiment": result["label"],
            })
        
        print(f"Sentiment analysis results: {json.dumps(output)}")
        
        return output, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
if(__name__ == "__main__"):
    custom_event = {
            'comments': ["abcde test comment"]
        }
    
    lambda_handler(custom_event, None)