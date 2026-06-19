#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compara métricas da pipeline de comprehensive_model_comparison em duas amostras de 20k:

  A) Amostra aleatória simples (random_state=42) — igual ao script original.
  B) Amostra balanceada: ~1/3 por classe (estratificação por contagem fixa por classe).

Escreve relatório em results/ nesta pasta.
"""

from __future__ import annotations

import os
import ssl
import sys
from datetime import datetime
from typing import Any, Dict, List, Tuple

import kagglehub
import nltk
import numpy as np
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from textblob import TextBlob

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

SAMPLE_N = 20000
TEST_SIZE = 0.2
RANDOM_STATE = 42
SENTIMENT_THRESHOLD = 0.05

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(HERE, "results")


def load_full_dataframe() -> Tuple[pd.DataFrame, int]:
    path = kagglehub.dataset_download("amaanpoonawala/youtube-comments-sentiment-dataset")
    file_path = f"{path}/youtube_comments_cleaned.csv"
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["VideoTitle", "CommentText", "Sentiment"])
    full_count = len(df)
    return df, full_count


def sample_random_n(df: pd.DataFrame, n: int, random_state: int) -> pd.DataFrame:
    take = min(n, len(df))
    return df.sample(n=take, random_state=random_state).reset_index(drop=True)


def sample_balanced_thirds(df: pd.DataFrame, n: int, random_state: int) -> pd.DataFrame:
    """
    Exatamente n linhas com distribuição o mais próxima possível de n/3 por classe.
    Rótulos agrupados por Sentiment normalizado (lower strip).
    """
    work = df.copy()
    work["_norm"] = work["Sentiment"].astype(str).str.strip().str.lower()
    classes = sorted(work["_norm"].unique())
    if len(classes) != 3:
        raise ValueError(f"Esperadas 3 classes, obtidas: {classes}")

    k = len(classes)
    base = n // k
    rem = n % k
    targets: Dict[str, int] = {}
    for i, c in enumerate(classes):
        targets[c] = base + (1 if i < rem else 0)

    parts: List[pd.DataFrame] = []
    for c, need in targets.items():
        pool = work[work["_norm"] == c]
        if len(pool) < need:
            raise ValueError(
                f"Classe '{c}' tem só {len(pool)} exemplos; precisamos {need}."
            )
        parts.append(pool.sample(n=need, random_state=random_state))
    out = pd.concat(parts, ignore_index=True)
    out = out.sample(frac=1, random_state=random_state).reset_index(drop=True)
    out = out.drop(columns=["_norm"])
    return out


def label_distribution(df: pd.DataFrame) -> Dict[str, int]:
    s = df["Sentiment"].astype(str).str.strip().str.lower()
    return s.value_counts().sort_index().to_dict()


def normalize_labels(labels: List[Any]) -> List[str]:
    return [str(l).lower() for l in labels]


def preprocess(texts: List[str]) -> List[str]:
    out = []
    for t in texts:
        if isinstance(t, str):
            out.append(" ".join(t.lower().strip().split()))
        else:
            out.append("")
    return out


def run_vader(comments: List[str], y_true: List[Any]) -> Dict[str, float]:
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
    y_t = normalize_labels(y_true)
    preds = normalize_labels(preds)
    return {
        "accuracy": accuracy_score(y_t, preds),
        "f1_macro": f1_score(y_t, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_t, preds, average="macro", zero_division=0),
    }


def run_textblob(comments: List[str], y_true: List[Any]) -> Dict[str, float]:
    preds = []
    for text in comments:
        p = TextBlob(str(text)).sentiment.polarity
        if p >= SENTIMENT_THRESHOLD:
            preds.append("positive")
        elif p <= -SENTIMENT_THRESHOLD:
            preds.append("negative")
        else:
            preds.append("neutral")
    y_t = normalize_labels(y_true)
    preds = normalize_labels(preds)
    return {
        "accuracy": accuracy_score(y_t, preds),
        "f1_macro": f1_score(y_t, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_t, preds, average="macro", zero_division=0),
    }


def run_tfidf_lr(
    X_train: List[str],
    X_test: List[str],
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> Dict[str, float]:
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
    model = LogisticRegression(
        C=1.0,
        max_iter=1000,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        solver="lbfgs",
    )
    model.fit(X_tr, y_train)
    preds = model.predict(X_te)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "f1_macro": f1_score(y_test, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_test, preds, average="macro", zero_division=0),
    }


def run_tfidf_svm(
    X_train: List[str],
    X_test: List[str],
    y_train: np.ndarray,
    y_test: np.ndarray,
) -> Dict[str, float]:
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
    model = SVC(
        C=1.0,
        kernel="rbf",
        gamma="scale",
        random_state=RANDOM_STATE,
        probability=True,
    )
    model.fit(X_tr, y_train)
    preds = model.predict(X_te)
    return {
        "accuracy": accuracy_score(y_test, preds),
        "f1_macro": f1_score(y_test, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(y_test, preds, average="macro", zero_division=0),
    }


def run_pipeline(sample_name: str, df: pd.DataFrame) -> List[Tuple[str, str, float, float, float]]:
    comments = df["CommentText"].tolist()
    labels = df["Sentiment"].tolist()
    n = len(comments)

    rows: List[Tuple[str, str, float, float, float]] = []

    print(f"\n=== {sample_name} (n={n}) ===")
    print("Distribuição (rótulo normalizado):", label_distribution(df))

    print("  VADER...")
    v = run_vader(comments, labels)
    rows.append(("VADER", "Rule-based", v["accuracy"], v["f1_macro"], v["precision_macro"]))

    print("  TextBlob...")
    tb = run_textblob(comments, labels)
    rows.append(("TextBlob", "Rule-based", tb["accuracy"], tb["f1_macro"], tb["precision_macro"]))

    processed = preprocess(comments)
    le = LabelEncoder()
    y = le.fit_transform(labels)
    X_train, X_test, y_train, y_test = train_test_split(
        processed,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print("  TF-IDF + LR...")
    lr = run_tfidf_lr(X_train, X_test, y_train, y_test)
    rows.append(
        ("TF-IDF + Logistic Regression", "Traditional ML", lr["accuracy"], lr["f1_macro"], lr["precision_macro"])
    )

    print("  TF-IDF + SVM...")
    svm = run_tfidf_svm(X_train, X_test, y_train, y_test)
    rows.append(("TF-IDF + SVM", "Traditional ML", svm["accuracy"], svm["f1_macro"], svm["precision_macro"]))

    return rows


def write_report(
    full_count: int,
    dist_random: Dict[str, int],
    dist_balanced: Dict[str, int],
    rows_random: List[Tuple],
    rows_balanced: List[Tuple],
    path: str,
) -> None:
    lines = [
        "Comparação: amostra 20k ALEATÓRIA vs. 20k BALANCEADA (~⅓ por classe)",
        "=====================================================================",
        "",
        "Dataset: amaanpoonawala/youtube-comments-sentiment-dataset (youtube_comments_cleaned.csv)",
        f"Registros após remoção de nulos (VideoTitle, CommentText, Sentiment): {full_count:,}",
        "",
        "Amostra A — aleatória simples: sample(n=20000, random_state=42)",
        f"Distribuição (contagem por classe, rótulo lower): {dist_random}",
        "",
        "Amostra B — balanceada: 6667 + 6667 + 6666 = 20000 (ordem alfabética negative, neutral, positive)",
        f"Distribuição: {dist_balanced}",
        "",
        "Para modelos TF-IDF: train/test 80/20 com stratify=y (igual ao comprehensive_model_comparison).",
        "",
        "RESULTADOS (Accuracy, F1-macro, Precision-macro)",
        "-------------------------------------------------",
        "",
        f"{'Modelo':<35} {'Tipo':<18} {'Acc_A':>8} {'F1_A':>8} {'Prec_A':>8} | {'Acc_B':>8} {'F1_B':>8} {'Prec_B':>8} | {'ΔAcc':>8}",
        "-" * 120,
    ]
    for i in range(len(rows_random)):
        name, mtype, a1, f1, p1 = rows_random[i]
        _, _, a2, f2, p2 = rows_balanced[i]
        dacc = a2 - a1
        lines.append(
            f"{name:<35} {mtype:<18} {a1:>8.4f} {f1:>8.4f} {p1:>8.4f} | {a2:>8.4f} {f2:>8.4f} {p2:>8.4f} | {dacc:>+8.4f}"
        )

    lines.extend(
        [
            "",
            "ΔAcc = Acc_B (balanceada) - Acc_A (aleatória), mesma linha de modelo.",
            "",
            "Notas:",
            "- VADER/TextBlob: métricas em todo o subconjunto de 20k.",
            "- TF-IDF+LR / TF-IDF+SVM: métricas no holdout 20% (~4k), após treino em 80%.",
            "- Pequenas diferenças são esperadas (outra composição da amostra + variância do split).",
            "",
        ]
    )

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> int:
    print("Carregando dataset completo...")
    df_full, full_count = load_full_dataframe()
    print(f"Total após dropna: {full_count:,}")

    df_random = sample_random_n(df_full, SAMPLE_N, RANDOM_STATE)
    df_balanced = sample_balanced_thirds(df_full, SAMPLE_N, RANDOM_STATE)

    dist_r = label_distribution(df_random)
    dist_b = label_distribution(df_balanced)

    rows_r = run_pipeline("A — Aleatória 20k", df_random)
    rows_b = run_pipeline("B — Balanceada 20k", df_balanced)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(RESULTS_DIR, f"random_vs_balanced_20k_{ts}.txt")
    write_report(full_count, dist_r, dist_b, rows_r, rows_b, out_path)

    print(f"\nRelatório salvo em: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
