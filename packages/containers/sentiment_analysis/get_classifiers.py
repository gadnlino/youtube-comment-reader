from classifiers.base_comment_classifier import BaseCommentClassifier
from classifiers.llm_classifier import LlmClassifier
from classifiers.vader_classifier import VaderClassifier


classifiers: dict[str, BaseCommentClassifier] = {
            "llm": LlmClassifier(),
            "vader": VaderClassifier()
        }


def get_classifier(classifier_name: str) -> BaseCommentClassifier:
    return classifiers[classifier_name]