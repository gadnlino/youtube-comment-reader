
from models.models import CommentAnalysisRequest, CommentAnalysisResult


class BaseCommentClassifier:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def analyse_comments(self, request: CommentAnalysisRequest) -> list[CommentAnalysisResult]:
        raise NotImplementedError("Subclass must implement this method")
