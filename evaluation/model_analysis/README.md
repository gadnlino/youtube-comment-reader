# Saídas da análise do modelo

Esta pasta contém **resultados, gráficos, dados e relatórios** das execuções de avaliação do modelo.

**Scripts executáveis** foram movidos para a árvore canónica:

**`evaluation/scripts/01_model_evaluation/`** — ver [`../scripts/CATALOG.md`](../scripts/CATALOG.md)

Cópias arquivadas: [`../06_archived/2025-11_duplicate_scripts/model_analysis_scripts/`](../06_archived/2025-11_duplicate_scripts/model_analysis_scripts/)

## Estrutura

```
model_analysis/
├── data/              # JSON de entrada (working_videos, etc.)
├── results/           # Saídas JSON/CSV das análises
├── graphs/            # Visualizações PNG geradas
├── reports/           # Relatórios em texto
└── scripts/README.md  # Apenas redirecionamento
```

## Scripts principais (executar a partir de `evaluation/scripts/01_model_evaluation/`)

| Script | Saída |
|--------|-------|
| `compare_metrics_vs_benchmark.py` | `model_analysis/results/` |
| `validate_model_accuracy_with_dataset.py` | `model_analysis/results/` |
| `validate_model_distribution_multiple_sets.py` | `model_analysis/results/` |
| `evaluate_tfidf_logistic_on_youtube_comments_with_labeled.py` | `results/`, `graphs/` |
| `generate_confusion_matrix.py` | PNG (offline; matriz fixa) |
| `language_impact_analysis.py` | `results/`, `graphs/` |

## Dependências

`pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `requests`, `scipy`, `kagglehub` (alguns scripts)
