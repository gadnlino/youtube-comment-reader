# Saídas da análise do modelo — `model_analysis/`

Resultados, gráficos, dados e relatórios das execuções de avaliação do **Pilar 1 — Modelo**.

## Propósito

Destino das saídas dos scripts em [`../scripts/01_model_evaluation/`](../scripts/CATALOG.md). Não execute scripts duplicados em `scripts/` (redirect) — use a árvore canónica.

## Conteúdo

| Subpasta | Finalidade |
|----------|------------|
| `data/` | JSON de entrada (working_videos, etc.) |
| `results/` | CSV/JSON das análises |
| `graphs/` | PNG gerados (maioria arquivada se não estiver no docx) |
| `reports/` | Relatórios em texto |
| `scripts/README.md` | Redirect para `../scripts/` |

Documentos de apoio: `FINAL_MULTILINGUAL_EVALUATION_SUMMARY.md`, `LANGUAGE_ANALYSIS_GRAPHS_GUIDE.md`, `TABELA_COMPARACAO_METRICAS.md`.

## Como usar

```bash
cd evaluation/scripts/01_model_evaluation
python compare_metrics_vs_benchmark.py   # exemplo
pip install -r ../../requirements.txt    # na raiz: evaluation/requirements.txt
```

## Figuras da monografia

- **Figura 23:** [`../02_graphs/figures/`](../02_graphs/figures/)
- **Figura 24:** [`../02_graphs/figures/`](../02_graphs/figures/) via `plot_tfidf_lr_selection_vs_kaggle_amitzala.py`
- Outros PNG em `graphs/`: fora do keep-list docx — [`../02_graphs/MANIFEST.md`](../02_graphs/MANIFEST.md)

## Ver também

- [`../README.md`](../README.md) — índice da avaliação
- [`../06_archived/2025-11_duplicate_scripts/model_analysis_scripts/`](../06_archived/2025-11_duplicate_scripts/model_analysis_scripts/) — cópias antigas
