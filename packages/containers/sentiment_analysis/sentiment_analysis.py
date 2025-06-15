import datetime
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
import json
import os

SENTIMENT_ANALYSIS_API_KEY = os.environ.get("SENTIMENT_ANALYSIS_API_KEY")

# Initialize the classifier
classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

def analyze_comments_in_batch(comments):
    """Analyze a batch of comments using the transformers pipeline."""
    try:
        texts = [comment["text"].lower() for comment in comments]
        results = classifier(texts)  # Process the batch of texts
        return [
            {
                "request": comment,
                "text": comment["text"],
                "label": result["label"],
                "score": result["score"],
                "sentiment": result["label"],
            }
            for comment, result in zip(comments, results)
        ]
    except Exception as e:
        return [{"error": str(e), "comment": comment} for comment in comments]

def lambda_handler(body, context):
    try:
        print(f"Received event: {json.dumps(body)}")
        
        comments = body.get("comments", [])
        
        comment_count = len(comments)
        
        start_time = int(datetime.datetime.now().timestamp())

        if not isinstance(comments, list) or not comments:
            return {"error": "Expected a non-empty list of 'comments'"}, 400
        
        # Split comments into smaller batches for processing
        batch_size = 16  # Adjust batch size based on your model and system resources
        batches = [comments[i:i + batch_size] for i in range(0, len(comments), batch_size)]
        
        # Process batches concurrently
        with ThreadPoolExecutor() as executor:
            results = executor.map(analyze_comments_in_batch, batches)
        
        # Flatten the results from all batches
        flattened_results = [item for batch in results for item in batch]
        
        total_time = int(datetime.datetime.now().timestamp()) - start_time
        
        print(f"Sentiment analysis results: {json.dumps(flattened_results)}")
        
        print(f"Total processing time: {comment_count} comments in {total_time} seconds")
        
        return flattened_results, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
if __name__ == "__main__":
    custom_event = {
        'comments': [
            {"text": "This is amazing!"},
            {"text": "I didn't like it."},
            {"text": "It was okay, not great."},
            {"text": "Absolutely fantastic!"},
            {"text": "Terrible experience."},
        ]
    }
    
    response = lambda_handler(custom_event, None)
    print(response)