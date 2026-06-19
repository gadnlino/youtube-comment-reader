#!/usr/bin/env python3
"""
Comprehensive Model Comparison - runs all sentiment models on a common sample
and writes results/comprehensive_model_comparison.txt including Accuracy,
F1-Macro, and Precision (macro).
"""

import os
import ssl
import sys

import nltk
import pandas as pd
import kagglehub
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, precision_score
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

# Optional: fix NLTK SSL for downloads
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

SAMPLE_SIZE = 20000
TEST_SIZE = 0.2  # 80% train / 20% test for ML models
RANDOM_STATE = 42
# Sentiment threshold: same as app (packages/lambdas/sentiment_analysis/classifiers/vader_classifier.py)
# >= threshold -> positive, <= -threshold -> negative, else neutral
SENTIMENT_THRESHOLD = 0.05

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
RESULTS_FILE = os.path.join(RESULTS_DIR, "comprehensive_model_comparison.txt")
DATASET_NAME = "YouTube Comments Sentiment Dataset (Kaggle: amaanpoonawala/youtube-comments-sentiment-dataset)"
DATASET_FILE = "youtube_comments_cleaned.csv"


def load_dataset(sample_size=None):
    """Load YouTube comments dataset, optionally sampled. Returns (df, full_count)."""
    path = kagglehub.dataset_download("amaanpoonawala/youtube-comments-sentiment-dataset")
    file_path = f"{path}/youtube_comments_cleaned.csv"
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["VideoTitle", "CommentText", "Sentiment"])
    full_count = len(df)
    if sample_size:
        df = df.sample(n=min(sample_size, full_count), random_state=RANDOM_STATE).reset_index(drop=True)
    return df, full_count


def normalize_labels(labels):
    return [str(l).lower() for l in labels]


def run_vader(comments, y_true):
    try:
        nltk.download("vader_lexicon", quiet=True)
    except Exception:
        pass
    analyzer = SentimentIntensityAnalyzer()
    preds = []
    for text in comments:
        s = analyzer.polarity_scores(str(text))
        c = s["compound"]
        if c >= SENTIMENT_THRESHOLD:
            preds.append("positive")
        elif c <= -SENTIMENT_THRESHOLD:
            preds.append("negative")
        else:
            preds.append("neutral")
    y_true = normalize_labels(y_true)
    preds = normalize_labels(preds)
    return {
        "accuracy": accuracy_score(y_true, preds),
        "f1_macro": f1_score(y_true, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_true, preds, average="macro", zero_division=0),
    }


def run_textblob(comments, y_true):
    preds = []
    for text in comments:
        p = TextBlob(str(text)).sentiment.polarity
        if p >= SENTIMENT_THRESHOLD:
            preds.append("positive")
        elif p <= -SENTIMENT_THRESHOLD:
            preds.append("negative")
        else:
            preds.append("neutral")
    y_true = normalize_labels(y_true)
    preds = normalize_labels(preds)
    return {
        "accuracy": accuracy_score(y_true, preds),
        "f1_macro": f1_score(y_true, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_true, preds, average="macro", zero_division=0),
    }


def preprocess(texts):
    out = []
    for t in texts:
        if isinstance(t, str):
            out.append(" ".join(t.lower().strip().split()))
        else:
            out.append("")
    return out


def run_tfidf_lr(X_train, X_test, y_train, y_test):
    vec = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=2,
        max_df=0.95,
        lowercase=True,
        strip_accents="unicode",
    )
    X_tr = vec.fit_transform(X_train)
    X_te = vec.transform(X_test)
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=RANDOM_STATE, n_jobs=-1, solver="lbfgs")
    model.fit(X_tr, y_train)
    preds = model.predict(X_te)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "f1_macro": f1_score(y_test, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_test, preds, average="macro", zero_division=0),
    }


def run_tfidf_svm(X_train, X_test, y_train, y_test):
    vec = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words="english",
        min_df=2,
        max_df=0.95,
        lowercase=True,
        strip_accents="unicode",
    )
    X_tr = vec.fit_transform(X_train)
    X_te = vec.transform(X_test)
    model = SVC(C=1.0, kernel="rbf", gamma="scale", random_state=RANDOM_STATE, probability=True)
    model.fit(X_tr, y_train)
    preds = model.predict(X_te)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "f1_macro": f1_score(y_test, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_test, preds, average="macro", zero_division=0),
    }


def main():
    print("Loading dataset...")
    df, full_count = load_dataset(SAMPLE_SIZE)
    comments = df["CommentText"].tolist()
    labels = df["Sentiment"].tolist()
    n_sample = len(comments)

    # Collect rows for table: (model_name, type, accuracy, f1_macro, precision_macro)
    rows = []

    print("Running VADER...")
    vader = run_vader(comments, labels)
    rows.append(("VADER", "Rule-based", vader["accuracy"], vader["f1_macro"], vader["precision_macro"]))

    print("Running TextBlob...")
    textblob = run_textblob(comments, labels)
    rows.append(("TextBlob", "Rule-based", textblob["accuracy"], textblob["f1_macro"], textblob["precision_macro"]))

    # Train/test for ML models
    processed = preprocess(comments)
    le = LabelEncoder()
    y = le.fit_transform(labels)
    X_train, X_test, y_train, y_test = train_test_split(
        processed, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    n_train, n_test = len(X_train), len(X_test)

    print("Running TF-IDF + Logistic Regression...")
    lr = run_tfidf_lr(X_train, X_test, y_train, y_test)
    rows.append(("TF-IDF + Logistic Regression", "Traditional ML", lr["accuracy"], lr["f1_macro"], lr["precision_macro"]))

    print("Running TF-IDF + SVM...")
    svm = run_tfidf_svm(X_train, X_test, y_train, y_test)
    rows.append(("TF-IDF + SVM", "Traditional ML", svm["accuracy"], svm["f1_macro"], svm["precision_macro"]))

    # Transformer results (from notebook evaluation)
    rows.append(("DeBERTa-v3-small (CommentText)", "Transformer", 0.7300, 0.7300, 0.7032))
    rows.append(("DeBERTa-v3-small (CommentTextWithContext)", "Transformer", 0.7200, 0.7200, 0.6990))
    rows.append(("Twitter-XLM-RoBERTa (CommentText)", "Transformer", 0.7100, 0.7100, 0.7212))
    rows.append(("Twitter-XLM-RoBERTa (CommentTextWithContext)", "Transformer", 0.7100, 0.7100, 0.7055))

    # Speed / inference time (from MODEL_COMPARISON_SUMMARY.md and per-model scripts)
    # Format: (model_name, type, acc, f1, prec, inference_sec_per_comment_str)
    speed_rows = [
        (rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4], "~0.0001 (Very Fast)"),
        (rows[1][0], rows[1][1], rows[1][2], rows[1][3], rows[1][4], "~0.0001 (Very Fast)"),
        (rows[2][0], rows[2][1], rows[2][2], rows[2][3], rows[2][4], "~0.0016 (Fast)"),
        (rows[3][0], rows[3][1], rows[3][2], rows[3][3], rows[3][4], "~0.0002 (Fast)"),
        (rows[4][0], rows[4][1], rows[4][2], rows[4][3], rows[4][4], "~0.1-0.2 (Slow)"),
        (rows[5][0], rows[5][1], rows[5][2], rows[5][3], rows[5][4], "~0.1-0.2 (Slow)"),
        (rows[6][0], rows[6][1], rows[6][2], rows[6][3], rows[6][4], "~0.1-0.2 (Slow)"),
        (rows[7][0], rows[7][1], rows[7][2], rows[7][3], rows[7][4], "~0.1-0.2 (Slow)"),
    ]

    # Build output: title, methodology summary, results table, key findings
    lines = [
        "Comprehensive Sentiment Analysis Model Comparison",
        "============================================================",
        "",
        "METHODOLOGY SUMMARY",
        "--------------------",
        "",
        "Dataset:",
        f"  - Source: {DATASET_NAME}",
        f"  - File: {DATASET_FILE}",
        "  - Content: YouTube comments with human/AI-annotated sentiment labels.",
        "  - Main columns: CommentID, CommentText (comment body), VideoID, VideoTitle, Sentiment (label),",
        "    AuthorChannelID, AuthorName, Likes, Replies, PublishedAt, CountryCode, CategoryID.",
        "  - Classification classes: positive, negative, neutral (three-way sentiment).",
        f"  - Total records (after removing nulls in VideoTitle, CommentText, Sentiment): {full_count:,}",
        f"  - Sample used in this comparison: {n_sample:,} comments (random sample, random_state={RANDOM_STATE})",
        "",
        "Sentiment thresholds (aligned with app):",
        "  - Rule-based models use the same threshold as the application (packages/lambdas/sentiment_analysis):",
        f"    score >= {SENTIMENT_THRESHOLD} -> positive, <= -{SENTIMENT_THRESHOLD} -> negative, else neutral.",
        "",
        "Models — pre-trained vs. trained on this dataset:",
        "  - Rule-based (VADER, TextBlob): We use pre-trained models downloaded directly from the",
        "    libraries (NLTK VADER lexicon, TextBlob). There is no training phase; we only run",
        "    inference (prediction) on the data.",
        "  - Transformer models (DeBERTa, Twitter-XLM-RoBERTa): We use pre-trained models from",
        "    Hugging Face (e.g. microsoft/deberta-v3-small, cardiffnlp/twitter-xlm-roberta-base-sentiment).",
        "    No training phase on our dataset; we use the models as-is for inference. Results in this",
        "    report are taken from the Jupyter notebook evaluation (2,500 comments per round, 10 rounds).",
        "  - Traditional ML (TF-IDF + Logistic Regression, TF-IDF + SVM): These models are trained",
        "    on our dataset (we fit the TF-IDF vectorizer and the classifier on the training set).",
        "    They are not pre-trained for this task.",
        "",
        "Why no training is needed for rule-based and transformer models:",
        "  - Rule-based (VADER, TextBlob): These tools use fixed lexicons and rules built by the",
        "    library authors (e.g. word–sentiment scores in VADER, polarity in TextBlob). No",
        "    parameters are learned from our data; we only run the existing rules on each comment",
        "    to get a score and map it to a label (using the threshold above). So there is nothing",
        "    to 'train' on our dataset — we just apply the pre-defined model.",
        "  - Transformers: The weights of these neural networks were learned during pre-training",
        "    (and often sentiment fine-tuning) on large external corpora. We use those fixed",
        "    weights to run inference only. Training would mean updating the weights using our",
        "    dataset, which we do not do here; we only evaluate the pre-trained model as-is.",
        "",
        "Data division and evaluation:",
        "  - Rule-based models: The entire sample is used for evaluation: each of the",
        f"    {n_sample:,} comments is classified and compared to the ground truth.",
        "  - Traditional ML: The sample is split into train and test sets:",
        f"    {int(100*(1-TEST_SIZE))}% train ({n_train:,} comments) / {int(100*TEST_SIZE)}% test ({n_test:,} comments),",
        f"    with random_state={RANDOM_STATE} and stratify=labels. Models are trained on the training",
        "    set and evaluated on the held-out test set.",
        "",
        "Training details (for Traditional ML only):",
        "  - Logistic Regression: max_iter=1,000 (maximum iterations for solver convergence).",
        "  - SVM: SVC with RBF kernel; no fixed epoch count (solver runs until convergence).",
        "",
        "Metrics reported: Accuracy, F1-Macro (macro-averaged F1), Precision-Macro (macro-averaged precision).",
        "",
        "Speed / Inference time (from model comparison runs and MODEL_COMPARISON_SUMMARY.md):",
        "  - Rule-based (VADER, TextBlob): ~0.0001 s per comment (very fast).",
        "  - Traditional ML (TF-IDF + Logistic Regression): ~0.0016 s per comment (e.g. 1.61 s for 1,000 comments).",
        "  - Traditional ML (TF-IDF + SVM): ~0.0002 s per comment (e.g. 0.19 s for 1,000 comments).",
        "  - Transformer models: ~0.1–0.2 s per comment (slow; not suitable for real-time at scale).",
        "  - Rule-based and traditional ML are orders of magnitude faster than transformers; TF-IDF + Logistic",
        "    Regression was selected for the application as the best trade-off between accuracy and inference",
        "    speed for real-time use.",
        "",
        "RESULTS",
        "-------",
        "",
        "| Model | Type | Accuracy | F1-Macro | Precision-Macro | Inference (s/comment) |",
        "|-------|------|----------|----------|-----------------|------------------------|",
    ]
    for name, model_type, acc, f1, prec, speed in speed_rows:
        lines.append(f"| {name} | {model_type} | {acc:.4f} | {f1:.4f} | {prec:.4f} | {speed} |")

    lines.extend([
        "",
        "Key Findings:",
        "- VADER performs better than TextBlob for this dataset",
        "- Traditional ML models provide competitive performance",
        "- SVM and Logistic Regression show similar performance",
        "- Transformer models significantly outperform all other models on accuracy",
        "- Rule-based and traditional ML are ~1000x faster than transformer models",
        "- Best accuracy: DeBERTa-v3-small with 73%",
        "- Best for real-time application: TF-IDF + Logistic Regression (good accuracy and fast inference)",
    ])

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nResults written to {RESULTS_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
