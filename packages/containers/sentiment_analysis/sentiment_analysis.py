import datetime
from pydantic import ValidationError

from concurrent.futures import ThreadPoolExecutor
import json
import os
from models.models import Comment, CommentAnalysisRequest, CommentAnalysisResult

BATCH_SIZE = int(os.environ.get("BATCH_SIZE", 16))

# Initialize the classifier

CLASSIFIERS = None

def initialize_classifiers():
    from transformers import pipeline
    
    global CLASSIFIERS
    
    if CLASSIFIERS is not None:
        return
    
    CLASSIFIERS = {
        "cardiffnlp/twitter-xlm-roberta-base-sentiment": pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment"),
        "microsoft/deberta-v3-small": pipeline("sentiment-analysis", model="microsoft/deberta-v3-small"),
    }

initialize_classifiers()

def analyze_comments_in_batch(model: str, comments: list):
    """Analyze a batch of comments using the transformers pipeline."""
   
    classifier = CLASSIFIERS.get(model) if model and model in CLASSIFIERS else CLASSIFIERS["cardiffnlp/twitter-xlm-roberta-base-sentiment"]
    
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
                request=comment,
                text=comment.text,
                label=result["label"],
                score=result["score"],
                sentiment=result["label"]
            )
            for comment, result in zip(comments, results)
        ]
    except Exception as e:
        return [{"error": str(e), "comment": comment} for comment in comments]

def handler(body, _):
    try:
        print(f"Received event: {json.dumps(body)}")
        comment_analysis_request = None
        
        try:
            comment_analysis_request = CommentAnalysisRequest.model_validate(body)
        except ValidationError as e:
            return {"error": f"Invalid request format: {str(e)}"}, 400
        
        comments = comment_analysis_request.comments
        
        comment_count = len(comments)
        
        start_time = datetime.datetime.now().timestamp()

        # Split comments into smaller batches for processing
        batches = [comments[i:i + BATCH_SIZE] for i in range(0, len(comments), BATCH_SIZE)]
        
        # Process batches concurrently
        with ThreadPoolExecutor() as executor:
            results = executor.map(lambda x : analyze_comments_in_batch(comment_analysis_request.model_name, x), batches)
        
        
        total_time = datetime.datetime.now().timestamp() - start_time
        # Flatten the results from all batches
        flattened_results: list[CommentAnalysisResult] = []
        
        for batch in results:
            if isinstance(batch, list):
                flattened_results.extend(batch)
            else:
                flattened_results.append(batch)
                
        for item in flattened_results:
            item.total_processing_time = total_time
        
        print(f"Total processing time: {comment_count} comments in {total_time} seconds")
        
        return list(map(lambda x : x.model_dump(), flattened_results)), 200

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
    
    response = handler(custom_event, None)
    print(response)