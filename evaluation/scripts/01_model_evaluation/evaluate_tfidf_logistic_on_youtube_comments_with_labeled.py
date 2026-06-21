#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluate the existing TF-IDF + Logistic Regression sentiment model on:
  "YouTube Comments with Labeled" (Kaggle,
  amitzala/youtube-comments-with-labeled).

Outputs:
- CSV with per-class metrics (+ global/macro)
- PNG grouped bar chart with thesis-required styling
- Text summary ready to paste into the thesis
  (includes required dictionary + analysis)
"""

from __future__ import annotations

import os
import re
import json
import pickle
import glob
import time
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

import kagglehub
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)


DATASET_SLUG = "amitzala/youtube-comments-with-labeled"
DATASET_NAME = "YouTube Comments with Labeled"

CLASSES = ["NEGATIVE", "NEUTRAL", "POSITIVE"]
CLASSES_DISPLAY_PT = ["NEGATIVO", "NEUTRO", "POSITIVO"]
LOWER_TO_STD = {c.lower(): c for c in CLASSES}

PRECISION_COLOR = "#87CEFA"  # light blue
RECALL_COLOR = "#FF7F7F"  # light red
F1_COLOR = "#800080"  # purple
ACCURACY_COLOR = "#A0522D"  # brown

SENTIMENT_MAP = {
    "positive": "POSITIVE",
    "pos": "POSITIVE",
    "neutral": "NEUTRAL",
    "negativo": "NEGATIVE",
    "negative": "NEGATIVE",
    "neg": "NEGATIVE",
}


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))


def load_pretrained_tfidf_lr_artifact() -> Tuple[Any, Any, Any]:
    """
    Loads the TF-IDF + Logistic Regression artifact trained in this repo.
    Expected artifact structure:
      {'model': <LogisticRegression>, 'vectorizer': <TfidfVectorizer>, 'label_encoder': <LabelEncoder>}
    """
    artifact_path = os.path.join(
        repo_root(),
        "packages/lambdas/sentiment_analysis/models/tfidf_logistic_model.pkl",
    )
    if not os.path.exists(artifact_path):
        raise FileNotFoundError(f"Pre-trained artifact not found: {artifact_path}")

    with open(artifact_path, "rb") as f:
        data = pickle.load(f)

    if isinstance(data, dict) and {"model", "vectorizer", "label_encoder"}.issubset(data.keys()):
        return data["model"], data["vectorizer"], data["label_encoder"]

    # Fallback: best-effort extraction
    model = data.get("model") if isinstance(data, dict) else None
    vectorizer = data.get("vectorizer") if isinstance(data, dict) else None
    label_encoder = data.get("label_encoder") if isinstance(data, dict) else None
    if model is not None and vectorizer is not None and label_encoder is not None:
        return model, vectorizer, label_encoder

    raise ValueError("Unsupported artifact format. Expected keys: model, vectorizer, label_encoder.")


def download_kaggle_dataset() -> str:
    return kagglehub.dataset_download(DATASET_SLUG)


def _score_column(name_lower: str, targets: Iterable[str]) -> int:
    return max((1 for t in targets if t in name_lower), default=0)


def load_csv_and_extract_columns(dataset_path: str) -> pd.DataFrame:
    """
    Returns a DataFrame with schema:
      df = {'text': <comment text>, 'label': <NEGATIVE/NEUTRAL/POSITIVE>}
    """
    csv_files = glob.glob(os.path.join(dataset_path, "**", "*.csv"), recursive=True)
    if not csv_files:
        raise FileNotFoundError(f"No CSV found under downloaded dataset path: {dataset_path}")

    # Find the CSV that contains the expected columns.
    # This dataset is expected to have 'comment' and 'sentiment', but we make it robust.
    candidates: List[Tuple[int, str, str, str]] = []

    for csv_path in csv_files:
        try:
            df_head = pd.read_csv(
                csv_path,
                nrows=20,
                low_memory=False,
                encoding="utf-8",
                encoding_errors="replace",
            )
        except Exception:
            continue

        col_names = list(df_head.columns)

        text_col = None
        label_col = None

        # Text column candidates
        text_targets = ["comment", "text", "review", "content", "body"]
        best_text_score = -1
        for c in col_names:
            cl = c.lower()
            sc = _score_column(cl, text_targets)
            # Prefer exact matches like "comment"
            if cl in {"comment", "commenttext", "text"}:
                sc += 2
            if sc > best_text_score:
                best_text_score = sc
                text_col = c

        # Label column candidates
        label_targets = ["sentiment", "label", "polarity", "class", "target"]
        best_label_score = -1
        for c in col_names:
            cl = c.lower()
            sc = _score_column(cl, label_targets)
            if cl in {"sentiment", "label"}:
                sc += 2
            if sc > best_label_score:
                best_label_score = sc
                label_col = c

        if text_col and label_col:
            candidates.append(
                (best_text_score + best_label_score, csv_path, text_col, label_col)
            )

    if not candidates:
        raise RuntimeError(
            "Could not identify comment/text and sentiment/label columns in "
            f"{dataset_path}"
        )

    candidates.sort(key=lambda x: x[0], reverse=True)
    _, csv_path, text_col, label_col = candidates[0]

    df = pd.read_csv(
        csv_path,
        usecols=[text_col, label_col],
        low_memory=False,
        encoding="utf-8",
        encoding_errors="replace",
    )

    df = df.dropna(subset=[text_col, label_col]).copy()
    df["text"] = df[text_col].fillna("").astype(str)
    df["label_raw"] = df[label_col]
    df["label"] = normalize_labels_series(df["label_raw"])
    df = df.dropna(subset=["label"]).copy()

    df = df[["text", "label"]].reset_index(drop=True)
    print(f"✅ Dataset CSV loaded: {os.path.basename(csv_path)}")
    print(f"   Text column: {text_col} | Label column: {label_col}")
    print(f"   Label distribution: {df['label'].value_counts().to_dict()}")
    return df


def preprocess_texts(texts: Iterable[Any]) -> List[str]:
    """
    Reuses the same basic preprocessing as the app TF-IDF classifier:
    - lowercase
    - strip
    - collapse multiple whitespace
    """
    out: List[str] = []
    for t in texts:
        if isinstance(t, str):
            cleaned = t.lower().strip()
            cleaned = " ".join(cleaned.split())
            out.append(cleaned)
        else:
            out.append("")
    return out


def normalize_labels_series(labels: pd.Series) -> pd.Series:
    def normalize_one(x: Any) -> Optional[str]:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return None
        s = str(x).strip().lower()
        if not s:
            return None

        if s in LOWER_TO_STD:
            return LOWER_TO_STD[s]
        if s in SENTIMENT_MAP:
            return SENTIMENT_MAP[s]

        # Numeric fallback: assume 0=negative, 1=neutral, 2=positive
        # (common convention).
        if re.fullmatch(r"-?\d+", s):
            try:
                v = int(s)
                if v == 0:
                    return "NEGATIVE"
                if v == 1:
                    return "NEUTRAL"
                if v == 2:
                    return "POSITIVE"
            except Exception:
                pass

        return None

    return labels.apply(normalize_one)


def predict_tfidf_lr_in_batches(
    texts: List[str],
    model: Any,
    vectorizer: Any,
    label_encoder: Any,
    batch_size: int = 5000,
) -> np.ndarray:
    """
    Batch inference to avoid creating one huge sparse matrix at once.
    """
    y_pred: List[str] = []
    n = len(texts)

    for start in range(0, n, batch_size):
        end = min(n, start + batch_size)
        batch = texts[start:end]

        X = vectorizer.transform(batch)
        probs = model.predict_proba(X)
        idx = np.argmax(probs, axis=1)
        pred_lower = label_encoder.inverse_transform(idx)

        y_batch = [
            LOWER_TO_STD.get(str(pl).lower(), "NEUTRAL") for pl in pred_lower
        ]
        y_pred.extend(y_batch)

        if start == 0 or end == n or (start // batch_size) % 10 == 0:
            print(f"   Inference progress: {end}/{n}")

    return np.array(y_pred, dtype=object)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
    precision_per = precision_score(
        y_true,
        y_pred,
        labels=CLASSES,
        average=None,
        zero_division=0,
    )
    recall_per = recall_score(
        y_true,
        y_pred,
        labels=CLASSES,
        average=None,
        zero_division=0,
    )
    f1_per = f1_score(
        y_true,
        y_pred,
        labels=CLASSES,
        average=None,
        zero_division=0,
    )

    accuracy = accuracy_score(y_true, y_pred)
    precision_macro = precision_score(
        y_true,
        y_pred,
        labels=CLASSES,
        average="macro",
        zero_division=0,
    )
    f1_macro = f1_score(
        y_true,
        y_pred,
        labels=CLASSES,
        average="macro",
        zero_division=0,
    )

    support = {c: int(np.sum(y_true == c)) for c in CLASSES}

    return {
        "accuracy": float(accuracy),
        "precision_macro": float(precision_macro),
        "f1_macro": float(f1_macro),
        "precision_per_class": {
            c: float(v) for c, v in zip(CLASSES, precision_per)
        },
        "recall_per_class": {c: float(v) for c, v in zip(CLASSES, recall_per)},
        "f1_per_class": {c: float(v) for c, v in zip(CLASSES, f1_per)},
        "support": support,
    }


def load_previous_tfidf_lr_metrics() -> Optional[Dict[str, float]]:
    prev_path = os.path.join(
        repo_root(),
        "evaluation/model_comparison/results/comprehensive_model_comparison.txt",
    )
    if not os.path.exists(prev_path):
        print(f"⚠️ Previous comparison file not found: {prev_path}")
        return None

    with open(prev_path, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()

    # Matches the row format in comprehensive_model_comparison.txt
    # | TF-IDF + Logistic Regression | Traditional ML | 0.5948 | 0.5961 | 0.6000 | ...
    m = re.search(
        r"\|\s*TF-IDF\s*\+\s*Logistic\s*Regression\s*\|\s*Traditional\s*ML\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|",
        txt,
    )
    if not m:
        print("⚠️ Could not parse TF-IDF + Logistic Regression row from previous comparison file.")
        return None

    return {
        "accuracy": float(m.group(1)),
        "f1_macro": float(m.group(2)),
        "precision_macro": float(m.group(3)),
    }


def build_generalization_analysis(current_metrics: Dict[str, Any]) -> Tuple[str, str]:
    """
    Returns (notes_short, thesis_block).
    """
    prev = load_previous_tfidf_lr_metrics()
    if not prev:
        notes_short = "Comparação limitada: não foi possível carregar métricas anteriores do benchmark."
        thesis_block = (
            "Generalização (comparação com benchmark anterior):\n"
            "- Não foi possível carregar as métricas anteriores de referência (TF-IDF + Logistic Regression) "
            "do arquivo `comprehensive_model_comparison.txt`. Assim, não há uma comparação quantitativa direta."
        )
        return notes_short, thesis_block

    cur_acc = float(current_metrics["accuracy"])
    cur_f1_macro = float(current_metrics["f1_macro"])

    prev_acc = float(prev["accuracy"])
    prev_f1_macro = float(prev["f1_macro"])

    delta_acc = cur_acc - prev_acc
    delta_f1 = cur_f1_macro - prev_f1_macro

    def sign_word(x: float) -> str:
        if x > 0:
            return "aumentou"
        if x < 0:
            return "diminuiu"
        return "permaneceu similar"

    def delta_pp(x: float) -> float:
        return round(x * 100, 2)

    notes_short = (
        "O modelo TF-IDF + Logistic Regression teve uma variação de "
        f"{delta_pp(delta_acc)} p.p. em accuracy e {delta_pp(delta_f1)} "
        "p.p. em F1-macro em relação ao benchmark anterior."
    )

    thesis_block = (
        "Generalização (comparação com benchmark anterior):\n"
        f"- Em {DATASET_NAME}, a accuracy do TF-IDF + Logistic Regression "
        f"{sign_word(delta_acc)} em "
        f"{delta_pp(delta_acc)} p.p. (de {prev_acc:.4f} para {cur_acc:.4f}).\n"
        f"- A F1-macro {sign_word(delta_f1)} em {delta_pp(delta_f1)} p.p. "
        f"(de {prev_f1_macro:.4f} para {cur_f1_macro:.4f}).\n"
        "- Possíveis causas para diferenças de desempenho (sem assumir causalidade direta): "
        "diferenças de domínio entre datasets, mismatch de vocabulário e maior presença de linguagem informal/slang em comentários. "
        "Esses fatores podem afetar a distribuição de termos e, consequentemente, a capacidade de generalização do classificador."
    )

    return notes_short, thesis_block


def plot_metrics_bar_chart(
    precision: List[float],
    recall: List[float],
    f1_score_vals: List[float],
    accuracy_vals: List[float],
    missing_classes: List[str],
    dataset_name_for_title: str,
    output_png_path: str,
) -> None:
    """
    Produces the chart in the exact grouped-bar format required by the thesis.
    """
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300
    # Larger fonts for readability when the chart is viewed as an image
    plt.rcParams["font.size"] = 13
    plt.rcParams["axes.labelsize"] = 14
    plt.rcParams["axes.titlesize"] = 16
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams["legend.fontsize"] = 12

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(CLASSES))
    width = 0.2
    offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]

    bars_precision = ax.bar(
        x + offsets[0],
        precision,
        width,
        label="Precisão",
        color=PRECISION_COLOR,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.9,
    )
    bars_recall = ax.bar(
        x + offsets[1],
        recall,
        width,
        label="Recall",
        color=RECALL_COLOR,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.9,
    )
    bars_f1 = ax.bar(
        x + offsets[2],
        f1_score_vals,
        width,
        label="F1-Score",
        color=F1_COLOR,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.9,
    )
    bars_accuracy = ax.bar(
        x + offsets[3],
        accuracy_vals,
        width,
        label="Acurácia",
        color=ACCURACY_COLOR,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.9,
    )

    ax.set_title(f"Métricas por Classe ({dataset_name_for_title})", pad=14)
    ax.set_xlabel("Classes (NEGATIVO, NEUTRO, POSITIVO)")
    ax.set_ylabel("Valores das Métricas (0 a 1)")
    ax.set_xticks(x)
    ax.set_xticklabels(CLASSES_DISPLAY_PT)
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    legend = ax.legend(
        title="Métricas de Desempenho",
        loc="upper left",
        frameon=True,
    )
    legend.get_frame().set_alpha(0.9)

    # Add numeric values on top of bars.
    def annotate_bars(bars: Any) -> None:
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                h + 0.01,
                f"{h:.2f}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold",
            )

    annotate_bars(bars_precision)
    annotate_bars(bars_recall)
    annotate_bars(bars_f1)
    annotate_bars(bars_accuracy)

    # Required note when any class is absent in ground truth.
    if missing_classes:
        note_text = "Nota: Classes ausentes no ground truth possuem métricas zeradas."
        plt.figtext(
            0.5,
            0.01,
            note_text,
            ha="center",
            fontsize=11,
            style="italic",
            color="gray",
            wrap=True,
        )

    plt.tight_layout()
    plt.savefig(output_png_path, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Chart saved: {output_png_path}")


def save_metrics_csv(
    dataset_name: str,
    metrics: Dict[str, Any],
    output_csv_path: str,
) -> None:
    rows = []
    for c in CLASSES:
        rows.append(
            {
                "dataset": dataset_name,
                "class": c,
                "support": metrics["support"][c],
                "precision": metrics["precision_per_class"][c],
                "recall": metrics["recall_per_class"][c],
                "f1_score": metrics["f1_per_class"][c],
                "accuracy_global": metrics["accuracy"],
            }
        )

    macro_row = {
        "dataset": dataset_name,
        "class": "MACRO",
        "support": int(sum(metrics["support"].values())),
        "precision": metrics["precision_macro"],
        "recall": np.nan,
        "f1_score": metrics["f1_macro"],
        "accuracy_global": metrics["accuracy"],
    }
    rows.append(macro_row)

    df_out = pd.DataFrame(rows)
    df_out.to_csv(output_csv_path, index=False)
    print(f"✅ Metrics CSV saved: {output_csv_path}")


def save_predictions_csv(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    output_csv_path: str,
) -> None:
    df = pd.DataFrame({"true_label": y_true, "predicted_label": y_pred})
    df.to_csv(output_csv_path, index=False)
    print(f"✅ Predictions CSV saved: {output_csv_path}")


def main() -> int:
    print(f"▶ Evaluating on Kaggle dataset: {DATASET_SLUG}")
    print(f"  Dataset display name: {DATASET_NAME}")

    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    graphs_dir = os.path.join(os.path.dirname(__file__), "..", "graphs")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_metrics_path = os.path.join(
        results_dir, f"metrics_tfidf_lr_{DATASET_SLUG.replace('/', '_')}_{ts}.csv"
    )
    csv_predictions_path = os.path.join(
        results_dir, f"predictions_tfidf_lr_{DATASET_SLUG.replace('/', '_')}_{ts}.csv"
    )
    chart_png_path = os.path.join(
        graphs_dir, f"metrics_per_class_tfidf_lr_{DATASET_SLUG.replace('/', '_')}_{ts}.png"
    )
    summary_txt_path = os.path.join(
        results_dir, f"metrics_summary_tfidf_lr_{DATASET_SLUG.replace('/', '_')}_{ts}.txt"
    )

    dataset_path = download_kaggle_dataset()
    df = load_csv_and_extract_columns(dataset_path)

    texts_raw = df["text"].tolist()
    y_true = df["label"].to_numpy(dtype=object)

    print("🧹 Preprocessing text...")
    texts_processed = preprocess_texts(texts_raw)

    print("📦 Loading pre-trained TF-IDF + Logistic Regression artifact...")
    model, vectorizer, label_encoder = load_pretrained_tfidf_lr_artifact()

    print(f"🔮 Running inference (batch_size=5000) on {len(texts_processed):,} comments...")
    start_time = time.time()
    y_pred = predict_tfidf_lr_in_batches(texts_processed, model, vectorizer, label_encoder, batch_size=5000)
    elapsed = time.time() - start_time
    print(f"✅ Inference complete in {elapsed:.2f}s")

    print("📊 Computing metrics...")
    metrics = compute_metrics(y_true, y_pred)

    missing_classes = [c for c in CLASSES if metrics["support"][c] == 0]
    print(f"Label support (ground truth): {metrics['support']}")

    # Chart values: enforce required "missing class -> 0 metrics" behavior.
    precision_vals = [metrics["precision_per_class"][c] for c in CLASSES]
    recall_vals = [metrics["recall_per_class"][c] for c in CLASSES]
    f1_vals = [metrics["f1_per_class"][c] for c in CLASSES]
    accuracy_global = metrics["accuracy"]
    accuracy_vals = [accuracy_global for _ in CLASSES]

    if missing_classes:
        for i, c in enumerate(CLASSES):
            if metrics["support"][c] == 0:
                precision_vals[i] = 0.0
                recall_vals[i] = 0.0
                f1_vals[i] = 0.0
                accuracy_vals[i] = 0.0

    plot_metrics_bar_chart(
        precision_vals,
        recall_vals,
        f1_vals,
        accuracy_vals,
        missing_classes=missing_classes,
        dataset_name_for_title=DATASET_NAME,
        output_png_path=chart_png_path,
    )

    save_metrics_csv(DATASET_NAME, metrics, csv_metrics_path)
    save_predictions_csv(y_true, y_pred, csv_predictions_path)

    notes_short, thesis_block = build_generalization_analysis(metrics)
    summary_dict = {
        "dataset": DATASET_NAME,
        "accuracy": float(metrics["accuracy"]),
        "precision_macro": float(metrics["precision_macro"]),
        "f1_macro": float(metrics["f1_macro"]),
        "notes": notes_short,
    }

    # Printed metrics summary (required by the plan).
    per_class_lines = []
    for c in CLASSES:
        per_class_lines.append(
            f"- {c}: precision={metrics['precision_per_class'][c]:.4f}, "
            f"recall={metrics['recall_per_class'][c]:.4f}, f1={metrics['f1_per_class'][c]:.4f}, "
            f"support={metrics['support'][c]}"
        )

    printed_summary = (
        f"TF-IDF + Logistic Regression evaluation on {DATASET_NAME}\n"
        f"Accuracy: {metrics['accuracy']:.4f}\n"
        f"Precision (macro): {metrics['precision_macro']:.4f}\n"
        f"F1 (macro): {metrics['f1_macro']:.4f}\n"
        f"Per-class metrics:\n"
        + "\n".join(per_class_lines)
    )

    print("\n" + "=" * 80)
    print("METRICS SUMMARY")
    print("=" * 80)
    print(printed_summary)
    print("\nRequired dictionary:\n" + json.dumps(summary_dict, ensure_ascii=False, indent=2))
    print("\n" + "=" * 80)
    print("GENERALIZATION ANALYSIS (THESIS-READY)")
    print("=" * 80)
    print(thesis_block)

    summary_txt = (
        printed_summary
        + "\n\n"
        + "Dictionary (required):\n"
        + json.dumps(summary_dict, ensure_ascii=False, indent=2)
        + "\n\n"
        + "Generalization analysis (thesis-ready):\n"
        + thesis_block
        + "\n"
    )
    with open(summary_txt_path, "w", encoding="utf-8") as f:
        f.write(summary_txt)

    print(f"✅ Thesis-ready summary saved: {summary_txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

