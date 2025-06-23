import datetime
from pydantic import ValidationError
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
import json
import os
from packages.containers.sentiment_analysis.models.models import Comment, CommentAnalysisRequest, CommentAnalysisResult

SENTIMENT_ANALYSIS_API_KEY = os.environ.get("SENTIMENT_ANALYSIS_API_KEY")
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", 16))

# Initialize the classifier
CLASSIFIERS = {
    "cardiffnlp/twitter-xlm-roberta-base-sentiment": pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment"),
    "microsoft/deberta-v3-small": pipeline("sentiment-analysis", model="microsoft/deberta-v3-small"),
}
# classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

def analyze_comments_in_batch(model: str, comments: list[Comment]):
    """Analyze a batch of comments using the transformers pipeline."""
    classifier = CLASSIFIERS.get(model) if model else CLASSIFIERS["cardiffnlp/twitter-xlm-roberta-base-sentiment"]
    
    def map_comment_content(comment: Comment):
        text = comment.text.lower() if comment.text else ""
        
        if comment.videoTitle:
            return f"VideoTitle: {comment.videoTitle.lower()} Comment: {text}"
        
        return text
    
    try:
        texts = [map_comment_content(comment) for comment in comments]
        results = classifier(texts)  # Process the batch of texts
        return [
            CommentAnalysisResult(
            **{
                "request": comment,
                "text": comment["text"],
                "label": result["label"],
                "score": result["score"],
                "sentiment": result["label"],
            })
            for comment, result in zip(comments, results)
        ]
    except Exception as e:
        return [{"error": str(e), "comment": comment} for comment in comments]

def lambda_handler(body, _):
    try:
        print(f"Received event: {json.dumps(body)}")
        comment_analysis_request = None
        
        try:
            comment_analysis_request = CommentAnalysisRequest.model_validate(body)
        except ValidationError as e:
            return {"error": f"Invalid request format: {str(e)}"}, 400
        
        comments = comment_analysis_request.comments
        
        comment_count = len(comments)
        
        start_time = int(datetime.datetime.now().timestamp())

        # Split comments into smaller batches for processing
        batches = [comments[i:i + BATCH_SIZE] for i in range(0, len(comments), BATCH_SIZE)]
        
        # Process batches concurrently
        with ThreadPoolExecutor() as executor:
            results = executor.map(analyze_comments_in_batch, batches)
        
        
        total_time = int(datetime.datetime.now().timestamp()) - start_time
        # Flatten the results from all batches
        flattened_results = [CommentAnalysisResult(**item.model_dump(), total_processing_time=total_time) for batch in results for item in batch]
        
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