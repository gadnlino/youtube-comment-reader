import datetime
from concurrent.futures import ThreadPoolExecutor
import os
from models.models import Comment, CommentAnalysisRequest, CommentAnalysisResult
from classifiers.base_comment_classifier import BaseCommentClassifier

BATCH_SIZE = int(os.environ.get("BATCH_SIZE", 16))


class LlmClassifier(BaseCommentClassifier):
    """A sentiment analysis classifier using transformers pipeline."""
    
    def __init__(
        self, 
        model_name: str = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    ):
        super().__init__(model_name)
        self._classifiers = None
        self._initialize_classifiers()
    
    def _initialize_classifiers(self):
        """Initialize the transformers pipeline classifiers."""
        from transformers import pipeline
        
        if self._classifiers is not None:
            return
        
        default_model = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        self._classifiers = {
            default_model: pipeline(
                "sentiment-analysis", 
                model=default_model
            ),
            "microsoft/deberta-v3-small": pipeline(
                "sentiment-analysis", 
                model="microsoft/deberta-v3-small"
            ),
        }
    
    def _get_classifier(self, model_name: str):
        """Get the appropriate classifier for the given model name."""
        if model_name and model_name in self._classifiers:
            return self._classifiers[model_name]
        default_model = (
            "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        )
        return self._classifiers[default_model]
    
    def _map_comment_content(self, comment: Comment) -> str:
        """Map comment content for analysis, including video title if available."""
        text = comment.text.lower() if comment.text else ""
        
        if comment.videoTitle:
            return f"VideoTitle: {comment.videoTitle.lower()} Comment: {text}"
        
        return text
    
    def _analyze_comments_in_batch(self, model: str, comments: list) -> list:
        """Analyze a batch of comments using the transformers pipeline."""
        classifier = self._get_classifier(model)
        
        try:
            texts = [self._map_comment_content(comment) for comment in comments]
            # Process the batch of texts
            results = classifier(texts)
            return [
                CommentAnalysisResult(
                    request=comment,
                    text=comment.text,
                    label=result["label"],
                    score=result["score"],
                    sentiment=result["label"]
                )
                for comment, result in zip(
                    comments, results
                )
            ]
        except Exception as e:
            return [
                {"error": str(e), "comment": comment}
                for comment in comments
            ]
    
    def analyse_comments(self, request: CommentAnalysisRequest) -> list[CommentAnalysisResult]:
        """Analyze comments using the specified model."""
        comments = request.comments
        comment_count = len(comments)
        
        start_time = datetime.datetime.now().timestamp()
        
        # Split comments into smaller batches for processing
        batches = [
            comments[i:i + BATCH_SIZE] 
            for i in range(0, len(comments), BATCH_SIZE)
        ]
        
        # Process batches concurrently
        with ThreadPoolExecutor() as executor:
            results = executor.map(
                lambda x: self._analyze_comments_in_batch(
                    request.model_name,
                    x
                ),
                batches
            )
        
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
        
        print(
            f"Total processing time: {comment_count} comments in "
            f"{total_time} seconds"
        )
        
        return flattened_results


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
    
    response = LlmClassifier().analyse_comments(custom_event)
    print(response)