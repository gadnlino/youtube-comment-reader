#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compara métricas do TF-IDF + Regressão Logística:

- Seleção do modelo: valores da tabela em
  evaluation/model_comparison/results/comprehensive_model_comparison.txt
  (amostra 20k, split 80/20 no dataset amaanpoonawala, conforme descrito no arquivo).

- Avaliação externa: último CSV gerado por
  evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py
  (dataset Kaggle amitzala, inferência com artefato pré-treinado, sem retreinamento).

Saída: PNG em evaluation/model_analysis/graphs/
"""

from __future__ import annotations

import glob
import os
import re
from datetime import datetime
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))


def load_selection_metrics_from_comparison_txt() -> Dict[str, float]:
    path = os.path.join(
        repo_root(),
        "evaluation/model_comparison/results/comprehensive_model_comparison.txt",
    )
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()

    m = re.search(
        r"\|\s*TF-IDF\s*\+\s*Logistic\s*Regression\s*\|\s*Traditional\s*ML\s*\|"
        r"\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|",
        txt,
    )
    if not m:
        raise ValueError(
            "Não foi possível extrair a linha TF-IDF + Logistic Regression do "
            "comprehensive_model_comparison.txt"
        )

    return {
        "accuracy": float(m.group(1)),
        "f1_macro": float(m.group(2)),
        "precision_macro": float(m.group(3)),
    }


def find_latest_kaggle_metrics_csv(
    explicit_path: Optional[str] = None,
) -> str:
    if explicit_path:
        if not os.path.isfile(explicit_path):
            raise FileNotFoundError(explicit_path)
        return explicit_path

    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    pattern = os.path.join(
        results_dir,
        "metrics_tfidf_lr_amitzala_youtube-comments-with-labeled_*.csv",
    )
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(
            "Nenhum CSV de métricas Kaggle encontrado. Execute antes "
            "evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py "
            f"ou passe --metrics-csv. Procurado em: {pattern}"
        )
    return max(files, key=os.path.getmtime)


def load_kaggle_metrics_from_csv(csv_path: str) -> Dict[str, float]:
    df = pd.read_csv(csv_path)
    macro = df[df["class"] == "MACRO"].iloc[0]
    return {
        "accuracy": float(macro["accuracy_global"]),
        "precision_macro": float(macro["precision"]),
        "f1_macro": float(macro["f1_score"]),
    }


def plot_comparison(
    selection: Dict[str, float],
    kaggle: Dict[str, float],
    kaggle_csv_basename: str,
    output_png: str,
) -> None:
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["font.size"] = 13
    plt.rcParams["axes.labelsize"] = 14
    plt.rcParams["axes.titlesize"] = 15
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams["legend.fontsize"] = 11

    metric_labels_pt = ["Acurácia", "Precisão\n(macro)", "F1\n(macro)"]
    keys = ["accuracy", "precision_macro", "f1_macro"]

    sel_pct = [selection[k] * 100 for k in keys]
    kag_pct = [kaggle[k] * 100 for k in keys]

    x = np.arange(len(metric_labels_pt))
    width = 0.36

    fig, ax = plt.subplots(figsize=(12, 7))

    bars1 = ax.bar(
        x - width / 2,
        sel_pct,
        width,
        label="Seleção do modelo\n(comparação original)",
        color="#2196F3",
        edgecolor="black",
        linewidth=1.0,
        alpha=0.88,
    )
    bars2 = ax.bar(
        x + width / 2,
        kag_pct,
        width,
        label="Avaliação Kaggle\n(amitzala)",
        color="#FF9800",
        edgecolor="black",
        linewidth=1.0,
        alpha=0.88,
    )

    ax.set_xlabel("Métrica")
    ax.set_ylabel("Valor (%)")
    ax.set_title(
        "TF-IDF + Regressão Logística: seleção do modelo vs. avaliação em dataset externo",
        pad=14,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(metric_labels_pt)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", frameon=True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                h + 1.0,
                f"{h:.1f}%",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
            )

    note = (
        "Seleção: métricas da tabela em comprehensive_model_comparison.txt "
        "(TF-IDF+RL). Avaliação: inferência no CSV "
        f"{kaggle_csv_basename} (sem retreinamento)."
    )
    plt.figtext(
        0.5,
        0.02,
        note,
        ha="center",
        fontsize=9,
        style="italic",
        color="gray",
        wrap=True,
    )

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    plt.savefig(output_png, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    import argparse

    p = argparse.ArgumentParser(
        description="Gráfico: seleção do modelo vs. avaliação Kaggle amitzala."
    )
    p.add_argument(
        "--metrics-csv",
        type=str,
        default=None,
        help="CSV de métricas Kaggle (default: mais recente em results/)",
    )
    args = p.parse_args()

    selection = load_selection_metrics_from_comparison_txt()
    csv_path = find_latest_kaggle_metrics_csv(args.metrics_csv)
    kaggle = load_kaggle_metrics_from_csv(csv_path)

    graphs_dir = os.path.join(os.path.dirname(__file__), "..", "graphs")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_png = os.path.join(
        graphs_dir,
        f"tfidf_lr_selection_vs_kaggle_amitzala_{ts}.png",
    )

    plot_comparison(
        selection,
        kaggle,
        os.path.basename(csv_path),
        out_png,
    )

    print("Seleção (comprehensive_model_comparison.txt, TF-IDF + Logistic Regression):")
    for k, v in selection.items():
        print(f"  {k}: {v:.4f} ({v*100:.2f}%)")
    print(f"\nAvaliação Kaggle (de {os.path.basename(csv_path)}):")
    for k, v in kaggle.items():
        print(f"  {k}: {v:.4f} ({v*100:.2f}%)")
    print(f"\nGráfico salvo: {out_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
